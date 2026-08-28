#!/usr/bin/env python3
"""Genera pagine hub per tema (umore), genere e autore.

Uso: python3 tools/generate_hub_pages.py
Dipende dallo stesso parsing di generate_quote_pages.py; rilegge index.html
ogni volta, ricostruisce temi/*.html, generi/*.html, autori/*.html da zero.
"""
import html
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate_quote_pages import (  # noqa: E402
    ROOT, INDEX, SITE_URL, parse_cards, slugify, assign_slugs, load_slugs, save_slugs, load_redirects,
)
from labels import CATEGORY_LABELS, GENRE_LABELS  # noqa: E402

HUB_TEMPLATE = """<!DOCTYPE html>
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
<script>
  try {{
    var savedTheme = localStorage.getItem('sottolineature-theme');
    if (savedTheme === 'dark') {{ document.documentElement.setAttribute('data-theme', 'dark'); }}
  }} catch (e) {{}}
</script>
</head>
<body>
<button class="theme-toggle" id="themeToggle" type="button" aria-label="Cambia tema chiaro/scuro">☾</button>
<nav class="site-nav sans">
  <a href="/">Citazioni</a>
  <a href="/metodo/">Metodo</a>
</nav>
<div class="page">
  <a class="back-link sans" href="/">← Tutte le citazioni</a>
  <p class="eyebrow sans">{eyebrow}</p>
  <h1>{h1}</h1>
  <p class="count sans">{count} citazion{count_suffix}</p>
  {nav_html}
  {cards_html}
  <footer class="sans">
    Da <a href="/" style="color:var(--ink-faint)">Sottolineature</a> — citazioni verificate a mano, senza algoritmo.
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


def render_hub(kind, slug, label, items, nav_links, current_href):
    count = len(items)
    count_suffix = 'i' if count != 1 else 'e'
    cards_html = '\n  '.join(card_html(s, q) for s, q in items)

    nav_items = ''.join(
        '<a href="' + href + '"' + (' class="is-current"' if href == current_href else '') + '>' + html.escape(text) + '</a>'
        for text, href in nav_links
    )
    nav_html = '<nav class="hub-nav sans">' + nav_items + '</nav>'

    if kind == 'tema':
        eyebrow = 'Un umore'
        h1 = 'Citazioni sull’amore' if label.lower() == 'amore' else 'Citazioni su ' + label.lower()
        description = 'Le citazioni raccolte su Sottolineature che parlano di ' + label.lower() + ': ' + str(count) + ' righe scelte a mano da romanzi, poesie e saggi.'
    elif kind == 'genere':
        eyebrow = 'Un genere'
        h1 = 'Citazioni ' + label.lower() if label != 'Saggistica' else 'Citazioni di saggistica'
        description = 'Le citazioni di ' + label.lower() + ' raccolte su Sottolineature: ' + str(count) + ' righe scelte a mano da romanzi e racconti del genere.'
    else:
        eyebrow = 'Un autore'
        h1 = label
        description = 'Le citazioni di ' + label + ' raccolte su Sottolineature: ' + str(count) + ' rig' + ('a' if count == 1 else 'he') + ' scelt' + ('a' if count == 1 else 'e') + ' a mano, verificat' + ('a' if count == 1 else 'e') + ' sulle fonti.'

    dir_by_kind = {'tema': 'temi', 'genere': 'generi', 'autore': 'autori'}
    canonical = SITE_URL + '/' + dir_by_kind[kind] + '/' + slug + '/'
    title_tag = h1 + ' | Sottolineature'

    return HUB_TEMPLATE.format(
        title_tag=html.escape(title_tag),
        description=html.escape(description),
        canonical=canonical,
        og_image=SITE_URL + '/og-banner.png',
        eyebrow=html.escape(eyebrow),
        h1=html.escape(h1),
        count=count,
        count_suffix=count_suffix,
        nav_html=nav_html,
        cards_html=cards_html,
    )


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
    with open(INDEX, encoding='utf-8') as f:
        content = f.read()
    quotes = parse_cards(content)

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

    # --- Temi (umore) ---
    temi_dir = os.path.join(ROOT, 'temi')
    os.makedirs(temi_dir, exist_ok=True)
    tema_nav = [(CATEGORY_LABELS[c], '/temi/' + c + '/') for c in CATEGORY_LABELS]
    tema_slugs = []
    for cat, label in CATEGORY_LABELS.items():
        items = [(s, q) for s, q in entries if q['category'] == cat]
        if not items:
            continue
        page = render_hub('tema', cat, label, items, tema_nav, '/temi/' + cat + '/')
        with open(os.path.join(temi_dir, cat + '.html'), 'w', encoding='utf-8') as f:
            f.write(page)
        tema_slugs.append(cat)
    print('Pagine tema generate:', len(tema_slugs))

    # --- Generi ---
    generi_dir = os.path.join(ROOT, 'generi')
    os.makedirs(generi_dir, exist_ok=True)
    genere_nav = [(GENRE_LABELS[g], '/generi/' + g + '/') for g in GENRE_LABELS]
    genere_slugs = []
    for gen, label in GENRE_LABELS.items():
        items = [(s, q) for s, q in entries if gen in (q['genre'] or '').split(' ')]
        if not items:
            continue
        page = render_hub('genere', gen, label, items, genere_nav, '/generi/' + gen + '/')
        with open(os.path.join(generi_dir, gen + '.html'), 'w', encoding='utf-8') as f:
            f.write(page)
        genere_slugs.append(gen)
    print('Pagine genere generate:', len(genere_slugs))

    # --- Autori ---
    autori_dir = os.path.join(ROOT, 'autori')
    os.makedirs(autori_dir, exist_ok=True)
    by_author = {}
    for s, q in entries:
        by_author.setdefault(q['author'], []).append((s, q))

    existing_author_files = set(os.listdir(autori_dir)) if os.path.isdir(autori_dir) else set()

    for author, items in by_author.items():
        aslug = author_slugs[author]
        page = render_hub('autore', aslug, author, items, [], '')
        with open(os.path.join(autori_dir, aslug + '.html'), 'w', encoding='utf-8') as f:
            f.write(page)
    generated_author_files = set(author_slugs[a] + '.html' for a in by_author)
    stale = existing_author_files - generated_author_files
    for fname in stale:
        if fname.endswith('.html'):
            os.remove(os.path.join(autori_dir, fname))
    print('Pagine autore generate:', len(by_author), '(rimosse obsolete:', len(stale), ')')

    return entries, author_slugs, tema_slugs, genere_slugs


if __name__ == '__main__':
    main()
