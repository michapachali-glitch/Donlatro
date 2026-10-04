"""Pixel art for Bähnle, Erdie Feuermann, Nolan, Frustsuppe, Shepherd's Pie and the two blinds.

Run from any directory: writes batch2_jokers_1x.png (5 cards) and blinds_1x.png
(2 rows x 21 animation frames, 34x34 each) into the current directory.
"""
import os
import sys
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from food_art import render, glyph, W, H  # noqa: E402

VANILLA = r'C:\Users\User\AppData\Roaming\Balatro\vanilla-src\resources\textures\1x'
DARK = (52, 48, 60)


# --- jokers ------------------------------------------------------------------------------
def baehnle(d):
    red, red_s, cream = (204, 42, 40), (150, 28, 28), (246, 240, 224)
    d.line((30, 15, 36, 9), fill=(80, 80, 92))                                 # pantograph
    d.line((42, 15, 36, 9), fill=(80, 80, 92))
    d.line((28, 9, 44, 9), fill=(80, 80, 92))
    d.rectangle((26, 15, 46, 17), fill=(110, 110, 120))
    d.rounded_rectangle((16, 18, 55, 80), 6, fill=red)                         # body
    d.rectangle((51, 22, 55, 77), fill=red_s)
    d.rounded_rectangle((16, 18, 55, 24), 3, fill=(214, 218, 228))             # roof
    d.rectangle((26, 19, 45, 23), fill=(30, 30, 36))                           # destination display
    for x in range(28, 44, 2):
        d.point((x, 21), fill=(255, 170, 40))
    d.rounded_rectangle((20, 27, 51, 46), 3, fill=(44, 64, 96))                # windshield
    d.line((23, 44, 33, 29), fill=(110, 150, 196))
    d.line((26, 44, 36, 29), fill=(90, 128, 176))
    d.rectangle((16, 50, 55, 54), fill=cream)                                  # stripe
    d.ellipse((20, 58, 26, 64), fill=(255, 232, 120))                          # headlights
    d.ellipse((45, 58, 51, 64), fill=(255, 232, 120))
    d.point((22, 60), fill=(255, 255, 255))
    d.point((47, 60), fill=(255, 255, 255))
    d.ellipse((33, 58, 38, 63), fill=(250, 200, 50))                           # emblem
    d.rectangle((21, 71, 50, 76), fill=(70, 70, 82))                           # bumper
    d.rectangle((33, 69, 38, 79), fill=(96, 96, 110))                          # coupler
    d.rectangle((19, 80, 52, 84), fill=(56, 56, 66))                           # bogie


def erdie(d):
    skin, skin_s = (240, 192, 152), (210, 160, 120)
    helmet, helmet_s, gold = (212, 42, 32), (160, 28, 22), (252, 204, 56)
    d.polygon([(13, 85), (17, 67), (29, 62), (43, 62), (55, 67), (59, 85)], fill=(40, 52, 84))  # jacket
    d.rectangle((15, 74, 57, 76), fill=(252, 222, 60))                        # reflective stripes
    d.rectangle((15, 77, 57, 77), fill=(210, 214, 220))
    d.rectangle((31, 58, 41, 64), fill=skin_s)                                 # neck
    d.ellipse((21, 38, 25, 46), fill=skin_s)                                   # ears
    d.ellipse((46, 38, 50, 46), fill=skin_s)
    d.ellipse((23, 28, 48, 61), fill=skin)                                     # face
    d.rectangle((43, 34, 47, 56), fill=skin_s)
    d.line((28, 39, 32, 39), fill=(90, 54, 30))                                # brows
    d.line((39, 39, 43, 39), fill=(90, 54, 30))
    d.rectangle((29, 42, 31, 43), fill=DARK)                                   # eyes
    d.rectangle((40, 42, 42, 43), fill=DARK)
    d.rectangle((35, 43, 36, 48), fill=skin_s)                                 # nose
    d.polygon([(26, 52), (31, 49), (40, 49), (45, 52), (42, 54), (36, 52), (29, 54)], fill=(118, 64, 30))  # mustache
    d.line((32, 56, 39, 56), fill=(170, 90, 80))                               # mouth
    d.pieslice((20, 14, 52, 42), 180, 360, fill=helmet)                        # helmet dome
    d.ellipse((14, 26, 58, 35), fill=helmet_s)                                 # brim
    d.ellipse((15, 26, 57, 33), fill=helmet)
    d.line((36, 15, 36, 27), fill=(236, 80, 64))                               # comb ridge
    d.polygon([(30, 17), (42, 17), (42, 25), (36, 29), (30, 25)], fill=gold)   # badge
    glyph(d, ['.#.', '##.', '.#.', '.#.', '###'], 35, 19, (160, 28, 22))       # "1"


