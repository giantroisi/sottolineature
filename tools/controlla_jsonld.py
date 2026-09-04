#!/usr/bin/env python3
"""Controlla i dati strutturati di tutte le pagine generate.

Il JSON-LD e' l'unica parte del sito che non si vede guardando: se un nodo e'
malformato o un @id non risolve, Google smette di mostrare il risultato
arricchito e nessuno se ne accorge finche' non spariscono le visite. Da quando
le pagine citazione hanno preso about, mainEntity, publisher, inLanguage e
spokenByCharacter, e gli hub autore il sameAs, niente di tutto questo e' mai
stato validato.

Controlla, su ogni pagina generata:
  - il JSON-LD e' JSON valido e ha @context
  - ogni riferimento {"@id": ...} punta a un nodo presente nello stesso grafo
    (Google non unisce grafi di pagine diverse: un @id che sta altrove e' un
    riferimento morto)
  - nessun campo vuoto o con spazi soltanto
  - gli URL sono assoluti e sul dominio giusto
  - le date sono ISO (anno, o anno-mese-giorno)
  - i tipi usati sono quelli attesi e i campi obbligatori ci sono
  - le posizioni del BreadcrumbList sono 1..n senza salti

Uso: python3 tools/controlla_jsonld.py [--tutto]
"""
import json
import os
import re
import sys

RADICE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITO = 'https://sottolineature.it'
SALTA = {'node_modules', '.git', 'tools', 'templates', 'data', 'assets', 'archivio', '_v'}

BLOCCO = re.compile(r'<script type="application/ld\+json">(.*?)</script>', re.S)
ISO = re.compile(r'^\d{4}(-\d{2}(-\d{2})?)?$')

OBBLIGATORI = {
    'WebPage': ['url'],
    'Organization': ['name', 'url'],
    'Quotation': ['text'],
    'Book': ['name'],
    'Person': ['name'],
    'BreadcrumbList': ['itemListElement'],
    'CollectionPage': ['url'],
    'ItemList': ['itemListElement'],
}


def pagine():
    for cartella, sub, file in os.walk(RADICE):
        sub[:] = [d for d in sub if d not in SALTA and not d.startswith('.')]
        for f in file:
            if f.endswith('.html'):
                yield os.path.join(cartella, f)


def raccogli_id(nodo, dentro):
    """Tutti gli @id *definiti* (nodi con un @type)."""
    if isinstance(nodo, dict):
        if '@type' in nodo and '@id' in nodo:
            dentro.add(nodo['@id'])
        for v in nodo.values():
            raccogli_id(v, dentro)
    elif isinstance(nodo, list):
        for v in nodo:
            raccogli_id(v, dentro)


def raccogli_riferimenti(nodo, dentro, via='$'):
    """Tutti i {"@id": ...} *senza* @type, cioe' i rimandi."""
    if isinstance(nodo, dict):
        if '@id' in nodo and '@type' not in nodo and len(nodo) == 1:
            dentro.append((nodo['@id'], via))
        for k, v in nodo.items():
            raccogli_riferimenti(v, dentro, via + '.' + k)
    elif isinstance(nodo, list):
        for i, v in enumerate(nodo):
            raccogli_riferimenti(v, dentro, via + '[%d]' % i)


def controlla_valori(nodo, via, errori, avvisi):
    if isinstance(nodo, dict):
        tipo = nodo.get('@type')
        if isinstance(tipo, str) and tipo in OBBLIGATORI:
            for campo in OBBLIGATORI[tipo]:
                if not nodo.get(campo):
                    errori.append('%s: %s senza %s' % (via, tipo, campo))
        for k, v in nodo.items():
            if isinstance(v, str):
                if v.strip() == '':
                    errori.append('%s.%s vuoto' % (via, k))
                if k in ('url', 'item', '@id') and v.startswith('http') and not v.startswith(SITO):
                    if k != '@id':
                        avvisi.append('%s.%s fuori dominio: %s' % (via, k, v))
                if k in ('url', 'item') and not v.startswith('http'):
                    errori.append('%s.%s non assoluto: %s' % (via, k, v))
                if k in ('datePublished', 'dateCreated', 'dateModified') and not ISO.match(v):
                    errori.append('%s.%s non ISO: %s' % (via, k, v))
                if k == 'sameAs' and not v.startswith('http'):
                    errori.append('%s.sameAs non assoluto: %s' % (via, v))
            elif isinstance(v, list) and k == 'sameAs':
                for u in v:
                    if not isinstance(u, str) or not u.startswith('http'):
                        errori.append('%s.sameAs voce non valida: %r' % (via, u))
            else:
                controlla_valori(v, via + '.' + k, errori, avvisi)
    elif isinstance(nodo, list):
        for i, v in enumerate(nodo):
            controlla_valori(v, via + '[%d]' % i, errori, avvisi)


