"""Skip tag art: assets/1x/Tags.png and assets/2x/Tags.png (34x34 cells), plus tag_preview.png
into the current directory.
  x=0 Der Umzug: a taped moving box on a blue tag
"""
import os
from PIL import Image, ImageDraw

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
S = 34
OUTLINE = (52, 48, 60, 255)
WHITE = (255, 255, 255, 255)


def tag_base(col, col_d):
    """Luggage-tag silhouette: rounded body, clipped top corners, eyelet, dark + white outline."""
    img = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    body = [(9, 3), (24, 3), (30, 9), (30, 28), (27, 31), (6, 31), (3, 28), (3, 9)]
    d.polygon(body, fill=col)
    d.polygon([(3, 24), (30, 24), (30, 28), (27, 31), (6, 31), (3, 28)], fill=col_d)   # bottom shade
    d.ellipse((14, 5, 19, 10), fill=(214, 216, 226, 255))                             # metal eyelet
    d.rectangle((16, 7, 17, 8), fill=OUTLINE)
    outline(img)
    return img


def outline(img):
    p = img.load()
    solid = lambda x, y: 0 <= x < S and 0 <= y < S and p[x, y][3] > 0
    n4 = ((1, 0), (-1, 0), (0, 1), (0, -1))
    ring = [(x, y) for x in range(S) for y in range(S)
            if solid(x, y) and not all(solid(x + dx, y + dy) for dx, dy in n4)]
    for x, y in ring:
        p[x, y] = OUTLINE
    ring2 = [(x, y) for x in range(S) for y in range(S)
             if not solid(x, y) and any(solid(x + dx, y + dy) for dx, dy in n4)]
    for x, y in ring2:
        p[x, y] = WHITE


def umzug():
    img = tag_base((90, 120, 200, 255), (64, 90, 160, 255))
    d = ImageDraw.Draw(img)
    card, card_d, card_h = (206, 150, 92, 255), (160, 108, 60, 255), (230, 184, 128, 255)
    tape = (236, 220, 170, 255)
    d.polygon([(8, 15), (12, 12), (27, 12), (23, 15)], fill=card_h)                    # box lid
    d.rectangle((8, 15, 23, 28), fill=card)                                           # front
    d.polygon([(23, 15), (27, 12), (27, 25), (23, 28)], fill=card_d)                  # side
    d.rectangle((14, 15, 17, 28), fill=tape)                                          # tape strip
    d.polygon([(14, 15), (17, 15), (21, 12), (18, 12)], fill=tape)
    d.line((10, 25, 12, 25), fill=OUTLINE)                                            # "this side up"
    d.point((11, 24), fill=OUTLINE)
    for x, y in ((8, 15), (23, 15), (8, 28), (23, 28), (27, 12), (27, 25)):
        d.point((x, y), fill=OUTLINE)
    d.line((8, 15, 8, 28), fill=OUTLINE)
    d.line((8, 28, 23, 28), fill=OUTLINE)
    d.line((23, 28, 27, 25), fill=OUTLINE)
    d.line((27, 12, 27, 25), fill=OUTLINE)
    d.line((8, 15, 12, 12), fill=OUTLINE)
    d.line((12, 12, 27, 12), fill=OUTLINE)
    d.line((8, 15, 23, 15), fill=OUTLINE)
    d.line((23, 15, 23, 28), fill=OUTLINE)
    d.line((23, 15, 27, 12), fill=OUTLINE)
    return img


TAGS = [umzug]

if __name__ == '__main__':
    tags = [fn() for fn in TAGS]
    for scale in (1, 2):
        sheet = Image.new('RGBA', (S * scale * len(tags), S * scale), (0, 0, 0, 0))
        for i, t in enumerate(tags):
            sheet.paste(t.resize((S * scale, S * scale), Image.NEAREST), (i * S * scale, 0))
        sheet.save(os.path.join(ROOT, 'assets', f'{scale}x', 'Tags.png'))
    prev = Image.new('RGBA', (S * 8 * len(tags), S * 8), (60, 60, 70, 255))
    for i, t in enumerate(tags):
        big = t.resize((S * 8, S * 8), Image.NEAREST)
        prev.paste(big, (i * S * 8, 0), big)
    prev.save('tag_preview.png')
