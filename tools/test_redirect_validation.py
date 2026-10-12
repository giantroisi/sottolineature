"""Regressioni per collisioni e catene nei redirect pubblici."""
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from redirect_validation import public_html_routes, validate_redirects


class RedirectValidationTests(unittest.TestCase):
    def test_public_routes_cover_root_nested_indexes_and_clean_urls(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'index.html').write_text('home')
            (root / 'privacy.html').write_text('privacy')
            (root / 'citazioni').mkdir()
            (root / 'citazioni' / 'frase.html').write_text('frase')
            (root / 'opere').mkdir()
            (root / 'opere' / 'index.html').write_text('opere')
            (root / 'templates').mkdir()
            (root / 'templates' / 'pagina.html').write_text('template')
            self.assertEqual(public_html_routes(root), {
                '/', '/privacy/', '/citazioni/frase/', '/opere/'
            })

    def test_redirect_source_cannot_be_a_public_page(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'citazioni').mkdir()
            (root / 'citazioni' / 'esistente.html').write_text('pagina')
            redirects = [{'from': '/citazioni/esistente/', 'to': '/citazioni/altra/'}]
            with self.assertRaisesRegex(ValueError, 'pagine pubbliche.*esistente'):
                validate_redirects(redirects, root)

    def test_redirect_chain_reports_the_complete_path(self):
        redirects = [
            {'from': '/prima/', 'to': '/seconda/'},
            {'from': '/seconda/', 'to': '/finale/'},
        ]
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(ValueError, '/prima/ -> /seconda/ -> /finale/'):
                validate_redirects(redirects, directory)

    def test_flat_redirects_are_valid(self):
        redirects = [
            {'from': '/vecchia/', 'to': '/finale/'},
            {'from': '/altra-vecchia/', 'to': '/finale/'},
        ]
        with tempfile.TemporaryDirectory() as directory:
            validate_redirects(redirects, directory)


if __name__ == '__main__':
    unittest.main()

