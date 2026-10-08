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

    def test_real_config_is_small_verified_prime_pilot(self):
        editions = affiliate.validated_editions(self.config)
        self.assertEqual(affiliate.load_tracking_id(self.config), 'sottolineature-21')
        self.assertEqual(len(editions), 5)
        self.assertTrue(all(item['amazon_edition_verified'] is True for item in editions.values()))
        self.assertTrue(all(item['prime_verified'] is True for item in editions.values()))

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
        self.assertIn('(link affiliato)', rendered)
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
            {'author': 'Harper Lee', 'title': 'Il buio oltre la siepe'}, self.config
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

    def test_sixth_active_work_is_rejected(self):
        config = dict(self.config)
        config['edizioni'] = list(self.config['edizioni']) + [dict(self.config['edizioni'][0])]
        with self.assertRaises(ValueError):
            affiliate.validated_editions(config)

    def test_collection_never_recommends_a_work_absent_from_its_quotes(self):
        unrelated = {'author': 'Harper Lee', 'title': 'Il buio oltre la siepe'}
        self.assertIsNone(affiliate.collection_edition_record([('lee', unrelated)], self.config))
        selected = {'author': 'George Orwell', 'title': '1984'}
        self.assertEqual(affiliate.collection_edition_record(
            [('lee', unrelated), ('orwell', selected)], self.config
        ), selected)


if __name__ == '__main__':
    unittest.main()
