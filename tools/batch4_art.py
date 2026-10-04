"""Boss chip for Dieb (bandit mask). Writes batch4_blinds_1x.png (1 row x 21 frames)."""
import os
import sys
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from batch2_art import blind_strip  # noqa: E402
from batch3_art import boss_disc  # noqa: E402


def dieb_glyph(d, ink):
    d.polygon([(6, 13), (12, 11), (17, 13), (22, 11), (28, 13), (27, 20), (21, 21), (17, 18),
               (13, 21), (7, 20)], fill=ink)                                   # mask band
    d.ellipse((10, 14, 14, 17), fill=(0, 0, 0, 0))                              # eye holes
    d.ellipse((20, 14, 24, 17), fill=(0, 0, 0, 0))
    d.line((6, 15, 3, 19), fill=ink)                                           # ribbon tails
    d.line((28, 15, 31, 19), fill=ink)
    d.text((14, 22), '$', fill=ink)


if __name__ == '__main__':
    chip = boss_disc((84, 132, 112), dieb_glyph)
    # eye holes were drawn transparent - fill them back with the disc colour underneath
    base = boss_disc((84, 132, 112), lambda d, ink: None)
    chip = Image.alpha_composite(base, chip)
    blind_strip(chip).save('batch4_blinds_1x.png')
    chip.resize((204, 204), Image.NEAREST).save('batch4_preview.png')
