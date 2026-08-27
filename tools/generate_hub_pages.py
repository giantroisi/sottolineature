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
from generate_quote_pages import ROOT, INDEX, SITE_URL, parse_cards, slugify, make_slug  # noqa: E402
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
<link rel="icon" type="image/svg+xml" href="{root}favicon.svg">
<link rel="icon" type="image/png" sizes="32x32" href="{root}favicon-32.png">
<link rel="icon" type="image/png" sizes="16x16" href="{root}favicon-16.png">
<link rel="apple-touch-icon" href="{root}apple-touch-icon.png">
<style>
  :root {{
    color-scheme: light;
    --paper: #f2f0eb;
    --paper-raised: #f8f7f3;
    --ink: #211f1b;
    --ink-soft: #5b564d;
    --ink-faint: #8c8577;
    --accent: #33523f;
    --accent-soft: #6b8574;
    --gold: #9c7a3c;
    --rule: #ddd9cf;
    --shadow: rgba(33, 31, 27, 0.08);
  }}
  :root[data-theme="dark"] {{
    color-scheme: dark;
    --paper: #16191a;
    --paper-raised: #1f2224;
    --ink: #ece7dd;
    --ink-soft: #a9a296;
    --ink-faint: #746e62;
    --accent: #8fb59b;
    --accent-soft: #5c7c68;
    --gold: #c9a45c;
    --rule: #33362f;
    --shadow: rgba(0, 0, 0, 0.4);
  }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0;
    background: var(--paper);
    color: var(--ink);
    font-family: "Iowan Old Style", "Palatino Linotype", Palatino, Georgia, "Times New Roman", serif;
    -webkit-font-smoothing: antialiased;
  }}
  .sans {{ font-family: ui-sans-serif, -apple-system, BlinkMacSystemFont, "Helvetica Neue", Arial, sans-serif; }}
  .page {{ max-width: 42rem; margin: 0 auto; padding: 4.5rem 1.75rem 6rem; }}
  .back-link {{
    display: inline-block;
    font-size: 0.85rem;
    color: var(--ink-soft);
    text-decoration: none;
    border-bottom: 1px solid var(--accent-soft);
    margin-bottom: 2.5rem;
  }}
  .back-link:hover {{ color: var(--gold); border-color: var(--gold); }}
  .theme-toggle {{
    all: unset;
    position: fixed;
    top: 1.1rem;
    left: 1.1rem;
    z-index: 20;
    width: 2.4rem;
    height: 2.4rem;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    background: var(--paper-raised);
    border: 1px solid var(--rule);
    border-radius: 50%;
    color: var(--ink-soft);
    font-size: 1.1rem;
    line-height: 1;
    box-shadow: 0 1px 3px var(--shadow);
  }}
  .theme-toggle:hover {{ color: var(--gold); border-color: var(--gold); }}
  .eyebrow {{
    font-size: 0.72rem;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: var(--gold);
    margin: 0 0 0.9rem;
  }}
  h1 {{ font-weight: 400; font-size: clamp(1.8rem, 4vw, 2.4rem); margin: 0 0 0.75rem; line-height: 1.2; }}
  .count {{ font-size: 0.95rem; color: var(--ink-faint); margin: 0 0 2.5rem; }}
  .card {{
    display: flex;
    align-items: flex-start;
    gap: 0.9rem;
    position: relative;
    margin: 0 0 2rem;
    padding: 0.1rem 0 0.1rem 1.35rem;
    border-left: 2px solid var(--rule);
  }}
  .card-mark {{
    position: absolute; left: -0.15rem; top: -1.1rem;
    font-size: 3rem; font-family: Georgia, serif; color: var(--gold); opacity: 0.35; line-height: 1;
  }}
  .card-quote {{ font-size: 1.05rem; line-height: 1.55; font-style: italic; margin: 0 0 0.6rem; }}
  .card-quote a {{ color: inherit; text-decoration: none; }}
  .card-quote a:hover {{ color: var(--accent); }}
  .card-citation {{ font-size: 0.85rem; color: var(--ink-soft); margin: 0; }}
  .card-citation .card-title {{ font-style: italic; }}
  .card-citation a {{ color: inherit; text-decoration: none; border-bottom: 1px solid var(--accent-soft); }}
  .card-citation a:hover {{ color: var(--gold); border-color: var(--gold); }}
  .hub-nav {{ margin-bottom: 3rem; display: flex; flex-wrap: wrap; gap: 0.6rem 1rem; }}
  .hub-nav a {{
    font-size: 0.78rem;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: var(--ink-faint);
    text-decoration: none;
    border-bottom: 1px solid transparent;
  }}
  .hub-nav a:hover, .hub-nav a.is-current {{ color: var(--accent); border-color: var(--accent); }}
  footer.sans {{
    margin-top: 3.5rem;
    padding-top: 1.75rem;
    border-top: 1px solid var(--rule);
    font-size: 0.85rem;
    color: var(--ink-faint);
  }}
