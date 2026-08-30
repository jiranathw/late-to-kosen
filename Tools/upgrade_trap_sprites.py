#!/usr/bin/env python3
"""
Upgrades all obstacle and trap sprites to fill the 32x32 hit block (hitbox) fully:
- spr_trap_laundry.png
- spr_trap_mopbucket.png
- spr_trap_extinguisher.png
- spr_trap_recycling.png
- spr_trap_bin.png
- spr_trap_post.png
- spr_trap_floorfan.png
- spr_trap_riser.png
- spr_trap_wetfloor.png
- spr_trap_hidden.png
- spr_trap_cable.png
- spr_trap_roadworks.png
- spr_trap_bollard.png
- spr_trap_doorstep.png
- spr_flowerpot.png
- spr_trap.png
- spr_trap_spike.png
- trap_hazard.png
"""

import os
from PIL import Image

def px(h):
    h = h.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), 255)

def new_img():
    return Image.new("RGBA", (32, 32), (0, 0, 0, 0))

def fill_rect(img, x0, y0, x1, y1, c):
    for y in range(y0, y1):
        for x in range(x0, x1):
            if 0 <= x < 32 and 0 <= y < 32:
                img.putpixel((x, y), c)

O = px("0f172a") # Thick dark outline

# 1. Laundry Basket (Large & Full)
def spr_trap_laundry():
    img = new_img()
    B = px("fb923c")    # Basket orange
    Bd = px("c2410c")   # Basket shadow
    W = px("f8fafc")    # White shirt
    R = px("ef4444")    # Red towel
    Bl = px("3b82f6")   # Blue jeans
    Gr = px("10b981")   # Green detergent bottle

    # Clothes pile overflowing at top (y: 2 to 14, x: 3 to 29)
    fill_rect(img, 5, 3, 13, 14, O)
    fill_rect(img, 6, 4, 12, 13, W)
    fill_rect(img, 11, 2, 21, 14, O)
    fill_rect(img, 12, 3, 20, 13, R)
    fill_rect(img, 18, 4, 27, 14, O)
    fill_rect(img, 19, 5, 26, 13, Bl)
    # Detergent bottle on top
    fill_rect(img, 22, 1, 26, 7, O)
    fill_rect(img, 23, 2, 25, 6, Gr)

    # Basket Rim (y: 12 to 15, x: 2 to 30)
    fill_rect(img, 2, 12, 30, 16, O)
    fill_rect(img, 3, 13, 29, 15, B)

    # Basket Body (y: 15 to 30, x: 3 to 29)
    fill_rect(img, 3, 15, 29, 30, O)
    fill_rect(img, 4, 16, 28, 29, B)

    # Woven wicker pattern
    for y in range(16, 29):
        for x in range(5, 27):
            if (x + y) % 3 == 0 or (x - y) % 4 == 0:
                img.putpixel((x, y), Bd)
    return img

# 2. Mop Bucket (Janitor Commercial Bucket - Large & Full)
def spr_trap_mopbucket():
    img = new_img()
    Y = px("facc15")    # Bright Yellow
    Yd = px("ca8a04")   # Dark Yellow
    Yh = px("fef08a")   # Light Yellow
    M = px("64748b")    # Metal handle / wringer
    Md = px("334155")
    stick = px("d97706")# Mop handle
    foam = px("f8fafc") # Suds/foam

    # Mop & Wringer Top (y: 2 to 14, x: 6 to 26)
    fill_rect(img, 14, 1, 18, 16, O)
    fill_rect(img, 15, 2, 17, 15, stick)
    fill_rect(img, 8, 3, 24, 9, O)
    fill_rect(img, 9, 4, 23, 8, M)

    # Bucket Rim (y: 11 to 15, x: 2 to 30)
    fill_rect(img, 2, 11, 30, 15, O)
    fill_rect(img, 3, 12, 29, 14, Yh)

    # Suds overflowing
    fill_rect(img, 6, 10, 12, 13, foam)
    fill_rect(img, 20, 10, 26, 13, foam)

    # Bucket Body (y: 14 to 28, x: 3 to 29)
    fill_rect(img, 3, 14, 29, 28, O)
    fill_rect(img, 4, 15, 28, 27, Y)
    fill_rect(img, 4, 22, 28, 27, Yd)

    # Janitor Caution symbol on bucket
    fill_rect(img, 13, 17, 19, 23, O)
    fill_rect(img, 14, 18, 18, 22, Yd)

    # Castor Wheels (y: 27 to 30, x: 4 to 10 and 22 to 28)
    fill_rect(img, 4, 27, 10, 31, O)
    fill_rect(img, 5, 28, 9, 30, Md)
    fill_rect(img, 22, 27, 28, 31, O)
    fill_rect(img, 23, 28, 27, 30, Md)
    return img

