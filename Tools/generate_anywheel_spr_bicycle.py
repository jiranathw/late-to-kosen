#!/usr/bin/env python3
"""
Generates pixel art for spr_bicycle.png (48x32) and spr_ajarn_bike.png (48x48)
matching the exact lime-green Anywheel bicycle from the user's reference photo.
"""

import os
from PIL import Image

def make_spr_bicycle_48x32():
    # 48x32 Anywheel Lime-Green Bicycle
    c_trans = (0, 0, 0, 0)
    c_black = (15, 23, 42, 255)         # Dark frame outline / saddle / basket
    c_lime_bright = (163, 230, 53, 255) # Anywheel light lime green #a3e635
    c_lime = (132, 204, 22, 255)        # Anywheel primary lime green #84cc16
    c_lime_dark = (101, 163, 13, 255)   # Anywheel dark green #65a30d
    c_tire = (30, 41, 59, 255)          # Dark tire rubber
    c_spoke = (226, 232, 240, 255)      # Silver spokes
    c_spoke_dark = (148, 163, 184, 255) # Spoke shadow
    c_refl_yellow = (250, 204, 21, 255) # Reflector yellow
    c_refl_red = (239, 68, 68, 255)     # Rear reflector red
    c_guard = (15, 20, 30, 255)         # Chain guard / basket plastic

    pal = {
        '.': c_trans,
        'k': c_black,
        'G': c_lime_bright,
        'g': c_lime,
        'd': c_lime_dark,
        't': c_tire,
        'w': c_spoke,
        's': c_spoke_dark,
        'y': c_refl_yellow,
        'r': c_refl_red,
        'b': c_guard,
    }

    grid = [
        "................................................", # 0
        "................................................", # 1
        "................................................", # 2
        "................................................", # 3
        "..............................kbkb..............", # 4 Handlebar stem & basket
        "...................kk.........kbkbbk............", # 5 Saddle top & basket
        ".................kkbbkk.......kbbbbk............", # 6 Saddle & wire basket
        "...................kk.........kbkbbk............", # 7
        "...................kk.........kkgkk.............", # 8 Seatpost & stem
        "...................kg.........kg................", # 9
        "...................kgg........kgk...............", # 10 Step-through curve
        "...................kgg.......kggk...............", # 11
        "....................kgg.....kgg.................", # 12
        ".........kkkk........kgggggggk........kkkk......", # 13 Mudguard top & Frame tube
        ".......kktbttkk.......kgggggk.......kktbttkk....", # 14 Mudguards
        "......ktwwwwwwtk.......kgbkg.......ktwwwwwwtk...", # 15 Wheels & bottom bracket
        ".....ktwwwwywwwtk....kbbbbbbk.....ktwwwwywwwtk..", # 16 Chaincase & reflectors
        "....rktwwswwwswtk....kbbgbgbk....rktwwswwwswtk..", # 17 Chain guard with anywheel green
        "....rktwwswwwswtk.....kbbbbk.....rktwwswwwswtk..", # 18
        ".....ktwwwwswwwtk......kbbk.......ktwwwwswwwtk..", # 19
        ".....ktwwwwswwwtk.......kk........ktwwwwswwwtk..", # 20
        "......ktwwwwwwtk...................ktwwwwwwtk...", # 21
        ".......kttttttk.....................kttttttk....", # 22
        ".........kkkk.........................kkkk......", # 23 Bottom of wheels
        "................................................", # 24
        "................................................", # 25
        "................................................", # 26
        "................................................", # 27
        "................................................", # 28
        "................................................", # 29
        "................................................", # 30
        "................................................", # 31
    ]

    im = Image.new('RGBA', (48, 32), (0, 0, 0, 0))
    for y, line in enumerate(grid):
        for x, ch in enumerate(line):
            im.putpixel((x, y), pal.get(ch, c_trans))
    return im

def make_spr_ajarn_bike_48x48():
    # Load original spr_ajarn_bike and convert cyan bike parts to Anywheel lime green
    p = 'Assets/Art/Sprites/spr_ajarn_bike.png'
    im = Image.open(p).convert('RGBA')
    
    # Replace cyan colors (14, 116, 144) and (34, 211, 238) with Anywheel green
    c_lime_dark = (101, 163, 13, 255)
    c_lime = (132, 204, 22, 255)
    c_lime_bright = (163, 230, 53, 255)

    out = Image.new('RGBA', im.size, (0, 0, 0, 0))
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = im.getpixel((x, y))
            if a < 50:
                out.putpixel((x, y), (0, 0, 0, 0))
            elif b > 140 and r < 40 and g > 100:
                # Cyan color -> replace with lime green
                if b > 200:
                    out.putpixel((x, y), c_lime_bright)
                else:
                    out.putpixel((x, y), c_lime)
            else:
                out.putpixel((x, y), (r, g, b, a))
    return out

def generate():
    spr_bike = make_spr_bicycle_48x32()
    spr_ajarn = make_spr_ajarn_bike_48x48()

    dirs = [r'Assets/Art/Sprites', r'Assets/Resources/Sprites']
    for d in dirs:
        os.makedirs(d, exist_ok=True)
        spr_bike.save(os.path.join(d, 'spr_bicycle.png'))
        spr_ajarn.save(os.path.join(d, 'spr_ajarn_bike.png'))

    print('Successfully generated green Anywheel spr_bicycle.png (48x32) and spr_ajarn_bike.png (48x48)!')

if __name__ == '__main__':
    generate()
