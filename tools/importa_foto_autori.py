#!/usr/bin/env python3
"""Porta dentro il sito le foto raccolte dal browser, verificandole.

Legge il pacchetto scritto da `archivio/raccogli-foto-autori.html` (di norma
~/Downloads/foto-autori.tar, o una cartella gia' scompattata), ricalcola per
ogni immagine l'impronta SHA-256 e la confronta con quella dichiarata nel
manifest: se non combacia il file non entra. Poi copia le immagini in
assets/autori/ e scrive data/autori_foto.json, che e' il dato da cui il
generatore stampa il ritratto e il suo credito.

Uso:
    python3 tools/importa_foto_autori.py ~/Downloads/foto-autori.tar
    python3 tools/importa_foto_autori.py ~/Downloads/foto-autori      # cartella

Non entra nessuna foto senza licenza libera dichiarata, fotografo (dove la
licenza lo richiede) e indirizzo del file su Commons: senza quei tre campi il
credito non si puo' scrivere, e senza credito la foto non si pubblica.
"""
import hashlib
import json
import os
import shutil
import sys
import tarfile
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEST_IMG = os.path.join(ROOT, 'assets', 'autori')
DEST_DATI = os.path.join(ROOT, 'data', 'autori_foto.json')
LICENZE_LIBERE = ('pd', 'cc0', 'cc-by')


def apri(percorso):
    """Ritorna la cartella con dentro manifest.json e foto/. Se e' un tar lo
    scompatta in una cartella temporanea."""
    percorso = os.path.expanduser(percorso)
    if os.path.isdir(percorso):
        return percorso, None
    tmp = tempfile.mkdtemp(prefix='foto-autori-')
    with tarfile.open(percorso) as t:
        for m in t.getmembers():
            # nessun percorso che esca dalla cartella: il pacchetto lo scrive il
            # nostro raccoglitore, ma un tar resta un tar
            if m.name.startswith('/') or '..' in m.name.split('/'):
                raise SystemExit('percorso sospetto nel pacchetto: ' + m.name)
        t.extractall(tmp)
    return tmp, tmp


def main():
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    cartella, da_pulire = apri(sys.argv[1])
    with open(os.path.join(cartella, 'manifest.json'), encoding='utf-8') as f:
        righe = json.load(f)

    os.makedirs(DEST_IMG, exist_ok=True)
    dati = {}
    dentro, fuori = [], []
    for r in righe:
        if not r.get('ok'):
            fuori.append((r['autore'], r.get('motivo', 'scartata dal raccoglitore')))
            continue
        lic = (r.get('licenza_codice') or '').lower()
        if not lic.startswith(LICENZE_LIBERE):
            fuori.append((r['autore'], 'licenza non libera: ' + lic))
            continue
        if not r.get('pagina_commons'):
            fuori.append((r['autore'], 'manca l\'indirizzo del file su Commons'))
            continue
        # CC BY e CC BY-SA obbligano a nominare l'autore della fotografia; il
        # pubblico dominio no, e li' il campo puo' restare vuoto senza colpa.
        if lic.startswith('cc-by') and not r.get('fotografo'):
            fuori.append((r['autore'], 'licenza ' + lic + ' senza nome del fotografo'))
            continue
        sorgente = os.path.join(cartella, 'foto', r['file'])
        if not os.path.exists(sorgente):
            fuori.append((r['autore'], 'file mancante nel pacchetto'))
            continue
        with open(sorgente, 'rb') as f:
            byte = f.read()
        sha = hashlib.sha256(byte).hexdigest()
        if sha != r.get('sha256'):
            fuori.append((r['autore'], 'impronta diversa da quella dichiarata'))
            continue
        shutil.copyfile(sorgente, os.path.join(DEST_IMG, r['file']))
        dati[r['autore']] = {
            'file': '/assets/autori/' + r['file'],
            'sha256': sha,
            'licenza': r.get('licenza_nome') or r.get('licenza_codice'),
            'licenza_codice': lic,
            'licenza_url': r.get('licenza_url', ''),
            'fotografo': r.get('fotografo', ''),
            'pagina_commons': r['pagina_commons'],
            'larghezza': r.get('larghezza'),
            'altezza': r.get('altezza'),
        }
        dentro.append(r['autore'])

    with open(DEST_DATI, 'w', encoding='utf-8') as f:
        json.dump(dati, f, ensure_ascii=False, indent=1, sort_keys=True)

    print('foto entrate:', len(dentro))
    print('scartate:    ', len(fuori))
    for a, m in fuori[:40]:
        print('   ', a, '—', m)
    if len(fuori) > 40:
        print('    ... e altre', len(fuori) - 40)
    print('scritto', DEST_DATI)
    if da_pulire:
        shutil.rmtree(da_pulire, ignore_errors=True)


if __name__ == '__main__':
    main()
