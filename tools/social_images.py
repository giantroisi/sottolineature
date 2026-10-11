"""Immagini social statiche: solo citazioni realmente presenti nell'archivio."""
from functools import lru_cache
import hashlib
import html
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / 'data/social_images.json'
MANIFEST = ROOT / 'assets/social/manifest.json'
VARIANTS = ('chiaro', 'scuro')


def configuration():
    data = json.loads(CONFIG.read_text(encoding='utf-8'))
    if data['format'] != 'post':
        raise ValueError('Le immagini della pagina usano il formato post 1080x1350')
    slugs = data['slugs']
    if data.get('scope', 'selected') not in ('selected', 'all'):
        raise ValueError('Ambito social non valido')
    if len(slugs) != len(set(slugs)) or any(
            not slug or any(c not in 'abcdefghijklmnopqrstuvwxyz0123456789-' for c in slug)
            for slug in slugs):
        raise ValueError('Slug social duplicati o non validi')
    return data


@lru_cache(maxsize=1)
def archive_slugs():
    import generate_quote_pages as qp
    entries, _ = qp.assign_slugs(qp.load_quotes(), qp.load_slugs(), qp.load_redirects())
    return tuple(slug for slug, _ in entries)


def selected_slugs(entries=None):
    config = configuration()
    if config.get('scope') == 'all':
        return [slug for slug, _ in entries] if entries is not None else archive_slugs()
    return config['slugs']


def generate(entries):
    """Rigenera solo quando quote, logo o renderer cambiano; errore esplicito se manca un prerequisito."""
    config = configuration()
    by_slug = dict(entries)
    slugs = selected_slugs(entries)
    unknown = set(slugs) - set(by_slug)
    if unknown:
        raise ValueError('Citazioni social assenti dall\'archivio: ' + ', '.join(sorted(unknown)))
    payload = {'format': config['format'], 'entries': [
        {'slug': slug, **{key: by_slug[slug].get(key, '')
                         for key in ('quote', 'author', 'title', 'year')}}
        for slug in slugs]}
    source = json.dumps(payload, ensure_ascii=False).encode('utf-8')
    fingerprint = hashlib.sha256(source + b''.join((ROOT / name).read_bytes() for name in (
        'assets/share.js', 'logo.svg', 'tools/social-images/render.cjs',
        'tools/social-images/package.json', 'tools/social-images/package-lock.json'))).hexdigest()
    images = [ROOT / 'assets/social' / (slug + '-' + variant + '.png')
              for slug in slugs for variant in VARIANTS]
    if MANIFEST.exists():
        previous = json.loads(MANIFEST.read_text())
        if previous.get('source_sha256') == fingerprint and all(
                p.exists() and previous.get('images', {}).get(p.name) ==
                hashlib.sha256(p.read_bytes()).hexdigest() for p in images):
            print('Immagini social gia aggiornate:', len(images))
            return
    subprocess.run([os.environ.get('SOTTOLINEATURE_NODE', 'node'),
                    str(ROOT / 'tools/social-images/render.cjs')],
                   input=source, check=True, cwd=ROOT)
    MANIFEST.write_text(json.dumps({
        'source_sha256': fingerprint,
        'images': {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in images},
    }, indent=2) + '\n', encoding='utf-8')
    print('Immagini social generate:', len(images))


def image_urls(slug):
    if slug not in selected_slugs():
        return []
    urls = []
    for variant in VARIANTS:
        filename = slug + '-' + variant + '.png'
        data = (ROOT / 'assets/social' / filename).read_bytes()
        urls.append('/assets/social/' + filename + '?v=' + hashlib.sha256(data).hexdigest()[:12])
    return urls


def render_head(slug):
    if not image_urls(slug):
        return ''
    version = hashlib.sha256((ROOT / 'assets/quote-social.css').read_bytes()).hexdigest()[:12]
    return '<link rel="stylesheet" href="/assets/quote-social.css?v=' + version + '">\n'


def render_figure(slug, quote):
    urls = image_urls(slug)
    if not urls:
        return ''
    links = []
    for variant, url in zip(VARIANTS, urls):
        alt = ('«' + quote['quote'] + '» — ' + quote['author'] + ', ' + quote['title'] +
               ' (' + quote['year'] + '). Grafica Sottolineature, versione ' +
               ('chiara' if variant == 'chiaro' else 'scura') + '.')
        links.append('<a class="quote-social-' + variant + '" href="' + url + '">'
                     '<img src="' + url + '" alt="' + html.escape(alt, quote=True) + '" '
                     'width="1080" height="1350" loading="lazy" decoding="async"></a>')
    return ('  <section class="quote-social" aria-labelledby="quoteSocialHeading">\n'
            '    <h2 class="sans" id="quoteSocialHeading">La citazione in immagine</h2>\n'
            '    <figure>' + ''.join(links) + '<figcaption class="sans">'
            'Grafica Sottolineature · ' + html.escape(quote['source_locus']) +
            '</figcaption></figure>\n  </section>\n')


def sitemap_images(slug, site_url):
    return ''.join('<image:image><image:loc>' + html.escape(site_url + url) +
                   '</image:loc></image:image>' for url in image_urls(slug))
