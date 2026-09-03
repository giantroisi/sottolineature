#!/usr/bin/env python3
"""Genera pagine hub per tema, genere e autore.

Uso: python3 tools/generate_hub_pages.py
Dipende dallo stesso parsing di generate_quote_pages.py; rilegge index.html
ogni volta, ricostruisce temi/*.html, generi/*.html, autori/*.html da zero.
"""
import html
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate_quote_pages import (  # noqa: E402
    ROOT, SITE_URL, load_quotes, slugify, assign_slugs, load_slugs, save_slugs, load_redirects,
)
from labels import CATEGORY_LABELS, GENRE_LABELS  # noqa: E402

HUB_INTROS_PATH = os.path.join(ROOT, 'data', 'hub_intros.json')
SAMEAS_PATH = os.path.join(ROOT, 'data', 'autori_sameas.json')


def load_sameas():
    """Voce di Wikipedia italiana ed elemento Wikidata di ogni autore.

    Serve al nodo Person delle pagine /autori/<slug>/: `sameAs` e' il modo in
    cui un motore di ricerca capisce che il Kafka di questo sito e' quello di
    Wikidata Q905 e non un omonimo. Ogni voce e' stata risolta interrogando
    l'API di Wikipedia e verificata su Wikidata (P31 = essere umano): nessun
    URL e' dedotto dal nome. Un autore assente da questo file semplicemente
    non ha il nodo Person - meglio nessun collegamento che uno sbagliato.
    """
    if os.path.exists(SAMEAS_PATH):
        with open(SAMEAS_PATH, encoding='utf-8') as f:
            return json.load(f)
    return {}


def load_hub_intros():
    """Introduzioni editoriali di 300-600 parole per temi/generi (Fase 5
    SEO.md), scritte a mano una volta e riusate a ogni build."""
    if os.path.exists(HUB_INTROS_PATH):
        with open(HUB_INTROS_PATH, encoding='utf-8') as f:
            return json.load(f)
    return {}

SAMEAS = load_sameas()

