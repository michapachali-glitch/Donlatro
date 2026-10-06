"""Pixel art for the 45 renamed vanilla jokers (src/reskins.lua) + 4 legendary soul layers.

Run from any directory: writes reskins_1x.png (10 x 5 grid, order = RESKINS then SOULS)
and reskins_preview.png into the current directory.
"""
import math
import os
import sys
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from food_art import render, glyph, outline, W, H  # noqa: E402
from batch2_art import nolan, DARK  # noqa: E402

WHITE = (255, 255, 255)
FONT = {
    '0': ['###', '#.#', '#.#', '#.#', '###'], '1': ['.#.', '##.', '.#.', '.#.', '###'],
    '2': ['##.', '..#', '.#.', '#..', '###'], '3': ['##.', '..#', '.#.', '..#', '##.'],
    'A': ['.#.', '#.#', '###', '#.#', '#.#'], 'D': ['##.', '#.#', '#.#', '#.#', '##.'],
    'I': ['###', '.#.', '.#.', '.#.', '###'], 'M': ['#.#', '###', '###', '#.#', '#.#'],
    '?': ['##.', '..#', '.#.', '...', '.#.'], '$': ['.##', '##.', '.#.', '.##', '##.'],
    '@': ['.#.', '#.#', '###', '#..', '.##'], 'E': ['###', '#..', '##.', '#..', '###'],
    'R': ['##.', '#.#', '##.', '#.#', '#.#'], 'C': ['.##', '#..', '#..', '#..', '.##'],
    'T': ['###', '.#.', '.#.', '.#.', '.#.'], 'K': ['#.#', '#.#', '##.', '#.#', '#.#'],
}


def txt(d, s, x, y, col):
    for ch in s:
        glyph(d, FONT[ch], x, y, col)
        x += 4


def txt2(d, s, x, y, col):
    """3x5 font at double size"""
    for ch in s:
        for j, row in enumerate(FONT[ch]):
            for i, c in enumerate(row):
                if c == '#':
                    d.rectangle((x + 2 * i, y + 2 * j, x + 2 * i + 1, y + 2 * j + 1), fill=col)
        x += 8


def person(d, skin=(238, 194, 156), hair=(90, 60, 40), shirt=(80, 90, 120), y0=0):
    skin_s = tuple(int(v * 0.86) for v in skin)
    d.polygon([(14, 85 + y0), (18, 68 + y0), (29, 63 + y0), (43, 63 + y0), (54, 68 + y0), (58, 85 + y0)], fill=shirt)
    d.rectangle((31, 57 + y0, 41, 64 + y0), fill=skin_s)
    d.ellipse((21, 38 + y0, 25, 46 + y0), fill=skin_s)
    d.ellipse((46, 38 + y0, 50, 46 + y0), fill=skin_s)
    d.ellipse((23, 26 + y0, 48, 61 + y0), fill=skin)
    d.pieslice((22, 22 + y0, 49, 44 + y0), 180, 360, fill=hair)
    d.rectangle((28, 41 + y0, 30, 42 + y0), fill=DARK)
    d.rectangle((40, 41 + y0, 42, 42 + y0), fill=DARK)
    d.rectangle((35, 44 + y0, 36, 48 + y0), fill=skin_s)
    d.line((31, 54 + y0, 40, 54 + y0), fill=(160, 80, 70))


def bubble(d, box, col=WHITE, tail=None):
    d.rounded_rectangle(box, 5, fill=col)
    if tail:
        d.polygon(tail, fill=col)


def suit(d, kind, cx, cy, col):
    if kind == 'spade':
        d.polygon([(cx, cy - 4), (cx - 4, cy + 1), (cx - 2, cy + 3), (cx, cy + 1), (cx + 2, cy + 3), (cx + 4, cy + 1)], fill=col)
        d.line((cx, cy + 1, cx, cy + 5), fill=col)
    elif kind == 'heart':
        d.polygon([(cx, cy + 4), (cx - 4, cy), (cx - 4, cy - 2), (cx - 2, cy - 3), (cx, cy - 1), (cx + 2, cy - 3), (cx + 4, cy - 2), (cx + 4, cy)], fill=col)
    elif kind == 'diamond':
        d.polygon([(cx, cy - 5), (cx + 4, cy), (cx, cy + 5), (cx - 4, cy)], fill=col)
    else:
        for x, y in ((cx, cy - 3), (cx - 3, cy + 1), (cx + 3, cy + 1)):
            d.ellipse((x - 2, y - 2, x + 2, y + 2), fill=col)
        d.line((cx, cy + 1, cx, cy + 5), fill=col)


