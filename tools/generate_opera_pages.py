#!/usr/bin/env python3
"""Genera pagine opera /opere/<slug>/ (Fase 4 SEO.md §9.3).

Solo per le opere elencate in data/opere.json: >=2 citazioni in archivio
o titoli del canone scolastico, e sempre con una scheda editoriale verificata
(anno, cos'e' il libro). Non si genera mai una pagina per tutte le 249 opere:
sarebbe la fabbrica di doorway page che il metodo del sito vuole evitare.

Uso: python3 tools/generate_opera_pages.py
"""
import html
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate_quote_pages import ROOT, SITE_URL, slugify  # noqa: E402

OPERE_PATH = os.path.join(ROOT, 'data', 'opere.json')
OUT_DIR = os.path.join(ROOT, 'opere')

PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="color-scheme" content="light dark">
<meta name="theme-color" content="#f2f0eb">
<title>{title_tag}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="article">
<meta property="og:title" content="{title_tag}">
<meta property="og:description" content="{description}">
<meta property="og:image" content="{og_image}">
<meta property="og:url" content="{canonical}">
<meta property="og:site_name" content="Sottolineature">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title_tag}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="{og_image}">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="stylesheet" href="/assets/site.css">
<script type="application/ld+json">{jsonld}</script>
<script>
  try {{
    document.documentElement.className += ' js';
    var savedTheme = localStorage.getItem('sottolineature-theme');
    if (savedTheme === 'dark') {{ document.documentElement.setAttribute('data-theme', 'dark'); var mtc = document.querySelector('meta[name="theme-color"]'); if (mtc) {{ mtc.setAttribute('content', '#16191a'); }} }}
  }} catch (e) {{}}
</script>
</head>
<body class="has-header">
<header class="site-header">
  <div class="site-header-inner">
    <a class="brand" href="/">
      <img src="/mark-quill.png" alt="" width="30" height="30">
      <span class="brand-name">Sottolineature</span>
    </a>
    <form class="header-search sans js-only" action="/" method="get" role="search" aria-label="Cerca dall'intestazione">
      <label class="visually-hidden" for="headerSearch">Cerca fra le citazioni</label>
      <input type="search" id="headerSearch" name="q" placeholder="Cerca autore, parola o frase…" autocomplete="off">
    </form>
    <nav class="site-nav sans" aria-label="Principale">
      <a href="/citazioni/">Citazioni</a>
      <a href="/autori/">Autori</a>
      <a href="/raccolte/">Raccolte</a>
      <a href="/temi/">Temi</a>
      <a href="/le-mie-sottolineature/" id="navMine">Le mie</a>
      <a href="/metodo/">Metodo</a>
      <button class="theme-toggle js-only" id="themeToggle" type="button" aria-label="Cambia tema chiaro/scuro">☾</button>
    </nav>
  </div>
</header>
<script src="/assets/nav.js" defer></script>
<div class="page">
<div class="page-main" role="main">
  <nav class="breadcrumb sans" aria-label="Percorso">
    <a href="/">Sottolineature</a> › <a href="/autori/{author_slug}/">{author}</a> › <span aria-current="page">{title}</span>
  </nav>
  <p class="eyebrow sans">Un'opera</p>
  <h1>{h1}</h1>
  <p class="count sans">{author}{year_html} · {count} citazion{count_suffix} in archivio</p>
  <p class="opera-scheda">{scheda}</p>
  {cards_html}
  </div>
  <footer class="sans">
    Da <a href="/" style="color:var(--ink-faint)">Sottolineature</a> — citazioni verificate a mano, senza algoritmo. <a href="/feed.xml" style="color:var(--ink-faint)">Segui le nuove citazioni</a>. <a href="mailto:sottolineature@outlook.it" style="color:var(--ink-faint)">Scrivici</a>. <a href="/privacy/" style="color:var(--ink-faint)">Privacy</a>.
  </footer>
