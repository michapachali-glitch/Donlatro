"""Draws Donlatro food jokers as pixel art in the vanilla food-joker card style."""
from PIL import Image, ImageDraw

REF = r'C:\Users\User\AppData\Roaming\Balatro\vanilla-src\resources\textures\1x\Jokers.png'  # vanilla sheet (template source)
W, H = 71, 95
WHITE = (255, 255, 255, 255)
OUTLINE = (52, 48, 60, 255)
ref_sheet = Image.open(REF).convert('RGBA')
ramen = ref_sheet.crop((2 * 71, 15 * 95, 3 * 71, 16 * 95))
rp = ramen.load()
FRAME = rp[5, 1]
LETTER_OUT = rp[9, 6]

# letter mask: top-left JOKER glyphs (white fill + dark outline) inside x 3..12, y 5..53
letters = {}
for y in range(5, 54):
    for x in range(3, 13):
        v = rp[x, y]
        if x >= 4 and v[:3] == (255, 255, 255):
            letters[(x, y)] = 'fill'
        elif v == LETTER_OUT:
            letters[(x, y)] = 'out'
for (x, y), k in list(letters.items()):
    letters[(W - 1 - x, H - 1 - y)] = k  # rotated copy, bottom-right


def shade(c, f):
    return tuple(max(0, min(255, int(v * f))) for v in c[:3]) + (255,)