# --- the 45 cards ------------------------------------------------------------------------
def half(d):
    d.pieslice((18, 20, 52, 54), 90, 270, fill=(255, 226, 90))                 # half light bulb
    d.rectangle((30, 52, 35, 62), fill=(170, 170, 184))
    d.line((35, 20, 35, 62), fill=(200, 160, 40))
    for x, y in ((14, 24), (12, 38), (16, 50)):
        d.line((x, y, x + 3, y), fill=(255, 240, 160))
    bubble(d, (40, 64, 56, 76), tail=[(42, 74), (38, 80), (46, 75)])
    d.point((44, 70), fill=DARK)
    d.point((47, 70), fill=DARK)


def mystic_summit(d):
    r = 32
    curve = [(16 + r * math.sin(math.radians(t)), 44 + r * math.cos(math.radians(t))) for t in range(0, 91, 10)]
    d.polygon(curve + [(16 + r, 44 + r)], fill=(176, 178, 190))
    d.ellipse((16, 28, 56, 68), outline=(220, 40, 40), width=3)                # "no" sign
    d.line((22, 34, 50, 62), fill=(220, 40, 40), width=3)


def flower_pot(d):
    green, green_d = (60, 150, 80), (40, 110, 60)
    for cx, cy, r in ((26, 34, 11), (44, 30, 12), (35, 22, 10)):
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=green)
        for k in range(3):                                                   # monstera slits
            a = math.radians(200 + 50 * k)
            d.line((cx, cy, cx + r * math.cos(a), cy + r * math.sin(a)), fill=green_d)
        d.ellipse((cx - 2, cy - 4, cx, cy - 2), fill=green_d)
    d.line((35, 44, 30, 36), fill=green_d)
    d.line((35, 44, 42, 34), fill=green_d)
    d.polygon([(22, 48), (48, 48), (44, 78), (26, 78)], fill=(206, 110, 70))   # pot
    d.rectangle((20, 46, 50, 52), fill=(226, 130, 90))


def stencil(d):
    d.polygon([(30, 10), (40, 10), (56, 80), (14, 80)], fill=(255, 246, 190))  # spotlight cone
    d.ellipse((16, 74, 54, 84), fill=(240, 220, 150))
    d.rectangle((34, 40, 36, 76), fill=(70, 70, 82))                           # mic stand
    d.rounded_rectangle((31, 30, 39, 42), 3, fill=(60, 60, 72))
    d.rectangle((28, 76, 42, 78), fill=(70, 70, 82))


def abstract(d):
    d.rounded_rectangle((18, 18, 52, 82), 3, fill=(200, 150, 90))             # clipboard
    d.rectangle((22, 24, 48, 78), fill=(250, 250, 244))
    d.rectangle((28, 14, 42, 22), fill=(150, 150, 166))
    for i, y in enumerate(range(30, 76, 8)):
        d.line((32, y, 46, y), fill=(150, 150, 170))
        if i < 4:
            d.line((24, y, 26, y + 2), fill=(60, 170, 80))
            d.line((26, y + 2, 29, y - 2), fill=(60, 170, 80))


def loyalty_card(d):
    d.rounded_rectangle((16, 22, 54, 76), 3, fill=(250, 250, 246))            # calendar
    d.rectangle((16, 22, 54, 34), fill=(210, 60, 60))
    for x in (24, 46):
        d.rectangle((x, 18, x + 2, 26), fill=(120, 120, 130))
    txt(d, 'MI', 31, 26, WHITE)
    d.polygon([(30, 44), (30, 66), (46, 55)], fill=(80, 170, 90))             # play button


def acrobat(d):
    d.ellipse((18, 56, 32, 68), fill=(60, 60, 80))                            # music note
    d.rectangle((29, 22, 32, 62), fill=(60, 60, 80))
    d.polygon([(32, 22), (48, 28), (48, 34), (32, 30)], fill=(60, 60, 80))
    d.rectangle((42, 50, 52, 54), fill=(80, 190, 90))                         # plus
    d.rectangle((45, 47, 49, 57), fill=(80, 190, 90))
    for x, y in ((16, 30), (52, 70), (40, 16)):
        d.point((x, y), fill=(255, 240, 120))


