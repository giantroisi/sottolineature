/*
 * Controllo runtime per lo scorrimento orizzontale su viewport mobile.
 *
 * Va eseguito in una pagina gia' caricata, con viewport 375x812 o 390x844.
 * Restituisce un oggetto serializzabile e non modifica la pagina. Gli elementi
 * invisibili e quelli larghi zero vengono ignorati; uno scroller intenzionale
 * con overflow-x:auto/scroll non e' considerato un errore finche' il suo box
 * resta dentro la viewport.
 */
(function () {
  'use strict';

  function checkMobileOverflow() {
    var root = document.documentElement;
    var viewportWidth = root.clientWidth;
    var tolerance = 1;
    var offenders = [];

    Array.prototype.forEach.call(document.querySelectorAll('body *'), function (element) {
      var style = window.getComputedStyle(element);
      if (style.display === 'none' || style.visibility === 'hidden') { return; }
      var rect = element.getBoundingClientRect();
      if (!rect.width || !rect.height) { return; }
      var scrollsItself = (style.overflowX === 'auto' || style.overflowX === 'scroll') &&
                          element.scrollWidth > element.clientWidth;
      if (scrollsItself && rect.left >= -tolerance && rect.right <= viewportWidth + tolerance) {
        return;
      }
      if (rect.left < -tolerance || rect.right > viewportWidth + tolerance) {
        offenders.push({
          tag: element.tagName.toLowerCase(),
          id: element.id || '',
          className: typeof element.className === 'string' ? element.className : '',
          left: Math.round(rect.left * 10) / 10,
          right: Math.round(rect.right * 10) / 10,
          width: Math.round(rect.width * 10) / 10
        });
      }
    });

    return {
      ok: root.scrollWidth <= viewportWidth + tolerance && offenders.length === 0,
      viewportWidth: viewportWidth,
      documentWidth: root.scrollWidth,
      offenders: offenders.slice(0, 20)
    };
  }

  window.SottolineatureCheckMobileOverflow = checkMobileOverflow;
  return checkMobileOverflow();
})();
