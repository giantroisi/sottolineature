#!/usr/bin/env python3
"""Genera le pagine indice che oggi mancano (Fase 2 SEO.md): /citazioni/
(paginata), /autori/ (A-Z), /temi/, /generi/. Prima erano vicoli ciechi:
nessuna pagina elencava tutte le citazioni, tutti gli autori o tutti gli hub.

Uso: python3 tools/generate_index_pages.py (chiamato da build.py)
"""
import html
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate_quote_pages import ROOT, SITE_URL  # noqa: E402
from labels import CATEGORY_LABELS, GENRE_LABELS  # noqa: E402

PAGE_SIZE = 30

PAGE_SHELL = """<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="color-scheme" content="light dark">
<meta name="theme-color" content="#f2f0eb">
<title>{title_tag}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
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
{link_rel_extra}<script type="application/ld+json">{jsonld}</script>
<script>
  try {{
    var savedTheme = localStorage.getItem('sottolineature-theme');
    if (savedTheme === 'dark') {{ document.documentElement.setAttribute('data-theme', 'dark'); }}
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
    <form class="header-search sans" action="/" method="get" role="search">
      <label class="visually-hidden" for="headerSearch">Cerca fra le citazioni</label>
      <input type="search" id="headerSearch" name="q" placeholder="Cerca autore, parola o frase…" autocomplete="off">
    </form>
    <nav class="site-nav sans" aria-label="Principale">
      <a href="/citazioni/">Citazioni</a>
      <a href="/autori/">Autori</a>
      <a href="/temi/">Temi</a>
      <a href="/le-mie-sottolineature/" id="navMine">Le mie</a>
      <a href="/metodo/">Metodo</a>
      <button class="theme-toggle" id="themeToggle" type="button" aria-label="Cambia tema chiaro/scuro">☾</button>
    </nav>
  </div>
</header>
<script src="/assets/nav.js" defer></script>
<div class="page">
  <a class="back-link sans" href="/">← Torna alla home</a>
  <p class="eyebrow sans">{eyebrow}</p>
  <h1>{h1}</h1>
  <p class="count sans">{count_line}</p>
  {body_html}
  <footer class="sans">
    Da <a href="/" style="color:var(--ink-faint)">Sottolineature</a> — citazioni verificate a mano, senza algoritmo. <a href="/feed.xml" style="color:var(--ink-faint)">Segui le nuove citazioni</a>.
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


def write_page(path, **kwargs):
    kwargs.setdefault('link_rel_extra', '')
    kwargs.setdefault('og_image', SITE_URL + '/og-banner.png')
    page = PAGE_SHELL.format(**kwargs)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(page)


def generate_citazioni_index(entries):
    """/citazioni/ paginata, 30 per pagina, ognuna self-canonical."""
    out_dir = os.path.join(ROOT, 'citazioni')
    total = len(entries)
    pages = [entries[i:i + PAGE_SIZE] for i in range(0, total, PAGE_SIZE)]
    num_pages = len(pages)
    urls = []

    for i, page_entries in enumerate(pages):
        page_num = i + 1
        href = '/citazioni/' if page_num == 1 else '/citazioni/' + str(page_num) + '/'
        canonical = SITE_URL + href
        path = os.path.join(out_dir, 'index.html') if page_num == 1 else os.path.join(out_dir, str(page_num), 'index.html')

        items_html = '\n  '.join(
            '<article class="card"><span class="card-mark" aria-hidden="true">“</span>'
            '<div class="card-body"><p class="card-quote"><a href="/citazioni/' + s + '/">' + html.escape(q['quote']) + '</a></p>'
            '<p class="card-citation sans"><a href="/citazioni/' + s + '/">'
            '<span class="card-author">' + html.escape(q['author']) + '</span> — '
            '<span class="card-title">' + html.escape(q['title']) + '</span></a></p></div></article>'
            for s, q in page_entries
        )

        pag_links = []
        if page_num > 1:
            prev_href = '/citazioni/' if page_num == 2 else '/citazioni/' + str(page_num - 1) + '/'
            pag_links.append('<a href="' + prev_href + '">← Pagina precedente</a>')
        if page_num < num_pages:
            pag_links.append('<a href="/citazioni/' + str(page_num + 1) + '/">Pagina successiva →</a>')
        pagination_html = '<nav class="hub-nav sans">' + ''.join(pag_links) + '</nav>' if pag_links else ''

        link_rel_extra = ''
        if page_num > 1:
            prev_href = '/citazioni/' if page_num == 2 else '/citazioni/' + str(page_num - 1) + '/'
            link_rel_extra += '<link rel="prev" href="' + SITE_URL + prev_href + '">\n'
        if page_num < num_pages:
            link_rel_extra += '<link rel="next" href="' + SITE_URL + '/citazioni/' + str(page_num + 1) + '/">\n'

        title_tag = 'Tutte le citazioni' + ('' if page_num == 1 else ' — pagina ' + str(page_num)) + ' | Sottolineature'
        description = ('Tutte le ' + str(total) + ' citazioni raccolte su Sottolineature' +
                        ('.' if page_num == 1 else ', pagina ' + str(page_num) + ' di ' + str(num_pages) + '.'))

        item_list = {
            '@type': 'ItemList',
            'itemListElement': [
                {'@type': 'ListItem', 'position': i * PAGE_SIZE + j + 1, 'url': SITE_URL + '/citazioni/' + s + '/'}
                for j, (s, _) in enumerate(page_entries)
            ],
        }
        jsonld = json.dumps({
            '@context': 'https://schema.org',
            '@type': 'CollectionPage',
            '@id': canonical + '#collectionpage',
            'url': canonical,
            'name': title_tag,
            'isPartOf': {'@type': 'WebSite', '@id': SITE_URL + '/#website'},
            'mainEntity': item_list,
        }, ensure_ascii=False)

        write_page(
            path,
            title_tag=html.escape(title_tag),
            description=html.escape(description),
            canonical=canonical,
            link_rel_extra=link_rel_extra,
            jsonld=jsonld,
            eyebrow='Archivio',
            h1='Tutte le citazioni' if page_num == 1 else 'Tutte le citazioni — pagina ' + str(page_num),
            count_line=str(total) + ' citazioni, pagina ' + str(page_num) + ' di ' + str(num_pages),
            body_html=items_html + pagination_html,
        )
        urls.append(href)

    print('Pagine /citazioni/ generate:', num_pages, '(', total, 'citazioni,', PAGE_SIZE, 'per pagina )')
    return urls


def generate_autori_index(author_slugs, by_author_count):
    """/autori/ A-Z: elenca tutti gli autori, anche quelli la cui pagina
    singola è in noindex sotto soglia — resta comunque un percorso di
    scansione verso di loro."""
    groups = {}
    for author, slug in author_slugs.items():
        letter = author[0].upper()
        groups.setdefault(letter, []).append((author, slug))

    body_parts = []
    for letter in sorted(groups):
        items = sorted(groups[letter], key=lambda x: x[0])
        lis = ''.join(
            '<li><a href="/autori/' + slug + '/">' + html.escape(author) + '</a> '
            '<span class="sans" style="color:var(--ink-faint)">(' + str(by_author_count.get(author, 0)) + ')</span></li>'
            for author, slug in items
        )
        body_parts.append('<h2 class="sans" style="font-size:0.85rem;letter-spacing:0.08em;text-transform:uppercase;color:var(--gold);margin:2rem 0 0.6rem">' + letter + '</h2><ul class="related-list index-list" style="list-style:none;margin:0;padding:0">' + lis + '</ul>')

    canonical = SITE_URL + '/autori/'
    title_tag = 'Tutti gli autori | Sottolineature'
    description = 'Indice alfabetico dei ' + str(len(author_slugs)) + ' autori con almeno una citazione su Sottolineature.'

    item_list = {
        '@type': 'ItemList',
        'itemListElement': [
            {'@type': 'ListItem', 'position': i + 1, 'url': SITE_URL + '/autori/' + slug + '/', 'name': author}
            for i, (author, slug) in enumerate(sorted(author_slugs.items(), key=lambda x: x[0]))
        ],
    }
    jsonld = json.dumps({
        '@context': 'https://schema.org',
        '@type': 'CollectionPage',
        '@id': canonical + '#collectionpage',
        'url': canonical,
        'name': title_tag,
        'isPartOf': {'@type': 'WebSite', '@id': SITE_URL + '/#website'},
        'mainEntity': item_list,
    }, ensure_ascii=False)

    write_page(
        os.path.join(ROOT, 'autori', 'index.html'),
        title_tag=html.escape(title_tag),
        description=html.escape(description),
        canonical=canonical,
        jsonld=jsonld,
        eyebrow='Indice',
        h1='Tutti gli autori',
        count_line=str(len(author_slugs)) + ' autori',
        body_html=''.join(body_parts),
    )
    print('Pagina /autori/ generata (', len(author_slugs), 'autori )')


def generate_taxonomy_index(kind, labels, counts):
    """/temi/ o /generi/: elenco degli hub con conteggio."""
    dir_name = 'temi' if kind == 'tema' else 'generi'
    lis = ''.join(
        '<li><a href="/' + dir_name + '/' + slug + '/">' + html.escape(label) + '</a> '
        '<span class="sans" style="color:var(--ink-faint)">(' + str(counts.get(slug, 0)) + ')</span></li>'
        for slug, label in labels.items() if counts.get(slug, 0) > 0
    )
    # Queste due erano le uniche pagine indice senza una riga di testo: una
    # cinquantina di parole in tutto, contando il menu. Un elenco di link e
    # basta non dice a nessuno - lettore o motore di ricerca - che cosa sta
    # guardando ne' perche' le etichette sono queste e non altre.
    if kind == 'tema':
        intro = (
            '<p class="index-intro">Non sono categorie rigide: la stessa pagina pu\u00f2 riconoscersi '
            'in pi\u00f9 di un tema, e nessuna citazione entra in un tema per riempirlo \u2014 '
            'l\u2019etichetta arriva dopo la lettura, non prima. Sette in tutto, perch\u00e9 un '
            'ottavo avrebbe voluto dire spezzare il capello.</p>')
    else:
        intro = (
            '<p class="index-intro">I generi valgono quando dicono qualcosa: un romanzo di '
            'fantascienza e un saggio non si leggono allo stesso modo. Sono pochi di proposito \u2014 '
            'ne entra uno solo se ha almeno quattro titoli dietro, altrimenti \u00e8 un\u2019etichetta '
            'che sta in piedi da sola.</p>')
    body_html = intro + '<ul class="index-list" style="list-style:none;margin:0;padding:0;font-size:1.1rem;line-height:2.2">' + lis + '</ul>'

    canonical = SITE_URL + '/' + dir_name + '/'
    label_word = 'temi' if kind == 'tema' else 'generi'
    title_tag = ('Tutti i temi' if kind == 'tema' else 'Tutti i generi') + ' | Sottolineature'
    if kind == 'tema':
        description = ('I sette temi in cui si raggruppano le citazioni di Sottolineature. Non una '
                       'classificazione rigida: la stessa pagina pu\u00f2 stare in pi\u00f9 di un tema.')
    else:
        description = ('I generi dell\u2019archivio di Sottolineature: fantasy, fantascienza, distopia, '
                       'horror, saggistica. Ne entra uno solo se ha almeno quattro titoli dietro.')

    item_list = {
        '@type': 'ItemList',
        'itemListElement': [
            {'@type': 'ListItem', 'position': i + 1, 'url': SITE_URL + '/' + dir_name + '/' + slug + '/', 'name': label}
            for i, (slug, label) in enumerate(labels.items()) if counts.get(slug, 0) > 0
        ],
    }
    jsonld = json.dumps({
        '@context': 'https://schema.org',
        '@type': 'CollectionPage',
        '@id': canonical + '#collectionpage',
        'url': canonical,
        'name': title_tag,
        'isPartOf': {'@type': 'WebSite', '@id': SITE_URL + '/#website'},
        'mainEntity': item_list,
    }, ensure_ascii=False)

    write_page(
        os.path.join(ROOT, dir_name, 'index.html'),
        title_tag=html.escape(title_tag),
        description=html.escape(description),
        canonical=canonical,
        jsonld=jsonld,
        eyebrow='Indice',
        h1='Tutti i temi' if kind == 'tema' else 'Tutti i generi',
        count_line=str(sum(1 for s in labels if counts.get(s, 0) > 0)) + (' temi' if kind == 'tema' else ' generi'),
        body_html=body_html,
    )
    print('Pagina /' + dir_name + '/ generata')


def generate_opere_index(opere, opera_status):
    """/opere/: elenco delle opere con pagina propria, raggruppate per
    autore. Le opere sotto soglia (nessuna citazione trovata) non compaiono:
    opera_status contiene solo quelle effettivamente generate."""
    published = [o for o in opere if o['slug'] in opera_status]
    by_author = {}
    for o in published:
        by_author.setdefault(o['author'], []).append(o)

    lis = ''.join(
        '<li><a href="/opere/' + o['slug'] + '/">' + html.escape(o['title']) + '</a> '
        '<span class="sans" style="color:var(--ink-faint)">— ' + html.escape(author) + '</span></li>'
        for author in sorted(by_author)
        for o in by_author[author]
    )
    body_html = '<ul class="index-list" style="list-style:none;margin:0;padding:0;font-size:1.1rem;line-height:2.2">' + lis + '</ul>'

    canonical = SITE_URL + '/opere/'
    title_tag = 'Tutte le opere | Sottolineature'
    description = 'Indice delle ' + str(len(published)) + ' opere con una pagina dedicata su Sottolineature: scheda editoriale e tutte le citazioni di ciascun libro.'

    item_list = {
        '@type': 'ItemList',
        'itemListElement': [
            {'@type': 'ListItem', 'position': i + 1, 'url': SITE_URL + '/opere/' + o['slug'] + '/', 'name': o['title']}
            for i, o in enumerate(published)
        ],
    }
    jsonld = json.dumps({
        '@context': 'https://schema.org',
        '@type': 'CollectionPage',
        '@id': canonical + '#collectionpage',
        'url': canonical,
        'name': title_tag,
        'isPartOf': {'@type': 'WebSite', '@id': SITE_URL + '/#website'},
        'mainEntity': item_list,
    }, ensure_ascii=False)

    write_page(
        os.path.join(ROOT, 'opere', 'index.html'),
        title_tag=html.escape(title_tag),
        description=html.escape(description),
        canonical=canonical,
        jsonld=jsonld,
        eyebrow='Indice',
        h1='Tutte le opere',
        count_line=str(len(published)) + ' opere',
        body_html=body_html,
    )
    print('Pagina /opere/ generata (', len(published), 'opere )')


def generate_raccolte_index(raccolte, raccolta_status):
    """/raccolte/: elenco delle raccolte curate a mano effettivamente
    pubblicate (>=8 citazioni pertinenti, vedi generate_raccolte_pages)."""
    published = [r for r in raccolte if r['slug'] in raccolta_status]
    lis = ''.join(
        '<li><a href="/raccolte/' + r['slug'] + '/">' + html.escape(r['title']) + '</a> '
        '<span class="sans" style="color:var(--ink-faint)">(' + str(raccolta_status[r['slug']]) + ')</span></li>'
        for r in published
    )
    body_html = '<ul class="index-list" style="list-style:none;margin:0;padding:0;font-size:1.1rem;line-height:2.2">' + lis + '</ul>'

    canonical = SITE_URL + '/raccolte/'
    title_tag = 'Tutte le raccolte | Sottolineature'
    description = 'Selezioni curate a mano di citazioni su Sottolineature, con introduzione scritta: ' + str(len(published)) + ' raccolte.'

    item_list = {
        '@type': 'ItemList',
        'itemListElement': [
            {'@type': 'ListItem', 'position': i + 1, 'url': SITE_URL + '/raccolte/' + r['slug'] + '/', 'name': r['title']}
            for i, r in enumerate(published)
        ],
    }
    jsonld = json.dumps({
        '@context': 'https://schema.org',
        '@type': 'CollectionPage',
        '@id': canonical + '#collectionpage',
        'url': canonical,
        'name': title_tag,
        'isPartOf': {'@type': 'WebSite', '@id': SITE_URL + '/#website'},
        'mainEntity': item_list,
    }, ensure_ascii=False)

    write_page(
        os.path.join(ROOT, 'raccolte', 'index.html'),
        title_tag=html.escape(title_tag),
        description=html.escape(description),
        canonical=canonical,
        jsonld=jsonld,
        eyebrow='Indice',
        h1='Tutte le raccolte',
        count_line=str(len(published)) + ' raccolte',
        body_html=body_html,
    )
    print('Pagina /raccolte/ generata (', len(published), 'raccolte )')


def main(qp_entries, author_slugs, tema_status, genere_status, opere=None, opera_status=None, raccolte=None, raccolta_status=None):
    citazioni_urls = generate_citazioni_index(qp_entries)

    by_author_count = {}
    for _, q in qp_entries:
        by_author_count[q['author']] = by_author_count.get(q['author'], 0) + 1
    generate_autori_index(author_slugs, by_author_count)

    tema_counts = {}
    for _, q in qp_entries:
        if q['category']:
            tema_counts[q['category']] = tema_counts.get(q['category'], 0) + 1
    generate_taxonomy_index('tema', CATEGORY_LABELS, tema_counts)

    genere_counts = {}
    for _, q in qp_entries:
        for g in (q['genre'] or '').split(' '):
            if g:
                genere_counts[g] = genere_counts.get(g, 0) + 1
    generate_taxonomy_index('genere', GENRE_LABELS, genere_counts)

    if opere is not None and opera_status is not None:
        generate_opere_index(opere, opera_status)
    if raccolte is not None and raccolta_status is not None:
        generate_raccolte_index(raccolte, raccolta_status)

    return citazioni_urls


if __name__ == '__main__':
    import generate_quote_pages as qp
    import generate_hub_pages as hp
    import generate_opera_pages as op
    import generate_raccolte_pages as rp
    entries = qp.main()
    hp_entries, author_slugs, tema_status, genere_status, author_status = hp.main()
    op_status = op.main(entries)
    rc_status = rp.main(entries)
    main(entries, author_slugs, tema_status, genere_status, op.load_opere(), op_status, rp.load_raccolte(), rc_status)
