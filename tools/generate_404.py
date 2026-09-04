#!/usr/bin/env python3
"""Genera 404.html.

La pagina esisteva ma era un vicolo cieco: una frase e un solo link alla home.
Contava poco finche' non ci arrivava nessuno; da quando l'archivio ha cambiato
forma - citazioni tolte, opere corrette, quattordici redirect - chi ci finisce
viene da un link vecchio, e merita una via d'uscita: la ricerca, gli ingressi
principali e tre righe vere su cui inciampare.

E' generata, non scritta a mano, perche' le tre citazioni in fondo devono
essere sempre esistenti: un link morto dentro la pagina degli errori sarebbe
il colmo. check_links.py lo verificherebbe comunque, ma meglio non dargliene
l'occasione.

Uso: python3 tools/generate_404.py (chiamato da build.py)
"""
import html
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import generate_quote_pages as qp  # noqa: E402
import generate_index_pages as ip  # noqa: E402

STILE = """<style>
  .nf-lead { font-size: 1.05rem; line-height: 1.7; color: var(--ink-soft); max-width: 34rem; }
  .nf-search { display: flex; gap: 0.6rem; margin: 2rem 0 2.5rem; max-width: 32rem; }
  .nf-search input {
    flex: 1 1 auto; font-family: inherit; font-size: 1rem; color: var(--ink);
    background: var(--paper-raised); border: 1px solid var(--rule); border-radius: 8px;
    padding: 0.7rem 0.9rem;
  }
  .nf-search input:focus-visible { outline: 2px solid var(--accent); outline-offset: 1px; }
  .nf-search button {
    font-family: inherit; font-size: 0.85rem; cursor: pointer; color: var(--ink-soft);
    background: none; border: 1px solid var(--rule); border-radius: 999px; padding: 0.5rem 1.1rem;
  }
  .nf-search button:hover { border-color: var(--accent); color: var(--accent); }
  .nf-title {
    font-size: 0.72rem; letter-spacing: 0.16em; text-transform: uppercase;
    color: var(--gold); margin: 2.5rem 0 1rem; font-weight: 400;
  }
  .nf-quote { display: block; font-style: italic; line-height: 1.5; }
  .nf-meta { display: block; margin-top: 0.25rem; font-size: 0.82rem; color: var(--ink-faint); }
</style>
<meta name="robots" content="noindex,follow">
"""


def voce(href, nome, conteggio):
    return ('<li><a href="' + href + '">' + html.escape(nome) + '</a> '
            '<span class="sans" style="color:var(--ink-faint)">(' + str(conteggio) + ')</span></li>')


def main(entries=None, author_slugs=None, opere=None, raccolte=None):
    quotes = qp.load_quotes()
    if entries is None:
        entries, _ = qp.assign_slugs(quotes, qp.load_slugs(), qp.load_redirects())
    n_autori = len(author_slugs) if author_slugs else len(set(q['author'] for q in quotes))
    n_opere = len(opere) if opere else 0
    n_raccolte = len(raccolte) if raccolte else 0

    ingressi = ''.join([
        voce('/citazioni/', 'Tutte le citazioni', len(entries)),
        voce('/autori/', 'Autori', n_autori),
        voce('/temi/', 'Temi', 7),
        voce('/opere/', 'Opere', n_opere) if n_opere else '',
        voce('/raccolte/', 'Raccolte', n_raccolte) if n_raccolte else '',
    ])

    # le tre aggiunte piu' di recente: sono sempre vive, e cambiano da sole
    datate = [(s, q) for s, q in entries if (q.get('added') or '')]
    datate.sort(key=lambda x: x[1]['added'], reverse=True)
    # una sola riga per opera: tre citazioni dallo stesso libro non sono tre vie
    viste = set()
    scelte = []
    for slug, q in datate:
        chiave = (q['author'], q['title'])
        if chiave in viste:
            continue
        viste.add(chiave)
        scelte.append((slug, q))
        if len(scelte) == 3:
            break
    righe = ''
    for slug, q in scelte:
        testo = q['quote']
        if len(testo) > 130:
            testo = testo[:127].rsplit(' ', 1)[0] + '…'
        righe += ('<li><a href="/citazioni/' + slug + '/">'
                  '<span class="nf-quote">«' + html.escape(testo) + '»</span>'
                  '<span class="nf-meta sans">' + html.escape(q['author']) +
                  ' — ' + html.escape(q['title']) + '</span></a></li>')

    body = (
        '<p class="nf-lead">O forse è stata segnata in un libro sbagliato: qualche indirizzo è '
        'cambiato quando l\'archivio è stato rimesso in ordine, e i link vecchi non portano più '
        'dove portavano. Da qui si riparte.</p>\n'
        '  <form class="nf-search sans js-only" action="/" method="get" role="search" aria-label="Cerca fra le citazioni">\n'
        '    <label class="visually-hidden" for="nfSearch">Cerca fra le citazioni</label>\n'
        '    <input type="search" id="nfSearch" name="q" placeholder="Cerca per autore, parola o frase…" autocomplete="off">\n'
        '    <button type="submit">Cerca</button>\n'
        '  </form>\n'
        '  <h2 class="nf-title">Riparti da qui</h2>\n'
        '  <ul class="index-list" style="list-style:none;margin:0;padding:0;font-size:1.05rem;line-height:2.1">' + ingressi + '</ul>\n'
        '  <h2 class="nf-title">Le ultime tre righe segnate</h2>\n'
        '  <ul class="index-list" style="list-style:none;margin:0;padding:0;display:grid;gap:1.1rem">' + righe + '</ul>'
    )

    jsonld = ('{"@context":"https://schema.org","@type":"WebPage","name":"Pagina non trovata",'
              '"url":"' + qp.SITE_URL + '/404/","isPartOf":{"@type":"WebSite","@id":"'
              + qp.SITE_URL + '/#website"}}')

    ip.write_page(
        os.path.join(qp.ROOT, '404.html'),
        title_tag='Pagina non trovata — Sottolineature',
        description='La pagina che cercavi non esiste più. Cerca fra le citazioni verificate, o riparti dagli autori, dai temi e dalle raccolte.',
        canonical=qp.SITE_URL + '/404/',
        eyebrow='Errore 404',
        h1='Questa pagina non esiste',
        count_line='',
        body_html=body,
        jsonld=jsonld,
        link_rel_extra=STILE,
    )
    print('404.html generato')
    return '/404/'


if __name__ == '__main__':
    main()
