"""Gli URL attivi non possono sovrapporsi ai redirect delle correzioni editoriali."""
import copy
import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_quote_pages as qp


class QuoteSlugTests(unittest.TestCase):
    def test_archive_has_no_redirect_source_as_active_quote(self):
        entries, changed = qp.assign_slugs(qp.load_quotes(), qp.load_slugs(), qp.load_redirects())
        self.assertFalse(changed)
        routes = {'/citazioni/' + slug + '/' for slug, _ in entries}
        self.assertFalse(routes & {r['from'] for r in qp.load_redirects()})

    def test_accabadora_incipit_has_its_own_address_and_historical_redirect_is_preserved(self):
        entries, _ = qp.assign_slugs(qp.load_quotes(), qp.load_slugs(), qp.load_redirects())
        selected = [(slug, q) for slug, q in entries
                    if q['author'] == 'Michela Murgia' and q['quote'].startswith('Fillus de anima.')]
        self.assertEqual(len(selected), 1)
        slug, quote = selected[0]
        self.assertEqual(slug, 'michela-murgia-accabadora-fillus-de-anima')
        self.assertEqual(quote['title'], 'Accabadora')
        self.assertIn({'from': '/citazioni/michela-murgia-accabadora/',
                       'to': '/citazioni/michela-murgia-chiru/'}, qp.load_redirects())
        self.assertIn('/citazioni/' + slug + '/', (Path(qp.ROOT) / 'sitemap-citazioni.xml').read_text())
        self.assertNotIn('<loc>' + qp.SITE_URL + '/citazioni/michela-murgia-accabadora/</loc>',
                         (Path(qp.ROOT) / 'sitemap-citazioni.xml').read_text())

    def test_new_quote_uses_incipit_instead_of_a_reserved_base(self):
        quote = {'author': 'Autore Prova', 'title': 'Opera Prova', 'quote': 'Una frase mai pubblicata'}
        redirects = [{'from': '/citazioni/autore-prova-opera-prova/', 'to': '/citazioni/altra/'}]
        entries, changed = qp.assign_slugs([quote], {'quotes': {}, 'authors': {}}, redirects)
        self.assertTrue(changed)
        self.assertEqual(entries[0][0], 'autore-prova-opera-prova-una-frase-mai')

    def test_conflicting_frozen_slug_is_an_error_not_a_silent_rename(self):
        quote = {'author': 'Autore Prova', 'title': 'Opera Prova', 'quote': 'Una frase mai pubblicata'}
        slugs = {'quotes': {qp.quote_key(quote): 'autore-prova-opera-prova'}}
        before = copy.deepcopy(slugs)
        redirects = [{'from': '/citazioni/autore-prova-opera-prova/', 'to': '/citazioni/altra/'}]
        with self.assertRaisesRegex(ValueError, 'redirect storico'):
            qp.assign_slugs([quote], slugs, redirects)
        self.assertEqual(before, slugs)


if __name__ == '__main__':
    unittest.main()
