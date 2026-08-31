/* Comportamenti comuni all'intestazione.
 * Per ora uno solo: il contatore sulla voce "Le mie". Senza, la voce sembra
 * vuota anche quando dentro ci sono venti citazioni, ed e' il motivo per cui
 * la funzione Sottolinea passava inosservata.
 * E' esposto come Sottolineature.refreshNavCount() perche' le pagine dove si
 * sottolinea o si toglie una sottolineatura possano aggiornarlo subito invece
 * di lasciare un numero vecchio finche' non si ricarica. */
(function () {
  'use strict';
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
  window.Sottolineature = window.Sottolineature || {};
  window.Sottolineature.refreshNavCount = refresh;
  refresh();
})();
