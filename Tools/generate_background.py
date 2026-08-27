#!/usr/bin/env python3
"""
Generates 8-bit pixel art background for KOSEN KMITL campus.
Widescreen (800x450), softer pastel tones to avoid visual clutter with gameplay elements.
"""

import os
from PIL import Image, ImageDraw

def hex_to_rgba(h, a=255):
    h = h.lstrip('#')
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), a)

W, H = 800, 450
img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# --- 1. Soft Morning Sky Gradient ---
sky_top = hex_to_rgba('6ba3eb')
sky_mid = hex_to_rgba('a8d4ff')
sky_horizon = hex_to_rgba('ffedd5')

for y in range(H):
    t = y / (H * 0.78)
    if t < 0.5:
        factor = t / 0.5
        r = int(sky_top[0] + (sky_mid[0] - sky_top[0]) * factor)
        g = int(sky_top[1] + (sky_mid[1] - sky_top[1]) * factor)
        b = int(sky_top[2] + (sky_mid[2] - sky_top[2]) * factor)
    else:
        factor = min(1.0, (t - 0.5) / 0.5)
        r = int(sky_mid[0] + (sky_horizon[0] - sky_mid[0]) * factor)
        g = int(sky_mid[1] + (sky_horizon[1] - sky_mid[1]) * factor)
        b = int(sky_mid[2] + (sky_horizon[2] - sky_mid[2]) * factor)
    draw.line([(0, y), (W, y)], fill=(r, g, b, 255))

# Soft Morning Sun
sun_center = (650, 100)
sun_r = 45
for r in range(sun_r + 30, 0, -3):
    alpha = int(90 * (1 - (r / (sun_r + 30))))
    draw.ellipse([sun_center[0] - r, sun_center[1] - r, sun_center[0] + r, sun_center[1] + r],
                 fill=(255, 245, 210, alpha))
draw.ellipse([sun_center[0] - sun_r, sun_center[1] - sun_r, sun_center[0] + sun_r, sun_center[1] + sun_r],
             fill=(255, 255, 235, 230))

# --- 2. Fluffy 8-Bit Clouds ---
def draw_pixel_cloud(cx, cy, scale=1.0):
    cloud_col = hex_to_rgba('ffffff', 220)
    shadow_col = hex_to_rgba('e2e8f0', 180)
    bubbles = [
        (0, 0, int(45 * scale), int(25 * scale)),
        (int(-28 * scale), int(6 * scale), int(32 * scale), int(18 * scale)),
        (int(30 * scale), int(7 * scale), int(35 * scale), int(18 * scale)),
        (int(-48 * scale), int(12 * scale), int(25 * scale), int(15 * scale)),
        (int(52 * scale), int(12 * scale), int(28 * scale), int(15 * scale)),
    ]
    for bx, by, bw, bh in bubbles:
        draw.ellipse([cx + bx - bw, cy + by - bh + 5, cx + bx + bw, cy + by + bh + 5], fill=shadow_col)
    for bx, by, bw, bh in bubbles:
        draw.ellipse([cx + bx - bw, cy + by - bh, cx + bx + bw, cy + by + bh], fill=cloud_col)

draw_pixel_cloud(110, 80, 0.9)
draw_pixel_cloud(340, 60, 1.3)
draw_pixel_cloud(560, 110, 0.8)
draw_pixel_cloud(740, 75, 0.9)

# --- 3. Distant KMITL & Lat Krabang Skyline ---
dist_col = hex_to_rgba('a0aec0', 170)
dist_win = hex_to_rgba('fef9c3', 130)

distant_buildings = [
    (15, 200, 60, 150),
    (80, 175, 70, 175),
    (155, 220, 50, 130),
    (210, 190, 75, 160),
    (290, 165, 85, 185),
    (385, 210, 65, 140),
    (460, 180, 70, 170),
    (540, 170, 80, 180),
    (630, 200, 60, 150),
    (700, 175, 85, 175),
]
for x, y, w, h in distant_buildings:
    draw.rectangle([x, y, x + w, y + h], fill=dist_col)
    for wy in range(y + 12, y + h - 12, 16):
        for wx in range(x + 8, x + w - 8, 12):
            draw.rectangle([wx, wy, wx + 5, wy + 7], fill=dist_win)

# Distant Communication Tower (KMITL Beacon)
tw_x = 345
draw.line([(tw_x, 100), (tw_x - 18, 165)], fill=dist_col, width=2)
draw.line([(tw_x, 100), (tw_x + 18, 165)], fill=dist_col, width=2)
draw.line([(tw_x - 18, 165), (tw_x + 18, 165)], fill=dist_col, width=2)
draw.line([(tw_x - 10, 135), (tw_x + 10, 135)], fill=dist_col, width=2)
draw.line([(tw_x, 88), (tw_x, 100)], fill=hex_to_rgba('f87171'), width=2)

# --- 4. Main Midground: KOSEN-KMITL Academic Buildings ---
wall_white = hex_to_rgba('f1f5f9', 240)
wall_shade = hex_to_rgba('cbd5e1', 240)
accent_kosen_orange = hex_to_rgba('fb923c', 240) # Softer KMITL Orange
glass_blue  = hex_to_rgba('7dd3fc', 220)
glass_refl  = hex_to_rgba('e0f2fe', 220)
roof_slate  = hex_to_rgba('475569', 240)

# Left Wing (Laboratories)
draw.rectangle([20, 240, 200, 390], fill=wall_white)
draw.rectangle([20, 233, 200, 240], fill=roof_slate)
draw.rectangle([20, 305, 200, 314], fill=accent_kosen_orange)
for r in range(4):
    for c in range(7):
        wx = 32 + c * 24
        wy = 250 + r * 32
        if wy < 305 or wy > 318:
            draw.rectangle([wx, wy, wx + 16, wy + 20], fill=glass_blue)
            draw.line([(wx, wy + 20), (wx + 16, wy)], fill=glass_refl, width=1)

