"""Regressioni SEO su un sito fittizio isolato, senza modificare l'archivio."""
import contextlib
import io
import json
from pathlib import Path
import re
import sys
import tempfile
import unittest
from unittest.mock import patch
from xml.sax.saxutils import escape

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_links as checker


class StructuralValidationTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix='sottolineature-seo-test-')
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        root_patch = patch.object(checker, 'ROOT', str(self.root))
        root_patch.start()
        self.addCleanup(root_patch.stop)
        self.home = self.page('/', 'Home di prova', 'WebSite', '<a href="/citazioni/prova/">Citazione</a>')
        self.quote = self.page('/citazioni/prova/', 'Citazione di prova',
                               ['WebPage', 'Quotation', 'BreadcrumbList'],
                               '<nav class="breadcrumb"><a href="/">Home</a></nav>')
        self.write('index.html', self.home)
        self.write('citazioni/prova.html', self.quote)
        self.sitemaps({'sitemap-pagine.xml': ['/', '/citazioni/prova/']})

    def write(self, name, source):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(source, encoding='utf-8')

    @staticmethod
    def page(route, title, types, body='', noindex=False):
        types = types if isinstance(types, list) else [types]
        graph = json.dumps({'@context': 'https://schema.org', '@graph': [{'@type': t} for t in types]})
        robots = '<meta name="robots" content="noindex,follow">' if noindex else ''
        return (f'<!doctype html><html lang="it"><head><title>{title}</title>'
                f'<meta name="description" content="Descrizione {title}">'
                f'<link rel="canonical" href="{checker.SITE_URL}{route}">{robots}'
                f'<script type="application/ld+json">{graph}</script></head>'
                f'<body><main><h1>{title}</h1>{body}</main></body></html>')

    def sitemaps(self, children):
        prefix = f'xmlns="{checker.SITEMAP_NS}"'
        index = ''.join(f'<sitemap><loc>{checker.SITE_URL}/{escape(name)}</loc></sitemap>' for name in children)
        self.write('sitemap.xml', f'<sitemapindex {prefix}>{index}</sitemapindex>')
        for name, routes in children.items():
            urls = ''.join(f'<url><loc>{escape(checker.SITE_URL + route)}</loc></url>' for route in routes)
            self.write(name, f'<urlset {prefix}>{urls}</urlset>')

    def audit(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            result = checker.main()
        return result, output.getvalue()

    def assert_rejected(self, message):
        result, output = self.audit()
        self.assertEqual(result, 1, output)
        self.assertIn(message, output)

    def test_complete_linked_site_passes(self):
        result, output = self.audit()
        self.assertEqual(result, 0, output)
        self.assertIn('Problemi totali: 0', output)
        self.assertIn('1 file figli, 2 URL', output)

    def test_mobile_grid_columns_have_explicit_full_width(self):
        template = (Path(__file__).resolve().parent.parent / 'templates/home_template.html').read_text()
        # Il blocco segue la griglia desktop: la larghezza esplicita impedisce
        # che content-visibility conservi la vecchia misura dopo una rotazione.
        responsive = re.search(
            r'@media\s*\(max-width:\s*700px\)\s*\{\s*\.grid\s*\{[^}]*\}\s*'
            r'\.grid\s+\.grid-col\s*\{([^}]*)\}', template)
        self.assertIsNotNone(responsive, 'manca la regola mobile per le colonne della griglia')
        self.assertRegex(responsive.group(1), r'\bwidth:\s*100%\s*;')

    def test_missing_and_duplicate_head_metadata_are_rejected(self):
        elements = [('<title>Citazione di prova</title>', 'title assente o multiplo'),
                    ('<meta name="description" content="Descrizione Citazione di prova">', 'meta description assente o multipla'),
                    ('<link rel="canonical" href="https://sottolineature.it/citazioni/prova/">', 'canonical assente o multiplo')]
        for element, message in elements:
            for replacement in ['', element + element]:
                with self.subTest(element=element, missing=not replacement):
                    self.write('citazioni/prova.html', self.quote.replace(element, replacement))
                    self.assert_rejected(message)

    def test_wrong_canonical_host_is_rejected(self):
        self.write('citazioni/prova.html', self.quote.replace(
            'href="https://sottolineature.it/citazioni/prova/"',
            'href="https://www.sottolineature.it/citazioni/prova/"'))
        self.assert_rejected('CANONICAL INCOERENTI')

    def test_duplicate_titles_and_descriptions_are_rejected(self):
        for before, after, message in [
            ('<title>Citazione di prova</title>', '<title>Home di prova</title>', 'TITLE DUPLICATI'),
            ('content="Descrizione Citazione di prova"', 'content="Descrizione Home di prova"', 'DESCRIPTION DUPLICATE')]:
            with self.subTest(message=message):
                self.write('citazioni/prova.html', self.quote.replace(before, after))
                self.assert_rejected(message)

    def test_semantic_main_and_single_h1_are_required(self):
        cases = [(self.quote.replace('<main>', '<div>').replace('</main>', '</div>'),
                  'numero di landmark main diverso da uno'),
                 (self.quote.replace('</main>', '</main><main></main>'), 'numero di landmark main diverso da uno'),
                 (self.quote.replace('<h1>Citazione di prova</h1>', ''), 'numero di H1 diverso da uno'),
                 (self.quote.replace('</main>', '<h1>Altro titolo</h1></main>'), 'numero di H1 diverso da uno')]
        for source, message in cases:
            with self.subTest(source=source):
                self.write('citazioni/prova.html', source)
                self.assert_rejected(message)

    def test_explicit_main_role_is_valid_and_not_double_counted(self):
        for opening, closing in [('<div role="main">', '</div>'),
                                 ('<main role="main">', '</main>')]:
            with self.subTest(opening=opening):
                self.write('citazioni/prova.html', self.quote.replace('<main>', opening).replace('</main>', closing))
                result, output = self.audit()
                self.assertEqual(result, 0, output)

    def test_mixed_duplicate_main_landmarks_are_rejected(self):
        self.write('citazioni/prova.html', self.quote.replace('</main>', '</main><div role="main"></div>'))
        self.assert_rejected('numero di landmark main diverso da uno')

    def test_skipped_heading_level_is_rejected(self):
        self.write('citazioni/prova.html', self.quote.replace('</main>', '<h3>Sezione</h3></main>'))
        self.assert_rejected('gerarchia heading con livello saltato')

    def test_expected_schema_and_visible_breadcrumb_are_required(self):
        for source, message in [
            (self.quote.replace('"Quotation"', '"Book"'), 'tipo JSON-LD atteso assente'),
            (self.quote.replace('class="breadcrumb"', 'class="altro"'), 'breadcrumb visibile atteso assente')]:
            with self.subTest(message=message):
                self.write('citazioni/prova.html', source)
                self.assert_rejected(message)

    def test_decorative_alt_is_valid_but_absent_alt_is_rejected(self):
        self.write('assets/prova.svg', '<svg xmlns="http://www.w3.org/2000/svg"/>')
        self.write('citazioni/prova.html', self.quote.replace('</main>', '<img src="/assets/prova.svg" alt=""></main>'))
        result, output = self.audit()
        self.assertEqual(result, 0, output)
        self.write('citazioni/prova.html', self.quote.replace('</main>', '<img src="/assets/prova.svg"></main>'))
        self.assert_rejected('immagine senza attributo alt')

    def test_broken_internal_link_is_rejected(self):
        self.write('citazioni/prova.html', self.quote.replace('</main>', '<a href="/inesistente/">Pagina</a></main>'))
        self.assert_rejected('LINK ROTTI')

    def test_noncanonical_internal_urls_are_rejected(self):
        for href in ['/citazioni/prova.html', '/citazioni/prova', '/index.html']:
            with self.subTest(href=href):
                self.write('index.html', self.home.replace('/citazioni/prova/', href))
                self.assert_rejected('URL INTERNI NON CANONICI')

    def test_orphan_page_is_rejected(self):
        self.write('index.html', self.home.replace('<a href="/citazioni/prova/">Citazione</a>', ''))
        self.assert_rejected('PAGINE ORFANE')

    def test_sitemap_must_include_every_indexable_page(self):
        self.sitemaps({'sitemap-pagine.xml': ['/']})
        self.assert_rejected('PAGINE INDICIZZABILI ASSENTI DALLA SITEMAP')

    def test_sitemap_rejects_missing_noindex_and_duplicate_urls(self):
        for routes, noindex, message in [
            (['/', '/citazioni/inesistente/'], set(), 'URL inesistente'),
            (['/', '/citazioni/prova/'], {'/citazioni/prova/'}, 'URL con noindex'),
            (['/', '/citazioni/prova/', '/citazioni/prova/'], set(), 'URL duplicato')]:
            with self.subTest(message=message):
                self.sitemaps({'sitemap-pagine.xml': routes})
                errors = checker.validate_sitemaps(noindex)['errors']
                self.assertTrue(any(message in detail for _, detail in errors), errors)

    def test_sitemap_rejects_unclean_urls_and_wrong_host(self):
        for url, message in [
            ('https://www.sottolineature.it/citazioni/prova/', 'host non canonico'),
            (checker.SITE_URL + '/citazioni/prova.html', 'URL senza slash finale'),
            (checker.SITE_URL + '/citazioni/prova/?q=prova', 'query o frammento'),
            (checker.SITE_URL + '/citazioni/prova/#frase', 'query o frammento')]:
            with self.subTest(url=url):
                self.write('sitemap-pagine.xml', f'<urlset xmlns="{checker.SITEMAP_NS}"><url><loc>{escape(url)}</loc></url></urlset>')
                errors = checker.validate_sitemaps(set())['errors']
                self.assertTrue(any(message in detail for _, detail in errors), errors)

    def test_sitemap_rejects_duplicate_children_and_urls_across_children(self):
        self.sitemaps({'sitemap-a.xml': ['/', '/citazioni/prova/'], 'sitemap-b.xml': ['/citazioni/prova/']})
        self.assert_rejected('URL duplicato anche in')
        index = (self.root / 'sitemap.xml').read_text()
        self.write('sitemap.xml', index.replace('sitemap-b.xml', 'sitemap-a.xml'))
        self.assert_rejected('sitemap figlia duplicata')

    def test_malformed_sitemap_index_and_child_are_rejected(self):
        for name in ['sitemap.xml', 'sitemap-pagine.xml']:
            with self.subTest(name=name):
                self.sitemaps({'sitemap-pagine.xml': ['/', '/citazioni/prova/']})
                self.write(name, '<xml')
                self.assert_rejected('XML non valido')

    def test_private_and_error_pages_stay_out_of_sitemap(self):
        self.write('404.html', self.page('/404/', 'Errore di prova', 'WebPage', noindex=True))
        self.write('le-mie-sottolineature.html', self.page('/le-mie-sottolineature/', 'Selezione privata', [], noindex=True))
        result, output = self.audit()
        self.assertEqual(result, 0, output)

    def test_inline_script_strings_are_not_treated_as_real_links(self):
        self.write('citazioni/prova.html', self.quote.replace('</main>',
            '<script>var esempio = \'<a href="/inesistente/">test</a><h1>test</h1>\';</script></main>'))
        result, output = self.audit()
        self.assertEqual(result, 0, output)

    def sitemap_image(self, locations):
        markup = ''.join('<image:image>' + ('' if url is None else
                         '<image:loc>' + escape(url) + '</image:loc>') +
                         '</image:image>' for url in locations)
        path = self.root / 'sitemap-pagine.xml'
        self.write('sitemap-pagine.xml', path.read_text().replace(
            '<urlset ', '<urlset xmlns:image="http://www.google.com/schemas/sitemap-image/1.1" ').replace(
            '<loc>https://sottolineature.it/citazioni/prova/</loc>',
            '<loc>https://sottolineature.it/citazioni/prova/</loc>' + markup))

    def image_page(self, src):
        self.write('assets/prova.svg', '<svg xmlns="http://www.w3.org/2000/svg"/>')
        self.write('citazioni/prova.html', self.quote.replace(
            '</main>', '<img src="' + escape(src, {'"': '&quot;'}) + '" alt="Grafica di prova"></main>'))

    def test_sitemap_image_with_cache_query_and_xml_escaping_passes(self):
        src = '/assets/prova.svg?v=abc123&tema=chiaro'
        self.image_page(src)
        self.sitemap_image([checker.SITE_URL + src])
        result, output = self.audit()
        self.assertEqual(result, 0, output)
        self.assertIn('1 immagini dichiarate', output)

    def test_sitemap_missing_image_file_is_rejected(self):
        self.sitemap_image([checker.SITE_URL + '/assets/mancante.png'])
        self.assert_rejected('file immagine inesistente')

    def test_sitemap_empty_image_loc_is_rejected(self):
        self.sitemap_image([None])
        self.assert_rejected('immagine senza <image:loc>')

    def test_sitemap_image_wrong_host_and_fragment_are_rejected(self):
        self.image_page('/assets/prova.svg')
        for url, message in [
                ('https://www.sottolineature.it/assets/prova.svg', 'immagine con host non canonico'),
                ('http://sottolineature.it/assets/prova.svg', 'immagine con host non canonico'),
                (checker.SITE_URL + '/assets/prova.svg#tema', 'immagine con frammento')]:
            with self.subTest(url=url):
                self.sitemaps({'sitemap-pagine.xml': ['/', '/citazioni/prova/']})
                self.sitemap_image([url])
                self.assert_rejected(message)

    def test_sitemap_image_path_traversal_is_rejected_without_reading_external_files(self):
        for path in ['/../prova.svg', '/%2e%2e/prova.svg']:
            with self.subTest(path=path):
                self.sitemaps({'sitemap-pagine.xml': ['/', '/citazioni/prova/']})
                self.sitemap_image([checker.SITE_URL + path])
                self.assert_rejected('percorso immagine fuori dal progetto')

    def test_sitemap_image_must_be_embedded_in_its_page(self):
        self.image_page('/assets/prova.svg')
        self.write('citazioni/prova.html', self.quote)
        self.sitemap_image([checker.SITE_URL + '/assets/prova.svg'])
        self.assert_rejected('immagine non presente nella pagina')

    def test_script_string_is_not_a_sitemap_image(self):
        self.image_page('/assets/prova.svg')
        self.write('citazioni/prova.html', self.quote.replace('</main>',
                   '<script>var figura = \'<img src="/assets/prova.svg" alt="">\';</script></main>'))
        self.sitemap_image([checker.SITE_URL + '/assets/prova.svg'])
        self.assert_rejected('immagine non presente nella pagina')

    def test_same_image_can_be_declared_on_two_pages(self):
        self.image_page('/assets/prova.svg')
        self.write('index.html', self.home.replace('</main>', '<img src="/assets/prova.svg" alt=""></main>'))
        self.sitemap_image([checker.SITE_URL + '/assets/prova.svg'])
        path = self.root / 'sitemap-pagine.xml'
        self.write('sitemap-pagine.xml', path.read_text().replace('<loc>https://sottolineature.it/</loc>',
            '<loc>https://sottolineature.it/</loc><image:image><image:loc>' + checker.SITE_URL +
            '/assets/prova.svg</image:loc></image:image>'))
        result, output = self.audit()
        self.assertEqual(result, 0, output)
        self.assertIn('2 immagini dichiarate', output)


if __name__ == '__main__':
    unittest.main()
