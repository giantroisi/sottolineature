#!/usr/bin/env python3
"""Genera /feed.xml con le ultime 20 citazioni per data di aggiunta nota.
Le citazioni senza data (aggiunte prima che LOG.md tracciasse ogni lotto in
modo identificabile) non compaiono: niente date inventate."""
import html
import os

import generate_quote_pages as qp

MAX_ITEMS = 20


def build_feed(entries):
    dated = [(s, q) for s, q in entries if q.get('added')]
    dated.sort(key=lambda item: item[1]['added'], reverse=True)
    recent = dated[:MAX_ITEMS]

    items_xml = []
    for slug, q in recent:
        link = qp.SITE_URL + '/citazioni/' + slug + '/'
        title = '«' + q['quote'][:80] + ('…' if len(q['quote']) > 80 else '') + '» — ' + q['author']
        pub_date = q['added'] + 'T00:00:00Z'
        items_xml.append(
            '  <item>\n'
            '    <title>' + html.escape(title) + '</title>\n'
            '    <link>' + link + '</link>\n'
            '    <guid>' + link + '</guid>\n'
            '    <pubDate>' + pub_date + '</pubDate>\n'
            '    <description>' + html.escape(q['quote'] + ' — ' + q['author'] + ', ' + q['title']) + '</description>\n'
            '  </item>'
        )

    feed = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<rss version="2.0">\n'
        '<channel>\n'
        '  <title>Sottolineature</title>\n'
        '  <link>' + qp.SITE_URL + '/</link>\n'
        '  <description>Le ultime citazioni aggiunte a Sottolineature.</description>\n'
        '  <language>it</language>\n'
        + '\n'.join(items_xml) + '\n'
        '</channel>\n'
        '</rss>\n'
    )
    return feed, len(recent)


def main(entries):
    feed, count = build_feed(entries)
    path = os.path.join(qp.ROOT, 'feed.xml')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(feed)
    print('feed.xml scritto con', count, 'citazioni (di', len(entries), 'totali,', sum(1 for _, q in entries if q.get('added')), 'con data nota)')
    return path


if __name__ == '__main__':
    entries = qp.main()
    main(entries)
