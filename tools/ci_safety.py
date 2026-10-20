#!/usr/bin/env python3
"""PR safety gate: exact impact, immutable initial dates, two disposable builds.

No signing key, App, deployment or indexing requests. GitHub branch protection
is the enforcement boundary; this is accidental-change protection, not a defence
against a repository administrator deliberately replacing the workflow.
"""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

MANIFEST = 'protection/change-manifest.json'
MAX_FILES, MAX_HTML = 25, 5
BOOTSTRAP_BASE = '29010e3e2b7c68f1a4f13bd11a55e961bd3054dc'
BOOTSTRAP_FILES = {
    '.github/workflows/seo-safety.yml', '.github/workflows/indexnow.yml',
    'tools/ci_safety.py', 'tools/test_ci_safety.py', 'tools/ci-requirements.txt',
    'tools/indexnow_production.py', 'tools/test_indexnow_production.py',
    'PROTEZIONE-PR.md', 'CLAUDE.md', 'LOG.md'}


def need(value, message):
    if not value:
        raise ValueError(message)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()


def sha(value):
    return hashlib.sha256(value).hexdigest()


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def owner_override(comments, head, impact):
    # CLI flags, labels, a manifest field or an agent-created file are NOT approval.
    if comments and isinstance(comments[0], list):
        comments = [comment for page in comments for comment in page]
    for comment in comments:
        if (comment.get('user', {}).get('login') != 'giantroisi' or
                comment.get('user', {}).get('type') != 'User' or
                comment.get('author_association') != 'OWNER'):
            continue
        body = comment.get('body', '')
        match = re.fullmatch(r'/seo-override ([a-f0-9]{40}) ([a-f0-9]{64}) ([^\r\n]{10,500})\s*', body)
        if match and match[1] == head and match[2] == impact:
            return {'comment_id': comment['id'], 'url': comment['html_url'],
                    'reason': match[3], 'created_at': comment.get('created_at')}
    return None


def scope(g, before, after):
    a, b = g.filesystem(before), g.filesystem(after)
    delta = g.changed(a, b)
    names = sorted(set(sum(delta.values(), [])) - {MANIFEST})
    files = {p: {'before': a.get(p, {}).get('sha256'), 'after': b.get(p, {}).get('sha256'),
                 'before_mode': a.get(p, {}).get('mode'), 'after_mode': b.get(p, {}).get('mode')}
             for p in names}
    return delta, files


def manifest_check(after, base, files):
    path = Path(after) / MANIFEST
    need(path.is_file(), 'Exact change manifest required for page/sitemap changes')
    data = json.loads(path.read_bytes())
    need(set(data) == {'version', 'base', 'reason', 'files'} and data['version'] == 1 and
         data['base'] == base and isinstance(data['reason'], str) and data['reason'].strip(),
         'Invalid exact change manifest')
    need(data['files'] == files, 'Manifest differs from exact files/hashes/modes (extra or missing)')


def protected_code(name):
    return (name.startswith(('.github/', 'templates/')) or name == 'vercel.json' or
            name.startswith('tools/') and not Path(name).name.startswith('test_') and
            name not in {'tools/slugs.json', 'tools/redirects.json'})


def evaluate(g, before, after, base, head, comments=()):
    delta, files = scope(g, before, after)
    a, sm_a, _ = g.site_state(before)
    b, sm_b, _ = g.site_state(after)
    pages = sorted(p for p in files if p in a or p in b)
    impact = sha(canonical({'base': base, 'head': head, 'files': files}))
    hard, findings = [], []
    if len(files) > MAX_FILES:
        findings.append('file budget exceeded: ' + str(len(files)))
    if len(pages) > MAX_HTML:
        findings.append('page budget exceeded: ' + str(len(pages)))
    if set(a) - set(b):
        hard.append('Removing published pages is not an ordinary PR operation')
    both = set(a) & set(b)
    for path in sorted(both):
        if a[path].published != b[path].published:
            hard.append('datePublished immutable: ' + path)
        if a[path].modified != b[path].modified and a[path].content() == b[path].content():
            hard.append('dateModified without real content change: ' + path)
        for field in ('canonical', 'robots', 'affiliate', 'related'):
            if getattr(a[path], field) != getattr(b[path], field):
                findings.append(field + ' changed: ' + path)
    for path in pages:
        if path in b and path != '404.html' and b[path].canonical != [g.SITE + g.route(path)]:
            hard.append('Canonical inconsistent with published URL: ' + path)
    if set(sm_a) != set(sm_b):
        findings.append('sitemap URL inventory changed')
    for url in sorted(set(sm_a) & set(sm_b)):
        if sm_a[url]['images'] != sm_b[url]['images']:
            findings.append('sitemap image inventory changed: ' + url)
        if sm_a[url]['lastmod'] != sm_b[url]['lastmod']:
            matches = [p for p in pages if g.SITE + g.route(p) == url]
            if not matches or any(p in a and a[p].content() == b[p].content() for p in matches):
                hard.append('lastmod without real page content change: ' + url)
    for name in ('robots.txt', 'vercel.json'):
        if name in files:
            findings.append('robots/redirect/hosting configuration changed: ' + name)
    old_slugs = g.json_file(before, 'tools/slugs.json', {})
    new_slugs = g.json_file(after, 'tools/slugs.json', {})
    for group, values in old_slugs.items():
        current = new_slugs.get(group, {})
        for key, value in values.items():
            if current.get(key) != value and not (group == 'quotes' and key not in current and list(current.values()).count(value) == 1):
                hard.append('Published slug changed: ' + group + '/' + key)
    def first_dates(root, slugs):
        return {slugs.get('quotes', {}).get(q['author'] + '|' + q['title'] + '|' + ' '.join(q['quote'].split()[:6])): q.get('added')
                for q in g.json_file(root, 'data/citazioni.json', [])}
    old_dates, new_dates = first_dates(before, old_slugs), first_dates(after, new_slugs)
    for key, value in old_dates.items():
        if key is None or key not in new_dates or new_dates[key] != value:
            hard.append('Original added date/quotation identity changed: ' + str(key))
    bootstrap = base == BOOTSTRAP_BASE and not (Path(before) / 'tools/ci_safety.py').exists() and set(files) <= BOOTSTRAP_FILES
    if not bootstrap:
        findings.extend('shared executable/control changed: ' + p for p in files if protected_code(p))
    needs_manifest = bool(pages or any(re.fullmatch(r'sitemap(?:-[a-z-]+)?\.xml', p) for p in files))
    if needs_manifest or (Path(after) / MANIFEST).exists():
        try:
            manifest_check(after, base, files)
        except (ValueError, KeyError, TypeError, OSError) as error:
            hard.append(str(error))
    approval = owner_override(list(comments), head, impact)
    result = {'base': base, 'head': head, 'impact_sha256': impact, 'files': files,
              'changed_pages': pages, 'before': {'html': len(a), 'sitemap_urls': len(sm_a)},
              'after': {'html': len(b), 'sitemap_urls': len(sm_b)},
              'hard_errors': hard, 'findings': findings, 'owner_override': approval,
              'bootstrap_technical_only': bootstrap,
              'allowed': not hard and (not findings or approval is not None)}
    return result


