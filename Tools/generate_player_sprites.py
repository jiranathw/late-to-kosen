#!/usr/bin/env python3
import os
from PIL import Image

def hex_to_rgba(h, a=255):
    h = h.lstrip('#')
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), a)

# Color Palette (8-bit Thai Student Uniform)
PALETTE = {
    ' ': (0, 0, 0, 0),             # Transparent
    'O': hex_to_rgba('111827'),     # Dark Outline (Near Black)
    'H': hex_to_rgba('271c19'),     # Hair Dark Brown
    'h': hex_to_rgba('4a332d'),     # Hair Mid Brown / Highlight
    'S': hex_to_rgba('ffd7a8'),     # Skin
    's': hex_to_rgba('f0b37e'),     # Skin Shadow
    'E': hex_to_rgba('111827'),     # Eye (Dark)
    'e': hex_to_rgba('ffffff'),     # Eye White
    'W': hex_to_rgba('ffffff'),     # Shirt White
    'w': hex_to_rgba('cbd5e1'),     # Shirt Shadow (Slate 300)
    'T': hex_to_rgba('94a3b8'),     # Shirt Dark Shadow (Slate 400)
    'B': hex_to_rgba('1e3a8a'),     # Shorts Blue (Navy)
    'b': hex_to_rgba('172554'),     # Shorts Blue Shadow
    'L': hex_to_rgba('78350f'),     # Belt / Leather Brown
    'K': hex_to_rgba('dc2626'),     # Backpack Red
    'k': hex_to_rgba('991b1b'),     # Backpack Red Shadow
    'J': hex_to_rgba('f87171'),     # Backpack Red Highlight
    'G': hex_to_rgba('f1f5f9'),     # Socks White
    'g': hex_to_rgba('94a3b8'),     # Socks Shadow
    'X': hex_to_rgba('0f172a'),     # Shoes Black
    'x': hex_to_rgba('334155'),     # Shoes Highlight
    'C': hex_to_rgba('fbbf24'),     # School Badge Gold
}

# 32x32 pixel frames definition as ASCII art
# Rows 0-31, Cols 0-31

IDLE_STR = [
    "                                ", # 0
    "                                ", # 1
    "                                ", # 2
    "             OOOOO              ", # 3
    "            OHHHhhO             ", # 4
    "           OHHHHHhhO            ", # 5
    "           OHHHSSSSO            ", # 6
    "          OHHHSsEsEO            ", # 7
    "          OHHSSsEsEO            ", # 8
    "          OHHSSSSSSO            ", # 9
    "           OHHsSSsO             ", # 10
    "           OOHssSO              ", # 11
    "          OKKOOWWO              ", # 12
    "         OKJKOOWWWO             ", # 13
    "        OKKKOOWWCWWO            ", # 14
    "        OKKKOOWWWwWO            ", # 15
    "        OKkkOOWWwwWO            ", # 16
    "         OkOOOWWwwWO            ", # 17
    "          OO OWwTTwO            ", # 18
    "            OLLLLLLO            ", # 19
    "            OBBBBBBO            ", # 20
    "            OBBbBBbO            ", # 21
    "            OBBbOBbO            ", # 22
    "            OBbO OBbO           ", # 23
    "            OSO  OSO            ", # 24
    "            OSO  OSO            ", # 25
    "            OGO  OGO            ", # 26
    "            OGgO OGgO           ", # 27
    "            OXXO OXXO           ", # 28
    "            OxxO OxxO           ", # 29
    "             OO   OO            ", # 30
    "                                "  # 31
]

RUN1_STR = [
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
    "         OKJKOOWWOO             ", # 11
    "        OKKKOOWWWOwO            ", # 12
    "        OKKKOOWWCWwSO           ", # 13
    "        OKkkOOWWWwwSO           ", # 14
    "         OkOOOWWwwWOO           ", # 15
    "          OO OWwTTwO            ", # 16
    "            OLLLLLLO            ", # 17
    "           OBBBBBBBO            ", # 18
    "          OBBbBBBbbO            ", # 19
    "         OBBbO  OBbO            ", # 20
    "         OBbO    OBbO           ", # 21
    "         OSO      OSO           ", # 22
    "         OGO       OGO          ", # 23
    "         OGgO      OGgO         ", # 24
    "        OXXXO       OXXO        ", # 25
    "        OxxxO       OxxO        ", # 26
    "         OOO         OO         ", # 27
    "                                ", # 28
    "                                ", # 29
    "                                ", # 30
    "                                "  # 31
]

