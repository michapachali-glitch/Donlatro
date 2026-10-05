"""Stoned Card: the vanilla Stone Card texture with a pixel cannabis leaf and a little smoke.
Writes stoned_1x.png and stoned_preview.png into the current directory.
"""
import math
import os
import sys
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from food_art import outline  # noqa: E402

W, H = 71, 95
VANILLA = r'C:\Users\User\AppData\Roaming\Balatro\vanilla-src\resources\textures\1x\Enhancers.png'


def leaf(d, cx, cy, size, col, vein):
    # 7 serrated leaflets fanning upwards; the middle one is the longest
    for i, ang in enumerate((-90, -58, -122, -28, -152, -5, -175)):
        length = size * (1.0, 0.85, 0.85, 0.65, 0.65, 0.42, 0.42)[i]
        a = math.radians(ang)
        tip = (cx + length * math.cos(a), cy + length * math.sin(a))
        n = (-math.sin(a), math.cos(a))                       # normal for the leaflet width
        w = size * 0.085
        pts = [(cx, cy)]
        steps = 6
        for s in range(1, steps):                             # serrated left edge
            t = s / steps
            k = w * math.sin(math.pi * t) * (1.25 if s % 2 else 0.85)
            pts.append((cx + (tip[0] - cx) * t + n[0] * k, cy + (tip[1] - cy) * t + n[1] * k))
        pts.append(tip)
        for s in range(steps - 1, 0, -1):                     # serrated right edge
            t = s / steps
            k = w * math.sin(math.pi * t) * (1.25 if s % 2 else 0.85)
            pts.append((cx + (tip[0] - cx) * t - n[0] * k, cy + (tip[1] - cy) * t - n[1] * k))
        d.polygon(pts, fill=col)
        d.line((cx, cy, tip[0], tip[1]), fill=vein)
    d.line((cx, cy, cx, cy + size * 0.35), fill=vein, width=2)   # stem


def render():
    card = Image.open(VANILLA).convert('RGBA').crop((5 * W, 0, 6 * W, H))   # vanilla Stone Card
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    leaf(ImageDraw.Draw(layer), 35, 60, 28, (64, 168, 72), (40, 118, 52))
    outline(layer)
    card.alpha_composite(layer)
    d = ImageDraw.Draw(card)
    for i, (x, y) in enumerate(((44, 20), (47, 15), (44, 10), (48, 6))):         # drifting smoke
        r = 2 + i
        d.ellipse((x - r, y - r, x + r, y + r), outline=(236, 236, 240, 200))
    return card


if __name__ == '__main__':
    card = render()
    card.save('stoned_1x.png')
    card.resize((W * 5, H * 5), Image.NEAREST).save('stoned_preview.png')
