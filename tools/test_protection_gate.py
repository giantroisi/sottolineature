"""Cicli Git SOLO in repository temporanei: nessun commit del progetto reale."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
import io
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import protection_gate as g
from protection_worker import stable_window
import run_trusted_protection as launcher


class ProtectionGateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='sottolineature-git-fixture-')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.git('init', '-q')
        self.git('config', 'user.name', 'Fixture tecnica (non proprietario)')
        self.git('config', 'user.email', 'fixture@example.invalid')
        self.git('config', 'core.hooksPath', '/dev/null')
        self.git('config', 'commit.gpgsign', 'false')
        for name in g.ENGINE:
            self.write(name, (Path(__file__).parent.parent / name).read_bytes())
        self.write('tools/affiliate.py', b'# fixture codice affiliato\n')
        self.write('tools/generate_quote_pages.py', b'# fixture generatore\n')
        self.write('vercel.json', b'{"redirects": []}\n')
        self.write('robots.txt', b'User-agent: *\nAllow: /\n')
        self.write('data/affiliazioni.json', self.raw({'amazon_it_tracking_id': 'sottolineature-21', 'edizioni': []}))
        self.quotes = [{'author': 'Autore', 'title': 'Opera', 'quote': 'Una frase ' + s,
                        'added': '2026-01-01', 'context': 'contesto ' + s} for s in ('uno', 'due')]
        self.write('data/citazioni.json', self.raw(self.quotes))
        self.write('tools/slugs.json', self.raw({'quotes': {
            'Autore|Opera|Una frase uno': 'uno', 'Autore|Opera|Una frase due': 'due'}, 'authors': {}}))
        self.write('citazioni/uno.html', self.page('uno'))
        self.write('citazioni/due.html', self.page('due'))
        self.write('sitemap-citazioni.xml', self.sitemap())
        self.base = self.commit('Fixture base installata')
        self.owner_state = self.base

    def git(self, *args, input=None):
        p = subprocess.run(['git', '-C', str(self.root), *args], input=input,
                           capture_output=True, check=True)
        return p.stdout.decode().strip()

    def commit(self, message):
        self.git('add', '.')
        self.git('commit', '-qm', message)
        return self.git('rev-parse', 'HEAD')

    def write(self, path, data):
        p = self.root / path
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(data if isinstance(data, bytes) else data.encode())

    def raw(self, data):
        return (json.dumps(data, sort_keys=True, ensure_ascii=False, indent=2) + '\n').encode()

    def page(self, slug, text=None, published='2026-01-01', modified='2026-01-01', url=None, robots=''):
        url = url or g.SITE + '/citazioni/' + slug + '/'
        graph = json.dumps({'@type': 'WebPage', '@id': url,
                            'datePublished': published, 'dateModified': modified})
        return ('<link rel="canonical" href="' + url + '">' + robots +
                '<script type="application/ld+json">' + graph + '</script>' +
                '<main><h1>' + (text or 'contesto ' + slug) + '</h1></main>' +
                '<aside class="affiliate-card sans"><a class="affiliate-link" href="https://www.amazon.it/dp/8804710217/?tag=sottolineature-21">Acquista su Amazon</a></aside>' +
                '<footer><p class="affiliate-disclosure">Dichiarazione invariata</p></footer>').encode()

    def sitemap(self, date='2026-01-01', extra=''):
        return ('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + ''.join(
            '<url><loc>' + g.SITE + '/citazioni/' + s + '/</loc><lastmod>' + date + '</lastmod></url>'
            for s in ('uno', 'due')) + extra + '</urlset>').encode()

    def contract(self, path, data, base=None):
        base = base or self.base
        old = subprocess.run(['git', '-C', str(self.root), 'show', base + ':' + path], capture_output=True)
        return {'before': g.sha(old.stdout) if old.returncode == 0 else None, 'after': g.sha(data)}

    def normal(self, slug='uno', base=None):
        base = base or self.base
        m = g.empty_manifest(base)
        m.update(id='lotto-' + slug, change_class='editorial-bounded')
        data = json.loads(self.git('show', base + ':data/citazioni.json'))
        for q in data:
            if q['quote'].endswith(slug):
                q['context'] = 'contenuto migliorato ' + slug
        contents = {'data/citazioni.json': self.raw(data),
                    'citazioni/' + slug + '.html': self.page(slug, 'contenuto migliorato ' + slug)}
        m['sources'] = {'data/citazioni.json': self.contract('data/citazioni.json', contents['data/citazioni.json'], base)}
        p = 'citazioni/' + slug + '.html'
        m['pages']['modified'][p] = {'url': g.SITE + g.route(p), 'kind': g.page_kind(p), **self.contract(p, contents[p], base)}
        return m, contents

    def approve(self, manifest, base=None):
        """Simula un intervento umano PRECEDENTE in un repository usa-e-getta."""
        path = 'protection/manifests/' + manifest['id'] + '.json'
        raw = self.raw(manifest)
        self.write(path, raw)
        self.write(g.APPROVALS, self.raw({'version': 1, 'baselines': [base or manifest['base']],
            'approvals': [{'manifest_sha256': g.sha(raw), 'manifest_path': path,
                           'base': manifest['base'], 'change_class': manifest['change_class'],
                           'evidence': 'SOLO FIXTURE: approvazione precedente simulata, non del proprietario reale'}]}))
        self.owner_state = self.commit('Fixture approvazione separata precedente')
        return path

    def checker(self):
        return g.Gate(self.root, trusted_state=self.owner_state)

    def apply(self, contents):
        for p, data in contents.items():
            self.write(p, data)

    def test_clean_checkout_after_install_commit_passes(self):
        self.assertEqual(self.git('status', '--porcelain'), '')
        checker = self.checker()
        checker.trusted_engine()
        self.assertEqual(checker.verify(self.base)['delta'], {'new': [], 'removed': [], 'modified': []})

    def test_normal_editorial_batch_with_prior_digest_approval(self):
        m, contents = self.normal()
        path = self.approve(m)
        self.apply(contents)
        result = self.checker().verify(self.base, path)
        self.assertTrue(result['approved'])
        self.assertEqual(result['counts']['affiliate_card_pages'], 2)

    def test_source_only_preflight_and_complete_generated_contract(self):
        m, contents = self.normal()
        path = self.approve(m)
        self.write('data/citazioni.json', contents['data/citazioni.json'])
        self.checker().plan(self.base, path, phase='inputs')
        with self.assertRaisesRegex(g.Rejected, 'Impatto non esatto'):
            self.checker().plan(self.base, path)
        self.apply(contents)
        self.checker().verify(self.base, path)

    def test_committed_clean_batch_is_still_compared_to_approved_base(self):
        m, contents = self.normal()
        path = self.approve(m)
        self.apply(contents)
        candidate = self.commit('Fixture lotto editoriale completo')
        self.assertEqual(self.git('status', '--porcelain'), '')
        self.checker().verify(self.base, path)
        with self.assertRaises(g.Rejected):
            self.checker().plan(self.base)  # status pulito non autorizza none
        with self.assertRaises(g.Rejected):
            self.checker().plan(candidate)

    def test_next_editorial_batch_after_separate_owner_promotion(self):
        m, contents = self.normal()
        path = self.approve(m)
        self.apply(contents)
        self.checker().verify(self.base, path)
        next_base = self.commit('Fixture primo lotto finito')
        m2, contents2 = self.normal('due', next_base)
        path2 = self.approve(m2, next_base)
        self.apply(contents2)
        result = self.checker().verify(next_base, path2)
        self.assertEqual(result['delta']['modified'], ['citazioni/due.html', 'data/citazioni.json'])

    def test_invalid_full_sha_or_nonexistent_or_nonancestor_fails(self):
        for value in ('HEAD', self.base[:8], 'f' * 40, '', None):
            with self.subTest(value=value), self.assertRaises(g.Rejected):
                self.checker().plan(value)
        empty_tree = self.git('mktree', input=b'')
        other = self.git('commit-tree', empty_tree, '-m', 'Fixture non antenato')
        with self.assertRaises(g.Rejected):
            self.checker().plan(other)

    def test_current_lot_cannot_create_its_own_approval_even_after_commit(self):
        original_trust = self.owner_state
        m, contents = self.normal()
        path = self.approve(m)
        self.apply(contents)
        self.commit('Fixture tentata auto-approvazione')
        with self.assertRaisesRegex(g.Rejected, 'Auto-approvazione'):
            g.Gate(self.root, trusted_state=original_trust).plan(self.base, path)

    def test_manifest_owner_boolean_is_not_authority(self):
        m, contents = self.normal()
        m['owner_approved'] = True
        path = self.approve(m)
        self.apply(contents)
        with self.assertRaisesRegex(g.Rejected, 'auto-approvazione'):
            self.checker().plan(self.base, path)

    def test_prior_manifest_cannot_be_rewritten_with_same_id(self):
        m, contents = self.normal()
        path = self.approve(m)
        self.apply(contents)
        self.write(path, self.raw(m) + b' ')
        with self.assertRaisesRegex(g.Rejected, 'radice fidata'):
            self.checker().plan(self.base, path)

    def test_approval_is_bound_to_exact_digest_not_only_id(self):
        m, contents = self.normal()
        path = self.approve(m)
        self.apply(contents)
        new_path = 'protection/manifests/copia.json'
        self.write(new_path, self.raw({**m, 'id': 'copia'}))
        with self.assertRaisesRegex(g.Rejected, 'digest esatto'):
            self.checker().plan(self.base, new_path)

    def test_amazon_configuration_and_code_are_global(self):
        for p in ('data/affiliazioni.json', 'tools/affiliate.py', 'tools/protection_gate.py',
                  'tools/generate_quote_pages.py', 'vercel.json', 'robots.txt'):
            with self.subTest(path=p):
                self.assertEqual(g.classification(p, set(g.tree(self.root, self.base))), 'global')
        m = g.empty_manifest(self.base)
        m.update(id='amazon-globale', change_class='editorial-bounded')
        data = b'{"amazon_it_tracking_id": "altro-21", "edizioni": []}\n'
        m['sources'] = {'data/affiliazioni.json': self.contract('data/affiliazioni.json', data)}
        m['global_components'] = ['data/affiliazioni.json']
        path = self.approve(m)
        self.write('data/affiliazioni.json', data)
        with self.assertRaisesRegex(g.Rejected, 'approvazione globale'):
            self.checker().plan(self.base, path)

    def test_engine_cannot_judge_its_own_mutation(self):
        self.write('tools/protection_gate.py', b'print("bypass")\n')
        with self.assertRaisesRegex(g.Rejected, 'propria modifica'):
            self.checker().trusted_engine()

    def test_unknown_file_fails_even_if_declared(self):
        m, contents = self.normal()
        data = b'{"nuovo": true}\n'
        m['sources']['data/ignoto.json'] = {'before': None, 'after': g.sha(data)}
        path = self.approve(m)
        self.apply(contents)
        self.write('data/ignoto.json', data)
        with self.assertRaisesRegex(g.Rejected, 'File sconosciuto'):
            self.checker().plan(self.base, path)

    def test_one_extra_page_below_numeric_budget_fails(self):
        m, contents = self.normal()
        path = self.approve(m)
        self.apply(contents)
        self.write('citazioni/due.html', self.page('due', 'modifica extra'))
        with self.assertRaisesRegex(g.Rejected, 'extra=.*due.html'):
            self.checker().plan(self.base, path)

    def test_environment_override_cannot_authorize(self):
        for name in ('SEO_EXPECTED_QUOTE_IMPACT', 'SEO_APPROVE_GLOBAL_CHANGE', 'SEO_IMPACT_BASE'):
            with patch.dict('os.environ', {name: self.base}), self.assertRaisesRegex(g.Rejected, 'Deroga'):
                self.checker().plan(self.base)

    def mutation_case(self, content, pattern):
        m, contents = self.normal()
        p = 'citazioni/uno.html'
        contents[p] = content
        m['pages']['modified'][p].update(self.contract(p, content))
        path = self.approve(m)
        self.apply(contents)
        with self.assertRaisesRegex(g.Rejected, pattern):
            self.checker().verify(self.base, path)

    def test_first_publication_immutable_on_approved_page(self):
        self.mutation_case(self.page('uno', 'nuovo', published='2026-10-20'), 'datePublished')

    def test_canonical_collateral_rejected(self):
        body = self.page('uno', 'nuovo').replace(b'href="https://sottolineature.it/citazioni/uno/"',
                                               b'href="https://www.sottolineature.it/citazioni/uno/"', 1)
        self.mutation_case(body, 'canonical')

    def test_robots_collateral_rejected_with_inverted_attributes(self):
        self.mutation_case(self.page('uno', 'nuovo', robots='<meta content="noindex" name="robots">'), 'robots')

    def test_modified_date_must_be_declared(self):
        self.mutation_case(self.page('uno', 'nuovo', modified='2026-10-20'), 'modified')

    def test_related_change_rejected_on_declared_page(self):
        body = self.page('uno', 'nuovo') + b'<div class="related sans"><h2>Altre citazioni di Autore</h2><ul><li><a href="/citazioni/due/">due</a></li></ul></div>'
        self.mutation_case(body, 'Correlati')

    def test_affiliate_html_cannot_change_in_editorial_batch(self):
        body = self.page('uno', 'nuovo').replace(b'8804710217', b'8806216465')
        self.mutation_case(body, 'Amazon richiede lotto globale')

    def test_sitemap_change_rejected_even_with_exact_file_digest(self):
        m, contents = self.normal()
        contents['sitemap-citazioni.xml'] = self.sitemap('2026-10-20')
        m['derived']['sitemap-citazioni.xml'] = self.contract('sitemap-citazioni.xml', contents['sitemap-citazioni.xml'])
        path = self.approve(m)
        self.apply(contents)
        with self.assertRaisesRegex(g.Rejected, 'Sitemap lastmod'):
            self.checker().verify(self.base, path)

    def test_stable_related_window_ignores_added_candidate_and_vacancies(self):
        frozen = {'uno': {'author': ['due'], 'theme': []}}
        candidates = [('due', {}), ('nuova', {}), ('terza', {})]
        self.assertEqual(stable_window(candidates, 'uno', 5, frozen), [('due', {})])
        self.assertEqual(stable_window(candidates, 'uno', 4, frozen), [])
        self.assertEqual(frozen['uno'], {'author': ['due'], 'theme': []})

    def test_real_public_pages_keep_amazon_html_and_base_counts(self):
        root = Path(__file__).resolve().parent.parent
        config = json.loads((root / 'data/affiliazioni.json').read_text())
        self.assertEqual(config['amazon_it_tracking_id'], 'sottolineature-21')
        self.assertEqual(len(config['edizioni']), 135)
        self.assertEqual(len(json.loads((root / 'data/citazioni.json').read_text())), 883)
        for name in ('opere/oscar-wilde-il-ritratto-di-dorian-gray.html',
                     'citazioni/haruki-murakami-norwegian-wood.html', 'autori/goliarda-sapienza.html'):
            expected = g.git(root, 'show', g.TRUSTED_STATE + ':' + name, binary=True)
            self.assertEqual((root / name).read_bytes(), expected)

    def test_trusted_launcher_can_verify_clean_post_commit_checkout(self):
        with patch.object(sys, 'argv', ['trusted', 'check', '--base', self.base]), redirect_stdout(io.StringIO()) as output:
            launcher.load_trusted(self.root, self.owner_state)
        self.assertIn('"baseline": "' + self.base + '"', output.getvalue())

    def test_trusted_launcher_does_not_import_modified_candidate_gate(self):
        marker = self.root / 'NON_DEVE_ESISTERE'
        code = 'from pathlib import Path\nPath(' + repr(str(marker)) + ').write_text("unsafe")\n'
        self.write('tools/protection_gate.py', code.encode())
        with patch.object(sys, 'argv', ['trusted', 'check', '--base', self.base]), self.assertRaises(SystemExit):
            launcher.load_trusted(self.root, self.owner_state)
        self.assertFalse(marker.exists())

    def test_real_bootstrap_cannot_be_self_authorized(self):
        root = Path(__file__).resolve().parent.parent
        with patch.object(sys, 'argv', ['trusted', 'check', '--base', g.TRUSTED_STATE]):
            with self.assertRaisesRegex(ValueError, 'Bootstrap assente'):
                launcher.load_trusted(root)

    def test_citation_key_typo_may_keep_its_original_slug(self):
        m, contents = self.normal()
        q = json.loads(contents['data/citazioni.json'])
        q[0]['quote'] = 'Una frase corretta uno'
        contents['data/citazioni.json'] = self.raw(q)
        slugs = json.loads(self.git('show', self.base + ':tools/slugs.json'))
        slugs['quotes']['Autore|Opera|Una frase corretta uno'] = slugs['quotes'].pop('Autore|Opera|Una frase uno')
        contents['tools/slugs.json'] = self.raw(slugs)
        for p in ('data/citazioni.json', 'tools/slugs.json'):
            m['sources'][p] = self.contract(p, contents[p])
        path = self.approve(m)
        self.apply(contents)
        self.checker().verify(self.base, path)

    def test_real_modified_date_and_lastmod_require_exact_prior_contract(self):
        m, contents = self.normal()
        p = 'citazioni/uno.html'
        contents[p] = self.page('uno', 'contenuto migliorato uno', modified='2026-10-20')
        m['pages']['modified'][p].update(self.contract(p, contents[p]))
        old = g.Page(self.page('uno').decode()).modified
        new = g.Page(contents[p].decode()).modified
        m['seo']['modified'][g.SITE + '/citazioni/uno/'] = {'before': old, 'after': new}
        contents['sitemap-citazioni.xml'] = self.sitemap().replace(b'<lastmod>2026-01-01', b'<lastmod>2026-10-20', 1)
        m['derived']['sitemap-citazioni.xml'] = self.contract('sitemap-citazioni.xml', contents['sitemap-citazioni.xml'])
        m['seo']['lastmod'][g.SITE + '/citazioni/uno/'] = {'before': '2026-01-01', 'after': '2026-10-20'}
        path = self.approve(m)
        self.apply(contents)
        self.checker().verify(self.base, path)

    def test_asset_impact_cannot_evade_page_budget(self):
        m = g.empty_manifest(self.base)
        m.update(id='asset', change_class='editorial-bounded')
        data = b'fixture immagine'
        p = 'assets/covers/fixture.jpg'
        m['derived'][p] = {'before': None, 'after': g.sha(data)}
        m['asset_consumers'][p] = [g.SITE + '/citazioni/uno/', g.SITE + '/citazioni/due/']
        path = self.approve(m)
        self.write(p, data)
        with self.assertRaisesRegex(g.Rejected, 'Budget'):
            self.checker().plan(self.base, path)


if __name__ == '__main__':
    unittest.main()
