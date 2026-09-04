#!/usr/bin/env python3
"""Elenca le citazioni il cui contesto e' troppo breve, in ordine di resa.

Il contesto e' l'unico testo originale della pagina citazione: tutto il resto
(la frase, il blocco fonte, i tag, le correlate) e' materiale altrui o
impaginazione. Al 2026-09-03 la sua mediana era di 31 parole e 623 citazioni su
749 stavano sotto le 45. Le pagine non sono povere di parole — mediana 237
visibili, minimo 167 — ma sono povere di *proprie*.

Il verso giusto in cui allungarle e' 60-90 parole: abbastanza per dire in che
punto dell'opera siamo e perche' quella frase conta, poche abbastanza da non
poter riempire. Sopra le 90 si comincia a girare intorno, e si vede.

L'ordine non e' casuale: prima le opere da cui il sito cita di piu', perche' un
contesto scritto bene li' vale per un lettore che ne aprira' quattro; poi i
contesti piu' corti. Ogni voce mostra quello che serve per scriverlo — il testo,
il punto nel testo, l'edizione — senza doverli cercare.

Uso:
    python3 tools/contesti_da_ampliare.py             riepilogo per opera
    python3 tools/contesti_da_ampliare.py 12          le prime 12 da scrivere
    python3 tools/contesti_da_ampliare.py --dialoghi  quelle con un personaggio
    python3 tools/contesti_da_ampliare.py --descrizione  quelle la cui descrizione
                                          nei risultati di ricerca ripiega sulla citazione

Da quando la meta description e' costruita sul contesto (generate_quote_pages.py,
DESC_MIN_CONTEXT), un contesto sotto gli 80 caratteri non e' piu' soltanto una
pagina magra: la pagina ripiega sulla citazione, cioe' mette nel risultato di
ricerca esattamente la riga che il lettore vedra' cliccando. Sono 61 pagine, ed
e' il sottoinsieme che rende di piu': la descrizione e' la riga che decide il
clic, e li' oggi non c'e' scritto niente che la frase non dica gia'.
"""
import collections
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(ROOT, 'data', 'citazioni.json')

SOGLIA = 45
DIALOGO = re.compile(r'[«"“].+[»"”]|\b(disse|dissi|pensò|rispose|esclamò|'
                     r'mormorò|gridò|chiese|replicò|sussurrò)\b', re.I)


def parole(testo):
    return len((testo or '').split())


def carica():
    with open(DATA_PATH, encoding='utf-8') as f:
        return json.load(f)


def da_fare(quotes):
    per_opera = collections.Counter((q['author'], q['title']) for q in quotes)
    corti = [q for q in quotes if parole(q.get('context')) < SOGLIA]
    corti.sort(key=lambda q: (-per_opera[(q['author'], q['title'])],
                              parole(q.get('context')), q['author']))
    return corti, per_opera


def scheda(q, n_opera):
    testo = q['quote'] if len(q['quote']) <= 200 else q['quote'][:197] + '...'
    righe = ['  «%s»' % testo,
             '   %s — %s%s   (%d citazioni da quest\'opera in archivio)'
             % (q['author'], q['title'], (' · ' + str(q['year'])) if q.get('year') else '',
                n_opera)]
    if q.get('source_locus'):
        righe.append('   dove: %s' % q['source_locus'])
    if q.get('source_edition'):
        righe.append('   edizione: %s' % q['source_edition'])
    if q.get('source_url'):
        righe.append('   testo online: %s' % q['source_url'])
    contesto = (q.get('context') or '').strip()
    righe.append('   contesto attuale (%d parole): %s' % (parole(contesto), contesto or '—'))
    if DIALOGO.search(q['quote']):
        righe.append('   → sembra una battuta: se sai chi la pronuncia, compila anche `speaker`')
    righe.append('')
    return '\n'.join(righe)


def main():
    argomenti = sys.argv[1:]
    solo_dialoghi = '--dialoghi' in argomenti
    solo_descrizione = '--descrizione' in argomenti
    numeri = [a for a in argomenti if a.isdigit()]
    quante = int(numeri[0]) if numeri else 0

    quotes = carica()
    corti, per_opera = da_fare(quotes)
    if solo_dialoghi:
        corti = [q for q in corti if DIALOGO.search(q['quote'])]
    if solo_descrizione:
        # la stessa soglia di generate_quote_pages.DESC_MIN_CONTEXT
        corti = [q for q in corti
                 if len(' '.join((q.get('context') or '').split())) < 80]

    lunghezze = sorted(parole(q.get('context')) for q in quotes)
    mediana = lunghezze[len(lunghezze) // 2]
    print('Archivio: %d citazioni — contesto mediano %d parole' % (len(quotes), mediana))
    # Le fasce si stampano sempre, e sempre sull'archivio intero. Il 2026-09-03
    # un lotto ha dichiarato "esaurita la fascia sotto le 20 parole, ne restano
    # 7" quando ne restavano 121: aveva letto il conteggio dell'elenco troncato
    # a N invece del totale. Un numero parziale che sembra totale e' peggio di
    # nessun numero, e questa e' la riga che lo impedisce.
    fasce = [('assente', 0, 1), ('1-19', 1, 20), ('20-29', 20, 30),
             ('30-44', 30, 45), ('45 e oltre', 45, 10 ** 6)]
    print('Fasce, su tutto l\'archivio:')
    for eti, lo, hi in fasce:
        n = sum(1 for v in lunghezze if lo <= v < hi)
        print('   %-12s %4d' % (eti, n))
    # Il filtro cambia cosa si sta contando, e la riga deve dirlo: e' la stessa
    # trappola del lotto del 2026-09-03, un numero vero sotto un'etichetta
    # sbagliata.
    if solo_descrizione:
        print('Con la descrizione che ripiega sulla citazione (contesto sotto '
              'gli 80 caratteri): %d' % len(corti))
    else:
        print('Sotto le %d parole: %d in tutto%s' % (SOGLIA, len(corti),
              ' (solo quelle con un dialogo)' if solo_dialoghi else ''))
    print('Bersaglio: 60-90 parole di testo originale per citazione.')
    print()

    if not quante:
        print('Le opere da cui conviene cominciare (piu\' citazioni = un lavoro che rende di piu\'):')
        print()
        conta = collections.Counter((q['author'], q['title']) for q in corti)
        for (autore, titolo), n in conta.most_common(15):
            print('  %2d da riscrivere  %s — %s' % (n, autore, titolo))
        print()
        print('Per vedere le schede pronte da compilare:')
        print('    python3 tools/contesti_da_ampliare.py 12')
        print('    python3 tools/contesti_da_ampliare.py --dialoghi 20')
        return 0

    for q in corti[:quante]:
        print(scheda(q, per_opera[(q['author'], q['title'])]))
    if len(corti) > quante:
        print('... e altre %d NON mostrate: questo elenco e\' troncato a %d.' % (len(corti) - quante, quante))
        print('    Il numero da guardare per sapere se una fascia e\' finita e\' quello in')
        print('    cima, non la lunghezza di questo elenco.')
    else:
        print('(mostrate tutte: sotto le %d parole non ne restano altre)' % SOGLIA)
    return 0


if __name__ == '__main__':
    sys.exit(main())
