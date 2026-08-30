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
</style>
<script>
  try {
    var savedTheme = localStorage.getItem('sottolineature-theme');
    if (savedTheme === 'dark') { document.documentElement.setAttribute('data-theme', 'dark'); }
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
    <form class="header-search sans" action="/" method="get" role="search">
      <label class="visually-hidden" for="headerSearch">Cerca fra le citazioni</label>
      <input type="search" id="headerSearch" name="q" placeholder="Cerca autore, parola o frase…" autocomplete="off">
    </form>
    <nav class="site-nav sans" aria-label="Principale">
      <a href="/citazioni/">Citazioni</a>
      <a href="/autori/">Autori</a>
      <a href="/temi/">Temi</a>
      <a href="/le-mie-sottolineature/" aria-current="page">Le mie</a>
      <a href="/metodo/">Metodo</a>
      <button class="theme-toggle" id="themeToggle" type="button" aria-label="Cambia tema chiaro/scuro">&#9790;</button>
    </nav>
  </div>
</header>
<script src="/assets/nav.js" defer></script>
<div class="page">
  <p class="eyebrow sans">La tua raccolta</p>
  <h1>Le mie sottolineature</h1>
  <p class="mine-count sans" id="mineCount"></p>
  <div id="mineList"></div>
  <div class="mine-empty sans" id="mineEmpty" hidden>
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
    <button type="button" id="printBtn">Stampa</button>
  </div>
  <footer class="sans">
    Da <a href="/" style="color:var(--ink-faint)">Sottolineature</a> &mdash; citazioni verificate a mano, senza algoritmo.
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
    emptyEl.hidden = false;
    return;
  }

  // Le chiavi salvate sono slug. Quelle vecchie (autore|titolo) si convertono
  // al volo, cosi' la pagina funziona anche per chi non e' ancora passato
  // dalla home dopo l'aggiornamento.
  var slugs = [];
  var noteBySlug = {};
  function addKey(k, note) {
    var list = k.indexOf('|') === -1 ? [k] : (LEGACY[k] || []);
    list.forEach(function (slug) {
      if (slugs.indexOf(slug) === -1) { slugs.push(slug); }
      if (note && !noteBySlug[slug]) { noteBySlug[slug] = note; }
    });
  }
  underlined.forEach(function (k) { addKey(k, (notes[k] || '').trim()); });
  slugs = slugs.filter(function (s) { return SLUG_INDEX[s] !== undefined; });
  if (!slugs.length) { emptyEl.hidden = false; return; }

  fetch('/data/citazioni.json').then(function (r) { return r.json(); }).then(function (quotes) {
    var found = slugs.map(function (slug) { return { slug: slug, q: quotes[SLUG_INDEX[slug]] }; })
                     .filter(function (x) { return x.q; });
    if (!found.length) { emptyEl.hidden = false; return; }
    countEl.textContent = found.length === 1 ? '1 citazione sottolineata' : found.length + ' citazioni sottolineate';
    list.innerHTML = found.map(function (x) {
      var q = x.q;
      var note = (noteBySlug[x.slug] || '').trim();
      var quoteHtml = '<a href="/citazioni/' + x.slug + '/">&laquo;' + esc(q.quote) + '&raquo;</a>';
      return '<article class="mine-item">' +
        '<p class="mine-quote">' + quoteHtml + '</p>' +
        '<p class="mine-meta sans">' + esc(q.author) + ' &mdash; <em>' + esc(q.title) + '</em>' +
        (q.year ? ' &middot; ' + esc(q.year) : '') + '</p>' +
        (note ? '<p class="mine-note sans"><span class="mine-note-label">La tua nota</span>' + esc(note) + '</p>' : '') +
        '</article>';
    }).join('');
    toolsEl.hidden = false;
    document.getElementById('printBtn').addEventListener('click', function () { window.print(); });
  }).catch(function () {
    emptyEl.hidden = false;
  });
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
