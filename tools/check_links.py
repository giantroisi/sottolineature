#!/usr/bin/env python3
"""Controllo di integrita' del sito generato: link interni, canonical, title e
descrizioni duplicate, pagine orfane, coerenza con la sitemap.

Nasce dopo il 2026-08-30, quando si e' scoperto che 35 link su 353 puntavano a
una 404: un errore in un generatore si moltiplica per centinaia di pagine e non
lo vede nessuno. Questo script percorre tutto il sito come farebbe un crawler,
ma leggendo i file, quindi funziona anche senza rete.

Uso: python3 tools/check_links.py   (esce con codice 1 se trova qualcosa)
"""
import collections
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {'.git', '.vercel', '.netlify', 'node_modules', 'archivio', 'tools',
             'templates', '__pycache__', '.claude', 'assets'}

HREF = re.compile(r'(?:href|src)="([^"]+)"')
TITLE = re.compile(r'<title>(.*?)</title>', re.S)
DESC = re.compile(r'<meta name="description" content="(.*?)"', re.S)
CANON = re.compile(r'<link rel="canonical" href="([^"]+)"')
ROBOTS = re.compile(r'<meta name="robots" content="([^"]+)"')


def html_files():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            if fn.endswith('.html'):
                yield os.path.join(dirpath, fn)


def as_url(path):
    """percorso del file -> URL pubblico, con cleanUrls e trailingSlash."""
    rel = os.path.relpath(path, ROOT).replace(os.sep, '/')
    if rel == 'index.html':
        return '/'
    if rel.endswith('/index.html'):
        return '/' + rel[:-len('index.html')]
    return '/' + rel[:-len('.html')] + '/'


def resolve(link, base_dir=None):
    """URL interno -> percorso del file che lo serve, o None se non esiste."""
    link = link.split('#')[0].split('?')[0]
    if not link or link.startswith(('mailto:', 'tel:', 'data:', 'javascript:')):
        return True
    if link.startswith('//') or link.startswith('http'):
        return True
    if not link.startswith('/'):
        if base_dir is None:
            return None
        full = os.path.normpath(os.path.join(base_dir, link))
        return full if os.path.isfile(full) else None
    p = link.lstrip('/')
    if p == '' :
        p = 'index.html'
    candidates = [p, p.rstrip('/') + '.html', os.path.join(p, 'index.html')]
    for c in candidates:
        full = os.path.join(ROOT, c)
        if os.path.isfile(full):
            return full
    return None


