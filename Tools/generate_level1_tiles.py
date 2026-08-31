#!/usr/bin/env python3
"""32x32 8-bit tiles for Level 1: dorm floors/walls, the soi/road, traps."""

import hashlib
import os
from PIL import Image, ImageDraw

PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIRS = [
    os.path.join(PROJECT, "Assets", "Art", "Sprites"),
    os.path.join(PROJECT, "Assets", "Resources", "Sprites"),
]


def guid_for(seed: str) -> str:
    return hashlib.md5(("late-to-kosen::sprite:" + seed).encode()).hexdigest()


def px(h):
    h = h.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), 255)


def hash_n(x, y, salt=0):
    n = (x * 374761393 + y * 668265263 + salt * 1274126177) & 0xFFFFFFFF
    n = (n ^ (n >> 13)) * 1274126177 & 0xFFFFFFFF
    return n


def put(img, x, y, c):
    img.putpixel((x % 32, y % 32), c)


def new_img():
    return Image.new("RGBA", (32, 32), (0, 0, 0, 0))


def tile_dorm_floor():
    """Worn linoleum tiles — dorm corridor."""
    grout = px("8b7355")
    a = px("e8d5b7")
    b = px("dcc4a0")
    c = px("c9ad86")
    spec = px("f4ead8")
    img = new_img()
    for y in range(32):
        for x in range(32):
            if x % 16 == 0 or y % 16 == 0:
                img.putpixel((x, y), grout)
                continue
            tx, ty = x // 16, y // 16
            base = a if (tx + ty) % 2 == 0 else b
            n = hash_n(x, y, 3) % 11
            if n == 0:
                col = c
            elif n == 1:
                col = spec
            else:
                col = base
            img.putpixel((x, y), col)
    return img