RUN2_STR = [
    "                                ", # 0
    "                                ", # 1
    "                                ", # 2
    "             OOOOO              ", # 3
    "            OHHHhhO             ", # 4
    "           OHHHHHhhO            ", # 5
    "           OHHHSSSSO            ", # 6
    "          OHHHSsEsEO            ", # 7
    "          OHHSSsEsEO            ", # 8
    "          OHHSSSSSSO            ", # 9
    "           OHHsSSsO             ", # 10
    "          OKKOssSO              ", # 11
    "         OKJKOOWWWO             ", # 12
    "        OKKKOOWWCWWO            ", # 13
    "        OKKKOOWWWwWO            ", # 14
    "        OKkkOOWWwwWOS           ", # 15
    "         OkOOOWWwwWOS           ", # 16
    "          OO OWwTTwOO           ", # 17
    "            OLLLLLLO            ", # 18
    "            OBBBBBBO            ", # 19
    "            OBBbBBbO            ", # 20
    "            OBBbOBbO            ", # 21
    "            OBbO  OSO           ", # 22
    "            OSO   OGO           ", # 23
    "            OGO   OGgO          ", # 24
    "            OGgO  OXXO          ", # 25
    "            OXXO  OxxO          ", # 26
    "            OxxO   OO           ", # 27
    "             OO                 ", # 28
    "                                ", # 29
    "                                ", # 30
    "                                "  # 31
]

RUN3_STR = [
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
    "         OKJKOOWWO              ", # 11
    "        OKKKOOWWWO              ", # 12
    "        OKKKOOWWCWWO            ", # 13
    "        OKkkOOWWWwWO            ", # 14
    "        SOkOOOWWwwWO            ", # 15
    "        SO OO OWwTTwO           ", # 16
    "        OO   OLLLLLLO           ", # 17
    "            OBBBBBBBO           ", # 18
    "           OBBbBBBbbO           ", # 19
    "           OBbO  OBBbO          ", # 20
    "          OBbO    OBbO          ", # 21
    "          OSO      OSO          ", # 22
    "          OGO       OGO         ", # 23
    "          OGgO      OGgO        ", # 24
    "          OXXO       OXXXO      ", # 25
    "          OxxO       OxxxO      ", # 26
    "           OO         OOO       ", # 27
    "                                ", # 28
    "                                ", # 29
    "                                ", # 30
    "                                "  # 31
]

RUN4_STR = [
    "                                ", # 0
    "                                ", # 1
    "                                ", # 2
    "             OOOOO              ", # 3
    "            OHHHhhO             ", # 4
    "           OHHHHHhhO            ", # 5
    "           OHHHSSSSO            ", # 6
    "          OHHHSsEsEO            ", # 7
    "          OHHSSsEsEO            ", # 8
    "          OHHSSSSSSO            ", # 9
    "           OHHsSSsO             ", # 10
    "          OKKOssSO              ", # 11
    "         OKJKOOWWWO             ", # 12
    "        OKKKOOWWCWWO            ", # 13
    "        OKKKOOWWWwWO            ", # 14
    "        OKkkOOWWwwWO            ", # 15
    "         OkOOOWWwwWSO           ", # 16
    "          OO OWwTTwSO           ", # 17
    "            OLLLLLLOO           ", # 18
    "            OBBBBBBO            ", # 19
    "            OBBbBBbO            ", # 20
    "            OBBbOBbO            ", # 21
    "            OSO  OBbO           ", # 22
    "            OGO   OSO           ", # 23
    "            OGgO  OGO           ", # 24
    "            OXXO  OGgO          ", # 25
    "            OxxO  OXXO          ", # 26
    "             OO   OxxO          ", # 27
    "                   OO           ", # 28
    "                                ", # 29
    "                                ", # 30
    "                                "  # 31
]

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
    
    # Left facing variants
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
    
    for name, img in {**frames, **left_frames}.items():
        p = os.path.join(out_dir, name)
        img.save(p)
        print(f'Saved {p}')
        
    # Generate spritesheet (6 frames wide: Idle, Run1, Run2, Run3, Run4, Jump)
    sheet = Image.new('RGBA', (32 * 6, 32), (0, 0, 0, 0))
    ordered_keys = ['player_idle.png', 'player_run_1.png', 'player_run_2.png', 'player_run_3.png', 'player_run_4.png', 'player_jump.png']
    for idx, k in enumerate(ordered_keys):
        sheet.paste(frames[k], (idx * 32, 0))
    sheet_path = os.path.join(out_dir, 'player_spritesheet.png')
    sheet.save(sheet_path)
    print(f'Saved {sheet_path}')