def controlla_breadcrumb(grafo, errori):
    for nodo in grafo:
        if not isinstance(nodo, dict) or nodo.get('@type') != 'BreadcrumbList':
            continue
        voci = nodo.get('itemListElement') or []
        atteso = 1
        for v in voci:
            if not isinstance(v, dict):
                errori.append('breadcrumb: voce non oggetto')
                continue
            if v.get('position') != atteso:
                errori.append('breadcrumb: posizione %r invece di %d' % (v.get('position'), atteso))
            if not v.get('name'):
                errori.append('breadcrumb: voce senza name')
            atteso += 1


def main():
    tutto = '--tutto' in sys.argv
    n_pagine = n_blocchi = 0
    senza = []
    problemi = {}
    avvisi_tot = {}
    tipi = {}
    for f in pagine():
        n_pagine += 1
        rel = os.path.relpath(f, RADICE)
        testo = open(f, encoding='utf-8').read()
        blocchi = BLOCCO.findall(testo)
        if not blocchi:
            senza.append(rel)
            continue
        errori, avvisi = [], []
        for b in blocchi:
            n_blocchi += 1
            try:
                dati = json.loads(b)
            except Exception as e:
                errori.append('JSON non valido: %s' % e)
                continue
            if '@context' not in dati:
                errori.append('senza @context')
            grafo = dati.get('@graph')
            if grafo is None:
                grafo = [dati]
            for nodo in grafo:
                t = nodo.get('@type') if isinstance(nodo, dict) else None
                if isinstance(t, str):
                    tipi[t] = tipi.get(t, 0) + 1
            definiti = set()
            raccogli_id(dati, definiti)
            rimandi = []
            raccogli_riferimenti(dati, rimandi)
            for rid, via in rimandi:
                if rid not in definiti:
                    errori.append('rimando morto %s (in %s)' % (rid, via))
            controlla_valori(dati, '$', errori, avvisi)
            controlla_breadcrumb(grafo, errori)
        if errori:
            problemi[rel] = errori
        if avvisi:
            avvisi_tot[rel] = avvisi

    print('Pagine esaminate: %d — blocchi JSON-LD: %d' % (n_pagine, n_blocchi))
    print('Tipi usati: ' + ', '.join('%s %d' % (k, v) for k, v in sorted(tipi.items(), key=lambda x: -x[1])))
    if senza:
        print('\nSenza JSON-LD: %d' % len(senza))
        for s in senza[:15]:
            print('   ' + s)
        if len(senza) > 15 and not tutto:
            print('   ... e altre %d (--tutto per vederle)' % (len(senza) - 15))
    if avvisi_tot:
        campioni = list(avvisi_tot.items())
        print('\nAvvisi (non bloccanti): %d pagine' % len(avvisi_tot))
        for rel, a in (campioni if tutto else campioni[:5]):
            print('   %s' % rel)
            for x in a[:4]:
                print('      %s' % x)
    if problemi:
        print('\nERRORI: %d pagine' % len(problemi))
        campioni = list(problemi.items())
        for rel, e in (campioni if tutto else campioni[:12]):
            print('   %s' % rel)
            for x in e[:6]:
                print('      %s' % x)
        if len(campioni) > 12 and not tutto:
            print('   ... e altre %d pagine (--tutto per vederle)' % (len(campioni) - 12))
        return 1
    print('\nNessun errore nei dati strutturati.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
