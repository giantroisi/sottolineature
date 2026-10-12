"""La migrazione URL preserva i dati personali e non sovrascrive note esistenti."""
import json
import os
import re
from pathlib import Path
import subprocess
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_quote_pages as qp
from quote_url_migrations import render_script

OLD = 'michela-murgia-accabadora'
NEW = OLD + '-fillus-de-anima'
SELECTED = 'sottolineature-underlined'
NOTES = 'sottolineature-notes'
NODE = """const fs = require('node:fs'), vm = require('node:vm');
const input = JSON.parse(fs.readFileSync(0, 'utf8'));
const data = input.data, writes = [];
vm.runInNewContext(input.script, {localStorage: {
 getItem: key => { if (input.blocked) throw Error('Storage blocked'); return data[key] || null; },
 setItem: (key, value) => { data[key] = value; writes.push(key); }
}});
process.stdout.write(JSON.stringify({data, writes}));"""


def simulate(data, blocked=False):
    script = re.search(r'<script[^>]*>(.*?)</script>', render_script({OLD: NEW}), re.S).group(1)
    return json.loads(subprocess.check_output([os.environ.get('SOTTOLINEATURE_NODE', 'node'), '-e', NODE],
        input=json.dumps({'script': script, 'data': data, 'blocked': blocked}).encode()))


class QuoteUrlMigrationTests(unittest.TestCase):
    def test_selection_and_note_are_moved_without_losing_other_data(self):
        actual = simulate({SELECTED: json.dumps([OLD, 'altra-citazione']),
                           NOTES: json.dumps({OLD: 'Nota personale', 'altra-citazione': 'Altra nota'})})
        self.assertEqual(json.loads(actual['data'][SELECTED]), [NEW, 'altra-citazione'])
        notes = json.loads(actual['data'][NOTES])
        self.assertEqual(notes[NEW], 'Nota personale')
        self.assertEqual(notes[OLD], 'Nota personale')
        self.assertEqual(notes['altra-citazione'], 'Altra nota')

    def test_existing_new_note_is_never_overwritten_and_selection_is_deduplicated(self):
        actual = simulate({SELECTED: json.dumps([OLD, NEW]),
                           NOTES: json.dumps({OLD: 'Vecchia nota', NEW: 'Nuova nota'})})
        self.assertEqual(json.loads(actual['data'][SELECTED]), [NEW])
        self.assertEqual(json.loads(actual['data'][NOTES]), {OLD: 'Vecchia nota', NEW: 'Nuova nota'})

    def test_second_run_is_idempotent(self):
        first = simulate({SELECTED: json.dumps([OLD]), NOTES: json.dumps({OLD: 'Nota'})})
        second = simulate(first['data'])
        self.assertEqual(second['data'], first['data'])
        self.assertEqual(second['writes'], [])

    def test_malformed_storage_is_not_cleared_or_replaced(self):
        data = {SELECTED: json.dumps([OLD]), NOTES: '{non valido'}
        actual = simulate(data)
        self.assertEqual(actual['data'], data)
        self.assertEqual(actual['writes'], [])

    def test_blocked_storage_does_not_throw_or_write(self):
        actual = simulate({}, blocked=True)
        self.assertEqual(actual, {'data': {}, 'writes': []})

    def test_script_precedes_readers_on_home_quote_and_personal_page(self):
        for name in ['index.html', 'citazioni/' + NEW + '.html', 'le-mie-sottolineature.html']:
            source = (Path(qp.ROOT) / name).read_text()
            self.assertEqual(source.count('<script data-quote-url-migration>'), 1, name)
            self.assertLess(source.index('<script data-quote-url-migration>'), source.index('<body'), name)
            self.assertIn('"' + OLD + '": "' + NEW + '"', source)


if __name__ == '__main__':
    unittest.main()
