#!/usr/bin/env python3
"""Regressioni del componente Amazon: attivazione selettiva e URL puliti."""
import json
import os
import sys
import unittest
import re
from pathlib import Path


TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(TOOLS_DIR)
sys.path.insert(0, TOOLS_DIR)

import affiliate  # noqa: E402


class AffiliateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = affiliate.load_config()
        with open(os.path.join(ROOT, 'data', 'citazioni.json'), encoding='utf-8') as source:
            cls.quotes = json.load(source)

    def test_real_config_contains_only_approved_verified_prime_editions(self):
        editions = affiliate.validated_editions(self.config)
        self.assertEqual(affiliate.load_tracking_id(self.config), 'sottolineature-21')
        self.assertEqual(len(editions), 135)
        self.assertTrue(all(item['amazon_edition_verified'] is True for item in editions.values()))
        exceptions = [item for item in editions.values() if not item['prime_verified']]
        self.assertEqual([item['author'] for item in exceptions],
                         ['Primo Levi', 'Amin Maalouf', 'Salman Rushdie', 'Astrid Lindgren'])
        self.assertTrue(all(item['prime_exception_reason'] for item in exceptions))

    def test_every_selected_work_has_citations_and_inherits_one_url(self):
        editions = affiliate.validated_editions(self.config)
        counts = {key: 0 for key in editions}
        for quote in self.quotes:
            key = (quote['author'], quote['title'])
            if key in editions:
                counts[key] += 1
                rendered = affiliate.render_amazon_link(quote, self.config)
                self.assertEqual(rendered.count('class="affiliate-link"'), 1)
                self.assertIn(editions[key]['amazon_url'], rendered)
        self.assertTrue(all(count > 0 for count in counts.values()))

    def test_owner_selected_october_20_editions_and_all_their_quotes(self):
        expected = {
            ('Oscar Wilde', 'Il ritratto di Dorian Gray'): ('8804710217', 6),
            ('Haruki Murakami', 'Norwegian Wood'): ('8806216465', 1),
        }
        editions = affiliate.validated_editions(self.config)
        for key, (asin, count) in expected.items():
            edition = editions[key]
            self.assertEqual(edition['amazon_url'],
                             f'https://www.amazon.it/dp/{asin}/?tag=sottolineature-21')
            self.assertEqual(edition['link_checker_verified_on'], '2026-10-20')
            quotes = [q for q in self.quotes if (q['author'], q['title']) == key]
            self.assertEqual(len(quotes), count)
            for quote in quotes:
                self.assertIn(edition['amazon_url'], affiliate.render_amazon_link(quote, self.config))
        wilde = editions[('Oscar Wilde', 'Il ritratto di Dorian Gray')]
        self.assertEqual(wilde['contributors'], [
            {'name': 'Oscar Wilde', 'role': 'Autore'},
            {'name': 'Nicholas Frankel', 'role': 'Curatore'},
            {'name': 'Michele Piumini', 'role': 'Traduttore'},
        ])

    def test_blank_tracking_id_disables_every_link(self):
        config = {'amazon_it_tracking_id': '', 'edizioni': self.config['edizioni']}
        record = {'author': 'George Orwell', 'title': '1984'}
        self.assertEqual(affiliate.render_amazon_link(record, config), '')

    def test_button_is_accessible_and_contains_no_amazon_asset_or_price(self):
        record = {'author': 'George Orwell', 'title': '1984'}
        rendered = affiliate.render_amazon_link(record, self.config)
        self.assertIn('<span>Acquista su Amazon</span>', rendered)
        self.assertNotIn('affiliate-button-disclosure', rendered)
        self.assertNotIn('link affiliato', rendered)
        self.assertIn('rel="sponsored nofollow noopener"', rendered)
        self.assertNotIn('(link affiliato)', rendered)
        self.assertNotIn('potremmo ricevere una commissione', rendered)
        self.assertIn('1984', rendered)
        self.assertIn('Nicola Gardini (Traduttore)', rendered)
        self.assertIn('Formato: Copertina flessibile', rendered)
        self.assertIn('<svg class="affiliate-cart"', rendered)
        self.assertNotIn('<img', rendered)
        self.assertNotIn('Prime', rendered)
        self.assertNotRegex(rendered, r'\d+[,.]\d{2}\s*€')

    def test_unselected_work_has_no_link(self):
        self.assertEqual(affiliate.render_amazon_link(
            {'author': 'Albert Camus', 'title': 'Lo straniero'}, self.config
        ), '')

    def test_all_selected_editions_have_only_cta_and_preserve_link_attributes(self):
        for edition in self.config['edizioni']:
            with self.subTest(author=edition['author'], title=edition['title']):
                rendered = affiliate.render_amazon_button(edition, self.config)
                self.assertEqual(rendered.count('<span>Acquista su Amazon</span>'), 1)
                self.assertNotIn('affiliate-button-text', rendered)
                self.assertNotIn('link affiliato', rendered)
                self.assertIn('href="' + edition['amazon_url'] + '"', rendered)
                self.assertIn('target="_blank" rel="sponsored nofollow noopener"', rendered)

    def test_generated_buttons_have_only_cta_and_one_footer_disclosure_per_page(self):
        button_count = 0
        for path in Path(ROOT).rglob('*.html'):
            if 'templates' in path.parts or any(part.startswith('.') for part in path.relative_to(ROOT).parts):
                continue
            source = path.read_text(encoding='utf-8')
            anchors = re.findall(r'<a\b[^>]*>.*?</a>', source, re.DOTALL)
            for anchor in anchors:
                if 'class="affiliate-link"' in anchor:
                    button_count += 1
                    self.assertEqual(anchor.count('<span>Acquista su Amazon</span>'), 1, str(path))
                    self.assertNotIn('link affiliato', anchor, str(path))
            self.assertNotIn('affiliate-button-disclosure', source, str(path))
            self.assertNotIn('affiliate-button-text', source, str(path))
            disclosure = 'In qualità di Affiliato Amazon io ricevo un guadagno dagli acquisti idonei.'
            self.assertEqual(source.count(disclosure), 1, str(path))
            self.assertEqual(source.count('class="affiliate-disclosure"'), 1, str(path))
            footer = re.search(r'<footer\b.*?</footer>', source, re.DOTALL)
            self.assertIsNotNone(footer, str(path))
            self.assertIn(disclosure, footer.group(), str(path))
        self.assertGreater(button_count, 0)

    def test_url_rejects_extra_query_and_asin_mismatch(self):
        with self.assertRaises(ValueError):
            affiliate._verified_amazon_url(
                'https://www.amazon.it/dp/8804796650/?tag=sottolineature-21&ref=x',
                'sottolineature-21', '8804796650'
            )
        with self.assertRaises(ValueError):
            affiliate._verified_amazon_url(
                'https://www.amazon.it/dp/8804796650/?tag=sottolineature-21',
                'sottolineature-21', '880625829X'
            )

    def test_work_beyond_approved_limit_is_rejected(self):
        config = dict(self.config)
        config['edizioni'] = list(self.config['edizioni']) + [dict(self.config['edizioni'][0])]
        with self.assertRaisesRegex(ValueError, 'lotto approvato'):
            affiliate.validated_editions(config)

    def test_inferno_work_alias_inherits_verified_cantica_not_another_volume(self):
        record = {'author': 'Dante Alighieri', 'title': 'Inferno',
                  'titles': ['Inferno, Divina Commedia']}
        edition = affiliate.edition_for_record(record, self.config)
        self.assertEqual(edition['asin'], '8804671653')
        self.assertIn('Inferno', edition['amazon_title'])

    def test_new_editions_were_checked_with_official_amazon_tool(self):
        additions = self.config['edizioni'][5:119]
        self.assertEqual(len(additions), 114)
        self.assertTrue(all(item['link_checker_verified_on'] == '2026-10-08'
                            for item in additions))

    def test_october_12_batch_adds_exactly_twenty_quote_pages(self):
        additions = self.config['edizioni'][119:123]
        expected = {
            ('Charlotte Brontë', 'Jane Eyre'): ('8807900777', 6),
            ('Luigi Pirandello', 'Il fu Mattia Pascal'): ('8807900386', 6),
            ('Anne Frank', 'Diario'): ('8806219286', 4),
            ('Walt Whitman', "Foglie d'erba"): ('880623000X', 4),
        }
        self.assertEqual(len(additions), 4)
        previous = dict(self.config, edizioni=self.config['edizioni'][:119])
        added_pages = []
        for edition in additions:
            key = (edition['author'], edition['title'])
            self.assertIn(key, expected)
            asin, count = expected[key]
            self.assertEqual(edition['asin'], asin)
            self.assertTrue(edition['prime_verified'])
            self.assertEqual(edition['format'], 'Copertina flessibile')
            self.assertEqual(edition['verified_on'], '2026-10-12')
            self.assertEqual(edition['link_checker_verified_on'], '2026-10-12')
            quotes = [quote for quote in self.quotes
                      if (quote['author'], quote['title']) == key]
            self.assertEqual(len(quotes), count)
            for quote in quotes:
                self.assertEqual(affiliate.render_amazon_link(quote, previous), '')
                self.assertIn(edition['amazon_url'],
                              affiliate.render_amazon_link(quote, self.config))
                added_pages.append(quote)
        self.assertEqual(len(added_pages), 20)

    def test_whitman_purchase_volume_includes_poems_after_1856(self):
        edition = affiliate.edition_for_record(
            {'author': 'Walt Whitman', 'title': "Foglie d'erba"}, self.config)
        self.assertEqual(edition['asin'], '880623000X')
        self.assertIn('versione del 1892', edition['edition_note'])
        self.assertNotIn('8854168106', edition['amazon_url'])
        self.assertNotIn('8804671416', edition['amazon_url'])

    def test_october_12_second_batch_adds_twenty_previously_unselected_quotes(self):
        additions = self.config['edizioni'][123:128]
        expected = {
            ('Ludovico Ariosto', 'Orlando furioso'): ('8817070513', 6),
            ('Khalil Gibran', 'Il Profeta'): ('8807882701', 5),
            ('Ernest Hemingway', 'Il vecchio e il mare'): ('8804734450', 3),
            ('J.D. Salinger', 'Il giovane Holden'): ('8806218182', 3),
            ('Milan Kundera', "L'insostenibile leggerezza dell'essere"): ('8845906868', 3),
        }
        self.assertEqual(len(additions), 5)
        previous = dict(self.config, edizioni=self.config['edizioni'][:123])
        added = []
        for edition in additions:
            key = (edition['author'], edition['title'])
            self.assertIn(key, expected)
            asin, count = expected[key]
            self.assertEqual(edition['asin'], asin)
            self.assertTrue(edition['amazon_edition_verified'])
            self.assertTrue(edition['prime_verified'])
            self.assertEqual(edition['format'], 'Copertina flessibile')
            self.assertEqual(edition['verified_on'], '2026-10-12')
            self.assertEqual(edition['link_checker_verified_on'], '2026-10-12')
            quotes = [q for q in self.quotes if (q['author'], q['title']) == key]
            self.assertEqual(len(quotes), count)
            for quote in quotes:
                self.assertEqual(affiliate.render_amazon_button(quote, previous), '')
                self.assertIn(edition['amazon_url'], affiliate.render_amazon_button(quote, self.config))
            added.extend(quotes)
        self.assertEqual(len(added), 20)

    def test_october_12_third_batch_adds_twenty_previously_unselected_quotes(self):
        additions = self.config['edizioni'][128:134]
        expected = {
            ('Marco Aurelio', 'Colloqui con sé stesso'): ('8844072629', 4),
            ("Sant'Agostino", 'Confessioni'): ('8806225650', 4),
            ('Giovanni Boccaccio', 'Decameron'): ('8817063266', 3),
            ('Seneca', 'Lettere a Lucilio'): ('886311532X', 3),
            ('Charles Baudelaire', 'I fiori del male'): ('8806221906', 3),
            ('Madeline Miller', 'Circe'): ('8829705322', 3),
        }
        self.assertEqual(len(additions), len(expected))
        previous = dict(self.config, edizioni=self.config['edizioni'][:128])
        added = []
        for edition in additions:
            key = (edition['author'], edition['title'])
            self.assertIn(key, expected)
            asin, count = expected[key]
            self.assertEqual(edition['asin'], asin)
            self.assertTrue(edition['amazon_edition_verified'])
            self.assertTrue(edition['prime_verified'])
            self.assertEqual(edition['format'], 'Copertina flessibile')
            self.assertEqual(edition['verified_on'], '2026-10-12')
            self.assertEqual(edition['link_checker_verified_on'], '2026-10-12')
            quotes = [q for q in self.quotes if (q['author'], q['title']) == key]
            self.assertEqual(len(quotes), count)
            for quote in quotes:
                self.assertEqual(affiliate.render_amazon_link(quote, previous), '')
                self.assertIn(edition['amazon_url'], affiliate.render_amazon_link(quote, self.config))
            added.extend(quotes)
        self.assertEqual(len(added), 20)

    def test_third_batch_purchase_translators_do_not_overwrite_quote_sources(self):
        editions = affiliate.validated_editions(self.config)
        self.assertIn('Luca Civitavecchia', str(editions[('Marco Aurelio', 'Colloqui con sé stesso')]['contributors']))
        self.assertIn('Giovanni Raboni', str(editions[('Charles Baudelaire', 'I fiori del male')]['contributors']))
        translators = {q.get('source_translator') for q in self.quotes
                       if (q['author'], q['title']) == ('Charles Baudelaire', 'I fiori del male')}
        self.assertEqual(translators, {'Attilio Bertolucci', 'Claudio Rendina'})

    def test_kundera_translator_credit_follows_publisher_without_duplicate_names(self):
        edition = affiliate.edition_for_record(
            {'author': 'Milan Kundera', 'title': "L'insostenibile leggerezza dell'essere"}, self.config)
        self.assertEqual(edition['contributors'], [
            {'name': 'Milan Kundera', 'role': 'Autore'},
            {'name': 'Giuseppe Dierna', 'role': 'Traduttore'},
        ])
        self.assertEqual(edition['bibliographic_source_url'], 'https://www.adelphi.it/libro/9788845906862')

    def test_collection_never_recommends_a_work_absent_from_its_quotes(self):
        unrelated = {'author': 'Albert Camus', 'title': 'Lo straniero'}
        self.assertIsNone(affiliate.collection_edition_record([('lee', unrelated)], self.config))
        selected = {'author': 'George Orwell', 'title': '1984'}
        self.assertEqual(affiliate.collection_edition_record(
            [('lee', unrelated), ('orwell', selected)], self.config
        ), selected)

    def test_1q84_link_uses_complete_three_book_edition(self):
        edition = affiliate.edition_for_record(
            {'author': 'Haruki Murakami', 'title': '1Q84'}, self.config)
        self.assertEqual(edition['asin'], '8806222902')
        self.assertIn('Libri 1 2 e 3', edition['amazon_title'])
        self.assertNotIn('8806226223', edition['amazon_url'])

    def test_remarque_contributors_are_distinct_people_and_roles(self):
        edition = affiliate.edition_for_record(
            {'author': 'Erich Maria Remarque',
             'title': 'Niente di nuovo sul fronte occidentale'}, self.config)
        self.assertIn({'name': 'Stefano Jacini', 'role': 'Traduttore'},
                      edition['contributors'])
        self.assertIn({'name': 'Wolfgango Della Croce', 'role': 'Curatore'},
                      edition['contributors'])

    def test_proust_edition_includes_all_seven_novels(self):
        edition = affiliate.edition_for_record(
            {'author': 'Marcel Proust', 'title': 'Alla ricerca del tempo perduto'}, self.config)
        self.assertEqual(edition['asin'], '8806234897')
        self.assertIn('sette romanzi', edition['edition_note'])
        self.assertTrue(edition['bibliographic_source_url'].startswith('https://www.einaudi.it/'))

    def test_alcott_edition_includes_second_part_quoted_in_archive(self):
        edition = affiliate.edition_for_record(
            {'author': 'Louisa May Alcott', 'title': 'Piccole donne'}, self.config)
        self.assertEqual(edition['asin'], '8831002473')
        self.assertIn('Piccole donne crescono', edition['amazon_title'])

    def test_invisible_man_is_ellison_not_wells(self):
        edition = affiliate.edition_for_record(
            {'author': 'Ralph Ellison', 'title': 'Uomo invisibile'}, self.config)
        self.assertEqual(edition['asin'], '8860447070')
        self.assertIsNone(affiliate.edition_for_record(
            {'author': 'H.G. Wells', 'title': "L'uomo invisibile"}, self.config))

    def test_martin_edition_is_complete_first_novel_not_another_volume(self):
        edition = affiliate.edition_for_record(
            {'author': 'George R.R. Martin', 'title': 'Il Trono di Spade'}, self.config)
        self.assertEqual(edition['asin'], '8804750782')
        self.assertIn('Un gioco di troni (Libro 1)', edition['amazon_title'])
        self.assertIn('romanzo completo', edition['edition_note'])

    def test_ende_edition_uses_verified_italian_variant(self):
        edition = affiliate.edition_for_record(
            {'author': 'Michael Ende', 'title': 'La storia infinita'}, self.config)
        self.assertEqual(edition['asin'], '8850273983')
        self.assertNotIn('8830451517', edition['amazon_url'])

    def test_foundation_edition_includes_first_novel(self):
        edition = affiliate.edition_for_record(
            {'author': 'Isaac Asimov', 'title': 'Fondazione'}, self.config)
        self.assertEqual(edition['asin'], '8804729198')
        self.assertIn('ciclo completo', edition['amazon_title'])
        self.assertNotIn('8804730390', edition['amazon_url'])

    def test_potter_translation_revision_is_not_a_translator_credit(self):
        edition = affiliate.edition_for_record(
            {'author': 'J.K. Rowling', 'title': 'Harry Potter e la Pietra Filosofale'},
            self.config)
        self.assertEqual(edition['asin'], '8831017322')
        self.assertIn({'name': 'Stefano Bartezzaghi', 'role': 'Revisione della traduzione'},
                      edition['contributors'])
        self.assertNotIn({'name': 'Stefano Bartezzaghi', 'role': 'Traduttore'},
                         edition['contributors'])
        self.assertTrue(edition['bibliographic_source_url'].startswith('https://www.salani.it/'))

    def test_carroll_novels_have_distinct_correct_editions(self):
        first = affiliate.edition_for_record(
            {'author': 'Lewis Carroll', 'title': 'Alice nel paese delle meraviglie'}, self.config)
        second = affiliate.edition_for_record(
            {'author': 'Lewis Carroll', 'title': 'Attraverso lo specchio'}, self.config)
        self.assertEqual(first['asin'], '885801393X')
        self.assertEqual(second['asin'], 'B0CWFCC7L6')

    def test_sartre_title_maps_to_verified_porta_chiusa(self):
        edition = affiliate.edition_for_record(
            {'author': 'Jean-Paul Sartre', 'title': 'A porte chiuse'}, self.config)
        self.assertEqual(edition['asin'], '884527523X')
        self.assertIn('Porta chiusa', edition['amazon_title'])

    def test_unverified_herbert_has_no_purchase_link(self):
        self.assertEqual(affiliate.render_amazon_link(
            {'author': 'Zbigniew Herbert', 'title': 'Un barbaro nel giardino'}, self.config), '')

    def test_bolano_edition_contains_both_parts_quoted_in_archive(self):
        edition = affiliate.edition_for_record(
            {'author': 'Roberto Bolaño', 'title': '2666'}, self.config)
        self.assertEqual(edition['asin'], '8845924351')
        self.assertIn('tutte le cinque parti', edition['edition_note'])
        self.assertIn('La parte dei critici', edition['edition_note'])
        self.assertIn('La parte di Arcimboldi', edition['edition_note'])

    def test_merini_volume_includes_requested_collection(self):
        edition = affiliate.edition_for_record(
            {'author': 'Alda Merini', 'title': 'La Terra Santa'}, self.config)
        self.assertEqual(edition['asin'], '8804787074')
        self.assertEqual(edition['amazon_title'], 'Testamento seguito da La Terra Santa')
        self.assertIn('comprende La Terra Santa', edition['edition_note'])

    def test_poe_poem_and_detective_story_have_distinct_editions(self):
        poem = affiliate.edition_for_record(
            {'author': 'Edgar Allan Poe', 'title': 'Il corvo'}, self.config)
        story = affiliate.edition_for_record(
            {'author': 'Edgar Allan Poe', 'title': 'I delitti della Rue Morgue'}, self.config)
        self.assertEqual(poem['asin'], '8807901323')
        self.assertEqual(story['asin'], '8811605210')


if __name__ == '__main__':
    unittest.main()