def nolan(d):
    skin, skin_s = (236, 190, 150), (206, 156, 116)
    cap, cap_s = (44, 94, 204), (28, 62, 150)
    d.polygon([(13, 85), (17, 68), (29, 63), (43, 63), (55, 68), (59, 85)], fill=(132, 134, 146))  # hoodie
    d.polygon([(27, 63), (36, 72), (45, 63)], fill=(104, 106, 118))            # hood opening
    d.line((32, 70, 31, 80), fill=(240, 240, 240))                             # drawstrings
    d.line((40, 70, 41, 80), fill=(240, 240, 240))
    d.rectangle((31, 58, 41, 65), fill=skin_s)                                 # neck
    d.ellipse((21, 38, 25, 47), fill=skin_s)                                   # ears
    d.ellipse((46, 38, 50, 47), fill=skin_s)
    d.ellipse((23, 26, 48, 62), fill=skin)                                     # face
    d.rectangle((43, 34, 47, 56), fill=skin_s)
    d.rectangle((28, 41, 30, 42), fill=DARK)                                   # eyes
    d.rectangle((40, 41, 42, 42), fill=DARK)
    d.line((27, 38, 31, 37), fill=(80, 54, 36))                                # brows
    d.line((39, 37, 43, 38), fill=(80, 54, 36))
    d.rectangle((35, 43, 36, 48), fill=skin_s)                                 # nose
    d.line((31, 54, 37, 55), fill=(160, 80, 70))                               # smirk
    d.line((37, 55, 40, 53), fill=(160, 80, 70))
    for x in range(27, 45, 2):                                                 # stubble
        d.point((x, 58 - (x % 4 == 1)), fill=skin_s)
    d.pieslice((21, 14, 50, 46), 180, 360, fill=cap)                           # backwards cap
    d.rectangle((21, 29, 50, 31), fill=cap_s)
    d.rectangle((31, 25, 40, 30), fill=(92, 60, 38))                           # snapback gap (hair)
    d.line((31, 27, 40, 27), fill=(240, 240, 240))                             # strap
    d.polygon([(45, 24), (60, 27), (59, 31), (47, 31)], fill=cap_s)            # brim pointing back
    d.point((35, 15), fill=cap_s)                                              # button


def frustsuppe(d):
    bowl, bowl_s, stripe = (242, 242, 236), (196, 196, 204), (70, 110, 190)
    d.pieslice((11, 30, 60, 86), 0, 180, fill=bowl_s)                          # bowl
    d.pieslice((11, 30, 58, 84), 0, 180, fill=bowl)
    d.arc((11, 36, 60, 80), 20, 160, fill=stripe, width=2)
    d.ellipse((11, 50, 60, 64), fill=bowl)                                     # rim
    soup, soup_d, face = (126, 132, 58), (94, 100, 40), (56, 58, 24)
    d.ellipse((14, 51, 57, 63), fill=soup_d)                                   # soup surface
    d.ellipse((15, 51, 56, 61), fill=soup)
    d.line((24, 53, 30, 55), fill=face)                                        # angry brows
    d.line((47, 53, 41, 55), fill=face)
    d.rectangle((27, 56, 28, 57), fill=face)                                   # eyes
    d.rectangle((43, 56, 44, 57), fill=face)
    d.arc((30, 58, 41, 64), 200, 340, fill=face)                               # frown
    for x, y in ((19, 55), (51, 57), (37, 53)):                                # carrot bits
        d.point((x, y), fill=(220, 124, 40))
        d.point((x + 1, y), fill=(240, 160, 70))


def frustsuppe_steam(card):
    """steam is drawn after the outline pass so it stays wispy"""
    d = ImageDraw.Draw(card)
    for x0 in (25, 35, 45):
        d.line([(x0, 46), (x0 - 2, 41), (x0, 36), (x0 - 2, 31), (x0, 26)], fill=(240, 240, 248, 190))


def shepherds_pie(d):
    dish, dish_d, dish_h = (64, 96, 170), (40, 64, 124), (110, 146, 214)
    mash, mash_s, brown = (252, 232, 172), (226, 196, 128), (196, 136, 64)
    d.ellipse((11, 58, 60, 85), fill=dish_d)                                   # dish
    d.ellipse((11, 52, 60, 77), fill=dish)
    d.ellipse((13, 53, 58, 72), fill=dish_h)
    d.ellipse((15, 38, 56, 70), fill=mash_s)                                   # potato mound
    d.ellipse((16, 37, 54, 66), fill=mash)
    for y in range(44, 64, 5):                                                 # fork ridges
        d.line((20, y, 50, y - 2), fill=mash_s)
    for x, y in ((22, 47), (30, 43), (44, 46), (49, 54), (26, 56), (38, 52)):  # browned peaks
        d.point((x, y), fill=brown)
        d.point((x + 1, y), fill=brown)
    d.rectangle((17, 66, 54, 68), fill=(130, 70, 40))                          # meat layer
    for x in (21, 30, 39, 48):
        d.point((x, 67), fill=(110, 176, 60))                                  # peas
    # little sheep on top
    for cx, cy in ((36, 30), (41, 28), (46, 30), (39, 33), (44, 33)):
        d.ellipse((cx - 4, cy - 4, cx + 4, cy + 4), fill=(255, 255, 255))
    d.ellipse((29, 25, 35, 33), fill=(60, 60, 70))                             # head
    d.point((31, 28), fill=(255, 255, 255))
    d.rectangle((38, 37, 39, 39), fill=(60, 60, 70))                           # legs
    d.rectangle((45, 37, 46, 39), fill=(60, 60, 70))


