#!/usr/bin/env python3
"""
Generates 8-bit pixel art background for KOSEN KMITL campus.
Theme: 'Late to KOSEN' - Morning rush from dorms toward KOSEN KMITL campus buildings.
"""

import os
from PIL import Image, ImageDraw, ImageFont

def hex_to_rgba(h, a=255):
    h = h.lstrip('#')
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), a)

W, H = 640, 360
img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# --- 1. Morning Sky Gradient ---
# Sky colors from top (deep morning blue) to horizon (warm golden peach)
sky_top = hex_to_rgba('4a88e8')
sky_mid = hex_to_rgba('8ec5fc')
sky_horizon = hex_to_rgba('fed7aa')
sun_glow = hex_to_rgba('ffedd5')

for y in range(H):
    t = y / (H * 0.75)
    if t < 0.5:
        # top to mid
        factor = t / 0.5
        r = int(sky_top[0] + (sky_mid[0] - sky_top[0]) * factor)
        g = int(sky_top[1] + (sky_mid[1] - sky_top[1]) * factor)
        b = int(sky_top[2] + (sky_mid[2] - sky_top[2]) * factor)
    else:
        # mid to horizon
        factor = min(1.0, (t - 0.5) / 0.5)
        r = int(sky_mid[0] + (sky_horizon[0] - sky_mid[0]) * factor)
        g = int(sky_mid[1] + (sky_horizon[1] - sky_mid[1]) * factor)
        b = int(sky_mid[2] + (sky_horizon[2] - sky_mid[2]) * factor)
    draw.line([(0, y), (W, y)], fill=(r, g, b, 255))

# Morning Sun
sun_center = (520, 80)
sun_r = 36
for r in range(sun_r + 20, 0, -2):
    alpha = int(120 * (1 - (r / (sun_r + 20))))
    draw.ellipse([sun_center[0] - r, sun_center[1] - r, sun_center[0] + r, sun_center[1] + r],
                 fill=(255, 240, 200, alpha))
draw.ellipse([sun_center[0] - sun_r, sun_center[1] - sun_r, sun_center[0] + sun_r, sun_center[1] + sun_r],
             fill=(255, 255, 230, 255))

# --- 2. Fluffy 8-Bit Clouds ---
def draw_pixel_cloud(cx, cy, scale=1.0):
    cloud_col = hex_to_rgba('ffffff', 230)
    shadow_col = hex_to_rgba('e2e8f0', 210)
    bubbles = [
        (0, 0, int(35 * scale), int(20 * scale)),
        (int(-20 * scale), int(5 * scale), int(25 * scale), int(15 * scale)),
        (int(22 * scale), int(6 * scale), int(28 * scale), int(15 * scale)),
        (int(-35 * scale), int(10 * scale), int(20 * scale), int(12 * scale)),
        (int(40 * scale), int(10 * scale), int(22 * scale), int(12 * scale)),
    ]
    # Shadow underneath
    for bx, by, bw, bh in bubbles:
        draw.ellipse([cx + bx - bw, cy + by - bh + 4, cx + bx + bw, cy + by + bh + 4], fill=shadow_col)
    # Highlight
    for bx, by, bw, bh in bubbles:
        draw.ellipse([cx + bx - bw, cy + by - bh, cx + bx + bw, cy + by + bh], fill=cloud_col)

draw_pixel_cloud(90, 70, 0.9)
draw_pixel_cloud(280, 50, 1.2)
draw_pixel_cloud(440, 95, 0.7)
draw_pixel_cloud(590, 60, 0.8)

# --- 3. Distant KMITL & Lat Krabang Skyline (Silhouettes) ---
dist_col = hex_to_rgba('94a3b8', 190)
dist_win = hex_to_rgba('fef08a', 140)

distant_buildings = [
    (20, 160, 45, 120),
    (70, 140, 55, 140),
    (130, 180, 40, 100),
    (175, 150, 60, 130),
    (240, 130, 70, 150),
    (315, 170, 50, 110),
    (370, 145, 55, 135),
    (430, 135, 65, 145),
    (500, 160, 45, 120),
    (550, 140, 70, 140),
]
for x, y, w, h in distant_buildings:
    draw.rectangle([x, y, x + w, y + h], fill=dist_col)
    # Tiny distant windows
    for wy in range(y + 10, y + h - 10, 14):
        for wx in range(x + 6, x + w - 6, 10):
            draw.rectangle([wx, wy, wx + 4, wy + 6], fill=dist_win)

