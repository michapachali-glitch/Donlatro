"""Original cartoon for TrekTrendy (replaces the earlier photo-based sprite).

Drawn from scratch - no photo, no real logos: a traveller in a hoodie with a generic
ringed-planet patch, toasting with a glass of bubbly in a plane seat.
Writes trektrendy_1x.png (one 71x95 card) into the current directory.
"""
import os
import sys
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from food_art import render  # noqa: E402
from batch2_art import DARK  # noqa: E402


def trektrendy(d):
    seat, seat_d = (70, 76, 96), (50, 54, 72)
    d.rounded_rectangle((12, 20, 30, 86), 6, fill=seat)                       # plane seat back
    d.rectangle((26, 24, 30, 84), fill=seat_d)
    d.ellipse((44, 14, 58, 30), fill=(200, 226, 250))                         # plane window
    d.ellipse((46, 16, 56, 28), fill=(150, 200, 245))
    d.ellipse((48, 22, 54, 26), fill=(255, 255, 255))                         # cloud
    hoodie, hoodie_d = (196, 198, 206), (160, 162, 174)
    d.polygon([(16, 86), (19, 66), (29, 60), (43, 60), (52, 66), (55, 86)], fill=hoodie)
    d.polygon([(27, 60), (35, 70), (44, 60)], fill=hoodie_d)                 # hood opening
    d.line((32, 66, 31, 76), fill=(250, 250, 250))                           # drawstrings
    d.line((39, 66, 40, 76), fill=(250, 250, 250))
    d.ellipse((40, 72, 50, 82), fill=(60, 70, 140))                          # planet patch
    d.ellipse((43, 75, 47, 79), fill=(250, 200, 80))
    d.line((38, 79, 52, 75), fill=(250, 250, 250))                           # ring
    skin, skin_s = (244, 200, 166), (216, 168, 132)
    d.rectangle((31, 54, 40, 61), fill=skin_s)                               # neck
    d.ellipse((22, 36, 26, 44), fill=skin_s)                                 # ears
    d.ellipse((45, 36, 49, 44), fill=skin_s)
    d.ellipse((24, 24, 47, 58), fill=skin)                                   # face
    d.polygon([(23, 34), (24, 22), (32, 16), (42, 17), (48, 24), (48, 33), (44, 27), (34, 26), (27, 30)],
              fill=(120, 78, 48))                                            # quiff
    d.line((30, 19, 40, 18), fill=(150, 104, 66))
    d.arc((27, 36, 33, 40), 200, 340, fill=DARK)                             # happy closed eyes
    d.arc((38, 36, 44, 40), 200, 340, fill=DARK)
    d.chord((29, 42, 43, 54), 0, 180, fill=(255, 255, 255))                  # big grin
    d.arc((29, 42, 43, 54), 0, 180, fill=(170, 80, 70))
    for x in range(28, 44, 3):                                               # stubble
        d.point((x, 55), fill=skin_s)
    d.ellipse((50, 58, 56, 64), fill=skin)                                   # raised hand
    d.polygon([(50, 40), (58, 40), (55, 50), (53, 50)], fill=(236, 240, 250))  # champagne flute
    d.polygon([(51, 42), (57, 42), (55, 49), (53, 49)], fill=(250, 220, 110))
    d.line((54, 50, 54, 58), fill=(236, 240, 250))
    for x, y in ((53, 38), (56, 36), (52, 34)):                              # bubbles
        d.point((x, y), fill=(255, 250, 200))


if __name__ == '__main__':
    card = render(trektrendy, (96, 150, 210))
    card.save('trektrendy_1x.png')
    card.resize((71 * 5, 95 * 5), Image.NEAREST).save('trektrendy_preview.png')