</style>
<script>
  try {{
    var savedTheme = localStorage.getItem('sottolineature-theme');
    if (savedTheme === 'dark') {{ document.documentElement.setAttribute('data-theme', 'dark'); }}
  }} catch (e) {{}}
</script>
</head>
<body>
<button class="theme-toggle" id="themeToggle" type="button" aria-label="Cambia tema chiaro/scuro">☾</button>
<div class="page">
  <a class="back-link sans" href="{root}index.html">← Tutte le citazioni</a>
  <p class="eyebrow sans">{eyebrow}</p>
  <h1>{h1}</h1>
  <p class="count sans">{count} citazion{count_suffix}</p>
  {nav_html}
  {cards_html}
  <footer class="sans">
    Da <a href="{root}index.html" style="color:var(--ink-faint)">Sottolineature</a> — citazioni verificate a mano, senza algoritmo.
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
        '<p class="card-quote"><a href="../citazioni/' + slug + '.html">' + html.escape(q['quote']) + '</a></p>'
        '<p class="card-citation sans"><a href="../citazioni/' + slug + '.html">'
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
    canonical = SITE_URL + '/' + dir_by_kind[kind] + '/' + slug + '.html'
    title_tag = h1 + ' | Sottolineature'

    return HUB_TEMPLATE.format(
        title_tag=html.escape(title_tag),
        description=html.escape(description),
        canonical=canonical,
        og_image=SITE_URL + '/og-banner.png',
        root='../',
        eyebrow=html.escape(eyebrow),
        h1=html.escape(h1),
        count=count,
        count_suffix=count_suffix,
        nav_html=nav_html,
        cards_html=cards_html,
    )


def main():
    with open(INDEX, encoding='utf-8') as f:
        content = f.read()
    quotes = parse_cards(content)

    used_slugs = set()
    entries = []
    for q in quotes:
        if not q['author'] or not q['quote']:
            continue
        slug = make_slug(q['author'], q['title'], used_slugs)
        entries.append((slug, q))

    # --- Temi (umore) ---
    temi_dir = os.path.join(ROOT, 'temi')
    os.makedirs(temi_dir, exist_ok=True)
    tema_nav = [(CATEGORY_LABELS[c], c + '.html') for c in CATEGORY_LABELS]
    tema_slugs = []
    for cat, label in CATEGORY_LABELS.items():
        items = [(s, q) for s, q in entries if q['category'] == cat]
        if not items:
            continue
        page = render_hub('tema', cat, label, items, tema_nav, cat + '.html')
        with open(os.path.join(temi_dir, cat + '.html'), 'w', encoding='utf-8') as f:
            f.write(page)
        tema_slugs.append(cat)
    print('Pagine tema generate:', len(tema_slugs))

    # --- Generi ---
    generi_dir = os.path.join(ROOT, 'generi')
    os.makedirs(generi_dir, exist_ok=True)
    genere_nav = [(GENRE_LABELS[g], g + '.html') for g in GENRE_LABELS]
    genere_slugs = []
    for gen, label in GENRE_LABELS.items():
        items = [(s, q) for s, q in entries if gen in (q['genre'] or '').split(' ')]
        if not items:
            continue
        page = render_hub('genere', gen, label, items, genere_nav, gen + '.html')
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
    used_author_slugs = set()
    author_slugs = {}
    for author in by_author:
        aslug = slugify(author)
        base = aslug
        i = 2
        while aslug in used_author_slugs:
            aslug = base + '-' + str(i)
            i += 1
        used_author_slugs.add(aslug)
        author_slugs[author] = aslug

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
