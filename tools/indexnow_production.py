"""Manual, explicit owner request only, after merged PR and successful production.

Normal build/CI never calls this. Preview deployments can never authorize it.
"""
import argparse
import json
from pathlib import Path
import re
import subprocess
import urllib.request
import xml.etree.ElementTree as ET

REPO = 'giantroisi/sottolineature'
SITE = 'https://sottolineature.it'


def need(value, message):
    if not value:
        raise ValueError(message)


def production_ok(sha, main, pulls, deployments, statuses):
    need(re.fullmatch('[a-f0-9]{40}', sha) and main == sha, 'Only current main can authorize IndexNow')
    need(any(p.get('merged_at') and p.get('merge_commit_sha') == sha and
             p.get('base', {}).get('ref') == 'main' for p in pulls), 'Merged main PR required')
    # Vercel's real GitHub Production deployments currently set the generic
    # production_environment flag to false; use its explicit environment label
    # and authenticated bot status, never the boolean alone.
    valid = [d for d in deployments if d.get('sha') == sha and
             d.get('environment', '').lower() == 'production' and
             d.get('creator', {}).get('login') == 'vercel[bot]']
    need(any(statuses.get(str(d['id']), []) and statuses[str(d['id'])][0].get('state') == 'success' and
             statuses[str(d['id'])][0].get('environment', '').lower() == 'production' and
             statuses[str(d['id'])][0].get('creator', {}).get('login') == 'vercel[bot]' for d in valid),
         'Successful Vercel production deployment required, never preview')


def selected_urls(root, values):
    need(isinstance(values, list) and 0 < len(values) <= 100 and all(isinstance(v, str) for v in values),
         'Explicit list of 1..100 sitemap URLs required')
    allowed = set()
    for path in Path(root).glob('sitemap*.xml'):
        tree = ET.parse(path)
        allowed.update(n.text for n in tree.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}url/{http://www.sitemaps.org/schemas/sitemap/0.9}loc'))
    need(len(values) == len(set(values)) and all(v in allowed and v.startswith(SITE + '/') for v in values),
         'URLs must be exact canonical sitemap entries; no arbitrary or preview URLs')
    return sorted(values)


def gh(path):
    return json.loads(subprocess.check_output(['gh', 'api', path]))


def main(root, commit, values, confirmed):
    need(confirmed, 'No notification without explicit manual confirmation')
    need(re.fullmatch('[a-f0-9]{40}', commit), 'Full production SHA required')
    need(subprocess.check_output(['git', '-C', str(root), 'rev-parse', 'HEAD']).decode().strip() == commit, 'Checkout mismatch')
    branch = gh('repos/' + REPO + '/branches/main')['commit']['sha']
    pulls = gh('repos/' + REPO + '/commits/' + commit + '/pulls?per_page=100')
    deployments = gh('repos/' + REPO + '/deployments?sha=' + commit + '&per_page=100')
    statuses = {str(d['id']): gh('repos/' + REPO + '/deployments/' + str(d['id']) + '/statuses?per_page=1')
                for d in deployments if d.get('environment', '').lower() == 'production'}
    production_ok(commit, branch, pulls, deployments, statuses)
    urls = selected_urls(root, values)
    keys = list(Path(root).glob('*.txt'))
    key = [p.stem for p in keys if re.fullmatch('[a-f0-9]{32}', p.stem) and p.read_text().strip() == p.stem]
    need(len(key) == 1, 'Existing public IndexNow verification key required')
    payload = json.dumps({'host': 'sottolineature.it', 'key': key[0],
                          'keyLocation': SITE + '/' + key[0] + '.txt', 'urlList': urls}).encode()
    # Recheck main immediately before the sole mutation; no automatic retries.
    need(gh('repos/' + REPO + '/branches/main')['commit']['sha'] == commit, 'Main changed; stop')
    request = urllib.request.Request('https://api.indexnow.org/indexnow', data=payload,
                                     headers={'Content-Type': 'application/json; charset=utf-8'}, method='POST')
    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, *args, **kwargs):
            return None
    with urllib.request.build_opener(NoRedirect).open(request, timeout=30) as response:
        need(response.status in (200, 202), 'IndexNow did not accept the explicit request')
    print(json.dumps({'production_sha': commit, 'explicit_urls_submitted': urls}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--production-sha', required=True)
    parser.add_argument('--urls-json', required=True)
    parser.add_argument('--confirm', action='store_true')
    args = parser.parse_args()
    try:
        main(args.root, args.production_sha, json.loads(args.urls_json), args.confirm)
    except (ValueError, KeyError, OSError, subprocess.SubprocessError) as error:
        parser.exit(1, 'INDEXNOW BLOCKED: ' + str(error) + '\n')