HUB_TEMPLATE = """<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="color-scheme" content="light dark">
<meta name="theme-color" content="#f2f0eb">
<title>{title_tag}</title>
<meta name="description" content="{description}">
{robots_meta}<link rel="canonical" href="{canonical}">
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
<script type="application/ld+json">{jsonld}</script>
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
    <form class="header-search sans" action="/" method="get" role="search" aria-label="Cerca dall'intestazione">
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
<div class="page-main" role="main">
  <a class="back-link sans" href="/">← Tutte le citazioni</a>
  <p class="eyebrow sans">{eyebrow}</p>
  <h1>{h1}</h1>
  <p class="count sans">{count} citazion{count_suffix}</p>
  {intro_html}
  {nav_html}
  {cards_html}
  </div>
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


MIN_INDEXABLE_QUOTES = 3


def render_hub(kind, slug, label, items, nav_links, current_href, intro_paragraphs=None):
    count = len(items)
    count_suffix = 'i' if count != 1 else 'e'
    cards_html = '\n  '.join(card_html(s, q) for s, q in items)
    intro_html = (
        '<div class="hub-intro">' +
        ''.join('<p>' + html.escape(p) + '</p>' for p in intro_paragraphs) +
        '</div>'
    ) if intro_paragraphs else ''

    nav_items = ''.join(
        '<a href="' + href + '"' + (' class="is-current"' if href == current_href else '') + '>' + html.escape(text) + '</a>'
        for text, href in nav_links
    )
    nav_html = '<nav class="hub-nav sans">' + nav_items + '</nav>'

    if kind == 'tema':
        eyebrow = 'Un tema'
        # Preposizione articolata corretta per ciascun tema (SEO.md: "Frasi
        # e citazioni sulla libertà", non il generico "su" per tutti).
        preposizione_tema = {
            'vita': 'sulla', 'amore': 'sull’', 'coraggio': 'sul', 'liberta': 'sulla',
            'tempo': 'sul', 'solitudine': 'sulla', 'verita': 'sulla',
        }
        prep = preposizione_tema.get(slug, 'su')
        sep = '' if prep.endswith('’') else ' '
        h1 = 'Citazioni ' + prep + sep + label.lower()
        description = 'Le citazioni raccolte su Sottolineature che parlano di ' + label.lower() + ': ' + str(count) + ' righe scelte a mano da romanzi, poesie e saggi.'
    elif kind == 'genere':
        eyebrow = 'Un genere'
        h1 = 'Citazioni ' + label.lower() if label != 'Saggistica' else 'Citazioni di saggistica'
        description = 'Le citazioni di ' + label.lower() + ' raccolte su Sottolineature: ' + str(count) + ' righe scelte a mano da romanzi e racconti del genere.'
    else:
        eyebrow = 'Un autore'
        # Fase 7 SEO-KEYWORDS.md: le pagine autore avevano H1/title col solo
        # nome, senza "frasi"/"citazioni" — la domanda reale cerca "frasi di
        # Oscar Wilde", non "Oscar Wilde" nudo. Coerente col pattern già in
        # uso per opere ("Frasi e citazioni da {Opera} di {Autore}").
        h1 = 'Frasi e citazioni di ' + label
        description = 'Le citazioni di ' + label + ' raccolte su Sottolineature: ' + str(count) + ' rig' + ('a' if count == 1 else 'he') + ' scelt' + ('a' if count == 1 else 'e') + ' a mano, verificat' + ('a' if count == 1 else 'e') + ' sulle fonti.'

    dir_by_kind = {'tema': 'temi', 'genere': 'generi', 'autore': 'autori'}
    canonical = SITE_URL + '/' + dir_by_kind[kind] + '/' + slug + '/'
    title_tag = h1 + ' | Sottolineature'

    # Gate di indicizzazione (Fase 2 SEO.md): un hub con poche citazioni e
    # nessun testo editoriale proprio non porta valore a un motore di
    # ricerca — resta pubblicato e linkato (percorso di scansione), ma
    # esce dalla sitemap e va in noindex,follow finché non supera la soglia
    # o non riceve un'introduzione scritta a mano (Fase 5/6).
    indexable = count >= MIN_INDEXABLE_QUOTES or bool(intro_paragraphs)
    robots_meta = '' if indexable else '<meta name="robots" content="noindex,follow">\n'

    item_list = {
        '@type': 'ItemList',
        'itemListElement': [
            {
                '@type': 'ListItem',
                'position': i + 1,
                'url': SITE_URL + '/citazioni/' + s + '/',
            }
            for i, (s, _) in enumerate(items)
        ],
    }
    collection_page = {
        '@context': 'https://schema.org',
        '@type': 'CollectionPage',
        '@id': canonical + '#collectionpage',
        'url': canonical,
        'name': title_tag,
        'description': description,
        'isPartOf': {'@type': 'WebSite', '@id': SITE_URL + '/#website'},
        'mainEntity': item_list,
    }
    if kind == 'autore':
        links = SAMEAS.get(label)
        if links:
            collection_page['about'] = {
                '@type': 'Person',
                '@id': canonical + '#person',
                'name': label,
                'sameAs': [links[k] for k in ('wikipedia', 'wikidata') if links.get(k)],
            }
    jsonld = json.dumps(collection_page, ensure_ascii=False)

    return HUB_TEMPLATE.format(
        title_tag=html.escape(title_tag),
        description=html.escape(description),
        robots_meta=robots_meta,
        canonical=canonical,
        og_image=SITE_URL + '/og-banner.png',
        jsonld=jsonld,
        eyebrow=html.escape(eyebrow),
        h1=html.escape(h1),
        count=count,
        count_suffix=count_suffix,
        intro_html=intro_html,
        nav_html=nav_html,
        cards_html=cards_html,
    ), indexable


def assign_author_slugs(authors, slugs_data):
    """Stesso principio di assign_slugs ma per gli autori: legge da slugs.json,
    assegna e persiste uno slug leggibile solo per gli autori nuovi."""
    author_slugs_map = slugs_data.setdefault('authors', {})
    used = set(author_slugs_map.values())
    changed = False
    for author in authors:
        if author in author_slugs_map:
            continue
        slug = slugify(author)
        base = slug
        i = 2
        while slug in used:
            slug = base + '-' + str(i)
            i += 1
        author_slugs_map[author] = slug
        used.add(slug)
        changed = True
    return author_slugs_map, changed


def main():
    quotes = load_quotes()

    slugs_data = load_slugs()
    entries, quotes_changed = assign_slugs(quotes, slugs_data, load_redirects())

    authors_in_order = []
    for _, q in entries:
        if q['author'] not in authors_in_order:
            authors_in_order.append(q['author'])
    author_slugs, authors_changed = assign_author_slugs(authors_in_order, slugs_data)

    if quotes_changed or authors_changed:
        save_slugs(slugs_data)
        print('slugs.json aggiornato (hub)')

    hub_intros = load_hub_intros()

    # --- Temi ---
    temi_dir = os.path.join(ROOT, 'temi')
    os.makedirs(temi_dir, exist_ok=True)
    tema_nav = [(CATEGORY_LABELS[c], '/temi/' + c + '/') for c in CATEGORY_LABELS]
    tema_status = {}
    for cat, label in CATEGORY_LABELS.items():
        items = [(s, q) for s, q in entries if q['category'] == cat]
        if not items:
            continue
        intro = hub_intros.get('temi', {}).get(cat)
        page, indexable = render_hub('tema', cat, label, items, tema_nav, '/temi/' + cat + '/', intro)
        with open(os.path.join(temi_dir, cat + '.html'), 'w', encoding='utf-8') as f:
            f.write(page)
        tema_status[cat] = indexable
    print('Pagine tema generate:', len(tema_status))

    # --- Generi ---
    generi_dir = os.path.join(ROOT, 'generi')
    os.makedirs(generi_dir, exist_ok=True)
    genere_nav = [(GENRE_LABELS[g], '/generi/' + g + '/') for g in GENRE_LABELS]
    genere_status = {}
    for gen, label in GENRE_LABELS.items():
        items = [(s, q) for s, q in entries if gen in (q['genre'] or '').split(' ')]
        if not items:
            continue
        intro = hub_intros.get('generi', {}).get(gen)
        page, indexable = render_hub('genere', gen, label, items, genere_nav, '/generi/' + gen + '/', intro)
        with open(os.path.join(generi_dir, gen + '.html'), 'w', encoding='utf-8') as f:
            f.write(page)
        genere_status[gen] = indexable
    print('Pagine genere generate:', len(genere_status))

    # --- Autori ---
    autori_dir = os.path.join(ROOT, 'autori')
    os.makedirs(autori_dir, exist_ok=True)
    by_author = {}
    for s, q in entries:
        by_author.setdefault(q['author'], []).append((s, q))

    existing_author_files = set(os.listdir(autori_dir)) if os.path.isdir(autori_dir) else set()

    author_status = {}
    for author, items in by_author.items():
        aslug = author_slugs[author]
        intro = hub_intros.get('autori', {}).get(author)
        page, indexable = render_hub('autore', aslug, author, items, [], '', intro)
        with open(os.path.join(autori_dir, aslug + '.html'), 'w', encoding='utf-8') as f:
            f.write(page)
        author_status[aslug] = indexable
    generated_author_files = set(author_slugs[a] + '.html' for a in by_author)
    # index.html non e' un file di questo generatore: lo scrive
    # generate_index_pages.py (l'indice A-Z), va escluso dalla pulizia stale.
    stale = existing_author_files - generated_author_files - {'index.html'}
    for fname in stale:
        if fname.endswith('.html'):
            os.remove(os.path.join(autori_dir, fname))
    print('Pagine autore generate:', len(by_author), '(rimosse obsolete:', len(stale), ')')

    # Agli altri generatori si passa solo la mappa degli autori ANCORA presenti
    # in archivio. slugs.json e' cumulativo per scelta - uno slug assegnato non
    # si cancella mai, cosi' un vecchio indirizzo non diventa una 404 - ma se
    # gli si passa cosi' com'e', l'indice A-Z elenca anche autori le cui pagine
    # non esistono piu'. E' successo con Amelie Nothomb e Thomas Bernhard.
    current_author_slugs = {a: author_slugs[a] for a in by_author if a in author_slugs}

    return entries, current_author_slugs, tema_status, genere_status, author_status


if __name__ == '__main__':
    main()