def smeared(d):
    d.rounded_rectangle((24, 28, 46, 80), 4, fill=(250, 246, 220))            # mayo bottle
    d.rectangle((30, 18, 40, 28), fill=(80, 140, 220))
    d.polygon([(33, 10), (37, 10), (38, 18), (32, 18)], fill=(80, 140, 220))
    d.rectangle((26, 44, 44, 60), fill=(240, 200, 60))
    txt(d, 'M', 34, 50, (200, 60, 40))
    d.ellipse((40, 72, 58, 80), fill=(250, 246, 220))                         # smear


def pareidolia(d):
    d.rounded_rectangle((20, 14, 50, 82), 4, fill=(40, 40, 52))               # phone
    d.rectangle((23, 20, 47, 72), fill=(120, 190, 240))
    d.ellipse((27, 28, 43, 46), fill=(238, 194, 156))                         # face on screen
    d.point((32, 35), fill=DARK)
    d.point((38, 35), fill=DARK)
    d.line((32, 41, 38, 41), fill=(160, 80, 70))
    d.polygon([(35, 66), (29, 58), (30, 54), (33, 53), (35, 56), (37, 53), (40, 54), (41, 58)], fill=(240, 70, 90))


def shortcut(d):
    bubble(d, (14, 56, 30, 70), col=(250, 250, 250))
    bubble(d, (40, 18, 56, 32), col=(250, 250, 250))
    d.arc((18, 20, 52, 66), 190, 300, fill=(250, 200, 60), width=3)           # jump arrow
    d.polygon([(42, 22), (50, 28), (40, 30)], fill=(250, 200, 60))


def arrowhead(d):
    d.rectangle((34, 10, 36, 20), fill=(200, 200, 210))                       # TV tower
    d.ellipse((27, 20, 43, 36), fill=(170, 176, 196))
    d.rectangle((27, 27, 43, 29), fill=(110, 116, 140))
    d.polygon([(32, 36), (38, 36), (40, 82), (30, 82)], fill=(220, 220, 230))
    d.rectangle((16, 76, 56, 84), fill=(120, 130, 150))
    suit(d, 'spade', 50, 60, (40, 40, 52))


def bloodstone(d):
    for i, x in enumerate((16, 28, 40)):                                       # half-timbered houses
        d.rectangle((x, 30, x + 11, 56), fill=(250, 240, 220))
        d.polygon([(x - 1, 30), (x + 5, 20), (x + 12, 30)], fill=(190, 70, 50))
        d.line((x, 38, x + 11, 38), fill=(120, 70, 40))
        d.line((x + 5, 30, x + 5, 56), fill=(120, 70, 40))
    d.rectangle((14, 56, 56, 72), fill=(80, 140, 190))                         # Neckar
    d.polygon([(18, 64), (52, 64), (48, 70), (22, 70)], fill=(140, 90, 50))  # Stocherkahn
    d.line((40, 48, 46, 68), fill=(120, 80, 40))
    suit(d, 'heart', 35, 80, (220, 50, 60))


def rough_gem(d):
    d.rectangle((26, 16, 30, 70), fill=(220, 120, 40))                         # harbour crane
    d.rectangle((14, 16, 52, 20), fill=(220, 120, 40))
    d.line((48, 20, 48, 40), fill=(80, 80, 90))
    d.rectangle((44, 40, 52, 46), fill=(60, 120, 200))                         # container
    d.rectangle((14, 66, 56, 82), fill=(60, 110, 170))                         # Elbe
    for x in range(16, 56, 8):
        d.line((x, 72, x + 4, 72), fill=(150, 200, 240))
    suit(d, 'diamond', 40, 58, (240, 120, 40))


def onyx_agate(d):
    d.ellipse((6, 50, 46, 86), fill=(80, 170, 90))                             # green hills
    d.ellipse((28, 46, 66, 86), fill=(60, 150, 70))
    for x, y in ((30, 26), (24, 34), (36, 34)):                                # shamrock (= club)
        d.ellipse((x - 6, y - 6, x + 6, y + 6), fill=(40, 130, 60))
    d.line((30, 36, 34, 48), fill=(40, 110, 50), width=2)


def credit_card(d):
    d.rectangle((14, 30, 56, 70), fill=(250, 248, 236))                        # tax letter
    d.polygon([(14, 30), (35, 50), (56, 30)], fill=(226, 222, 206))
    d.ellipse((38, 52, 54, 68), fill=(210, 50, 50))                            # red stamp
    txt(d, '$', 45, 57, WHITE)
    d.line((18, 62, 32, 62), fill=(150, 150, 160))