</div>
<script>
  (function () {{
    var toggle = document.getElementById('themeToggle');
    var root = document.documentElement;
    function currentTheme() {{ return root.getAttribute('data-theme') === 'dark' ? 'dark' : 'light'; }}
    function render() {{ toggle.textContent = currentTheme() === 'dark' ? '☀' : '☾'; }}
    render();
    toggle.addEventListener('click', function () {{
      var next = currentTheme() === 'dark' ? 'light' : 'dark';
      if (next === 'dark') {{ root.setAttribute('data-theme', 'dark'); }} else {{ root.removeAttribute('data-theme'); }}
      try {{ localStorage.setItem('sottolineature-theme', next); }} catch (e) {{}}
      render();
    }});
  }})();
</script>
</body>
</html>
"""


def load_opere():
    with open(OPERE_PATH, encoding='utf-8') as f:
        return json.load(f)


def card_html(slug, q):
    year_html = (' · <span class="card-year">' + html.escape(q['year']) + '</span>') if q['year'] else ''
    return (
        '<article class="card">'
        '<span class="card-mark" aria-hidden="true">“</span>'
        '<div class="card-body">'
        '<p class="card-quote"><a href="/citazioni/' + slug + '/">' + html.escape(q['quote']) + '</a></p>'
        '<p class="card-citation sans"><a href="/citazioni/' + slug + '/">'
        '<span class="card-author">' + html.escape(q['author']) + '</span> — '
        '<span class="card-title">' + html.escape(q['title']) + '</span>' + year_html + '</a></p>'
        '</div></article>'
    )


def build_opera_map(entries, opere):
    """Mappa (autore, titolo) -> info sull'opera, usata da generate_quote_pages
    per riusare lo stesso Book @id su tutte le citazioni della stessa opera e
    linkare la pagina opera dalla pagina citazione. `entries` sono le coppie
    (slug, q) gia' assegnate da assign_slugs (non serve che siano renderizzate)."""
    by_slug_lookup = {}
    for op in opere:
        canonical = SITE_URL + '/opere/' + op['slug'] + '/'
        info = {
            'opera_slug': op['slug'],
            'opera_url': canonical,
            'book_id': canonical + '#book',
            'title': op['title'],
        }
        for t in op['titles']:
            by_slug_lookup[(op['author'], t)] = info
    return by_slug_lookup


