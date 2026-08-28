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
SLUGS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'slugs.json')
REDIRECTS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'redirects.json')


def load_slugs():
    if os.path.exists(SLUGS_PATH):
        with open(SLUGS_PATH, encoding='utf-8') as f:
            return json.load(f)
    return {'quotes': {}, 'authors': {}}


def save_slugs(data):
    with open(SLUGS_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2, sort_keys=True)


def quote_key(q):
    return q['author'] + '|' + q['title'] + '|' + ' '.join(q['quote'].split()[:6])


def load_redirects():
    if os.path.exists(REDIRECTS_PATH):
        with open(REDIRECTS_PATH, encoding='utf-8') as f:
            return json.load(f)
    return []


def save_redirects(data):
    with open(REDIRECTS_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


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


def assign_slugs(quotes, slugs_data, redirects):
    """Assegna a ogni citazione lo slug congelato in slugs.json. Per le citazioni
    nuove (chiave non trovata) calcola uno slug leggibile invece di un numero
    progressivo, lo aggiunge a slugs_data (persistito dal chiamante) e registra
    un redirect solo se lo slug di quella stessa chiave cambia rispetto a prima
    (non dovrebbe mai succedere in condizioni normali: gli slug esistenti non si
    toccano)."""
    quote_slugs = slugs_data.setdefault('quotes', {})
    used = set(quote_slugs.values())
    entries = []
    changed = False
    for q in quotes:
        if not q['author'] or not q['quote']:
            continue
        key = quote_key(q)
        if key in quote_slugs:
            slug = quote_slugs[key]
        else:
            author_slug = slugify(q['author'])
            title_slug = slugify(q['title'])
            same_work_exists = any(
                k.startswith(q['author'] + '|' + q['title'] + '|') for k in quote_slugs
            )
            if same_work_exists:
                incipit_words = q['quote'].split()[:3]
                slug = slugify(author_slug + '-' + title_slug + '-' + '-'.join(incipit_words))
            else:
                slug = author_slug + '-' + title_slug
            base = slug
            i = 2
            while slug in used:
                slug = base + '-' + str(i)
                i += 1
            quote_slugs[key] = slug
            changed = True
        used.add(slug)
        entries.append((slug, q))
    return entries, changed


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
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preconnect" href="https://covers.openlibrary.org">
<link rel="stylesheet" href="/assets/site.css">
<script type="application/ld+json">{jsonld}</script>
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
  <nav class="breadcrumb sans" aria-label="Percorso">
    <a href="/">Sottolineature</a> › <a href="/autori/{author_slug}/">{author}</a> › <span aria-current="page">{breadcrumb_last}</span>
  </nav>
  <figure class="card" data-category="{category}"{genre_attr}>
    <span class="card-mark" aria-hidden="true">“</span>
    <div class="card-body">
      <blockquote class="card-quote-block">
        <h1 class="card-quote">{h1_quote}</h1>
        {full_quote_html}
      </blockquote>
      <figcaption class="card-citation sans">— <a href="/autori/{author_slug}/" class="card-author">{author}</a>, <cite class="card-title">{title}</cite>{year_html}</figcaption>
      {context_html}
    </div>
    {cover_html}
  </figure>
  <div class="actions sans">
    <button type="button" id="copyBtn">Copia citazione</button>
    <a href="/#{slug}">Vedi sul sito →</a>
  </div>
  {tags_html}
  {related_html}
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


def truncate_words(text, max_len):
    if len(text) <= max_len:
        return text, False
    return text[:max_len].rsplit(' ', 1)[0] + '…', True


def render_page(q, slug, same_author, same_theme):
    quote_esc = html.escape(q['quote'])
    author_esc = html.escape(q['author'])
    title_esc = html.escape(q['title'])
    context_html = ('<p class="card-context sans">' + html.escape(q['context']) + '</p>') if q['context'] else ''
    year_html = (' · <span class="card-year">' + html.escape(q['year']) + '</span>') if q['year'] else ''
    cover_src = q['cover'] if q['cover'].startswith('http') else '/' + q['cover']
    cover_alt = html.escape('Copertina di "' + q['title'] + '" di ' + q['author'])
    # LCP: la copertina e' l'immagine piu' importante della pagina citazione,
    # niente lazy e priorita' di caricamento alta.
    cover_html = ('<img class="card-cover" src="' + cover_src + '" alt="' + cover_alt + '" width="54" height="81" fetchpriority="high" referrerpolicy="no-referrer" onerror="this.remove()">') if q['cover'] else ''
    genre_attr = (' data-genre="' + html.escape(q['genre']) + '"') if q['genre'] else ''
    author_slug = slugify(q['author'])

    # H1 = testo della citazione; se troppo lungo, H1 troncato e testo
    # integrale mostrato comunque sotto (non come intestazione).
    h1_text, was_truncated = truncate_words(q['quote'], 200)
    h1_quote = html.escape(h1_text)
    full_quote_html = ('<p class="card-quote-full">' + quote_esc + '</p>') if was_truncated else ''

    ref = q['title'] + (', ' + q['year'] if q['year'] else '')
    description = ('«' + q['quote'] + '» — ' + q['author'] + ', ' + ref)
    if len(description) > 200:
        description = description[:197].rsplit(' ', 1)[0] + '…'

    title_incipit, _ = truncate_words(q['quote'], 45)
    title_tag = '«' + title_incipit + '» — ' + q['author'] + ', ' + q['title']
    og_title = '«' + (q['quote'] if len(q['quote']) <= 120 else q['quote'][:117].rsplit(' ', 1)[0] + '…') + '»'
    canonical = SITE_URL + '/citazioni/' + slug + '/'
    og_image = SITE_URL + '/assets/og/' + slug + '.png'
    copy_text = '"' + q['quote'] + '" — ' + q['author'] + ', ' + q['title']

    breadcrumb_last, _ = truncate_words(q['quote'], 40)
    breadcrumb_last_esc = html.escape(breadcrumb_last)

    tag_links = []
    tag_links.append('<a href="/autori/' + author_slug + '/">' + author_esc + '</a>')
    if q['category'] and q['category'] in CATEGORY_LABELS:
        tag_links.append('<a href="/temi/' + q['category'] + '/">' + CATEGORY_LABELS[q['category']] + '</a>')
    for g in (q['genre'] or '').split(' '):
        if g in GENRE_LABELS:
            tag_links.append('<a href="/generi/' + g + '/">' + GENRE_LABELS[g] + '</a>')
    tags_html = '<div class="tags sans">' + ''.join(tag_links) + '</div>' if tag_links else ''

    related_sections = []
    if same_author:
        items = ''.join(
            '<li><a href="/citazioni/' + s + '/">«' + html.escape(truncate_words(oq['quote'], 70)[0]) + '»</a> — <span class="sans" style="font-style:normal">' + html.escape(oq['title']) + '</span></li>'
            for s, oq in same_author[:5]
        )
        related_sections.append('<div class="related sans"><h2>Altre citazioni di ' + author_esc + '</h2><ul>' + items + '</ul></div>')
    if same_theme and q['category'] in CATEGORY_LABELS:
        items = ''.join(
            '<li><a href="/citazioni/' + s + '/">«' + html.escape(truncate_words(oq['quote'], 70)[0]) + '»</a> — <span class="sans" style="font-style:normal">' + html.escape(oq['author']) + '</span></li>'
            for s, oq in same_theme[:4]
        )
        related_sections.append(
            '<div class="related sans"><h2>Altre citazioni su ' + CATEGORY_LABELS[q['category']] + '</h2><ul>' + items + '</ul></div>'
        )
    related_html = ''.join(related_sections)

    book_id = canonical + '#book'
    author_id = SITE_URL + '/autori/' + author_slug + '/#person'
    jsonld = json.dumps({
        '@context': 'https://schema.org',
        '@graph': [
            {
                '@type': 'WebPage',
                '@id': canonical + '#webpage',
                'url': canonical,
                'name': title_tag,
                'breadcrumb': {'@id': canonical + '#breadcrumb'},
            },
            {
                '@type': 'Quotation',
                '@id': canonical + '#quotation',
                'text': q['quote'],
                'creator': {'@id': author_id},
                'isPartOf': {'@id': book_id},
                'url': canonical,
            },
            {
                '@type': 'Book',
                '@id': book_id,
                'name': q['title'],
                'author': {'@id': author_id},
                **({'datePublished': q['year']} if q['year'] else {}),
            },
            {
                '@type': 'Person',
                '@id': author_id,
                'name': q['author'],
                'url': SITE_URL + '/autori/' + author_slug + '/',
            },
            {
                '@type': 'BreadcrumbList',
                '@id': canonical + '#breadcrumb',
                'itemListElement': [
                    {'@type': 'ListItem', 'position': 1, 'name': 'Sottolineature', 'item': SITE_URL + '/'},
                    {'@type': 'ListItem', 'position': 2, 'name': q['author'], 'item': SITE_URL + '/autori/' + author_slug + '/'},
                    {'@type': 'ListItem', 'position': 3, 'name': breadcrumb_last, 'item': canonical},
                ],
            },
        ],
    }, ensure_ascii=False)

    return PAGE_TEMPLATE.format(
        title_tag=html.escape(title_tag),
        description=html.escape(description),
        canonical=canonical,
        og_title=html.escape(og_title),
        og_image=og_image,
        h1_quote=h1_quote,
        full_quote_html=full_quote_html,
        author=author_esc,
        author_slug=author_slug,
        title=title_esc,
        year_html=year_html,
        context_html=context_html,
        cover_html=cover_html,
        category=html.escape(q['category']),
        genre_attr=genre_attr,
        slug=slug,
        breadcrumb_last=breadcrumb_last_esc,
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

    slugs_data = load_slugs()
    entries, changed = assign_slugs(quotes, slugs_data, load_redirects())
    if changed:
        save_slugs(slugs_data)
        print('slugs.json aggiornato con nuove citazioni')

    by_author = {}
    by_category = {}
    for slug, q in entries:
        by_author.setdefault(q['author'], []).append((slug, q))
        if q['category']:
            by_category.setdefault(q['category'], []).append((slug, q))

    for slug, q in entries:
        same_author = [(s, oq) for s, oq in by_author[q['author']] if s != slug]
        same_theme = [(s, oq) for s, oq in by_category.get(q['category'], []) if s != slug]
        page = render_page(q, slug, same_author, same_theme)
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
