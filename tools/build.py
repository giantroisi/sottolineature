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
            }
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

    total = 2 + len(qp_entries) + len(tema_slugs) + len(genere_slugs) + len(set(author_slugs.values()))

    # --- Controlli di qualita (Fase 0): title duplicati fra le pagine citazione ---
    title_tags = {}
    for slug, q in qp_entries:
        t = q['author'] + ' — ' + q['title']
        title_tags.setdefault(t, []).append(slug)
    dup_titles = {t: s for t, s in title_tags.items() if len(s) > 1}

    print()
    print('--- Rapporto build.py ---')
    print('URL totali in sitemap:', total)
    print('  citazioni:', len(qp_entries))
    print('  temi:', len(tema_slugs), '| generi:', len(genere_slugs), '| autori:', len(set(author_slugs.values())))
    print('Redirect in vercel.json:', len(redirects))
    print('Title <title> duplicati fra pagine citazione (stesso autore+opera, atteso finche\' non c\'e\' un H1 distintivo):', len(dup_titles))
    print('vercel.json scritto in', vercel_path)
    print('sitemap aggiornata in', sitemap_path)


if __name__ == '__main__':
    main()
