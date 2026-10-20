"""Synthetic fixtures only; no GitHub comments, approvals or network writes."""
import copy
import json
from pathlib import Path
import shutil
import tempfile
import unittest

import ci_safety as ci
import protection_gate as g
import test_protection_gate as fixtures


class CiSafetyTests(unittest.TestCase):
    def setUp(self):
        self.f = fixtures.ProtectionGateTests()
        self.f.setUp()
        self.addCleanup(self.f.doCleanups)
        self.temp = tempfile.TemporaryDirectory(prefix='seo-safety-TEST-before-')
        self.addCleanup(self.temp.cleanup)
        self.before = Path(self.temp.name) / 'before'
        shutil.copytree(self.f.root, self.before)
        self.base, self.head = 'a' * 40, 'b' * 40

    def evaluate(self, comments=()):
        return ci.evaluate(g, self.before, self.f.root, self.base, self.head, comments)

    def manifest(self):
        _, files = ci.scope(g, self.before, self.f.root)
        self.f.write(ci.MANIFEST, self.f.raw({'version': 1, 'base': self.base,
                     'reason': 'TEST exact scope, not owner approval', 'files': files}))

    def comment(self, impact, **changes):
        value = {'id': 1, 'html_url': 'https://example.invalid/TEST-comment',
                 'user': {'login': 'giantroisi', 'type': 'User'}, 'author_association': 'OWNER',
                 'body': '/seo-override ' + self.head + ' ' + impact + ' TEST fixture only, not a human approval'}
        value.update(changes)
        return value

    def test_positive_technical_document_only(self):
        self.f.write('LOG.md', b'TEST progress')
        self.assertTrue(self.evaluate()['allowed'])

    def test_positive_exact_small_content_change(self):
        self.f.write('citazioni/uno.html', self.f.page('uno', 'Contesto migliorato TEST'))
        self.manifest()
        result = self.evaluate()
        self.assertTrue(result['allowed'], result)

    def test_page_without_manifest_blocked(self):
        self.f.write('citazioni/uno.html', self.f.page('uno', 'Contesto migliorato TEST'))
        self.assertFalse(self.evaluate()['allowed'])

    def test_extra_page_not_declared_blocked(self):
        self.f.write('citazioni/uno.html', self.f.page('uno', 'Contesto migliorato TEST'))
        self.manifest()
        self.f.write('citazioni/due.html', self.f.page('due', 'TEST collateral page'))
        result = self.evaluate()
        self.assertFalse(result['allowed'])
        self.assertTrue(any('extra or missing' in error for error in result['hard_errors']))

    def test_published_date_never_overridden(self):
        self.f.write('citazioni/uno.html', self.f.page('uno', published='2026-10-20'))
        self.manifest()
        result = self.evaluate()
        result = self.evaluate([self.comment(result['impact_sha256'])])
        self.assertFalse(result['allowed'])
        self.assertTrue(any('datePublished' in error for error in result['hard_errors']))

    def test_date_only_change_blocked(self):
        self.f.write('citazioni/uno.html', self.f.page('uno', modified='2026-10-20'))
        self.manifest()
        self.assertFalse(self.evaluate()['allowed'])

    def test_real_modified_content_allowed_exactly(self):
        self.f.write('citazioni/uno.html', self.f.page('uno', 'Contesto migliorato TEST', modified='2026-10-20'))
        self.manifest()
        self.assertTrue(self.evaluate()['allowed'])

    def test_lastmod_without_content_blocked(self):
        self.f.write('sitemap-citazioni.xml', self.f.sitemap(date='2026-10-20'))
        self.manifest()
        self.assertFalse(self.evaluate()['allowed'])

    def test_canonical_changed_blocked(self):
        self.f.write('citazioni/uno.html', self.f.page('uno', url='https://example.invalid/other/'))
        self.manifest()
        self.assertFalse(self.evaluate()['allowed'])

    def test_robots_changed_requires_exact_owner_exception(self):
        self.f.write('robots.txt', b'User-agent: *\nDisallow: /TEST-only/\n')
        result = self.evaluate()
        self.assertFalse(result['allowed'])
        result = self.evaluate([self.comment(result['impact_sha256'])])
        self.assertTrue(result['allowed'])
        self.assertEqual(result['owner_override']['comment_id'], 1)

    def test_wrong_owner_cannot_override(self):
        comment = self.comment('c' * 64, user={'login': 'another', 'type': 'User'})
        self.assertIsNone(ci.owner_override([comment], self.head, 'c' * 64))

    def test_bot_cannot_override(self):
        comment = self.comment('c' * 64, user={'login': 'giantroisi', 'type': 'Bot'})
        self.assertIsNone(ci.owner_override([comment], self.head, 'c' * 64))

    def test_stale_sha_cannot_override(self):
        self.assertIsNone(ci.owner_override([self.comment('c' * 64)], 'd' * 40, 'c' * 64))

    def test_wrong_impact_cannot_override(self):
        self.assertIsNone(ci.owner_override([self.comment('c' * 64)], self.head, 'd' * 64))

    def test_paginated_comments_supported(self):
        self.assertIsNotNone(ci.owner_override([[self.comment('c' * 64)]], self.head, 'c' * 64))

    def test_file_budget_blocks_mass_changes(self):
        for index in range(26):
            self.f.write('notes-' + str(index) + '.md', b'TEST only')
        self.assertFalse(self.evaluate()['allowed'])

    def test_shared_code_requires_owner_exception(self):
        self.f.write('tools/generate_quote_pages.py', b'# TEST changed shared code\n')
        self.assertFalse(self.evaluate()['allowed'])

    def test_added_date_immutable(self):
        data = copy.deepcopy(self.f.quotes)
        data[0]['added'] = '2026-10-20'
        self.f.write('data/citazioni.json', self.f.raw(data))
        self.assertFalse(self.evaluate()['allowed'])

    def test_published_slug_immutable(self):
        path = self.f.root / 'tools/slugs.json'
        data = json.loads(path.read_bytes())
        data['quotes']['Autore|Opera|Una frase uno'] = 'different-slug'
        self.f.write('tools/slugs.json', self.f.raw(data))
        self.assertFalse(self.evaluate()['allowed'])

    def test_bootstrap_exact_technical_scope_only(self):
        self.base = ci.BOOTSTRAP_BASE
        self.f.write('tools/ci_safety.py', b'# TEST initial install')
        self.assertTrue(self.evaluate()['bootstrap_technical_only'])
        self.f.write('robots.txt', b'TEST unapproved root change')
        result = self.evaluate()
        self.assertFalse(result['bootstrap_technical_only'])
        self.assertFalse(result['allowed'])


if __name__ == '__main__':
    unittest.main()
