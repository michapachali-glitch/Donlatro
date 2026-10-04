"""Pixel art for batch 6: 10 vouchers, 2 tarots, 3 spectrals, 2 deck backs, 2 boss chips.

Run from any directory; writes into the current directory:
  b6_vouchers_1x.png  (5 x 2 cells: tier 1 on row 0, tier 2 on row 1)
  b6_consumables_1x.png (5 cells: 2 tarots + 3 spectrals)
  b6_backs_1x.png     (2 cells)
  b6_blinds_1x.png    (2 rows x 21 frames)
  b6_preview.png
"""
import math
import os
import sys
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from food_art import W, H  # noqa: E402
from batch2_art import blind_strip, DARK  # noqa: E402
from batch3_art import boss_disc  # noqa: E402

VAN = r'C:\Users\User\AppData\Roaming\Balatro\vanilla-src\resources\textures\1x'
PHOTO = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'working', 'Daunendonnie.jpg')

FONT = {
    'A': ['.#.', '#.#', '###', '#.#', '#.#'], 'B': ['##.', '#.#', '##.', '#.#', '##.'],
    'C': ['.##', '#..', '#..', '#..', '.##'], 'D': ['##.', '#.#', '#.#', '#.#', '##.'],
    'E': ['###', '#..', '##.', '#..', '###'], 'F': ['###', '#..', '##.', '#..', '#..'],
    'G': ['.##', '#..', '#.#', '#.#', '.##'], 'H': ['#.#', '#.#', '###', '#.#', '#.#'],
    'I': ['###', '.#.', '.#.', '.#.', '###'], 'K': ['#.#', '#.#', '##.', '#.#', '#.#'],
    'L': ['#..', '#..', '#..', '#..', '###'], 'M': ['#.#', '###', '###', '#.#', '#.#'],
    'N': ['#.#', '###', '###', '###', '#.#'], 'O': ['.#.', '#.#', '#.#', '#.#', '.#.'],
    'P': ['##.', '#.#', '##.', '#..', '#..'], 'R': ['##.', '#.#', '##.', '#.#', '#.#'],
    'S': ['.##', '#..', '.#.', '..#', '##.'], 'T': ['###', '.#.', '.#.', '.#.', '.#.'],
    'U': ['#.#', '#.#', '#.#', '#.#', '###'], 'Z': ['###', '..#', '.#.', '#..', '###'],
    ' ': ['...', '...', '...', '...', '...'],
}


def text_width(s):
    return len(s) * 4 - 1


def draw_text(d, s, x, y, col):
    for ch in s:
        for j, row in enumerate(FONT[ch]):
            for i, c in enumerate(row):
                if c == '#':
                    d.point((x + i, y + j), fill=col)
        x += 4


def shade(c, f):
    return tuple(max(0, min(255, int(v * f))) for v in c[:3]) + (255,)


def outlined(draw_fn, col=(52, 48, 60, 255)):
    """draw an icon on its own layer and give it a 1px dark outline"""
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    draw_fn(ImageDraw.Draw(layer))
    src = layer.load()
    solid = lambda x, y: 0 <= x < W and 0 <= y < H and src[x, y][3] > 0
    ring = [(x, y) for x in range(W) for y in range(H) if not solid(x, y)
            and any(solid(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))]
    for p in ring:
        src[p] = col
    return layer


def cell(sheet, x, y):
    return Image.open(os.path.join(VAN, sheet)).convert('RGBA').crop((x * W, y * H, x * W + W, y * H + H))