def delayed_grat(d):
    d.ellipse((16, 22, 54, 60), fill=(250, 250, 246))                         # clock
    d.ellipse((16, 22, 54, 60), outline=(70, 70, 90), width=2)
    d.line((35, 41, 35, 28), fill=DARK, width=2)
    d.line((35, 41, 44, 45), fill=DARK, width=2)
    d.polygon([(26, 66), (44, 66), (35, 74)], fill=(240, 200, 120))           # hourglass
    d.polygon([(26, 84), (44, 84), (35, 74)], fill=(240, 200, 120))
    d.rectangle((24, 64, 46, 66), fill=(140, 90, 50))
    d.rectangle((24, 84, 46, 86), fill=(140, 90, 50))


def business(d):
    d.rectangle((14, 30, 56, 66), fill=(250, 250, 246))                        # e-mail
    d.polygon([(14, 30), (35, 50), (56, 30)], fill=(220, 226, 240))
    d.ellipse((40, 54, 58, 72), fill=(250, 200, 50))                           # coin
    txt(d, '$', 48, 61, (150, 100, 20))
    txt(d, '@', 20, 56, (80, 120, 210))


def rocket(d):
    d.rectangle((33, 30, 37, 82), fill=(150, 150, 166))                        # radio mast
    d.polygon([(26, 82), (35, 30), (44, 82)], outline=(120, 120, 136))
    d.ellipse((31, 24, 39, 32), fill=(220, 60, 60))
    for r in (10, 16, 22):                                                     # reach waves
        d.arc((35 - r, 28 - r, 35 + r, 28 + r), 300, 60, fill=(250, 240, 160), width=2)
        d.arc((35 - r, 28 - r, 35 + r, 28 + r), 120, 240, fill=(250, 240, 160), width=2)


def bull(d):
    d.arc((18, 20, 52, 54), 180, 360, fill=(50, 50, 60), width=3)             # headphones
    d.rounded_rectangle((14, 34, 22, 50), 3, fill=(50, 50, 60))
    d.rounded_rectangle((48, 34, 56, 50), 3, fill=(50, 50, 60))
    d.rounded_rectangle((28, 36, 42, 60), 6, fill=(200, 200, 214))           # podcast mic
    for y in range(40, 58, 3):
        d.line((30, y, 40, y), fill=(150, 150, 166))
    d.rectangle((34, 60, 36, 74), fill=(80, 80, 92))
    d.rectangle((26, 74, 44, 78), fill=(80, 80, 92))


def bootstraps(d):
    d.rectangle((18, 30, 52, 56), fill=(60, 64, 80))                           # laptop
    d.rectangle((21, 33, 49, 53), fill=(120, 200, 240))
    d.polygon([(12, 58), (58, 58), (54, 64), (16, 64)], fill=(170, 174, 190))
    txt(d, '$', 34, 41, (40, 120, 60))
    d.rounded_rectangle((44, 66, 54, 78), 2, fill=(250, 250, 246))            # coffee
    d.rectangle((46, 68, 52, 70), fill=(110, 64, 36))


def matador(d):
    d.line((22, 30, 22, 84), fill=(120, 120, 130), width=2)                    # flipped umbrella
    d.polygon([(10, 20), (22, 34), (40, 14), (34, 28), (50, 24), (22, 34)], fill=(210, 60, 60))
    for y in (40, 54, 68):                                                     # wind gusts
        d.line((28, y, 52, y), fill=(240, 246, 255), width=2)
        d.arc((46, y - 6, 56, y + 2), 270, 90, fill=(240, 246, 255), width=2)


def troubadour(d):
    bubble(d, (12, 20, 42, 42), col=(250, 250, 250), tail=[(18, 40), (14, 48), (24, 41)])
    bubble(d, (28, 46, 58, 68), col=(200, 230, 250), tail=[(50, 66), (54, 74), (46, 67)])
    d.line((18, 31, 22, 29), fill=DARK)
    d.line((22, 29, 26, 33), fill=DARK)
    d.line((26, 33, 30, 29), fill=DARK)
    d.line((30, 29, 36, 31), fill=DARK)
    suit(d, 'heart', 43, 57, (230, 70, 90))


def burglar(d):
    bubble(d, (18, 50, 56, 74), col=(250, 250, 250), tail=[(24, 72), (20, 80), (30, 73)])
    d.line((24, 58, 50, 58), fill=(150, 150, 170))
    d.line((24, 64, 44, 64), fill=(150, 150, 170))
    d.polygon([(14, 22), (24, 18), (35, 22), (46, 18), (56, 22), (54, 34), (44, 36), (35, 30), (26, 36), (16, 34)], fill=(30, 30, 40))
    d.ellipse((21, 24, 29, 30), fill=(250, 250, 250))
    d.ellipse((41, 24, 49, 30), fill=(250, 250, 250))


