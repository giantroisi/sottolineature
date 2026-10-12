"""Mantiene la larghezza mobile anche dopo il ridimensionamento desktop."""
from pathlib import Path
import re
import unittest


class HomeResponsiveTests(unittest.TestCase):
    def test_mobile_columns_have_explicit_full_width(self):
        template = (Path(__file__).resolve().parent.parent /
                    'templates/home_template.html').read_text(encoding='utf-8')
        responsive = re.search(
            r'@media\s*\(max-width:\s*700px\)\s*\{\s*\.grid\s*\{[^}]*\}\s*'
            r'\.grid\s+\.grid-col\s*\{([^}]*)\}', template)
        self.assertIsNotNone(responsive, 'Manca la regola per le colonne mobili')
        self.assertRegex(responsive.group(1), r'\bwidth:\s*100%\s*;')


if __name__ == '__main__':
    unittest.main()
