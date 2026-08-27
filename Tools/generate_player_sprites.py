#!/usr/bin/env python3
"""
Generates crisp, highly distinct 8-bit pixel art character frames for KOSEN student.
Legs have clear, exaggerated walk/run stride cycles with visible left/right alternating steps.
"""

import os
import shutil
from PIL import Image

def hex_to_rgba(h, a=255):
    h = h.lstrip('#')
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), a)

PALETTE = {
    ' ': (0, 0, 0, 0),             # Transparent
    'O': hex_to_rgba('0f172a'),     # Dark Outline (Near Black)
    'H': hex_to_rgba('271c19'),     # Hair Dark Brown
    'h': hex_to_rgba('4a332d'),     # Hair Highlight
    'S': hex_to_rgba('ffd7a8'),     # Skin
    's': hex_to_rgba('f0b37e'),     # Skin Shadow
    'E': hex_to_rgba('0f172a'),     # Eye Dark
    'W': hex_to_rgba('ffffff'),     # Shirt White
    'w': hex_to_rgba('cbd5e1'),     # Shirt Shadow
    'B': hex_to_rgba('1e3a8a'),     # Shorts Blue (Navy)
    'b': hex_to_rgba('172554'),     # Shorts Blue Shadow
    'L': hex_to_rgba('78350f'),     # Belt Brown
    'K': hex_to_rgba('dc2626'),     # Backpack Red
    'k': hex_to_rgba('991b1b'),     # Backpack Red Shadow
    'J': hex_to_rgba('f87171'),     # Backpack Red Highlight
    'G': hex_to_rgba('f8fafc'),     # Socks White
    'X': hex_to_rgba('18181b'),     # Shoes Dark
    'x': hex_to_rgba('3f3f46'),     # Shoes Highlight
    'C': hex_to_rgba('fbbf24'),     # Badge Gold
}

# 32x32 Pixel Art Matrices

# 1. IDLE (Standing, breathing)
IDLE_STR = [
    "                                ", # 0
    "                                ", # 1
    "             OOOOO              ", # 2
    "            OHHHhhO             ", # 3
    "           OHHHHHhhO            ", # 4
    "           OHHHSSSSO            ", # 5
    "          OHHHSsEsEO            ", # 6
    "          OHHSSsEsEO            ", # 7
    "          OHHSSSSSSO            ", # 8
    "           OHHsSSsO             ", # 9
    "          OKKOssSO              ", # 10
    "         OKJKOOWWWO             ", # 11
    "        OKKKOOWWCWWO            ", # 12
    "        OKKKOOWWWwWO            ", # 13
    "        OKkkOOWWwwWO            ", # 14
    "         OkOOOWWwwWO            ", # 15
    "          OO OWwTTwO            ", # 16
    "            OLLLLLLO            ", # 17
    "            OBBBBBBO            ", # 18
    "            OBBbBBbO            ", # 19
    "            OBBbOBbO            ", # 20
    "            OBbO OBbO           ", # 21
    "            OSO  OSO            ", # 22
    "            OSO  OSO            ", # 23
    "            OGO  OGO            ", # 24
    "            OXXO OXXO           ", # 25
    "            OxxO OxxO           ", # 26
    "             OO   OO            ", # 27
    "                                ", # 28
    "                                ", # 29
    "                                ", # 30
    "                                "  # 31
]

# 2. RUN 1 (Right leg thrust forward, Left leg back - Wide stride)
RUN1_STR = [
    "                                ", # 0
    "             OOOOO              ", # 1
    "            OHHHhhO             ", # 2
    "           OHHHHHhhO            ", # 3
    "           OHHHSSSSO            ", # 4
    "          OHHHSsEsEO            ", # 5
    "          OHHSSsEsEO            ", # 6
    "          OHHSSSSSSO            ", # 7
    "           OHHsSSsO             ", # 8
    "          OKKOssSO              ", # 9
    "         OKJKOOWWOO             ", # 10
    "        OKKKOOWWWOwO            ", # 11
    "        OKKKOOWWCWwSO           ", # 12
    "        OKkkOOWWWwwSO           ", # 13
    "         OkOOOWWwwWOO           ", # 14
    "          OO OWwTTwO            ", # 15
    "            OLLLLLLO            ", # 16
    "           OBBBBBBBO            ", # 17
    "          OBBbBBBbbO            ", # 18
    "         OBBbO  OBbO            ", # 19
    "        OBbO     OBbO           ", # 20
    "        OSO       OSO           ", # 21
    "       OGO         OGO          ", # 22
    "      OXXO          OGgO        ", # 23
    "     OxxxO           OXXO       ", # 24
    "      OOO            OxxO       ", # 25
    "                      OO        ", # 26
    "                                ", # 27
    "                                ", # 28
    "                                ", # 29
    "                                ", # 30
    "                                "  # 31
]

