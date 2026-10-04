"""Pixel art for batch 5: Die Rampe, Classic Donnie, Ihr checkt schon was ich meine, Anyway,
Raketenstart, Der Akkuschrauber, Buttplugs bei Butlers, Kaffee, Donnie O'Sullivan (+ soul layer).

Run from any directory: writes batch5_jokers_1x.png (10 cells: 9 cards + Donnie's soul
layer) and batch5_preview.png into the current directory.
"""
import math
import os
import sys
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from food_art import render, glyph, outline, W, H, OUTLINE  # noqa: E402
from batch2_art import DARK  # noqa: E402

PHOTO = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'working', 'Daunendonnie.jpg')
VANILLA = r'C:\Users\User\AppData\Roaming\Balatro\vanilla-src\resources\textures\1x\Jokers.png'

# 3x5 pixel font for signs
FONT = {
    'A': ['.#.', '#.#', '###', '#.#', '#.#'], 'N': ['#.#', '###', '###', '###', '#.#'],
    'Y': ['#.#', '#.#', '.#.', '.#.', '.#.'], 'W': ['#.#', '#.#', '###', '###', '#.#'],
}


def text(d, s, x, y, col):
    for ch in s:
        glyph(d, FONT[ch], x, y, col)
        x += 4


# --- drawn jokers ------------------------------------------------------------------------
def die_rampe(d):
    concrete, concrete_d, coping = (176, 178, 190), (130, 132, 146), (230, 232, 240)
    cx, cy, r = 13, 36, 44
    curve = [(cx + r * math.sin(math.radians(t)), cy + r * math.cos(math.radians(t))) for t in range(0, 91, 5)]
    d.polygon(curve + [(57, 80)], fill=concrete)                                # quarter pipe
    d.polygon([(57, 36), (60, 36), (60, 82), (57, 80)], fill=concrete_d)
    d.line(curve, fill=concrete_d)
    d.rectangle((50, 33, 60, 36), fill=coping)                                  # deck + coping
    d.rectangle((13, 80, 57, 84), fill=concrete_d)                              # ground
    # skateboard in the air, tilted
    d.polygon([(18, 26), (38, 18), (39, 21), (19, 29)], fill=(204, 60, 44))
    d.line((18, 26, 38, 18), fill=(240, 120, 90))
    for x, y in ((22, 30), (35, 25)):
        d.ellipse((x - 2, y - 1, x + 1, y + 2), fill=(250, 220, 120))
    for x in range(16, 46, 6):                                                  # speed lines
        d.point((x, 40 + (x % 4)), fill=(255, 255, 255))


def ihr_checkt(d):
    d.rounded_rectangle((18, 9, 54, 27), 5, fill=(255, 255, 255))               # speech bubble
    d.polygon([(26, 26), (24, 33), (32, 26)], fill=(255, 255, 255))
    for x in (29, 36, 43):
        d.rectangle((x, 17, x + 2, 19), fill=DARK)                              # "..."
    face, face_s = (252, 210, 62), (226, 170, 40)
    d.ellipse((17, 34, 55, 74), fill=face_s)                                    # emoji face
    d.ellipse((17, 33, 54, 71), fill=face)
    d.line((25, 46, 31, 47), fill=DARK, width=2)                                # wink
    d.line((24, 40, 31, 41), fill=(120, 80, 20))                                # brows
    d.line((40, 39, 47, 37), fill=(120, 80, 20))
    d.ellipse((41, 43, 45, 48), fill=DARK)                                      # open eye
    d.point((43, 44), fill=(255, 255, 255))
    d.arc((28, 50, 48, 64), 20, 120, fill=DARK, width=2)                        # smirk
    d.ellipse((47, 54, 52, 59), fill=(250, 150, 110))                           # blush


def anyway(d):
    wood, wood_d, post = (196, 140, 80), (150, 100, 52), (120, 82, 46)
    d.rectangle((33, 46, 38, 84), fill=post)                                    # post
    d.rectangle((36, 46, 38, 84), fill=wood_d)
    d.polygon([(12, 26), (50, 26), (60, 35), (50, 44), (12, 44)], fill=wood)    # arrow sign
    d.polygon([(12, 41), (50, 41), (53, 44), (12, 44)], fill=wood_d)
    for y in (31, 37):
        d.line((14, y, 48, y), fill=(210, 160, 100))                            # wood grain
    text(d, 'ANYWAY', 16, 32, DARK)
    d.ellipse((16, 78, 55, 85), fill=(90, 150, 80))                             # grass tuft