# --- vouchers ----------------------------------------------------------------------------
def voucher(tier, colour, icon):
    t = cell('Vouchers.png', 0, tier - 1)     # Overstock (tier 1) / Overstock Plus (tier 2)
    p = t.load()
    counts = {}
    for y in range(30, 80):
        for x in range(8, 62):
            if p[x, y][3]:
                counts[p[x, y]] = counts.get(p[x, y], 0) + 1
    light, dark = sorted(sorted(counts, key=counts.get)[-2:], key=lambda c: -sum(c[:3]))
    base_lum = sum(light[:3])
    for y in range(H):
        for x in range(W):
            c = p[x, y]
            if c[3] and y >= 19 and (c == light or c == dark or abs(sum(c[:3]) - base_lum) < 120 and c[0] > c[2] + 30):
                p[x, y] = shade(colour, sum(c[:3]) / base_lum)
            if tier == 2 and c[3] and y < 21 and c[1] > 150 and c[2] < 120:   # header stripe
                p[x, y] = shade(colour, 1.25)
    d = ImageDraw.Draw(t)
    for y in range(24, 84):                                                  # wipe vanilla icon
        for x in range(10, 61):
            if p[x, y][3]:
                p[x, y] = shade(colour, 1.0 if x < 35 else 0.82)
    d.rounded_rectangle((14, 28, 56, 80), 3, outline=shade(colour, 1.35))
    t.alpha_composite(outlined(icon))
    return t


def ico_patreon(d):
    d.ellipse((20, 36, 50, 66), fill=(250, 200, 60))                        # coin
    d.ellipse((23, 39, 47, 63), fill=(232, 170, 40))
    d.polygon([(35, 58), (27, 49), (28, 44), (32, 43), (35, 46), (38, 43), (42, 44), (43, 49)],
              fill=(240, 80, 70))                                            # heart
    for x, y in ((18, 30), (52, 32), (50, 70)):
        d.point((x, y), fill=(255, 255, 255))


def ico_patreon_exklusiv(d):
    ico_patreon(d)
    d.polygon([(24, 32), (28, 24), (32, 30), (35, 22), (38, 30), (42, 24), (46, 32)], fill=(255, 220, 80))  # crown
    d.rectangle((24, 32, 46, 35), fill=(230, 180, 40))


def ico_couch(d):
    d.rounded_rectangle((16, 48, 54, 62), 3, fill=(150, 90, 70))             # couch
    d.rounded_rectangle((14, 42, 22, 64), 3, fill=(130, 76, 58))
    d.rounded_rectangle((46, 36, 56, 64), 3, fill=(130, 76, 58))
    d.rectangle((16, 64, 18, 70), fill=(80, 50, 40))
    d.rectangle((52, 64, 54, 70), fill=(80, 50, 40))
    d.ellipse((20, 42, 30, 50), fill=(240, 240, 250))                        # pillow
    d.rectangle((26, 26, 44, 34), fill=(255, 255, 255))                      # "1x" tag
    d.text((28, 25), '1x', fill=DARK)


def ico_kasse(d):
    d.rounded_rectangle((14, 36, 56, 66), 3, fill=(70, 170, 120))            # insurance card
    d.rectangle((14, 42, 56, 46), fill=(40, 120, 84))
    d.rounded_rectangle((18, 50, 28, 58), 1, fill=(240, 200, 80))            # chip
    d.line((23, 50, 23, 58), fill=(200, 150, 40))
    for y in (52, 56, 60):
        d.line((32, y, 50, y), fill=(220, 245, 230))
    d.text((24, 22), 'inf', fill=(255, 255, 255))


def ico_pill(d, a, b):
    d.rounded_rectangle((18, 44, 52, 60), 8, fill=a)                         # capsule
    d.rounded_rectangle((35, 44, 52, 60), 8, fill=b)
    d.rectangle((35, 44, 40, 60), fill=b)
    d.line((22, 47, 32, 47), fill=(255, 255, 255))


def ico_medikinet(d):
    ico_pill(d, (240, 240, 250), (60, 120, 220))


def ico_elvanse(d):
    d.polygon([(35, 26), (52, 32), (50, 54), (35, 66), (20, 54), (18, 32)], fill=(150, 120, 220))  # shield
    d.polygon([(35, 30), (48, 35), (46, 52), (35, 61)], fill=(120, 92, 196))
    ico_pill(d, (250, 240, 250), (220, 90, 160))


def ico_arcaden(d):
    d.rectangle((14, 40, 56, 72), fill=(230, 226, 214))                     # shop front
    d.rectangle((14, 34, 56, 40), fill=(220, 90, 60))                        # awning
    for x in range(14, 56, 6):
        d.rectangle((x, 34, x + 2, 40), fill=(255, 240, 220))
    d.rectangle((20, 48, 32, 72), fill=(90, 140, 190))                       # door
    d.rectangle((38, 48, 50, 60), fill=(150, 200, 230))                      # window
    d.text((40, 24), '+1', fill=(255, 255, 255))