# Distant Communication / Transmission Tower (สจล. เสาสื่อสารโทรคมนาคม)
tw_x = 275
draw.line([(tw_x, 80), (tw_x - 15, 130)], fill=dist_col, width=2)
draw.line([(tw_x, 80), (tw_x + 15, 130)], fill=dist_col, width=2)
draw.line([(tw_x - 15, 130), (tw_x + 15, 130)], fill=dist_col, width=2)
draw.line([(tw_x - 8, 105), (tw_x + 8, 105)], fill=dist_col, width=2)
draw.line([(tw_x, 70), (tw_x, 80)], fill=hex_to_rgba('ef4444'), width=2) # Red beacon

# --- 4. Main Midground: KOSEN-KMITL Academic Buildings ---
wall_white = hex_to_rgba('f8fafc')
wall_shade = hex_to_rgba('cbd5e1')
wall_dark  = hex_to_rgba('94a3b8')
accent_kosen_orange = hex_to_rgba('ea580c') # KMITL / KOSEN Orange
accent_blue = hex_to_rgba('1e40af')
glass_blue  = hex_to_rgba('67e8f9')
glass_refl  = hex_to_rgba('cffafe')
roof_slate  = hex_to_rgba('334155')

# KOSEN Complex Left Wing (Dorm / Lab Building)
draw.rectangle([10, 190, 160, 310], fill=wall_white)
draw.rectangle([10, 185, 160, 190], fill=roof_slate)
draw.rectangle([10, 245, 160, 252], fill=accent_kosen_orange)
# Windows on Left Wing
for r in range(4):
    for c in range(6):
        wx = 20 + c * 22
        wy = 198 + r * 26
        if wy < 245 or wy > 255:
            draw.rectangle([wx, wy, wx + 14, wy + 16], fill=glass_blue)
            draw.line([(wx, wy + 16), (wx + 14, wy)], fill=glass_refl, width=1)

# Center-Right Main Complex: KOSEN KMITL Engineering Building
draw.rectangle([180, 160, 480, 320], fill=wall_white)
draw.rectangle([180, 153, 480, 160], fill=roof_slate)

# Orange Accent Façade & Pillars (KOSEN Branding)
draw.rectangle([180, 160, 210, 320], fill=wall_shade)
draw.rectangle([210, 160, 230, 320], fill=accent_kosen_orange)
draw.rectangle([430, 160, 450, 320], fill=accent_kosen_orange)
draw.rectangle([450, 160, 480, 320], fill=wall_shade)

# Central Clock Tower / Logo Section
draw.rectangle([280, 130, 380, 320], fill=hex_to_rgba('f1f5f9'))
draw.rectangle([280, 122, 380, 130], fill=accent_kosen_orange)
# Clock
clock_c = (330, 148)
draw.ellipse([clock_c[0] - 12, clock_c[1] - 12, clock_c[0] + 12, clock_c[1] + 12], fill=hex_to_rgba('ffffff'), outline=roof_slate, width=2)
# Clock hands pointing to 8:25 (Almost late!)
draw.line([clock_c, (clock_c[0] + 6, clock_c[1] + 3)], fill=roof_slate, width=2)
draw.line([clock_c, (clock_c[0] - 4, clock_c[1] - 8)], fill=hex_to_rgba('dc2626'), width=2)

# Large "KOSEN" Pixel Lettering Signboard
sign_bg = hex_to_rgba('1e293b')
draw.rectangle([250, 175, 410, 198], fill=sign_bg)
draw.rectangle([248, 173, 412, 175], fill=accent_kosen_orange)
draw.rectangle([248, 198, 412, 200], fill=accent_kosen_orange)

# Draw Pixel Text "KOSEN - KMITL"
# Simple pixel font rendering for "K O S E N   K M I T L"
def draw_pixel_letter(char, start_x, start_y, color):
    font_map = {
        'K': ["#  #", "##  ", "# # ", "#  #", "#  #"],
        'O': [" ## ", "#  #", "#  #", "#  #", " ## "],
        'S': [" ###", "#   ", " ## ", "   #", "### "],
        'E': ["####", "#   ", "### ", "#   ", "####"],
        'N': ["#  #", "## #", "# ##", "#  #", "#  #"],
        '-': ["    ", "    ", "####", "    ", "    "],
        'M': ["#  #", "####", "#  #", "#  #", "#  #"],
        'I': ["###", " # ", " # ", " # ", "###"],
        'T': ["###", " # ", " # ", " # ", " # "],
        'L': ["#   ", "#   ", "#   ", "#   ", "####"],
    }
    matrix = font_map.get(char, ["    "] * 5)
    for r, row in enumerate(matrix):
        for c, ch in enumerate(row):
            if ch == '#':
                draw.rectangle([start_x + c * 2, start_y + r * 2, start_x + c * 2 + 1, start_y + r * 2 + 1], fill=color)

