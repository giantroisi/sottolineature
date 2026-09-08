#!/usr/bin/env python3
"""Rigenera tutte le pagine derivate da index.html: citazioni, temi, generi,
autori, la sitemap.xml unificata e vercel.json (redirect inclusi). Unico entry
point da lanciare dopo aver modificato index.html.

Uso: python3 tools/build.py
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import generate_home as gh  # noqa: E402
import check_links
import controlla_jsonld
import generate_mine_page as mine
import generate_quote_pages as qp  # noqa: E402
import generate_hub_pages as hp  # noqa: E402
import generate_opera_pages as op  # noqa: E402
import generate_raccolte_pages as rp  # noqa: E402
import generate_og_images as og  # noqa: E402
import generate_index_pages as ip  # noqa: E402
import generate_feed as feed  # noqa: E402
import generate_404 as nf  # noqa: E402


HOST_REDIRECTS = [
    {
        "source": "/:path*",
        "has": [{"type": "host", "value": "www.sottolineature.it"}],
        "destination": "https://sottolineature.it/:path*",
        "permanent": True,
    },
    {
        "source": "/:path*",
        "has": [{"type": "host", "value": "sottolineature.vercel.app"}],
        "destination": "https://sottolineature.it/:path*",
        "permanent": True,
    },
]


def write_vercel_json(redirects):
    path = os.path.join(qp.ROOT, 'vercel.json')
    slug_redirects = [
        {"source": r['from'], "destination": r['to'], "permanent": True}
        for r in redirects
    ]
    config = {
        "cleanUrls": True,
        "trailingSlash": True,
        # Ordine voluto: prima l'host canonico (via a prescindere dal path),
        # poi gli slug cambiati. Vercel applica il primo redirect che
        # corrisponde, quindi l'host va valutato prima dei path specifici.
        "redirects": HOST_REDIRECTS + slug_redirects,
        "headers": [
            {
                "source": "/assets/(.*)",
                "headers": [
                    {"key": "Cache-Control", "value": "public, max-age=31536000, immutable"}
                ],
            },
            {
                "source": "/:path*",
                "has": [{"type": "host", "value": "sottolineature.vercel.app"}],
                "headers": [{"key": "X-Robots-Tag", "value": "noindex"}],
            },
            {
                "source": "/:path*",
                "has": [{"type": "host", "value": "www.sottolineature.it"}],
                "headers": [{"key": "X-Robots-Tag", "value": "noindex"}],
            },
        ],
    }
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
        f.write('\n')
    return path


def stamp_assets():
    """Aggiunge ?v=<hash> ai riferimenti di site.css, share.js, nav.js e home-resto.js.

    vercel.json serve /assets/* con Cache-Control immutable per un anno: senza
    un'impronta nell'URL il browser di chi ha gia' visitato il sito continua a
    usare la versione vecchia del foglio di stile *per un anno*, e la pagina si
    rompe (e' successo il 2026-08-30: intestazione scomposta, pillole tornate
    link, etichette nascoste diventate visibili). Con l'impronta, ogni modifica
    genera un URL nuovo e la cache si aggiorna da sola.
    """
    import hashlib
    import re
    fingerprints = {}
    for name in ('site.css', 'share.js', 'nav.js', 'home-resto.js'):
        path = os.path.join(qp.ROOT, 'assets', name)
        if os.path.exists(path):
            with open(path, 'rb') as f:
                fingerprints[name] = hashlib.md5(f.read()).hexdigest()[:8]
    pattern = re.compile(r'(/assets/(site\.css|share\.js|nav\.js|home-resto\.js))(\?v=[0-9a-f]+)?')

    def replace(match):
        return match.group(1) + '?v=' + fingerprints.get(match.group(2), '0')

    skip = ('.git', 'node_modules', 'archivio', 'templates', 'tools', 'assets')
    touched = 0
    for dirpath, dirnames, filenames in os.walk(qp.ROOT):
        dirnames[:] = [d for d in dirnames if d not in skip]
        for filename in filenames:
            if not filename.endswith('.html'):
                continue
            full = os.path.join(dirpath, filename)
            with open(full, encoding='utf-8') as f:
                before = f.read()
            after = pattern.sub(replace, before)
            if after != before:
                with open(full, 'w', encoding='utf-8') as f:
                    f.write(after)
                touched += 1
    return fingerprints, touched


def main():
    # L'elenco opere->citazioni serve prima di renderizzare le pagine
    # citazione (Book @id condiviso, link "tutte le citazioni da quest'opera").
    # Basta assegnare gli slug in anteprima, senza serializzare nulla: qp.main()
    # rifa' l'assegnazione (idempotente) e scrive slugs.json se necessario.
    preview_entries, _ = qp.assign_slugs(qp.load_quotes(), qp.load_slugs(), qp.load_redirects())
    opere = op.load_opere()
    raccolte = rp.load_raccolte()
    opera_map = op.build_opera_map(preview_entries, opere)
    raccolta_map = rp.build_raccolta_map(preview_entries, raccolte)

    qp_entries = qp.main(opera_map, raccolta_map)
    # gh.main() legge slugs.json da disco: va lanciato solo dopo che qp.main()
    # l'ha persistito, altrimenti fallisce su ogni citazione appena aggiunta
    # (slug ancora assente su disco).
    gh.main()
    op_status = op.main(qp_entries)
    rc_status = rp.main(qp_entries)
    raccolta_keys = {k for r in raccolte for k in r['quote_keys']}
    hp_entries, author_slugs, tema_status, genere_status, author_status = hp.main(opere)
    citazioni_index_urls = ip.main(qp_entries, author_slugs, tema_status, genere_status, opere, op_status, raccolte, rc_status)
    feed_path = feed.main(qp_entries)
    mine.main()
    nf.main(qp_entries, author_slugs, opere, raccolte)

    indexable_temi = [c for c, ok in tema_status.items() if ok]
    indexable_generi = [g for g, ok in genere_status.items() if ok]
    indexable_autori = sorted(a for a, ok in author_status.items() if ok)
    hub_below_threshold = (
        [c for c, ok in tema_status.items() if not ok] +
        [g for g, ok in genere_status.items() if not ok] +
        [a for a, ok in author_status.items() if not ok]
    )

    # La sitemap si costruisce prima come lista, poi si scrive: il rapporto di
    # fine build conta questa lista invece di ricalcolare la stessa somma a
    # mano. Il conteggio scritto a mano era gia' andato fuori sincrono una
    # volta (mancava /privacy/, aggiunta alla sitemap e mai al totale): un
    # numero che si deriva da cio' che e' stato scritto non puo' sbagliare.
    #
    # La sitemap e' divisa per tipo di pagina, e sitemap.xml e' l'indice che
    # le elenca (stessa struttura di dietroiltesto). Non e' cosmesi: in Search
    # Console il rapporto Sitemap mostra "rilevate / indicizzate" *per singolo
    # file*, quindi separando i tipi si legge quali pagine Google tiene
    # davvero. Con un file solo da 1.244 URL quel numero e' un totale muto.
    # Serve a rispondere alla domanda aperta dell'8 settembre: delle ~107
    # indicizzate, quante sono hub (autori, opere, raccolte) e quante foglie?
    # Vedi 05-INDICIZZAZIONE nel progetto SEO.
    citazioni_urls = []
    for slug, q in qp_entries:
        lastmod = ('<lastmod>' + q['added'] + '</lastmod>') if q.get('added') else ''
        citazioni_urls.append(('/citazioni/' + slug + '/', lastmod))

    sitemap_groups = [
        ('sitemap-pagine.xml', [
            ('/', ''), ('/metodo/', ''), ('/privacy/', ''),
            ('/autori/', ''), ('/temi/', ''), ('/generi/', ''),
            ('/opere/', ''), ('/raccolte/', ''),
        ]),
        ('sitemap-citazioni.xml', citazioni_urls),
        ('sitemap-indice-citazioni.xml', [(href, '') for href in citazioni_index_urls]),
        ('sitemap-autori.xml', [('/autori/' + a + '/', '') for a in indexable_autori]),
        ('sitemap-opere.xml', [('/opere/' + o + '/', '') for o in op_status]),
        ('sitemap-raccolte.xml', [('/raccolte/' + r + '/', '') for r in rc_status]),
        ('sitemap-temi-generi.xml', (
            [('/temi/' + c + '/', '') for c in indexable_temi] +
            [('/generi/' + g + '/', '') for g in indexable_generi]
        )),
    ]
    sitemap_urls = [u for _, urls in sitemap_groups for u in urls]

    for filename, urls in sitemap_groups:
        with open(os.path.join(qp.ROOT, filename), 'w', encoding='utf-8') as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
            for href, lastmod in urls:
                f.write('  <url><loc>' + qp.SITE_URL + href + '</loc>' + lastmod + '</url>\n')
            f.write('</urlset>\n')

    sitemap_path = os.path.join(qp.ROOT, 'sitemap.xml')
    with open(sitemap_path, 'w', encoding='utf-8') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for filename, _ in sitemap_groups:
            f.write('  <sitemap><loc>' + qp.SITE_URL + '/' + filename + '</loc></sitemap>\n')
        f.write('</sitemapindex>\n')

    redirects = qp.load_redirects()
    vercel_path = write_vercel_json(redirects)

    og_generated, og_skipped, og_stray = og.generate(qp_entries)

    total_indexable = len(sitemap_urls)
    total_pages = total_indexable + len(hub_below_threshold)

    # --- Controlli di qualita: title/description duplicati, H1 presente ---
    title_tags = {}
    description_tags = {}
    for slug, q in qp_entries:
        incipit, _ = qp.truncate_words(q['quote'], 45)
        t = '«' + incipit + '» — ' + q['author'] + ', ' + q['title']
        title_tags.setdefault(t, []).append(slug)

        ref = q['title'] + (', ' + q['year'] if q['year'] else '')
        d = '«' + q['quote'] + '» — ' + q['author'] + ', ' + ref
        if len(d) > 200:
            d = d[:197].rsplit(' ', 1)[0] + '…'
        description_tags.setdefault(d, []).append(slug)

    dup_titles = {t: s for t, s in title_tags.items() if len(s) > 1}
    dup_descriptions = {d: s for d, s in description_tags.items() if len(s) > 1}

    missing_h1 = []
    for slug, _ in qp_entries:
        path = os.path.join(qp.OUT_DIR, slug + '.html')
        with open(path, encoding='utf-8') as f:
            if '<h1 class="quote-h1">' not in f.read():
                missing_h1.append(slug)

    quotes_with_source = sum(1 for _, q in qp_entries if q.get('source_edition') or q.get('source_locus'))
    dated = sum(1 for _, q in qp_entries if q.get('added'))

    covers_local = sum(1 for _, q in qp_entries if q.get('cover', '').startswith('/assets/covers/'))
    covers_remote = sum(1 for _, q in qp_entries if q.get('cover', '').startswith('http'))

    # Stessa trappola gia' vista con i contesti duplicati (Fase 1 LOG.md):
    # una fonte scritta per una citazione puo' finire applicata per errore
    # anche a un'altra citazione dello STESSO autore/opera. Il controllo e'
    # scoperto apposta su (autore, opera, locus): un locus generico come
    # "incipit" o "ultime righe del romanzo" e' legittimo su decine di libri
    # diversi, il problema e' solo se si ripete due volte sulla stessa opera.
    source_texts = {}
    dup_sources = {}
    for slug, q in qp_entries:
        locus = q.get('source_locus', '')
        if not locus:
            continue
        key = (q['author'], q['title'], locus)
        source_texts.setdefault(key, []).append(slug)
    for key, slugs in source_texts.items():
        if len(slugs) > 1:
            dup_sources[key] = slugs

    print()
    fingerprints, stamped = stamp_assets()

    # Controllo di integrita' del sito appena generato. Non blocca il build:
    # stampa cosa ha trovato, cosi' chi lancia il comando lo vede subito
    # invece di scoprirlo mesi dopo da un utente.
    print()
    link_problems = check_links.main()
    print()
    # I dati strutturati sono l'unica parte del sito che non si vede
    # guardandola: un valore invalido non rompe niente a schermo, sparisce
    # solo il risultato arricchito su Google. Quindi si controlla a ogni
    # build, come i link.
    jsonld_problems = controlla_jsonld.main()
    print()

    print('--- Rapporto build.py ---')
    print('Impronta sugli asset:', ', '.join(n + '=' + h for n, h in sorted(fingerprints.items())),
          '(' + str(stamped) + ' pagine aggiornate)')
    print('URL totali generati (indicizzabili + noindex):', total_pages)
    print('URL indicizzabili (in sitemap):', total_indexable, '(differenza:', total_pages - total_indexable, 'hub sotto soglia, vedi sotto)')
    print('  citazioni:', len(qp_entries), '| indice /citazioni/:', len(citazioni_index_urls), 'pagine')
    print('  temi:', len(indexable_temi), '/', len(tema_status), '| generi:', len(indexable_generi), '/', len(genere_status),
          '| autori:', len(indexable_autori), '/', len(author_status), '| opere:', len(op_status), '| raccolte:', len(rc_status), '/', len(raccolte))
    print('Hub sotto soglia (< 3 citazioni, noindex,follow ma linkati):', len(hub_below_threshold))
    print('Redirect in vercel.json:', len(redirects))
    print('Title <title> duplicati fra pagine citazione:', len(dup_titles))
    print('Meta description duplicate fra pagine citazione:', len(dup_descriptions))
    print('Pagine citazione senza <h1>:', len(missing_h1))
    print('Citazioni con data di aggiunta nota (<lastmod>/feed.xml):', dated, '/', len(qp_entries))
    print('Citazioni con blocco fonte:', quotes_with_source, '/', len(qp_entries), '| fonti duplicate su citazioni diverse:', len(dup_sources))
    print('Immagini OG generate:', og_generated, '| gia aggiornate:', og_skipped, '| totale attese:', len(qp_entries))
    print('Copertine locali (assets/covers/):', covers_local, '| ancora remote (Open Library):', covers_remote)

    # Copertura delle raccolte. E' il passaggio della lista di chiusura (punto 10)
    # che salta piu' spesso: e' l'unico che non rompe niente se lo si dimentica —
    # la citazione esce, la pagina e' valida, e l'unica traccia e' una percentuale
    # che scende in silenzio. E' gia' successo tre volte: ad agosto le raccolte
    # sono rimaste a 234 citazioni su 749, e fra il 6 e l'8 settembre la copertura
    # e' scesa dall'85% al 67% mentre l'archivio cresceva di 65 citazioni. Da qui
    # in avanti ogni build la dice, e chi aggiunge citazioni senza collocarle la
    # vede scendere sotto gli occhi.
    in_raccolta = sum(1 for _, q in qp_entries if rp.quote_key(q) in raccolta_keys)
    perc = round(100 * in_raccolta / len(qp_entries)) if qp_entries else 0
    print('Citazioni in almeno una raccolta:', in_raccolta, '/', len(qp_entries),
          '=', str(perc) + '%', '(sotto l\'80% vuol dire che il punto 10 e\' stato saltato)')
    print('vercel.json scritto in', vercel_path)
    print('sitemap aggiornata in', sitemap_path)
    for filename, urls in sitemap_groups:
        print('   ', filename, len(urls), 'URL')
    print('feed.xml scritto in', feed_path)

    missing_og = [slug for slug, _ in qp_entries if not os.path.isfile(os.path.join(og.OUT_DIR, slug + '.png'))]

    if dup_titles or missing_h1 or missing_og:
        print()
        print('ERRORE: build non valido.')
        for t, slugs in dup_titles.items():
            print('  title duplicato su', slugs, ':', t[:80])
        for slug in missing_h1:
            print('  H1 mancante:', slug)
        for slug in missing_og:
            print('  Immagine OG mancante:', slug)
        raise SystemExit(1)

    if dup_sources:
        # Avviso, non blocco: due citazioni diverse dello stesso capitolo
        # (es. due passaggi della stessa scena) sono legittime. Da
        # controllare a mano che non sia il bug delle fonti copiaincollate.
        print('ATTENZIONE: stesso locus su piu citazioni della stessa opera, verificare a mano:')
        for key, slugs in dup_sources.items():
            print('  ', key, '->', slugs)

    if og_stray:
        print('ATTENZIONE: file OG orfani in assets/og (citazione rimossa/slug cambiato):', og_stray)


if __name__ == '__main__':
    main()