# 3. Fire Extinguisher (Large Unit with Wall Mount & Base)
def spr_trap_extinguisher():
    img = new_img()
    R = px("ef4444")    # Red
    Rd = px("991b1b")   # Dark Red
    Rh = px("fca5a5")   # Red highlight
    M = px("94a3b8")    # Metal / valve
    Md = px("334155")
    H = px("0f172a")    # Black hose

    # Valve & Gauge Top (y: 2 to 10, x: 7 to 25)
    fill_rect(img, 13, 2, 19, 7, O)
    fill_rect(img, 14, 3, 18, 6, M)
    fill_rect(img, 20, 3, 25, 7, O) # Gauge
    fill_rect(img, 21, 4, 24, 6, px("fef08a"))
    fill_rect(img, 7, 5, 14, 8, O) # Handle

    # Tank Body (y: 8 to 28, x: 5 to 27)
    fill_rect(img, 5, 8, 27, 28, O)
    fill_rect(img, 6, 9, 26, 27, R)
    fill_rect(img, 7, 10, 11, 25, Rh) # Highlight
    fill_rect(img, 21, 10, 25, 26, Rd) # Shadow

    # Instruction White Label
    fill_rect(img, 11, 14, 21, 22, px("f8fafc"))
    fill_rect(img, 13, 16, 19, 18, px("1e293b"))
    fill_rect(img, 13, 19, 19, 20, px("1e293b"))

    # Black Hose along side
    fill_rect(img, 3, 9, 6, 27, O)
    fill_rect(img, 4, 10, 5, 26, H)

    # Base Stand (y: 27 to 30, x: 4 to 28)
    fill_rect(img, 4, 27, 28, 31, O)
    fill_rect(img, 5, 28, 27, 30, Md)
    return img

# 4. Recycling Bin (Large Blue Bin)
def spr_trap_recycling():
    img = new_img()
    B = px("2563eb")    # Blue
    Bd = px("1e3a8a")   # Dark Blue
    Bh = px("93c5fd")   # Light Blue
    W = px("f8fafc")

    # Lid & Handle (y: 2 to 8, x: 2 to 30)
    fill_rect(img, 12, 2, 20, 5, O)
    fill_rect(img, 13, 3, 19, 4, Bh)
    fill_rect(img, 2, 5, 30, 9, O)
    fill_rect(img, 3, 6, 29, 8, Bh)

    # Bin Body (y: 8 to 28, x: 3 to 29)
    fill_rect(img, 3, 8, 29, 28, O)
    fill_rect(img, 4, 9, 28, 27, B)
    fill_rect(img, 4, 21, 28, 27, Bd)

    # Recycling Symbol in center
    fill_rect(img, 10, 13, 22, 21, W)
    fill_rect(img, 12, 15, 20, 19, B)

    # Wheels (y: 27 to 30)
    fill_rect(img, 4, 27, 9, 31, O)
    fill_rect(img, 23, 27, 28, 31, O)
    return img