def tile_dorm_wall():
    """Painted brick — stairwell shafts."""
    mortar = px("5c4033")
    bricks = [px("c4a574"), px("d4b896"), px("b8956a"), px("c9aa7e"), px("a67c52")]
    img = new_img()
    bh, bw = 8, 16
    for y in range(32):
        row = y // bh
        shift = (row % 2) * (bw // 2)
        for x in range(32):
            if y % bh == 0 or (x + shift) % bw == 0:
                img.putpixel((x, y), mortar)
            else:
                bx = (x + shift) // bw
                img.putpixel((x, y), bricks[hash_n(bx, row, 9) % len(bricks)])
    return img


def tile_road():
    """Asphalt with a yellow edge so 1-unit platforms read as a road surface."""
    dark = px("2b2f36")
    mid = px("3a4049")
    light = px("4c5560")
    line = px("eab308")
    line_d = px("a16207")
    img = new_img()
    for y in range(32):
        for x in range(32):
            n = hash_n(x, y, 21) % 17
            if n == 0:
                col = light
            elif n < 6:
                col = mid
            else:
                col = dark
            img.putpixel((x, y), col)
    # PIL y=0 is the top of the PNG, which is the walkable edge of the platform.
    for x in range(32):
        img.putpixel((x, 0), line_d)
        img.putpixel((x, 1), line if (x // 6) % 2 == 0 else line_d)
        img.putpixel((x, 2), line_d)
    return img


def tile_kerb():
    """Concrete kerb / forecourt pavement."""
    grout = px("64748b")
    a = px("94a3b8")
    b = px("cbd5e1")
    c = px("7b8794")
    img = new_img()
    for y in range(32):
        for x in range(32):
            if x % 16 == 0 or y % 16 == 0:
                img.putpixel((x, y), grout)
                continue
            n = hash_n(x, y, 44) % 9
            if n == 0:
                col = c
            elif n == 1:
                col = b
            else:
                col = a
            img.putpixel((x, y), col)
    return img


def spr_trap():
    """Laundry basket — the honest visible trap."""
    img = new_img()
    O = px("0f172a")
    R = px("dc2626")
    r = px("991b1b")
    C = px("f8fafc")
    B = px("fb923c")
    b = px("c2410c")
    # basket body
    for y in range(12, 28):
        for x in range(6, 26):
            if y == 12 or y == 27 or x == 6 or x == 25:
                img.putpixel((x, y), O)
            elif y > 24:
                img.putpixel((x, y), r)
            elif ((x + y) % 3) == 0:
                img.putpixel((x, y), B)
            else:
                img.putpixel((x, y), b)
    # rim
    for x in range(5, 27):
        img.putpixel((x, 11), O)
        if 6 <= x <= 25:
            img.putpixel((x, 12), R)
    # clothes peeking out
    for x, y, c in [
        (10, 8, C), (11, 8, C), (12, 8, C), (11, 9, C), (12, 9, R),
        (13, 9, R), (14, 9, R), (15, 8, R), (16, 8, C), (17, 9, C),
        (18, 9, px("1d4ed8")), (19, 8, px("1d4ed8")), (20, 9, C),
        (12, 10, R), (13, 10, C), (17, 10, C), (18, 10, px("1d4ed8")),
    ]:
        img.putpixel((x, y), c)
        img.putpixel((x, y - 1), O if y == 8 else img.getpixel((x, y - 1)))
    for x in range(10, 21):
        if img.getpixel((x, 7))[3] == 0:
            img.putpixel((x, 7), O)
    return img


def spr_trap_spike():
    """Floor-fan / spike that rises from the ground."""
    img = new_img()
    O = px("0f172a")
    M = px("94a3b8")
    D = px("334155")
    H = px("e2e8f0")
    R = px("ef4444")
    # three spikes
    tips = [(8, 4), (16, 2), (24, 4)]
    for cx, top in tips:
        for y in range(top, 28):
            half = max(1, int((y - top) * 0.35) + 1)
            for x in range(cx - half, cx + half + 1):
                if x < 0 or x > 31:
                    continue
                if x == cx - half or x == cx + half or y == 27:
                    img.putpixel((x, y), O)
                elif x == cx:
                    img.putpixel((x, y), H)
                elif abs(x - cx) == 1:
                    img.putpixel((x, y), M)
                else:
                    img.putpixel((x, y), D)
        img.putpixel((cx, top), R)
    return img


def spr_trap_hidden():
    """Wet-floor gotcha, shown after it kills you."""
    img = new_img()
    O = px("0f172a")
    Y = px("facc15")
    y = px("ca8a04")
    K = px("111827")
    for row in range(32):
        for col in range(32):
            band = ((col + row) // 6) % 2
            img.putpixel((col, row), Y if band == 0 else K)
    # puddle oval
    for row in range(8, 24):
        for col in range(4, 28):
            dx = (col - 16) / 12.0
            dy = (row - 16) / 7.0
            if dx * dx + dy * dy <= 1.0:
                img.putpixel((col, row), y if (col + row) % 5 == 0 else px("38bdf8"))
                if abs(dx * dx + dy * dy - 1.0) < 0.18:
                    img.putpixel((col, row), O)
    return img


def fill_rect(img, x0, y0, x1, y1, c):
    for y in range(y0, y1):
        for x in range(x0, x1):
            if 0 <= x < img.size[0] and 0 <= y < img.size[1]:
                img.putpixel((x, y), c)


def spr_elevator():
    """Dorm lift, 2 x 3 world units at 32 PPU (64 x 96 px)."""
    img = Image.new("RGBA", (64, 96), (0, 0, 0, 0))
    O = px("0f172a")
    frame = px("64748b")
    frame_d = px("334155")
    panel = px("94a3b8")
    door = px("cbd5e1")
    door_d = px("64748b")
    gap = px("1e293b")
    gold = px("eab308")
    red = px("ef4444")
    dark = px("0f172a")
    fill_rect(img, 2, 2, 62, 94, O)
    fill_rect(img, 4, 4, 60, 92, frame)
    fill_rect(img, 6, 6, 58, 18, frame_d)
    fill_rect(img, 8, 8, 56, 16, panel)
    fill_rect(img, 26, 10, 38, 14, dark)
    fill_rect(img, 28, 11, 31, 13, gold)
    fill_rect(img, 33, 11, 36, 13, red)
    fill_rect(img, 8, 20, 56, 88, O)
    fill_rect(img, 10, 22, 31, 86, door)
    fill_rect(img, 33, 22, 54, 86, door)
    fill_rect(img, 31, 22, 33, 86, gap)
    for y in range(24, 84, 6):
        fill_rect(img, 12, y, 29, y + 1, door_d)
        fill_rect(img, 35, y, 52, y + 1, door_d)
    fill_rect(img, 12, 48, 16, 56, frame_d)
    fill_rect(img, 48, 48, 52, 56, frame_d)
    fill_rect(img, 4, 88, 60, 92, frame_d)
    return img


def spr_flowerpot():
    """Terracotta pot with a plant, balcony hazard."""
    img = new_img()
    O = px("0f172a")
    pot = px("c2410c")
    pot_l = px("fb923c")
    pot_d = px("7c2d12")
    dirt = px("44403c")
    leaf = px("16a34a")
    leaf_d = px("14532d")
    flower = px("e11d48")
    # plant
    for x, y, c in [
        (16, 4, leaf), (15, 5, leaf), (16, 5, leaf_d), (17, 5, leaf),
        (14, 6, leaf), (16, 6, leaf_d), (18, 6, leaf),
        (13, 7, leaf), (15, 7, leaf), (16, 7, O), (17, 7, leaf), (19, 7, leaf),
        (12, 8, leaf_d), (16, 8, leaf_d), (20, 8, leaf),
        (14, 9, leaf), (16, 9, leaf_d), (18, 9, leaf),
        (16, 10, leaf_d), (15, 10, leaf), (17, 10, leaf),
        (11, 6, flower), (21, 7, flower), (13, 5, px("fde047")),
    ]:
        img.putpixel((x, y), c)
    # rim
    fill_rect(img, 8, 12, 24, 15, O)
    fill_rect(img, 9, 13, 23, 14, pot_l)
    # body
    for y in range(15, 28):
        inset = (y - 15) // 4
        x0, x1 = 9 + inset, 23 - inset
        fill_rect(img, x0, y, x1, y + 1, O)
        fill_rect(img, x0 + 1, y, x1 - 1, y + 1, pot if y < 24 else pot_d)
        if y < 18:
            fill_rect(img, x0 + 2, y, x1 - 4, y + 1, pot_l)
    fill_rect(img, 12, 15, 20, 17, dirt)
    return img


def spr_trap_laundry():
    """Pile of laundry in a basket."""
    img = new_img()
    O = px("0f172a")
    B = px("fb923c")
    Bd = px("c2410c")
    W = px("f8fafc")
    R = px("dc2626")
    Bl = px("3b82f6")
    fill_rect(img, 6, 14, 26, 28, O)
    fill_rect(img, 7, 15, 25, 27, B)
    for y in range(16, 26):
        for x in range(8, 24):
            if (x + y) % 3 == 0:
                img.putpixel((x, y), Bd)
    fill_rect(img, 5, 13, 27, 16, O)
    fill_rect(img, 6, 14, 26, 15, B)
    fill_rect(img, 10, 8, 14, 15, W)
    fill_rect(img, 13, 7, 19, 14, R)
    fill_rect(img, 17, 9, 22, 15, Bl)
    fill_rect(img, 12, 6, 16, 8, O)
    return img


def spr_trap_mopbucket():
    """Yellow mop bucket with a mop."""
    img = new_img()
    O = px("0f172a")
    Y = px("facc15")
    Yd = px("ca8a04")
    stick = px("a16207")
    head = px("64748b")
    fill_rect(img, 8, 16, 24, 28, O)
    fill_rect(img, 9, 17, 23, 27, Y)
    fill_rect(img, 9, 24, 23, 27, Yd)
    fill_rect(img, 7, 16, 25, 18, O)
    fill_rect(img, 8, 17, 24, 18, Yd)
    fill_rect(img, 15, 4, 17, 20, O)
    fill_rect(img, 16, 5, 17, 19, stick)
    fill_rect(img, 11, 2, 21, 6, O)
    fill_rect(img, 12, 3, 20, 5, head)
    return img


def spr_trap_extinguisher():
    """Red fire extinguisher."""
    img = new_img()
    O = px("0f172a")
    R = px("dc2626")
    Rd = px("991b1b")
    M = px("94a3b8")
    fill_rect(img, 11, 8, 21, 28, O)
    fill_rect(img, 12, 9, 20, 27, R)
    fill_rect(img, 12, 22, 20, 27, Rd)
    fill_rect(img, 14, 9, 16, 20, px("fca5a5"))
    fill_rect(img, 10, 6, 22, 9, O)
    fill_rect(img, 11, 7, 21, 8, M)
    fill_rect(img, 18, 3, 20, 8, O)
    fill_rect(img, 19, 2, 26, 4, O)
    fill_rect(img, 20, 2, 25, 3, M)
    fill_rect(img, 13, 4, 17, 7, M)
    return img


def spr_trap_recycling():
    """Blue recycling bin."""
    img = new_img()
    O = px("0f172a")
    B = px("2563eb")
    Bd = px("1e3a8a")
    L = px("93c5fd")
    fill_rect(img, 7, 10, 25, 28, O)
    fill_rect(img, 8, 11, 24, 27, B)
    fill_rect(img, 8, 22, 24, 27, Bd)
    fill_rect(img, 6, 9, 26, 12, O)
    fill_rect(img, 7, 10, 25, 11, L)
    for x, y in [(12, 16), (13, 15), (14, 14), (15, 15), (16, 16),
                 (16, 17), (15, 18), (14, 19), (13, 18), (12, 17)]:
        img.putpixel((x, y), L)
        img.putpixel((x + 4, y), L)
    return img


def spr_trap_bin():
    """Dark hallway trash bin."""
    img = new_img()
    O = px("0f172a")
    G = px("3f3f46")
    Gd = px("18181b")
    L = px("a1a1aa")
    fill_rect(img, 8, 12, 24, 28, O)
    fill_rect(img, 9, 13, 23, 27, G)
    fill_rect(img, 9, 22, 23, 27, Gd)
    fill_rect(img, 7, 10, 25, 14, O)
    fill_rect(img, 8, 11, 24, 13, L)
    fill_rect(img, 14, 8, 18, 11, O)
    fill_rect(img, 15, 9, 17, 11, L)
    return img


def spr_trap_post():
    """Notice post in the lobby."""
    img = new_img()
    O = px("0f172a")
    wood = px("a16207")
    wood_d = px("78350f")
    paper = px("fef3c7")
    fill_rect(img, 14, 4, 18, 28, O)
    fill_rect(img, 15, 5, 17, 27, wood)
    fill_rect(img, 15, 20, 17, 27, wood_d)
    fill_rect(img, 8, 6, 24, 16, O)
    fill_rect(img, 9, 7, 23, 15, paper)
    fill_rect(img, 10, 9, 22, 10, O)
    fill_rect(img, 10, 12, 18, 13, O)
    return img


def spr_trap_floorfan():
    """Floor fan — the spike that rises in the dorm room."""
    img = new_img()
    O = px("0f172a")
    M = px("94a3b8")
    Md = px("334155")
    L = px("e2e8f0")
    fill_rect(img, 6, 24, 26, 30, O)
    fill_rect(img, 7, 25, 25, 29, Md)
    fill_rect(img, 14, 18, 18, 25, O)
    fill_rect(img, 15, 19, 17, 24, M)
    for y in range(6, 20):
        for x in range(6, 26):
            dx, dy = x - 16, y - 12
            d2 = dx * dx + dy * dy
            if 64 <= d2 <= 81:
                img.putpixel((x, y), O)
            elif d2 < 64:
                img.putpixel((x, y), L if (dx + dy) % 4 == 0 else M)
    fill_rect(img, 15, 11, 17, 13, O)
    return img


def spr_trap_riser():
    """Stair-riser spikes."""
    img = new_img()
    O = px("0f172a")
    M = px("cbd5e1")
    D = px("334155")
    R = px("ef4444")
    fill_rect(img, 2, 24, 30, 30, O)
    fill_rect(img, 3, 25, 29, 29, D)
    for cx in (7, 16, 25):
        for y in range(6, 26):
            half = max(1, (y - 6) // 4)
            for x in range(cx - half, cx + half + 1):
                if 0 <= x < 32:
                    img.putpixel((x, y), O if x in (cx - half, cx + half) else (M if x == cx else D))
        img.putpixel((cx, 6), R)
    return img


def spr_trap_wetfloor():
    return spr_trap_hidden()


def spr_trap_landing():
    """Loose / cracked landing tile — hidden until it kills you."""
    img = new_img()
    O = px("0f172a")
    A = px("e8d5b7")
    B = px("c9ad86")
    C = px("7c2d12")
    fill_rect(img, 2, 8, 30, 24, O)
    fill_rect(img, 3, 9, 29, 23, A)
    for y in range(10, 22):
        for x in range(4, 28):
            if (x + y * 3) % 11 == 0:
                img.putpixel((x, y), B)
    for x in range(8, 24):
        img.putpixel((x, 12 + (x % 3)), C)
        img.putpixel((x, 16 - (x % 2)), C)
    return img


def spr_trap_cable():
    """Loose cable on the soi."""
    img = new_img()
    O = px("0f172a")
    K = px("1c1917")
    Y = px("eab308")
    fill_rect(img, 4, 18, 28, 24, O)
    fill_rect(img, 5, 19, 27, 23, K)
    for x in range(6, 26):
        img.putpixel((x, 20 + (1 if x % 4 < 2 else 0)), Y)
    fill_rect(img, 3, 16, 8, 26, O)
    fill_rect(img, 4, 17, 7, 25, Y)
    return img


def spr_trap_roadworks():
    """Roadworks barrier."""
    img = new_img()
    O = px("0f172a")
    R = px("dc2626")
    W = px("f8fafc")
    fill_rect(img, 4, 10, 28, 22, O)
    for y in range(11, 21):
        for x in range(5, 27):
            img.putpixel((x, y), R if ((x + y) // 4) % 2 == 0 else W)
    fill_rect(img, 6, 20, 10, 28, O)
    fill_rect(img, 22, 20, 26, 28, O)
    fill_rect(img, 7, 21, 9, 27, px("57534e"))
    fill_rect(img, 23, 21, 25, 27, px("57534e"))
    return img


def spr_trap_bollard():
    """Traffic bollard."""
    img = new_img()
    O = px("0f172a")
    Y = px("facc15")
    K = px("111827")
    fill_rect(img, 12, 4, 20, 28, O)
    fill_rect(img, 13, 5, 19, 27, Y)
    fill_rect(img, 13, 8, 19, 12, K)
    fill_rect(img, 13, 16, 19, 20, K)
    fill_rect(img, 10, 26, 22, 30, O)
    fill_rect(img, 11, 27, 21, 29, px("334155"))
    return img


def spr_trap_doorstep():
    """Hidden doorstep at the fake entrance."""
    img = new_img()
    O = px("0f172a")
    A = px("94a3b8")
    B = px("64748b")
    fill_rect(img, 2, 10, 30, 22, O)
    fill_rect(img, 3, 11, 29, 21, A)
    fill_rect(img, 3, 18, 29, 21, B)
    fill_rect(img, 8, 12, 24, 13, O)
    return img


def spr_bicycle():
    """Anywheel rental — cyan frame, lock on the back wheel."""
    img = Image.new("RGBA", (48, 32), (0, 0, 0, 0))
    O = px("0f172a")
    C = px("22d3ee")
    Cd = px("0e7490")
    T = px("e2e8f0")
    lock = px("f97316")

    def wheel(cx, cy, r):
        for y in range(cy - r, cy + r + 1):
            for x in range(cx - r, cx + r + 1):
                d2 = (x - cx) ** 2 + (y - cy) ** 2
                if r * r - 6 <= d2 <= r * r + 2:
                    img.putpixel((x, y), O)
                elif d2 <= r * r - 8:
                    img.putpixel((x, y), T if d2 % 7 == 0 else Cd)

    wheel(10, 22, 8)
    wheel(36, 22, 8)
    fill_rect(img, 10, 14, 36, 16, O)
    fill_rect(img, 11, 13, 35, 15, C)
    fill_rect(img, 18, 8, 28, 10, O)
    fill_rect(img, 19, 7, 27, 9, C)
    fill_rect(img, 26, 4, 28, 14, O)
    fill_rect(img, 27, 4, 34, 6, O)
    fill_rect(img, 28, 3, 33, 5, C)
    fill_rect(img, 8, 12, 12, 22, O)
    fill_rect(img, 9, 13, 11, 21, C)
    fill_rect(img, 34, 12, 38, 22, O)
    fill_rect(img, 35, 13, 37, 21, C)
    fill_rect(img, 32, 18, 40, 22, lock)
    fill_rect(img, 33, 17, 39, 18, O)
    return img


def spr_ajarn_bike():
    """Lecturer chasing on a bike."""
    img = Image.new("RGBA", (48, 48), (0, 0, 0, 0))
    O = px("0f172a")
    skin = px("ffd7a8")
    hair = px("1c1917")
    shirt = px("e2e8f0")
    shirt_d = px("94a3b8")
    pants = px("1e3a8a")
    C = px("22d3ee")
    Cd = px("0e7490")
    T = px("e2e8f0")

    def wheel(cx, cy, r):
        for y in range(cy - r, cy + r + 1):
            for x in range(cx - r, cx + r + 1):
                if 0 <= x < 48 and 0 <= y < 48:
                    d2 = (x - cx) ** 2 + (y - cy) ** 2
                    if r * r - 5 <= d2 <= r * r + 2:
                        img.putpixel((x, y), O)
                    elif d2 <= r * r - 7:
                        img.putpixel((x, y), T if (x + y) % 5 == 0 else Cd)

    wheel(12, 38, 8)
    wheel(36, 38, 8)
    fill_rect(img, 12, 30, 36, 32, O)
    fill_rect(img, 13, 29, 35, 31, C)
    fill_rect(img, 24, 20, 26, 30, O)
    fill_rect(img, 26, 18, 34, 20, C)
    fill_rect(img, 10, 28, 14, 38, C)
    fill_rect(img, 34, 28, 38, 38, C)
    # rider
    fill_rect(img, 20, 6, 30, 14, O)
    fill_rect(img, 21, 7, 29, 13, hair)
    fill_rect(img, 22, 10, 28, 14, skin)
    img.putpixel((23, 11), O)
    img.putpixel((27, 11), O)
    fill_rect(img, 22, 12, 28, 13, px("334155"))  # glasses bar
    fill_rect(img, 20, 14, 30, 24, O)
    fill_rect(img, 21, 15, 29, 23, shirt)
    fill_rect(img, 21, 20, 29, 23, shirt_d)
    fill_rect(img, 18, 23, 22, 30, pants)
    fill_rect(img, 26, 23, 32, 28, pants)
    fill_rect(img, 30, 16, 34, 20, skin)
    return img


def spr_bike_rack():
    """Anywheel parking — three inverted-U racks on a pad. Same art for fake."""
    img = Image.new("RGBA", (84, 40), (0, 0, 0, 0))
    O = px("0f172a")
    metal = px("94a3b8")
    metal_l = px("e2e8f0")
    pad = px("64748b")
    pad_d = px("334155")
    sign = px("facc15")
    fill_rect(img, 4, 32, 80, 40, pad_d)
    fill_rect(img, 6, 30, 78, 36, pad)
    for cx in (18, 42, 66):
        fill_rect(img, cx - 6, 10, cx - 4, 32, O)
        fill_rect(img, cx + 4, 10, cx + 6, 32, O)
        fill_rect(img, cx - 6, 8, cx + 6, 12, O)
        fill_rect(img, cx - 5, 11, cx - 3, 31, metal)
        fill_rect(img, cx + 3, 11, cx + 5, 31, metal)
        fill_rect(img, cx - 5, 9, cx + 5, 11, metal_l)
    fill_rect(img, 70, 4, 72, 32, O)
    fill_rect(img, 60, 2, 82, 14, O)
    fill_rect(img, 61, 3, 81, 13, sign)
    return img


def spr_lizard():
    """Water monitor (ตัวเงินตัวทอง), side-on, facing right."""
    img = new_img()
    O = px("0f172a")
    G = px("4d7c0f")
    GL = px("a3e635")
    GD = px("365314")
    Gold = px("eab308")
    eye = px("fef08a")
    # tail
    fill_rect(img, 1, 14, 8, 18, O)
    fill_rect(img, 2, 15, 8, 17, Gold)
    fill_rect(img, 4, 13, 10, 19, O)
    fill_rect(img, 5, 14, 10, 18, G)
    # body
    fill_rect(img, 8, 11, 24, 21, O)
    fill_rect(img, 9, 12, 23, 20, G)
    fill_rect(img, 10, 13, 22, 15, GL)
    for x in range(10, 22, 3):
        fill_rect(img, x, 16, x + 2, 19, Gold)
    # legs
    fill_rect(img, 11, 19, 14, 26, O)
    fill_rect(img, 12, 20, 13, 25, GD)
    fill_rect(img, 18, 19, 21, 26, O)
    fill_rect(img, 19, 20, 20, 25, GD)
    fill_rect(img, 11, 24, 15, 26, O)
    fill_rect(img, 18, 24, 22, 26, O)
    # neck + head
    fill_rect(img, 22, 10, 27, 17, O)
    fill_rect(img, 23, 11, 26, 16, G)
    fill_rect(img, 25, 8, 31, 16, O)
    fill_rect(img, 26, 9, 30, 15, GL)
    fill_rect(img, 27, 10, 29, 12, eye)
    img.putpixel((29, 11), O)
    fill_rect(img, 29, 13, 31, 15, GD)
    return img


def tile_school_floor():
    """KOSEN corridor linoleum — cream tiles with a green walkable lip."""
    grout = px("64748b")
    a = px("e2e8f0")
    b = px("cbd5e1")
    c = px("94a3b8")
    spec = px("f8fafc")
    lip = px("16a34a")
    lip_d = px("166534")
    img = new_img()
    for y in range(32):
        for x in range(32):
            if y <= 2:
                img.putpixel((x, y), lip if y == 1 else lip_d)
                continue
            if x % 16 == 0 or y % 16 == 0:
                img.putpixel((x, y), grout)
                continue
            tx, ty = x // 16, y // 16
            base = a if (tx + ty) % 2 == 0 else b
            n = hash_n(x, y, 17) % 13
            if n == 0:
                col = c
            elif n == 1:
                col = spec
            else:
                col = base
            img.putpixel((x, y), col)
    return img


def tile_school_wall():
    """Classroom plaster with a birch dado rail."""
    plaster = px("f1f5f9")
    plaster_d = px("e2e8f0")
    wood = px("d97706")
    wood_d = px("92400e")
    wood_l = px("fbbf24")
    img = new_img()
    for y in range(32):
        for x in range(32):
            n = hash_n(x, y, 31) % 19
            col = plaster_d if n == 0 else plaster
            img.putpixel((x, y), col)
    for y in range(22, 27):
        for x in range(32):
            if y == 22 or y == 26:
                img.putpixel((x, y), wood_d)
            elif y == 23:
                img.putpixel((x, y), wood_l)
            else:
                img.putpixel((x, y), wood)
    return img


def tile_basement_floor():
    """Secret-ending slab — wet concrete, moss, hairline cracks."""
    dark = px("1e293b")
    mid = px("334155")
    light = px("475569")
    moss = px("3f6212")
    wet = px("0ea5e9")
    crack = px("0f172a")
    img = new_img()
    for y in range(32):
        for x in range(32):
            n = hash_n(x, y, 61) % 23
            if n == 0:
                col = light
            elif n < 8:
                col = mid
            else:
                col = dark
            if n == 2:
                col = moss
            elif n == 3:
                col = wet
            img.putpixel((x, y), col)
    for x in range(32):
        if 8 <= x <= 22:
            img.putpixel((x, 14 + (x % 3) // 2), crack)
        if 18 <= x <= 30:
            img.putpixel((x, 24), crack)
    return img


def tile_basement_wall():
    """Cinder-block basement wall."""
    mortar = px("1e293b")
    blocks = [px("475569"), px("334155"), px("64748b"), px("3f4f63"), px("52607a")]
    stain = px("365314")
    img = new_img()
    bh, bw = 8, 16
    for y in range(32):
        row = y // bh
        shift = (row % 2) * (bw // 2)
        for x in range(32):
            if y % bh == 0 or (x + shift) % bw == 0:
                img.putpixel((x, y), mortar)
            else:
                bx = (x + shift) // bw
                col = blocks[hash_n(bx, row, 77) % len(blocks)]
                if hash_n(x, y, 88) % 17 == 0:
                    col = stain
                img.putpixel((x, y), col)
    return img


def spr_trap_school():
    """School backpack — the honest visible trap on stage 2."""
    img = new_img()
    O = px("0f172a")
    N = px("1e3a8a")
    Nl = px("3b82f6")
    Nd = px("172554")
    R = px("dc2626")
    Y = px("facc15")
    C = px("f8fafc")
    # body
    fill_rect(img, 6, 8, 26, 30, O)
    fill_rect(img, 7, 9, 25, 29, N)
    fill_rect(img, 8, 10, 24, 16, Nl)
    fill_rect(img, 8, 22, 24, 28, Nd)
    # front pocket
    fill_rect(img, 9, 16, 23, 24, O)
    fill_rect(img, 10, 17, 22, 23, Nd)
    fill_rect(img, 10, 17, 22, 19, Y)
    # zipper pull
    fill_rect(img, 15, 18, 17, 22, R)
    # straps
    fill_rect(img, 8, 6, 12, 10, O)
    fill_rect(img, 9, 7, 11, 9, Nd)
    fill_rect(img, 20, 6, 24, 10, O)
    fill_rect(img, 21, 7, 23, 9, Nd)
    # notebook peeking out
    fill_rect(img, 12, 4, 20, 9, O)
    fill_rect(img, 13, 5, 19, 8, C)
    fill_rect(img, 13, 5, 14, 8, R)
    return img


def spr_trap_basement():
    """Rusty barrel — secret-ending trap."""
    img = new_img()
    O = px("0f172a")
    rust = px("9a3412")
    rust_l = px("c2410c")
    rust_d = px("7c2d12")
    band = px("78716c")
    drip = px("365314")
    fill_rect(img, 7, 4, 25, 30, O)
    fill_rect(img, 8, 5, 24, 29, rust)
    for y in range(6, 29):
        for x in range(9, 23):
            n = hash_n(x, y, 99) % 9
            if n == 0:
                img.putpixel((x, y), rust_l)
            elif n == 1:
                img.putpixel((x, y), rust_d)
    for y in (10, 18, 26):
        fill_rect(img, 8, y, 24, y + 2, band)
    fill_rect(img, 8, 5, 24, 8, rust_d)
    fill_rect(img, 14, 28, 17, 32, drip)
    fill_rect(img, 15, 27, 16, 31, drip)
    return img


META = """fileFormatVersion: 2
guid: {guid}
TextureImporter:
  internalIDToNameTable: []
  externalObjects: {{}}
  serializedVersion: 13
  mipmaps:
    mipMapMode: 0
    enableMipMap: 0
    sRGBTexture: 1
    linearTexture: 0
    fadeOut: 0
    borderMipMap: 0
    mipMapsPreserveCoverage: 0
    alphaTestReferenceValue: 0.5
    mipMapFadeDistanceStart: 1
    mipMapFadeDistanceEnd: 3
  bumpmap:
    convertToNormalMap: 0
    externalNormalMap: 0
    heightScale: 0.25
    normalMapFilter: 0
    flipGreenChannel: 0
  isReadable: 0
  streamingMipmaps: 0
  streamingMipmapsPriority: 0
  vTOnly: 0
  ignoreMipmapLimit: 0
  grayScaleToAlpha: 0
  generateCubemap: 6
  cubemapConvolution: 0
  seamlessCubemap: 0
  textureFormat: 1
  maxTextureSize: 2048
  textureSettings:
    serializedVersion: 2
    filterMode: 0
    aniso: 1
    mipBias: 0
    wrapU: 1
    wrapV: 1
    wrapW: 1
  nPOTScale: 0
  lightmap: 0
  compressionQuality: 50
  spriteMode: 1
  spriteExtrude: 0
  spriteMeshType: 0
  alignment: 0
  spritePivot: {{x: 0.5, y: 0.5}}
  spritePixelsToUnits: 32
  spriteBorder: {{x: 0, y: 0, z: 0, w: 0}}
  spriteGenerateFallbackPhysicsShape: 1
  alphaUsage: 1
  alphaIsTransparency: 1
  spriteTessellationDetail: -1
  textureType: 8
  textureShape: 1
  singleChannelComponent: 0
  flipbookRows: 1
  flipbookColumns: 1
  maxTextureSizeSet: 0
  compressionQualitySet: 0
  textureFormatSet: 0
  ignorePngGamma: 0
  applyGammaDecoding: 0
  swizzle: 50462976
  cookieLightType: 0
  platformSettings:
  - serializedVersion: 4
    buildTarget: DefaultTexturePlatform
    maxTextureSize: 2048
    resizeAlgorithm: 0
    textureFormat: -1
    textureCompression: 0
    compressionQuality: 50
    crunchedCompression: 0
    allowsAlphaSplitting: 0
    overridden: 0
    ignorePlatformSupport: 0
    androidETC2FallbackOverride: 0
    forceMaximumCompressionQuality_BC6H_BC7: 0
  - serializedVersion: 4
    buildTarget: Standalone
    maxTextureSize: 2048
    resizeAlgorithm: 0
    textureFormat: -1
    textureCompression: 0
    compressionQuality: 50
    crunchedCompression: 0
    allowsAlphaSplitting: 0
    overridden: 0
    ignorePlatformSupport: 0
    androidETC2FallbackOverride: 0
    forceMaximumCompressionQuality_BC6H_BC7: 0
  spriteSheet:
    serializedVersion: 2
    sprites: []
    outline: []
    customData:
    physicsShape: []
    bones: []
    spriteID: 5e97eb03825dee720800000000000000
    internalID: 21300000
    vertices: []
    indices:
    edges: []
    weights: []
    secondaryTextures: []
    spriteCustomMetadata:
      entries: []
    nameFileIdTable: {{}}
  mipmapLimitGroupName:
  pSDRemoveMatte: 0
  userData:
  assetBundleName:
  assetBundleVariant:
"""

SPRITES = {
    "tile_dorm_floor.png": tile_dorm_floor,
    "tile_dorm_wall.png": tile_dorm_wall,
    "tile_school_floor.png": tile_school_floor,
    "tile_school_wall.png": tile_school_wall,
    "tile_basement_floor.png": tile_basement_floor,
    "tile_basement_wall.png": tile_basement_wall,
    "tile_road.png": tile_road,
    "tile_kerb.png": tile_kerb,
    "spr_trap.png": spr_trap,
    "spr_trap_school.png": spr_trap_school,
    "spr_trap_basement.png": spr_trap_basement,
    "spr_trap_spike.png": spr_trap_spike,
    "spr_trap_hidden.png": spr_trap_hidden,
    "spr_trap_laundry.png": spr_trap_laundry,
    "spr_trap_mopbucket.png": spr_trap_mopbucket,
    "spr_trap_extinguisher.png": spr_trap_extinguisher,
    "spr_trap_recycling.png": spr_trap_recycling,
    "spr_trap_bin.png": spr_trap_bin,
    "spr_trap_post.png": spr_trap_post,
    "spr_trap_floorfan.png": spr_trap_floorfan,
    "spr_trap_riser.png": spr_trap_riser,
    "spr_trap_wetfloor.png": spr_trap_wetfloor,
    "spr_trap_landing.png": spr_trap_landing,
    "spr_trap_cable.png": spr_trap_cable,
    "spr_trap_roadworks.png": spr_trap_roadworks,
    "spr_trap_bollard.png": spr_trap_bollard,
    "spr_trap_doorstep.png": spr_trap_doorstep,
    "spr_elevator.png": spr_elevator,
    "spr_flowerpot.png": spr_flowerpot,
    "spr_bicycle.png": spr_bicycle,
    "spr_ajarn_bike.png": spr_ajarn_bike,
    "spr_bike_rack.png": spr_bike_rack,
    "spr_lizard.png": spr_lizard,
}


def main():
    import sys
    wanted = set(sys.argv[1:])
    for d in OUT_DIRS:
        os.makedirs(d, exist_ok=True)
    for name, fn in SPRITES.items():
        if wanted and name not in wanted:
            continue
        img = fn()
        for d in OUT_DIRS:
            path = os.path.join(d, name)
            img.save(path)
            seed = os.path.basename(d) + ":" + name
            with open(path + ".meta", "w", encoding="utf-8", newline="\n") as fh:
                fh.write(META.format(guid=guid_for(seed)))
        print("wrote", name)
    print("done")


if __name__ == "__main__":
    main()
