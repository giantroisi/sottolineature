#!/usr/bin/env python3
"""Trova le citazioni che potrebbero entrare in una raccolta e non ci sono.

Le raccolte non sono interrogazioni: sono elenchi scritti a mano in
`data/raccolte.json`, e ognuna e' stata pubblicata alla taglia minima prevista
dal CATALOGO (otto citazioni) e poi lasciata li'. Nel frattempo l'archivio e'
piu' che raddoppiato: al 2026-09-03, 234 citazioni su 749 comparivano in
almeno una raccolta. Due terzi dell'archivio non stava in nessuna, non per
una scelta di curatela ma perche' nessuno era piu' passato a guardare.

Questo strumento non aggiunge niente e non decide niente: fa la ricerca al
posto di chi cura, elencando le citazioni che nominano le parole di una
raccolta e che quella raccolta non contiene. La scelta di quali meritino di
entrare resta di chi legge, una per una — che e' l'unica cosa che distingue
una raccolta curata da un elenco generato da una parola chiave.

Uso:
    python3 tools/raccolte_da_ampliare.py            riepilogo di tutte
    python3 tools/raccolte_da_ampliare.py mare       le candidate di una
    python3 tools/raccolte_da_ampliare.py mare 40    con un tetto diverso
"""
import json
import os
import re
import sys
import unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(ROOT, 'data', 'citazioni.json')
RACCOLTE_PATH = os.path.join(ROOT, 'data', 'raccolte.json')

