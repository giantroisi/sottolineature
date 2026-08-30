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
DATA_PATH = os.path.join(ROOT, 'data', 'citazioni.json')


def load_quotes():
    """Fonte di verità per le citazioni: data/citazioni.json. index.html è
    generato da qui (tools/generate_home.py), non va più letto per i dati."""
    with open(DATA_PATH, encoding='utf-8') as f:
        return json.load(f)


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
<body class="page-quote">
<header class="site-header">
  <div class="site-header-inner">
    <a class="brand" href="/">
      <img src="/mark-quill.png" alt="" width="30" height="30">
      <span class="brand-name">Sottolineature</span>
    </a>
    <nav class="site-nav sans" aria-label="Principale">
      <a href="/citazioni/">Citazioni</a>
      <a href="/autori/">Autori</a>
      <a href="/temi/">Temi</a>
      <a href="/metodo/">Metodo</a>
      <button class="theme-toggle" id="themeToggle" type="button" aria-label="Cambia tema chiaro/scuro">☾</button>
    </nav>
  </div>
</header>
<div class="page">
  <nav class="breadcrumb sans" aria-label="Percorso">
    <a href="/">Sottolineature</a> › <a href="/autori/{author_slug}/">{author}</a> › <span aria-current="page">{breadcrumb_last}</span>
  </nav>
  <figure class="card" data-category="{category}"{genre_attr}>
    <blockquote class="card-quote-block">
      <h1 class="card-quote"><span class="quote-open" aria-hidden="true">«</span><span id="quoteText" class="quote-text" role="button" tabindex="0" title="Clic per copiare la citazione">{h1_quote}</span><span class="quote-close" aria-hidden="true">»</span></h1>
      {full_quote_html}
    </blockquote>
    <div class="card-body">
      <figcaption class="card-citation sans">— <a href="/autori/{author_slug}/" class="card-author">{author}</a>, <cite class="card-title">{title}</cite>{year_html}</figcaption>
      {context_html}
      {source_html}
    </div>
    {cover_html}
  </figure>
  <div class="actions sans">
    {opera_link_html}
    {raccolta_link_html}
    <button type="button" id="copyBtn">Copia citazione</button>
    <button type="button" id="shareBtn" aria-expanded="false" aria-controls="shareChoice">Condividi</button>
    <a href="/#{slug}">Vedi sul sito</a>
  </div>
  <div class="share-choice sans" id="shareChoice" hidden>
    <span class="share-choice-label">Sfondo dell'immagine:</span>
    <button type="button" data-variant="chiaro">Chiaro</button>
    <button type="button" data-variant="scuro">Scuro</button>
  </div>
  {tags_html}
  {related_html}
  <footer class="sans">
    Da <a href="/" style="color:var(--ink-faint)">Sottolineature</a> — citazioni verificate a mano, senza algoritmo.
  </footer>
