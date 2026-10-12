/* Riusa assets/share.js senza browser: nessuna seconda composizione da mantenere.
 * npm install --prefix tools/social-images, poi python3 tools/build.py.
 * I font di sistema vengono usati ma non copiati/distribuiti nel repository. */
'use strict';
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const { createCanvas, loadImage, GlobalFonts } = require('@napi-rs/canvas');

async function main() {
  const root = path.resolve(__dirname, '../..');
  const input = JSON.parse(fs.readFileSync(0, 'utf8'));
  for (const [filename, family] of [
    ['Iowan Old Style.ttc', 'Iowan Old Style'], ['Georgia.ttf', 'Georgia'],
    ['Arial.ttf', 'Arial'], ['Arial.ttf', '-apple-system'],
    ['Arial.ttf', 'Helvetica Neue'],
  ]) {
    const candidates = [path.join(root, 'assets/fonts', filename),
      path.join('/System/Library/Fonts/Supplemental', filename)];
    const font = candidates.find(p => fs.existsSync(p));
    if (!font) throw new Error('Font mancante: ' + filename);
    if (!GlobalFonts.registerFromPath(font, family)) throw new Error('Font non caricabile: ' + font);
  }
  const logo = await loadImage(fs.readFileSync(path.join(root, 'logo.svg')));
  // Queste sono le sole API DOM usate dal disegno esistente, non dal download.
  const shareLogo = { complete: true, naturalWidth: logo.width,
    naturalHeight: logo.height, _image: logo, set src(value) {
      if (value !== '/logo.svg') throw new Error('Risorsa inattesa: ' + value);
    }};
  function canvas(w, h) {
    const result = createCanvas(w, h);
    result.socialText = [];
    const getContext = result.getContext.bind(result);
    result.getContext = function(kind) {
      const context = getContext(kind);
      const drawImage = context.drawImage.bind(context);
      context.drawImage = (source, ...args) => drawImage(source._image || source, ...args);
      const fillText = context.fillText.bind(context);
      context.fillText = (text, x, y, ...args) => {
        const measure = context.measureText(text);
        result.socialText.push({text, left: x - measure.width / 2,
          right: x + measure.width / 2, top: y - measure.actualBoundingBoxAscent,
          bottom: y + measure.actualBoundingBoxDescent});
        return fillText(text, x, y, ...args);
      };
      return context;
    };
    return result;
  }
  const sandbox = {
    window: {}, Image: function() { return shareLogo; },
    document: {
      createElement: name => {
        if (name !== 'canvas') throw new Error('Elemento inatteso: ' + name);
        return canvas(1, 1);
      },
      documentElement: { getAttribute: () => null },
    },
  };
  vm.runInNewContext(fs.readFileSync(path.join(root, 'assets/share.js'), 'utf8'), sandbox,
    { timeout: 10000, filename: 'assets/share.js' });
  const output = path.join(root, 'assets/social');
  fs.mkdirSync(output, { recursive: true });
  for (const item of input.entries) {
    for (const variant of ['chiaro', 'scuro']) {
      const { canvas: image, fmt } = sandbox.window.Sottolineature.disegna(
        item.quote, item.author, item.title, item.year, input.format, variant);
      const expectedHeight = {post: 1350, storia: 1920}[input.format];
      if (fmt.w !== 1080 || fmt.h !== expectedHeight) throw new Error('Formato social inatteso');
      if (image.socialText.some(t => t.left < fmt.inserto || t.right > fmt.w - fmt.inserto ||
          t.top < fmt.marginTop || t.bottom > fmt.h - fmt.marginBottom)) {
        throw new Error('Testo fuori dalla cornice: ' + item.slug + '-' + variant);
      }
      const drawn = image.socialText.slice(2, -1).map(t => t.text).join(' ');
      const normalized = value => value.replace(/\s+/g, ' ').trim();
      if (!normalized(drawn).includes(normalized(item.quote))) {
        throw new Error('Citazione incompleta nella grafica: ' + item.slug);
      }
      const work = item.title + (item.year ? ' · ' + item.year : '');
      if (!normalized(image.socialText.map(t => t.text).join(' ')).endsWith(normalized(work))) {
        throw new Error('Titolo incompleto nella grafica: ' + item.slug);
      }
      fs.writeFileSync(path.join(output, item.slug + '-' + variant + '.png'), image.toBuffer('image/png'));
    }
  }
}
main().catch(error => { console.error(error.message); process.exitCode = 1; });
