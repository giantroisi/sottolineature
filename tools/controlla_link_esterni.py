#!/usr/bin/env python3
"""Controlla uno per uno i link esterni delle citazioni (`source_url`).

Perche' esiste: il crawl dell'11 settembre 2026 ha trovato **189 link esterni
che rispondono 4xx**. Sono le fonti delle citazioni - Wikiquote, Wikisource,
Liberliber -, e una citazione che rimanda a una pagina che non esiste piu' e'
la sola cosa che questo sito non puo' permettersi: la verificabilita' e' la
promessa.

Perche' e' uno script da lanciare a mano e non un passo di `build.py`: dalle
sessioni Claude la rete verso quei domini e' chiusa, e comunque seicento
richieste non vanno fatte a ogni build. Si lancia da un terminale qualsiasi che
abbia rete:

    python3 tools/controlla_link_esterni.py

Scrive `archivio/link_esterni.json` (il dato, per chi poi corregge) e stampa un
riepilogo leggibile. Non modifica nessuna citazione: leggere e correggere sono
due mestieri diversi, e il secondo va fatto guardando caso per caso.

Educazione verso i siti che ci ospitano le fonti: una richiesta alla volta per
dominio, mezzo secondo di pausa, `HEAD` prima di `GET`, e uno user-agent che
dice chi siamo e dove scrivere.
"""
import json
import os
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATI = os.path.join(ROOT, 'data', 'citazioni.json')
USCITA = os.path.join(ROOT, 'archivio', 'link_esterni.json')
UA = ('Mozilla/5.0 (compatible; SottolineatureLinkCheck/1.0; '
      '+https://sottolineature.it/; sottolineature@outlook.it)')
PAUSA = 0.5      # secondi fra due richieste allo stesso dominio
TIMEOUT = 20


def carica():
    with open(DATI, encoding='utf-8') as f:
        d = json.load(f)
    return d if isinstance(d, list) else d['citazioni']


def chiedi(url, metodo='HEAD'):
    """Ritorna (stato, url_finale, nota). Lo stato e' un numero HTTP, oppure 0
    quando non si e' arrivati a parlare col server."""
    req = urllib.request.Request(url, method=metodo, headers={
        'User-Agent': UA,
        'Accept': 'text/html,application/xhtml+xml,*/*;q=0.8',
        'Accept-Language': 'it,en;q=0.8',
    })
    ctx = ssl.create_default_context()
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT, context=ctx) as r:
            return r.status, r.url, ''
    except urllib.error.HTTPError as e:
        # 405/403 su HEAD capita spesso: non e' il link a essere rotto, e' il
        # metodo a non piacere. Si riprova una volta sola, con GET.
        if metodo == 'HEAD' and e.code in (400, 403, 405, 501):
            return chiedi(url, 'GET')
        return e.code, getattr(e, 'url', url), ''
    except urllib.error.URLError as e:
        return 0, url, str(getattr(e, 'reason', e))[:120]
    except Exception as e:  # timeout, certificati, redirect infiniti
        return 0, url, type(e).__name__ + ': ' + str(e)[:100]


def main():
    quotes = carica()
    per_url = defaultdict(list)
    for q in quotes:
        u = (q.get('source_url') or '').strip()
        if u:
            per_url[u].append({'author': q['author'], 'title': q['title'],
                               'quote': q['quote'][:70]})
    per_dominio = defaultdict(list)
    for u in per_url:
        per_dominio[urllib.parse.urlparse(u).netloc].append(u)

    print(len(per_url), 'indirizzi distinti su', sum(len(v) for v in per_url.values()),
          'citazioni,', len(per_dominio), 'domini')
    esiti = {}
    fatti = 0
    for dominio, urls in sorted(per_dominio.items(), key=lambda t: -len(t[1])):
        for u in urls:
            stato, finale, nota = chiedi(u)
            esiti[u] = {
                'stato': stato,
                'finale': finale if finale != u else '',
                'nota': nota,
                'citazioni': per_url[u],
            }
            fatti += 1
            if stato >= 400 or stato == 0:
                print('  [%d/%d] %s  %s' % (fatti, len(per_url), stato or 'irraggiungibile', u))
            elif fatti % 25 == 0:
                print('  [%d/%d] ...' % (fatti, len(per_url)))
            sys.stdout.flush()
            time.sleep(PAUSA)

    os.makedirs(os.path.dirname(USCITA), exist_ok=True)
    with open(USCITA, 'w', encoding='utf-8') as f:
        json.dump(esiti, f, ensure_ascii=False, indent=1, sort_keys=True)

    rotti = {u: e for u, e in esiti.items() if e['stato'] >= 400}
    spostati = {u: e for u, e in esiti.items() if 200 <= e['stato'] < 300 and e['finale']}
    muti = {u: e for u, e in esiti.items() if e['stato'] == 0}
    print()
    print('=' * 60)
    print('rotti (4xx/5xx):    ', len(rotti), 'indirizzi,',
          sum(len(e['citazioni']) for e in rotti.values()), 'citazioni')
    print('spostati (redirect):', len(spostati), 'indirizzi')
    print('irraggiungibili:    ', len(muti), 'indirizzi (rete, certificato o timeout)')
    print('a posto:            ', len(esiti) - len(rotti) - len(spostati) - len(muti))
    print()
    for u, e in sorted(rotti.items(), key=lambda t: -len(t[1]['citazioni'])):
        print(e['stato'], u)
        for c in e['citazioni']:
            print('      ', c['author'], '-', c['title'])
    print()
    print('dettaglio completo in', USCITA)


if __name__ == '__main__':
    main()
