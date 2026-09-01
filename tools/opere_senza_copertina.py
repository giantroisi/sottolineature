#!/usr/bin/env python3
"""Elenca le opere che non hanno ancora una copertina.

La copertina appartiene all'opera, non alla singola citazione: qui si conta
per (autore, titolo) e si mostra quante citazioni resterebbero senza immagine.
L'elenco e' ordinato per numero di citazioni decrescente, cosi' si parte da
dove la copertina si vede di piu'.

Uso: python3 tools/opere_senza_copertina.py [quante]
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(ROOT, 'data', 'citazioni.json')


def main():
    limite = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    with open(DATA_PATH, encoding='utf-8') as f:
        quotes = json.load(f)

    opere = {}
    for q in quotes:
        chiave = (q['author'], q['title'])
        voce = opere.setdefault(chiave, {'tot': 0, 'con': 0, 'anno': q.get('year', '')})
        voce['tot'] += 1
        if q.get('cover'):
            voce['con'] += 1

    senza = [(k, v) for k, v in opere.items() if v['con'] == 0]
    senza.sort(key=lambda x: (-x[1]['tot'], x[0][0], x[0][1]))

    print('Opere totali: %d — senza copertina: %d (%d citazioni)'
          % (len(opere), len(senza), sum(v['tot'] for _, v in senza)))
    print()
    mostrate = senza[:limite] if limite else senza
    for (autore, titolo), v in mostrate:
        anno = (' (%s)' % v['anno']) if v['anno'] else ''
        print('%2d  %s — %s%s' % (v['tot'], autore, titolo, anno))
    if limite and len(senza) > limite:
        print('... e altre %d opere' % (len(senza) - limite))
    return 0


if __name__ == '__main__':
    sys.exit(main())
