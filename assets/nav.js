/* Comportamenti comuni all'intestazione.
 * Per ora uno solo: il contatore sulla voce "Le mie". Senza, la voce sembra
 * vuota anche quando dentro ci sono venti citazioni, ed e' il motivo per cui
 * la funzione Sottolinea passava inosservata. */
(function () {
  'use strict';
  var link = document.getElementById('navMine');
  if (!link) { return; }
  var n = 0;
  try {
    var stored = JSON.parse(localStorage.getItem('sottolineature-underlined') || '[]');
    n = Array.isArray(stored) ? stored.length : 0;
  } catch (e) { return; }
  if (!n) { return; }
  var badge = document.createElement('span');
  badge.className = 'nav-count';
  badge.textContent = n;
  badge.setAttribute('aria-label', n === 1 ? '1 citazione sottolineata' : n + ' citazioni sottolineate');
  link.appendChild(badge);
})();
