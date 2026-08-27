#!/usr/bin/env python3
"""Genera una pagina HTML dedicata per ogni citazione in index.html.

Uso: python3 tools/generate_quote_pages.py
Rilegge index.html, ricostruisce citazioni/*.html da zero ogni volta:
non modificare le pagine generate a mano, si perderebbero al prossimo giro.
"""
import html
import json
import os
import re
import sys
import unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from labels import CATEGORY_LABELS, GENRE_LABELS  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX = os.path.join(ROOT, 'index.html')
OUT_DIR = os.path.join(ROOT, 'citazioni')
SITE_URL = 'https://sottolineature.it'


def slugify(text):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text


def strip_tags(s):
    return re.sub(r'<[^<]+?>', '', s).strip()


def parse_cards(content):
    raw_cards = re.findall(r'<article class="card"(.*?)</article>', content, re.S)
    quotes = []
    for raw in raw_cards:
        cat_m = re.search(r'data-category="([^"]*)"', raw)
        genre_m = re.search(r'data-genre="([^"]*)"', raw)
        quote_m = re.search(r'<p class="card-quote">(.*?)</p>', raw, re.S)
        author_m = re.search(r'<span class="card-author">(.*?)</span>', raw, re.S)
        title_m = re.search(r'<span class="card-title">(.*?)</span>', raw, re.S)
        year_m = re.search(r'<span class="card-year">(.*?)</span>', raw, re.S)
        context_m = re.search(r'<p class="card-context sans">(.*?)</p>', raw, re.S)
        cover_m = re.search(r'<img class="card-cover" src="([^"]+)"', raw)

        quotes.append({
            'quote': html.unescape(strip_tags(quote_m.group(1))) if quote_m else '',
            'author': html.unescape(strip_tags(author_m.group(1))) if author_m else '',
            'title': html.unescape(strip_tags(title_m.group(1))) if title_m else '',
            'year': html.unescape(strip_tags(year_m.group(1))) if year_m else '',
            'context': html.unescape(strip_tags(context_m.group(1))) if context_m else '',
            'cover': cover_m.group(1) if cover_m else '',
            'category': cat_m.group(1) if cat_m else '',
            'genre': genre_m.group(1) if genre_m else '',
        })
    return quotes


