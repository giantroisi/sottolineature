#!/usr/bin/env python3
"""Controllo strutturale del sito generato.

Verifica link interni, metadati, landmark, gerarchia dei titoli, immagini,
breadcrumb/dati strutturati attesi, pagine orfane e coerenza bidirezionale con
la sitemap. Eseguito direttamente (``python3 tools/check_links.py``) esce con
codice 1 sugli errori reali; ``build.py`` lo richiama in modalita' diagnostica,
cosi' un controllo euristico non rende fragile la generazione del sito.

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
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {'.git', '.vercel', '.netlify', 'node_modules', 'archivio', 'tools',
             'templates', '__pycache__', '.claude', 'assets'}

HREF = re.compile(r'(?:href|src)="([^"]+)"')
ANCHOR_HREF = re.compile(r'<a\b[^>]*href="([^"]+)"', re.I)
TITLE = re.compile(r'<title>(.*?)</title>', re.S)
DESC = re.compile(r'<meta name="description" content="(.*?)"', re.S)
CANON = re.compile(r'<link rel="canonical" href="([^"]+)"')
ROBOTS = re.compile(r'<meta name="robots" content="([^"]+)"')
H1 = re.compile(r'<h1\b', re.I)
MAIN = re.compile(r'<main\b', re.I)
ROLE_MAIN = re.compile(r'\brole=["\']main["\']', re.I)
HEADING = re.compile(r'<h([1-6])\b', re.I)
IMAGE = re.compile(r'<img\b([^>]*)>', re.I | re.S)
JSONLD = re.compile(r'<script\b[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', re.I | re.S)
VISIBLE_BREADCRUMB = re.compile(r'<nav\b[^>]*class=["\'][^"\']*\bbreadcrumb\b', re.I)

SITE_URL = 'https://sottolineature.it'
SITEMAP_NS = 'http://www.sitemaps.org/schemas/sitemap/0.9'

# Autori che scrivono/scrivevano in italiano: per le loro opere il "traduttore"
# non esiste per definizione, quindi non vanno contati fra le citazioni senza
# traduttore. Il criterio e' la lingua originale del testo, non la nazionalita'
# dell'autore o l'epoca: latino e greco antico restano fuori (Aristotele,
# Boezio, Epitteto, Marco Aurelio, Marco Tullio Cicerone, Omero, Platone,
# Sant'Agostino, Seneca, Virgilio), perche' anche quei testi vanno tradotti.
ITALIAN_AUTHORS = {
    'Alba de Céspedes', 'Alberto Moravia', 'Alda Merini', 'Alessandro Baricco',
    'Alessandro Manzoni', 'Andrea Camilleri', 'Anna Maria Ortese',
    'Antonio Tabucchi', 'Beppe Fenoglio', 'Carlo Collodi', 'Carlo Goldoni',
    'Carlo Levi', 'Cesare Pavese', 'Curzio Malaparte', 'Dacia Maraini',
    'Dante Alighieri', 'Dino Buzzati', 'Elena Ferrante', 'Elio Vittorini',
    'Elsa Morante', 'Erri De Luca', 'Eugenio Montale', 'Francesco Petrarca',
    "Gabriele D'Annunzio", 'Giacomo Leopardi', 'Giorgio Bassani',
    'Giovanni Boccaccio', 'Giovanni Pascoli', 'Giovanni Verga',
    'Giuseppe Tomasi di Lampedusa', 'Giuseppe Ungaretti', 'Goliarda Sapienza',
    'Grazia Deledda', 'Ignazio Silone', 'Ippolito Nievo', 'Italo Calvino',
    'Italo Svevo', 'Leonardo Sciascia', 'Ludovico Ariosto', 'Luigi Pirandello',
    'Mario Rigoni Stern', 'Michela Murgia', 'Natalia Ginzburg',
    'Niccolò Ammaniti', 'Niccolò Machiavelli', 'Paolo Cognetti',
    'Pier Paolo Pasolini', 'Primo Levi', 'Salvatore Quasimodo',
    'Sandro Veronesi', 'Sibilla Aleramo', 'Susanna Tamaro', 'Torquato Tasso',
    'Ugo Foscolo', 'Umberto Eco', 'Umberto Saba', 'Vasco Pratolini',
    'Vittorio Alfieri',
}

# Eccezione dentro un autore altrimenti italiano: opere scritte in un'altra
# lingua dallo stesso autore. Petrarca scriveva sia in volgare (Canzoniere,
# Rime estravaganti) sia in latino: la "Lettera ai posteri" (Epistola
# posteritati) e' un testo latino e va tradotta come le altre.
NON_ITALIAN_WORKS = {
    ('Francesco Petrarca', 'Lettera ai posteri'),
}


def is_italian_original(quote):
    if (quote['author'], quote['title']) in NON_ITALIAN_WORKS:
        return False
    return quote['author'] in ITALIAN_AUTHORS


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


def validate_sitemaps(noindex):
    """Controlla l'indice e, soprattutto, tutte le sitemap figlie.

    Il vecchio controllo leggeva soltanto i ``<loc>`` di sitemap.xml: quindi
    verificava che esistessero i sette file XML, ma non una sola delle oltre
    mille pagine dichiarate al loro interno. Questo controllo segue l'indice,
    rifiuta host o percorsi non canonici, apre ogni figlia e verifica che ogni
    URL esista, non sia ``noindex`` e non compaia in due sitemap diverse.
    """
    index_path = os.path.join(ROOT, 'sitemap.xml')
    report = {'children': 0, 'urls': 0, 'errors': [], 'seen_urls': set()}
    if not os.path.isfile(index_path):
        return report

    ns = '{' + SITEMAP_NS + '}'
    try:
        index_root = ET.parse(index_path).getroot()
    except (ET.ParseError, OSError) as err:
        report['errors'].append(('sitemap.xml', 'XML non valido: ' + str(err)))
        return report

    if index_root.tag != ns + 'sitemapindex':
        report['errors'].append(('sitemap.xml', 'radice diversa da <sitemapindex>'))
        return report

    child_locs = []
    for sitemap in index_root.findall(ns + 'sitemap'):
        loc = sitemap.find(ns + 'loc')
        if loc is None or not (loc.text or '').strip():
            report['errors'].append(('sitemap.xml', '<sitemap> senza <loc>'))
            continue
        child_locs.append(loc.text.strip())

    if not child_locs:
        report['errors'].append(('sitemap.xml', 'nessuna sitemap figlia dichiarata'))
        return report

    duplicate_children = [loc for loc, count in collections.Counter(child_locs).items()
                          if count > 1]
    for loc in duplicate_children:
        report['errors'].append(('sitemap.xml', 'sitemap figlia duplicata: ' + loc))

    seen_urls = {}
    for child_loc in child_locs:
        prefix = SITE_URL + '/'
        if not child_loc.startswith(prefix):
            report['errors'].append(('sitemap.xml', 'host non canonico nella figlia: ' + child_loc))
            continue
        relative = child_loc[len(prefix):]
        if not relative or '?' in relative or '#' in relative:
            report['errors'].append(('sitemap.xml', 'percorso figlia non valido: ' + child_loc))
            continue
        child_path = os.path.abspath(os.path.join(ROOT, relative))
        try:
            inside_root = os.path.commonpath((ROOT, child_path)) == ROOT
        except ValueError:
            inside_root = False
        if not inside_root or not os.path.isfile(child_path):
            report['errors'].append(('sitemap.xml', 'file figlio inesistente: ' + child_loc))
            continue

        try:
            child_root = ET.parse(child_path).getroot()
        except (ET.ParseError, OSError) as err:
            report['errors'].append((relative, 'XML non valido: ' + str(err)))
            continue
        report['children'] += 1
        if child_root.tag != ns + 'urlset':
            report['errors'].append((relative, 'radice diversa da <urlset>'))
            continue

        url_nodes = child_root.findall(ns + 'url')
        if not url_nodes:
            report['errors'].append((relative, 'nessun URL dichiarato'))
        for url_node in url_nodes:
            loc = url_node.find(ns + 'loc')
            if loc is None or not (loc.text or '').strip():
                report['errors'].append((relative, '<url> senza <loc>'))
                continue
            absolute = loc.text.strip()
            report['urls'] += 1
            if absolute == SITE_URL + '/':
                url = '/'
            elif absolute.startswith(prefix):
                url = absolute[len(SITE_URL):]
            else:
                report['errors'].append((relative, 'URL con host non canonico: ' + absolute))
                continue
            if '?' in url or '#' in url:
                report['errors'].append((relative, 'URL non canonico con query o frammento: ' + absolute))
                continue
            if not url.endswith('/'):
                report['errors'].append((relative, 'URL senza slash finale: ' + absolute))
                continue
            if resolve(url) is None:
                report['errors'].append((relative, 'URL inesistente: ' + absolute))
            if url in noindex:
                report['errors'].append((relative, 'URL con noindex: ' + absolute))
            if absolute in seen_urls:
                report['errors'].append((relative, 'URL duplicato anche in ' + seen_urls[absolute] + ': ' + absolute))
            else:
                seen_urls[absolute] = relative
                report['seen_urls'].add(url)

    return report


def jsonld_types(html):
    """Restituisce i tipi Schema.org presenti, ignorando l'ordine del grafo."""
    found = set()

    def walk(node):
        if isinstance(node, dict):
            value = node.get('@type')
            if isinstance(value, str):
                found.add(value)
            elif isinstance(value, list):
                found.update(v for v in value if isinstance(v, str))
            for child in node.values():
                walk(child)
        elif isinstance(node, list):
            for child in node:
                walk(child)

    for raw in JSONLD.findall(html):
        try:
            walk(json.loads(raw))
        except (TypeError, ValueError):
            # controlla_jsonld.py stampa il dettaglio dell'errore di sintassi;
            # qui evitiamo un doppio referto meno preciso.
            pass
    return found


