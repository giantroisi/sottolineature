#!/usr/bin/env python3
"""Componente per i collegamenti affiliati Amazon Italia.

La configurazione centrale associa ogni edizione verificata a una sola opera;
le pagine dell'opera e tutte le sue citazioni ereditano lo stesso link. Senza
Tracking ID l'output resta completamente spento. Con il
Tracking ID attivo vengono accettati soltanto URL Amazon.it puliti nella forma
``/dp/ASIN/?tag=TRACKING_ID``: niente prezzi, immagini, widget o testi copiati
da Amazon.
"""
import html
import json
import os
import re
import urllib.parse


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(ROOT, 'data', 'affiliazioni.json')
ASIN_RE = re.compile(r'^[A-Z0-9]{10}$')
AMAZON_PATH_RE = re.compile(r'^/dp/([A-Z0-9]{10})/?$')
# Opere approvate esplicitamente: 5 iniziali, poi lotti di 20, 6, 11, 12, 20, 10, 18, 11 e 6 titoli nuovi.
MAX_ACTIVE_WORKS = 119

LINK_TEXT = 'Acquista su Amazon'
AMAZON_DISCLOSURE = 'In qualità di Affiliato Amazon io ricevo un guadagno dagli acquisti idonei'


def load_config():
    """Carica l'unica configurazione autorizzata per le affiliazioni."""
    with open(CONFIG_PATH, encoding='utf-8') as config_file:
        config = json.load(config_file)
    if not isinstance(config, dict):
        raise ValueError('La configurazione affiliazioni deve essere un oggetto JSON.')
    return config


def load_tracking_id(config=None):
    """Restituisce il Tracking ID centrale; vuoto significa componente spento."""
    config = load_config() if config is None else config
    return str(config.get('amazon_it_tracking_id', '')).strip()


def _verified_amazon_url(url, tracking_id, expected_asin=None):
    parsed = urllib.parse.urlparse(str(url).strip())
    if parsed.scheme != 'https' or (parsed.hostname or '').lower() not in {'amazon.it', 'www.amazon.it'}:
        raise ValueError('Il collegamento affiliato deve usare HTTPS e il dominio amazon.it.')
    if parsed.username or parsed.password or parsed.port or parsed.params or parsed.fragment:
        raise ValueError('Il collegamento Amazon contiene componenti non ammessi.')

    path_match = AMAZON_PATH_RE.fullmatch(parsed.path)
    if not path_match:
        raise ValueError('Il collegamento Amazon deve usare il percorso pulito /dp/ASIN/.')
    asin = path_match.group(1)
    if expected_asin and asin != expected_asin:
        raise ValueError("L'ASIN configurato non corrisponde all'URL Amazon.")

    query = urllib.parse.parse_qsl(parsed.query, keep_blank_values=True)
    if query != [('tag', tracking_id)]:
        raise ValueError('Il collegamento Amazon deve contenere soltanto il Tracking ID configurato.')
    return parsed.geturl()


def validated_editions(config=None):
    """Valida e restituisce le edizioni attive, indicizzate per autore e opera."""
    config = load_config() if config is None else config
    tracking_id = load_tracking_id(config)
    raw_editions = config.get('edizioni', [])
    if not isinstance(raw_editions, list):
        raise ValueError('La voce edizioni deve essere una lista.')
    if not tracking_id:
        return {}
    if len(raw_editions) > MAX_ACTIVE_WORKS:
        raise ValueError(f'Il lotto approvato consente al massimo {MAX_ACTIVE_WORKS} opere affiliate.')

    editions = {}
    for index, raw in enumerate(raw_editions, start=1):
        if not isinstance(raw, dict):
            raise ValueError(f'Edizione affiliata {index}: record non valido.')
        required = ('author', 'title', 'asin', 'amazon_url', 'amazon_title', 'format')
        missing = [field for field in required if not str(raw.get(field, '')).strip()]
        if missing:
            raise ValueError(f'Edizione affiliata {index}: campi mancanti: {", ".join(missing)}.')
        contributors = raw.get('contributors', [])
        if not contributors or any(not person.get('name') or not person.get('role') for person in contributors):
            raise ValueError(f'Edizione affiliata {index}: autore e collaboratori non verificati.')
        if raw.get('amazon_edition_verified') is not True:
            raise ValueError(f'Edizione affiliata {index}: verifica bibliografica non confermata.')
        if raw.get('prime_verified') is not True and not str(raw.get('prime_exception_reason', '')).strip():
            raise ValueError(f'Edizione affiliata {index}: Prime non verificato e nessuna eccezione motivata.')

        author = str(raw['author']).strip()
        title = str(raw['title']).strip()
        work_key = (author, title)
        if work_key in editions:
            raise ValueError(f'Opera affiliata duplicata: {author} — {title}.')
        asin = str(raw['asin']).strip().upper()
        if not ASIN_RE.fullmatch(asin):
            raise ValueError(f'ASIN non valido per {author} — {title}.')

        edition = dict(raw)
        edition['author'] = author
        edition['title'] = title
        edition['asin'] = asin
        edition['amazon_url'] = _verified_amazon_url(raw['amazon_url'], tracking_id, asin)
        editions[work_key] = edition
    return editions