def render_opera(op, items):
    count = len(items)
    count_suffix = 'i' if count != 1 else 'e'
    cards_html = '\n  '.join(card_html(s, q) for s, q in items)
    author_slug = slugify(op['author'])
    author_esc = html.escape(op['author'])
    title_esc = html.escape(op['title'])
    year_html = (', ' + html.escape(op['year'])) if op.get('year') else ''

    h1 = 'Frasi e citazioni da ' + op['title'] + ' di ' + op['author']
    description = (
        str(count) + ' citazion' + count_suffix + ' verificat' + ('a' if count == 1 else 'e') +
        ' da «' + op['title'] + '» di ' + op['author'] +
        (' (' + op['year'] + ')' if op.get('year') else '') + '.'
    )
    canonical = SITE_URL + '/opere/' + op['slug'] + '/'
    # Nei risultati di ricerca si leggono si' e no 64 caratteri: con un titolo
    # lungo il marchio in coda spariva comunque, e con «Canto notturno di un
    # pastore errante dell'Asia» spariva anche il nome dell'autore. Si scala:
    # forma piena, poi senza marchio, poi senza autore.
    for candidate in (h1 + ' | Sottolineature', h1, 'Frasi e citazioni da ' + op['title']):
        title_tag = candidate
        if len(title_tag) <= 64:
            break
    og_image = SITE_URL + '/og-banner.png'

    author_id = SITE_URL + '/autori/' + author_slug + '/#person'
    book_id = canonical + '#book'
    item_list = {
        '@type': 'ItemList',
        'itemListElement': [
            {'@type': 'ListItem', 'position': i + 1, 'url': SITE_URL + '/citazioni/' + s + '/'}
            for i, (s, _) in enumerate(items)
        ],
    }
    jsonld = json.dumps({
        '@context': 'https://schema.org',
        '@graph': [
            {
                '@type': 'WebPage',
                '@id': canonical + '#webpage',
                'url': canonical,
                'name': title_tag,
                'description': description,
                'breadcrumb': {'@id': canonical + '#breadcrumb'},
                'mainEntity': {'@id': book_id},
            },
            {
                '@type': 'Book',
                '@id': book_id,
                'name': op['title'],
                'author': {'@id': author_id},
                **({'datePublished': op['year']} if op.get('year') else {}),
            },
            {
                '@type': 'Person',
                '@id': author_id,
                'name': op['author'],
                'url': SITE_URL + '/autori/' + author_slug + '/',
            },
            {
                '@type': 'CollectionPage',
                '@id': canonical + '#collectionpage',
                'url': canonical,
                'name': title_tag,
                'isPartOf': {'@type': 'WebSite', '@id': SITE_URL + '/#website'},
                'mainEntity': item_list,
            },
            {
                '@type': 'BreadcrumbList',
                '@id': canonical + '#breadcrumb',
                'itemListElement': [
                    {'@type': 'ListItem', 'position': 1, 'name': 'Sottolineature', 'item': SITE_URL + '/'},
                    {'@type': 'ListItem', 'position': 2, 'name': op['author'], 'item': SITE_URL + '/autori/' + author_slug + '/'},
                    {'@type': 'ListItem', 'position': 3, 'name': op['title'], 'item': canonical},
                ],
            },
        ],
    }, ensure_ascii=False)

    return PAGE_TEMPLATE.format(
        title_tag=html.escape(title_tag),
        description=html.escape(description),
        canonical=canonical,
        og_image=og_image,
        jsonld=jsonld,
        author_slug=author_slug,
        author=author_esc,
        title=title_esc,
        h1=html.escape(h1),
        year_html=year_html,
        count=count,
        count_suffix=count_suffix,
        scheda=html.escape(op['scheda']),
        cards_html=cards_html,
    )


def main(entries):
    """`entries` = le coppie (slug, q) gia' renderizzate da generate_quote_pages,
    cosi' le card dell'opera linkano a citazioni gia' scritte su disco."""
    opere = load_opere()
    by_author_title = {}
    for slug, q in entries:
        by_author_title.setdefault((q['author'], q['title']), []).append((slug, q))

    os.makedirs(OUT_DIR, exist_ok=True)
    existing = set(os.listdir(OUT_DIR)) if os.path.isdir(OUT_DIR) else set()

    opera_status = {}
    for op in opere:
        items = []
        for t in op['titles']:
            items.extend(by_author_title.get((op['author'], t), []))
        if not items:
            print('ATTENZIONE: nessuna citazione trovata per opera', op['slug'], '- pagina non generata')
            continue
        page = render_opera(op, items)
        with open(os.path.join(OUT_DIR, op['slug'] + '.html'), 'w', encoding='utf-8') as f:
            f.write(page)
        opera_status[op['slug']] = len(items)

    generated_files = set(slug + '.html' for slug in opera_status)
    # index.html della cartella e' l'indice, lo scrive generate_index_pages:
    # non e' una pagina orfana
    stale = existing - generated_files - {'index.html'}
    removed = []
    for fname in stale:
        if not fname.endswith('.html'):
            continue
        try:
            os.remove(os.path.join(OUT_DIR, fname))
            removed.append(fname)
        except OSError as err:
            print('Attenzione: non ho potuto rimuovere', fname, '-', err)
    if removed:
        print('Rimosse pagine opera obsolete:', len(removed))

    print('Pagine opera generate:', len(opera_status), '/', len(opere))
    return opera_status


if __name__ == '__main__':
    from generate_quote_pages import load_quotes, load_slugs, load_redirects, assign_slugs
    quotes = load_quotes()
    entries, _ = assign_slugs(quotes, load_slugs(), load_redirects())
    main(entries)