# 5. Hallway Trash Bin (Large Stainless Can with Dome Lid)
def spr_trap_bin():
    img = new_img()
    M = px("94a3b8")
    Md = px("475569")
    Mh = px("e2e8f0")

    # Dome Top (y: 2 to 9, x: 4 to 28)
    fill_rect(img, 4, 2, 28, 9, O)
    fill_rect(img, 5, 3, 27, 8, Mh)
    fill_rect(img, 10, 5, 22, 8, O) # Flap slot

    # Can Body (y: 8 to 28, x: 3 to 29)
    fill_rect(img, 3, 8, 29, 28, O)
    fill_rect(img, 4, 9, 28, 27, M)
    fill_rect(img, 6, 10, 10, 26, Mh)
    fill_rect(img, 22, 10, 27, 26, Md)

    # Foot Pedal (y: 27 to 30)
    fill_rect(img, 11, 27, 21, 30, O)
    fill_rect(img, 12, 28, 20, 29, Mh)
    return img

# 6. Industrial Floor Fan (Large Metal Cage)
def spr_trap_floorfan():
    img = new_img()
    M = px("94a3b8")
    Md = px("334155")
    Mh = px("f1f5f9")
    Bl = px("0284c7")

    # Fan Base & Stand (y: 22 to 30, x: 2 to 30)
    fill_rect(img, 2, 27, 30, 31, O)
    fill_rect(img, 3, 28, 29, 30, Md)
    fill_rect(img, 14, 18, 18, 28, O)
    fill_rect(img, 15, 19, 17, 27, M)

    # Fan Cage Circle (y: 2 to 24, x: 2 to 30)
    for y in range(2, 24):
        for x in range(2, 30):
            dx = x - 16
            dy = y - 13
            d2 = dx * dx + dy * dy
            if 115 <= d2 <= 144:
                img.putpixel((x, y), O)
            elif d2 < 115:
                if (dx + dy) % 3 == 0:
                    img.putpixel((x, y), Mh)
                elif abs(dx) < 2 or abs(dy) < 2:
                    img.putpixel((x, y), Bl) # Spinning blade
                else:
                    img.putpixel((x, y), M)
    fill_rect(img, 14, 11, 18, 15, O)
    fill_rect(img, 15, 12, 17, 14, Mh)
    return img

# 7. Notice Board Post (Wide Wooden Cork Board with Papers)
def spr_trap_post():
    img = new_img()
    W = px("b45309")
    Wd = px("78350f")
    paper = px("fef3c7")
    red = px("ef4444")

    # Board (y: 2 to 20, x: 2 to 30)
    fill_rect(img, 2, 2, 30, 20, O)
    fill_rect(img, 3, 3, 29, 19, W)
    fill_rect(img, 5, 5, 27, 17, paper)
    # Pinned notice sheets
    fill_rect(img, 7, 7, 15, 15, px("ffffff"))
    fill_rect(img, 10, 6, 12, 8, red)
    fill_rect(img, 17, 7, 25, 15, px("fef08a"))
    fill_rect(img, 20, 6, 22, 8, red)

    # Stand Legs (y: 19 to 30, x: 4 to 9 and 23 to 28)
    fill_rect(img, 4, 19, 9, 31, O)
    fill_rect(img, 5, 20, 8, 30, Wd)
    fill_rect(img, 23, 19, 28, 31, O)
    fill_rect(img, 24, 20, 27, 30, Wd)
    return img

# 8. Traffic Bollard (Thick Heavy Metal with Reflective Stripes)
def spr_trap_bollard():
    img = new_img()
    Y = px("facc15")
    K = px("111827")
    M = px("475569")

    # Bollard Dome Top (y: 2 to 6, x: 6 to 26)
    fill_rect(img, 6, 2, 26, 7, O)
    fill_rect(img, 7, 3, 25, 6, Y)

    # Bollard Body (y: 6 to 28, x: 5 to 27)
    fill_rect(img, 5, 6, 27, 28, O)
    fill_rect(img, 6, 7, 26, 27, Y)
    # Black stripes
    fill_rect(img, 6, 10, 26, 15, K)
    fill_rect(img, 6, 19, 26, 24, K)

    # Heavy Base (y: 27 to 31, x: 2 to 30)
    fill_rect(img, 2, 27, 30, 31, O)
    fill_rect(img, 3, 28, 29, 30, M)
    return img

