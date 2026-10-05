"""Jochen: an older man grinning on his yacht, cocktail in hand, while his Steuererklärung
blows away in the wind. Writes jochen_1x.png / jochen_preview.png into the current directory.
"""
import os
import sys
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from food_art import render  # noqa: E402
from batch2_art import DARK  # noqa: E402


def jochen(d):
    # sea + yacht
    d.rectangle((13, 76, 58, 86), fill=(52, 120, 196))
    for x in range(15, 57, 7):
        d.line((x, 79, x + 3, 79), fill=(150, 200, 240))
    d.polygon([(13, 64), (58, 64), (54, 78), (17, 78)], fill=(246, 246, 250))   # hull
    d.rectangle((13, 70, 58, 72), fill=(40, 90, 170))                          # stripe
    # Hawaiian shirt
    shirt, flower = (226, 70, 60), (255, 220, 90)
    d.polygon([(16, 66), (19, 54), (29, 50), (43, 50), (52, 54), (55, 66)], fill=shirt)
    d.polygon([(31, 50), (36, 58), (41, 50)], fill=(240, 200, 170))             # open collar
    for x, y in ((22, 58), (47, 57), (27, 63), (43, 63)):
        d.point((x, y), fill=flower)
        d.point((x + 1, y), fill=flower)
        d.point((x, y + 1), fill=(255, 255, 255))
    d.line((13, 62, 58, 62), fill=(200, 160, 110), width=2)                     # wooden railing
    # head
    skin, skin_s = (240, 190, 150), (212, 156, 118)
    d.ellipse((21, 30, 25, 38), fill=skin_s)                                    # ears
    d.ellipse((46, 30, 50, 38), fill=skin_s)
    d.ellipse((23, 20, 48, 52), fill=skin)                                      # face
    d.rectangle((43, 26, 47, 46), fill=skin_s)
    d.rectangle((22, 28, 25, 34), fill=(214, 214, 220))                         # grey sideburns
    d.rectangle((46, 28, 49, 34), fill=(214, 214, 220))
    d.line((27, 30, 31, 29), fill=(190, 190, 196))                              # bushy grey brows
    d.line((39, 29, 43, 30), fill=(190, 190, 196))
    d.arc((27, 31, 32, 35), 200, 340, fill=DARK)                                # happy squint
    d.arc((38, 31, 43, 35), 200, 340, fill=DARK)
    d.line((27, 37, 29, 38), fill=skin_s)                                       # laugh lines
    d.line((43, 37, 41, 38), fill=skin_s)
    d.chord((28, 40, 42, 50), 0, 180, fill=(255, 255, 255))                     # big grin
    d.arc((28, 40, 42, 50), 0, 180, fill=(160, 70, 60))
    d.polygon([(27, 41), (35, 38), (43, 41), (39, 43), (35, 41), (31, 43)], fill=(236, 236, 240))  # white moustache
    # captain's hat
    d.rounded_rectangle((24, 12, 47, 22), 3, fill=(250, 250, 252))
    d.rectangle((22, 21, 49, 24), fill=(30, 34, 50))                            # brim
    d.rectangle((25, 19, 46, 20), fill=(30, 34, 50))                            # band
    d.ellipse((33, 13, 38, 18), fill=(240, 196, 60))                            # gold badge
    # cocktail in the raised hand
    d.ellipse((50, 46, 56, 52), fill=skin)
    d.polygon([(49, 34), (59, 34), (54, 41)], fill=(250, 250, 255))             # glass
    d.polygon([(50, 35), (58, 35), (54, 40)], fill=(255, 140, 80))              # drink
    d.line((54, 41, 54, 47), fill=(250, 250, 255))
    d.polygon([(55, 28), (61, 31), (55, 31)], fill=(80, 200, 120))              # umbrella
    d.line((55, 31, 53, 35), fill=(140, 100, 60))
    # the Steuererklärung blowing away
    for (x, y, tilt) in ((38, 2, 2), (52, 14, -2)):
        d.polygon([(x, y), (x + 9, y + tilt), (x + 9 + tilt, y + 11), (x + tilt, y + 11 - tilt)], fill=(250, 250, 244))
        d.line((x + 2, y + 4, x + 7, y + 4 + tilt // 2), fill=(170, 170, 180))
        d.line((x + 2, y + 7, x + 6, y + 7 + tilt // 2), fill=(170, 170, 180))
    d.rectangle((40, 4, 42, 6), fill=(200, 50, 50))                            # red 'tax office' stamp


if __name__ == '__main__':
    card = render(jochen, (120, 190, 235))
    card.save('jochen_1x.png')
    card.resize((71 * 5, 95 * 5), Image.NEAREST).save('jochen_preview.png')