def expected_jsonld_types(url):
    """Contratto minimo per tipo di pagina, non una whitelist esaustiva."""
    if url == '/':
        return {'WebSite'}
    if url == '/404/':
        return {'WebPage'}
    if url == '/metodo/':
        return {'AboutPage', 'BreadcrumbList'}
    if url in {'/privacy/', '/note-legali/', '/affiliazioni/'}:
        return {'WebPage', 'BreadcrumbList'}
    if url == '/le-mie-sottolineature/':
        # Raccolta privata nel browser: deliberatamente fuori dall'indice e
        # senza entita' pubblica da dichiarare ai motori.
        return set()
    parts = [p for p in url.split('/') if p]
    if (parts and parts[0] == 'citazioni' and len(parts) == 2 and
            not parts[1].startswith('pagina-') and not parts[1].isdigit()):
        return {'WebPage', 'Quotation', 'BreadcrumbList'}
    if parts and parts[0] in {'citazioni', 'autori', 'opere', 'raccolte', 'temi', 'generi'}:
        return {'CollectionPage', 'BreadcrumbList'}
    return set()


def expects_visible_breadcrumb(url):
    """Le pagine di dettaglio che nel design hanno una briciola visibile."""
    parts = [p for p in url.split('/') if p]
    return (len(parts) == 2 and parts[0] == 'opere') or (
        len(parts) >= 2 and parts[0] == 'raccolte') or (
        len(parts) == 2 and parts[0] == 'citazioni' and
        not parts[1].startswith('pagina-') and not parts[1].isdigit()
    )