def raketenstart(d):
    body, body_s, red, red_s = (240, 240, 246), (196, 200, 214), (214, 50, 44), (160, 32, 30)
    for x, y, r in ((22, 80, 7), (34, 82, 8), (48, 80, 7), (28, 75, 6), (42, 75, 6)):  # smoke
        d.ellipse((x - r, y - r, x + r, y + r), fill=(214, 214, 224))
    d.polygon([(30, 62), (36, 78), (42, 62)], fill=(252, 160, 40))              # flame
    d.polygon([(32, 62), (36, 72), (40, 62)], fill=(255, 236, 120))
    d.polygon([(36, 8), (44, 22), (44, 58), (28, 58), (28, 22)], fill=body)     # body
    d.rectangle((40, 22, 44, 58), fill=body_s)
    d.polygon([(36, 8), (44, 22), (28, 22)], fill=red)                          # nose
    d.polygon([(36, 8), (44, 22), (40, 22)], fill=red_s)
    d.polygon([(28, 44), (20, 58), (20, 62), (28, 56)], fill=red)               # fins
    d.polygon([(44, 44), (52, 58), (52, 62), (44, 56)], fill=red_s)
    d.rectangle((33, 56, 39, 62), fill=(110, 110, 124))                         # nozzle
    d.ellipse((31, 28, 41, 38), fill=(70, 90, 130))                             # window
    d.ellipse((33, 30, 39, 36), fill=(120, 180, 230))
    d.point((34, 31), fill=(255, 255, 255))


def akkuschrauber(d):
    yellow, yellow_s, black, steel = (250, 200, 40), (210, 156, 20), (46, 46, 54), (196, 200, 210)
    d.rectangle((13, 32, 19, 34), fill=steel)                                   # bit
    d.rectangle((19, 29, 25, 37), fill=(150, 154, 166))                         # chuck
    d.rectangle((22, 30, 24, 36), fill=steel)
    d.rounded_rectangle((25, 24, 56, 41), 4, fill=yellow)                       # body
    d.rectangle((25, 37, 56, 41), fill=yellow_s)
    d.rectangle((27, 27, 30, 38), fill=black)                                   # nose grip
    for x in range(44, 54, 3):
        d.line((x, 27, x, 31), fill=yellow_s)                                   # vents
    d.polygon([(34, 41), (46, 41), (44, 66), (36, 66)], fill=black)             # handle
    d.rectangle((33, 43, 35, 48), fill=(210, 40, 40))                           # trigger
    d.rectangle((28, 66, 52, 78), fill=black)                                   # battery
    d.rectangle((28, 66, 52, 68), fill=yellow)
    d.rectangle((47, 71, 50, 73), fill=(90, 220, 110))                          # charge led


def butlers(d):
    paper, paper_s, red = (250, 246, 238), (214, 206, 190), (196, 40, 52)
    d.polygon([(38, 30), (31, 16), (33, 13), (44, 13), (46, 16), (40, 30)], fill=(40, 40, 50))  # mystery item
    d.ellipse((30, 10, 47, 17), fill=(62, 62, 74))
    d.arc((22, 18, 34, 34), 180, 360, fill=paper_s, width=2)                    # handles
    d.arc((38, 18, 50, 34), 180, 360, fill=paper_s, width=2)
    d.polygon([(16, 28), (56, 28), (58, 84), (14, 84)], fill=paper)             # shopping bag
    d.polygon([(50, 28), (56, 28), (58, 84), (52, 84)], fill=paper_s)
    d.rectangle((16, 28, 56, 31), fill=red)
    d.ellipse((24, 44, 46, 66), fill=red)                                       # logo
    glyph(d, ['###.', '#..#', '###.', '#..#', '###.'], 33, 52, (255, 255, 255))  # "B"
    d.polygon([(44, 70), (52, 74), (44, 78)], fill=(250, 200, 60))              # price tag


def kaffee(d):
    cup, cup_s = (246, 244, 240), (200, 198, 206)
    d.ellipse((12, 74, 60, 84), fill=(214, 214, 222))                           # saucer
    d.ellipse((24, 50, 52, 64), outline=cup, width=4)                           # handle
    d.rounded_rectangle((16, 40, 46, 80), 6, fill=cup)                          # mug
    d.rectangle((40, 42, 46, 78), fill=cup_s)
    d.ellipse((16, 36, 46, 46), fill=cup)
    d.ellipse((18, 37, 44, 44), fill=(110, 64, 36))                             # coffee
    d.ellipse((24, 38, 36, 42), fill=(160, 104, 64))                            # crema
    d.rectangle((20, 56, 34, 62), fill=(196, 60, 52))                           # heart print
    d.point((20, 56), fill=cup)
    d.point((34, 56), fill=cup)


def kaffee_steam(card):
    d = ImageDraw.Draw(card)
    for x0 in (24, 32, 40):
        d.line([(x0, 33), (x0 - 2, 28), (x0, 23), (x0 - 2, 18)], fill=(240, 240, 248, 190))


