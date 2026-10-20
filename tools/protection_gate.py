"""Proposta pubblica: gate Git fail-closed, nessuna baseline riscritta sul disco.

TRUSTED_STATE e' il commit indicato dal proprietario, NON un valore letto dal
manifest, dall'ambiente o da HEAD. Cambiarlo richiede una promozione separata.
L'approvazione viene letta solo da quel commit e copre i byte esatti del manifest.
"""
import hashlib
from html.parser import HTMLParser
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import tarfile
import tempfile
import xml.etree.ElementTree as ET

TRUSTED_STATE = 'ec9287e4c9038b53c93219168e77bcffbc4f215b'
SITE = 'https://sottolineature.it'
APPROVALS = 'protection/owner-approvals.json'
ENGINE = ('tools/protection_gate.py', 'tools/protection_worker.py', 'tools/build_protected.py',
          'tools/run_trusted_protection.py')
PROPOSAL_FILES = set(ENGINE) | {'tools/test_protection_gate.py', 'PROTEZIONE-LOTTI.md',
    'protection/manifests/noop-ec9287e4.json', 'protection/manifests/install-public-20261020.json',
    'protection/owner-approvals.example.json'}
DOCS = {'AGENTS.md', 'CATALOGO.md', 'CLAUDE.md', 'LOG.md', 'SEO.md', 'SEO-KEYWORDS.md',
        'SEO-CITA-QUESTA-FRASE.md', 'SEO-REDIRECT-2026-09-21.md', 'VALIDAZIONE.md',
        'VERIFICHE-FONTI.md', 'PROTEZIONE-LOTTI.md'}
BOUNDED = {'data/citazioni.json', 'data/opere.json', 'data/raccolte.json',
           'data/hub_intros.json', 'data/autori_foto.json', 'data/autori_sameas.json', 'tools/slugs.json'}
GLOBAL = {'data/affiliazioni.json', 'data/social_images.json', 'data/keywords.json',
          'vercel.json', 'robots.txt', '.gitignore', 'package.json', 'package-lock.json',
          'pnpm-lock.yaml', 'yarn.lock', 'pyproject.toml', 'requirements.txt', APPROVALS,
          'AGENTS.md', 'CLAUDE.md', 'CATALOGO.md', 'SEO.md', 'VALIDAZIONE.md', 'PROTEZIONE-LOTTI.md'}
ROOT_HTML = {'index.html', '404.html', 'metodo.html', 'privacy.html', 'affiliazioni.html',
             'note-legali.html', 'le-mie-sottolineature.html'}
SM = '{http://www.sitemaps.org/schemas/sitemap/0.9}'
IM = '{http://www.google.com/schemas/sitemap-image/1.1}'


class Rejected(ValueError):
    pass