# Center Main Complex (KOSEN Building)
draw.rectangle([225, 200, 580, 400], fill=wall_white)
draw.rectangle([225, 192, 580, 200], fill=roof_slate)

# Orange Pillars
draw.rectangle([225, 200, 260, 400], fill=wall_shade)
draw.rectangle([260, 200, 285, 400], fill=accent_kosen_orange)
draw.rectangle([520, 200, 545, 400], fill=accent_kosen_orange)
draw.rectangle([545, 200, 580, 400], fill=wall_shade)

# Clock Tower
draw.rectangle([345, 160, 460, 400], fill=hex_to_rgba('e2e8f0', 240))
draw.rectangle([345, 150, 460, 160], fill=accent_kosen_orange)
clock_c = (402, 178)
draw.ellipse([clock_c[0] - 15, clock_c[1] - 15, clock_c[0] + 15, clock_c[1] + 15], fill=hex_to_rgba('ffffff'), outline=roof_slate, width=2)
draw.line([clock_c, (clock_c[0] + 7, clock_c[1] + 4)], fill=roof_slate, width=2)
draw.line([clock_c, (clock_c[0] - 5, clock_c[1] - 10)], fill=hex_to_rgba('ef4444'), width=2)

# Signboard: KOSEN - KMITL
sign_bg = hex_to_rgba('334155', 240)
draw.rectangle([310, 218, 495, 246], fill=sign_bg)
draw.rectangle([308, 215, 497, 218], fill=accent_kosen_orange)
draw.rectangle([308, 246, 497, 249], fill=accent_kosen_orange)

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
px = 325
py = 227
text_col = hex_to_rgba('ffffff')
for ch in title_text:
    draw_pixel_letter(ch, px, py, text_col if ch != '-' else accent_kosen_orange)
    px += 15 if ch not in ('I', 'T', '-') else 11

# Glass grid façade
for r in range(4):
    for c in range(12):
        gx = 295 + c * 23
        gy = 258 + r * 30
        if not (345 <= gx <= 445 and r == 0):
            draw.rectangle([gx, gy, gx + 18, gy + 22], fill=glass_blue)
            draw.line([(gx, gy + 22), (gx + 18, gy)], fill=glass_refl, width=1)
            draw.rectangle([gx, gy, gx + 18, gy + 22], outline=wall_shade, width=1)

# Main Entrance Glass Doors
draw.rectangle([365, 345, 440, 400], fill=hex_to_rgba('1e293b'))
draw.rectangle([370, 350, 400, 400], fill=glass_blue, outline=wall_white, width=1)
draw.rectangle([405, 350, 435, 400], fill=glass_blue, outline=wall_white, width=1)

# Right Wing
draw.rectangle([600, 230, 780, 390], fill=wall_white)
draw.rectangle([600, 223, 780, 230], fill=roof_slate)
draw.rectangle([600, 295, 780, 304], fill=accent_kosen_orange)
for r in range(4):
    for c in range(6):
        wx = 612 + c * 25
        wy = 240 + r * 32
        if wy < 295 or wy > 308:
            draw.rectangle([wx, wy, wx + 17, wy + 20], fill=glass_blue)
            draw.line([(wx, wy + 20), (wx + 17, wy)], fill=glass_refl, width=1)

# --- 5. Campus Trees & Greenery ---
tree_dark  = hex_to_rgba('15803d', 220)
tree_mid   = hex_to_rgba('22c55e', 220)
tree_light = hex_to_rgba('86efac', 220)
trunk_col  = hex_to_rgba('854d0e', 220)

def draw_pixel_tree(tx, ty, scale=1.0):
    tw = int(30 * scale)
    th = int(55 * scale)
    draw.rectangle([tx - int(4 * scale), ty, tx + int(4 * scale), ty + th], fill=trunk_col)
    draw.ellipse([tx - tw, ty - th + 6, tx + tw, ty + 12], fill=tree_dark)
    draw.ellipse([tx - tw + 4, ty - th + 3, tx + tw - 4, ty + 6], fill=tree_mid)
    draw.ellipse([tx - int(tw * 0.6), ty - th, tx + int(tw * 0.4), ty - int(th * 0.4)], fill=tree_light)

draw_pixel_tree(210, 325, 1.1)
draw_pixel_tree(590, 325, 1.2)
draw_pixel_tree(10, 335, 0.9)
draw_pixel_tree(790, 335, 0.9)

# Campus Streetlamps
def draw_lamp(lx, ly):
    lamp_col = hex_to_rgba('475569')
    light_glow = hex_to_rgba('fef08a', 180)
    draw.rectangle([lx, ly, lx + 3, ly + 80], fill=lamp_col)
    draw.rectangle([lx - 8, ly, lx + 11, ly + 4], fill=lamp_col)
    draw.rectangle([lx - 5, ly + 4, lx + 8, ly + 9], fill=light_glow)

draw_lamp(190, 305)
draw_lamp(565, 305)

# --- 6. Lawn & Ground at base ---
draw.rectangle([0, 390, W, H], fill=hex_to_rgba('16a34a', 220))
draw.rectangle([0, 405, W, H], fill=hex_to_rgba('15803d', 220))
draw.rectangle([0, 420, W, H], fill=hex_to_rgba('64748b', 220))
draw.rectangle([0, 430, W, H], fill=hex_to_rgba('475569', 220))

out_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Assets', 'Art', 'Sprites', 'background_kosen.png')
img.save(out_path)
print(f'Generated soft widescreen KOSEN background: {out_path} ({W}x{H})')