def stuntman(d):
    for x0 in (14, 46):                                                        # dumbbell
        d.rounded_rectangle((x0, 34, x0 + 10, 62), 2, fill=(60, 60, 72))
    d.rectangle((24, 44, 46, 52), fill=(170, 170, 184))
    d.rounded_rectangle((24, 64, 46, 80), 2, fill=(40, 40, 52))
    txt2(d, '23', 27, 67, (120, 230, 120))


def juggler(d):
    d.rectangle((14, 60, 56, 82), fill=(80, 140, 200))                         # river
    d.arc((14, 34, 56, 82), 180, 360, fill=(170, 120, 80), width=4)           # arch bridge
    d.rectangle((12, 54, 58, 58), fill=(190, 140, 90))
    for x in range(20, 54, 6):
        d.line((x, 42, x, 54), fill=(150, 100, 60))


def drunkard(d):
    d.rounded_rectangle((26, 36, 44, 82), 4, fill=(110, 70, 20))              # beer bottle
    d.polygon([(30, 36), (40, 36), (38, 20), (32, 20)], fill=(110, 70, 20))
    d.rectangle((31, 14, 39, 20), fill=(220, 180, 60))
    d.rectangle((26, 50, 44, 66), fill=(250, 236, 200))
    d.rectangle((28, 52, 42, 54), fill=(200, 60, 50))
    d.rectangle((28, 40, 29, 78), fill=(160, 110, 40))


def chaos(d):
    d.rectangle((14, 40, 56, 76), fill=(40, 40, 52))                           # clapperboard
    d.polygon([(14, 30), (54, 22), (56, 30), (16, 38)], fill=(250, 250, 250))
    for i in range(5):
        x = 18 + i * 8
        d.polygon([(x, 29 - i * 1.6), (x + 4, 28 - i * 1.6), (x + 6, 36 - i * 1.6), (x + 2, 37 - i * 1.6)], fill=(40, 40, 52))
    d.line((18, 52, 52, 52), fill=(200, 200, 210))
    txt(d, '2', 22, 60, WHITE)


def luchador(d):
    d.polygon([(16, 44), (30, 38), (44, 26), (44, 70), (30, 58), (16, 54)], fill=(230, 80, 60))  # megaphone
    d.rectangle((12, 44, 18, 54), fill=(60, 60, 72))
    d.ellipse((40, 26, 50, 70), fill=(250, 200, 190))
    txt(d, 'AD', 50, 76, (250, 250, 250))


def mr_bones(d):
    d.rectangle((14, 34, 56, 58), fill=(50, 50, 60))                           # film strip
    for x in range(16, 56, 6):
        d.rectangle((x, 36, x + 2, 38), fill=(250, 250, 250))
        d.rectangle((x, 54, x + 2, 56), fill=(250, 250, 250))
    d.rectangle((20, 40, 50, 52), fill=(150, 200, 240))
    d.line((24, 66, 32, 76), fill=(60, 190, 80), width=4)                      # check mark
    d.line((32, 76, 48, 60), fill=(60, 190, 80), width=4)


def ceremonial(d):
    d.rectangle((14, 52, 56, 70), fill=(50, 50, 60))                           # film strip
    for x in range(16, 56, 6):
        d.rectangle((x, 54, x + 2, 56), fill=(250, 250, 250))
    d.line((14, 50, 56, 72), fill=(250, 250, 250))
    d.ellipse((16, 16, 28, 28), outline=(200, 40, 40), width=3)                # scissors
    d.ellipse((16, 32, 28, 44), outline=(200, 40, 40), width=3)
    d.polygon([(26, 24), (54, 40), (52, 42), (26, 30)], fill=(200, 204, 214))
    d.polygon([(26, 36), (54, 24), (52, 22), (26, 32)], fill=(200, 204, 214))


def marble(d):
    d.rectangle((14, 14, 56, 84), fill=(236, 230, 214))                        # wall
    for x, y in ((22, 24), (44, 30), (30, 70), (48, 64)):
        d.ellipse((x - 3, y - 3, x + 3, y + 3), fill=(120, 110, 100))         # holes
    d.polygon([(22, 40), (44, 36), (46, 50), (24, 54)], fill=(200, 204, 214))  # putty knife
    d.rectangle((40, 48, 46, 64), fill=(200, 120, 50))
    d.ellipse((24, 42, 32, 48), fill=(250, 250, 250))