def need(condition, message):
    if not condition:
        raise Rejected(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def git(root, *args, binary=False):
    p = subprocess.run(['git', '-C', str(root), *args], stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE, check=False)
    need(p.returncode == 0, 'Git/base non valida: ' + ' '.join(args[:2]))
    return p.stdout if binary else p.stdout.decode().strip()


def full_commit(root, value):
    need(isinstance(value, str) and re.fullmatch('[0-9a-f]{40}', value),
         'La base deve essere un full SHA di 40 caratteri')
    need(git(root, 'rev-parse', '--verify', value + '^{commit}') == value, 'Base non commit')
    git(root, 'merge-base', '--is-ancestor', value, 'HEAD')
    return value


def path_name(value):
    need(isinstance(value, str) and value and '\\' not in value, 'Percorso non valido')
    p = PurePosixPath(value)
    need(not p.is_absolute() and '..' not in p.parts and str(p) == value and
         not any(c in value for c in '*?[]\0'), 'Serve un percorso relativo esatto: ' + value)
    return value


def route(path):
    need(path.endswith('.html'), 'Percorso non HTML')
    return '/' + (path[:-10] if path.endswith('index.html') else path[:-5] + '/')


def page_kind(path):
    if path.endswith('/index.html') or path == 'index.html':
        return 'index'
    return {'citazioni': 'quotation', 'opere': 'work', 'autori': 'author',
            'raccolte': 'hub', 'temi': 'hub', 'generi': 'hub'}.get(path.split('/')[0], 'static')


def classification(path, trusted_paths):
    """Nessun fallback permissivo: ignoto resta ignoto, anche se dichiarato."""
    if path in GLOBAL or path in ENGINE or path == 'tools/test_protection_gate.py':
        return 'global'
    if path in BOUNDED:
        return 'source'
    if path in DOCS:
        return 'documentation'
    if path.startswith('protection/manifests/') and re.fullmatch(r'protection/manifests/[a-z0-9-]+\.json', path):
        return 'control'
    if path == 'protection/owner-approvals.example.json':
        return 'global'
    if path in ROOT_HTML or re.fullmatch(r'(citazioni|opere|autori|raccolte|temi|generi)/[a-z0-9-]+\.html', path) or re.fullmatch(r'citazioni/\d+/index\.html', path):
        return 'page'
    if path == 'feed.xml' or re.fullmatch(r'sitemap(?:-[a-z-]+)?\.xml', path):
        return 'derived-protected'
    if path == 'assets/social/manifest.json' or path == 'assets/home-resto.js':
        return 'derived'
    if re.fullmatch(r'assets/(covers|autori)/[a-zA-Z0-9_-]+\.(jpg|png|webp)', path):
        return 'asset'
    if re.fullmatch(r'assets/(og|social)/[a-z0-9-]+\.png', path):
        return 'derived'
    # Un vecchio file noto ma non editoriale e' una radice protetta, mai escluso.
    if path in trusted_paths:
        return 'global'
    return 'unknown'


def tree(root, commit):
    result = {}
    for record in git(root, 'ls-tree', '-rz', '--full-tree', commit, binary=True).split(b'\0'):
        if not record:
            continue
        meta, name = record.split(b'\t', 1)
        mode, kind, oid = meta.decode().split()
        need(kind == 'blob' and mode in {'100644', '100755'}, 'Git link/submodule non ammesso')
        result[name.decode()] = {'oid': oid, 'mode': mode}
    return result


def export(root, commit, destination):
    """Esporta solo blob Git fidati: non esegue file nuovi o cache del checkout."""
    destination = Path(destination)
    p = subprocess.Popen(['git', '-C', str(root), 'archive', commit], stdout=subprocess.PIPE)
    with tarfile.open(fileobj=p.stdout, mode='r|') as archive:
        for item in archive:
            name = path_name(item.name.rstrip('/'))
            target = destination / name
            if item.isdir():
                target.mkdir(parents=True, exist_ok=True)
            else:
                need(item.isfile(), 'Tipo archivio non ammesso')
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(archive.extractfile(item).read())
                target.chmod(0o755 if item.mode & 0o111 else 0o644)
                os.utime(target, (item.mtime, item.mtime))
    p.stdout.close()
    need(p.wait() == 0, 'Export Git fallito')


def filesystem(root):
    result = {}
    for directory, dirs, files in os.walk(root):
        # Solo cache/runtime non eseguiti dal runner, e rapporti non pubblicabili.
        dirs[:] = sorted(d for d in dirs if d not in {'.git', 'archivio', '__pycache__',
                          '.vercel', '.netlify', 'node_modules'} and
                         not (Path(directory).relative_to(root).as_posix() == 'assets' and d == 'fonts'))
        for d in dirs:
            need(not (Path(directory) / d).is_symlink(), 'Directory simbolica vietata')
        for name in sorted(files):
            if name == '.DS_Store' or (Path(directory) == Path(root) and name == '.git'):
                continue
            p = Path(directory) / name
            need(not p.is_symlink(), 'File simbolico vietato')
            data = p.read_bytes()
            result[p.relative_to(root).as_posix()] = {
                'oid': hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest(),
                'mode': '100755' if p.stat().st_mode & 0o111 else '100644', 'sha256': sha(data)}
    return result


def changed(before, after):
    return {kind: sorted(paths) for kind, paths in {
        'new': set(after) - set(before), 'removed': set(before) - set(after),
        'modified': {p for p in before.keys() & after.keys() if
                     any(before[p][k] != after[p][k] for k in ('oid', 'mode'))}}.items()}


def _walk_dates(obj, field):
    if isinstance(obj, list):
        return sum((_walk_dates(x, field) for x in obj), [])
    if not isinstance(obj, dict):
        return []
    own = [[obj.get('@id', obj.get('@type', '')), obj[field]]] if field in obj else []
    return own + sum((_walk_dates(x, field) for x in obj.values()), [])


class Page(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.canonical, self.robots, self.dates, self.text, self.resources = [], [], {}, [], []
        self.hidden = 0
        self.feed(source)
        self.graphs = [json.loads(x) for x in re.findall(r'<script\b[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', source, re.S | re.I)]
        self.published = _walk_dates(self.graphs, 'datePublished') + self.dates.get('published', [])
        self.modified = _walk_dates(self.graphs, 'dateModified') + self.dates.get('modified', [])
        sections = re.findall(r'<div class="related sans"><h2>(Altre citazioni (?:di|su) [^<]+)</h2><ul>(.*?)</ul></div>', source, re.S)
        self.related = {('author' if title.startswith('Altre citazioni di ') else 'theme'):
                        re.findall(r'href="/citazioni/([^/]+)/"', body) for title, body in sections}
        self.related = {k: self.related.get(k, []) for k in ('author', 'theme')}
        self.affiliate = re.findall(r'<aside class="affiliate-card sans".*?</aside>|<a class="affiliate-link".*?</a>|<p class="affiliate-disclosure">.*?</p>', source, re.S)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in {'script', 'style'}:
            self.hidden += 1
        if tag == 'link' and 'canonical' in a.get('rel', '').lower().split():
            self.canonical.append(a.get('href'))
        if tag == 'meta':
            name = a.get('name', a.get('property', a.get('itemprop', a.get('http-equiv', '')))).lower()
            if name in {'robots', 'googlebot', 'x-robots-tag'}:
                self.robots.append([name, a.get('content')])
            if name in {'datepublished', 'article:published_time', 'datemodified', 'article:modified_time'}:
                field = 'modified' if 'modified' in name else 'published'
                self.dates.setdefault(field, []).append([name, a.get('content')])
            if name in {'og:image', 'twitter:image'} and a.get('content'):
                self.resources.append({'src': a['content']})
        if tag in {'a', 'img'}:
            self.resources.append({k: a[k] for k in ('href', 'src', 'alt') if k in a})

    def handle_endtag(self, tag):
        if tag in {'script', 'style'}:
            self.hidden = max(0, self.hidden - 1)

    def handle_data(self, text):
        if not self.hidden and text.strip():
            self.text.append(' '.join(text.split()))

    def metadata(self):
        return {'canonical': self.canonical, 'robots': self.robots,
                'published': self.published, 'modified': self.modified, 'related': self.related}

    def content(self):
        return {'text': self.text, 'resources': self.resources}


def site_state(root):
    pages, maps, consumers = {}, {}, {}
    for path in Path(root).rglob('*.html'):
        p = path.relative_to(root).as_posix()
        if p.startswith(('tools/', 'templates/', 'archivio/')):
            continue
        page = Page(path.read_text())
        pages[p] = page
        for asset in page.resources:
            src = asset.get('src', '').removeprefix(SITE).split('?')[0]
            if src.startswith('/assets/'):
                consumers.setdefault(src[1:], set()).add(SITE + route(p))
    for path in Path(root).glob('sitemap*.xml'):
        for item in ET.fromstring(path.read_bytes()).findall(SM + 'url'):
            url = item.findtext(SM + 'loc')
            need(url not in maps, 'URL sitemap duplicato')
            maps[url] = {'lastmod': item.findtext(SM + 'lastmod'),
                         'images': [x.text for x in item.findall(IM + 'image/' + IM + 'loc')]}
    return pages, maps, consumers


def json_file(root, path, default=None):
    p = Path(root) / path
    return json.loads(p.read_text()) if p.exists() else default


def seo_check(before_root, after_root, manifest):
    a, sm_a, consumers_a = site_state(before_root)
    b, sm_b, consumers_b = site_state(after_root)
    spec = manifest['seo']
    expected_fields = {'canonical', 'robots', 'modified', 'lastmod', 'sitemap_images', 'sitemap_added', 'sitemap_removed'}
    need(set(spec) == expected_fields, 'Schema SEO non valido')
    both = a.keys() & b.keys()
    for p in both:
        need(a[p].published == b[p].published, 'datePublished immutabile: ' + p)
        need(a[p].related == b[p].related, 'Correlati collaterali: ' + p)
        if manifest['change_class'] != 'global-structural':
            need(a[p].affiliate == b[p].affiliate, 'Amazon richiede lotto globale: ' + p)
    for field in ('canonical', 'robots', 'modified'):
        delta = {SITE + route(p): {'before': getattr(a[p], field), 'after': getattr(b[p], field)}
                 for p in both if getattr(a[p], field) != getattr(b[p], field)}
        need(delta == spec[field], 'Cambio SEO non dichiarato: ' + field)
        if field == 'modified':
            for p in both:
                if a[p].modified != b[p].modified:
                    need(a[p].content() != b[p].content(), 'Sola dateModified senza contenuto: ' + p)
    touched = set(manifest['pages']['new']) | set(manifest['pages']['modified'])
    for p in touched:
        need(p in b and (p == '404.html' or b[p].canonical == [SITE + route(p)]), 'Canonical incoerente: ' + p)
    need(sorted(set(sm_b) - set(sm_a)) == spec['sitemap_added'], 'Inventario sitemap aggiunto non dichiarato')
    need(sorted(set(sm_a) - set(sm_b)) == spec['sitemap_removed'], 'Inventario sitemap rimosso non dichiarato')
    for url in sm_a.keys() ^ sm_b.keys():
        need(url in {SITE + route(p) for p in touched}, 'URL sitemap senza pagina dichiarata')
    for field, key in (('lastmod', 'lastmod'), ('images', 'sitemap_images')):
        delta = {u: {'before': sm_a[u][field], 'after': sm_b[u][field]}
                 for u in sm_a.keys() & sm_b.keys() if sm_a[u][field] != sm_b[u][field]}
        need(delta == spec[key], 'Sitemap ' + key + ' non dichiarata')
        for url in delta:
            matches = [p for p in touched if SITE + route(p) == url]
            need(matches and all(p not in a or a[p].content() != b[p].content() for p in matches),
                 'Sitemap/data senza modifica reale della pagina: ' + url)
    slugs_a, slugs_b = json_file(before_root, 'tools/slugs.json', {}), json_file(after_root, 'tools/slugs.json', {})
    for group, values in slugs_a.items():
        for key, value in values.items():
            current = slugs_b.get(group, {})
            # CLAUDE.md richiede di rinominare la chiave di un refuso conservando
            # il medesimo slug; non si impone una nuova URL per far passare il gate.
            same_quote_slug = group == 'quotes' and key not in current and list(current.values()).count(value) == 1
            need(current.get(key) == value or same_quote_slug, 'Slug/alias congelato alterato')
    def published(root, slugs):
        return {slugs.get('quotes', {}).get(q['author'] + '|' + q['title'] + '|' + ' '.join(q['quote'].split()[:6])): q.get('added')
                for q in json_file(root, 'data/citazioni.json', [])}
    old, new = published(before_root, slugs_a), published(after_root, slugs_b)
    for key, value in old.items():
        need(key is not None and new.get(key) == value, 'Prima pubblicazione citazione alterata')
    actual_consumers = {}
    for path in manifest['derived']:
        if path.startswith('assets/') and Path(path).suffix.lower() in {'.jpg', '.png', '.webp'}:
            actual_consumers[path] = sorted(consumers_a.get(path, set()) | consumers_b.get(path, set()))
    need(actual_consumers == manifest['asset_consumers'], 'Consumatori asset non dichiarati esattamente')
    return {'html': len(b), 'sitemap_urls': len(sm_b),
            'affiliate_card_pages': sum(bool(re.search(r'<aside class="affiliate-card sans"',
                (Path(after_root) / p).read_text())) for p in b),
            'amazon_buttons': sum((Path(after_root) / p).read_text().count('class="affiliate-link"') for p in b)}


class Gate:
    def __init__(self, root, *, trusted_state=TRUSTED_STATE):
        # trusted_state e' dipendenza del launcher fidato/test, MAI un campo del lotto.
        self.root = Path(root).resolve()
        self.trusted = full_commit(self.root, trusted_state)
        self.trusted_tree = tree(self.root, self.trusted)

    def authority(self):
        if APPROVALS not in self.trusted_tree:
            return {'version': 1, 'baselines': [self.trusted], 'approvals': []}
        record = json.loads(git(self.root, 'show', self.trusted + ':' + APPROVALS))
        need(set(record) == {'version', 'baselines', 'approvals'} and record['version'] == 1,
             'Stato fidato approvazioni non valido')
        return record

    def plan(self, base, manifest_path=None, *, phase='final', observed_root=None):
        need(not any(k.startswith(('SEO_EXPECTED_', 'SEO_APPROVE_', 'SEO_IMPACT_')) for k in os.environ),
             'Deroga ambiente vietata')
        self.base = full_commit(self.root, base)
        git(self.root, 'merge-base', '--is-ancestor', self.base, self.trusted)
        need(self.base in self.authority()['baselines'], 'Baseline non promossa dal proprietario nello stato fidato')
        self.base_tree = tree(self.root, self.base)
        observed_root = Path(observed_root or self.root)
        current = filesystem(observed_root)
        for p in current:
            need(classification(p, self.trusted_tree) != 'unknown', 'File sconosciuto: ' + p)
        # Il registro di autorita' e i manifest gia' fidati NON si modificano nel lotto.
        fixed_controls = {p for p in self.trusted_tree if p == APPROVALS or p.startswith('protection/manifests/')}
        for p in fixed_controls:
            need(p in current and all(current[p][k] == self.trusted_tree[p][k] for k in ('oid', 'mode')),
                 'Auto-approvazione/radice fidata modificata: ' + p)
        need(APPROVALS in self.trusted_tree or APPROVALS not in current,
             'Auto-approvazione nello stesso lotto vietata')
        baseline = {p: v for p, v in self.base_tree.items() if p not in fixed_controls}
        compare = {p: v for p, v in current.items() if p not in fixed_controls}
        selected = None
        if manifest_path:
            selected = path_name(Path(manifest_path).as_posix())
            need(re.fullmatch(r'protection/manifests/[a-z0-9-]+\.json', selected), 'Percorso manifest non ammesso')
            need(selected in current, 'Manifest mancante')
            raw = (self.root / selected).read_bytes()
            m = json.loads(raw)
            need(set(m) == {'version', 'id', 'base', 'change_class', 'sources', 'pages', 'derived',
                           'global_components', 'seo', 'asset_consumers'}, 'Schema manifest/auto-approvazione non ammesso')
            need(m['version'] == 1 and m['base'] == self.base and isinstance(m['id'], str) and m['id'], 'Identita/base del manifest non valida')
            need(m['change_class'] in {'none', 'editorial-bounded', 'global-structural'}, 'change_class sconosciuta')
            approval = [x for x in self.authority()['approvals'] if x.get('manifest_sha256') == sha(raw)
                        and x.get('manifest_path') == selected and x.get('base') == self.base
                        and x.get('change_class') == m['change_class'] and x.get('evidence')]
            need(m['change_class'] == 'none' or len(approval) == 1,
                 'Manca approvazione PRECEDENTE legata al digest esatto del manifest')
            compare.pop(selected, None)
            baseline.pop(selected, None)
        else:
            m = empty_manifest(self.base)
        delta = changed(baseline, compare)
        need(not delta['removed'], 'Rimozioni vietate: serve lotto separato')
        if m['change_class'] == 'none':
            need(not any(delta.values()), 'none ammesso soltanto a checkout e baseline invariati')
            need(not m['sources'] and not m['derived'] and m['pages'] == {'new': {}, 'modified': {}}
                 and not m['global_components'] and not m['asset_consumers'] and m['seo'] == empty_seo(),
                 'none non autorizza cambiamenti')
        expected = self.contracts(m)
        actual = set(delta['new'] + delta['modified'])
        need(actual <= set(expected) and (phase == 'inputs' or actual == set(expected)), 'Impatto non esatto: extra=' + str(sorted(actual - set(expected))) +
             '; dichiarati non cambiati=' + str(sorted(set(expected) - actual)))
        for p, values in expected.items():
            need(p != APPROVALS and p not in fixed_controls, 'Radice approvazioni non modificabile dal lotto')
            before = sha(git(self.root, 'show', self.base + ':' + p, binary=True)) if p in self.base_tree else None
            need(values['before'] == before and isinstance(values['after'], str) and re.fullmatch('[0-9a-f]{64}', values['after']), 'Digest contratto non valido: ' + p)
            if p in actual:
                need(values['after'] == current[p]['sha256'], 'Digest sorgente/output non esatto: ' + p)
                need(current[p]['mode'] == self.base_tree.get(p, {'mode': '100644'})['mode'],
                     'Cambio permessi non autorizzabile implicitamente: ' + p)
        actual_globals = sorted(p for p in actual if classification(p, self.trusted_tree) in {'global', 'control'})
        need(actual_globals == m['global_components'], 'Componenti globali non dichiarati esattamente')
        need(not actual_globals or m['change_class'] == 'global-structural', 'Amazon/codice/config: serve approvazione globale precedente')
        page_paths = set(m['pages']['new']) | set(m['pages']['modified'])
        impacted_urls = {SITE + route(p) for p in page_paths}
        need(isinstance(m['asset_consumers'], dict), 'Mappa consumatori asset non valida')
        for values in m['asset_consumers'].values():
            need(isinstance(values, list) and all(isinstance(x, str) for x in values), 'Elenco consumatori asset non valido')
            impacted_urls.update(values)
        if m['change_class'] != 'global-structural':
            need(len(impacted_urls) <= max(1, min(25, int(sum(classification(p, self.trusted_tree) == 'page' for p in self.base_tree) * .05))), 'Budget numerico superato')
        return {'manifest': m, 'delta': delta, 'snapshot': current, 'authority': self.trusted,
                'baseline': self.base, 'approved': m['change_class'] != 'none', 'global': bool(actual_globals)}

    def contracts(self, m):
        need(set(m['pages']) == {'new', 'modified'}, 'Schema pagine incompleto')
        result = {}
        for category in ('sources', 'derived'):
            need(isinstance(m[category], dict), 'Elenco file deve essere una mappa esatta')
            for p, values in m[category].items():
                path_name(p)
                kind = classification(p, self.trusted_tree)
                allowed = {'source', 'documentation', 'global'} if category == 'sources' else {'derived', 'derived-protected', 'asset'}
                if category == 'sources' and m['change_class'] == 'global-structural':
                    allowed.add('control')  # altro manifest: solo globale con digest gia' approvato
                need(kind in allowed and set(values) == {'before', 'after'}, 'Classificazione file errata/sconosciuta: ' + p)
                need(p not in result, 'File duplicato')
                result[p] = values
        for status, pages in m['pages'].items():
            need(isinstance(pages, dict), 'Pagine devono essere una mappa esatta')
            for p, values in pages.items():
                path_name(p)
                need(classification(p, self.trusted_tree) == 'page' and
                     set(values) == {'url', 'kind', 'before', 'after'} and values['url'] == SITE + route(p)
                     and values['kind'] == page_kind(p), 'URL/file/tipo pagina non valido')
                need((p in self.base_tree) == (status == 'modified'), 'Pagina nuova/modificata classificata male')
                need(p not in result, 'File duplicato')
                result[p] = {k: values[k] for k in ('before', 'after')}
        return result

    def trusted_engine(self):
        for p in ENGINE:
            need(p in self.trusted_tree, 'Bootstrap non approvato: il gate non esiste ancora nel commit fidato')
            need(sha((self.root / p).read_bytes()) == sha(git(self.root, 'show', self.trusted + ':' + p, binary=True)),
                 'Il codice del gate non puo\' giudicare la propria modifica: eseguire dal commit fidato')

    def verify(self, base, manifest_path=None):
        plan = self.plan(base, manifest_path)
        with tempfile.TemporaryDirectory(prefix='sottolineature-trusted-') as tmp:
            export(self.root, self.base, tmp)
            plan['counts'] = seo_check(tmp, self.root, plan['manifest'])
        return plan


def empty_seo():
    return {'canonical': {}, 'robots': {}, 'modified': {}, 'lastmod': {}, 'sitemap_images': {},
            'sitemap_added': [], 'sitemap_removed': []}


def empty_manifest(base):
    return {'version': 1, 'id': 'verifica-senza-modifiche', 'base': base, 'change_class': 'none',
            'sources': {}, 'pages': {'new': {}, 'modified': {}}, 'derived': {},
            'global_components': [], 'seo': empty_seo(), 'asset_consumers': {}}
