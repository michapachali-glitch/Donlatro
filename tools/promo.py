"""Builds the Donlatro overview poster (promo/donlatro_overview.png) from the mod's sprites.

Usage: python promo.py <path to m6x11plus.ttf>
(Balatro's pixel font; extract it from Balatro.exe: resources/fonts/m6x11plus.ttf)

Rendered at S times the base layout from the 2x sprite sheets, so the art stays crisp.
"""
import os
import sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
A = os.path.join(ROOT, 'assets', '2x')
FONT_PATH = sys.argv[1]

S = 2                      # output scale; layout numbers below are in 1x units
W, H = 71 * 2, 95 * 2      # card cell size in the 2x sheets
BG, PANEL, PANEL_EDGE = (30, 38, 44), (48, 58, 64), (70, 84, 92)
WHITE, GREY, LIGHT = (255, 255, 255), (150, 156, 170), (214, 220, 228)
RARITY = {
    'Common': (0, 157, 255), 'Uncommon': (75, 194, 146), 'Rare': (254, 95, 85),
    'Legendary': (178, 108, 187), 'Boss': (230, 70, 70), 'Final Boss': (224, 40, 220),
    'Voucher': (250, 180, 60), 'Tarot': (200, 160, 100), 'Spectral': (100, 140, 220), 'Deck': (150, 150, 170),
}
NEW_C, REPL_C, FOOD_C = (80, 200, 110), (120, 128, 146), (236, 146, 60)

sheets = {}


def sheet(name):
    if name not in sheets:
        sheets[name] = Image.open(os.path.join(A, name)).convert('RGBA')
    return sheets[name]


def sprite(name, x, y, soul=None, w=W, h=H):
    if (w, h) != (W, H):
        w, h = w * 2, h * 2  # other cell sizes are given in 1x pixels
    im = sheet(name).crop((x * w, y * h, x * w + w, y * h + h))
    if soul:
        im = im.copy()
        im.alpha_composite(sheet(name).crop((soul[0] * w, soul[1] * h, soul[0] * w + w, soul[1] * h + h)))
    return im


def font(size):
    return ImageFont.truetype(FONT_PATH, size * S)


F_TITLE, F_SUB, F_HEAD, F_NAME, F_BODY, F_BADGE = font(150), font(42), font(60), font(30), font(24), font(20)


# --- content -----------------------------------------------------------------------------
def J(x, y, soul=None):
    return sprite('Jokers.png', x, y, soul)