title_text = "KOSEN-KMITL"
px = 260
py = 182
text_col = hex_to_rgba('ffffff')
for ch in title_text:
    draw_pixel_letter(ch, px, py, text_col if ch != '-' else accent_kosen_orange)
    px += 13 if ch not in ('I', 'T', '-') else 9

# Engineering Laboratory Glass Grid Façade
for r in range(4):
    for c in range(10):
        gx = 236 + c * 19
        gy = 208 + r * 24
        if not (280 <= gx <= 370 and r == 0):
            draw.rectangle([gx, gy, gx + 15, gy + 18], fill=glass_blue)
            draw.line([(gx, gy + 18), (gx + 15, gy)], fill=glass_refl, width=1)
            draw.rectangle([gx, gy, gx + 15, gy + 18], outline=wall_shade, width=1)

# Main Entrance Glass Doors (KOSEN Hall)
draw.rectangle([295, 275, 365, 320], fill=hex_to_rgba('0f172a'))
draw.rectangle([300, 280, 328, 320], fill=glass_blue, outline=wall_white, width=1)
draw.rectangle([332, 280, 360, 320], fill=glass_blue, outline=wall_white, width=1)

# Right Wing (Research Wing)
draw.rectangle([500, 180, 630, 310], fill=wall_white)
draw.rectangle([500, 175, 630, 180], fill=roof_slate)
draw.rectangle([500, 235, 630, 242], fill=accent_kosen_orange)
for r in range(4):
    for c in range(5):
        wx = 510 + c * 22
        wy = 188 + r * 26
        if wy < 235 or wy > 245:
            draw.rectangle([wx, wy, wx + 14, wy + 16], fill=glass_blue)
            draw.line([(wx, wy + 16), (wx + 14, wy)], fill=glass_refl, width=1)

# --- 5. Foreground Campus Greenery, Trees & Lamp Posts ---
tree_dark  = hex_to_rgba('14532d')
tree_mid   = hex_to_rgba('16a34a')
tree_light = hex_to_rgba('4ade80')
trunk_col  = hex_to_rgba('78350f')

def draw_pixel_tree(tx, ty, scale=1.0):
    tw = int(24 * scale)
    th = int(45 * scale)
    # Trunk
    draw.rectangle([tx - int(3 * scale), ty, tx + int(3 * scale), ty + th], fill=trunk_col)
    # Leaves clusters
    draw.ellipse([tx - tw, ty - th + 5, tx + tw, ty + 10], fill=tree_dark)
    draw.ellipse([tx - tw + 3, ty - th + 2, tx + tw - 3, ty + 5], fill=tree_mid)
    draw.ellipse([tx - int(tw * 0.6), ty - th, tx + int(tw * 0.4), ty - int(th * 0.4)], fill=tree_light)

# Trees along the walkway
draw_pixel_tree(170, 260, 1.1)
draw_pixel_tree(490, 260, 1.2)
draw_pixel_tree(5, 270, 0.9)
draw_pixel_tree(635, 270, 0.9)

# Campus Modern Streetlamp
def draw_lamp(lx, ly):
    lamp_col = hex_to_rgba('334155')
    light_glow = hex_to_rgba('fef08a', 200)
    draw.rectangle([lx, ly, lx + 2, ly + 65], fill=lamp_col)
    draw.rectangle([lx - 6, ly, lx + 8, ly + 3], fill=lamp_col)
    draw.rectangle([lx - 4, ly + 3, lx + 6, ly + 7], fill=light_glow)

draw_lamp(150, 245)
draw_lamp(470, 245)

# --- 6. Campus Pathway / Green lawn at base ---
draw.rectangle([0, 310, W, H], fill=hex_to_rgba('15803d')) # Lawn
draw.rectangle([0, 320, W, H], fill=hex_to_rgba('166534'))
draw.rectangle([0, 335, W, H], fill=hex_to_rgba('475569')) # Pavement
draw.rectangle([0, 340, W, H], fill=hex_to_rgba('334155'))

# Save Output
out_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Assets', 'Art', 'Sprites', 'background_kosen.png')
img.save(out_path)
print(f'Generated KOSEN KMITL background: {out_path} ({W}x{H})')