def hiker(d):
    d.polygon([(14, 62), (40, 62), (54, 70), (54, 78), (14, 78)], fill=(230, 80, 70))  # sneaker
    d.rectangle((14, 74, 56, 80), fill=(250, 250, 250))
    for x in range(22, 40, 5):
        d.line((x, 62, x + 3, 66), fill=(250, 250, 250))
    for x, y in ((20, 30), (32, 42), (24, 50), (40, 22)):                      # footprints
        d.ellipse((x, y, x + 5, y + 8), fill=(160, 120, 80))


def swashbuckler(d):
    d.polygon([(22, 22), (30, 18), (40, 18), (48, 22), (58, 40), (50, 44), (48, 38), (48, 82), (22, 82), (22, 38), (20, 44), (12, 40)],
              fill=(60, 60, 80))                                               # merch hoodie
    d.arc((28, 14, 42, 28), 0, 180, fill=(40, 40, 56), width=3)
    d.ellipse((27, 40, 43, 56), fill=(250, 200, 60))
    txt(d, 'D', 34, 46, (60, 60, 80))


def misprint(d):
    d.rounded_rectangle((14, 20, 34, 38), 3, fill=(250, 250, 250))
    d.rounded_rectangle((36, 56, 56, 74), 3, fill=(250, 250, 250))
    txt2(d, '23', 17, 24, DARK)
    txt2(d, '32', 39, 60, (200, 50, 60))
    d.arc((22, 34, 54, 66), 300, 60, fill=(250, 200, 60), width=2)
    d.arc((16, 30, 48, 62), 120, 240, fill=(250, 200, 60), width=2)


def baseball(d):
    for x, s, col in ((18, 0.8, (120, 150, 200)), (30, 1.1, (200, 120, 90)), (44, 0.8, (120, 180, 120))):
        r = int(5 * s)
        d.ellipse((x, 36, x + 2 * r, 36 + 2 * r), fill=(238, 194, 156))       # side characters
        d.rounded_rectangle((x - 2, 36 + 2 * r, x + 2 * r + 2, 76), 3, fill=col)


def idol(d):
    cx, cy = 35, 46
    for k in range(8):                                                         # gear
        a = math.radians(k * 45)
        d.rectangle((cx + 17 * math.cos(a) - 3, cy + 17 * math.sin(a) - 3, cx + 17 * math.cos(a) + 3, cy + 17 * math.sin(a) + 3), fill=(170, 176, 196))
    d.ellipse((cx - 16, cy - 16, cx + 16, cy + 16), fill=(170, 176, 196))
    d.ellipse((cx - 10, cy - 10, cx + 10, cy + 10), fill=(220, 50, 60))
    d.polygon([(cx - 3, cy - 6), (cx - 3, cy + 6), (cx + 6, cy)], fill=(250, 250, 250))


def oops(d):
    for i, col in enumerate(((230, 70, 70), (240, 160, 60), (240, 220, 80), (80, 190, 90), (70, 130, 220))):
        r = 26 - i * 3                                                         # rainbow
        d.arc((35 - r, 66 - r, 35 + r, 66 + r), 180, 360, fill=col, width=3)
    d.polygon([(48, 14), (50, 20), (56, 20), (51, 24), (53, 30), (48, 26), (43, 30), (45, 24), (40, 20), (46, 20)], fill=(255, 230, 90))


def cartomancer(d):
    d.ellipse((18, 22, 52, 56), fill=(150, 120, 220))                          # crystal ball
    d.ellipse((22, 26, 34, 36), fill=(210, 190, 250))
    d.polygon([(20, 66), (50, 66), (46, 56), (24, 56)], fill=(140, 90, 50))
    for x, y in ((40, 36), (30, 46), (44, 48)):
        d.point((x, y), fill=(255, 255, 200))
        d.point((x + 1, y), fill=(255, 255, 200))


def astronomer(d):
    nolan(d)
    for x, y in ((16, 14), (54, 20), (48, 10)):                                # stars
        d.line((x - 2, y, x + 2, y), fill=(255, 240, 160))
        d.line((x, y - 2, x, y + 2), fill=(255, 240, 160))


def vagabond(d):
    d.rectangle((14, 56, 56, 82), fill=(60, 140, 90))                          # crate
    for x in range(16, 56, 9):
        d.rounded_rectangle((x, 28, x + 6, 58), 2, fill=(120, 180, 120))     # bottles
        d.rectangle((x + 2, 22, x + 4, 28), fill=(120, 180, 120))
    d.rectangle((14, 64, 56, 66), fill=(40, 110, 70))