</div>
<script src="/assets/share.js"></script>
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

    // Clic (o Invio/Spazio) sul testo della citazione: copia, come in home.
    var quoteText = document.getElementById('quoteText');
    function copyQuote(feedbackEl) {{
      var text = {copy_js_string};
      var el = feedbackEl || copyBtn;
      var original = el.textContent;
      function done() {{ el.textContent = 'Copiato'; setTimeout(function () {{ el.textContent = original; }}, 1400); }}
      if (navigator.clipboard && navigator.clipboard.writeText) {{
        navigator.clipboard.writeText(text).then(done, done);
      }} else {{ done(); }}
    }}
    quoteText.addEventListener('click', function () {{ copyQuote(); }});
    quoteText.addEventListener('keydown', function (e) {{
      if (e.key === 'Enter' || e.key === ' ') {{ e.preventDefault(); copyQuote(); }}
    }});

    // Condividi: la scelta chiaro/scuro riguarda solo l'immagine generata,
    // non il tema con cui si sta leggendo la pagina.
    var shareBtn = document.getElementById('shareBtn');
    var shareChoice = document.getElementById('shareChoice');
    shareBtn.addEventListener('click', function () {{
      var open = shareChoice.hidden;
      shareChoice.hidden = !open;
      shareBtn.setAttribute('aria-expanded', String(open));
    }});
    Array.prototype.forEach.call(shareChoice.querySelectorAll('button'), function (b) {{
      b.addEventListener('click', function () {{
        window.Sottolineature.share(
          {share_quote_js}, {share_author_js}, {share_title_js}, {share_year_js},
          b, 'post', b.getAttribute('data-variant')
        );
      }});
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


def render_page(q, slug, same_author, same_theme, opera_map=None, raccolta_map=None):
    quote_esc = html.escape(q['quote'])
    author_esc = html.escape(q['author'])
    title_esc = html.escape(q['title'])
    context_html = ('<p class="card-context sans">' + html.escape(q['context']) + '</p>') if q['context'] else ''

    # Blocco fonte (Fase 3 SEO.md): compare solo se c'e' almeno un campo
    # verificato. Mai un campo vuoto "riempito" con un placeholder — un
    # riferimento assente e' onesto, uno inventato non lo è mai.
    source_parts = []
    if q.get('source_edition'):
        source_parts.append(html.escape(q['source_edition']))
    if q.get('source_locus'):
        source_parts.append(html.escape(q['source_locus']))
    if q.get('source_translator'):
        source_parts.append('trad. ' + html.escape(q['source_translator']))
    source_html = ''
    if source_parts:
        source_url = q.get('source_url', '')
        if 'wikisource' in source_url:
            link_label = 'Testo su Wikisource'
        elif 'wikiquote' in source_url:
            link_label = 'Fonte su Wikiquote'
        else:
            link_label = 'Approfondisci'
        source_link = (' <a href="' + html.escape(source_url, quote=True) + '">' + link_label + ' →</a>') if source_url else ''
        source_html = '<p class="card-source sans"><span class="source-label">Dove si trova</span>' + ', '.join(source_parts) + '.' + source_link + '</p>'
    year_html = (' · <span class="card-year">' + html.escape(q['year']) + '</span>') if q['year'] else ''
    cover_src = q['cover'] if q['cover'].startswith('http') else '/' + q['cover']
    cover_alt = html.escape('Copertina di "' + q['title'] + '" di ' + q['author'])
    # LCP: la copertina e' l'immagine piu' importante della pagina citazione,
    # niente lazy e priorita' di caricamento alta.
    cover_html = ('<figure class="cover-wrap"><img class="card-cover" src="' + cover_src + '" alt="' + cover_alt + '" width="150" height="225" fetchpriority="high" referrerpolicy="no-referrer" onerror="this.closest(\'.cover-wrap\').remove()"><figcaption class="cover-caption sans">' + html.escape(q['title']) + (('<span class="cover-caption-year"> \u00b7 ' + html.escape(q['year']) + '</span>') if q['year'] else '') + '</figcaption></figure>') if q['cover'] else ''
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
    related_html = ('<div class="related-grid">' + ''.join(related_sections) + '</div>') if related_sections else ''

    # Fase 4 SEO.md §9.3: quando l'opera ha una pagina propria in /opere/, il
    # Book @id e il nome vanno presi da li' e riusati su tutte le citazioni
    # della stessa opera (anche quando il campo `title` varia per volume,
    # es. i tre libri del Signore degli Anelli).
    opera_info = (opera_map or {}).get((q['author'], q['title']))
    book_id = opera_info['book_id'] if opera_info else (canonical + '#book')
    book_name = opera_info['title'] if opera_info else q['title']
    opera_link_html = (
        '<p class="opera-link sans"><a class="is-primary" href="' + opera_info['opera_url'] +
        '">Tutte le citazioni da «' + html.escape(opera_info['title']) + '»</a></p>'
    ) if opera_info else ''

    # Fase 5 SEO.md: una citazione puo' comparire in una o piu' raccolte
    # curate a mano (data/raccolte.json) - link di ritorno verso ciascuna.
    raccolte_for_quote = (raccolta_map or {}).get(quote_key(q), [])
    raccolta_link_html = ''.join(
        '<p class="opera-link sans"><a href="' + r['url'] + '">Raccolta: ' +
        html.escape(r['title']) + '</a></p>'
        for r in raccolte_for_quote
    )
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
                **({'citation': q['source_locus']} if q.get('source_locus') else {}),
                **({'sameAs': q['source_url']} if q.get('source_url') else {}),
            },
            {
                '@type': 'Book',
                '@id': book_id,
                'name': book_name,
                'author': {'@id': author_id},
                **({'datePublished': q['year']} if q['year'] else {}),
                **({'translator': {'@type': 'Person', 'name': q['source_translator']}} if q.get('source_translator') else {}),
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
        source_html=source_html,
        opera_link_html=opera_link_html,
        raccolta_link_html=raccolta_link_html,
        cover_html=cover_html,
        category=html.escape(q['category']),
        genre_attr=genre_attr,
        slug=slug,
        breadcrumb_last=breadcrumb_last_esc,
        tags_html=tags_html,
        related_html=related_html,
        jsonld=jsonld,
        copy_js_string=json.dumps(copy_text, ensure_ascii=False),
        share_quote_js=json.dumps(q['quote'], ensure_ascii=False),
        share_author_js=json.dumps(q['author'], ensure_ascii=False),
        share_title_js=json.dumps(q['title'], ensure_ascii=False),
        share_year_js=json.dumps(q.get('year') or '', ensure_ascii=False),
    )


def main(opera_map=None, raccolta_map=None):
    quotes = load_quotes()
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
        page = render_page(q, slug, same_author, same_theme, opera_map, raccolta_map)
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
