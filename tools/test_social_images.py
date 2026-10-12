"""Regressioni dell'archivio: HTML scansionabile, due temi, immagini vere."""
import json
from pathlib import Path
import sys
import unittest
from unittest import mock
import urllib.parse
import xml.etree.ElementTree as ET

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
import social_images
import generate_quote_pages as qp

SLUG = 'dante-alighieri-inferno-divina-commedia'


class SocialImageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.entries, _ = qp.assign_slugs(qp.load_quotes(), qp.load_slugs(), qp.load_redirects())
        cls.quote = dict(cls.entries)[SLUG]

    def test_all_existing_quotes_are_selected(self):
        self.assertEqual(social_images.configuration()['scope'], 'all')
        self.assertEqual(social_images.configuration()['format'], 'storia')
        self.assertEqual(set(social_images.selected_slugs()), {slug for slug, _ in self.entries})
        self.assertEqual(self.quote['quote'], "Amor, ch'a nullo amato amar perdona.")

    def test_two_real_static_urls_are_versioned(self):
        urls = social_images.image_urls(SLUG)
        self.assertEqual(len(urls), 2)
        for url in urls:
            parsed = urllib.parse.urlsplit(url)
            self.assertTrue((social_images.ROOT / parsed.path.lstrip('/')).is_file())
            self.assertRegex(parsed.query, r'^v=[a-f0-9]{12}$')

    def test_unknown_quotes_do_not_get_markup_or_assets(self):
        other = 'citazione-non-esistente'
        self.assertEqual(social_images.image_urls(other), [])
        self.assertEqual(social_images.render_head(other), '')
        self.assertEqual(social_images.render_figure(other, self.quote), '')

    def test_html_uses_real_img_sources_alt_dimensions_and_lazy_loading(self):
        markup = social_images.render_figure(SLUG, self.quote)
        self.assertEqual(markup.count('<img src="/assets/social/'), 2)
        self.assertEqual(markup.count('width="1080" height="1920" loading="lazy" decoding="async"'), 2)
        self.assertIn('Dante Alighieri', markup)
        self.assertIn('Inferno, canto V, v. 103', markup)
        self.assertIn('versione chiara', markup)
        self.assertIn('versione scura', markup)
        self.assertNotIn('data:image', markup)
        self.assertNotIn('<canvas', markup)

    def test_png_dimensions_palette_and_centered_frame(self):
        for variant, color in [('chiaro', (242, 240, 235)), ('scuro', (22, 25, 26))]:
            path = social_images.ROOT / 'assets/social' / (SLUG + '-' + variant + '.png')
            with Image.open(path) as source:
                self.assertEqual(source.size, (1080, 1920))
                image = source.convert('RGB')
            self.assertEqual(image.getpixel((0, 0)), color)
            rows = [y for y in range(image.height) if image.getpixel((72, y)) != color]
            # La Storia originale ha margini 224/236: centro della cornice a 954.
            self.assertLessEqual(abs((min(rows) + max(rows)) / 2 - 954), 1)
            self.assertLess(path.stat().st_size, 200000)

    def test_image_sitemap_refers_to_every_quote_and_actual_assets(self):
        tree = ET.parse(social_images.ROOT / 'sitemap-citazioni.xml')
        ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9',
              'i': 'http://www.google.com/schemas/sitemap-image/1.1'}
        selected = [u for u in tree.getroot() if u.findall('i:image', ns)]
        self.assertEqual(len(selected), len(self.entries))
        actual = {u.find('s:loc', ns).text: [n.text for n in u.findall('i:image/i:loc', ns)]
                  for u in selected}
        for slug, _ in self.entries:
            self.assertEqual(actual[qp.SITE_URL + '/citazioni/' + slug + '/'],
                             [qp.SITE_URL + u for u in social_images.image_urls(slug)])

    def test_every_quote_has_both_images_and_one_section(self):
        manifest = json.loads(social_images.MANIFEST.read_text())
        self.assertEqual(len(manifest['images']), 2 * len(self.entries))
        for slug, quote in self.entries:
            page = (social_images.ROOT / 'citazioni' / (slug + '.html')).read_text()
            self.assertEqual(page.count('<section class="quote-social"'), 1, slug)
            for url in social_images.image_urls(slug):
                self.assertIn('<img src="' + url + '"', page, slug)
            for variant in social_images.VARIANTS:
                with Image.open(social_images.ROOT / 'assets/social' / (slug + '-' + variant + '.png')) as image:
                    self.assertEqual(image.size, (1080, 1920), slug)

    def test_unchanged_inputs_do_not_regenerate_images(self):
        with mock.patch.object(social_images.subprocess, 'run') as renderer:
            social_images.generate(self.entries)
        renderer.assert_not_called()

    def test_unknown_quote_stops_before_rendering(self):
        with mock.patch.object(social_images, 'configuration', return_value={
                'format': 'post', 'slugs': ['non-esiste']}):
            with self.assertRaisesRegex(ValueError, 'assenti'):
                social_images.generate(self.entries)


if __name__ == '__main__':
    unittest.main()