def ico_erdgeschoss(d):
    d.rectangle((12, 32, 58, 74), fill=(226, 222, 210))                      # mall facade
    d.rectangle((12, 28, 58, 32), fill=(120, 120, 140))
    for i, x in enumerate((14, 25, 36, 47)):                                 # four shops
        col = [(220, 90, 60), (70, 160, 110), (80, 120, 210), (230, 180, 50)][i]
        d.rectangle((x, 36, x + 9, 40), fill=col)
        d.rectangle((x + 1, 44, x + 8, 58), fill=(150, 200, 230))
    d.rectangle((26, 62, 44, 74), fill=(90, 140, 190))                       # entrance
    d.line((35, 62, 35, 74), fill=(60, 100, 150))
    d.text((24, 18), '+2', fill=(255, 255, 255))


def ramp_shape(d, x0, y0, s, col, col_d):
    r = 30 * s
    curve = [(x0 + r * math.sin(math.radians(t)), y0 + r * math.cos(math.radians(t))) for t in range(0, 91, 10)]
    d.polygon(curve + [(x0 + r, y0 + r)], fill=col)
    d.line(curve, fill=col_d)


def ico_superrampe(d):
    ramp_shape(d, 16, 38, 1.2, (180, 182, 194), (130, 132, 146))
    d.rectangle((14, 74, 54, 76), fill=(130, 132, 146))


def ico_mini_superrampe(d):
    ico_superrampe(d)
    ramp_shape(d, 30, 56, 0.55, (230, 120, 70), (170, 80, 40))               # small ramp inside


VOUCHERS = [  # tier 1 / tier 2 pairs: colour, icon1, icon2
    ((240, 104, 90), ico_patreon, ico_patreon_exklusiv),
    ((70, 150, 150), ico_couch, ico_kasse),
    ((70, 110, 200), ico_medikinet, ico_elvanse),
    ((226, 140, 60), ico_arcaden, ico_erdgeschoss),
    ((130, 130, 150), ico_superrampe, ico_mini_superrampe),
]