JOKERS = [  # draw fn, background, optional post-outline step
    (baehnle, (96, 160, 222), None),
    (erdie, (232, 112, 44), None),
    (nolan, (92, 170, 112), None),
    (frustsuppe, (112, 100, 134), frustsuppe_steam),
    (shepherds_pie, (72, 150, 160), None),
]


# --- blind chips -------------------------------------------------------------------------
def boss_wasserschaden():
    """Blue boss disc (vanilla style) with a water-drop rune."""
    ref = Image.open(os.path.join(VANILLA, 'BlindChips.png')).convert('RGBA')
    chip = ref.crop((0, 3 * 34, 34, 4 * 34))          # blue boss chip
    p = chip.load()
    counts = {}
    for y in range(34):
        for x in range(34):
            if p[x, y][3]:
                counts[p[x, y]] = counts.get(p[x, y], 0) + 1
    base = max(counts, key=counts.get)
    glyph_col = min(counts, key=lambda c: sum(c[:3]))
    drop_col = tuple(int(v * 0.45) for v in base[:3]) + (255,)
    for y in range(34):                                 # erase the vanilla glyph
        for x in range(34):
            if p[x, y] == glyph_col and (x - 17) ** 2 + (y - 17) ** 2 < 12 ** 2:
                p[x, y] = base
    d = ImageDraw.Draw(chip)
    d.line([(17, 6), (12, 15), (10, 20), (12, 25), (17, 27), (22, 25), (24, 20), (22, 15), (17, 6)],
           fill=drop_col, width=2)                      # drop
    d.line([(8, 29), (11, 27), (14, 29), (17, 27), (20, 29), (23, 27), (26, 29)], fill=drop_col)  # wave
    return chip


def showdown_nachbar():
    """Showdown poker chip (vanilla ring) recoloured neon, speaker + notes in the middle."""
    ref = Image.open(os.path.join(VANILLA, 'BlindChips.png')).convert('RGBA')
    chip = ref.crop((0, 25 * 34, 34, 26 * 34))         # red showdown chip
    p = chip.load()
    inner = p[17, 6]
    for y in range(34):
        for x in range(34):
            r, g, b, a = p[x, y]
            if not a:
                continue
            dist2 = (x - 16.5) ** 2 + (y - 16.5) ** 2
            if dist2 < 10.5 ** 2:
                p[x, y] = inner                          # clear centre icon
            elif r > g + 40 and r > b + 40:              # red ring segments -> neon magenta
                f = r / 200
                p[x, y] = (min(255, int(236 * f)), int(40 * f), min(255, int(220 * f)), a)
    d = ImageDraw.Draw(chip)
    neon, neon_d = (60, 236, 255), (30, 150, 190)
    d.rectangle((9, 13, 13, 20), fill=neon_d)            # speaker
    d.polygon([(13, 13), (19, 8), (19, 25), (13, 20)], fill=neon)
    d.arc((19, 10, 25, 23), 300, 60, fill=neon)          # sound waves
    d.arc((19, 7, 29, 26), 300, 60, fill=neon)
    return chip


def blind_strip(chip):
    strip = Image.new('RGBA', (34 * 21, 34), (0, 0, 0, 0))
    for k in range(21):
        strip.paste(chip, (k * 34, 0))
    return strip


if __name__ == '__main__':
    cards = []
    for fn, bg, post in JOKERS:
        card = render(fn, bg)
        if post:
            post(card)
        cards.append(card)
    sheet = Image.new('RGBA', (W * len(cards), H), (0, 0, 0, 0))
    for i, c in enumerate(cards):
        sheet.paste(c, (i * W, 0))
    sheet.save('batch2_jokers_1x.png')
    blinds = Image.new('RGBA', (34 * 21, 68), (0, 0, 0, 0))
    blinds.paste(blind_strip(boss_wasserschaden()), (0, 0))
    blinds.paste(blind_strip(showdown_nachbar()), (0, 34))
    blinds.save('blinds_1x.png')
    prev = Image.new('RGBA', (len(cards) * (W * 4 + 8) + 2 * (34 * 6 + 8), H * 4), (40, 40, 40, 255))
    for i, c in enumerate(cards):
        prev.paste(c.resize((W * 4, H * 4), Image.NEAREST), (i * (W * 4 + 8), 0))
    ox = len(cards) * (W * 4 + 8)
    for j in range(2):
        b = blinds.crop((0, j * 34, 34, j * 34 + 34)).resize((204, 204), Image.NEAREST)
        prev.paste(b, (ox + j * 212, 60), b)
    prev.save('batch2_preview.png')