def make_slug(author, title, used):
    base = slugify(author + '-' + title)
    slug = base
    i = 2
    while slug in used:
        slug = base + '-' + str(i)
        i += 1
    used.add(slug)
    return slug


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
<meta property="og:title" content="{og_title}">
<meta property="og:description" content="{description}">
<meta property="og:image" content="{og_image}">
<meta property="og:url" content="{canonical}">
<meta property="og:site_name" content="Sottolineature">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{og_title}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="{og_image}">
<link rel="icon" type="image/svg+xml" href="../favicon.svg">
<link rel="icon" type="image/png" sizes="32x32" href="../favicon-32.png">
<link rel="icon" type="image/png" sizes="16x16" href="../favicon-16.png">
<link rel="apple-touch-icon" href="../apple-touch-icon.png">
<script type="application/ld+json">{jsonld}</script>
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
    text-rendering: optimizeLegibility;
  }}
  .sans {{ font-family: ui-sans-serif, -apple-system, BlinkMacSystemFont, "Helvetica Neue", Arial, sans-serif; }}
  .page {{ max-width: 38rem; margin: 0 auto; padding: 4.5rem 1.75rem 6rem; }}
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
  .theme-toggle:focus-visible {{ outline: 2px solid var(--accent); outline-offset: 2px; }}
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
    position: absolute;
    left: -0.15rem;
    top: -1.1rem;
    font-size: 3rem;
    font-family: Georgia, serif;
    color: var(--gold);
    opacity: 0.35;
    line-height: 1;
  }}
  .card-quote {{
    font-size: clamp(1.15rem, 2.6vw, 1.4rem);
    line-height: 1.55;
    font-style: italic;
    margin: 0 0 0.9rem;
  }}
  .card-citation {{ font-size: 0.9rem; color: var(--ink-soft); margin: 0 0 0.7rem; }}
  .card-citation .card-title {{ font-style: italic; }}
  .card-context {{ font-size: 0.85rem; line-height: 1.55; color: var(--ink-faint); margin: 0; }}
  .card-cover {{ width: 54px; height: 81px; object-fit: cover; border-radius: 2px; flex-shrink: 0; box-shadow: 0 1px 3px var(--shadow); }}
  .actions {{ margin-top: 2rem; display: flex; gap: 1.4rem; flex-wrap: wrap; }}
  .actions a, .actions button {{
    all: unset;
    cursor: pointer;
    font-size: 0.85rem;
    font-family: inherit;
    color: var(--accent);
    border-bottom: 1px solid var(--accent-soft);
    padding-bottom: 2px;
  }}
  .actions a:hover, .actions button:hover {{ color: var(--gold); border-color: var(--gold); }}
  .tags {{ margin-top: 1.5rem; display: flex; gap: 0.6rem 1rem; flex-wrap: wrap; }}
  .tags a {{
    font-size: 0.75rem;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: var(--ink-faint);
    text-decoration: none;
    border-bottom: 1px solid transparent;
  }}
  .tags a:hover {{ color: var(--accent); border-color: var(--accent); }}
  .related {{ margin-top: 2.5rem; padding-top: 1.5rem; border-top: 1px solid var(--rule); }}
  .related h2 {{
    font-size: 0.72rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    font-weight: 400;
    font-family: inherit;
    color: var(--ink-faint);
    margin: 0 0 0.9rem;
  }}
  .related ul {{ list-style: none; margin: 0; padding: 0; }}
  .related li {{ margin: 0 0 0.6rem; }}
  .related a {{
    font-size: 0.92rem;
    font-style: italic;
    color: var(--ink-soft);
    text-decoration: none;
    border-bottom: 1px solid transparent;
  }}
  .related a:hover {{ color: var(--gold); border-color: var(--gold); }}
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
  <a class="back-link sans" href="../index.html">← Tutte le citazioni</a>
  <article class="card" data-category="{category}"{genre_attr}>
    <span class="card-mark" aria-hidden="true">“</span>
    <div class="card-body">
      <p class="card-quote">{quote}</p>
      <p class="card-citation sans"><span class="card-author">{author}</span> — <span class="card-title">{title}</span>{year_html}</p>
      {context_html}
    </div>
    {cover_html}
  </article>
  <div class="actions sans">
    <button type="button" id="copyBtn">Copia citazione</button>
    <a href="../index.html#{slug}">Vedi sul sito →</a>
  </div>
  {tags_html}
  {related_html}
  <footer class="sans">
    Da <a href="../index.html" style="color:var(--ink-faint)">Sottolineature</a> — citazioni verificate a mano, senza algoritmo.
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
    var copyBtn = document.getElementById('copyBtn');
    copyBtn.addEventListener('click', function () {{
      var text = {copy_js_string};
      var original = copyBtn.textContent;
      function feedback() {{ copyBtn.textContent = 'Copiato'; setTimeout(function () {{ copyBtn.textContent = original; }}, 1400); }}
      if (navigator.clipboard && navigator.clipboard.writeText) {{
        navigator.clipboard.writeText(text).then(feedback, feedback);
      }} else {{ feedback(); }}
    }});
  }})();
