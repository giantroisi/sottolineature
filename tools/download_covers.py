#!/usr/bin/env python3
"""Scarica in locale le copertine Open Library referenziate in
data/citazioni.json, cosi' ogni visita al sito non dipende piu' da
covers.openlibrary.org: se il servizio e' lento o cambia indirizzo la
copertina non sparisce.

Legge i valori distinti del campo `cover`, scarica ciascuno in
assets/covers/<id>.jpg (<id> e' il numero gia' presente nell'URL Open
Library) e riscrive il campo `cover` delle citazioni con la copertina
scaricata e validata verso il percorso locale. Le citazioni la cui copertina
non e' stata scaricata (o non e' un'immagine Open Library riconosciuta)
restano con l'URL remoto: meglio una copertina remota che una rotta.

Rilanciabile: salta i file gia' presenti in assets/covers/ senza
riscaricarli.

Uso: python3 tools/download_covers.py
"""
import io
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request

from PIL import Image, UnidentifiedImageError

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(ROOT, 'data', 'citazioni.json')
COVERS_DIR = os.path.join(ROOT, 'assets', 'covers')

COVER_ID_RE = re.compile(r'covers\.openlibrary\.org/b/id/(\d+)-[A-Z]\.jpg$')

PAUSE_SECONDS = 1.0
MIN_SIDE_PX = 10
USER_AGENT = 'Mozilla/5.0 (compatible; sottolineature.it cover fetcher)'


def load_quotes():
    with open(DATA_PATH, encoding='utf-8') as f:
        return json.load(f)


def distinct_covers(quotes):
    """{id: url} per ogni copertina Open Library distinta referenziata."""
    by_id = {}
    for q in quotes:
        m = COVER_ID_RE.search(q.get('cover', ''))
        if m:
            by_id[m.group(1)] = q['cover']
    return by_id


def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return resp.read()


def is_valid_image(raw):
    """PIL.Image.verify() invalida l'oggetto per un uso successivo: si
    riapre da zero per leggere le dimensioni reali dopo la verifica di
    integrita'."""
    try:
        Image.open(io.BytesIO(raw)).verify()
        width, height = Image.open(io.BytesIO(raw)).size
    except (UnidentifiedImageError, OSError):
        return False
    return width >= MIN_SIDE_PX and height >= MIN_SIDE_PX


def download_one(cover_id, url):
    dest = os.path.join(COVERS_DIR, cover_id + '.jpg')
    try:
        raw = fetch(url)
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as e:
        return False, str(e)

    if not is_valid_image(raw):
        return False, 'file scaricato non e\' un\'immagine valida (placeholder o risposta vuota)'

    with open(dest, 'wb') as f:
        f.write(raw)
    return True, None


def rewrite_citazioni(local_ids):
    """Riscrive il campo cover in data/citazioni.json -> /assets/covers/<id>.jpg
    per le sole citazioni la cui copertina e' presente e valida in locale
    (scaricata ora o in un lancio precedente). Le altre restano con l'URL
    Open Library invariato."""
    with open(DATA_PATH, encoding='utf-8') as f:
        quotes = json.load(f)

    changed = 0
    for q in quotes:
        m = COVER_ID_RE.search(q.get('cover', ''))
        if m and m.group(1) in local_ids:
            local_path = '/assets/covers/' + m.group(1) + '.jpg'
            if q['cover'] != local_path:
                q['cover'] = local_path
                changed += 1

    with open(DATA_PATH, 'w', encoding='utf-8') as f:
        json.dump(quotes, f, ensure_ascii=False, indent=2)
        f.write('\n')

    return changed


def main():
    os.makedirs(COVERS_DIR, exist_ok=True)
    quotes = load_quotes()
    by_id = distinct_covers(quotes)
    ids = sorted(by_id, key=int)
    print('Copertine Open Library distinte referenziate:', len(ids))

    already, downloaded, failed = [], [], []
    for i, cover_id in enumerate(ids):
        dest = os.path.join(COVERS_DIR, cover_id + '.jpg')
        if os.path.isfile(dest):
            already.append(cover_id)
            continue
        ok, reason = download_one(cover_id, by_id[cover_id])
        if ok:
            downloaded.append(cover_id)
            print('  [%d/%d] scaricata %s' % (i + 1, len(ids), cover_id))
        else:
            failed.append((cover_id, by_id[cover_id], reason))
            print('  [%d/%d] fallita %s: %s' % (i + 1, len(ids), cover_id, reason))
        time.sleep(PAUSE_SECONDS)

    local_ids = set(already) | set(downloaded)
    changed = rewrite_citazioni(local_ids)

    print()
    print('Gia\' presenti in assets/covers/:', len(already))
    print('Scaricate ora:', len(downloaded))
    print('Fallite (restano con URL Open Library):', len(failed))
    print('Citazioni riscritte su percorso locale in data/citazioni.json:', changed)
    if failed:
        print()
        print('Elenco copertine non scaricate:')
        for cover_id, url, reason in failed:
            print('  %s (%s): %s' % (cover_id, url, reason))

    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