# 9. Roadworks Barrier (Wide Striped Safety Barrier)
def spr_trap_roadworks():
    img = new_img()
    R = px("dc2626")
    W = px("f8fafc")
    Y = px("facc15")
    M = px("57534e")

    # Flashing beacon light on top (y: 1 to 7, x: 12 to 20)
    fill_rect(img, 12, 1, 20, 7, O)
    fill_rect(img, 13, 2, 19, 6, Y)

    # Striped Board (y: 6 to 22, x: 1 to 31)
    fill_rect(img, 1, 6, 31, 22, O)
    for y in range(7, 21):
        for x in range(2, 30):
            img.putpixel((x, y), R if ((x + y) // 4) % 2 == 0 else W)

    # Sturdy A-frame Legs (y: 21 to 30, x: 2 to 9 and 23 to 30)
    fill_rect(img, 2, 21, 9, 31, O)
    fill_rect(img, 3, 22, 8, 30, M)
    fill_rect(img, 23, 21, 30, 31, O)
    fill_rect(img, 24, 22, 29, 30, M)
    return img

# 10. Wet Floor Caution Sign (Large A-Frame Cone)
def spr_trap_wetfloor():
    img = new_img()
    Y = px("facc15")
    Yd = px("ca8a04")
    K = px("111827")
    puddle = px("38bdf8")

    # Water puddle at base (y: 22 to 31, x: 1 to 31)
    fill_rect(img, 1, 24, 31, 31, O)
    fill_rect(img, 2, 25, 30, 30, puddle)

    # A-frame sign (y: 2 to 27, x: 4 to 28)
    fill_rect(img, 4, 2, 28, 27, O)
    fill_rect(img, 5, 3, 27, 26, Y)
    # Caution symbol / Slipping stickman
    fill_rect(img, 11, 8, 21, 18, K)
    fill_rect(img, 13, 10, 19, 16, Y)
    fill_rect(img, 8, 20, 24, 23, K)
    return img

# 11. Cable Ramp (Heavy Duty Yellow/Black Floor Ramp)
def spr_trap_cable():
    img = new_img()
    K = px("18181b")
    Y = px("eab308")

    # Full Width Ramp (y: 8 to 30, x: 1 to 31)
    fill_rect(img, 1, 8, 31, 30, O)
    for y in range(9, 29):
        for x in range(2, 30):
            img.putpixel((x, y), Y if (x // 4) % 2 == 0 else K)
    # Top cable channel
    fill_rect(img, 6, 12, 26, 16, O)
    fill_rect(img, 7, 13, 25, 15, px("3b82f6"))
    return img

# 12. Doorstep / Threshold Hazard
def spr_trap_doorstep():
    img = new_img()
    A = px("94a3b8")
    B = px("475569")
    Y = px("eab308")
    K = px("0f172a")

    fill_rect(img, 1, 8, 31, 30, O)
    fill_rect(img, 2, 9, 30, 29, A)
    fill_rect(img, 2, 18, 30, 29, B)
    # Warning chevron on front
    for y in range(10, 18):
        for x in range(3, 29):
            img.putpixel((x, y), Y if ((x + y) // 3) % 2 == 0 else K)
    return img

# 13. Stair Riser Spikes (Full Width Sharp Metal Spikes)
def spr_trap_riser():
    img = new_img()
    M = px("e2e8f0")
    D = px("334155")
    R = px("ef4444")

    # Base (y: 24 to 30, x: 1 to 31)
    fill_rect(img, 1, 24, 31, 30, O)
    fill_rect(img, 2, 25, 30, 29, D)

    # 4 Sharp Spikes (cx: 5, 12, 19, 26)
    for cx in (5, 12, 19, 26):
        for y in range(3, 26):
            half = max(1, (y - 3) // 4)
            for x in range(cx - half, cx + half + 1):
                if 0 <= x < 32:
                    img.putpixel((x, y), O if x in (cx - half, cx + half) else (M if x == cx else D))
        img.putpixel((cx, 3), R)
    return img

# 14. Balcony Flowerpot (Big Pot with Lush Green Plants & Flowers)
def spr_flowerpot():
    img = new_img()
    pot = px("c2410c")
    pot_d = px("7c2d12")
    pot_l = px("fb923c")
    leaf = px("22c55e")
    leaf_d = px("15803d")
    flower = px("f43f5e")
    yellow = px("facc15")

    # Lush leaves & flowers on top (y: 2 to 16, x: 2 to 30)
    for y in range(2, 16):
        for x in range(2, 30):
            dx = x - 16
            dy = y - 9
            if dx * dx + dy * dy * 1.6 <= 70:
                img.putpixel((x, y), O if dx * dx + dy * dy * 1.6 > 55 else (leaf if (x + y) % 2 == 0 else leaf_d))
    # Flowers
    fill_rect(img, 8, 4, 12, 8, flower)
    fill_rect(img, 9, 5, 11, 7, yellow)
    fill_rect(img, 20, 5, 24, 9, flower)
    fill_rect(img, 21, 6, 23, 8, yellow)

    # Pot Rim (y: 14 to 18, x: 3 to 29)
    fill_rect(img, 3, 14, 29, 18, O)
    fill_rect(img, 4, 15, 28, 17, pot_l)

    # Pot Body (y: 17 to 30, x: 5 to 27)
    for y in range(17, 30):
        inset = (y - 17) // 3
        x0, x1 = 5 + inset, 27 - inset
        fill_rect(img, x0, y, x1, y + 1, O)
        fill_rect(img, x0 + 1, y, x1 - 1, y + 1, pot if y < 25 else pot_d)
    return img

# 15. Standard Spikes (Trap Spike)
def spr_trap_spike():
    return spr_trap_riser()

def generate_all():
    sprites = {
        'spr_trap_laundry.png': spr_trap_laundry(),
        'spr_trap_mopbucket.png': spr_trap_mopbucket(),
        'spr_trap_extinguisher.png': spr_trap_extinguisher(),
        'spr_trap_recycling.png': spr_trap_recycling(),
        'spr_trap_bin.png': spr_trap_bin(),
        'spr_trap_post.png': spr_trap_post(),
        'spr_trap_floorfan.png': spr_trap_floorfan(),
        'spr_trap_riser.png': spr_trap_riser(),
        'spr_trap_wetfloor.png': spr_trap_wetfloor(),
        'spr_trap_hidden.png': spr_trap_wetfloor(),
        'spr_trap_cable.png': spr_trap_cable(),
        'spr_trap_roadworks.png': spr_trap_roadworks(),
        'spr_trap_bollard.png': spr_trap_bollard(),
        'spr_trap_doorstep.png': spr_trap_doorstep(),
        'spr_flowerpot.png': spr_flowerpot(),
        'spr_trap.png': spr_trap_laundry(),
        'spr_trap_spike.png': spr_trap_spike(),
        'trap_hazard.png': spr_trap_spike(),
    }

    dirs = [r'Assets/Art/Sprites', r'Assets/Resources/Sprites']
    for d in dirs:
        os.makedirs(d, exist_ok=True)
        for name, img in sprites.items():
            img.save(os.path.join(d, name))
            print(f"Saved full-sized {name} in {d}")

if __name__ == '__main__':
    generate_all()
