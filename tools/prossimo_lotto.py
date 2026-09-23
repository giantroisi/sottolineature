#!/usr/bin/env python3
"""Dice da dove conviene ripartire quando si aggiungono citazioni.

Non aggiunge e non decide niente: legge l'archivio e stampa i numeri che
servono a scegliere il lotto successivo senza doverli ricontare ogni volta —
la quota di saggistica rispetto al tetto del CATALOGO, gli autori fermi a
poche righe, le opere a una citazione dalla pagina propria, le raccolte
sottili e gli autori senza ritratto.

E' lo strumento con cui si apre ogni turno della routine oraria: chi legge
sceglie poi una riga sola da questo elenco, e la verifica sul testo.

Uso:
    python3 tools/prossimo_lotto.py
"""
import collections
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TETTO_SAGGISTICA = 15.0   # CATALOGO, quota massima della saggistica
SOGLIA_OPERA = 6          # citazioni sulla stessa opera per avere la pagina


def carica(nome):
    with open(os.path.join(ROOT, 'data', nome), encoding='utf-8') as f:
        return json.load(f)


def main():
    q = carica('citazioni.json')
    raccolte = carica('raccolte.json')
    try:
        foto = carica('autori_foto.json')
    except FileNotFoundError:
        foto = {}

    tot = len(q)
    sag = sum(1 for x in q if (x.get('genre') or '') == 'saggistica')
    quota = 100.0 * sag / tot if tot else 0.0
    print('Archivio: %d citazioni, %d autori, %d opere con pagina possibile'
          % (tot, len({x['author'] for x in q}),
             sum(1 for _, n in collections.Counter(
                 (x['author'], x['title']) for x in q).items() if n >= SOGLIA_OPERA)))
    print('Saggistica: %d citazioni, %.1f%% (tetto %.0f%%) -> %s'
          % (sag, quota, TETTO_SAGGISTICA,
             'solo narrativa e poesia' if quota > TETTO_SAGGISTICA else 'saggistica ammessa'))

    per_autore = collections.Counter(x['author'] for x in q)
    per_opera = collections.Counter((x['author'], x['title']) for x in q)

    print('\nOpere a una o due citazioni dalla pagina propria (soglia %d):' % SOGLIA_OPERA)
    vicine = [(a, t, n) for (a, t), n in per_opera.items() if SOGLIA_OPERA - 2 <= n < SOGLIA_OPERA]
    for a, t, n in sorted(vicine, key=lambda r: -r[2])[:20]:
        print('  %d/%d  %s - %s' % (n, SOGLIA_OPERA, a, t))
    if not vicine:
        print('  nessuna')

    print('\nAutori gia in archivio fermi a 3-5 citazioni:')
    fermi = [(a, n) for a, n in per_autore.items() if 3 <= n <= 5]
    for a, n in sorted(fermi, key=lambda r: (-r[1], r[0]))[:30]:
        titoli = sorted({x['title'] for x in q if x['author'] == a})
        print('  %d  %-28s  %s' % (n, a, '; '.join(titoli)))

    print('\nRaccolte piu sottili:')
    for r in sorted(raccolte, key=lambda r: len(r['quote_keys']))[:8]:
        print('  %3d  %s' % (len(r['quote_keys']), r['slug']))

    senza = sorted({x['author'] for x in q} - set(foto))
    print('\nAutori senza ritratto: %d%s' % (len(senza),
                                             (' -> ' + ', '.join(senza)) if senza else ''))


if __name__ == '__main__':
    main()
