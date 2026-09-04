#!/usr/bin/env python3
"""Rimette le copertine del commit 744305f2 sulle citazioni che ne sono prive.

Serve perche' due sessioni scrivono sullo stesso data/citazioni.json: chi ha
il file aperto in memoria e lo risalva riporta indietro il campo `cover` senza
accorgersene. E' successo il 2026-09-04: 64 copertine appena aggiunte sono
tornate vuote perche' l'altra sessione ha salvato la sua copia.

Non sovrascrive il file intero - sarebbe lo stesso errore al contrario, e
cancellerebbe il lavoro altrui. Prende solo il campo `cover`, e solo dove
adesso e' vuoto: qualunque altra cosa l'altra sessione abbia scritto resta.

Uso: python3 tools/riapplica_copertine.py
"""
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATI = os.path.join(ROOT, 'data', 'citazioni.json')
COMMIT = '744305f2'


def main():
    try:
        grezzo = subprocess.check_output(
            ['git', '-C', ROOT, 'show', COMMIT + ':data/citazioni.json'],
            stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        print('Non trovo il commit', COMMIT)
        return 1
    buone = {(q['author'], q['title']): q['cover']
             for q in json.loads(grezzo) if q.get('cover')}

    with open(DATI, encoding='utf-8') as f:
        d = json.load(f)
    n = 0
    for q in d:
        if q.get('cover'):
            continue
        c = buone.get((q['author'], q['title']))
        if c:
            q['cover'] = c
            n += 1
    if n:
        tmp = DATI + '.nuovo'
        with open(tmp, 'w', encoding='utf-8') as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
            f.write('\n')
        os.replace(tmp, DATI)
    print('copertine rimesse:', n)
    print('con copertina:', sum(1 for q in d if q.get('cover')), '/', len(d))
    return 0


if __name__ == '__main__':
    sys.exit(main())
