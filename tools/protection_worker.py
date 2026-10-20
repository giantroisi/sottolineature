"""Adattatore di sola staging: usa generatori Git fidati, non quelli del lotto.

Mantiene calendario e scelte correlate della baseline senza riscrivere i loro
sorgenti o importare il registro della vecchia worktree da 912 citazioni.
"""
import datetime
import hashlib
import json
from pathlib import Path
import sys
from types import SimpleNamespace


def stable_window(candidates, slug, count, frozen):
    group = {5: 'author', 4: 'theme'}.get(count)
    if group is None:
        raise ValueError('Contratto finestra del generatore cambiato: revisione globale necessaria')
    by_slug = dict(candidates)
    if slug in frozen:
        chosen = frozen[slug][group]
        if any(key not in by_slug for key in chosen):
            raise ValueError('Correlato congelato non piu valido: ' + slug)
        return [(key, by_slug[key]) for key in chosen]
    # Soltanto le nuove citazioni ricevono una scelta nuova.
    ordered = sorted(by_slug, key=lambda key: hashlib.sha256((slug + '\0' + group + '\0' + key).encode()).hexdigest())
    return [(key, by_slug[key]) for key in ordered[:count]]


def main(site, reference):
    site = Path(site).resolve()
    ref = json.loads(Path(reference).read_text())
    sys.path.insert(0, str(site / 'tools'))
    import build
    import generate_home as home
    import generate_quote_pages as quotes
    original_date = datetime.date
    anchor = original_date.fromisoformat(ref['home_date'])

    class FrozenDate(original_date):
        @classmethod
        def today(cls):
            return cls(anchor.year, anchor.month, anchor.day)

    home.datetime = SimpleNamespace(date=FrozenDate, timedelta=datetime.timedelta)
    quotes.finestra = lambda candidates, slug, count: stable_window(candidates, slug, count, ref['related'])
    build.main()
    if build.check_links.main() or build.controlla_jsonld.main():
        raise SystemExit('Controlli strutturali/JSON-LD falliti: output non applicabile')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
