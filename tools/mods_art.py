"""Die Mods: a ban hammer coming down on a playing card stamped "BAN", watched by the three
mods (small round avatars in the background).

Writes the card straight into assets/1x/Jokers.png and assets/2x/Jokers.png at cell x=7, y=2,
plus mods_preview.png into the current directory.
"""
import os
import sys
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from food_art import render, glyph, W, H  # noqa: E402

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
CELL = (7, 2)
BG = (70, 96, 170)

FONT = {
    'B': ['##.', '#.#', '##.', '#.#', '##.'],
    'A': ['.#.', '#.#', '###', '#.#', '#.#'],
    'N': ['#.#', '###', '###', '###', '#.#'],
}


def avatar(d, cx, cy, ring, hair, skin=(240, 200, 170)):
    """Small round chat avatar of a woman: long hair framing the face, lashes, red lips."""
    d.ellipse((cx - 7, cy - 7, cx + 7, cy + 7), fill=ring)                     # avatar disc
    d.ellipse((cx - 5, cy - 5, cx + 5, cy + 6), fill=hair)                     # hair (back)
    d.rectangle((cx - 5, cy, cx + 5, cy + 6), fill=hair)                       # long hair
    d.ellipse((cx - 3, cy - 3, cx + 3, cy + 4), fill=skin)                     # face
    d.line((cx - 3, cy - 4, cx + 2, cy - 3), fill=hair)                        # fringe
    d.point((cx - 1, cy), fill=(40, 30, 40))                                   # eyes
    d.point((cx + 2, cy), fill=(40, 30, 40))
    d.point((cx - 2, cy - 1), fill=(40, 30, 40))                               # lashes
    d.point((cx + 3, cy - 1), fill=(40, 30, 40))
    d.line((cx, cy + 2, cx + 1, cy + 2), fill=(214, 60, 80))                   # lips


def mods(d):
    # the three mods watching from the background (drawn first, so the hammer is in front)
    avatar(d, 22, 11, (240, 140, 180), (110, 64, 40))
    avatar(d, 37, 9, (150, 220, 160), (240, 210, 110))
    avatar(d, 52, 11, (170, 160, 240), (40, 30, 34))
    red, red_d = (214, 48, 44), (160, 30, 30)
    paper, paper_s = (250, 248, 242), (210, 206, 214)
    # playing card lying under the hammer
    d.rounded_rectangle((22, 50, 52, 86), 3, fill=paper)
    d.rectangle((48, 52, 52, 84), fill=paper_s)
    glyph(d, ['.#.#.', '#####', '#####', '.###.', '..#..'], 25, 53, red)       # heart pip
    # red "BAN" stamp across it
    d.rectangle((25, 63, 49, 75), outline=red, width=1)
    d.rectangle((26, 64, 48, 74), outline=red_d, width=1)
    x = 28
    for ch in 'BAN':
        glyph(d, FONT[ch], x, 67, red)
        x += 6
    # ban hammer, swung down from the top right
    wood, wood_d = (186, 120, 64), (130, 80, 40)
    steel, steel_d, steel_h = (170, 176, 196), (110, 116, 140), (226, 230, 240)
    d.line((60, 8, 40, 34), fill=wood, width=4)                                # handle
    d.line((61, 10, 42, 35), fill=wood_d)
    d.polygon([(24, 28), (34, 18), (52, 36), (42, 46)], fill=steel)            # head
    d.polygon([(42, 46), (52, 36), (54, 38), (44, 48)], fill=steel_d)
    d.line((25, 28, 34, 19), fill=steel_h)
    d.polygon([(30, 31), (36, 25), (40, 29), (34, 35)], fill=red)              # band on the head
    # impact sparks
    for x0, y0, x1, y1 in ((20, 46, 17, 43), (19, 50, 16, 50), (54, 48, 57, 45)):
        d.line((x0, y0, x1, y1), fill=(255, 230, 110))


if __name__ == '__main__':
    card = render(mods, BG)
    x, y = CELL
    for scale in (1, 2):
        path = os.path.join(ROOT, 'assets', f'{scale}x', 'Jokers.png')
        sheet = Image.open(path).convert('RGBA')
        big = card.resize((W * scale, H * scale), Image.NEAREST)
        sheet.paste(big, (x * W * scale, y * H * scale))
        sheet.save(path)
    card.resize((W * 4, H * 4), Image.NEAREST).save('mods_preview.png')