# --- tarots / spectrals ------------------------------------------------------------------
def consumable(kind, label, art):
    """kind 'tarot' (Fool frame) or 'spectral' (Familiar frame); art(img) paints the window"""
    t = cell('Tarots.png', 0, 0 if kind == 'tarot' else 4)
    p = t.load()
    pal = {'tarot': ((246, 226, 180), (196, 160, 100), (90, 70, 50)),
           'spectral': ((200, 214, 236), (130, 150, 190), (70, 80, 110))}[kind]
    win = (9, 9, 61, 80) if kind == 'tarot' else (8, 8, 62, 78)
    win_img = Image.new('RGBA', (win[2] - win[0] + 1, win[3] - win[1] + 1), pal[0] + (255,))
    wd = ImageDraw.Draw(win_img)
    for y in range(win_img.height):                                          # soft gradient
        wd.line((0, y, win_img.width, y), fill=shade(pal[0], 1.0 - 0.25 * y / win_img.height))
    art(win_img)
    t.paste(win_img, win[:2])
    d = ImageDraw.Draw(t)
    by = 82 if kind == 'tarot' else 81
    d.rectangle((9, by, 61, by + 7), fill=pal[0])                            # name banner
    d.rectangle((9, by, 61, by + 7), outline=pal[2])
    draw_text(d, label, 35 - text_width(label) // 2, by + 2, pal[2])
    return t


def art_classic_donnie(img):
    photo = Image.open(PHOTO).convert('L').crop((150, 0, 530, 560))
    photo = ImageEnhance.Contrast(photo).enhance(1.4)
    small = photo.resize(img.size, Image.LANCZOS).filter(ImageFilter.SHARPEN).quantize(6, dither=Image.NONE).convert('L')
    sp, ip = small.load(), img.load()
    for y in range(img.height):
        for x in range(img.width):
            v = sp[x, y] / 255
            ip[x, y] = (int(110 + 140 * v), int(80 + 140 * v), int(50 + 120 * v), 255)


def art_therapie(img):
    img.alpha_composite(outlined_small(img.size, lambda d: (
        d.rounded_rectangle((8, 40, 46, 54), 3, fill=(150, 90, 70)),
        d.rounded_rectangle((6, 34, 14, 56), 3, fill=(130, 76, 58)),
        d.ellipse((12, 34, 22, 42), fill=(240, 240, 250)),
        d.polygon([(30, 30), (22, 20), (23, 14), (28, 13), (30, 16), (32, 13), (37, 14), (38, 20)], fill=(230, 70, 80)),
    )))


def outlined_small(size, fn):
    layer = Image.new('RGBA', size, (0, 0, 0, 0))
    fn(ImageDraw.Draw(layer))
    src = layer.load()
    w, h = size
    solid = lambda x, y: 0 <= x < w and 0 <= y < h and src[x, y][3] > 0
    ring = [(x, y) for x in range(w) for y in range(h) if not solid(x, y)
            and any(solid(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))]
    for q in ring:
        src[q] = (52, 48, 60, 255)
    return layer


def art_rueckspul(img):
    img.alpha_composite(outlined_small(img.size, lambda d: (
        d.ellipse((6, 14, 48, 56), fill=(60, 70, 110)),
        d.polygon([(26, 25), (12, 35), (26, 45)], fill=(250, 250, 255)),
        d.polygon([(40, 25), (26, 35), (40, 45)], fill=(250, 250, 255)),
        d.arc((2, 10, 52, 60), 200, 340, fill=(250, 220, 90), width=2),
    )))


def art_eingeschissen(img):
    def fn(d):
        brown, brown_d = (130, 80, 46), (96, 58, 32)
        d.ellipse((10, 46, 44, 62), fill=brown_d)
        d.ellipse((12, 44, 42, 58), fill=brown)
        d.ellipse((16, 34, 38, 48), fill=brown)
        d.ellipse((20, 24, 34, 38), fill=brown)
        d.polygon([(26, 16), (24, 26), (32, 26)], fill=brown)
        d.ellipse((19, 38, 25, 44), fill=(255, 255, 255))
        d.ellipse((29, 38, 35, 44), fill=(255, 255, 255))
        d.point((22, 41), fill=DARK)
        d.point((32, 41), fill=DARK)
        d.arc((20, 46, 34, 54), 20, 160, fill=DARK)
    img.alpha_composite(outlined_small(img.size, fn))
    d = ImageDraw.Draw(img)
    for x, y in ((8, 10), (46, 14), (44, 52), (6, 40)):                      # negative sparkles
        d.line((x - 2, y, x + 2, y), fill=(240, 90, 200))
        d.line((x, y - 2, x, y + 2), fill=(240, 90, 200))


def art_unsicherheit(img):
    def fn(d):
        d.rounded_rectangle((8, 16, 30, 48), 2, fill=(240, 240, 250))       # joker slots
        d.rounded_rectangle((24, 20, 46, 52), 2, fill=(220, 220, 236))
        d.text((32, 30), '?', fill=DARK)
        d.text((16, 26), '+1', fill=(70, 160, 90))
    img.alpha_composite(outlined_small(img.size, fn))
    d = ImageDraw.Draw(img)
    for x in (6, 50):                                                        # wobble lines
        d.line((x, 24, x - 2, 30), fill=(90, 100, 140))
        d.line((x - 2, 30, x, 36), fill=(90, 100, 140))


CONSUMABLES = [
    ('tarot', 'DONNIE', art_classic_donnie),
    ('tarot', 'THERAPIE', art_therapie),
    ('spectral', 'RUECKSPUL', art_rueckspul),
    ('spectral', 'EINGESCHISSEN', art_eingeschissen),
    ('spectral', 'UNSICHERHEIT', art_unsicherheit),
]


# --- deck backs --------------------------------------------------------------------------
def back(colour, emblem):
    t = cell('Enhancers.png', 0, 0)                                          # Red Deck back
    p = t.load()
    ref = max(((p[x, y], 0) for x in range(W) for y in range(H) if p[x, y][3] and p[x, y][1] < 150),
              key=lambda c: sum(c[0][:3]))[0]
    for y in range(H):
        for x in range(W):
            c = p[x, y]
            if c[3] and not (c[0] > 240 and c[1] > 240 and c[2] > 240):
                p[x, y] = shade(colour, sum(c[:3]) / max(1, sum(ref[:3])))
    d = ImageDraw.Draw(t)
    d.ellipse((19, 31, 51, 63), fill=(255, 255, 255))
    d.ellipse((21, 33, 49, 61), fill=shade(colour, 0.85))
    t.alpha_composite(outlined(emblem))
    return t


def emb_adhs(d):
    d.line([(25, 40), (29, 36), (32, 42), (36, 35), (39, 42), (43, 37), (46, 41)], fill=(255, 245, 140), width=2)
    d.line([(24, 54), (28, 49), (31, 56), (35, 50), (38, 57), (42, 51), (45, 55)], fill=(255, 245, 140), width=2)


def emb_frustsuppe(d):
    d.pieslice((24, 38, 46, 60), 0, 180, fill=(240, 240, 236))
    d.ellipse((24, 45, 46, 52), fill=(126, 132, 58))
    d.line((30, 46, 33, 48), fill=(56, 58, 24))
    d.line((40, 46, 37, 48), fill=(56, 58, 24))


BACKS = [((214, 196, 52), emb_adhs), ((112, 100, 134), emb_frustsuppe)]


# --- boss chips --------------------------------------------------------------------------
def flusen_glyph(d, ink):
    d.rounded_rectangle((8, 9, 26, 25), 3, outline=ink, width=2)             # lint screen
    for x in range(11, 25, 3):
        d.line((x, 11, x, 23), fill=ink)
    for x, y in ((13, 16), (19, 13), (22, 19)):                              # lint balls
        d.ellipse((x - 1, y - 1, x + 1, y + 1), fill=ink)


def folge_glyph(d, ink):
    d.rectangle((7, 8, 27, 24), outline=ink, width=2)                        # screen
    d.line((13, 27, 21, 27), fill=ink, width=2)
    d.text((10, 10), '#?', fill=ink)


if __name__ == '__main__':
    vsheet = Image.new('RGBA', (W * 5, H * 2), (0, 0, 0, 0))
    for i, (col, i1, i2) in enumerate(VOUCHERS):
        vsheet.paste(voucher(1, col, i1), (i * W, 0))
        vsheet.paste(voucher(2, col, i2), (i * W, H))
    vsheet.save('b6_vouchers_1x.png')
    csheet = Image.new('RGBA', (W * 5, H), (0, 0, 0, 0))
    for i, (kind, label, art) in enumerate(CONSUMABLES):
        csheet.paste(consumable(kind, label, art), (i * W, 0))
    csheet.save('b6_consumables_1x.png')
    bsheet = Image.new('RGBA', (W * 2, H), (0, 0, 0, 0))
    for i, (col, emb) in enumerate(BACKS):
        bsheet.paste(back(col, emb), (i * W, 0))
    bsheet.save('b6_backs_1x.png')
    chips = [boss_disc((150, 150, 166), flusen_glyph), boss_disc((206, 96, 70), folge_glyph)]
    blinds = Image.new('RGBA', (34 * 21, 68), (0, 0, 0, 0))
    for j, chip in enumerate(chips):
        blinds.paste(blind_strip(chip), (0, j * 34))
    blinds.save('b6_blinds_1x.png')
    # preview: vouchers (2 rows), consumables + backs, chips
    s = 3
    prev = Image.new('RGBA', (7 * (W * s + 6), 3 * (H * s + 6)), (40, 40, 40, 255))
    prev.paste(vsheet.resize((W * 5 * s, H * 2 * s), Image.NEAREST), (0, 0))
    row2 = Image.new('RGBA', (W * 7, H), (0, 0, 0, 0))
    row2.paste(csheet, (0, 0))
    row2.paste(bsheet, (W * 5, 0))
    prev.alpha_composite(row2.resize((W * 7 * s, H * s), Image.NEAREST), (0, 2 * H * s + 12))
    for j, chip in enumerate(chips):
        prev.alpha_composite(chip.resize((34 * 4, 34 * 4), Image.NEAREST), (W * 5 * s + 20, 20 + j * 150))
    prev.save('b6_preview.png')