# Le parole con cui si cerca. Stanno qui e non in data/raccolte.json di
# proposito: non sono un dato del sito, non finiscono in nessuna pagina e non
# definiscono la raccolta — sono solo il setaccio con cui si pesca. Cambiarle
# non cambia niente di pubblicato.
#
# Convenzione: una parola che finisce con "-" e' una radice ("scritt-" prende
# scritto, scrittura, scrittore); tutte le altre valgono come parola intera.
#
# Serve tutte e due le forme, e la prima versione lo ha imparato sbagliando due
# volte. Cercando la sottostringa ovunque, «Amare o essere stati amati» finiva
# fra le citazioni sul mare; cercando la radice a inizio di parola, «mio marito
# mi annuncio' che voleva lasciarmi» ci finiva per "mari-", e «Il sole di San
# Silvestro spandeva non so che tepor velato» per "vela". Un setaccio che pesca
# tutto non fa risparmiare niente a chi poi deve buttare via.
PAROLE = {
    'libri-e-scrittura': ['libro', 'libri', 'legger-', 'lettura', 'letture', 'lettore', 'lettori',
                          'scriver-', 'scritt-', 'pagina', 'pagine', 'romanz-', 'poesia', 'poesie',
                          'poeta', 'poeti', 'parole', 'racconto', 'racconti', 'biblioteca',
                          'penna', 'inchiostro'],
    'mare': ['mare', 'mari', 'onda', 'onde', 'ocean-', 'marin-', 'scogli-', 'naufrag-', 'vela',
             'vele', 'riva', 'rive', 'spiaggia', 'spiagge', 'nave', 'navi', 'barca', 'barche',
             'marea', 'maree', 'isola', 'isole'],
    'morte': ['morte', 'morti', 'morire', 'muore', 'muoio', 'morto', 'morta', 'morendo',
              'defunt-', 'cadaver-', 'tomba', 'tombe', 'sepolcr-', 'funeral-', 'perire'],
    'frasi-brevi': [],  # criterio di lunghezza, non di parole: vedi candidate()
    'incipit': [],      # criterio strutturale: la citazione e' l'inizio dell'opera
    'amicizia': ['amico', 'amici', 'amica', 'amiche', 'amicizia', 'compagno', 'compagni'],
    'cambiamento': ['cambia', 'cambiare', 'cambiano', 'cambiato', 'mutare', 'mutamento',
                    'divent-', 'trasform-', 'diverso', 'rinasc-'],
    'sogni': ['sogno', 'sogni', 'sognar-', 'sognav-', 'sognat-', 'incubo', 'incubi'],
    'tristezza': ['triste', 'tristi', 'tristezza', 'dolore', 'dolori', 'pianto', 'piange',
                  'piangere', 'lacrim-', 'malincon-', 'sofferenz-', 'angoscia'],
    'bellezza': ['bello', 'bella', 'belle', 'belli', 'bellezz-', 'bellissim-', 'splendid-'],
    'viaggio': ['viaggio', 'viaggi', 'viaggiar-', 'cammin-', 'partire', 'partenza',
                          'strada', 'strade', 'sentiero', 'ritorno', 'valigia'],
    'donne': ['donna', 'donne', 'femmin-', 'madre', 'madri', 'sorella', 'sorelle', 'ragazza',
              'ragazze', 'moglie', 'signora'],
    'guerra': ['guerra', 'guerre', 'battagli-', 'soldat-', 'esercit-', 'armi', 'trincea',
               'nemico', 'nemici', 'combatt-', 'pace', 'fucil-'],
    'natura': ['albero', 'alberi', 'fiore', 'fiori', 'bosco', 'boschi', 'foresta', 'montagn-',
               'erba', 'giardino', 'natura', 'campagna', 'pioggia', 'vento', 'fiume', 'fiumi',
               'prato', 'radice', 'radici'],
    'animali': ['cane', 'cani', 'gatto', 'gatti', 'cavall-', 'uccell-', 'lupo', 'lupi',
                'animal-', 'bestia', 'bestie', 'insetto', 'farfalla', 'pesce', 'pesci'],
    'figli': ['figlio', 'figlia', 'figli', 'figlie', 'bambin-', 'nascere', 'nascita',
              'partorir-', 'genitor-'],
    'felicita': ['felice', 'felici', 'felicit-', 'gioia', 'contento', 'allegr-', 'lieto'],
    'infanzia': ['bambin-', 'infanzia', 'fanciull-', 'giocare', 'gioco', 'giochi', 'scuola'],
    'lavoro': ['lavoro', 'lavori', 'lavorar-', 'lavorare', 'mestiere', 'fatica', 'operai',
               'contadin-', 'ufficio', 'guadagn-', 'denaro'],
    'ricordo-e-memoria': ['ricord-', 'memoria', 'memorie', 'dimentic-', 'oblio', 'rammentar-',
                          'rimembr-', 'passato'],
    'famiglia': ['padre', 'madre', 'figlio', 'figlia', 'famiglia', 'fratell-', 'sorella',
                 'nonno', 'nonna', 'parenti'],
    'arte': ['arte', 'arti', 'artista', 'artisti', 'pittur-', 'quadro', 'quadri', 'dipint-',
             'scultur-', 'capolavor-', 'teatro'],
    'occhi-e-sguardo': ['occhi', 'occhio', 'sguardo', 'sguardi', 'guardar-', 'guarda', 'vedere',
                        'vista', 'pupill-', 'ciglia'],
    'notte': ['notte', 'notti', 'nottur-', 'buio', 'tenebr-', 'oscurit-', 'alba', 'tramonto'],
    'stelle-e-cielo': ['stella', 'stelle', 'cielo', 'cieli', 'luna', 'astri', 'firmament-',
                       'sole', 'nuvol-', 'costellaz-'],
    'silenzio': ['silenzio', 'silenzios-', 'tacere', 'tace', 'taceva', 'zitto', 'muto',
                 'mutismo'],
    'musica': ['musica', 'musical-', 'canto', 'cantar-', 'canzone', 'canzoni', 'suonar-',
               'violin-', 'melodi-', 'sinfoni-', 'orchestra'],
}

FRASE_BREVE_MAX = 12  # parole: la soglia con cui e' nata la raccolta


def strip_accenti(testo):
    scomposto = unicodedata.normalize('NFD', testo.lower())
    return ''.join(c for c in scomposto if unicodedata.category(c) != 'Mn')


def quote_key(q):
    return q['author'] + '|' + q['title'] + '|' + ' '.join(q['quote'].split()[:6])


