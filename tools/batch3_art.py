"""Pixel art for Bierbrunnen, Jochen, UDK Abschlussarbeit and the bosses Die Kammer / ADHS.

Run from any directory: writes batch3_jokers_1x.png (3 cards), batch3_blinds_1x.png
(2 rows x 21 frames of 34x34) and batch3_preview.png into the current directory.
"""
import os
import sys
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from food_art import render, glyph, W, H  # noqa: E402
from batch2_art import VANILLA, DARK, blind_strip  # noqa: E402


# --- jokers ------------------------------------------------------------------------------
def bierbrunnen(d):
    glass, glass_h = (214, 232, 240), (250, 252, 255)
    beer, beer_d, foam = (246, 176, 40), (214, 132, 22), (255, 250, 236)
    chrome, chrome_d = (200, 206, 216), (130, 138, 152)
    d.rectangle((22, 76, 49, 84), fill=chrome_d)                               # base
    d.rectangle((24, 74, 47, 78), fill=chrome)
    d.rounded_rectangle((26, 12, 45, 75), 4, fill=glass)                       # glass tower
    d.rectangle((28, 22, 43, 73), fill=beer)                                   # beer
    d.rectangle((39, 22, 43, 73), fill=beer_d)
    d.rectangle((28, 16, 43, 22), fill=foam)                                   # foam head
    for x, y in ((31, 30), (35, 41), (32, 52), (37, 60), (33, 67), (36, 26)):  # bubbles
        d.point((x, y), fill=(255, 226, 140))
    d.rectangle((28, 14, 29, 72), fill=glass_h)                                # glass shine
    d.rectangle((24, 10, 47, 13), fill=chrome)                                 # top cap
    d.rectangle((33, 7, 38, 10), fill=chrome_d)
    d.rectangle((45, 60, 54, 63), fill=chrome)                                 # tap arm
    d.rectangle((51, 57, 54, 66), fill=chrome_d)
    d.rectangle((50, 49, 55, 57), fill=(40, 40, 48))                           # tap handle
    d.rectangle((52, 67, 53, 72), fill=beer)                                   # pour
    d.rectangle((47, 72, 58, 84), fill=glass)                                  # glass below tap
    d.rectangle((48, 75, 57, 83), fill=beer)
    d.rectangle((48, 73, 57, 75), fill=foam)


def jochen(d):
    skin, skin_s = (238, 194, 156), (208, 162, 122)
    suit, suit_s, shirt, tie = (60, 66, 84), (42, 46, 62), (246, 246, 250), (160, 30, 44)
    d.polygon([(13, 85), (17, 66), (29, 61), (43, 61), (55, 66), (59, 85)], fill=suit)  # suit
    d.polygon([(29, 61), (36, 76), (43, 61)], fill=shirt)                      # shirt
    d.polygon([(34, 63), (38, 63), (39, 74), (36, 78), (33, 74)], fill=tie)   # tie
    d.line((29, 61, 33, 72), fill=suit_s)                                      # lapels
    d.line((43, 61, 39, 72), fill=suit_s)
    d.rectangle((31, 55, 41, 62), fill=skin_s)                                 # neck
    d.ellipse((21, 36, 25, 45), fill=skin_s)                                   # ears
    d.ellipse((46, 36, 50, 45), fill=skin_s)
    d.ellipse((23, 22, 48, 58), fill=skin)                                     # face
    d.rectangle((43, 30, 47, 52), fill=skin_s)
    d.pieslice((22, 18, 49, 40), 180, 360, fill=(110, 90, 70))                 # side-parted hair
    d.rectangle((22, 28, 25, 34), fill=(110, 90, 70))
    d.line((30, 19, 26, 29), fill=(150, 126, 100))                             # parting
    d.rectangle((26, 38, 33, 43), outline=(30, 30, 36))                        # glasses
    d.rectangle((38, 38, 45, 43), outline=(30, 30, 36))
    d.line((34, 40, 37, 40), fill=(30, 30, 36))
    d.rectangle((29, 40, 30, 41), fill=DARK)                                   # eyes
    d.rectangle((41, 40, 42, 41), fill=DARK)
    d.rectangle((35, 44, 36, 48), fill=skin_s)                                 # nose
    d.line((32, 52, 39, 52), fill=(160, 90, 80))                               # mouth
    d.rounded_rectangle((44, 66, 57, 83), 1, fill=(70, 74, 86))                # calculator
    d.rectangle((46, 68, 55, 71), fill=(170, 210, 150))
    for y in (73, 76, 79):
        for x in (46, 49, 52, 55):
            d.point((x, y), fill=(220, 220, 228))