def osullivan(d):
    cue, cue_d = (226, 186, 120), (160, 110, 60)
    for x, y in ((24, 44), (30, 44), (36, 44), (27, 50), (33, 50), (30, 56)):   # reds triangle
        d.ellipse((x - 3, y - 3, x + 3, y + 3), fill=(204, 30, 30))
        d.point((x - 1, y - 1), fill=(255, 140, 130))
    d.ellipse((42, 64, 49, 71), fill=(24, 24, 30))                              # black ball
    d.point((44, 66), fill=(160, 160, 170))
    d.ellipse((18, 64, 25, 71), fill=(250, 250, 246))                           # cue ball
    d.line((10, 86, 22, 70), fill=cue, width=3)                                 # cue
    d.line((10, 86, 13, 82), fill=cue_d, width=3)


# --- photo-based pieces ------------------------------------------------------------------
def photo_card(crop, tint):
    """Classic Donnie: the Daunendonnie photo, pixelated in sepia, in a vanilla card frame."""
    ref = Image.open(VANILLA).convert('RGBA').crop((0, 0, W, H))
    rp = ref.load()
    opaque = lambda x, y: 0 <= x < W and 0 <= y < H and rp[x, y][3] > 0
    ring = {(x, y) for x in range(W) for y in range(H) if opaque(x, y)
            and not all(opaque(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))}
    inner = [(x, y) for x in range(W) for y in range(H) if opaque(x, y) and (x, y) not in ring]
    x0, x1 = min(p[0] for p in inner), max(p[0] for p in inner)
    y0, y1 = min(p[1] for p in inner), max(p[1] for p in inner)
    photo = Image.open(PHOTO).convert('L').crop(crop)
    photo = ImageEnhance.Contrast(photo).enhance(1.35)
    small = photo.resize((x1 - x0 + 1, y1 - y0 + 1), Image.LANCZOS).filter(ImageFilter.SHARPEN)
    small = small.quantize(8, dither=Image.NONE).convert('L')
    sp = small.load()
    card = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    cp = card.load()
    for x, y in inner:
        v = sp[x - x0, y - y0] / 255
        cp[x, y] = tuple(int(c * (0.25 + 0.85 * v)) for c in tint) + (255,)
    for x, y in ring:
        cp[x, y] = rp[x, y]
    return card


def soul_head():
    """Donnie's head cut out of the photo as a floating legendary layer (with sunglasses)."""
    head = Image.open(PHOTO).convert('RGB').crop((262, 10, 422, 250))
    head = ImageEnhance.Color(ImageEnhance.Contrast(head).enhance(1.25)).enhance(1.2)
    small = head.resize((32, 48), Image.LANCZOS).quantize(16, dither=Image.NONE).convert('RGBA')
    mask = Image.new('L', small.size, 0)
    ImageDraw.Draw(mask).ellipse((1, 0, 30, 47), fill=255)
    small.putalpha(mask)
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    layer.paste(small, ((W - 32) // 2, 14), small)
    outline(layer)
    return layer


JOKERS = [  # (draw fn or None, bg, post-step)
    (die_rampe, (232, 150, 60), None),
    (None, None, None),                      # Classic Donnie (photo)
    (ihr_checkt, (150, 96, 200), None),
    (anyway, (80, 160, 170), None),
    (raketenstart, (40, 52, 96), None),
    (akkuschrauber, (200, 64, 56), None),
    (butlers, (226, 130, 160), None),
    (kaffee, (156, 104, 66), kaffee_steam),
    (osullivan, (40, 128, 72), None),
]

if __name__ == '__main__':
    cards = []
    for fn, bg, post in JOKERS:
        if fn is None:
            card = photo_card((120, 0, 560, 598), (255, 214, 160))
        else:
            card = render(fn, bg)
            if post:
                post(card)
        cards.append(card)
    cards.append(soul_head())
    sheet = Image.new('RGBA', (W * len(cards), H), (0, 0, 0, 0))
    for i, c in enumerate(cards):
        sheet.paste(c, (i * W, 0))
    sheet.save('batch5_jokers_1x.png')
    prev = Image.new('RGBA', (5 * (W * 3 + 6), 2 * (H * 3 + 6)), (40, 40, 40, 255))
    for i, c in enumerate(cards[:9]):
        big = c.resize((W * 3, H * 3), Image.NEAREST)
        if i == 8:
            big.alpha_composite(cards[9].resize((W * 3, H * 3), Image.NEAREST))
        prev.paste(big, ((i % 5) * (W * 3 + 6), (i // 5) * (H * 3 + 6)), big)
    prev.save('batch5_preview.png')