def burnt(d):
    """One-Take Donnie: clapperboard for take 1, with a red REC light."""
    slate, slate_h, white = (44, 44, 54), (70, 70, 84), (246, 246, 246)
    red = (230, 40, 40)
    d.ellipse((18, 9, 23, 14), fill=red)                                      # REC light
    d.point((19, 10), fill=(255, 160, 160))
    txt(d, 'REC', 26, 10, red)
    # open clapper stick (hinged at the left)
    d.polygon([(17, 31), (52, 19), (54, 25), (19, 37)], fill=slate)
    for i in range(5):
        x = 22 + i * 7
        y = 30 - i * 2.4
        d.polygon([(x, y), (x + 4, y - 1.4), (x + 6, y + 4.6), (x + 2, y + 6)], fill=white)
    d.ellipse((16, 34, 20, 38), fill=(170, 170, 184))                         # hinge
    # fixed striped bar + slate
    d.rectangle((17, 39, 55, 45), fill=slate)
    for x in range(20, 55, 8):
        d.polygon([(x, 39), (x + 4, 39), (x + 2, 45), (x - 2, 45)], fill=white)
    d.rectangle((17, 46, 55, 80), fill=slate)
    d.rectangle((17, 46, 55, 47), fill=slate_h)
    d.line((20, 56, 52, 56), fill=(120, 120, 136))                            # chalk lines
    d.line((36, 56, 36, 77), fill=(120, 120, 136))
    txt(d, 'TAKE', 39, 50, white)
    txt2(d, '1', 41, 61, white)                                               # take 1
    for y in (51, 61, 66, 71):                                                    # scribbles
        d.line((21, y, 32, y), fill=(200, 200, 210))


def triboulet(d):
    d.rectangle((12, 66, 58, 74), fill=(120, 80, 50))                          # podcast table
    for x in (22, 46):
        d.rectangle((x, 52, x + 2, 66), fill=(70, 70, 82))
        d.rounded_rectangle((x - 3, 42, x + 5, 54), 3, fill=(60, 60, 72))


def yorick(d):
    d.rounded_rectangle((18, 46, 52, 82), 2, fill=(250, 246, 232))            # notebook
    for y in range(52, 80, 5):
        d.line((22, y, 48, y), fill=(160, 180, 220))
    d.line((18, 46, 18, 82), fill=(200, 60, 60), width=2)


def chicot(d):
    d.rectangle((16, 40, 54, 84), fill=(250, 250, 246))                        # contract
    for y in range(46, 70, 5):
        d.line((20, y, 50, y), fill=(160, 160, 170))
    d.line([(22, 76), (28, 72), (32, 78), (40, 72), (48, 76)], fill=(40, 60, 160))  # signature


def perkeo(d):
    d.rectangle((16, 40, 54, 84), fill=(250, 250, 246))                        # transcript
    for i, y in enumerate(range(46, 82, 5)):
        d.line((20, y, 30 if i % 2 else 26, y), fill=(200, 60, 60))
        d.line((32, y, 50 - (i * 3) % 10, y), fill=(140, 140, 150))