# 3. RUN 2 (Passing pose / Right foot contact, Left knee raising)
RUN2_STR = [
    "                                ", # 0
    "                                ", # 1
    "             OOOOO              ", # 2
    "            OHHHhhO             ", # 3
    "           OHHHHHhhO            ", # 4
    "           OHHHSSSSO            ", # 5
    "          OHHHSsEsEO            ", # 6
    "          OHHSSsEsEO            ", # 7
    "          OHHSSSSSSO            ", # 8
    "           OHHsSSsO             ", # 9
    "          OKKOssSO              ", # 10
    "         OKJKOOWWWO             ", # 11
    "        OKKKOOWWCWWO            ", # 12
    "        OKKKOOWWWwWO            ", # 13
    "        OKkkOOWWwwWOS           ", # 14
    "         OkOOOWWwwWOS           ", # 15
    "          OO OWwTTwOO           ", # 16
    "            OLLLLLLO            ", # 17
    "            OBBBBBBO            ", # 18
    "            OBBbBBbO            ", # 19
    "            OBBbOBbO            ", # 20
    "            OBbO OBBbO          ", # 21
    "            OSO   OBbO          ", # 22
    "            OGO    OSO          ", # 23
    "            OXXO   OGO          ", # 24
    "            OxxO   OXXO         ", # 25
    "             OO    OxxO         ", # 26
    "                    OO          ", # 27
    "                                ", # 28
    "                                ", # 29
    "                                ", # 30
    "                                "  # 31
]

# 4. RUN 3 (Left leg thrust forward, Right leg back - Wide stride)
RUN3_STR = [
    "                                ", # 0
    "             OOOOO              ", # 1
    "            OHHHhhO             ", # 2
    "           OHHHHHhhO            ", # 3
    "           OHHHSSSSO            ", # 4
    "          OHHHSsEsEO            ", # 5
    "          OHHSSsEsEO            ", # 6
    "          OHHSSSSSSO            ", # 7
    "           OHHsSSsO             ", # 8
    "          OKKOssSO              ", # 9
    "         OKJKOOWWO              ", # 10
    "        OKKKOOWWWO              ", # 11
    "        OKKKOOWWCWWO            ", # 12
    "        OKkkOOWWWwWO            ", # 13
    "        SOkOOOWWwwWO            ", # 14
    "        SO OO OWwTTwO           ", # 15
    "        OO   OLLLLLLO           ", # 16
    "            OBBBBBBBO           ", # 17
    "           OBBbBBBbbO           ", # 18
    "           OBbO  OBBbO          ", # 19
    "          OBbO    OBbO          ", # 20
    "          OSO      OSO          ", # 21
    "         OGgO       OGO         ", # 22
    "        OXXO         OGO        ", # 23
    "        OxxO          OXXO      ", # 24
    "         OO          OxxxO      ", # 25
    "                      OOO       ", # 26
    "                                ", # 27
    "                                ", # 28
    "                                ", # 29
    "                                ", # 30
    "                                "  # 31
]

# 5. RUN 4 (Passing pose / Left foot contact, Right knee raising)
RUN4_STR = [
    "                                ", # 0
    "                                ", # 1
    "             OOOOO              ", # 2
    "            OHHHhhO             ", # 3
    "           OHHHHHhhO            ", # 4
    "           OHHHSSSSO            ", # 5
    "          OHHHSsEsEO            ", # 6
    "          OHHSSsEsEO            ", # 7
    "          OHHSSSSSSO            ", # 8
    "           OHHsSSsO             ", # 9
    "          OKKOssSO              ", # 10
    "         OKJKOOWWWO             ", # 11
    "        OKKKOOWWCWWO            ", # 12
    "        OKKKOOWWWwWO            ", # 13
    "        OKkkOOWWwwWO            ", # 14
    "         OkOOOWWwwWSO           ", # 15
    "          OO OWwTTwSO           ", # 16
    "            OLLLLLLOO           ", # 17
    "            OBBBBBBO            ", # 18
    "            OBBbBBbO            ", # 19
    "            OBBbOBbO            ", # 20
    "          OBBbO  OBbO           ", # 21
    "          OBbO   OSO            ", # 22
    "          OSO    OGO            ", # 23
    "          OGO    OXXO           ", # 24
    "          OXXO   OxxO           ", # 25
    "          OxxO    OO            ", # 26
    "           OO                   ", # 27
    "                                ", # 28
    "                                ", # 29
    "                                ", # 30
    "                                "  # 31
]

