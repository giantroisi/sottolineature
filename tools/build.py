#!/usr/bin/env python3
"""Rigenera tutte le pagine derivate da index.html: citazioni, temi, generi,
autori, e la sitemap.xml unificata. Unico entry point da lanciare dopo aver
modificato index.html.

Uso: python3 tools/build.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import generate_quote_pages as qp  # noqa: E402
import generate_hub_pages as hp  # noqa: E402


def main():
    qp_entries = qp.main()
    hp_entries, author_slugs, tema_slugs, genere_slugs = hp.main()

    sitemap_path = os.path.join(qp.ROOT, 'sitemap.xml')
    with open(sitemap_path, 'w', encoding='utf-8') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        f.write('  <url><loc>' + qp.SITE_URL + '/</loc></url>\n')
        f.write('  <url><loc>' + qp.SITE_URL + '/metodo.html</loc></url>\n')
        for slug, _ in qp_entries:
            f.write('  <url><loc>' + qp.SITE_URL + '/citazioni/' + slug + '.html</loc></url>\n')
        for cat in tema_slugs:
            f.write('  <url><loc>' + qp.SITE_URL + '/temi/' + cat + '.html</loc></url>\n')
        for gen in genere_slugs:
            f.write('  <url><loc>' + qp.SITE_URL + '/generi/' + gen + '.html</loc></url>\n')
        for aslug in sorted(set(author_slugs.values())):
            f.write('  <url><loc>' + qp.SITE_URL + '/autori/' + aslug + '.html</loc></url>\n')
        f.write('</urlset>\n')

    total = 2 + len(qp_entries) + len(tema_slugs) + len(genere_slugs) + len(set(author_slugs.values()))
    print('Sitemap aggiornata:', sitemap_path, '(', total, 'URL )')


if __name__ == '__main__':
    main()
