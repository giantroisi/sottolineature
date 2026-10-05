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
from labels import grafo_con_breadcrumb  # noqa: E402

RACCOLTE_PATH = os.path.join(ROOT, 'data', 'raccolte.json')
OUT_DIR = os.path.join(ROOT, 'raccolte')
MIN_QUOTES = 8
PAGE_SIZE = 30

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
{link_rel_extra}
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
<main class="page-main">
  <nav class="breadcrumb sans" aria-label="Percorso">
    {breadcrumb_html}
  </nav>
  <p class="eyebrow sans">Una raccolta</p>
  <h1>{h1}</h1>
  <p class="count sans">{count_line}</p>
  <div class="hub-intro">{intro_html}</div>
  {h2_lista}
  {cards_html}
  </main>
  <footer class="sans">
    Da <a href="/" style="color:var(--ink-faint)">Sottolineature</a> — citazioni verificate a mano, senza algoritmo.<span class="footer-servizi"> <a href="/feed.xml" style="color:var(--ink-faint)">Segui le nuove citazioni</a>. <a href="mailto:sottolineature@outlook.it" style="color:var(--ink-faint)">Scrivici</a>. <a href="/privacy/" style="color:var(--ink-faint)">Privacy</a>. <a href="/note-legali/" style="color:var(--ink-faint)">Note legali</a>. <a href="/affiliazioni/" style="color:var(--ink-faint)">Affiliazioni</a>.</span>
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


def raccolta_href(slug, page_num):
    return '/raccolte/' + slug + '/' if page_num == 1 else '/raccolte/' + slug + '/' + str(page_num) + '/'


def pagination_link(slug, page_num, current):
    cls = ' class="is-current" aria-current="page"' if page_num == current else ''
    return '<a href="' + raccolta_href(slug, page_num) + '"' + cls + '>' + str(page_num) + '</a>'


def build_pagination_html(slug, page_num, num_pages):
    """Pagina 1 collega tutte le parti; le successive usano una finestra corta."""
    if num_pages <= 1:
        return ''
    parts = []
    if page_num > 1:
        parts.append('<a href="' + raccolta_href(slug, page_num - 1) + '">← Pagina precedente</a>')
    if page_num == 1:
        parts.extend(pagination_link(slug, p, page_num) for p in range(1, num_pages + 1))
    else:
        shown = sorted({1, 2, num_pages - 1, num_pages, page_num - 1, page_num, page_num + 1} &
                       set(range(1, num_pages + 1)))
        last = None
        for p in shown:
            if last is not None and p - last > 1:
                parts.append('<span class="pagination-ellipsis" aria-hidden="true">…</span>')
            parts.append(pagination_link(slug, p, page_num))
            last = p
    if page_num < num_pages:
        parts.append('<a href="' + raccolta_href(slug, page_num + 1) + '">Pagina successiva →</a>')
    return '<nav class="hub-nav sans" aria-label="Paginazione della raccolta">' + ''.join(parts) + '</nav>'