def candidate(slug, quotes, dentro):
    """Citazioni non ancora nella raccolta che ne nominano le parole.

    Due raccolte non si fondano su un argomento e hanno un criterio proprio:
    «Frasi brevi» guarda la lunghezza, «Incipit memorabili» guarda il luogo nel
    testo (una citazione che sta all'inizio dell'opera lo dichiara nel campo
    source_locus).
    """
    fuori = [q for q in quotes if quote_key(q) not in dentro]
    if slug == 'frasi-brevi':
        return [(q, '%d parole' % len(q['quote'].split()))
                for q in fuori if len(q['quote'].split()) <= FRASE_BREVE_MAX]
    if slug == 'incipit':
        trovate = []
        for q in fuori:
            locus = strip_accenti(q.get('source_locus') or '')
            if re.search(r'\b(incipit|prima frase|prime righe|apertura|verso iniziale)\b', locus):
                trovate.append((q, q.get('source_locus')))
        return trovate
    chiavi = PAROLE.get(slug) or []
    if not chiavi:
        return []
    pezzi = []
    for k in chiavi:
        if k.endswith('-'):
            pezzi.append(re.escape(k[:-1]) + r'\w*')
        else:
            pezzi.append(re.escape(k) + r'\b')
    cerca = re.compile(r'\b(' + '|'.join(pezzi) + r')', re.I)
    trovate = []
    for q in fuori:
        testo = strip_accenti(q['quote'])
        colpite = []
        for m in cerca.finditer(testo):
            if m.group(1) not in colpite:
                colpite.append(m.group(1))
        if colpite:
            trovate.append((q, ', '.join(colpite[:3])))
    return trovate


def estratto(testo, parola, larghezza=150):
    """Mostra la parte della citazione dove sta la parola trovata.

    Tagliando sempre dall'inizio, di una citazione lunga si leggeva un pezzo
    che non conteneva la parola per cui era stata proposta, e non si capiva
    perche' fosse li'."""
    if len(testo) <= larghezza:
        return testo
    pos = strip_accenti(testo).find(strip_accenti(parola))
    if pos <= larghezza - 30:
        return testo[:larghezza - 3] + '...'
    inizio = max(0, pos - larghezza // 2)
    fine = min(len(testo), inizio + larghezza)
    return ('...' if inizio else '') + testo[inizio:fine] + ('...' if fine < len(testo) else '')


def main():
    with open(DATA_PATH, encoding='utf-8') as f:
        quotes = json.load(f)
    with open(RACCOLTE_PATH, encoding='utf-8') as f:
        raccolte = json.load(f)

    argomento = sys.argv[1] if len(sys.argv) > 1 else None
    tetto = int(sys.argv[2]) if len(sys.argv) > 2 else 25

    per_slug = {r['slug']: r for r in raccolte}
    if argomento and argomento not in per_slug:
        print('Raccolta sconosciuta: %s' % argomento)
        print('Disponibili: %s' % ', '.join(sorted(per_slug)))
        return 1

    if not argomento:
        senza = set(quotes and [quote_key(q) for q in quotes])
        usate = set()
        for r in raccolte:
            usate.update(r['quote_keys'])
        print('Archivio: %d citazioni — in almeno una raccolta: %d (%.0f%%)'
              % (len(quotes), len(usate & senza), 100.0 * len(usate & senza) / len(quotes)))
        print()
        print('%-22s %6s %11s' % ('raccolta', 'dentro', 'candidate'))
        righe = []
        for r in raccolte:
            dentro = set(r['quote_keys'])
            righe.append((len(candidate(r['slug'], quotes, dentro)), len(dentro), r['slug']))
        for n_cand, n_dentro, slug in sorted(righe, reverse=True):
            print('%-22s %6d %11d' % (slug, n_dentro, n_cand))
        print()
        print('Per vedere le candidate di una raccolta:')
        print('    python3 tools/raccolte_da_ampliare.py <slug>')
        return 0

    r = per_slug[argomento]
    dentro = set(r['quote_keys'])
    trovate = candidate(argomento, quotes, dentro)
    print('%s — %d citazioni dentro, %d candidate in archivio'
          % (r['title'], len(dentro), len(trovate)))
    print('(la chiave da incollare in quote_keys e\' la riga "chiave:")')
    print()
    for q, perche in trovate[:tetto]:
        print('  «%s»' % estratto(q['quote'], perche.split(', ')[0]))
        print('   %s — %s%s   [%s]'
              % (q['author'], q['title'], (' · ' + str(q['year'])) if q.get('year') else '', perche))
        print('   chiave: %s' % quote_key(q))
        print()
    if len(trovate) > tetto:
        print('... e altre %d. Alza il tetto: python3 tools/raccolte_da_ampliare.py %s %d'
              % (len(trovate) - tetto, argomento, len(trovate)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
