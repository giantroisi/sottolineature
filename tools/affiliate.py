#!/usr/bin/env python3
"""Componente per i futuri collegamenti affiliati Amazon Italia.

Il componente resta completamente spento finche' `amazon_it_tracking_id` e'
vuoto. Anche dopo l'attivazione rende un collegamento soltanto quando la
singola edizione e' stata verificata e l'URL Amazon contiene esattamente il
Tracking ID configurato. Prezzi, immagini e testi commerciali non fanno parte
del componente: la scheda resta un semplice collegamento contestuale.
"""
import html
import json
import os
import urllib.parse


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(ROOT, 'data', 'affiliazioni.json')

LINK_TEXT = 'Consulta questa edizione su Amazon'
LINK_NOTICE = 'Link affiliato: potremmo ricevere una commissione senza costi aggiuntivi per te'
AMAZON_DISCLOSURE = 'In qualità di Affiliato Amazon io ricevo un guadagno dagli acquisti idonei'


def load_tracking_id():
    """Restituisce il Tracking ID centrale; vuoto significa componente spento."""
    with open(CONFIG_PATH, encoding='utf-8') as config_file:
        config = json.load(config_file)
    return str(config.get('amazon_it_tracking_id', '')).strip()


def _verified_amazon_url(url, tracking_id):
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme != 'https' or (parsed.hostname or '').lower() not in {'amazon.it', 'www.amazon.it'}:
        raise ValueError('Il collegamento affiliato deve usare HTTPS e il dominio amazon.it.')
    tags = urllib.parse.parse_qs(parsed.query, keep_blank_values=True).get('tag', [])
    if tags != [tracking_id]:
        raise ValueError('Il collegamento Amazon non contiene il Tracking ID configurato.')
    return url


def render_amazon_link(record, tracking_id=None):
    """Rende la scheda soltanto per un'edizione certa e un link ufficiale.

    I dati editoriali possono in futuro usare i campi `amazon_url` e
    `amazon_edition_verified`. Nessuno dei due da solo basta: senza Tracking ID
    centrale, oppure con edizione non verificata, l'output e' sempre vuoto.
    Il parametro `tracking_id` serve ai test; in produzione si legge soltanto
    la configurazione centrale.
    """
    configured_id = load_tracking_id() if tracking_id is None else str(tracking_id).strip()
    if not configured_id:
        return ''
    if not record.get('amazon_edition_verified'):
        return ''
    url = str(record.get('amazon_url', '')).strip()
    if not url:
        return ''
    url = _verified_amazon_url(url, configured_id)
    return (
        '<aside class="affiliate-card sans" aria-label="Collegamento affiliato">'
        '<a class="affiliate-link" href="' + html.escape(url, quote=True) + '" '
        'target="_blank" rel="sponsored nofollow noopener">' + LINK_TEXT + '</a>'
        '<p class="affiliate-note">' + LINK_NOTICE + '</p>'
        '</aside>'
    )
