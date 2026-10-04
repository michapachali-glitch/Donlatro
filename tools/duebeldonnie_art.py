"""DübelDonnie: Donnie (head from the Daunendonnie photo) in his puffer jacket with a big joint.

Writes the card straight into assets/1x/Jokers.png and assets/2x/Jokers.png at cell x=9, y=1
(where the old "Anyway" sign was), plus duebeldonnie_preview.png into the current directory.
"""
import os
import sys
from PIL import Image, ImageDraw, ImageEnhance

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from food_art import card_base, add_letters, outline, W, H  # noqa: E402

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
PHOTO = os.path.join(ROOT, 'working', 'Daunendonnie.jpg')
CELL = (9, 1)
BG = (84, 150, 78)


def head():
    """Head cut out of the photo (with sunglasses), pixelated to 30x44."""
    src = Image.open(PHOTO).convert('RGB').crop((262, 10, 422, 250))
    src = ImageEnhance.Color(ImageEnhance.Contrast(src).enhance(1.25)).enhance(1.2)
    small = src.resize((30, 44), Image.LANCZOS).quantize(16, dither=Image.NONE).convert('RGBA')
    mask = Image.new('L', small.size, 0)
    ImageDraw.Draw(mask).ellipse((1, 0, 28, 43), fill=255)
    small.putalpha(mask)
    return small


def body(d):
    jacket, jacket_s, jacket_h = (226, 228, 230), (178, 182, 190), (246, 247, 250)
    d.rounded_rectangle((11, 62, 59, 100), 14, fill=jacket)                    # puffer jacket
    d.rounded_rectangle((25, 53, 46, 66), 5, fill=jacket)                      # high collar
    for y in (72, 81):                                                         # quilting
        d.line((12, y, 58, y), fill=jacket_s)
    d.line((35, 57, 35, 90), fill=jacket_s)                                    # zip
    d.line((15, 68, 15, 90), fill=jacket_h)
    d.line((55, 68, 55, 90), fill=jacket_s)
    d.rectangle((0, 89, W, H), fill=(0, 0, 0, 0))                              # cut off at the frame


def joint(d):
    paper, paper_s, filt = (250, 248, 240), (214, 208, 196), (222, 186, 132)
    d.polygon([(34, 43), (54, 32), (57, 39), (35, 46)], fill=paper)            # big cone
    d.line((35, 46, 57, 39), fill=paper_s)
    d.rectangle((31, 43, 34, 46), fill=filt)                                   # tip in mouth
    d.ellipse((53, 31, 59, 39), fill=(240, 90, 40))                            # ember
    d.point((55, 33), fill=(255, 210, 90))
    d.point((56, 35), fill=(255, 170, 60))


def smoke(card):
    d = ImageDraw.Draw(card)
    col = (236, 236, 244, 200)
    for x, y, r in ((55, 26, 3), (51, 19, 4), (55, 12, 3)):
        d.ellipse((x - r, y - r, x + r, y + r), fill=col)


def draw():
    card = card_base(BG)
    obj = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    body(ImageDraw.Draw(obj))
    h = head()
    obj.alpha_composite(h, (20, 9))
    joint(ImageDraw.Draw(obj))
    outline(obj)
    card.alpha_composite(obj)
    smoke(card)
    add_letters(card, BG)
    return card


if __name__ == '__main__':
    card = draw()
    x, y = CELL
    for scale in (1, 2):
        path = os.path.join(ROOT, 'assets', f'{scale}x', 'Jokers.png')
        sheet = Image.open(path).convert('RGBA')
        big = card.resize((W * scale, H * scale), Image.NEAREST)
        sheet.paste(big, (x * W * scale, y * H * scale))
        sheet.save(path)
    card.resize((W * 4, H * 4), Image.NEAREST).save('duebeldonnie_preview.png')