def udk_abschlussarbeit(d):
    cover, cover_s, gold = (36, 52, 104), (24, 34, 72), (240, 200, 70)
    d.polygon([(16, 24), (50, 18), (56, 76), (22, 82)], fill=cover_s)          # thesis (spine shadow)
    d.polygon([(18, 22), (52, 16), (56, 72), (22, 78)], fill=cover)
    d.polygon([(52, 16), (55, 18), (58, 73), (56, 72)], fill=(236, 232, 220))  # pages
    d.line((20, 23, 24, 78), fill=(70, 90, 150))                               # binding
    glyph(d, ['#..#.###..#..#', '#..#.#..#.#.#.', '#..#.#..#.##..', '#..#.#..#.#.#.', '####.###..#..#'],
          25, 27, gold)                                                        # "UDK"
    d.line((26, 34, 47, 31), fill=gold)
    # ace of spades on the cover
    d.rectangle((29, 41, 46, 66), fill=(250, 250, 246))
    d.polygon([(37, 46), (32, 53), (34, 56), (37, 54), (40, 56), (42, 53)], fill=DARK)
    d.polygon([(37, 54), (35, 60), (39, 60)], fill=DARK)
    glyph(d, ['.#.', '#.#', '###', '#.#'], 30, 42, (200, 30, 30))              # "A"
    # graduation cap on top
    d.polygon([(30, 12), (44, 8), (56, 12), (42, 16)], fill=(30, 30, 36))
    d.rectangle((36, 13, 48, 16), fill=(44, 44, 52))
    d.line((55, 12, 56, 20), fill=gold)
    d.rectangle((55, 20, 57, 22), fill=gold)


JOKERS = [
    (bierbrunnen, (78, 140, 70)),
    (jochen, (150, 150, 168)),
    (udk_abschlussarbeit, (200, 70, 90)),
]


# --- boss chips --------------------------------------------------------------------------
def boss_disc(base_rgb, draw_glyph):
    """vanilla boss disc (blue chip) recoloured to base_rgb, glyph replaced"""
    ref = Image.open(os.path.join(VANILLA, 'BlindChips.png')).convert('RGBA')
    chip = ref.crop((0, 3 * 34, 34, 4 * 34))
    p = chip.load()
    counts = {}
    for y in range(34):
        for x in range(34):
            if p[x, y][3]:
                counts[p[x, y]] = counts.get(p[x, y], 0) + 1
    base = max(counts, key=counts.get)
    glyph_col = min(counts, key=lambda c: sum(c[:3]))
    lum = lambda c: sum(c[:3]) / max(1, sum(base[:3]))
    for y in range(34):
        for x in range(34):
            c = p[x, y]
            if not c[3]:
                continue
            if c == glyph_col and (x - 17) ** 2 + (y - 17) ** 2 < 12 ** 2:
                c = base
            f = lum(c)
            p[x, y] = tuple(min(255, int(v * f)) for v in base_rgb) + (c[3],)
    ink = tuple(int(v * 0.45) for v in base_rgb) + (255,)
    draw_glyph(ImageDraw.Draw(chip), ink)
    return chip


def kammer_glyph(d, ink):
    d.rectangle((10, 7, 23, 26), outline=ink, width=2)                         # face-down card
    d.line((13, 10, 20, 23), fill=ink)
    d.line((20, 10, 13, 23), fill=ink)


def adhs_glyph(d, ink):
    d.line([(7, 12), (11, 8), (14, 14), (18, 7), (21, 15), (25, 9), (27, 13)], fill=ink, width=2)
    d.line([(8, 24), (12, 19), (15, 26), (19, 20), (22, 27), (26, 21)], fill=ink, width=2)


if __name__ == '__main__':
    cards = [render(fn, bg) for fn, bg in JOKERS]
    sheet = Image.new('RGBA', (W * len(cards), H), (0, 0, 0, 0))
    for i, c in enumerate(cards):
        sheet.paste(c, (i * W, 0))
    sheet.save('batch3_jokers_1x.png')
    chips = [boss_disc((96, 84, 120), kammer_glyph), boss_disc((214, 196, 52), adhs_glyph)]
    blinds = Image.new('RGBA', (34 * 21, 68), (0, 0, 0, 0))
    for j, chip in enumerate(chips):
        blinds.paste(blind_strip(chip), (0, j * 34))
    blinds.save('batch3_blinds_1x.png')
    prev = Image.new('RGBA', (len(cards) * (W * 4 + 8) + 2 * 212, H * 4), (40, 40, 40, 255))
    for i, c in enumerate(cards):
        prev.paste(c.resize((W * 4, H * 4), Image.NEAREST), (i * (W * 4 + 8), 0))
    for j, chip in enumerate(chips):
        b = chip.resize((204, 204), Image.NEAREST)
        prev.paste(b, (len(cards) * (W * 4 + 8) + j * 212, 60), b)
    prev.save('batch3_preview.png')