# 6. JUMP (Tucked air pose)
JUMP_STR = [
    "                                ", # 0
    "             OOOOO              ", # 1
    "            OHHHhhO             ", # 2
    "           OHHHHHhhO            ", # 3
    "           OHHHSSSSO            ", # 4
    "          OHHHSsEsEO            ", # 5
    "          OHHSSsEsEO            ", # 6
    "          OHHSSSSSSO            ", # 7
    "           OHHsSSsO             ", # 8
    "          OKKOssSO              ", # 9
    "         OKJKOOWWOO             ", # 10
    "        OKKKOOWWWOwO            ", # 11
    "        OKKKOOWWCWwSO           ", # 12
    "        OKkkOOWWWwwSO           ", # 13
    "         OkOOOWWwwWOO           ", # 14
    "          OO OWwTTwO            ", # 15
    "            OLLLLLLO            ", # 16
    "           OBBBBBBBO            ", # 17
    "          OBBbBBBbbO            ", # 18
    "          OBbO   OBbO           ", # 19
    "          OSSO   OSSO           ", # 20
    "          OGGO   OGGO           ", # 21
    "          OXXO   OXXO           ", # 22
    "          OxxO   OxxO           ", # 23
    "           OO     OO            ", # 24
    "                                ", # 25
    "                                ", # 26
    "                                ", # 27
    "                                ", # 28
    "                                ", # 29
    "                                ", # 30
    "                                "  # 31
]

def str_to_image(ascii_lines):
    img = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    for y, line in enumerate(ascii_lines):
        for x, char in enumerate(line):
            if x < 32 and y < 32:
                img.putpixel((x, y), PALETTE.get(char, (0, 0, 0, 0)))
    return img

def flip_image_h(img):
    return img.transpose(Image.FLIP_LEFT_RIGHT)

if __name__ == '__main__':
    frames = {
        'player_idle.png': str_to_image(IDLE_STR),
        'player_run_1.png': str_to_image(RUN1_STR),
        'player_run_2.png': str_to_image(RUN2_STR),
        'player_run_3.png': str_to_image(RUN3_STR),
        'player_run_4.png': str_to_image(RUN4_STR),
        'player_jump.png': str_to_image(JUMP_STR),
    }
    
    left_frames = {
        'player_idle_left.png': flip_image_h(frames['player_idle.png']),
        'player_run_1_left.png': flip_image_h(frames['player_run_1.png']),
        'player_run_2_left.png': flip_image_h(frames['player_run_2.png']),
        'player_run_3_left.png': flip_image_h(frames['player_run_3.png']),
        'player_run_4_left.png': flip_image_h(frames['player_run_4.png']),
        'player_jump_left.png': flip_image_h(frames['player_jump.png']),
    }
    
    out_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Assets', 'Art', 'Sprites')
    os.makedirs(out_dir, exist_ok=True)
    
    # Also save to Resources/Sprites for 100% guaranteed runtime loading
    res_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Assets', 'Resources', 'Sprites')
    os.makedirs(res_dir, exist_ok=True)
    
    for name, img in {**frames, **left_frames}.items():
        p1 = os.path.join(out_dir, name)
        img.save(p1)
        p2 = os.path.join(res_dir, name)
        img.save(p2)
        print(f'Saved {name}')
        
    sheet = Image.new('RGBA', (32 * 6, 32), (0, 0, 0, 0))
    ordered_keys = ['player_idle.png', 'player_run_1.png', 'player_run_2.png', 'player_run_3.png', 'player_run_4.png', 'player_jump.png']
    for idx, k in enumerate(ordered_keys):
        sheet.paste(frames[k], (idx * 32, 0))
    sheet_path = os.path.join(out_dir, 'player_spritesheet.png')
    sheet.save(sheet_path)
    sheet.save(os.path.join(res_dir, 'player_spritesheet.png'))
    print('Generated all distinct player sprite frames!')
