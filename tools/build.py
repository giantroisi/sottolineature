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
import generate_quote_pages as qp  # noqa: E402
import generate_hub_pages as hp  # noqa: E402
import generate_og_images as og  # noqa: E402


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


def main():
    qp_entries = qp.main()
    hp_entries, author_slugs, tema_slugs, genere_slugs = hp.main()

    sitemap_path = os.path.join(qp.ROOT, 'sitemap.xml')
    with open(sitemap_path, 'w', encoding='utf-8') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        f.write('  <url><loc>' + qp.SITE_URL + '/</loc></url>\n')
        f.write('  <url><loc>' + qp.SITE_URL + '/metodo/</loc></url>\n')
        for slug, _ in qp_entries:
            f.write('  <url><loc>' + qp.SITE_URL + '/citazioni/' + slug + '/</loc></url>\n')
        for cat in tema_slugs:
            f.write('  <url><loc>' + qp.SITE_URL + '/temi/' + cat + '/</loc></url>\n')
        for gen in genere_slugs:
            f.write('  <url><loc>' + qp.SITE_URL + '/generi/' + gen + '/</loc></url>\n')
        for aslug in sorted(set(author_slugs.values())):
            f.write('  <url><loc>' + qp.SITE_URL + '/autori/' + aslug + '/</loc></url>\n')
        f.write('</urlset>\n')

    redirects = qp.load_redirects()
    vercel_path = write_vercel_json(redirects)

    og_generated, og_skipped, og_stray = og.generate(qp_entries)

    total = 2 + len(qp_entries) + len(tema_slugs) + len(genere_slugs) + len(set(author_slugs.values()))

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
            if '<h1 class="card-quote">' not in f.read():
                missing_h1.append(slug)

    print()
    print('--- Rapporto build.py ---')
    print('URL totali in sitemap:', total)
    print('  citazioni:', len(qp_entries))
    print('  temi:', len(tema_slugs), '| generi:', len(genere_slugs), '| autori:', len(set(author_slugs.values())))
    print('Redirect in vercel.json:', len(redirects))
    print('Title <title> duplicati fra pagine citazione:', len(dup_titles))
    print('Meta description duplicate fra pagine citazione:', len(dup_descriptions))
    print('Pagine citazione senza <h1>:', len(missing_h1))
    print('Immagini OG generate:', og_generated, '| gia aggiornate:', og_skipped, '| totale attese:', len(qp_entries))
    print('vercel.json scritto in', vercel_path)
    print('sitemap aggiornata in', sitemap_path)

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

    if og_stray:
        print('ATTENZIONE: file OG orfani in assets/og (citazione rimossa/slug cambiato):', og_stray)


if __name__ == '__main__':
    main()