def internal_url_style_problem(link):
    """Ritorna il motivo se un href interno espone una forma non canonica."""
    if not link.startswith('/') or link.startswith('//'):
        return None
    path = link.split('#')[0].split('?')[0]
    if not path:
        return None
    if path.endswith('/index.html') or path == '/index.html':
        return 'usa index.html invece dell’URL pulito'
    if path.endswith('.html'):
        return 'espone l’estensione .html'
    if '//' in path:
        return 'contiene una doppia slash'
    basename = path.rsplit('/', 1)[-1]
    if not path.endswith('/') and '.' not in basename:
        return 'pagina senza slash finale'
    return None


def main():
    pages = sorted(html_files())
    titles, descs, canons = collections.defaultdict(list), collections.defaultdict(list), {}
    broken, relative, insecure = [], [], []
    bad_url_style = []
    structure = collections.defaultdict(list)
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
        page_titles = TITLE.findall(html)
        page_descs = DESC.findall(html)
        page_canons = CANON.findall(html)
        if len(page_titles) != 1:
            structure['title assente o multiplo'].append((url, str(len(page_titles))))
        else:
            titles[page_titles[0].strip()].append(url)
        if len(page_descs) != 1:
            structure['meta description assente o multipla'].append((url, str(len(page_descs))))
        else:
            descs[page_descs[0].strip()].append(url)
        if len(page_canons) != 1:
            structure['canonical assente o multiplo'].append((url, str(len(page_canons))))
        else:
            canons[url] = page_canons[0]

        h1_count = len(H1.findall(scan))
        if h1_count != 1:
            structure['numero di H1 diverso da uno'].append((url, str(h1_count)))
        main_count = len(MAIN.findall(scan))
        if main_count != 1:
            detail = str(main_count)
            if ROLE_MAIN.search(scan):
                detail += ' (presente role="main", ma serve il tag semantico <main>)'
            structure['numero di <main> diverso da uno'].append((url, detail))

        headings = [int(level) for level in HEADING.findall(scan)]
        for before, after in zip(headings, headings[1:]):
            if after > before + 1:
                structure['gerarchia heading con livello saltato'].append(
                    (url, 'h%d seguito da h%d' % (before, after)))
                break

        for attrs in IMAGE.findall(scan):
            if not re.search(r'\balt\s*=', attrs, re.I):
                src = re.search(r'\bsrc=["\']([^"\']+)', attrs, re.I)
                structure['immagine senza attributo alt'].append(
                    (url, src.group(1) if src else '<src assente>'))

        present_types = jsonld_types(html)
        missing_types = expected_jsonld_types(url) - present_types
        if missing_types:
            structure['tipo JSON-LD atteso assente'].append(
                (url, ', '.join(sorted(missing_types))))
        if expects_visible_breadcrumb(url) and not VISIBLE_BREADCRUMB.search(scan):
            structure['breadcrumb visibile atteso assente'].append((url, 'nav.breadcrumb'))

        for link in ANCHOR_HREF.findall(scan):
            reason = internal_url_style_problem(link)
            if reason:
                bad_url_style.append((url, link, reason))
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
    if bad_url_style:
        problems += len(bad_url_style)
        print('\nURL INTERNI NON CANONICI:', len(bad_url_style))
        for src, link, reason in bad_url_style[:15]:
            print('  ', src, '->', link, '(' + reason + ')')

    if structure:
        structural_count = sum(len(items) for items in structure.values())
        problems += structural_count
        print('\nERRORI STRUTTURALI:', structural_count)
        for label, items in structure.items():
            print('  ', label + ':', len(items))
            for url, detail in items[:8]:
                print('     ', url, '->', detail)

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

    sitemap_report = validate_sitemaps(noindex)
    if sitemap_report['children'] or sitemap_report['urls']:
        print('Sitemap esaminate:', sitemap_report['children'], 'file figli,',
              sitemap_report['urls'], 'URL')
    if sitemap_report['errors']:
        problems += len(sitemap_report['errors'])
        print('\nERRORI NELLE SITEMAP:', len(sitemap_report['errors']))
        for source, message in sitemap_report['errors'][:20]:
            print('  ', source, '->', message)

    # Il controllo precedente andava in una sola direzione (URL dichiarato ->
    # file esistente). Anche una pagina indicizzabile dimenticata dalla sitemap
    # e' un errore: esiste, ma il canale con cui segnaliamo gli URL ai motori
    # non la include. La 404 e la raccolta personale sono esclusioni volute.
    sitemap_exempt = {'/404/', '/le-mie-sottolineature/'}
    expected_in_sitemap = {as_url(p) for p in pages} - noindex - sitemap_exempt
    missing_from_sitemap = sorted(expected_in_sitemap - sitemap_report['seen_urls'])
    if missing_from_sitemap:
        problems += len(missing_from_sitemap)
        print('\nPAGINE INDICIZZABILI ASSENTI DALLA SITEMAP:', len(missing_from_sitemap))
        for url in missing_from_sitemap[:20]:
            print('  ', url)

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

    # --- copertine: la copertina e' una proprieta' dell'opera, come il genere.
    #     Due citazioni dallo stesso libro non possono mostrarne una diversa, ne'
    #     una si' e una no. Il 2026-09-01 questo controllo ha trovato 19 opere
    #     con la copertina a meta' e, soprattutto, «Non lasciarmi» di Ishiguro
    #     che ne mostrava due: una delle due era «Quando eravamo orfani», cioe'
    #     il libro sbagliato, rimasto da una citazione tolta mesi prima. ---
    if os.path.isfile(data_path):
        per_opera = collections.defaultdict(list)
        for q in quotes:
            per_opera[(q['author'], q['title'])].append((q.get('cover') or '').strip())
        diverse, meta, senza_file = [], [], set()
        for (autore, titolo), covs in per_opera.items():
            distinte = set(c for c in covs if c)
            if len(distinte) > 1:
                diverse.append((autore, titolo, sorted(distinte)))
            elif distinte and len(covs) != sum(1 for c in covs if c):
                meta.append((autore, titolo, len(covs), sum(1 for c in covs if c)))
            for c in distinte:
                if not os.path.isfile(os.path.join(ROOT, c.lstrip('/'))):
                    senza_file.add(c)
        if diverse:
            problems += len(diverse)
            print('\nCOPERTINE DIVERSE PER LA STESSA OPERA:', len(diverse))
            for a, t, cs in diverse[:10]:
                print('   %s — %s: %s' % (a, t, ', '.join(cs)))
        if meta:
            problems += len(meta)
            print('\nCOPERTINA SOLO SU ALCUNE CITAZIONI DELLA STESSA OPERA:', len(meta))
            for a, t, tot, con in meta[:10]:
                print('   %s — %s (%d citazioni, %d con copertina)' % (a, t, tot, con))
        if senza_file:
            problems += len(senza_file)
            print('\nCOPERTINE DICHIARATE MA SENZA FILE:', len(senza_file))
            for c in sorted(senza_file)[:10]:
                print('  ', c)

    # --- sameAs: ogni autore dovrebbe avere la sua voce Wikipedia/Wikidata
    #     verificata in data/autori_sameas.json. Un autore nuovo che arriva con
    #     un lotto di citazioni non ce l'ha: e' un avviso, non un problema
    #     (il nodo Person semplicemente non viene emesso), ma va visto, perche'
    #     senza sameAs la pagina autore resta un'entita' anonima per un motore. ---
    sameas_path = os.path.join(ROOT, 'data', 'autori_sameas.json')
    if os.path.isfile(data_path) and os.path.isfile(sameas_path):
        with open(sameas_path, encoding='utf-8') as f:
            sameas = json.load(f)
        senza = sorted(set(q['author'] for q in quotes) - set(sameas))
        if senza:
            print('\nAVVISO — autori senza voce in data/autori_sameas.json:', len(senza))
            for a in senza[:15]:
                print('  ', a)
            print('   (vanno risolti su it.wikipedia.org e verificati su Wikidata, mai dedotti dal nome)')

    # --- contesto: la pagina citazione non e' povera di parole (mediana 237
    #     visibili, minimo 167), ma quasi tutte vengono dalla citazione, dal
    #     blocco fonte e dalle correlate. L'unico testo originale e' il
    #     contesto, e al 2026-09-03 la sua mediana era di 31 parole. E' li' che
    #     si gioca la differenza fra una pagina che aggiunge qualcosa e una
    #     scheda. Avviso, non problema: allungare per allungare sarebbe peggio. ---
    if os.path.isfile(data_path):
        corti = [q for q in quotes if 0 < len((q.get('context') or '').split()) < 45]
        vuoti = [q for q in quotes if not (q.get('context') or '').strip()]
        if corti or vuoti:
            print('\nAVVISO — contesti brevi: %d sotto le 45 parole, %d assenti (su %d)'
                  % (len(corti), len(vuoti), len(quotes)))
            print('   il contesto e\' l\'unico testo originale della pagina citazione:')
            print('   60-90 parole la rendono una pagina che spiega, 30 la lasciano una scheda')

    # --- traduttore: su un'opera tradotta la frase italiana e' del traduttore.
    #     Senza il suo nome la citazione non e' attribuibile, ed e' esattamente
    #     cio' che metodo.html promette. Due controlli: uno bloccante, uno di
    #     avviso. Bloccante e' l'incoerenza — la stessa edizione con due
    #     traduttori diversi, o con il nome su una citazione e non sulle altre:
    #     il traduttore appartiene all'edizione, come la copertina all'opera. ---
    if os.path.isfile(data_path):
        per_ed = collections.defaultdict(list)
        for q in quotes:
            if q.get('source_edition'):
                per_ed[(q['author'], q['title'], q['source_edition'])].append(q)
        discordi, meta_trad = [], []
        for (a, t, ed), gruppo in per_ed.items():
            nomi = set(q.get('source_translator') or '' for q in gruppo)
            pieni = set(n for n in nomi if n)
            if len(pieni) > 1:
                discordi.append((a, t, sorted(pieni)))
            elif pieni and '' in nomi:
                meta_trad.append((a, t, len(gruppo), len(gruppo) - sum(1 for q in gruppo if not q.get('source_translator'))))
        if discordi:
            problems += len(discordi)
            print('\nTRADUTTORI DIVERSI PER LA STESSA EDIZIONE:', len(discordi))
            for a, t, ns in discordi[:10]:
                print('   %s — %s: %s' % (a, t, ', '.join(ns)))
        if meta_trad:
            problems += len(meta_trad)
            print('\nTRADUTTORE SOLO SU ALCUNE CITAZIONI DELLA STESSA EDIZIONE:', len(meta_trad))
            for a, t, tot, con in meta_trad[:10]:
                print('   %s — %s (%d citazioni, %d con traduttore)' % (a, t, tot, con))
        senza_trad = [q for q in quotes
                      if q.get('source_edition') and not q.get('source_translator')
                      and not is_italian_original(q)]
        if senza_trad:
            print('\nAVVISO — citazioni con edizione ma senza traduttore: %d' % len(senza_trad))
            print('   su un\'opera tradotta la frase italiana e\' del traduttore: senza il suo')
            print('   nome la citazione non e\' attribuibile (le opere italiane non contano)')

    print('\nProblemi totali:', problems)
    return 1 if problems else 0


if __name__ == '__main__':
    sys.exit(main())