def main():
    pages = sorted(html_files())
    titles, descs, canons = collections.defaultdict(list), collections.defaultdict(list), {}
    broken, relative, insecure = [], [], []
    linked = set()
    noindex = set()

    for path in pages:
        with open(path, encoding='utf-8') as f:
            html = f.read()
        url = as_url(path)
        # gli script contengono stringhe che somigliano a href ma non lo sono
        scan = re.sub(r'<script\b.*?</script>', '', html, flags=re.S | re.I)
        m = ROBOTS.search(html)
        if m and 'noindex' in m.group(1):
            noindex.add(url)
        m = TITLE.search(html)
        if m:
            titles[m.group(1).strip()].append(url)
        m = DESC.search(html)
        if m:
            descs[m.group(1).strip()].append(url)
        m = CANON.search(html)
        if m:
            canons[url] = m.group(1)
        for link in HREF.findall(scan):
            if link.startswith('http://'):
                insecure.append((url, link))
            target = resolve(link, os.path.dirname(path))
            if target is None:
                broken.append((url, link))
            elif target is not True and not link.startswith('/'):
                relative.append((url, link))
                linked.add(as_url(target)) if target.endswith('.html') else None
            elif target is not True:
                linked.add(as_url(target))

    problems = 0
    print('Pagine esaminate:', len(pages))

    if broken:
        problems += len(broken)
        print('\nLINK ROTTI:', len(broken))
        for src, link in broken[:20]:
            print('  ', src, '->', link)
    if relative:
        problems += len(relative)
        print('\nLINK RELATIVI (risolvono, ma si rompono se la pagina cambia cartella):', len(relative))
        for src, link in relative[:10]:
            print('  ', src, '->', link)
    if insecure:
        problems += len(insecure)
        print('\nLINK IN HTTP (non cifrati):', len(insecure))
        for src, link in insecure[:10]:
            print('  ', src, '->', link)

    dup_t = {t: u for t, u in titles.items() if len(u) > 1}
    dup_d = {d: u for d, u in descs.items() if len(u) > 1}
    if dup_t:
        problems += len(dup_t)
        print('\nTITLE DUPLICATI:', len(dup_t))
        for t, urls in list(dup_t.items())[:10]:
            print('  ', t[:70], '->', len(urls), 'pagine:', ', '.join(urls[:3]))
    if dup_d:
        problems += len(dup_d)
        print('\nDESCRIPTION DUPLICATE:', len(dup_d))
        for d, urls in list(dup_d.items())[:10]:
            print('  ', d[:70], '->', len(urls), 'pagine:', ', '.join(urls[:3]))

    bad_canon = []
    for url, canon in canons.items():
        expected = 'https://sottolineature.it' + url
        if canon != expected:
            bad_canon.append((url, canon))
    if bad_canon:
        problems += len(bad_canon)
        print('\nCANONICAL INCOERENTI:', len(bad_canon))
        for url, canon in bad_canon[:10]:
            print('  ', url, '-> dichiara', canon)

    orphans = [as_url(p) for p in pages
               if as_url(p) not in linked and as_url(p) != '/' and as_url(p) not in noindex]
    if orphans:
        problems += len(orphans)
        print('\nPAGINE ORFANE (nessun link interno ci arriva):', len(orphans))
        for u in orphans[:15]:
            print('  ', u)

    sitemap = os.path.join(ROOT, 'sitemap.xml')
    if os.path.isfile(sitemap):
        with open(sitemap, encoding='utf-8') as f:
            urls = re.findall(r'<loc>https://sottolineature\.it([^<]*)</loc>', f.read())
        missing = [u for u in urls if resolve(u) in (None,)]
        in_sitemap_noindex = [u for u in urls if u in noindex]
        if missing:
            problems += len(missing)
            print('\nURL IN SITEMAP CHE NON ESISTONO:', len(missing))
            for u in missing[:10]:
                print('  ', u)
        if in_sitemap_noindex:
            problems += len(in_sitemap_noindex)
            print('\nURL IN SITEMAP MA CON noindex:', len(in_sitemap_noindex))
            for u in in_sitemap_noindex[:10]:
                print('  ', u)

    # --- tassonomia: tema e genere si scrivono a mano in data/citazioni.json, e
    #     niente controllava che fossero valori esistenti. Il 2026-08-30 sono
    #     finite 162 citazioni con un genere scritto nel campo del tema
    #     ("Narrativa", "Saggistica", "Poesia") e temi inventati ("arte",
    #     "morte"): valori che non corrispondono a nessun filtro e a nessun hub,
    #     quindi quelle citazioni erano raggiungibili solo dalla ricerca. Un
    #     refuso di maiuscola ("Fantascienza" invece di "fantascienza") fa lo
    #     stesso danno in silenzio. ---
    data_path = os.path.join(ROOT, 'data', 'citazioni.json')
    if os.path.isfile(data_path):
        sys.path.insert(0, os.path.join(ROOT, 'tools'))
        from labels import CATEGORY_LABELS, GENRE_LABELS
        with open(data_path, encoding='utf-8') as f:
            quotes = json.load(f)
        bad_cat = collections.Counter()
        bad_gen = collections.Counter()
        for q in quotes:
            cat = (q.get('category') or '').strip()
            if cat and cat not in CATEGORY_LABELS:
                bad_cat[cat] += 1
            for g in (q.get('genre') or '').split():
                if g not in GENRE_LABELS:
                    bad_gen[g] += 1
        if bad_cat:
            problems += sum(bad_cat.values())
            print('\nTEMI INESISTENTI in data/citazioni.json:', sum(bad_cat.values()), 'citazioni')
            print('   (non compaiono in nessun filtro ne in nessun hub: solo ricerca)')
            for v, n in bad_cat.most_common():
                print('   %-16s %d' % (v, n))
            print('   temi validi:', ', '.join(sorted(CATEGORY_LABELS)))
        if bad_gen:
            problems += sum(bad_gen.values())
            print('\nGENERI INESISTENTI in data/citazioni.json:', sum(bad_gen.values()), 'citazioni')
            for v, n in bad_gen.most_common():
                print('   %-16s %d' % (v, n))
            print('   generi validi:', ', '.join(sorted(GENRE_LABELS)))

    print('\nProblemi totali:', problems)
    return 1 if problems else 0


if __name__ == '__main__':
    sys.exit(main())
