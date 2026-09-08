"""Etichette condivise tra i generatori, piu' l'helper del breadcrumb."""

import json

CATEGORY_LABELS = {
    'vita': 'Vita',
    'amore': 'Amore',
    'coraggio': 'Coraggio',
    'liberta': 'Libertà',
    'tempo': 'Tempo',
    'solitudine': 'Solitudine',
    'verita': 'Verità',
}

GENRE_LABELS = {
    'fantasy': 'Fantasy',
    'fantascienza': 'Fantascienza',
    'distopia': 'Distopia',
    'horror': 'Horror/Gotico',
    'saggistica': 'Saggistica',
    'poesia': 'Poesia',
}


# Nome leggibile della prima cartella di un URL, usato dal breadcrumb.
SEZIONI = {
    'citazioni': 'Tutte le citazioni',
    'autori': 'Autori',
    'opere': 'Opere',
    'raccolte': 'Raccolte',
    'temi': 'Temi',
    'generi': 'Generi',
}


def grafo_con_breadcrumb(collection_page, canonical, site_url, foglia=None):
    """Avvolge una CollectionPage e il suo BreadcrumbList in un @graph.

    Le pagine citazione e opera avevano gia' il breadcrumb; hub, raccolte e
    pagine indice no. All'8 settembre 2026 erano 333 pagine su 1.244 senza.
    Il breadcrumb e' cio' che fa mostrare a Google il percorso invece
    dell'URL nudo, e soprattutto dichiara che gli hub stanno *sopra* le
    foglie: e' il segnale di gerarchia che a questo sito manca, ed e' lo
    stesso problema della home piatta. Vedi 05-INDICIZZAZIONE nel progetto
    SEO.

    Il percorso si ricava dal canonical, cosi' non va passato a mano:
      /autori/            -> Sottolineature > Autori
      /autori/dante/      -> Sottolineature > Autori > Dante Alighieri
      /citazioni/5/       -> Sottolineature > Tutte le citazioni > Pagina 5
    `foglia` serve solo a dare all'ultimo elemento il nome vero al posto
    dello slug.
    """
    pagina = dict(collection_page)
    pagina.pop('@context', None)
    parti = [x for x in canonical[len(site_url):].split('/') if x]
    voci = [{'@type': 'ListItem', 'position': 1,
             'name': 'Sottolineature', 'item': site_url + '/'}]
    if parti:
        sezione = parti[0]
        voci.append({'@type': 'ListItem', 'position': 2,
                     'name': SEZIONI.get(sezione, sezione.capitalize()),
                     'item': site_url + '/' + sezione + '/'})
        if len(parti) > 1:
            nome = foglia or ('Pagina ' + parti[1] if parti[1].isdigit() else parti[1])
            voci.append({'@type': 'ListItem', 'position': 3,
                         'name': nome, 'item': canonical})
    return json.dumps({
        '@context': 'https://schema.org',
        '@graph': [
            pagina,
            {'@type': 'BreadcrumbList', '@id': canonical + '#breadcrumb',
             'itemListElement': voci},
        ],
    }, ensure_ascii=False)
