"""Pure tests, no URLs submitted or external calls made."""
import copy
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import indexnow_production as indexnow


class IndexNowProductionTests(unittest.TestCase):
    def setUp(self):
        self.sha = 'a' * 40
        self.pulls = [{'merged_at': 'TEST', 'merge_commit_sha': self.sha, 'base': {'ref': 'main'}}]
        self.deployments = [{'id': 1, 'sha': self.sha, 'environment': 'Production',
                             'production_environment': False, 'creator': {'login': 'vercel[bot]'}}]
        self.statuses = {'1': [{'state': 'success', 'environment': 'Production', 'creator': {'login': 'vercel[bot]'}}]}

    def test_real_vercel_production_shape_supported(self):
        indexnow.production_ok(self.sha, self.sha, self.pulls, self.deployments, self.statuses)

    def test_preview_never_qualifies(self):
        self.deployments[0]['environment'] = 'Preview'
        self.deployments[0]['production_environment'] = True
        with self.assertRaises(ValueError):
            indexnow.production_ok(self.sha, self.sha, self.pulls, self.deployments, self.statuses)

    def test_failed_deployment_blocked(self):
        self.statuses['1'][0]['state'] = 'failure'
        with self.assertRaises(ValueError):
            indexnow.production_ok(self.sha, self.sha, self.pulls, self.deployments, self.statuses)

    def test_non_main_sha_blocked(self):
        with self.assertRaises(ValueError):
            indexnow.production_ok(self.sha, 'b' * 40, self.pulls, self.deployments, self.statuses)

    def test_unmerged_commit_blocked(self):
        with self.assertRaises(ValueError):
            indexnow.production_ok(self.sha, self.sha, [], self.deployments, self.statuses)

    def test_wrong_status_author_blocked(self):
        self.statuses['1'][0]['creator']['login'] = 'another'
        with self.assertRaises(ValueError):
            indexnow.production_ok(self.sha, self.sha, self.pulls, self.deployments, self.statuses)

    def test_no_confirmation_makes_zero_requests(self):
        with patch.object(indexnow, 'gh') as gh, patch.object(indexnow.urllib.request, 'Request') as request:
            with self.assertRaises(ValueError):
                indexnow.main(Path('/TEST'), self.sha, [], False)
            gh.assert_not_called()
            request.assert_not_called()

    def test_only_exact_canonical_sitemap_entries(self):
        with tempfile.TemporaryDirectory(prefix='indexnow-TEST-') as tmp:
            root = Path(tmp)
            (root / 'sitemap.xml').write_text('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>https://sottolineature.it/</loc></url></urlset>')
            self.assertEqual(indexnow.selected_urls(root, ['https://sottolineature.it/']), ['https://sottolineature.it/'])
            for values in ([], ['https://preview.vercel.app/'], ['https://sottolineature.it/?x=1'], ['https://sottolineature.it/'] * 2):
                with self.assertRaises(ValueError):
                    indexnow.selected_urls(root, values)


if __name__ == '__main__':
    unittest.main()
