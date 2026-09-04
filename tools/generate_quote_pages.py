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
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from labels import CATEGORY_LABELS, GENRE_LABELS  # noqa: E402


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX = os.path.join(ROOT, 'index.html')
OUT_DIR = os.path.join(ROOT, 'citazioni')
SITE_URL = 'https://sottolineature.it'

SAMEAS_PATH = os.path.join(ROOT, 'data', 'autori_sameas.json')


def carica_sameas():
    """Wikipedia e Wikidata di ogni autore, risolti e verificati una volta.

    Stavano solo sugli hub /autori/<slug>/, che sono 257 e quasi nessuno
    cerca. Le pagine che la gente trova sono le 749 citazioni, e li' il nodo
    Person era un nome senza appigli: un motore non ha modo di sapere che
    quell'Albert Camus e' Q34670. Google non unisce i grafi di pagine diverse,
    quindi il collegamento va ripetuto dove serve.
    """
    if os.path.exists(SAMEAS_PATH):
        with open(SAMEAS_PATH, encoding='utf-8') as f:
            return json.load(f)
    return {}


SAMEAS = carica_sameas()

ANNO_PULITO = re.compile(r'^\s*(\d{1,4})\s*$')


def data_pubblicazione(anno):
    """Il campo datePublished, ma solo quando e' davvero una data.

    Trentotto citazioni e quattro opere portavano anni che una data non sono:
    "397-400 d.C. ca.", "IV secolo a.C.", "1833 (comp.), 1842", "Antichita'".
    Finivano tali e quali dentro datePublished, che per schema.org vuole una
    data ISO 8601: "1349-1353" si legge come mese tredici, "Antichita'" non si
    legge affatto. Un valore invalido non e' neutro - Search Console lo
    segnala come errore e puo' portarsi dietro l'intero risultato arricchito.

    Regola: se e' un anno e basta lo dichiariamo come data (con lo zero
    davanti dove serve, perche' l'anno 49 in ISO si scrive 0049); in tutti
    gli altri casi niente datePublished e la dicitura umana va in
    temporalCoverage, che il testo libero lo accetta. Sulla pagina l'anno
    resta scritto com'e': la datazione incerta di un testo antico e' un fatto,
    non un difetto da nascondere.
    """
    anno = (anno or '').strip()
    if not anno:
        return {}
    m = ANNO_PULITO.match(anno)
    if m:
        return {'datePublished': m.group(1).zfill(4)}
    return {'temporalCoverage': anno}
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


