"""Crediti e descrizioni dei ritratti, senza modificare l'archivio."""
import unittest

from generate_hub_pages import immagine_jsonld, ritratto_html


class AuthorPortraitTests(unittest.TestCase):
    def setUp(self):
        self.image = {
            'file': '/assets/autori/esempio.jpg', 'fotografo': 'HerB104',
            'licenza': 'CC BY-SA 4.0',
            'licenza_url': 'https://creativecommons.org/licenses/by-sa/4.0',
            'pagina_commons': 'https://commons.wikimedia.org/wiki/File:G.sapienza.jpg',
            'larghezza': 380, 'altezza': 450,
        }

    def test_legacy_description_and_credit_remain_unchanged(self):
        markup = ritratto_html('Autore', self.image)
        self.assertIn('alt="Ritratto di Autore"', markup)
        self.assertIn('width="380" height="450"', markup)
        self.assertIn('Immagine: HerB104', markup)
        self.assertNotIn('ridimensionato', markup)
        schema = immagine_jsonld('Autore', self.image, 'https://sottolineature.it/autori/autore/')
        self.assertEqual(schema['caption'], 'Ritratto di Autore')

    def test_illustrated_description_is_shared_by_alt_and_schema(self):
        self.image['didascalia'] = 'Ritratto illustrato di Goliarda Sapienza'
        markup = ritratto_html('Goliarda Sapienza', self.image)
        self.assertIn('alt="Ritratto illustrato di Goliarda Sapienza"', markup)
        schema = immagine_jsonld('Goliarda Sapienza', self.image,
                                'https://sottolineature.it/autori/goliarda-sapienza/')
        self.assertEqual(schema['caption'], self.image['didascalia'])
        self.assertEqual(schema['creator']['name'], 'HerB104')
        self.assertEqual(schema['license'], self.image['licenza_url'])

    def test_change_notice_and_description_are_escaped(self):
        self.image['nota_modifiche'] = 'Ridimensionato <senza ritagli>'
        self.image['didascalia'] = 'Ritratto "illustrato"'
        markup = ritratto_html('Autore', self.image)
        self.assertIn('Ridimensionato &lt;senza ritagli&gt;', markup)
        self.assertIn('alt="Ritratto &quot;illustrato&quot;"', markup)
        self.assertIn('rel="license nofollow"', markup)
        self.assertIn('Wikimedia Commons', markup)


if __name__ == '__main__':
    unittest.main()