def render_raccolta(r, page_items, total, page_num, num_pages):
    count_suffix = 'i' if total != 1 else 'e'
    cards_html = '\n  '.join(card_html(s, q) for s, q in page_items)
    title_esc = html.escape(r['title'])
    h1 = r['h1']
    intro_html = ''.join('<p>' + html.escape(p) + '</p>' for p in r['intro'])
    # 155 caratteri: oltre, Google taglia e la coda non la legge nessuno
    description = (
        str(total) + ' citazion' + count_suffix + ' scelt' + ('a' if total == 1 else 'e') +
        ' a mano — ' + r['intro'][0]
    )
    if page_num > 1:
        authors = []
        for _, q in page_items:
            if q['author'] not in authors:
                authors.append(q['author'])
        description = (r['title'] + ', pagina ' + str(page_num) + ' di ' + str(num_pages) +
                       ': citazioni da ' + authors[0] + ' a ' + authors[-1] + '.')
    if len(description) > 155:
        description = description[:154].rsplit(' ', 1)[0] + '…'
    href = raccolta_href(r['slug'], page_num)
    canonical = SITE_URL + href
    title_tag = h1 + ('' if page_num == 1 else ' — pagina ' + str(page_num)) + ' | Sottolineature'
    og_image = SITE_URL + '/og-banner.png'

    item_list = {
        '@type': 'ItemList',
        'itemListElement': [
            {'@type': 'ListItem', 'position': (page_num - 1) * PAGE_SIZE + i + 1,
             'url': SITE_URL + '/citazioni/' + s + '/'}
            for i, (s, _) in enumerate(page_items)
        ],
    }
    jsonld = grafo_con_breadcrumb({
        '@type': 'CollectionPage',
        '@id': canonical + '#collectionpage',
        'url': canonical,
        'name': title_tag,
        'description': description,
        'isPartOf': {'@type': 'WebSite', '@id': SITE_URL + '/#website'},
        'mainEntity': item_list,
    }, canonical, SITE_URL, foglia=r['title'], pagina=page_num if page_num > 1 else None)

    link_rel_extra = ''
    if page_num > 1:
        link_rel_extra += '<link rel="prev" href="' + SITE_URL + raccolta_href(r['slug'], page_num - 1) + '">\n'
    if page_num < num_pages:
        link_rel_extra += '<link rel="next" href="' + SITE_URL + raccolta_href(r['slug'], page_num + 1) + '">\n'

    if page_num == 1:
        intro_for_page = intro_html
        breadcrumb_html = ('<a href="/">Sottolineature</a> › <a href="/raccolte/">Raccolte</a> '
                           '› <span aria-current="page">' + title_esc + '</span>')
    else:
        intro_for_page = ('<p>Continua la selezione <a href="/raccolte/' + r['slug'] + '/">' +
                          title_esc + '</a>, curata a mano.</p>')
        breadcrumb_html = ('<a href="/">Sottolineature</a> › <a href="/raccolte/">Raccolte</a> '
                           '› <a href="/raccolte/' + r['slug'] + '/">' + title_esc + '</a> '
                           '› <span aria-current="page">Pagina ' + str(page_num) + '</span>')

    start = (page_num - 1) * PAGE_SIZE + 1
    end = start + len(page_items) - 1
    pagination_html = build_pagination_html(r['slug'], page_num, num_pages)

    return PAGE_TEMPLATE.format(
        title_tag=html.escape(title_tag),
        description=html.escape(description),
        canonical=canonical,
        link_rel_extra=link_rel_extra,
        og_image=og_image,
        jsonld=jsonld,
        breadcrumb_html=breadcrumb_html,
        h1=html.escape(h1 + ('' if page_num == 1 else ' — pagina ' + str(page_num))),
        count_line=(str(total) + ' citazion' + count_suffix + ' scelte a mano · pagina ' +
                    str(page_num) + ' di ' + str(num_pages)),
        intro_html=intro_for_page,
        # Le 34 raccolte non avevano nessun H2: il titolo, l'introduzione e
        # poi le schede, senza un'intestazione che dicesse dove comincia
        # l'elenco. «Righe» e non «citazioni», che sta gia' nell'H1.
        h2_lista=('<h2 class="lista-h2 sans">Righe ' + str(start) + '–' + str(end) +
                  ' di ' + str(total) + '</h2>'),
        cards_html=cards_html + pagination_html,
    )


def main(entries):
    """`entries` = le coppie (slug, q) gia' renderizzate da generate_quote_pages."""
    raccolte = load_raccolte()
    by_key = {quote_key(q): (s, q) for s, q in entries}

    os.makedirs(OUT_DIR, exist_ok=True)
    raccolta_status = {}
    generated_files = set()
    for r in raccolte:
        items = [by_key[k] for k in r['quote_keys'] if k in by_key]
        missing = [k for k in r['quote_keys'] if k not in by_key]
        if missing:
            print('ATTENZIONE: chiavi non trovate per raccolta', r['slug'], '-', missing)
        if len(items) < MIN_QUOTES:
            print('ATTENZIONE: raccolta', r['slug'], 'sotto la soglia di', MIN_QUOTES, 'citazioni - non pubblicata')
            continue
        chunks = [items[i:i + PAGE_SIZE] for i in range(0, len(items), PAGE_SIZE)]
        for page_num, page_items in enumerate(chunks, 1):
            page = render_raccolta(r, page_items, len(items), page_num, len(chunks))
            relpath = (r['slug'] + '.html' if page_num == 1 else
                       os.path.join(r['slug'], str(page_num), 'index.html'))
            output_path = os.path.join(OUT_DIR, relpath)
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(page)
            generated_files.add(relpath)
        raccolta_status[r['slug']] = len(items)

    # index.html della cartella e' l'indice, lo scrive generate_index_pages:
    # non e' una pagina orfana
    removed = []
    for dirpath, dirnames, filenames in os.walk(OUT_DIR, topdown=False):
        for fname in filenames:
            if not fname.endswith('.html'):
                continue
            path = os.path.join(dirpath, fname)
            relpath = os.path.relpath(path, OUT_DIR)
            if relpath == 'index.html' or relpath in generated_files:
                continue
            try:
                os.remove(path)
                removed.append(relpath)
            except OSError as err:
                print('Attenzione: non ho potuto rimuovere', relpath, '-', err)
        for dirname in dirnames:
            path = os.path.join(dirpath, dirname)
            try:
                os.rmdir(path)
            except OSError:
                pass
    if removed:
        print('Rimosse pagine raccolta obsolete:', len(removed))

    print('Raccolte generate:', len(raccolta_status), '/', len(raccolte),
          'in', len(generated_files), 'pagine')
    return raccolta_status


if __name__ == '__main__':
    from generate_quote_pages import load_quotes, load_slugs, load_redirects, assign_slugs
    quotes = load_quotes()
    entries, _ = assign_slugs(quotes, load_slugs(), load_redirects())
    main(entries)
