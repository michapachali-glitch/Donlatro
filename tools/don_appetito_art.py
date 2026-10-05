"""Don Appetito: the Daunendonnie photo (pixelated, warm tint) holding a hand-drawn Kochlöffel.

Usage: python don_appetito_art.py <pixelated base card png>
(base = the photo card made like Daunendonnie's, see pixelize step in the session notes)
Writes don_appetito_1x.png and don_appetito_preview.png into the current directory.
"""
import os
import sys
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from food_art import outline  # noqa: E402

W, H = 71, 95


def spoon_layer():
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    wood, wood_d, wood_h = (196, 140, 86), (146, 98, 56), (226, 182, 128)
    d.line((30, 86, 52, 34), fill=wood, width=4)                               # handle
    d.line((31, 86, 53, 34), fill=wood_d, width=1)
    d.ellipse((47, 14, 61, 36), fill=wood)                                     # spoon bowl
    d.ellipse((50, 18, 58, 32), fill=wood_d)
    d.ellipse((50, 17, 54, 22), fill=wood_h)
    for x, y in ((55, 12), (58, 9), (52, 8)):                                  # steam / sauce drops
        d.point((x, y), fill=(250, 250, 250))
    outline(layer)
    return layer


if __name__ == '__main__':
    card = Image.open(sys.argv[1]).convert('RGBA')
    frame = card.getchannel('A')
    card.alpha_composite(spoon_layer())
    card.putalpha(Image.composite(card.getchannel('A'), frame, frame))         # keep spoon inside the card
    card.save('don_appetito_1x.png')
    card.resize((W * 5, H * 5), Image.NEAREST).save('don_appetito_preview.png')