RESKINS = [  # (vanilla key, draw fn, background)
    ('half', half, (240, 180, 60)), ('mystic_summit', mystic_summit, (120, 170, 210)),
    ('flower_pot', flower_pot, (230, 200, 160)), ('stencil', stencil, (60, 60, 80)),
    ('abstract', abstract, (150, 110, 200)), ('loyalty_card', loyalty_card, (90, 160, 200)),
    ('acrobat', acrobat, (240, 140, 150)), ('smeared', smeared, (240, 210, 120)),
    ('pareidolia', pareidolia, (220, 120, 170)), ('shortcut', shortcut, (90, 170, 160)),
    ('arrowhead', arrowhead, (110, 130, 170)), ('bloodstone', bloodstone, (150, 190, 120)),
    ('rough_gem', rough_gem, (110, 150, 190)), ('onyx_agate', onyx_agate, (150, 210, 230)),
    ('credit_card', credit_card, (190, 80, 80)), ('delayed_grat', delayed_grat, (200, 170, 110)),
    ('business', business, (90, 120, 200)), ('rocket', rocket, (50, 60, 110)),
    ('bull', bull, (200, 90, 70)), ('bootstraps', bootstraps, (110, 160, 120)),
    ('matador', matador, (130, 160, 200)), ('troubadour', troubadour, (70, 90, 150)),
    ('burglar', burglar, (84, 132, 112)), ('stuntman', stuntman, (200, 70, 60)),
    ('juggler', juggler, (150, 200, 230)), ('drunkard', drunkard, (210, 160, 60)),
    ('chaos', chaos, (220, 200, 90)), ('luchador', luchador, (90, 170, 220)),
    ('mr_bones', mr_bones, (150, 150, 166)), ('ceremonial', ceremonial, (110, 110, 130)),
    ('marble', marble, (170, 150, 130)), ('hiker', hiker, (120, 190, 110)),
    ('swashbuckler', swashbuckler, (230, 120, 60)), ('misprint', misprint, (150, 90, 160)),
    ('baseball', baseball, (100, 160, 180)), ('idol', idol, (60, 60, 80)),
    ('oops', oops, (120, 180, 230)), ('cartomancer', cartomancer, (60, 50, 100)),
    ('astronomer', astronomer, (30, 40, 80)), ('vagabond', vagabond, (200, 180, 140)),
    ('burnt', burnt, (110, 60, 60)),
    ('triboulet', triboulet, (200, 150, 60)), ('yorick', yorick, (120, 110, 150)),
    ('chicot', chicot, (40, 170, 90)), ('perkeo', perkeo, (90, 120, 170)),
]


# --- legendary soul layers (floating above the card) -------------------------------------
def soul(fn):
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    fn(ImageDraw.Draw(layer))
    outline(layer)
    return layer


def head(d, cx, cy, skin, hair, glasses=False, beard=None):
    d.ellipse((cx - 9, cy - 11, cx + 9, cy + 11), fill=skin)
    d.pieslice((cx - 10, cy - 14, cx + 10, cy + 2), 180, 360, fill=hair)
    d.point((cx - 4, cy), fill=DARK)
    d.point((cx + 4, cy), fill=DARK)
    if glasses:
        d.rectangle((cx - 7, cy - 2, cx - 2, cy + 2), outline=(30, 30, 36))
        d.rectangle((cx + 2, cy - 2, cx + 7, cy + 2), outline=(30, 30, 36))
    if beard:
        d.pieslice((cx - 9, cy - 2, cx + 9, cy + 13), 0, 180, fill=beard)
    d.line((cx - 3, cy + 6, cx + 3, cy + 6), fill=(160, 80, 70))


SOULS = [
    lambda d: (head(d, 25, 30, (238, 194, 156), (40, 30, 30), beard=(60, 40, 30)),
               head(d, 46, 30, (238, 194, 156), (110, 90, 70), glasses=True)),     # Costa und Jochen
    lambda d: (head(d, 35, 30, (238, 194, 156), (90, 60, 40)),
               bubble(d, (44, 8, 58, 22), col=(250, 250, 250)), txt(d, '?', 50, 12, DARK)),  # Wo war ich?
    lambda d: (d.ellipse((22, 14, 48, 40), fill=(40, 200, 100)),
               d.arc((28, 20, 44, 32), 200, 340, fill=DARK, width=2),
               d.arc((29, 24, 43, 34), 200, 340, fill=DARK, width=2),
               d.arc((31, 28, 41, 36), 200, 340, fill=DARK, width=2)),            # Spotify-Deal
    lambda d: (d.polygon([(44, 12), (50, 16), (30, 40), (26, 40), (26, 36)], fill=(240, 200, 60)),
               d.polygon([(26, 36), (26, 40), (22, 42)], fill=DARK)),             # Transkript pen
]

if __name__ == '__main__':
    cells = [render(fn, bg) for _, fn, bg in RESKINS] + [soul(fn) for fn in SOULS]
    sheet = Image.new('RGBA', (W * 10, H * 5), (0, 0, 0, 0))
    for i, c in enumerate(cells):
        sheet.paste(c, ((i % 10) * W, (i // 10) * H))
    sheet.save('reskins_1x.png')
    prev = Image.new('RGBA', (10 * (W * 2 + 4), 5 * (H * 2 + 4)), (40, 40, 40, 255))
    for i, c in enumerate(cells[:45]):
        big = c.resize((W * 2, H * 2), Image.NEAREST)
        if i >= 41:
            big.alpha_composite(cells[45 + i - 41].resize((W * 2, H * 2), Image.NEAREST))
        prev.paste(big, ((i % 10) * (W * 2 + 4), (i // 10) * (H * 2 + 4)), big)
    prev.save('reskins_preview.png')
