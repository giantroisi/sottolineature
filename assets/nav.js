/* Comportamenti comuni all'intestazione.
 * Per ora uno solo: il contatore sulla voce "Le mie". Senza, la voce sembra
 * vuota anche quando dentro ci sono venti citazioni, ed e' il motivo per cui
 * la funzione Sottolinea passava inosservata.
 * E' esposto come Sottolineature.refreshNavCount() perche' le pagine dove si
 * sottolinea o si toglie una sottolineatura possano aggiornarlo subito invece
 * di lasciare un numero vecchio finche' non si ricarica. */
(function () {
  'use strict';
  // Riparazione una tantum, 2026-09-01: vedi il commento nelle pagine che
  // leggono le sottolineature. Qui serve perche' il contatore sulla voce
  // "Le mie" compare su ogni pagina del sito, anche su quelle che l'elenco
  // non lo scrivono mai.
  try {
    if (localStorage.getItem('sottolineature-reset') !== '2026-09-01') {
      localStorage.removeItem('sottolineature-underlined');
      localStorage.setItem('sottolineature-reset', '2026-09-01');
    }
  } catch (e) {}
  function count() {
    try {
      var stored = JSON.parse(localStorage.getItem('sottolineature-underlined') || '[]');
      return Array.isArray(stored) ? stored.length : 0;
    } catch (e) { return 0; }
  }
  function refresh() {
    var link = document.getElementById('navMine');
    if (!link) { return; }
    var badge = link.querySelector('.nav-count');
    var n = count();
    if (!n) {
      if (badge) { badge.parentNode.removeChild(badge); }
      return;
    }
    if (!badge) {
      badge = document.createElement('span');
      badge.className = 'nav-count';
      link.appendChild(badge);
    }
    badge.textContent = n;
    badge.setAttribute('aria-label', n === 1 ? '1 citazione sottolineata' : n + ' citazioni sottolineate');
  }
  // --- colore della barra di stato -------------------------------------
  // Su telefono la striscia in alto (ora, batteria, segnale) prende il colore
  // da <meta name="theme-color">. Le due meta nell'head lo legano al tema del
  // sistema, e per il primo disegno basta; ma il sito ha un interruttore
  // proprio, e chi teneva il telefono in chiaro e il sito in scuro vedeva una
  // striscia bianca sopra una pagina nera. Qui le meta si allineano al tema
  // che si sta davvero mostrando.
  var COLORE = { light: '#f2f0eb', dark: '#16191a' };
  function temaCorrente() {
    return document.documentElement.getAttribute('data-theme') === 'dark' ? 'dark' : 'light';
  }
  function allineaBarra() {
    var metas = document.querySelectorAll('meta[name="theme-color"]');
    if (!metas.length) { return; }
    var c = COLORE[temaCorrente()];
    for (var i = 0; i < metas.length; i++) { metas[i].setAttribute('content', c); }
  }
  window.Sottolineature = window.Sottolineature || {};
  window.Sottolineature.allineaBarraDiStato = allineaBarra;
  // il primo colore lo mette gia' lo script in testa alla pagina, prima del
  // disegno; qui si ripassa per sicurezza e si resta in ascolto dell'interruttore
  allineaBarra();
  // e ogni volta che qualcuno tocca l'interruttore
  document.addEventListener('click', function (e) {
    var t = e.target;
    if (t && t.closest && t.closest('.theme-toggle')) { setTimeout(allineaBarra, 0); }
  });

  window.Sottolineature = window.Sottolineature || {};
  window.Sottolineature.refreshNavCount = refresh;
  refresh();
})();