def card_base(bg):
    img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    p = img.load()
    for y in range(H):
        for x in range(W):
            v = rp[x, y]
            if v[3] == 0:
                continue
            edge = x <= 3 or x >= W - 4 or y <= 3 or y >= H - 4
            if v == FRAME or (v[:3] == (255, 255, 255) and edge):
                p[x, y] = v  # outer ring + white inner border
            else:
                band = (y // 6) % 2
                p[x, y] = shade(bg, 1.12 - 0.3 * y / H + (0.04 if band else 0))
    return img


def add_letters(img, bg):
    p = img.load()
    dark = shade(bg, 0.45)
    for (x, y), k in letters.items():
        p[x, y] = WHITE if k == 'fill' else dark


def outline(obj):
    """vanilla look: 1px dark outline hugging the object, then 1px white outside it."""
    src = obj.load()
    w, h = obj.size
    solid = lambda x, y: 0 <= x < w and 0 <= y < h and src[x, y][3] > 0
    n4 = ((1, 0), (-1, 0), (0, 1), (0, -1))
    n8 = n4 + ((1, 1), (1, -1), (-1, 1), (-1, -1))
    ring1 = [(x, y) for x in range(w) for y in range(h)
             if not solid(x, y) and any(solid(x + dx, y + dy) for dx, dy in n4)]
    for x, y in ring1:
        src[x, y] = OUTLINE
    ring2 = [(x, y) for x in range(w) for y in range(h)
             if not solid(x, y) and any(solid(x + dx, y + dy) for dx, dy in n8)]
    for x, y in ring2:
        src[x, y] = WHITE


def glyph(d, rows, x0, y0, col):
    for j, row in enumerate(rows):
        for i, ch in enumerate(row):
            if ch == '#':
                d.point((x0 + i, y0 + j), fill=col)


# --- the foods ---------------------------------------------------------------------------
def sosse(d):
    cream, cream_s, cream_h = (246, 238, 214), (214, 200, 168), (255, 253, 244)
    red, red_s = (222, 62, 48), (170, 40, 34)
    d.polygon([(28, 34), (42, 34), (46, 40), (24, 40)], fill=cream)            # shoulder
    d.rounded_rectangle((24, 38, 46, 81), 3, fill=cream)                       # body
    d.rectangle((41, 40, 45, 79), fill=cream_s)
    d.rectangle((26, 41, 27, 76), fill=cream_h)
    d.rectangle((29, 25, 41, 33), fill=red)                                    # cap
    d.rectangle((38, 25, 41, 33), fill=red_s)
    d.polygon([(32, 25), (38, 25), (36, 15), (34, 15)], fill=red)              # nozzle
    d.line((37, 24, 36, 16), fill=red_s)
    d.ellipse((33, 9, 37, 13), fill=cream)                                     # sauce drop
    d.rectangle((26, 48, 44, 70), fill=red)                                    # label
    d.rectangle((26, 48, 44, 49), fill=red_s)
    d.rectangle((26, 69, 44, 70), fill=red_s)
    glyph(d, ['.###.', '#...#', '#..#.', '#.#..', '#..#.', '#...#', '#...#', '#.##.', '#....'],
          33, 54, (255, 255, 255))                                             # "ß"


def doener(d):
    bread, bread_s, bread_h = (226, 176, 104), (178, 120, 60), (246, 216, 156)
    meat, meat_d, meat_h = (150, 84, 42), (100, 54, 26), (186, 116, 64)
    d.ellipse((14, 16, 58, 44), fill=meat)                                     # meat heap
    for i, x in enumerate(range(16, 57, 3)):                                   # shaved strips
        y = 22 + (i % 3) * 2
        d.line((x, y, x + 2, 40), fill=meat_d)
        d.point((x + 1, y + 1), fill=meat_h)
    for x, y in ((14, 30), (20, 20), (52, 21), (58, 31), (36, 14)):             # lettuce
        d.polygon([(x - 4, y + 5), (x - 1, y - 3), (x + 4, y + 4), (x, y + 6)], fill=(110, 192, 68))
        d.point((x, y + 1), fill=(176, 232, 112))
    for x, y in ((26, 22), (44, 24), (34, 30)):                                # tomato slices
        d.ellipse((x - 3, y - 3, x + 3, y + 3), fill=(222, 58, 46))
        d.point((x, y), fill=(255, 150, 130))
    for x, y in ((22, 31), (48, 32)):                                          # red onion rings
        d.arc((x - 4, y - 3, x + 4, y + 3), 180, 360, fill=(180, 84, 172))
    d.line([(15, 36), (20, 33), (25, 37), (30, 33), (35, 37), (40, 33), (45, 37), (50, 33), (56, 36)],
           fill=(250, 250, 244), width=2)                                      # white sauce
    d.pieslice((-22, 28, 94, 144), 248, 292, fill=bread_s)                     # bread wedge, point down
    d.pieslice((-19, 31, 91, 141), 249, 291, fill=bread)
    d.arc((-22, 28, 94, 144), 249, 291, fill=bread_h, width=3)                 # top crust rim
    for x, y in ((30, 50), (40, 52), (35, 60), (28, 66), (43, 64), (36, 73)):  # sesame
        d.point((x, y), fill=(252, 238, 204))


def holy_energy(d):
    """Slim energy-drink can: tapered top and bottom, ring pull, "HOLY" label, bolt, halo."""
    can, can_s, can_h = (60, 196, 120), (34, 136, 84), (170, 240, 200)
    metal, metal_s, metal_h = (206, 210, 220), (140, 148, 164), (240, 242, 248)
    gold, gold_s = (255, 210, 64), (214, 150, 30)
    dark = (30, 34, 44)
    d.ellipse((25, 5, 45, 11), outline=gold, width=2)                          # halo
    d.polygon([(28, 18), (42, 18), (46, 24), (24, 24)], fill=metal)             # tapered neck
    d.polygon([(42, 18), (46, 24), (43, 24)], fill=metal_s)
    d.ellipse((28, 15, 42, 20), fill=metal_s)                                  # lid
    d.ellipse((30, 16, 40, 19), fill=metal)
    d.ellipse((32, 15, 37, 18), outline=metal_h)                               # ring pull
    d.rectangle((24, 24, 46, 78), fill=can)                                    # body
    d.rectangle((42, 24, 46, 78), fill=can_s)
    d.rectangle((26, 26, 27, 76), fill=can_h)
    d.rectangle((24, 30, 46, 39), fill=dark)                                   # label band
    x = 28
    for ch in ('#.#', '#.#', '###', '#.#', '#.#'), ('###', '#.#', '#.#', '#.#', '###'),               ('#..', '#..', '#..', '#..', '###'), ('#.#', '#.#', '.#.', '.#.', '.#.'):
        glyph(d, ch, x, 32, gold)                                              # H O L Y
        x += 4
    d.polygon([(38, 42), (29, 59), (35, 59), (31, 74), (43, 54), (37, 54), (41, 42)], fill=gold)
    d.line((38, 43, 30, 58), fill=(255, 245, 170))
    d.line((41, 43, 37, 53), fill=gold_s)
    d.polygon([(24, 78), (46, 78), (43, 84), (27, 84)], fill=metal)            # tapered base
    d.polygon([(43, 78), (46, 78), (43, 84), (41, 84)], fill=metal_s)
    for x, y in ((29, 44), (44, 64), (27, 70), (45, 46)):                      # condensation
        d.point((x, y), fill=(230, 255, 240))
        d.point((x, y + 1), fill=(200, 245, 220))


def maggi(d):
    glass, glass_s, glass_h = (70, 40, 26), (44, 24, 16), (128, 82, 50)
    yellow, yellow_s, red, red_s = (252, 204, 40), (214, 160, 20), (216, 40, 38), (160, 26, 26)
    d.polygon([(31, 34), (39, 34), (46, 46), (24, 46)], fill=glass)           # shoulders
    d.rectangle((24, 46, 46, 83), fill=glass)                                  # body
    d.rectangle((42, 46, 46, 83), fill=glass_s)
    d.rectangle((31, 19, 39, 34), fill=glass)                                  # neck
    d.rectangle((26, 47, 27, 80), fill=glass_h)
    d.rectangle((32, 20, 32, 33), fill=glass_h)
    d.rectangle((30, 11, 40, 19), fill=red)                                    # cap
    d.rectangle((37, 11, 40, 19), fill=red_s)
    d.rectangle((30, 11, 40, 12), fill=yellow)
    d.rectangle((31, 25, 39, 29), fill=yellow)                                 # neck label
    d.polygon([(35, 52), (45, 63), (35, 74), (25, 63)], fill=yellow)           # diamond label
    d.polygon([(41, 59), (45, 63), (41, 67)], fill=yellow_s)
    d.rectangle((27, 60, 43, 66), fill=red)                                    # red band
    glyph(d, ['#...#', '##.##', '#.#.#', '#...#', '#...#'], 33, 61, (255, 255, 255))  # "M"


def maultaschen(d):
    plate, plate_s, plate_h = (232, 238, 246), (176, 188, 206), (255, 255, 255)
    pasta, pasta_s, pasta_h = (242, 214, 140), (206, 164, 86), (252, 236, 186)
    d.ellipse((14, 56, 58, 82), fill=plate_s)                                  # plate
    d.ellipse((14, 54, 58, 79), fill=plate)
    d.ellipse((20, 58, 52, 75), fill=plate_h)

    def pocket(x0, y0, x1, y1):
        d.rectangle((x0, y0, x1, y1), fill=pasta)
        d.rectangle((x0, y1 - 2, x1, y1), fill=pasta_s)
        d.rectangle((x0 + 1, y0 + 1, x1 - 4, y0 + 2), fill=pasta_h)
        for x in range(x0, x1 + 1, 2):                                         # crimped edges
            d.point((x, y0), fill=pasta_s)
            d.point((x, y1), fill=pasta_s)
        for y in range(y0, y1 + 1, 2):
            d.point((x0, y), fill=pasta_s)
            d.point((x1, y), fill=pasta_s)

    pocket(18, 40, 34, 58)
    pocket(37, 38, 53, 56)
    pocket(26, 52, 46, 70)
    d.rectangle((27, 60, 45, 62), fill=(120, 150, 70))                         # cut: spinach filling
    d.rectangle((27, 60, 45, 60), fill=(150, 110, 70))
    for x, y in ((22, 44), (30, 46), (42, 42), (49, 47), (35, 55), (40, 66)):  # parsley
        d.point((x, y), fill=(70, 150, 60))
        d.point((x + 1, y), fill=(110, 190, 80))


def sauerteigbrot(d):
    crust, crust_d, crust_h = (184, 112, 56), (130, 74, 36), (216, 150, 84)
    score, flour = (240, 206, 146), (250, 246, 236)
    d.ellipse((14, 38, 58, 80), fill=crust_d)                                  # loaf
    d.ellipse((14, 34, 58, 76), fill=crust)
    d.ellipse((19, 37, 46, 56), fill=crust_h)
    d.arc((22, 38, 50, 74), 200, 340, fill=score, width=2)                     # scoring (ear)
    for i in range(4):                                                         # wheat-ear cuts
        x = 24 + i * 7
        d.line((x, 60, x + 4, 54), fill=score)
        d.line((x + 1, 61, x + 5, 55), fill=crust_d)
    for x, y in ((20, 45), (27, 40), (33, 43), (41, 39), (48, 44), (52, 51), (24, 52), (38, 48)):
        d.point((x, y), fill=flour)                                            # flour dust


FOODS = [  # key, draw fn, background
    ('sosse', sosse, (238, 166, 40)),
    ('doener', doener, (214, 70, 60)),
    ('holyenergy', holy_energy, (128, 90, 200)),
    ('maggi', maggi, (240, 200, 70)),
    ('maultaschen', maultaschen, (84, 160, 110)),
    ('sauerteigbrot', sauerteigbrot, (90, 150, 210)),
]


def render(draw_fn, bg):
    card = card_base(bg)
    obj = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    draw_fn(ImageDraw.Draw(obj))
    outline(obj)
    card.alpha_composite(obj)
    add_letters(card, bg)
    return card


if __name__ == '__main__':
    cards = [render(fn, bg) for _, fn, bg in FOODS]
    strip = Image.new('RGBA', (W * len(cards), H), (0, 0, 0, 0))
    for i, c in enumerate(cards):
        strip.paste(c, (i * W, 0))
    strip.save('food_1x.png')  # paste into assets/1x/Jokers.png at x=2..7; 2x = nearest-neighbour x2
    prev = Image.new('RGBA', (len(cards) * (W * 4 + 8), H * 4), (40, 40, 40, 255))
    for i, c in enumerate(cards):
        prev.paste(c.resize((W * 4, H * 4), Image.NEAREST), (i * (W * 4 + 8), 0))
    prev.save('food_preview.png')
