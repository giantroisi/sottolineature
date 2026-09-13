#!/usr/bin/env python3
"""Legge archivio/link_esterni.json e dice, per ogni link rotto, cosa farne.

`controlla_link_esterni.py` chiede agli indirizzi come stanno; questo li divide
in mucchi secondo cosa comporta ciascun caso per la citazione che ci sta sotto.
La distinzione che conta non e' fra 404 e 301: e' fra **una citazione che resta
verificabile anche senza quel link** e una che senza quel link non lo e' piu'.

Per il punto 2 della lista di chiusura (`CATALOGO.md`) una citazione e'
tracciabile se ha edizione e luogo nel testo; il link e' la comodita' che
risparmia la biblioteca, non la prova. Quindi:

- link spostato (redirect a una pagina vera)  -> si aggiorna l'indirizzo, fine
- link spostato alla home o a una ricerca     -> vale come morto: non porta piu'
                                                 a quel testo
- link morto, citazione con edizione + locus  -> si toglie il link, la citazione
                                                 resta in piedi
- link morto, citazione senza edizione o locus-> **da riverificare a mano**: e'
                                                 l'unico mucchio che vale
                                                 davvero il tempo di qualcuno

Non modifica niente: stampa e basta. Le correzioni si fanno guardando.
"""
import json
import os
import urllib.parse
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REFERTO = os.path.join(ROOT, 'archivio', 'link_esterni.json')
DATI = os.path.join(ROOT, 'data', 'citazioni.json')


def carica_citazioni():
    with open(DATI, encoding='utf-8') as f:
        d = json.load(f)
    return d if isinstance(d, list) else d['citazioni']


def e_home_o_ricerca(url):
    p = urllib.parse.urlparse(url)
    if p.path in ('', '/'):
        return True
    if p.query and any(k in p.query.lower() for k in ('search', 'cerca', 'q=', 's=')):
        return True
    return p.path.rstrip('/').lower() in ('/index.php', '/wiki', '/home')


def main():
    if not os.path.exists(REFERTO):
        raise SystemExit('manca ' + REFERTO + ': lancia prima tools/controlla_link_esterni.py')
    with open(REFERTO, encoding='utf-8') as f:
        esiti = json.load(f)
    per_url = defaultdict(list)
    for q in carica_citazioni():
        u = (q.get('source_url') or '').strip()
        if u:
            per_url[u].append(q)

    aggiorna, morti_reggono, morti_scoperti, muti = [], [], [], []
    for u, e in esiti.items():
        stato = e.get('stato', 0)
        finale = e.get('finale') or ''
        citazioni = per_url.get(u, [])
        if 200 <= stato < 300 and finale and not e_home_o_ricerca(finale):
            aggiorna.append((u, finale, citazioni))
            continue
        if 200 <= stato < 300 and not finale:
            continue
        if stato == 0:
            muti.append((u, e.get('nota', ''), citazioni))
            continue
        # morto: 4xx/5xx, oppure redirect finito sulla home o su una ricerca -
        # che e' morto lo stesso, perche' a quel testo non porta piu'
        motivo = str(stato) if stato >= 400 else 'spostato alla home'
        for q in citazioni:
            regge = bool(q.get('source_edition')) and bool(q.get('source_locus'))
            (morti_reggono if regge else morti_scoperti).append((u, motivo, q))

    print('=' * 70)
    print('DA AGGIORNARE — la fonte si e\' spostata e la pagina nuova esiste:',
          len(aggiorna), 'indirizzi')
    for u, finale, cs in aggiorna[:60]:
        print('  ', u)
        print('   ->', finale, '  (%d citazion%s)' % (len(cs), 'e' if len(cs) == 1 else 'i'))
    print()
    print('DA RIVERIFICARE A MANO — link morto e la citazione non ha edizione o luogo nel testo:',
          len(morti_scoperti))
    for u, motivo, q in morti_scoperti:
        print('  ', motivo, q['author'], '-', q['title'])
        print('       edizione:', repr(q.get('source_edition', '')), '| locus:', repr(q.get('source_locus', '')))
        print('       ', u)
    print()
    print('LINK DA TOGLIERE — morto, ma la citazione regge su edizione e luogo nel testo:',
          len(morti_reggono))
    conteggio = defaultdict(int)
    for u, _motivo, q in morti_reggono:
        conteggio[urllib.parse.urlparse(u).netloc] += 1
    for d, n in sorted(conteggio.items(), key=lambda t: -t[1]):
        print('   %4d  %s' % (n, d))
    print()
    print('IRRAGGIUNGIBILI — non si conclude niente, non si tocca niente:', len(muti))
    for u, nota, cs in muti[:20]:
        print('  ', u, ' —', nota)


if __name__ == '__main__':
    main()
