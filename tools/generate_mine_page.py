#!/usr/bin/env python3
"""Genera /le-mie-sottolineature/ : la pagina personale di chi legge.

Fino a oggi "Sottolinea" e le note esistevano ma non c'era nessun posto dove
rivederle: restavano nel localStorage del browser senza un modo per tornarci.
Questa pagina le raccoglie.

E' interamente lato client (i dati non lasciano il browser di chi legge) e
porta noindex: non e' contenuto per i motori, e' contenuto di una persona.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import generate_quote_pages as qp  # noqa: E402

OUT = os.path.join(qp.ROOT, 'le-mie-sottolineature.html')

PAGE = '''<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="color-scheme" content="light dark">
<meta name="theme-color" content="#f2f0eb">
<title>Le mie sottolineature | Sottolineature</title>
<meta name="description" content="Le citazioni che hai sottolineato su Sottolineature, con le tue note. Restano su questo dispositivo.">
<meta name="robots" content="noindex,follow">
<link rel="canonical" href="https://sottolineature.it/le-mie-sottolineature/">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="stylesheet" href="/assets/site.css">
<style>
  .mine-empty { max-width: 34rem; }
  .mine-empty p { color: var(--ink-soft); line-height: 1.7; }
  .mine-item { padding: 1.4rem 0; border-bottom: 1px solid var(--rule); }
  .mine-quote { font-size: 1.12rem; line-height: 1.5; font-style: italic; margin: 0 0 0.5rem; }
  .mine-quote a { color: inherit; text-decoration: none; }
  .mine-quote a:hover { color: var(--accent); }
  .mine-meta { font-size: 0.85rem; color: var(--ink-soft); margin: 0; }
  .mine-note {
    margin: 0.7rem 0 0; padding: 0.7rem 0.9rem; border-left: 2px solid var(--gold);
    background: var(--paper-raised); font-size: 0.88rem; line-height: 1.6; color: var(--ink-soft);
  }
  .mine-note-label {
    display: block; font-size: 0.64rem; letter-spacing: 0.14em; text-transform: uppercase;
    color: var(--gold); margin-bottom: 0.25rem;
  }
  .mine-count { font-size: 0.95rem; color: var(--ink-faint); margin: 0 0 2rem; }
  .mine-tools { display: flex; gap: 0.6rem; flex-wrap: wrap; margin: 2rem 0 0; }
  .mine-tools button, .mine-tools a {
    border: 1px solid var(--rule); border-radius: 999px; padding: 0.5rem 1.05rem;
    font-size: 0.85rem; color: var(--ink-soft); background: none; cursor: pointer;
    text-decoration: none; line-height: 1;
  }
  .mine-tools button:hover, .mine-tools a:hover { border-color: var(--accent); color: var(--accent); }
  .mine-actions { display: flex; gap: 1.1rem; flex-wrap: wrap; margin: 0.8rem 0 0; }
  .mine-actions button {
    border: 0; background: none; padding: 0; cursor: pointer; font-family: inherit;
    font-size: 0.78rem; color: var(--ink-faint);
    border-bottom: 1px solid var(--rule); line-height: 1.6;
  }
  .mine-actions button:hover { color: var(--accent); border-color: var(--accent); }
  .mine-item .share-choice { margin: 0.8rem 0 0; }
  .mine-removed { padding: 1.1rem 0; border-bottom: 1px solid var(--rule); font-size: 0.88rem; color: var(--ink-faint); }
  .mine-removed button {
    border: 0; background: none; padding: 0; margin-left: 0.6rem; cursor: pointer;
    font-family: inherit; font-size: 0.88rem; color: var(--accent);
    border-bottom: 1px solid var(--accent);
  }
</style>
<script>
  try {
    document.documentElement.className += ' js';
    var savedTheme = localStorage.getItem('sottolineature-theme');
    if (savedTheme === 'dark') { document.documentElement.setAttribute('data-theme', 'dark'); var mtc = document.querySelector('meta[name="theme-color"]'); if (mtc) { mtc.setAttribute('content', '#16191a'); } }
    /* Riparazione una tantum, 2026-09-01. La conversione delle chiavi vecchie
       "autore|titolo" in slug prendeva tutte le citazioni dell'opera invece di
       una: chi apriva il sito si ritrovava segnate frasi che non aveva mai
       letto, e quelle finivano scritte nel browser, dove restavano anche dopo
       la correzione del difetto. Non c'e' modo di distinguere le vere dalle
       inventate, quindi l'elenco si azzera una volta sola. Le note scritte a
       mano non si toccano: sono testo di chi legge, e tornano visibili appena
       la citazione viene sottolineata di nuovo. */
    if (localStorage.getItem('sottolineature-reset') !== '2026-09-01') {
      localStorage.removeItem('sottolineature-underlined');
      localStorage.setItem('sottolineature-reset', '2026-09-01');
    }

  } catch (e) {}
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
      <a href="/le-mie-sottolineature/" aria-current="page">Le mie</a>
      <a href="/metodo/">Metodo</a>
      <button class="theme-toggle js-only" id="themeToggle" type="button" aria-label="Cambia tema chiaro/scuro">&#9790;</button>
    </nav>
  </div>
</header>
<script src="/assets/nav.js" defer></script>
<script src="/assets/share.js" defer></script>
<div class="page">
<div class="page-main" role="main">
  <p class="eyebrow sans">La tua raccolta</p>
  <h1>Le mie sottolineature</h1>
  <p class="mine-count sans" id="mineCount"></p>
  <div id="mineList"></div>
  <div class="mine-empty sans" id="mineEmpty">
    <p>Qui finiscono le citazioni che segni con <strong>Sottolinea</strong>, insieme alle note che
    scrivi accanto a ciascuna. Per ora non ce n'e' nessuna.</p>
    <p>Vai all&#39;archivio, e quando una riga ti riguarda premi <em>Sottolinea</em>: la ritrovi qui,
    anche fra un mese.</p>
    <p style="font-size:0.85rem;color:var(--ink-faint)">Le tue sottolineature restano su questo
    dispositivo, in questo browser: non vengono inviate da nessuna parte e nessuno le vede oltre a te.
    Se cambi computer o cancelli i dati del sito, non ci sono piu&#39;.</p>
  </div>
  <div class="mine-tools sans" id="mineTools" hidden>
    <a href="/citazioni/">Aggiungine altre</a>
    <button class="js-only" type="button" id="printBtn">Stampa</button>
  </div>
  </div>
  <p class="print-only sans" id="minePrintDate"></p>
  <footer class="sans" data-url="sottolineature.it">
    Da <a href="/" style="color:var(--ink-faint)">Sottolineature</a> &mdash; citazioni verificate a mano, senza algoritmo.<span class="footer-servizi"> <a href="mailto:sottolineature@outlook.it" style="color:var(--ink-faint)">Scrivici</a>. <a href="/privacy/" style="color:var(--ink-faint)">Privacy</a>.</span>
  </footer>
</div>
<script>
(function () {
  var toggle = document.getElementById('themeToggle');
  var root = document.documentElement;
  function currentTheme() { return root.getAttribute('data-theme') === 'dark' ? 'dark' : 'light'; }
  function render() { toggle.textContent = currentTheme() === 'dark' ? '\\u2600' : '\\u263e'; }
  render();
  toggle.addEventListener('click', function () {
    var next = currentTheme() === 'dark' ? 'light' : 'dark';
    if (next === 'dark') { root.setAttribute('data-theme', 'dark'); } else { root.removeAttribute('data-theme'); }
    try { localStorage.setItem('sottolineature-theme', next); } catch (e) {}
    render();
  });

  function readStore(key, fallback) {
    try { return JSON.parse(localStorage.getItem(key) || fallback); } catch (e) { return JSON.parse(fallback); }
  }
  // Stesse chiavi usate dalla home: autore|titolo. Non e' univoca quando di
  // una stessa opera ci sono piu' citazioni - limite noto, da sanare passando
  // allo slug con una migrazione dei dati gia' salvati.
  var SLUG_INDEX = __SLUG_INDEX__;
  var LEGACY = __LEGACY_MAP__;
  var underlined = readStore('sottolineature-underlined', '[]');
  var notes = readStore('sottolineature-notes', '{}');
  var list = document.getElementById('mineList');
  var countEl = document.getElementById('mineCount');
  var emptyEl = document.getElementById('mineEmpty');
  var toolsEl = document.getElementById('mineTools');

  function esc(t) { var d = document.createElement('div'); d.textContent = t; return d.innerHTML; }

  if (!underlined.length) {
    countEl.textContent = '';
    return;
  }

  // Le chiavi salvate sono slug. Quelle vecchie (autore|titolo) si convertono
  // qui una volta per tutte: da lì in avanti togliere una sottolineatura è
  // togliere una riga sola, senza ambiguità fra due citazioni della stessa opera.
  var slugs = [];
  var noteBySlug = {};
  var hadLegacy = false;
  function addKey(k, note) {
    if (k.indexOf('|') !== -1) { hadLegacy = true; }
    // di una chiave vecchia "autore|titolo" si prende la PRIMA citazione
    // dell'opera e basta: prendendole tutte, una sottolineatura ne faceva
    // comparire due, e la seconda non l'aveva mai segnata nessuno
    var keys = k.indexOf('|') === -1 ? [k] : (LEGACY[k] || []).slice(0, 1);
    keys.forEach(function (slug) {
      if (slugs.indexOf(slug) === -1) { slugs.push(slug); }
      if (note && !noteBySlug[slug]) { noteBySlug[slug] = note; }
    });
  }
  underlined.forEach(function (k) { addKey(k, (notes[k] || '').trim()); });
  slugs = slugs.filter(function (s) { return SLUG_INDEX[s] !== undefined; });

  function save() {
    try {
      localStorage.setItem('sottolineature-underlined', JSON.stringify(slugs));
      localStorage.setItem('sottolineature-notes', JSON.stringify(notes));
    } catch (e) {}
    // il contatore sulla voce "Le mie" resterebbe fermo al numero di partenza
    if (window.Sottolineature && window.Sottolineature.refreshNavCount) {
      window.Sottolineature.refreshNavCount();
    }
  }

  if (hadLegacy) {
    Object.keys(notes).forEach(function (k) {
      if (k.indexOf('|') === -1) { return; }
      (LEGACY[k] || []).slice(0, 1).forEach(function (slug) {
        if (!notes[slug]) { notes[slug] = notes[k]; }
      });
      delete notes[k];
    });
    save();
  }

  // La spiegazione nasce visibile, cosi' chi arriva senza JavaScript la
  // legge lo stesso; da qui in poi e' il numero di righe a decidere, e la
  // decide refreshCount() in un posto solo - anche quando le righe le
  // toglie l'utente una a una.
  if (!slugs.length) { return; }

  var quoteBySlug = {};
  var removedHTML = {};

  function refreshCount() {
    var n = list.querySelectorAll('.mine-item').length;
    if (n === 0) {
      countEl.textContent = 'Nessuna citazione sottolineata';
      toolsEl.hidden = true;
      emptyEl.hidden = false;
    } else {
      countEl.textContent = n === 1 ? '1 citazione sottolineata' : n + ' citazioni sottolineate';
      toolsEl.hidden = false;
      emptyEl.hidden = true;
    }
  }

  function itemHTML(slug, q, note) {
    return '<article class="mine-item" data-slug="' + esc(slug) + '">' +
      '<p class="mine-quote"><a href="/citazioni/' + slug + '/">&laquo;' + esc(q.quote) + '&raquo;</a></p>' +
      '<p class="mine-meta sans">' + esc(q.author) + ' &mdash; <em>' + esc(q.title) + '</em>' +
      (q.year ? ' &middot; ' + esc(String(q.year)) : '') + '</p>' +
      (note ? '<p class="mine-note sans"><span class="mine-note-label">La tua nota</span>' + esc(note) + '</p>' : '') +
      '<div class="mine-actions sans">' +
        '<button type="button" data-act="share" aria-expanded="false">Condividi</button>' +
        '<button type="button" data-act="remove">Togli la sottolineatura</button>' +
      '</div>' +
      '<div class="share-choice sans" hidden>' +
        '<span class="share-choice-label">Sfondo dell&#39;immagine:</span>' +
        '<button type="button" data-variant="chiaro">Chiaro</button>' +
        '<button type="button" data-variant="scuro">Scuro</button>' +
      '</div>' +
      '</article>';
  }

  function onListClick(e) {
    var t = e.target;
    if (!t || t.tagName !== 'BUTTON') { return; }

    var variant = t.getAttribute('data-variant');
    if (variant) {
      var art = t.closest('.mine-item');
      var q = quoteBySlug[art.getAttribute('data-slug')];
      if (q && window.Sottolineature && window.Sottolineature.share) {
        window.Sottolineature.share(q.quote, q.author, q.title, q.year ? String(q.year) : '', t, 'post', variant);
      }
      return;
    }

    var act = t.getAttribute('data-act');
    if (act === 'share') {
      var panel = t.closest('.mine-item').querySelector('.share-choice');
      var open = panel.hidden;
      panel.hidden = !open;
      t.setAttribute('aria-expanded', String(open));
      return;
    }

    // Togliere una sottolineatura e' l'unica azione distruttiva della pagina:
    // resta un "Annulla" finche' non si ricarica.
    if (act === 'remove') {
      var article = t.closest('.mine-item');
      var slug = article.getAttribute('data-slug');
      removedHTML[slug] = article.outerHTML;
      var i = slugs.indexOf(slug);
      if (i !== -1) { slugs.splice(i, 1); }
      save();
      var row = document.createElement('div');
      row.className = 'mine-removed sans';
      row.setAttribute('data-slug', slug);
      row.innerHTML = 'Sottolineatura tolta.<button type="button" data-act="undo">Annulla</button>';
      article.parentNode.replaceChild(row, article);
      refreshCount();
      return;
    }

    if (act === 'undo') {
      var oldRow = t.closest('.mine-removed');
      var back = oldRow.getAttribute('data-slug');
      if (slugs.indexOf(back) === -1) { slugs.push(back); }
      save();
      var tmp = document.createElement('div');
      tmp.innerHTML = removedHTML[back];
      oldRow.parentNode.replaceChild(tmp.firstChild, oldRow);
      refreshCount();
    }
  }

  fetch('/data/citazioni.json').then(function (r) { return r.json(); }).then(function (quotes) {
    var found = slugs.map(function (slug) { return { slug: slug, q: quotes[SLUG_INDEX[slug]] }; })
                     .filter(function (x) { return x.q; });
    if (!found.length) { return; }
    found.forEach(function (x) { quoteBySlug[x.slug] = x.q; });
    list.innerHTML = found.map(function (x) {
      return itemHTML(x.slug, x.q, (noteBySlug[x.slug] || '').trim());
    }).join('');
    refreshCount();
    // Chi stampa la propria raccolta la consegna, o la rilegge fra un mese:
    // senza una data non sa piu' a quando risale.
    var dataEl = document.getElementById('minePrintDate');
    if (dataEl) {
      try {
        dataEl.textContent = 'Selezione presa da sottolineature.it il ' +
          new Date().toLocaleDateString('it-IT', { day: 'numeric', month: 'long', year: 'numeric' }) + '.';
      } catch (e) {}
    }
    list.addEventListener('click', onListClick);
    document.getElementById('printBtn').addEventListener('click', function () { window.print(); });
  }).catch(function () {});
})();
</script>
</body>
</html>
'''


def main():
    quotes = qp.load_quotes()
    entries, _ = qp.assign_slugs(quotes, qp.load_slugs(), qp.load_redirects())
    index_by_slug = {}
    legacy = {}
    order = {id(q): i for i, q in enumerate(quotes)}
    for slug, q in entries:
        index_by_slug[slug] = order[id(q)]
        legacy.setdefault(q['author'] + '|' + q['title'], []).append(slug)
    page = PAGE.replace('__SLUG_INDEX__', json.dumps(index_by_slug, ensure_ascii=False))
    page = page.replace('__LEGACY_MAP__', json.dumps(legacy, ensure_ascii=False))
    with open(OUT, 'w', encoding='utf-8') as f:
        f.write(page)
    print('Pagina /le-mie-sottolineature/ generata')
    return '/le-mie-sottolineature/'


if __name__ == '__main__':
    main()
