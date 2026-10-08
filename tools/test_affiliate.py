#!/usr/bin/env python3
"""Regressioni del componente Amazon: attivazione selettiva e URL puliti."""
import json
import os
import sys
import unittest


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
        self.assertEqual(len(editions), 74)
        self.assertTrue(all(item['amazon_edition_verified'] is True for item in editions.values()))
        exceptions = [item for item in editions.values() if not item['prime_verified']]
        self.assertEqual([item['author'] for item in exceptions], ['Primo Levi', 'Amin Maalouf'])
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

    def test_blank_tracking_id_disables_every_link(self):
        config = {'amazon_it_tracking_id': '', 'edizioni': self.config['edizioni']}
        record = {'author': 'George Orwell', 'title': '1984'}
        self.assertEqual(affiliate.render_amazon_link(record, config), '')

    def test_button_is_accessible_and_contains_no_amazon_asset_or_price(self):
        record = {'author': 'George Orwell', 'title': '1984'}
        rendered = affiliate.render_amazon_link(record, self.config)
        self.assertIn('<span>Acquista su Amazon</span>', rendered)
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
        additions = self.config['edizioni'][5:]
        self.assertEqual(len(additions), 69)
        self.assertTrue(all(item['link_checker_verified_on'] == '2026-10-08'
                            for item in additions))

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

    def test_poe_poem_and_detective_story_have_distinct_editions(self):
        poem = affiliate.edition_for_record(
            {'author': 'Edgar Allan Poe', 'title': 'Il corvo'}, self.config)
        story = affiliate.edition_for_record(
            {'author': 'Edgar Allan Poe', 'title': 'I delitti della Rue Morgue'}, self.config)
        self.assertEqual(poem['asin'], '8807901323')
        self.assertEqual(story['asin'], '8811605210')


if __name__ == '__main__':
    unittest.main()
