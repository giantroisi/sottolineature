#!/usr/bin/env python3
"""Genera pagine raccolta /raccolte/<slug>/ (Fase 5 SEO.md).

Selezioni curate a mano di citazioni gia' pubblicate, con introduzione
editoriale scritta a mano: intercettano intenti di ricerca stretti ("frasi
sul mare", "incipit memorabili") che i 7 temi, tenuti volutamente
larghi, non coprono. Una raccolta si pubblica solo con >=8 citazioni
pertinenti e un'introduzione scritta - mai generate combinando filtri.

Uso: python3 tools/generate_raccolte_pages.py
"""
import html
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate_quote_pages import ROOT, SITE_URL, quote_key  # noqa: E402

RACCOLTE_PATH = os.path.join(ROOT, 'data', 'raccolte.json')
OUT_DIR = os.path.join(ROOT, 'raccolte')
MIN_QUOTES = 8

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
    <a href="/">Sottolineature</a> › <a href="/raccolte/">Raccolte</a> › <span aria-current="page">{title}</span>
  </nav>
  <p class="eyebrow sans">Una raccolta</p>
  <h1>{h1}</h1>
  <p class="count sans">{count} citazion{count_suffix} scelte a mano</p>
  <div class="hub-intro">{intro_html}</div>
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


def load_raccolte():
    with open(RACCOLTE_PATH, encoding='utf-8') as f:
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


def build_raccolta_map(entries, raccolte):
    """Mappa quote_key -> lista di {slug, title} delle raccolte che la
    contengono (una citazione puo' comparire in piu' raccolte). Usata da
    generate_quote_pages per il link "In questa raccolta ->" sulla pagina
    citazione corrispondente."""
    by_key = {}
    for r in raccolte:
        for k in r['quote_keys']:
            by_key.setdefault(k, []).append({
                'slug': r['slug'],
                'title': r['title'],
                'url': SITE_URL + '/raccolte/' + r['slug'] + '/',
            })
    return by_key


def render_raccolta(r, items):
    count = len(items)
    count_suffix = 'i' if count != 1 else 'e'
    cards_html = '\n  '.join(card_html(s, q) for s, q in items)
    title_esc = html.escape(r['title'])
    h1 = r['h1']
    intro_html = ''.join('<p>' + html.escape(p) + '</p>' for p in r['intro'])
    # 155 caratteri: oltre, Google taglia e la coda non la legge nessuno
    description = (
        str(count) + ' citazion' + count_suffix + ' scelt' + ('a' if count == 1 else 'e') +
        ' a mano — ' + r['intro'][0]
    )
    if len(description) > 155:
        description = description[:154].rsplit(' ', 1)[0] + '…'
    canonical = SITE_URL + '/raccolte/' + r['slug'] + '/'
    title_tag = h1 + ' | Sottolineature'
    og_image = SITE_URL + '/og-banner.png'

    item_list = {
        '@type': 'ItemList',
        'itemListElement': [
            {'@type': 'ListItem', 'position': i + 1, 'url': SITE_URL + '/citazioni/' + s + '/'}
            for i, (s, _) in enumerate(items)
        ],
    }
    jsonld = json.dumps({
        '@context': 'https://schema.org',
        '@type': 'CollectionPage',
        '@id': canonical + '#collectionpage',
        'url': canonical,
        'name': title_tag,
        'description': description,
        'isPartOf': {'@type': 'WebSite', '@id': SITE_URL + '/#website'},
        'mainEntity': item_list,
    }, ensure_ascii=False)

    return PAGE_TEMPLATE.format(
        title_tag=html.escape(title_tag),
        description=html.escape(description),
        canonical=canonical,
        og_image=og_image,
        jsonld=jsonld,
        title=title_esc,
        h1=html.escape(h1),
        count=count,
        count_suffix=count_suffix,
        intro_html=intro_html,
        cards_html=cards_html,
    )


def main(entries):
    """`entries` = le coppie (slug, q) gia' renderizzate da generate_quote_pages."""
    raccolte = load_raccolte()
    by_key = {quote_key(q): (s, q) for s, q in entries}

    os.makedirs(OUT_DIR, exist_ok=True)
    existing = set(os.listdir(OUT_DIR)) if os.path.isdir(OUT_DIR) else set()

    raccolta_status = {}
    for r in raccolte:
        items = [by_key[k] for k in r['quote_keys'] if k in by_key]
        missing = [k for k in r['quote_keys'] if k not in by_key]
        if missing:
            print('ATTENZIONE: chiavi non trovate per raccolta', r['slug'], '-', missing)
        if len(items) < MIN_QUOTES:
            print('ATTENZIONE: raccolta', r['slug'], 'sotto la soglia di', MIN_QUOTES, 'citazioni - non pubblicata')
            continue
        page = render_raccolta(r, items)
        with open(os.path.join(OUT_DIR, r['slug'] + '.html'), 'w', encoding='utf-8') as f:
            f.write(page)
        raccolta_status[r['slug']] = len(items)

    generated_files = set(slug + '.html' for slug in raccolta_status)
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
        print('Rimosse pagine raccolta obsolete:', len(removed))

    print('Pagine raccolta generate:', len(raccolta_status), '/', len(raccolte))
    return raccolta_status


if __name__ == '__main__':
    from generate_quote_pages import load_quotes, load_slugs, load_redirects, assign_slugs
    quotes = load_quotes()
    entries, _ = assign_slugs(quotes, load_slugs(), load_redirects())
    main(entries)
