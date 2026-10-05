"""Batch 8: Rampen-Karte enhancement, the 'Rampenfieber' tarot and the renamed 'Zocker' spectral.

Writes into the current directory:
  rampe_enh_1x.png       (1 cell: enhancement card background; rank/suit are drawn on top by the game)
  b8_consumables_1x.png  (2 cells: Zocker spectral, Rampenfieber tarot)
"""
import math
import os
import sys
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from batch6_art import consumable, art_unsicherheit, outlined_small, cell, W, H  # noqa: E402


def rampe_enhancement():
    card = cell('Enhancers.png', 1, 0).copy()                       # blank white base card
    p = card.load()
    d = ImageDraw.Draw(card)
    # light blue frame inside the card edge (like other enhancements)
    for y in range(H):
        for x in range(W):
            if p[x, y][3] and (x in (3, 4, W - 5, W - 4) or y in (4, 5, H - 6, H - 5)) and 3 <= x <= W - 4 and 4 <= y <= H - 5:
                p[x, y] = (120, 180, 230, 255)
    # a quarter-pipe ramp in the lower half, behind where the suit pips sit
    r, cx, cy = 30, 20, 58
    curve = [(cx + r * math.sin(math.radians(t)), cy + r * math.cos(math.radians(t)) - r) for t in range(0, 91, 10)]
    d.polygon(curve + [(cx + r, cy)], fill=(250, 196, 140))
    d.line(curve, fill=(226, 130, 60), width=2)
    d.line((cx, cy, cx + r, cy), fill=(226, 130, 60), width=2)
    d.rectangle((cx + r - 1, cy - r - 2, cx + r + 3, cy - r), fill=(226, 130, 60))   # coping
    return card


def art_rampenfieber(img):
    def fn(d):
        d.polygon([(26, 2), (34, 2), (52, 64), (8, 64)], fill=(255, 246, 200))     # spotlight
        r = 22
        curve = [(10 + r * math.sin(math.radians(t)), 64 + r * math.cos(math.radians(t)) - r) for t in range(0, 91, 10)]
        d.polygon(curve + [(10 + r, 64)], fill=(220, 150, 90))                     # ramp on stage
        d.rectangle((2, 64, 52, 68), fill=(150, 100, 60))                          # stage floor
        d.ellipse((32, 30, 40, 38), fill=(240, 200, 170))                          # nervous performer
        d.rectangle((33, 38, 39, 52), fill=(90, 80, 140))
        for x, y in ((28, 30), (44, 32)):
            d.line((x, y, x, y + 3), fill=(120, 180, 240))                         # sweat drops
    img.alpha_composite(outlined_small(img.size, fn))


if __name__ == '__main__':
    rampe_enhancement().save('rampe_enh_1x.png')
    sheet = Image.new('RGBA', (W * 2, H), (0, 0, 0, 0))
    sheet.paste(consumable('spectral', 'ZOCKER', art_unsicherheit), (0, 0))
    sheet.paste(consumable('tarot', 'RAMPENFIEBER', art_rampenfieber), (W, 0))
    sheet.save('b8_consumables_1x.png')
    prev = Image.new('RGBA', (W * 3 * 4 + 16, H * 4), (40, 40, 40, 255))
    prev.paste(rampe_enhancement().resize((W * 4, H * 4), Image.NEAREST), (0, 0))
    prev.paste(sheet.resize((W * 8, H * 4), Image.NEAREST), (W * 4 + 16, 0))
    prev.save('b8_preview.png')
