#!/usr/bin/env python3
"""Genera index.html a partire da templates/home_template.html (la parte
fissa: header, filtri, script) e data/citazioni.json (le 256 citazioni).

Uso: python3 tools/generate_home.py
Non modificare index.html a mano: viene sovrascritto a ogni build. Per
aggiungere/modificare una citazione si edita data/citazioni.json, per
cambiare markup/stile/script fissi si edita templates/home_template.html.

Il contesto (card-context) NON viene pubblicato qui: resta esclusivo di
/citazioni/<slug>/, per non far competere la home con le pagine citazione
sullo stesso testo (Fase 2 di SEO.md).
"""
import html
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import generate_quote_pages as qp  # noqa: E402

TEMPLATE_PATH = os.path.join(qp.ROOT, 'templates', 'home_template.html')
OUT_PATH = qp.INDEX

_UNITS = ['', 'uno', 'due', 'tre', 'quattro', 'cinque', 'sei', 'sette', 'otto', 'nove']
_TEENS = ['dieci', 'undici', 'dodici', 'tredici', 'quattordici', 'quindici', 'sedici',
          'diciassette', 'diciotto', 'diciannove']
_TENS = ['', '', 'venti', 'trenta', 'quaranta', 'cinquanta', 'sessanta', 'settanta', 'ottanta', 'novanta']


def italian_number_words(n):
    """Numero cardinale in lettere italiane, 0-999 (usato per il paragrafo
    introduttivo della home: 'Duecentocinquantasei righe...')."""
    if n < 10:
        word = _UNITS[n] or 'zero'
    elif n < 20:
        word = _TEENS[n - 10]
    elif n < 100:
        tens, units = divmod(n, 10)
        word = _TENS[tens]
        if units in (1, 8):
            word = word[:-1]
        word += _UNITS[units]
    else:
        hundreds, rest = divmod(n, 100)
        word = 'cento' if hundreds == 1 else _UNITS[hundreds] + 'cento'
        if rest:
            word += italian_number_words(rest)
    if n % 10 == 3 and n > 3 and word.endswith('tre'):
        word = word[:-1] + 'é'
    return word


def render_card(q):
    attrs = ''
    if q['genre']:
        attrs += ' data-genre="' + html.escape(q['genre'], quote=True) + '"'
    attrs += ' data-category="' + html.escape(q['category'], quote=True) + '"'

    cover_html = ''
    if q['cover']:
        alt = 'Copertina di "' + q['title'] + '" di ' + q['author']
        cover_html = (
            '\n      <img class="card-cover" src="' + html.escape(q['cover'], quote=True) +
            '" alt="' + html.escape(alt, quote=True) +
            '" loading="lazy" referrerpolicy="no-referrer" onerror="this.remove()">'
        )

    year_html = ''
    if q['year']:
        year_html = ' · <span class="card-year">' + html.escape(q['year']) + '</span>'

    return (
        '    <article class="card"' + attrs + ' tabindex="0">\n'
        '      <span class="card-mark" aria-hidden="true">“</span>\n'
        '      <div class="card-body">\n'
        '        <p class="card-quote">' + html.escape(q['quote']) + '</p>\n'
        '        <p class="card-citation sans"><span class="card-author">' + html.escape(q['author']) +
        '</span> — <span class="card-title">' + html.escape(q['title']) + '</span>' + year_html + '</p>\n'
        '        <p class="card-hint sans">Clic per copiare</p>\n'
        '      </div>' + cover_html + '\n'
        '    </article>\n'
    )


def main():
    quotes = qp.load_quotes()

    with open(TEMPLATE_PATH, encoding='utf-8') as f:
        template = f.read()

    cards_html = '\n'.join(render_card(q) for q in quotes)
    count_words = italian_number_words(len(quotes))
    page = template.replace('{{CARDS}}', cards_html.rstrip('\n'))
    page = page.replace('{{COUNT}}', str(len(quotes)))
    page = page.replace('{{COUNT_WORDS}}', count_words[0].upper() + count_words[1:])

    with open(OUT_PATH, 'w', encoding='utf-8') as f:
        f.write(page)

    print('index.html generato con', len(quotes), 'citazioni')


if __name__ == '__main__':
    main()