# Limiti di lunghezza per <title> e meta description: non sono estetici, sono
# quanto ne mostra Google prima di tagliare.
CONTATTO = 'sottolineature@outlook.it'
TITLE_MAX = 64
TITLE_MIN_INCIPIT = 30
TITLE_MAX_INCIPIT = 48
DESC_MAX = 155


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
<link rel="stylesheet" href="/assets/site.css">
<script type="application/ld+json">{jsonld}</script>
<script>
  try {{
    document.documentElement.className += ' js';
    var savedTheme = localStorage.getItem('sottolineature-theme');
    if (savedTheme === 'dark') {{ document.documentElement.setAttribute('data-theme', 'dark'); var mtc = document.querySelector('meta[name="theme-color"]'); if (mtc) {{ mtc.setAttribute('content', '#16191a'); }} }}
    /* Riparazione una tantum, 2026-09-01. La conversione delle chiavi vecchie
       "autore|titolo" in slug prendeva tutte le citazioni dell'opera invece di
       una: chi apriva il sito si ritrovava segnate frasi che non aveva mai
       letto, e quelle finivano scritte nel browser, dove restavano anche dopo
       la correzione del difetto. Non c'e' modo di distinguere le vere dalle
       inventate, quindi l'elenco si azzera una volta sola. Le note scritte a
       mano non si toccano: sono testo di chi legge, e tornano visibili appena
       la citazione viene sottolineata di nuovo. */
    if (localStorage.getItem('sottolineature-reset') !== '2026-09-01') {{
      localStorage.removeItem('sottolineature-underlined');
      localStorage.setItem('sottolineature-reset', '2026-09-01');
    }}

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
    <a href="/">Sottolineature</a> › <a href="/autori/{author_slug}/">{author}</a> › <span aria-current="page">{breadcrumb_last}</span>
  </nav>
  <h1 class="quote-h1">{h1_esplicativo}</h1>
  <figure class="card" data-category="{category}"{genre_attr}>
    <blockquote class="card-quote-block"{blockquote_cite}>
      <p class="card-quote">{quote_open}<span id="quoteText" class="quote-text" role="button" tabindex="0" title="Clic per copiare la citazione">{h1_quote}</span>{quote_close}</p>
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
    <button type="button" class="js-only" id="copyBtn">Copia citazione</button>
    <button type="button" class="js-only" id="shareBtn" aria-expanded="false" aria-controls="shareChoice">Condividi</button>
    <button type="button" class="js-only" id="underlineBtn" aria-pressed="false">Sottolinea</button>
    <a href="/#{slug}">Vedi sul sito</a>
  </div>
  <div class="share-choice sans" id="shareChoice" hidden>
    <span class="share-choice-label">Sfondo dell'immagine:</span>
    <button type="button" data-variant="chiaro">Chiaro</button>
    <button type="button" data-variant="scuro">Scuro</button>
  </div>
  <div class="quote-note sans" id="quoteNote" hidden>
    <label class="visually-hidden" for="quoteNoteField">La tua nota su questa citazione</label>
    <textarea id="quoteNoteField" class="quote-note-field sans" rows="2" placeholder="Perché ti ha colpita? (facoltativo)"></textarea>
    <p class="quote-note-print sans" id="quoteNotePrint" hidden></p>
    <p class="quote-note-hint">Resta su questo dispositivo. La ritrovi in <a href="/le-mie-sottolineature/">Le mie sottolineature</a>.</p>
  </div>
  {tags_html}
  <p class="segnala sans"><a class="segnala-errore" href="{segnala_href}">Segnala un errore in questa citazione</a></p>
  {related_html}
  </div>
  <footer class="sans" data-url="sottolineature.it/citazioni/{slug}/">
    Da <a href="/" style="color:var(--ink-faint)">Sottolineature</a> — citazioni verificate a mano, senza algoritmo. <a href="/feed.xml" style="color:var(--ink-faint)">Segui le nuove citazioni</a>. <a href="mailto:sottolineature@outlook.it" style="color:var(--ink-faint)">Scrivici</a>. <a href="/privacy/" style="color:var(--ink-faint)">Privacy</a>.
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

    // Sottolinea: stesso archivio della home (localStorage, chiave = slug), cosi'
    // una citazione sottolineata qui compare fra "Le mie" e resta segnata anche
    // sulla card in home. Questa e' la pagina su cui si arriva dalle ricerche:
    // finche' non c'era il pulsante, chi entrava da qui non poteva salvare nulla.
    var SLUG = {slug_js};
    var LEGACY_KEY = {legacy_key_js};
    var SIBLING_SLUGS = {sibling_slugs_js};

    function readStore(key, fallback) {{
      try {{ return JSON.parse(localStorage.getItem(key) || fallback); }}
      catch (e) {{ return JSON.parse(fallback); }}
    }}
    var underlined = readStore('sottolineature-underlined', '[]');
    var notes = readStore('sottolineature-notes', '{{}}');
    if (!Array.isArray(underlined)) {{ underlined = []; }}

    function saveStore() {{
      try {{
        localStorage.setItem('sottolineature-underlined', JSON.stringify(underlined));
        localStorage.setItem('sottolineature-notes', JSON.stringify(notes));
      }} catch (e) {{}}
      if (window.Sottolineature && window.Sottolineature.refreshNavCount) {{
        window.Sottolineature.refreshNavCount();
      }}
    }}

    // Le sottolineature salvate prima del passaggio agli slug hanno chiave
    // "autore|titolo", che di un'opera con due citazioni non dice quale fosse.
    // Si converte sulla PRIMA citazione dell'opera e basta - la stessa scelta
    // che fa la home, cosi' le due pagine non si contraddicono. Prendendole
    // tutte, una sottolineatura sola ne faceva comparire due.
    var legacyAt = underlined.indexOf(LEGACY_KEY);
    if (legacyAt !== -1) {{
      underlined.splice(legacyAt, 1);
      var first = SIBLING_SLUGS[0];
      if (first && underlined.indexOf(first) === -1) {{ underlined.push(first); }}
      if (notes[LEGACY_KEY]) {{
        if (first && !notes[first]) {{ notes[first] = notes[LEGACY_KEY]; }}
        delete notes[LEGACY_KEY];
      }}
      saveStore();
    }}

    var underlineBtn = document.getElementById('underlineBtn');
    var noteWrap = document.getElementById('quoteNote');
    var noteField = document.getElementById('quoteNoteField');
    var notePrint = document.getElementById('quoteNotePrint');

    function isUnderlined() {{ return underlined.indexOf(SLUG) !== -1; }}
    function syncNotePrint() {{
      var text = noteField.value.trim();
      notePrint.textContent = text;
      notePrint.hidden = !text;
    }}
    function renderUnderline() {{
      var on = isUnderlined();
      underlineBtn.textContent = on ? 'Sottolineata' : 'Sottolinea';
      underlineBtn.setAttribute('aria-pressed', String(on));
      underlineBtn.classList.toggle('is-underlined', on);
      noteWrap.hidden = !on;
    }}

    noteField.value = notes[SLUG] || '';
    syncNotePrint();
    renderUnderline();

    underlineBtn.addEventListener('click', function () {{
      var at = underlined.indexOf(SLUG);
      if (at === -1) {{ underlined.push(SLUG); }} else {{ underlined.splice(at, 1); }}
      saveStore();
      renderUnderline();
      if (isUnderlined() && !noteField.value) {{ noteField.focus(); }}
    }});

    var noteTimer;
    noteField.addEventListener('input', function () {{
      syncNotePrint();
      clearTimeout(noteTimer);
      noteTimer = setTimeout(function () {{
        var text = noteField.value.trim();
        if (text) {{ notes[SLUG] = text; }} else {{ delete notes[SLUG]; }}
        saveStore();
      }}, 400);
    }});
  }})();
