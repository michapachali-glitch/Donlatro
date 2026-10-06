""""BANNED" stamp for cards banned by Die Mods (sticker donl_banned).

Writes the stamp into assets/1x/Stickers.png and assets/2x/Stickers.png at cell x=1, y=0
(widening the sheets if needed), plus banned_preview.png into the current directory.
"""
import os
from PIL import Image, ImageDraw

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
W, H = 71, 95
CELL = (1, 0)
RED = (206, 34, 40, 235)

FONT = {
    'B': ['##.', '#.#', '##.', '#.#', '##.'],
    'A': ['.#.', '#.#', '###', '#.#', '#.#'],
    'N': ['#..#', '##.#', '#.##', '#..#', '#..#'],
    'E': ['###', '#..', '##.', '#..', '###'],
    'D': ['##.', '#.#', '#.#', '#.#', '##.'],
}


def stamp():
    img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    x0, y0, x1, y1 = 7, 38, 63, 56
    d.rectangle((x0, y0, x1, y1), outline=RED, width=2)                       # stamp frame
    x = 11
    for ch in 'BANNED':                                                       # 2x pixel letters
        for j, row in enumerate(FONT[ch]):
            for i, c in enumerate(row):
                if c == '#':
                    d.rectangle((x + 2 * i, 42 + 2 * j, x + 2 * i + 1, 43 + 2 * j), fill=RED)
        x += 2 * len(FONT[ch][0]) + 2
    # worn ink: knock a few pixels out so it reads as a rubber stamp
    p = img.load()
    for k in range(0, W * H, 37):
        px, py = (k * 7) % W, k // W
        if p[px, py][3]:
            p[px, py] = (0, 0, 0, 0)
    return img


if __name__ == '__main__':
    card = stamp()
    x, y = CELL
    for scale in (1, 2):
        path = os.path.join(ROOT, 'assets', f'{scale}x', 'Stickers.png')
        old = Image.open(path).convert('RGBA')
        sheet = Image.new('RGBA', (max(old.width, (x + 1) * W * scale), max(old.height, (y + 1) * H * scale)))
        sheet.paste(old, (0, 0))
        sheet.paste(card.resize((W * scale, H * scale), Image.NEAREST), (x * W * scale, y * H * scale))
        sheet.save(path)
    card.resize((W * 4, H * 4), Image.NEAREST).save('banned_preview.png')