def R(i, soul=None):
    return sprite('Reskins.png', i % 10, i // 10, (soul % 10, soul // 10) if soul is not None else None)


NEW_JOKERS = [  # sprite, name, rarity, food?, effect
    (J(0, 0), 'Daunendonnie', 'Uncommon', False, '+100 Chips. Always Foil.'),
    (J(1, 0), 'TrekTrendy', 'Uncommon', False, 'Doubles the sell value of all your cards. Stacks.'),
    (J(2, 0), 'So(ß)e', 'Common', True, '+100 Chips, -5 each round. Spills if another food Joker is held.'),
    (J(3, 0), 'Döner', 'Uncommon', True, '+10 Mult, +5 for every Donlatro food that ran out. 0 Mult with So(ß)e.'),
    (J(4, 0), 'HolyEnergy', 'Uncommon', True, 'Gains X0.2 Mult each round. Destroyed when it reaches X2.'),
    (J(5, 0), 'Maggi', 'Uncommon', True, '+5 discards, -1 each round.'),
    (J(6, 0), 'Maultaschen', 'Uncommon', True, '+5 hand size, -1 each round.'),
    (J(7, 0), 'Sauerteigbrot', 'Common', True, 'Doubles its sell value each round. 1 in 4 chance to be eaten.'),
    (J(8, 0), 'Bähnle', 'Common', False, 'Gains +2 Mult each time a held Gold card pays out.'),
    (J(9, 0), 'Erdie Feuermann', 'Uncommon', False, 'Sell to remove all stickers from your other Jokers.'),
    (J(0, 1), 'Nolan', 'Uncommon', False, 'Descending Straight: +$5 sell value. At $20: -1 Ante, then gone.'),
    (J(1, 1), 'Frustsuppe', 'Rare', True, '+100 Chips, +30 Mult, X2 Mult. You earn $0 while held.'),
    (J(2, 1), "Shepherd's Pie", 'Common', True, 'Scored cards permanently gain +1 Mult. Lasts 3 rounds.'),
    (J(3, 1), 'Bierbrunnen', 'Uncommon', True, '1 in 5: scored cards turn Gold. Runs dry after 5.'),
    (J(4, 1), 'Jochen', 'Common', False, 'Cash out: a random -$5 to +$15. Your Steuerberater decides.'),
    (J(5, 1), 'UDK Abschlussarbeit', 'Uncommon', False, 'Only Aces scored: X1 Mult per scored Ace.'),
    (J(6, 1), 'Die Rampe', 'Rare', False, 'X0.25 Mult for each discard used this round.'),
    (J(7, 1), 'Classic Donnie', 'Rare', False, 'Retriggers cards whose rank you played last hand.'),
    (J(8, 1), 'Ihr checkt schon, was ich meine', 'Rare', False, 'Flushes and Straights may be one card short.'),
    (J(9, 1), 'DübelDonnie', 'Uncommon', False, 'Every High Card played: permanently +1 Mult.'),
    (J(1, 2), 'Der Akkuschrauber', 'Common', False, 'Gains +3 Mult each round. Beat a Boss: +$15, then gone.'),
    (J(2, 2), 'Buttplugs bei Butlers', 'Uncommon', False, 'Scored cards retrigger once per hand already played this round (3rd hand: they score 3 times).'),
    (J(3, 2), 'Kaffee', 'Common', True, '+1 discard next round. Costs $4 each round.'),
    (J(4, 2, (5, 2)), "Donnie O'Sullivan", 'Legendary', False, 'X6.9 Mult. 1 in 4: loses the thread, debuffed next round.'),
]

REPLACEMENTS = [  # reskin index, name, vanilla name, rarity, effect
    (0, 'Der kurze Gedanke', 'Half Joker', 'Common', '+20 Mult if the hand has 3 or fewer cards'),
    (1, 'Ohne Rampe, ohne mich', 'Mystic Summit', 'Common', '+15 Mult with 0 discards left'),
    (2, 'Die Monstera', 'Flower Pot', 'Uncommon', 'X3 Mult if the hand has all 4 suits'),
    (3, 'Das Solo-Format', 'Joker Stencil', 'Uncommon', 'X1 Mult per empty Joker slot'),
    (4, 'Die Gästeliste', 'Abstract Joker', 'Common', '+3 Mult for each Joker'),
    (5, 'Die Mittwochsfolge', 'Loyalty Card', 'Uncommon', 'X4 Mult every 6 hands played'),
    (6, 'Auf einer positiven Note', 'Acrobat', 'Uncommon', 'X3 Mult on the final hand of the round'),
    (7, 'Die Mayo-Chronik', 'Smeared Joker', 'Uncommon', 'Hearts=Diamonds, Spades=Clubs'),
    (8, 'Parasozial', 'Pareidolia', 'Uncommon', 'All cards count as face cards'),
    (9, 'Der Themensprung', 'Shortcut', 'Uncommon', 'Straights may skip 1 rank'),
    (10, 'Berlin', 'Arrowhead', 'Uncommon', 'Played Spades give +50 Chips'),
    (11, 'Tübingen', 'Bloodstone', 'Uncommon', 'Played Hearts: 1 in 2 for X1.5 Mult'),
    (12, 'Hamburg', 'Rough Gem', 'Uncommon', 'Played Diamonds earn $1'),
    (13, 'Irland', 'Onyx Agate', 'Uncommon', 'Played Clubs give +7 Mult'),
    (14, 'Erste Steuernachzahlung', 'Credit Card', 'Common', 'Go up to -$20 in debt'),
    (15, '"Ich komme gleich dazu"', 'Delayed Gratification', 'Common', '$2 per unused discard, if none used'),
    (16, 'Die Werbeanfrage', 'Business Card', 'Common', 'Face cards: 1 in 2 to give $2'),
    (17, 'Die Reichweite', 'Rocket', 'Uncommon', '$1 per round, +$2 per Boss defeated'),
    (18, 'Das neue Studio', 'Bull', 'Uncommon', '+2 Chips for each $1 you have'),
    (19, 'Der Selbstständige', 'Bootstraps', 'Uncommon', '+2 Mult for every $5 you have'),
    (20, 'Der Gegenwind', 'Matador', 'Uncommon', '$8 if your hand triggers the Boss'),
    (21, 'Der Deep Talk', 'Troubadour', 'Uncommon', '+2 hand size, -1 hand per round'),
    (22, 'Dieb Talk', 'Burglar', 'Uncommon', '+3 hands on Blind select, no discards'),
    (23, 'Disziplin-Donnie', 'Stuntman', 'Rare', '+250 Chips, -2 hand size'),
    (24, 'Die Überleitung', 'Juggler', 'Common', '+1 hand size'),
    (25, 'Das Bierchen', 'Drunkard', 'Common', '+1 discard'),
    (26, 'Noch ein Take', 'Chaos the Clown', 'Common', '1 free reroll per shop'),
    (27, 'Der Werbepartner', 'Luchador', 'Uncommon', 'Sell to disable the Boss Blind'),
    (28, '"Lass ihn mal drin"', 'Mr. Bones', 'Uncommon', 'Prevents death at 25% chips, then gone'),
    (29, 'Rausgeschnitten', 'Ceremonial Dagger', 'Uncommon', 'Eats the Joker to its right for Mult'),
    (30, 'Löcher spachteln', 'Marble Joker', 'Uncommon', 'Adds a Stone card each Blind'),
    (31, 'Der Spaziergang', 'Hiker', 'Uncommon', 'Played cards gain +5 Chips forever'),
    (32, 'Das Merch', 'Swashbuckler', 'Common', 'Mult = sell value of your other Jokers'),
    (33, 'Der Zahlendreher', 'Misprint', 'Common', 'Random +0 to +23 Mult'),
    (34, 'Die Nebenfiguren', 'Baseball Card', 'Rare', 'Uncommon Jokers each give X1.5 Mult'),
    (35, 'Der Algorithmus', 'The Idol', 'Uncommon', 'Random card each round gives X2 Mult'),
    (36, 'Die Hoffnung', 'Oops! All 6s', 'Uncommon', 'Doubles all probabilities'),
    (37, 'Die Astrologie', 'Cartomancer', 'Uncommon', 'Creates a Tarot each Blind'),
    (38, 'Nolan Schmolan', 'Astronomer', 'Uncommon', 'Planets and Celestial Packs are free'),
    (39, 'Die Pfandflaschen', 'Vagabond', 'Rare', 'Tarot if you play with $4 or less'),
    (40, 'Die Pause-Taste', 'Burnt Joker', 'Rare', 'Levels up your first discarded hand'),
    (None, 'Die Rakete', 'Space Joker', 'Common', '1 in 4 to level up the played hand'),
    (41, 'Costa und Jochen', 'Triboulet', 'Legendary', 'Kings and Queens give X2 Mult'),
    (42, '"Wo war ich?"', 'Yorick', 'Legendary', 'X1 Mult per 23 cards discarded'),
    (43, 'Der Spotify-Deal', 'Chicot', 'Legendary', 'Disables every Boss Blind'),
    (44, 'Das Transkript', 'Perkeo', 'Legendary', 'Negative copy of a consumable after shop'),
]


def blind(row):
    return sprite('Blinds.png', 0, row, w=34, h=34)


BOSSES = [
    (blind(0), 'Wasserschaden', 'Boss', 'Each scored card: 1 in 10 to be destroyed.'),
    (blind(2), 'Die Kammer', 'Boss', 'First hand is drawn face down.'),
    (blind(3), 'ADHS', 'Boss', 'Played cards are shuffled before scoring.'),
    (blind(4), 'Dieb', 'Boss', 'Lose $1 for every discarded card.'),
    (blind(5), 'Hans Flusensieb', 'Boss', 'After each hand, a random card in hand is destroyed.'),
    (blind(6), 'Die falsche Folgennummer', 'Boss', 'Scored as a random other hand you played this run.'),
    (blind(1), 'Nachbar von oben', 'Final Boss', 'All Chips halved. Plays LOUD techno.'),
]

VOUCHERS = [
    (sprite('Vouchers.png', 0, 0), 'Patreon', '$2 per Joker at cash out.'),
    (sprite('Vouchers.png', 0, 1), 'Patreon Exklusiv', '$4 per Joker; one free shop item per Ante.'),
    (sprite('Vouchers.png', 1, 0), 'Therapieplatz', 'Free Boss reroll once per Ante.'),
    (sprite('Vouchers.png', 1, 1), 'Kassenzulassung', 'Free, unlimited Boss rerolls.'),
    (sprite('Vouchers.png', 2, 0), 'Medikinet', '+1 hand size.'),
    (sprite('Vouchers.png', 2, 1), 'Elvanse', '+1 hand size; Blinds can\'t debuff or shuffle Jokers.'),
    (sprite('Vouchers.png', 3, 0), 'Schönhauser Allee Arcaden', '+1 shop card slot.'),
    (sprite('Vouchers.png', 3, 1), 'Das ganze Erdgeschoss', '+1 card slot and +1 Voucher slot.'),
    (sprite('Vouchers.png', 4, 0), 'Superrampe', '+1 discard each round.'),
    (sprite('Vouchers.png', 4, 1), 'Mini-Superrampe in der Superrampe', '+1 discard; discards add +5 Chips to your next hand.'),
]

CONSUMABLES = [
    (sprite('Consumables.png', 0, 0), 'Classic Donnie', 'Tarot', 'Copies 1 selected card into your deck.'),
    (sprite('Consumables.png', 1, 0), 'Die Therapie', 'Tarot', 'Cleans 1 card (debuff, edition, enhancement). -$2.'),
    (sprite('Consumables.png', 2, 0), 'Die Rückspultaste', 'Spectral', 'Restore your deck to the start of this Ante. Lose all money.'),
    (sprite('Consumables.png', 3, 0), 'Eingeschissen', 'Spectral', 'Random Joker becomes Negative; destroys a random card.'),
    (sprite('Consumables.png', 4, 0), 'Die Unsicherheit', 'Spectral', '+1 Joker slot; your Jokers are debuffed for a round.'),
    (sprite('Backs.png', 0, 0), 'Das ADHS-Deck', 'Deck', '+2 hand size, +1 discard. Jokers reshuffle every round.'),
    (sprite('Backs.png', 1, 0), 'Das Frustsuppen-Deck', 'Deck', 'Start at $0, no interest, +2 hands per round.'),
]


# --- drawing -----------------------------------------------------------------------------
# layout numbers are written in 1x units and multiplied by S
COLS, TILE_W, TILE_H, GAP, MARGIN = 5, 500 * S, 226 * S, 18 * S, 50 * S
PAGE_W = MARGIN * 2 + COLS * TILE_W + (COLS - 1) * GAP
SHADOW = (12, 14, 18)


def wrap(d, text, f, width):
    words, lines, cur = text.split(), [], ''
    for w in words:
        test = (cur + ' ' + w).strip()
        if d.textlength(test, font=f) <= width:
            cur = test
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def shadow_text(d, xy, text, f, fill, off=2):
    d.text((xy[0] + off * S, xy[1] + off * S), text, font=f, fill=SHADOW)
    d.text(xy, text, font=f, fill=fill)


def badge(d, x, y, text, colour):
    tw = d.textlength(text, font=F_BADGE)
    d.rounded_rectangle((x, y + 2 * S, x + tw + 14 * S, y + 28 * S), 6 * S, fill=tuple(int(c * 0.55) for c in colour))
    d.rounded_rectangle((x, y, x + tw + 14 * S, y + 26 * S), 6 * S, fill=colour)
    d.text((x + 7 * S, y + 3 * S), text, font=F_BADGE, fill=WHITE)
    return x + tw + 22 * S


def drop_shadow(page, box, radius, offset, alpha):
    x0, y0, x1, y1 = box
    pad = radius * 3
    sh = Image.new('RGBA', (x1 - x0 + pad * 2, y1 - y0 + pad * 2), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((pad, pad, pad + x1 - x0, pad + y1 - y0), 14 * S, fill=(0, 0, 0, alpha))
    sh = sh.filter(ImageFilter.GaussianBlur(radius))
    page.alpha_composite(sh, (x0 - pad + offset, y0 - pad + offset))


def tile(page, x, y, img, scale, name, rarity, badges, effect):
    accent = RARITY.get(rarity, WHITE)
    drop_shadow(page, (x, y, x + TILE_W, y + TILE_H), 6 * S, 5 * S, 140)
    panel = Image.new('RGBA', (TILE_W + 1, TILE_H + 1), (0, 0, 0, 0))
    pd = ImageDraw.Draw(panel)
    pd.rounded_rectangle((0, 0, TILE_W, TILE_H), 14 * S, fill=PANEL + (232,), outline=PANEL_EDGE + (255,), width=3 * S)
    pd.rounded_rectangle((3 * S, 3 * S, TILE_W - 3 * S, 40 * S), 11 * S, fill=(255, 255, 255, 10))  # top sheen
    pd.rectangle((3 * S, 18 * S, 7 * S, TILE_H - 18 * S), fill=accent + (255,))                   # rarity stripe
    page.alpha_composite(panel, (x, y))
    big = img.resize((img.width * scale, img.height * scale), Image.NEAREST)
    sh = Image.new('RGBA', big.size, (0, 0, 0, 0))
    sh.putalpha(big.getchannel('A').point(lambda a: 120 if a else 0))
    bx, by = x + 16 * S + (142 * S - big.width) // 2, y + (TILE_H - big.height) // 2
    page.alpha_composite(sh, (bx + 4 * S, by + 4 * S))
    page.alpha_composite(big, (bx, by))
    d = ImageDraw.Draw(page)
    tx, tw = x + 172 * S, TILE_W - 186 * S
    ty = y + 14 * S
    for line in wrap(d, name, F_NAME, tw):
        shadow_text(d, (tx, ty), line, F_NAME, accent)
        ty += 32 * S
    bx = tx
    for text, colour in badges:
        bx = badge(d, bx, ty + 2 * S, text, colour)
    ty += 38 * S
    for line in wrap(d, effect, F_BODY, tw):
        d.text((tx, ty), line, font=F_BODY, fill=LIGHT)
        ty += 26 * S


def swirl_background(w, h):
    """Balatro-style swirly backdrop, rendered at 1/(8S) size and upscaled for chunky pixels."""
    import numpy as np
    sw, sh = w // (8 * S), h // (8 * S)
    yy, xx = np.mgrid[0:sh, 0:sw].astype(float)
    cx, cy = sw * 0.5, sh * 0.12
    r = np.hypot(xx - cx, yy - cy)
    a = np.arctan2(yy - cy, xx - cx)
    v = np.sin(r * 0.09 - a * 3 + np.sin(yy * 0.02) * 2) + 0.6 * np.sin(xx * 0.05 + yy * 0.03)
    t = np.floor((v - v.min()) / (v.max() - v.min()) * 5) / 4               # 5 colour bands
    dark, warm = np.array([22, 44, 50]), np.array([62, 30, 40])
    fade = np.clip(yy / sh * 1.6, 0, 1)[..., None]                           # calmer further down
    rgb = dark + (warm - dark) * t[..., None] * (1 - 0.6 * fade)
    img = Image.fromarray(rgb.astype('uint8'), 'RGB').resize((w, h), Image.NEAREST)
    return img.convert('RGBA')


def rotate_crisp(img, angle):
    """Rotate pixel art without jagged edges: supersample, rotate smoothly, scale back down."""
    up = img.resize((img.width * 2, img.height * 2), Image.NEAREST)
    rot = up.rotate(angle, resample=Image.BICUBIC, expand=True)
    return rot.resize((rot.width // 2, rot.height // 2), Image.LANCZOS)


def card_fan(page, cards, cx, top, scale=4, spread=14):
    n = len(cards)
    for i, card in enumerate(cards):
        k = i - (n - 1) / 2
        big = card.resize((card.width * scale // 2 * S, card.height * scale // 2 * S), Image.NEAREST)
        shadow = Image.new('RGBA', big.size, (0, 0, 0, 0))
        shadow.putalpha(big.getchannel('A').point(lambda a: 110 if a else 0))
        angle = -k * spread / max(1, (n - 1) / 2)
        rot = rotate_crisp(big, angle)
        rsh = shadow.rotate(angle, resample=Image.BICUBIC, expand=True).filter(ImageFilter.GaussianBlur(4 * S))
        x = int(cx + k * 205 * S - rot.width / 2)
        y = int(top + abs(k) ** 1.6 * 14 * S)
        page.alpha_composite(rsh, (x + 10 * S, y + 12 * S))
        page.alpha_composite(rot, (x, y))


def section(page, y, title, subtitle, colour):
    d = ImageDraw.Draw(page)
    d.rectangle((MARGIN + 2 * S, y + 72 * S, PAGE_W - MARGIN + 2 * S, y + 76 * S), fill=SHADOW)
    d.rectangle((MARGIN, y + 70 * S, PAGE_W - MARGIN, y + 74 * S), fill=colour)
    shadow_text(d, (MARGIN, y), title, F_HEAD, colour, 3)
    d.text((MARGIN + d.textlength(title, font=F_HEAD) + 24 * S, y + 26 * S), subtitle, font=F_BODY, fill=GREY)
    return y + 100 * S


def grid(page, y, items, draw_item):
    for i, item in enumerate(items):
        x = MARGIN + (i % COLS) * (TILE_W + GAP)
        draw_item(page, x, y + (i // COLS) * (TILE_H + GAP), item)
    rows = (len(items) + COLS - 1) // COLS
    return y + rows * (TILE_H + GAP) + 30 * S


def rows_height(n):
    return ((n + COLS - 1) // COLS) * (TILE_H + GAP) + 130 * S


if __name__ == '__main__':
    header = 860 * S
    total = (header + rows_height(len(NEW_JOKERS)) + rows_height(len(REPLACEMENTS)) + rows_height(len(BOSSES))
             + rows_height(len(VOUCHERS)) + rows_height(len(CONSUMABLES)) + 120 * S)
    page = swirl_background(PAGE_W, total)
    d = ImageDraw.Draw(page)

    title = 'DONLATRO'
    tw = d.textlength(title, font=F_TITLE)
    for off, col in ((8, (16, 18, 22)), (0, (254, 95, 85))):
        d.text(((PAGE_W - tw) / 2 + off * S, (30 + off) * S), title, font=F_TITLE, fill=col)
    fan = [J(0, 0), J(3, 0), J(1, 1), J(4, 2, (5, 2)), J(6, 1), J(9, 1), J(1, 0)]
    card_fan(page, fan, PAGE_W / 2, 215 * S)
    d = ImageDraw.Draw(page)
    sub = 'A Balatro mod  -  everything new at a glance'
    shadow_text(d, ((PAGE_W - d.textlength(sub, font=F_SUB)) / 2, 680 * S), sub, F_SUB, WHITE, 3)
    stats = (f'{len(NEW_JOKERS)} new Jokers  |  {len(REPLACEMENTS)} reworked Jokers  |  {len(BOSSES)} Bosses  |  '
             f'{len(VOUCHERS)} Vouchers  |  2 Tarots  |  3 Spectrals  |  2 Decks')
    shadow_text(d, ((PAGE_W - d.textlength(stats, font=F_BODY)) / 2, 740 * S), stats, F_BODY, LIGHT)
    lx = (PAGE_W - 900 * S) / 2                                              # legend
    lx = badge(d, lx, 790 * S, 'NEW', NEW_C)
    d.text((lx, 791 * S), 'brand-new creation', font=F_BODY, fill=LIGHT)
    lx += 260 * S
    lx = badge(d, lx, 790 * S, 'REPLACES ...', REPL_C)
    d.text((lx, 791 * S), 'vanilla Joker, renamed + redrawn', font=F_BODY, fill=LIGHT)
    lx += 400 * S
    lx = badge(d, lx, 790 * S, 'FOOD', FOOD_C)
    d.text((lx, 791 * S), 'runs out', font=F_BODY, fill=LIGHT)
    y = header

    y = section(page, y, 'NEW JOKERS', 'original Donlatro creations', NEW_C)
    y = grid(page, y, NEW_JOKERS, lambda p, x, yy, it: tile(
        p, x, yy, it[0], S, it[1], it[2],
        [('NEW', NEW_C), (it[2].upper(), RARITY[it[2]])] + ([('FOOD', FOOD_C)] if it[3] else []), it[4]))

    def repl(p, x, yy, it):
        idx, name, vanilla, rarity, effect = it
        img = sprite('Jokers.png', 0, 2) if idx is None else R(idx, idx + 4 if idx >= 41 else None)
        tile(p, x, yy, img, S, name, rarity, [('REPLACES ' + vanilla.upper(), REPL_C)], effect)

    y = section(page, y, 'REWORKED JOKERS', 'vanilla effects with a Donlatro name and new art', REPL_C)
    y = grid(page, y, REPLACEMENTS, repl)

    y = section(page, y, 'BOSS BLINDS', 'new opponents', RARITY['Boss'])
    y = grid(page, y, BOSSES, lambda p, x, yy, it: tile(p, x, yy, it[0], 2 * S, it[1], it[2], [(it[2].upper(), RARITY[it[2]])], it[3]))

    y = section(page, y, 'VOUCHERS', 'base voucher and its upgrade', RARITY['Voucher'])
    y = grid(page, y, VOUCHERS, lambda p, x, yy, it: tile(p, x, yy, it[0], S, it[1], 'Voucher', [('VOUCHER', RARITY['Voucher'])], it[2]))

    y = section(page, y, 'TAROTS, SPECTRALS & DECKS', 'more ways to break the run', RARITY['Spectral'])
    y = grid(page, y, CONSUMABLES, lambda p, x, yy, it: tile(p, x, yy, it[0], S, it[1], it[2], [(it[2].upper(), RARITY[it[2]])], it[3]))

    out = os.path.join(ROOT, 'promo')
    os.makedirs(out, exist_ok=True)
    page.convert('RGB').save(os.path.join(out, 'donlatro_overview.png'), optimize=True)
    print(page.size)