</script>
</body>
</html>
"""


def strip_accenti(testo):
    """Confronti sul luogo nel testo senza inciampare sugli accenti."""
    scomposto = unicodedata.normalize('NFD', testo)
    return ''.join(c for c in scomposto if unicodedata.category(c) != 'Mn')


def truncate_words(text, max_len):
    if len(text) <= max_len:
        return text, False
    return text[:max_len].rsplit(' ', 1)[0] + '…', True


def related_card(slug, q, meta_html):
    """Voce delle citazioni correlate: scheda con copertina invece della riga
    di testo che rendeva spoglia la parte bassa della pagina."""
    cover = ''
    if q.get('cover'):
        cover = ('<img class="related-cover" src="' + html.escape(q['cover'], quote=True) +
                 '" alt="" width="40" height="60" loading="lazy" referrerpolicy="no-referrer" '
                 'onerror="this.remove()">')
    return (
        '<li class="related-card"><a href="/citazioni/' + slug + '/">' + cover +
        '<span class="related-text"><span class="related-quote">«' +
        html.escape(truncate_words(q['quote'], 70)[0]) + '»</span>' +
        '<span class="related-meta sans">' + meta_html + '</span></span></a></li>'
    )


def finestra(candidati, slug, quante):
    """Le stesse quattro citazioni non possono comparire in fondo a tutte.

    Le sezioni «Altre citazioni di X» e «Altre citazioni su TEMA» prendevano
    sempre le prime della lista. Misurato il 2026-09-03: quattro pagine
    ricevevano 189 link interni ciascuna, la mediana era 3, e in un tema da
    cinquanta citazioni le altre quarantasei non venivano linkate mai. Un
    motore che scopre le pagine seguendo i link vedeva sempre le stesse.

    Qui la finestra scorre: ogni pagina parte da un punto diverso della lista,
    scelto dal proprio slug. E' deterministico — la stessa pagina mostra sempre
    le stesse correlate, cosi' la build resta riproducibile — ma su cinquanta
    pagine i link si distribuiscono su tutte e cinquanta invece di ammucchiarsi
    sulle prime quattro.
    """
    if not candidati:
        return []
    if len(candidati) <= quante:
        return candidati
    seme = 0
    for ch in slug:
        seme = (seme * 31 + ord(ch)) % 1000003
    inizio = seme % len(candidati)
    doppia = candidati + candidati
    return doppia[inizio:inizio + quante]


def titolo_esplicativo(q):
    """H1 della pagina citazione: dice di che frase si tratta e da dove viene.

    Non nomina il personaggio che la pronuncia - sarebbe la cosa piu' utile per
    chi cerca, ma in `data/citazioni.json` quel dato non esiste e dedurlo dal
    titolo dell'opera vorrebbe dire inventarlo. Si dice quello che si sa:
    l'autore, l'opera e, quando il luogo nel testo lo dichiara, che quella
    frase e' l'incipit o un verso.
    """
    incipit, _ = truncate_words(q['quote'], 52)
    # virgolette annidate: una citazione che contiene gia' un dialogo
    # («Uccidi il ragazzo» penso' Jon) dentro le caporali dell'H1 darebbe
    # ««Uccidi il ragazzo»...». In italiano il secondo livello sono gli apici
    # doppi alti.
    incipit = incipit.replace('\u00ab', '\u201c').replace('\u00bb', '\u201d')
    locus = strip_accenti((q.get('source_locus') or '').lower())
    apertura = ('incipit' in locus or 'prima frase' in locus or 'prime righe' in locus
                or 'apertura' in locus)
    verso = (q.get('genre') == 'poesia' or 'verso' in locus or 'canto' in locus
             or 'strofa' in locus)
    # Chi cerca una battuta cerca quasi sempre il personaggio, non l'autore:
    # «chi dice uccidi il ragazzo» prima di «citazione Martin». Il campo
    # `speaker` esiste per questo ed e' facoltativo: si compila solo quando si
    # sa chi parla, e resta vuoto per il narratore o quando c'e' un dubbio.
    speaker = (q.get('speaker') or '').strip()
    if speaker:
        return ('\u00ab' + incipit + '\u00bb: la frase di ' + speaker + ' in \u00ab' + q['title']
                + '\u00bb di ' + q['author'])
    if apertura:
        return '\u00ab' + incipit + '\u00bb: l\u2019incipit di \u00ab' + q['title'] + '\u00bb di ' + q['author']
    if verso:
        return '\u00ab' + incipit + '\u00bb: il verso di ' + q['author'] + ' da \u00ab' + q['title'] + '\u00bb'
    return '\u00ab' + incipit + '\u00bb: la frase di ' + q['author'] + ' in \u00ab' + q['title'] + '\u00bb'


def render_page(q, slug, same_author, same_theme, opera_map=None, raccolta_map=None,
                sibling_slugs=None):
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
    # Su 79 citazioni l'edizione conteneva gia' il traduttore ("trad. Renato
    # Giani, Fratelli Bocca, 1915") e la pagina lo ripeteva subito dopo: «trad.
    # Renato Giani, Fratelli Bocca, 1915, trad. Renato Giani». Si stampa solo
    # se non e' gia nominato nell'edizione.
    if q.get('source_translator'):
        # confronto per parole e non per sottostringa: l'edizione scrive
        # "trad. Sergio Altieri e Gaetano Luigi Staffilano", il campo
        # traduttore "Sergio Altieri, Gaetano Luigi Staffilano" - stesse
        # persone, separatore diverso
        edizione = strip_accenti((q.get('source_edition') or '').lower())
        nomi = [w for w in re.split(r'[^\w]+', strip_accenti(q['source_translator'].lower())) if len(w) > 2]
        gia_detto = bool(nomi) and all(n in edizione for n in nomi)
        if not gia_detto:
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
    cover_src = q['cover'] if q['cover'].startswith(('http', '/')) else '/' + q['cover']
    cover_alt = html.escape('Copertina di "' + q['title'] + '" di ' + q['author'])
    # LCP: la copertina e' l'immagine piu' importante della pagina citazione,
    # niente lazy e priorita' di caricamento alta.
    cover_html = ('<figure class="cover-wrap"><img class="card-cover" src="' + cover_src + '" alt="' + cover_alt + '" width="150" height="225" fetchpriority="high" referrerpolicy="no-referrer" onerror="this.closest(\'.cover-wrap\').remove()"><figcaption class="cover-caption sans">' + html.escape(q['title']) + (('<span class="cover-caption-year"> \u00b7 ' + html.escape(q['year']) + '</span>') if q['year'] else '') + '</figcaption></figure>') if q['cover'] else ''
    genre_attr = (' data-genre="' + html.escape(q['genre']) + '"') if q['genre'] else ''
    author_slug = slugify(q['author'])

    # Fino al 2026-09-03 l'H1 era la citazione stessa: ripeteva parola per
    # parola il tag <title> e il testo visibile subito sotto, e su una frase
    # lunga diventava un'intestazione di duecento caratteri. La citazione resta
    # l'elemento visivamente dominante, ma dentro un <blockquote>, che e' cio'
    # che e'; l'H1 dice invece di che pagina si tratta - chi ha scritto quella
    # frase e dove - che e' la domanda con cui la gente arriva.
    # Tre citazioni contengono un dialogo e iniziano gia' con le caporali: le
    # virgolette decorative del modello ne aggiungevano un secondo paio
    # («\u00ab\u00abUccidi il ragazzo\u00bb pens\u00f2 Jon\u2026\u00bb\u00bb). In quel caso il testo si
    # presenta nudo, le sue virgolette bastano.
    gia_virgolettata = q['quote'].strip().startswith('\u00ab')
    h1_text, was_truncated = truncate_words(q['quote'], 200)
    h1_quote = html.escape(h1_text)
    full_quote_html = ('<p class="card-quote-full">' + quote_esc + '</p>') if was_truncated else ''
    h1_esplicativo = html.escape(titolo_esplicativo(q))
    # <blockquote cite> vuole l'URL del documento da cui la citazione proviene:
    # e' quello che il campo source_url contiene gia'.
    blockquote_cite = (' cite="' + html.escape(q['source_url'], quote=True) + '"') if q.get('source_url') else ''

    ref = q['title'] + (', ' + q['year'] if q['year'] else '')
    # Google taglia la descrizione intorno ai 155-160 caratteri: quello che sta
    # oltre non lo legge nessuno, e la coda troncata a meta' frase fa un effetto
    # peggiore di una frase corta.
    description = ('«' + q['quote'] + '» — ' + q['author'] + ', ' + ref)
    if len(description) > DESC_MAX:
        description = description[:DESC_MAX - 1].rsplit(' ', 1)[0] + '…'

    # Il <title> lo si scriveva come incipit di 45 caratteri piu' autore e opera
    # per intero: veniva fuori una media di 80 caratteri e punte di 127, quando
    # nei risultati di ricerca se ne vedono si' e no 64. Il pezzo che spariva
    # era la coda, cioe' proprio autore e opera. Qui il conto si fa al
    # contrario: prima si decide se autore e opera ci stanno insieme, poi quel
    # che avanza va all'incipit.
    tail_full = ' — ' + q['author'] + ', ' + q['title']
    tail_short = ' — ' + q['author']
    tail = tail_full if 2 + TITLE_MIN_INCIPIT + len(tail_full) <= TITLE_MAX else tail_short
    room = max(min(TITLE_MAX_INCIPIT, TITLE_MAX - 2 - len(tail)), 26)
    title_incipit, _ = truncate_words(q['quote'], room)
    title_tag = '«' + title_incipit + '»' + tail
    og_title = '«' + (q['quote'] if len(q['quote']) <= 120 else q['quote'][:117].rsplit(' ', 1)[0] + '…') + '»'
    canonical = SITE_URL + '/citazioni/' + slug + '/'

    oggetto = 'Errore in: ' + q['author'] + ', ' + q['title']
    corpo = ('Pagina: ' + canonical + '\n\n'
             'Che cosa non torna (testo, autore, opera, anno, luogo nel testo, '
             'traduttore, contesto o copertina):\n\n')
    segnala_href = ('mailto:' + CONTATTO
                    + '?subject=' + urllib.parse.quote(oggetto)
                    + '&body=' + urllib.parse.quote(corpo))

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
        items = ''.join(related_card(s, oq, html.escape(oq['title'])) for s, oq in finestra(same_author, slug, 5))
        related_sections.append('<div class="related sans"><h2>Altre citazioni di ' + author_esc + '</h2><ul>' + items + '</ul></div>')
    if same_theme and q['category'] in CATEGORY_LABELS:
        items = ''.join(related_card(s, oq, html.escape(oq['author'])) for s, oq in finestra(same_theme, slug, 4))
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
                # di che cosa parla la pagina (il libro) e qual e' il suo
                # contenuto principale (la citazione): senza questi due, un
                # motore vede cinque nodi slegati e deve indovinare il legame
                'about': {'@id': book_id},
                'mainEntity': {'@id': canonical + '#quotation'},
                'publisher': {'@id': SITE_URL + '/#publisher'},
                'inLanguage': 'it',
            },
            {
                '@type': 'Organization',
                '@id': SITE_URL + '/#publisher',
                'name': 'Sottolineature',
                'url': SITE_URL + '/',
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
                **({'spokenByCharacter': {'@type': 'Person', 'name': q['speaker']}}
                   if q.get('speaker') else {}),
            },
            {
                '@type': 'Book',
                '@id': book_id,
                'name': book_name,
                'author': {'@id': author_id},
                **data_pubblicazione(q['year']),
                **({'translator': {'@type': 'Person', 'name': q['source_translator']}} if q.get('source_translator') else {}),
            },
            {
                '@type': 'Person',
                '@id': author_id,
                'name': q['author'],
                'url': SITE_URL + '/autori/' + author_slug + '/',
                **({'sameAs': [SAMEAS[q['author']][k] for k in ('wikipedia', 'wikidata')
                               if SAMEAS[q['author']].get(k)]}
                   if SAMEAS.get(q['author']) else {}),
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
        segnala_href=html.escape(segnala_href, quote=True),
        quote_open='' if gia_virgolettata else '<span class="quote-open" aria-hidden="true">\u00ab</span>',
        quote_close='' if gia_virgolettata else '<span class="quote-close" aria-hidden="true">\u00bb</span>',
        h1_esplicativo=h1_esplicativo,
        blockquote_cite=blockquote_cite,
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
        slug_js=json.dumps(slug, ensure_ascii=False),
        legacy_key_js=json.dumps(q['author'] + '|' + q['title'], ensure_ascii=False),
        sibling_slugs_js=json.dumps(sibling_slugs or [slug], ensure_ascii=False),
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
    # Serve alla pagina per convertire in modo sicuro una vecchia sottolineatura
    # salvata come "autore|titolo": va sostituita con gli slug di tutte le
    # citazioni di quell'opera, non solo con il proprio.
    by_legacy_key = {}
    for slug, q in entries:
        by_author.setdefault(q['author'], []).append((slug, q))
        if q['category']:
            by_category.setdefault(q['category'], []).append((slug, q))
        by_legacy_key.setdefault(q['author'] + '|' + q['title'], []).append(slug)

    for slug, q in entries:
        same_author = [(s, oq) for s, oq in by_author[q['author']] if s != slug]
        same_theme = [(s, oq) for s, oq in by_category.get(q['category'], []) if s != slug]
        siblings = by_legacy_key.get(q['author'] + '|' + q['title'], [slug])
        page = render_page(q, slug, same_author, same_theme, opera_map, raccolta_map, siblings)
        path = os.path.join(OUT_DIR, slug + '.html')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(page)

    generated_files = set(slug + '.html' for slug, _ in entries)
    # index.html della cartella /citazioni/ e' l'indice paginato, lo scrive
    # generate_index_pages: non e' una pagina citazione orfana
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
        print('Rimosse pagine obsolete:', len(removed))

    print('Pagine generate in', OUT_DIR)
    return entries


if __name__ == '__main__':
    main()