</script>
</body>
</html>
"""


def render_page(q, slug, same_author):
    quote_esc = html.escape(q['quote'])
    author_esc = html.escape(q['author'])
    title_esc = html.escape(q['title'])
    context_html = ('<p class="card-context sans">' + html.escape(q['context']) + '</p>') if q['context'] else ''
    year_html = (' · <span class="card-year">' + html.escape(q['year']) + '</span>') if q['year'] else ''
    cover_src = q['cover'] if q['cover'].startswith('http') else '../' + q['cover']
    cover_alt = html.escape('Copertina di "' + q['title'] + '" di ' + q['author'])
    cover_html = ('<img class="card-cover" src="' + cover_src + '" alt="' + cover_alt + '" loading="lazy" referrerpolicy="no-referrer" onerror="this.remove()">') if q['cover'] else ''
    genre_attr = (' data-genre="' + html.escape(q['genre']) + '"') if q['genre'] else ''

    ref = q['title'] + (', ' + q['year'] if q['year'] else '')
    description = ('«' + q['quote'] + '» — ' + q['author'] + ', ' + ref)
    if len(description) > 200:
        description = description[:197].rsplit(' ', 1)[0] + '…'

    title_tag = q['author'] + ' — ' + q['title'] + ' | Sottolineature'
    og_title = '«' + (q['quote'] if len(q['quote']) <= 120 else q['quote'][:117].rsplit(' ', 1)[0] + '…') + '»'
    canonical = SITE_URL + '/citazioni/' + slug + '.html'
    og_image = SITE_URL + '/og-banner.png'
    copy_text = '"' + q['quote'] + '" — ' + q['author'] + ', ' + q['title']

    tag_links = []
    author_slug = slugify(q['author'])
    tag_links.append('<a href="../autori/' + author_slug + '.html">' + author_esc + '</a>')
    if q['category'] and q['category'] in CATEGORY_LABELS:
        tag_links.append('<a href="../temi/' + q['category'] + '.html">' + CATEGORY_LABELS[q['category']] + '</a>')
    for g in (q['genre'] or '').split(' '):
        if g in GENRE_LABELS:
            tag_links.append('<a href="../generi/' + g + '.html">' + GENRE_LABELS[g] + '</a>')
    tags_html = '<div class="tags sans">' + ''.join(tag_links) + '</div>' if tag_links else ''

    if same_author:
        items = ''.join(
            '<li><a href="' + s + '.html">«' + html.escape(oq['quote'][:70] + ('…' if len(oq['quote']) > 70 else '')) + '»</a> — <span class="sans" style="font-style:normal">' + html.escape(oq['title']) + '</span></li>'
            for s, oq in same_author[:5]
        )
        related_html = (
            '<div class="related sans"><h2>Altre citazioni di ' + author_esc + '</h2><ul>' + items + '</ul></div>'
        )
    else:
        related_html = ''

    jsonld = json.dumps([
        {
            '@context': 'https://schema.org',
            '@type': 'Quotation',
            'text': q['quote'],
            'creator': {'@type': 'Person', 'name': q['author']},
            'isPartOf': {'@type': 'Book', 'name': q['title']},
            'url': canonical,
        },
        {
            '@context': 'https://schema.org',
            '@type': 'BreadcrumbList',
            'itemListElement': [
                {'@type': 'ListItem', 'position': 1, 'name': 'Sottolineature', 'item': SITE_URL + '/'},
                {'@type': 'ListItem', 'position': 2, 'name': title_tag, 'item': canonical},
            ],
        },
    ], ensure_ascii=False)

    return PAGE_TEMPLATE.format(
        title_tag=html.escape(title_tag),
        description=html.escape(description),
        canonical=canonical,
        og_title=html.escape(og_title),
        og_image=og_image,
        quote=quote_esc,
        author=author_esc,
        title=title_esc,
        year_html=year_html,
        context_html=context_html,
        cover_html=cover_html,
        category=html.escape(q['category']),
        genre_attr=genre_attr,
        slug=slug,
        tags_html=tags_html,
        related_html=related_html,
        jsonld=jsonld,
        copy_js_string=json.dumps(copy_text, ensure_ascii=False),
    )


def main():
    with open(INDEX, encoding='utf-8') as f:
        content = f.read()
    quotes = parse_cards(content)
    print('Citazioni trovate:', len(quotes))

    os.makedirs(OUT_DIR, exist_ok=True)
    # pulizia: rimuove pagine di citazioni non più presenti
    existing = set(os.listdir(OUT_DIR)) if os.path.isdir(OUT_DIR) else set()

    used_slugs = set()
    entries = []
    for q in quotes:
        if not q['author'] or not q['quote']:
            continue
        slug = make_slug(q['author'], q['title'], used_slugs)
        entries.append((slug, q))

    by_author = {}
    for slug, q in entries:
        by_author.setdefault(q['author'], []).append((slug, q))

    for slug, q in entries:
        same_author = [(s, oq) for s, oq in by_author[q['author']] if s != slug]
        page = render_page(q, slug, same_author)
        path = os.path.join(OUT_DIR, slug + '.html')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(page)

    generated_files = set(slug + '.html' for slug, _ in entries)
    stale = existing - generated_files
    for fname in stale:
        if fname.endswith('.html'):
            os.remove(os.path.join(OUT_DIR, fname))
    if stale:
        print('Rimosse pagine obsolete:', len(stale))

    print('Pagine generate in', OUT_DIR)
    return entries


if __name__ == '__main__':
    main()
