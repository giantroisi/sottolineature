/* Generazione dell'immagine di condivisione (canvas).
 *
 * Vive qui e non dentro le pagine perche' serve sia alla home sia alle 445
 * pagine citazione: inline sarebbero 8 KB moltiplicati per ogni pagina, qui
 * e' un file solo che il browser scarica una volta e tiene in cache.
 *
 * Uso:
 *   Sottolineature.share(citazione, autore, titolo, anno, pulsante, formato, variante)
 *   formato:  'post' (1080x1350, predefinito) oppure 'storia' (1080x1920)
 *   variante: 'chiaro' | 'scuro'; se assente segue il tema della pagina
 */
(function () {
  'use strict';

  function wrapCanvasText(ctx, text, maxWidth) {
    var words = text.split(' ');
    var lines = [];
    var current = '';
    words.forEach(function (word) {
      var test = current ? current + ' ' + word : word;
      if (ctx.measureText(test).width > maxWidth && current) {
        lines.push(current);
        current = word;
      } else {
        current = test;
      }
    });
    if (current) { lines.push(current); }
    return lines;
  }

  var shareLogoImg = new Image();
  shareLogoImg.src = '/logo.svg';

  // Ricolora il logo (inchiostro nero su fondo trasparente) nel colore dato,
  // conservando la trasparenza. Si usa la composizione invece di ctx.filter,
  // che Safari non supporta in modo affidabile sul canvas.
  function tintedLogo(img, color, w, h) {
    var off = document.createElement('canvas');
    off.width = Math.max(1, Math.round(w));
    off.height = Math.max(1, Math.round(h));
    var octx = off.getContext('2d');
    octx.drawImage(img, 0, 0, off.width, off.height);
    octx.globalCompositeOperation = 'source-in';
    octx.fillStyle = color;
    octx.fillRect(0, 0, off.width, off.height);
    return off;
  }

  // Formati di condivisione. Nelle storie Instagram sovrappone la propria
  // interfaccia sopra e sotto: i margini verticali ampi tengono il contenuto
  // dentro la zona sicura, così il logo non finisce sotto la barra dei messaggi.
  var SHARE_FORMATS = {
    post: { w: 1080, h: 1350, marginTop: 40, marginBottom: 40, label: 'post' },
    storia: { w: 1080, h: 1920, marginTop: 250, marginBottom: 280, label: 'storia' }
  };
  // Formato usato dal pulsante Condividi. Si usa 4:5 perché è il più
  // tollerante: pubblicato in una storia resta tutto visibile (con due bande),
  // mentre un 9:16 messo nel feed verrebbe ritagliato e perderebbe il logo.
  var DEFAULT_SHARE_FORMAT = 'post';

  function downloadQuoteImage(quote, author, title, year, btn, formatName, variantName) {
    var fmt = SHARE_FORMATS[formatName || DEFAULT_SHARE_FORMAT] || SHARE_FORMATS.post;
    var width = fmt.w;
    var height = fmt.h;
    var padding = 90;
    var maxWidth = width - padding * 2;
    var canvas = document.createElement('canvas');
    canvas.width = width;
    canvas.height = height;
    var ctx = canvas.getContext('2d');

    var cx = width / 2;
    var frameTop = fmt.marginTop;
    var frameBottom = height - fmt.marginBottom;

    // La variante (chiaro/scuro) e' indipendente dal tema della pagina: chi
    // legge di giorno puo' comunque condividere l'immagine scura, e viceversa.
    // Senza variante si segue il tema attivo, com'era prima.
    var variant = variantName;
    if (variant !== 'chiaro' && variant !== 'scuro') {
      variant = document.documentElement.getAttribute('data-theme') === 'dark' ? 'scuro' : 'chiaro';
    }
    var isDarkTheme = variant === 'scuro';
    var palette = isDarkTheme
      ? { paper: '#16191a', rule: '#33362f', gold: '#c9a45c', ink: '#ece7dd', inkSoft: '#a9a296' }
      : { paper: '#f2f0eb', rule: '#ddd9cf', gold: '#9c7a3c', ink: '#211f1b', inkSoft: '#5b564d' };
    var colPaper = palette.paper;
    var colRule = palette.rule;
    var colGold = palette.gold;
    var colInk = palette.ink;
    var colInkSoft = palette.inkSoft;

    ctx.fillStyle = colPaper;
    ctx.fillRect(0, 0, width, height);
    ctx.strokeStyle = colRule;
    ctx.lineWidth = 2;
    ctx.strokeRect(40, frameTop, width - 80, frameBottom - frameTop);

    ctx.textAlign = 'center';
    ctx.textBaseline = 'alphabetic';

    // --- blocco firma in basso: logo + url ---
    var urlBaseline = frameBottom - 52;
    var brandTop = urlBaseline;
    if (shareLogoImg.complete && shareLogoImg.naturalWidth > 0) {
      var logoH = 92;
      var logoW = logoH * (shareLogoImg.naturalWidth / shareLogoImg.naturalHeight);
      var logoTop = urlBaseline - 34 - logoH;
      // il logo è a inchiostro nero: sul fondo scuro va schiarito, come nel sito
      var logoSource = isDarkTheme
        ? tintedLogo(shareLogoImg, colInk, logoW, logoH)
        : shareLogoImg;
      ctx.drawImage(logoSource, cx - logoW / 2, logoTop, logoW, logoH);
      brandTop = logoTop;
    }
    ctx.fillStyle = colGold;
    ctx.font = '22px -apple-system, "Helvetica Neue", Arial, sans-serif';
    var urlLetterSpacing = 5;
    ctx.letterSpacing = urlLetterSpacing + 'px';
    // la spaziatura viene aggiunta anche dopo l'ultima lettera: si recupera meta
    ctx.fillText('SOTTOLINEATURE.IT', cx + urlLetterSpacing / 2, urlBaseline);
    ctx.letterSpacing = '0px';

    // Citazione e attribuzione formano un blocco unico, centrato nello spazio
    // sopra la firma: così l'attribuzione resta legata alla citazione invece
    // di sembrare appartenere al logo.
    var markSize = 108;
    var markGap = 26;
    var quoteToAuthorGap = 78;
    var authorToWorkGap = 46;
    var workLineHeight = 37;

    var areaTop = frameTop + 100;
    var areaBottom = brandTop - 104;

    // opera (titolo · anno), in corsivo
    var work = title + (year ? ' · ' + year : '');
    ctx.font = 'italic 27px "Iowan Old Style", Georgia, serif';
    var workLines = wrapCanvasText(ctx, work, maxWidth).slice(0, 2);
    var workHeight = (workLines.length - 1) * workLineHeight;

    // autore in maiuscolo spaziato, rimpicciolito se il nome è lungo
    var authorText = author.toUpperCase();
    var authorSpacing = 6;
    var authorSize = 26;
    ctx.letterSpacing = authorSpacing + 'px';
    while (authorSize > 16) {
      ctx.font = authorSize + 'px -apple-system, "Helvetica Neue", Arial, sans-serif';
      if (ctx.measureText(authorText).width <= maxWidth) { break; }
      authorSize -= 1;
    }
    ctx.letterSpacing = '0px';

    var attributionHeight = quoteToAuthorGap + authorSize + authorToWorkGap + workHeight;

    // corpo della citazione: il più grande che entra nello spazio restante
    var sizes = [72, 64, 58, 52, 46, 40, 35, 30, 26, 22];
    var chosenLines = [];
    var chosenSize = sizes[sizes.length - 1];
    var lineHeight = 0;
    var maxTextHeight = (areaBottom - areaTop) - markSize - markGap - attributionHeight;
    for (var i = 0; i < sizes.length; i++) {
      ctx.font = 'italic ' + sizes[i] + 'px "Iowan Old Style", Georgia, serif';
      var lines = wrapCanvasText(ctx, quote, maxWidth);
      lineHeight = Math.round(sizes[i] * 1.45);
      if (lines.length * lineHeight <= maxTextHeight || i === sizes.length - 1) {
        chosenLines = lines;
        chosenSize = sizes[i];
        break;
      }
    }

    var textHeight = chosenLines.length * lineHeight;
    var groupHeight = markSize + markGap + textHeight + attributionHeight;
    var groupTop = areaTop + ((areaBottom - areaTop) - groupHeight) / 2;

    // virgolette
    ctx.fillStyle = colGold;
    ctx.font = markSize + 'px Georgia, serif';
    ctx.fillText('“', cx, groupTop + markSize * 0.82);

    // testo della citazione
    ctx.fillStyle = colInk;
    ctx.font = 'italic ' + chosenSize + 'px "Iowan Old Style", Georgia, serif';
    var textY = groupTop + markSize + markGap + chosenSize;
    chosenLines.forEach(function (line) {
      ctx.fillText(line, cx, textY);
      textY += lineHeight;
    });

    // autore
    var quoteBottom = groupTop + markSize + markGap + textHeight;
    var authorBaseline = quoteBottom + quoteToAuthorGap;
    ctx.fillStyle = colInk;
    ctx.font = authorSize + 'px -apple-system, "Helvetica Neue", Arial, sans-serif';
    ctx.letterSpacing = authorSpacing + 'px';
    ctx.fillText(authorText, cx + authorSpacing / 2, authorBaseline);
    ctx.letterSpacing = '0px';

    // opera
    ctx.fillStyle = colInkSoft;
    ctx.font = 'italic 27px "Iowan Old Style", Georgia, serif';
    var workY = authorBaseline + authorToWorkGap;
    workLines.forEach(function (line) {
      ctx.fillText(line, cx, workY);
      workY += workLineHeight;
    });

    canvas.toBlob(function (blob) {
      var filename = 'sottolineature-' + author.toLowerCase().replace(/[^a-z0-9]+/g, '-') + '-' + fmt.label + '.png';
      var original = btn ? btn.textContent : '';

      function feedback(text) {
        if (!btn) { return; }
        btn.textContent = text;
        setTimeout(function () { btn.textContent = original; }, 1400);
      }

      function downloadFallback() {
        var url = URL.createObjectURL(blob);
        var a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        setTimeout(function () { URL.revokeObjectURL(url); }, 2000);
        feedback('Scaricata');
      }

      var file = new File([blob], filename, { type: 'image/png' });
      if (navigator.canShare && navigator.canShare({ files: [file] })) {
        navigator.share({
          files: [file],
          title: 'Sottolineature',
          text: '"' + quote + '" — ' + author
        }).then(function () {
          feedback('Condiviso');
        }).catch(function (err) {
          if (err && err.name === 'AbortError') { return; }
          downloadFallback();
        });
      } else {
        downloadFallback();
      }
    }, 'image/png');
  }
  window.Sottolineature = window.Sottolineature || {};
  window.Sottolineature.share = downloadQuoteImage;
  window.Sottolineature.SHARE_FORMATS = SHARE_FORMATS;
})();