def run(root, base, head, comments, report, builds=True):
    root = Path(root).resolve()
    need(not Path(report).resolve().is_relative_to(root), 'Report outside checkout required')
    need(re.fullmatch('[a-f0-9]{40}', base) and re.fullmatch('[a-f0-9]{40}', head), 'Full SHAs required')
    def git(*args):
        return subprocess.check_output(['git', '-C', str(root), *args])
    need(git('rev-parse', 'HEAD').decode().strip() == head, 'Head differs from checked-out candidate')
    git('merge-base', '--is-ancestor', base, head)
    with tempfile.TemporaryDirectory(prefix='sottolineature-pr-safety-') as directory:
        tmp = Path(directory)
        # Reuse the already published stdlib snapshot/export/parser, always from base.
        for name in ('protection_gate.py', 'protection_worker.py', 'build_protected.py'):
            (tmp / name).write_bytes(git('show', base + ':tools/' + name))
        g = load('base_protection_gate', tmp / 'protection_gate.py')
        original = g.filesystem(root)
        need(not any(g.changed(g.tree(root, head), original).values()), 'Dirty/extra checkout files')
        before = tmp / 'before'
        g.export(root, base, before)
        result = evaluate(g, before, root, base, head, comments)
        Path(report).write_bytes(canonical(result) + b'\n')
        print(json.dumps({'impact_sha256': result['impact_sha256'], 'hard_errors': result['hard_errors'],
                          'findings': result['findings'], 'owner_override': result['owner_override']}, ensure_ascii=False))
        need(result['allowed'], 'PR BLOCKED; see exact impact/report. No automatic approval.')
        need(builds, 'Builds cannot be skipped in CI')
        previous = sys.modules.get('protection_gate')
        sys.modules['protection_gate'] = g
        try:
            builder = load('base_protected_build', tmp / 'build_protected.py')
            ref = tmp / 'reference.json'
            ref.write_bytes(canonical(builder.reference(before)))
            runs = []
            for number in (1, 2):
                stage = tmp / ('build-' + str(number))
                g.export(root, head, stage)
                builder.run_worker(stage, ref, tmp / 'protection_worker.py', tmp / ('build-' + str(number) + '.log'))
                diff = g.changed(original, g.filesystem(stage))
                need(not any(diff.values()), 'Build creates undeclared/different artifacts: ' + str(diff))
                runs.append({'run': number, 'file_delta': diff})
            # Tests need historical Git blobs, so run in a separate local clone.
            tests = tmp / 'tests'
            subprocess.run(['git', '-c', 'core.hooksPath=/dev/null', 'clone', '--shared', '--no-checkout', str(root), str(tests)], check=True, capture_output=True)
            g.export(root, head, tests)
            tested = subprocess.run([sys.executable, '-m', 'unittest', 'discover', '-s', 'tools', '-p', 'test_*.py'],
                                    cwd=tests, capture_output=True, text=True, timeout=600,
                                    env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'})
            need(tested.returncode == 0, 'Unit tests failed: ' + (tested.stdout + tested.stderr)[-3000:])
            need(not any(g.changed(original, g.filesystem(tests)).values()), 'Tests changed site artifacts')
            need(g.filesystem(root) == original, 'Concurrent file changes detected')
            result.update(builds=runs, tests_passed=True, verified=True, applied=False, submitted_urls=[])
            Path(report).write_bytes(canonical(result) + b'\n')
            return result
        finally:
            if previous is None:
                sys.modules.pop('protection_gate', None)
            else:
                sys.modules['protection_gate'] = previous


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--base', required=True)
    parser.add_argument('--head', required=True)
    parser.add_argument('--comments', type=Path, required=True)
    parser.add_argument('--report', type=Path, required=True)
    args = parser.parse_args()
    try:
        output = run(args.root, args.base, args.head, json.loads(args.comments.read_bytes()), args.report)
        print(json.dumps({'verified': output['verified'], 'builds': len(output['builds']), 'tests_passed': True}))
    except (ValueError, KeyError, TypeError, OSError, subprocess.SubprocessError) as error:
        parser.exit(1, 'SEO SAFETY: ' + str(error) + '\n')