def edition_for_record(record, config=None):
    """Trova l'edizione approvata, senza dedurre associazioni bibliografiche."""
    config = load_config() if config is None else config
    if not load_tracking_id(config):
        return None

    author = str(record.get('author', '')).strip()
    titles = {str(record.get('title', '')).strip()}
    titles.update(str(title).strip() for title in record.get('titles', []) if str(title).strip())
    editions = validated_editions(config)
    edition = None
    for title in titles:
        edition = editions.get((author, title))
        if edition:
            break
    return edition


def render_amazon_button(record, config=None):
    """Pulsante locale con il testo richiesto e la stessa destinazione ovunque."""
    edition = edition_for_record(record, config)
    if not edition:
        return ''
    url = edition['amazon_url']
    cart_icon = (
        '<svg class="affiliate-cart" aria-hidden="true" viewBox="0 0 24 24" '
        'width="22" height="22"><path d="M3 4h2l2.2 10.1a2 2 0 0 0 2 1.6h7.9a2 2 0 0 0 1.9-1.4L21 8H7" '
        'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
        'stroke-linejoin="round"/><circle cx="10" cy="19" r="1.5" fill="currentColor"/>'
        '<circle cx="18" cy="19" r="1.5" fill="currentColor"/></svg>'
    )
    return (
        '<a class="affiliate-link" href="' + html.escape(url, quote=True) + '" '
        'target="_blank" rel="sponsored nofollow noopener" '
        'aria-label="' + LINK_TEXT + ' — link affiliato">' + cart_icon
        + '<span class="affiliate-button-text"><span>' + LINK_TEXT + '</span>'
        + '<span class="affiliate-button-disclosure">link affiliato</span></span></a>'
    )


def render_amazon_link(record, config=None):
    """Scheda bibliografica dell'edizione disponibile, prima del pulsante."""
    edition = edition_for_record(record, config)
    if not edition:
        return ''
    byline = ', '.join(html.escape(person['name']) + ' (' + html.escape(person['role']) + ')'
                       for person in edition['contributors'])
    return (
        '<aside class="affiliate-card sans" aria-label="Edizione disponibile su Amazon">'
        '<p class="affiliate-edition-title">' + html.escape(edition['amazon_title']) + '</p>'
        '<p class="affiliate-edition-byline">di ' + byline + '</p>'
        '<p class="affiliate-edition-format">Formato: ' + html.escape(edition['format']) + '</p>'
        + render_amazon_button(record, config)
        + '</aside>'
    )


def render_affiliate_footer(config=None):
    """Dichiarazione centralizzata, pubblicata nel footer di ogni pagina."""
    if not load_tracking_id(config):
        return ''
    return '<p class="affiliate-disclosure">' + AMAZON_DISCLOSURE + '.</p>'


def collection_edition_record(items, config=None):
    """Un solo classico presente nella raccolta; preferisce quello piu' rappresentato."""
    editions = validated_editions(config)
    counts = {}
    representatives = {}
    for _, quote in items:
        key = (quote['author'], quote['title'])
        if key in editions:
            counts[key] = counts.get(key, 0) + 1
            representatives[key] = quote
    if not counts:
        return None
    # L'ordine dei dati centrali risolve i pari merito in modo riproducibile.
    best = max((key for key in editions if key in counts), key=lambda key: counts[key])
    return representatives[best]
