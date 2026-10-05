"""Donnie Pack cover: Daunendonnie (from the photo, with his sunglasses) wearing a jester
crown, on a booster pack (foil strips taken from the vanilla Buffoon pack).

Usage: python pack_art.py <m6x11plus.ttf>
Writes donnie_pack_1x.png and donnie_pack_preview.png into the current directory.
"""
import os
import sys
from PIL import Image, ImageDraw, ImageEnhance, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from food_art import outline  # noqa: E402

W, H = 71, 95
HERE = os.path.dirname(os.path.abspath(__file__))
PHOTO = os.path.join(HERE, '..', 'working', 'Daunendonnie.jpg')
VANILLA = r'C:\Users\User\AppData\Roaming\Balatro\vanilla-src\resources\textures\1x\boosters.png'
DARK = (40, 30, 56, 255)


def body_mask(ref):
    p = ref.load()
    return {(x, y) for x in range(W) for y in range(10, 85) if p[x, y][3]}


def donnie_head():
    head = Image.open(PHOTO).convert('RGB').crop((262, 10, 422, 250))
    head = ImageEnhance.Contrast(head).enhance(1.2)
    small = head.resize((30, 44), Image.LANCZOS).quantize(14, dither=Image.NONE).convert('RGBA')
    mask = Image.new('L', small.size, 0)
    ImageDraw.Draw(mask).ellipse((1, 0, 28, 43), fill=255)
    small.putalpha(mask)
    return small


def jester_hat(d, cx, top):
    red, blue, gold = (226, 64, 60), (60, 120, 220), (250, 200, 60)
    d.polygon([(cx - 15, top + 16), (cx - 22, top + 2), (cx - 6, top + 10)], fill=red)     # left point
    d.polygon([(cx + 15, top + 16), (cx + 22, top + 2), (cx + 6, top + 10)], fill=blue)    # right point
    d.polygon([(cx - 8, top + 14), (cx, top - 2), (cx + 8, top + 14)], fill=(250, 150, 50))  # middle point
    d.rectangle((cx - 16, top + 13, cx + 16, top + 17), fill=gold)                         # band
    for bx, by in ((cx - 22, top + 2), (cx + 22, top + 2), (cx, top - 2)):
        d.ellipse((bx - 2, by - 2, bx + 2, by + 2), fill=gold)                             # bells


def render(font_path):
    ref = Image.open(VANILLA).convert('RGBA').crop((0, 8 * H, W, 9 * H))          # Buffoon pack
    rp = ref.load()
    card = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    cp = card.load()
    for y in list(range(0, 10)) + list(range(85, H)):                            # foil strips
        for x in range(W):
            cp[x, y] = rp[x, y]
    mask = body_mask(ref)
    edge = {(x, y) for (x, y) in mask if any((x + dx, y + dy) not in mask for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
            and 10 < y < 84}
    for (x, y) in mask:                                                          # purple body
        t = (y - 10) / 75
        cp[x, y] = (int(120 - 50 * t), int(70 - 30 * t), int(170 - 40 * t), 255)
    for (x, y) in edge:
        cp[x, y] = DARK
    d = ImageDraw.Draw(card)
    for i, (x, y) in enumerate(((16, 20), (55, 26), (20, 50), (52, 52), (34, 14))):  # sparkles
        d.point((x, y), fill=(255, 230, 140))
    # Donnie + hat (outlined like the cards)
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    layer.paste(donnie_head(), (20, 19), donnie_head())
    jester_hat(ImageDraw.Draw(layer), 35, 9)
    outline(layer)
    card.alpha_composite(layer)
    # label
    d.rounded_rectangle((10, 63, 60, 81), 3, fill=(250, 200, 60), outline=DARK)
    font = ImageFont.truetype(font_path, 11)
    for text, y in (('DONNIE', 63), ('PACK', 71)):
        tw = d.textlength(text, font=font)
        x = (W - tw) / 2
        for ox, oy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            d.text((x + ox, y + oy), text, font=font, fill=DARK)
        d.text((x, y), text, font=font, fill=(255, 255, 255))
    return card


if __name__ == '__main__':
    card = render(sys.argv[1])
    card.save('donnie_pack_1x.png')
    card.resize((W * 5, H * 5), Image.NEAREST).save('donnie_pack_preview.png')
