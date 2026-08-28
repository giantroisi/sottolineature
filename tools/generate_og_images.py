#!/usr/bin/env python3
"""Genera l'immagine OG (1200x630) per ogni pagina citazione, riusando la
stessa composizione (virgolette dorate, citazione in corsivo, autore in
maiuscolo, opera, logo + url) del canvas di condivisione in index.html,
adattata al formato orizzontale richiesto da Open Graph/Twitter Card.

Uso: python3 tools/generate_og_images.py
Va rilanciato dopo ogni build.py, perche' gli slug/le citazioni possono
cambiare. Scrive in assets/og/<slug>.png, salta i file gia' aggiornati
(confronta mtime del sorgente index.html) per non rigenerare tutto ad ogni
run.
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import generate_quote_pages as qp  # noqa: E402

OUT_DIR = os.path.join(qp.ROOT, 'assets', 'og')
LOGO_PATH = os.path.join(qp.ROOT, 'logo.svg')

WIDTH, HEIGHT = 1200, 630
PADDING = 70

COL_PAPER = '#f2f0eb'
COL_RULE = '#ddd9cf'
COL_GOLD = '#9c7a3c'
COL_INK = '#211f1b'
COL_INK_SOFT = '#5b564d'

FONT_SERIF = '/System/Library/Fonts/Supplemental/Iowan Old Style.ttc'
FONT_SERIF_ITALIC_INDEX = 2
FONT_SANS = '/System/Library/Fonts/Supplemental/Arial.ttf'


def serif_italic(size):
    return ImageFont.truetype(FONT_SERIF, size, index=FONT_SERIF_ITALIC_INDEX)


def sans(size):
    return ImageFont.truetype(FONT_SANS, size)


def wrap_text(draw, text, font, max_width):
    words = text.split(' ')
    lines = []
    current = ''
    for word in words:
        test = (current + ' ' + word).strip()
        if draw.textlength(test, font=font) > max_width and current:
            lines.append(current)
            current = word
        else:
            current = test
    if current:
        lines.append(current)
    return lines


def draw_tracked_text(draw, xy, text, font, fill, tracking, anchor_center_x):
    total = draw.textlength(text, font=font) + tracking * max(0, len(text) - 1)
    x = anchor_center_x - total / 2
    y = xy[1]
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill, anchor='la')
        x += draw.textlength(ch, font=font) + tracking


def render_og_image(quote, author, title, year, out_path):
    img = Image.new('RGB', (WIDTH, HEIGHT), COL_PAPER)
    draw = ImageDraw.Draw(img)

    frame = (40, 40, WIDTH - 40, HEIGHT - 40)
    draw.rectangle(frame, outline=COL_RULE, width=2)

    cx = WIDTH / 2
    max_width = WIDTH - PADDING * 2 - 60

    # --- firma in basso: url (il logo va caricato da raster, qui si usa solo
    # il testo per restare autonomi da un rasterizzatore SVG) ---
    url_font = sans(20)
    url_baseline_top = HEIGHT - 40 - 46
    draw_tracked_text(draw, (0, url_baseline_top), 'SOTTOLINEATURE.IT', url_font, COL_GOLD, 4, cx)
    brand_top = url_baseline_top

    area_top = 40 + 46
    area_bottom = brand_top - 30

    # opera (titolo, anno)
    work = title + (' · ' + year if year else '')
    work_font = serif_italic(20)
    work_lines = wrap_text(draw, work, work_font, max_width)[:2]
    work_line_height = 26
    work_height = (len(work_lines) - 1) * work_line_height

    # autore
    author_text = author.upper()
    author_tracking = 4
    author_size = 19
    author_font = sans(author_size)
    while author_size > 13:
        author_font = sans(author_size)
        total = draw.textlength(author_text, font=author_font) + author_tracking * max(0, len(author_text) - 1)
        if total <= max_width:
            break
        author_size -= 1

    quote_to_author_gap = 34
    author_to_work_gap = 22
    attribution_height = quote_to_author_gap + author_size + author_to_work_gap + work_height

    mark_size = 64
    mark_gap = 14

    sizes = [46, 42, 38, 34, 30, 26, 23, 20]
    chosen_lines = []
    chosen_size = sizes[-1]
    line_height = 0
    max_text_height = (area_bottom - area_top) - mark_size - mark_gap - attribution_height
    for size in sizes:
        font = serif_italic(size)
        lines = wrap_text(draw, quote, font, max_width)
        line_height = round(size * 1.42)
        if len(lines) * line_height <= max_text_height or size == sizes[-1]:
            chosen_lines = lines
            chosen_size = size
            break

    text_height = len(chosen_lines) * line_height
    group_height = mark_size + mark_gap + text_height + attribution_height
    group_top = area_top + ((area_bottom - area_top) - group_height) / 2

    # virgolette
    mark_font = ImageFont.truetype('/System/Library/Fonts/Supplemental/Georgia.ttf', mark_size)
    draw.text((cx, group_top), '“', font=mark_font, fill=COL_GOLD, anchor='ma')

    # testo citazione
    quote_font = serif_italic(chosen_size)
    text_y = group_top + mark_size + mark_gap
    for line in chosen_lines:
        draw.text((cx, text_y), line, font=quote_font, fill=COL_INK, anchor='ma')
        text_y += line_height

    # autore
    quote_bottom = group_top + mark_size + mark_gap + text_height
    author_y = quote_bottom + quote_to_author_gap
    draw_tracked_text(draw, (0, author_y), author_text, author_font, COL_INK, author_tracking, cx)

    # opera
    work_font_draw = serif_italic(20)
    work_y = author_y + author_size + author_to_work_gap
    for line in work_lines:
        draw.text((cx, work_y), line, font=work_font_draw, fill=COL_INK_SOFT, anchor='ma')
        work_y += work_line_height

    img.save(out_path, 'PNG')


def generate(entries):
    """entries: lista di (slug, q) come restituita da generate_quote_pages.main().
    Ritorna (generated, skipped, stray) per il rapporto di build.py."""
    os.makedirs(OUT_DIR, exist_ok=True)

    data_mtime = os.path.getmtime(qp.DATA_PATH)
    generated = 0
    skipped = 0
    for slug, q in entries:
        out_path = os.path.join(OUT_DIR, slug + '.png')
        if os.path.exists(out_path) and os.path.getmtime(out_path) >= data_mtime:
            skipped += 1
            continue
        render_og_image(q['quote'], q['author'], q['title'], q['year'], out_path)
        generated += 1

    expected = {slug + '.png' for slug, _ in entries}
    on_disk = set(os.listdir(OUT_DIR))
    stray = sorted(on_disk - expected)

    return generated, skipped, stray


def main():
    quotes = qp.load_quotes()

    slugs_data = qp.load_slugs()
    redirects = qp.load_redirects()
    entries, changed = qp.assign_slugs(quotes, slugs_data, redirects)
    if changed:
        qp.save_slugs(slugs_data)
        qp.save_redirects(redirects)

    generated, skipped, stray = generate(entries)
    print('Immagini OG generate:', generated, '| gia aggiornate (saltate):', skipped, '| totale attese:', len(entries))
    if stray:
        print('ATTENZIONE: file OG orfani in assets/og (citazione rimossa/slug cambiato):', stray)


if __name__ == '__main__':
    main()
