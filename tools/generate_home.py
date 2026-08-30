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


def render_card(q, slug):
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

    href = '/citazioni/' + slug + '/'
    return (
        '    <article class="card" data-slug="' + html.escape(slug, quote=True) + '"' + attrs + '>\n'
        '      <span class="card-mark" aria-hidden="true">“</span>\n'
        '      <div class="card-body">\n'
        '        <p class="card-quote"><a class="card-open" href="' + href + '">' +
        html.escape(q['quote']) + '</a></p>\n'
        '        <p class="card-citation sans"><span class="card-author">' + html.escape(q['author']) +
        '</span> — <span class="card-title">' + html.escape(q['title']) + '</span>' + year_html + '</p>\n'
        '        <p class="card-hint sans">Apri la pagina</p>\n'
        '      </div>' + cover_html + '\n'
        '    </article>\n'
    )


def main():
    quotes = qp.load_quotes()

    with open(TEMPLATE_PATH, encoding='utf-8') as f:
        template = f.read()

    slugs_data = qp.load_slugs()
    slug_map = slugs_data.get('quotes', {})
    missing = [q for q in quotes if qp.quote_key(q) not in slug_map]
    if missing:
        raise SystemExit(
            'generate_home: slug mancante per %d citazioni (esegui prima '
            'generate_quote_pages). Prima: %s' % (len(missing), qp.quote_key(missing[0]))
        )
    cards_html = '\n'.join(render_card(q, slug_map[qp.quote_key(q)]) for q in quotes)
    count_words = italian_number_words(len(quotes))
    page = template.replace('{{CARDS}}', cards_html.rstrip('\n'))
    page = page.replace('{{COUNT}}', str(len(quotes)))
    page = page.replace('{{COUNT_WORDS}}', count_words[0].upper() + count_words[1:])

    # Conteggi della fascia "Esplora l'archivio": si leggono dalle cartelle
    # gia' generate, cosi' restano veri senza doverli aggiornare a mano.
    def count_pages(folder):
        d = os.path.join(qp.ROOT, folder)
        if not os.path.isdir(d):
            return 0
        return len([f for f in os.listdir(d) if f.endswith('.html') and f != 'index.html'])

    authors = len({q['author'] for q in quotes})
    for token, value in (
        ('{{N_AUTORI}}', authors),
        ('{{N_OPERE}}', count_pages('opere')),
        ('{{N_RACCOLTE}}', count_pages('raccolte')),
        ('{{N_TEMI}}', count_pages('temi')),
        ('{{N_GENERI}}', count_pages('generi')),
    ):
        page = page.replace(token, str(value))

    with open(OUT_PATH, 'w', encoding='utf-8') as f:
        f.write(page)

    print('index.html generato con', len(quotes), 'citazioni')


if __name__ == '__main__':
    main()
