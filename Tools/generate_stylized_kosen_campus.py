#!/usr/bin/env python3
"""
Generates an original, fully hand-crafted 800x450 16:9 retro pixel art
masterpiece of the KOSEN-KMITL Campus & Building:
- Seamless vibrant morning sky gradient with fluffy pixel clouds
- Distant university campus skyline silhouettes
- Stylized modern angular KOSEN engineering building with glass diamond windows & roof terrace
- Lush green pixel trees, bushes, and campus landscaping
- Paved plaza, asphalt road with red-white curbs, and street lamps
- Prominent KOSEN KMITL landmark sign in foreground
"""

import os
import math
from PIL import Image

def px(h):
    h = h.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), 255)

def fill_rect(img, x0, y0, x1, y1, c):
    for y in range(max(0, int(y0)), min(450, int(y1))):
        for x in range(max(0, int(x0)), min(800, int(x1))):
            img.putpixel((x, y), c)

def draw_polygon(img, points, c):
    # Simple rasterizer for convex polygons
    min_y = max(0, min(p[1] for p in points))
    max_y = min(449, max(p[1] for p in points))
    n = len(points)
    for y in range(min_y, max_y + 1):
        nodes = []
        for i in range(n):
            j = (i + 1) % n
            y1, y2 = points[i][1], points[j][1]
            x1, x2 = points[i][0], points[j][0]
            if (y1 <= y < y2) or (y2 <= y < y1):
                if y2 != y1:
                    x = x1 + (y - y1) * (x2 - x1) / float(y2 - y1)
                    nodes.append(x)
        nodes.sort()
        for k in range(0, len(nodes) - 1, 2):
            x_start = max(0, int(nodes[k]))
            x_end = min(799, int(nodes[k+1]))
            for x in range(x_start, x_end + 1):
                img.putpixel((x, y), c)

def make_stylized_kosen_bg():
    w, h = 800, 450
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))

    # --- COLOR PALETTE ---
    # Sky
    Sky_top = px("1e3a8a")     # Deep blue
    Sky_mid = px("3b82f6")     # Vivid blue
    Sky_low = px("93c5fd")     # Soft cyan
    Sky_hor = px("e0f2fe")     # Horizon glow
    Cloud_w = px("ffffff")
    Cloud_s = px("bfdbfe")
    Cloud_d = px("93c5fd")

    # Distant Campus Skyline
    Distant_bldg = px("7dd3fc")
    Distant_roof = px("60a5fa")

    # KOSEN Building (Modern Slate, Steel & Diamond Glass)
    B_dark = px("0f172a")      # Dark structure
    B_frame = px("1e293b")     # Main steel frame
    B_metal = px("334155")     # Brushed slate metal
    B_light = px("64748b")     # Metal highlight
    B_white = px("e2e8f0")     # White wall panels
    B_terrace = px("d97706")   # Wood louvers / orange terrace accent
    
    # Glass & Reflections
    G_deep = px("0369a1")      # Deep blue glass
    G_mid = px("0284c7")       # Window cyan
    G_light = px("38bdf8")     # Glass reflection
    G_shine = px("e0f2fe")     # Pure reflection white-cyan
    G_spec = px("ffffff")

    # Trees & Foliage
    T_dark = px("14532d")
    T_mid = px("15803d")
    T_light = px("22c55e")
    T_bright = px("86efac")
    T_trunk = px("78350f")

    # Ground, Plaza & Road
    P_plaza = px("cbd5e1")     # Concrete plaza
    P_plaza_d = px("94a3b8")
    R_asphalt = px("334155")   # Asphalt road
    R_curb_r = px("ef4444")    # Red curb
    R_curb_w = px("f8fafc")    # White curb
    R_line = px("facc15")      # Yellow lane line

    # Monument Sign
    S_black = px("0f172a")
    S_blue = px("38bdf8")
    S_orange = px("f97316")

    # =========================================================================
    # 1. SKY GRADIENT (y: 0 to 360)
    # =========================================================================
    for y in range(360):
        t = y / 360.0
        if t < 0.35:
            k = t / 0.35
            r = int(Sky_top[0]*(1-k) + Sky_mid[0]*k)
            g = int(Sky_top[1]*(1-k) + Sky_mid[1]*k)
            b = int(Sky_top[2]*(1-k) + Sky_mid[2]*k)
        elif t < 0.75:
            k = (t - 0.35) / 0.40
            r = int(Sky_mid[0]*(1-k) + Sky_low[0]*k)
            g = int(Sky_mid[1]*(1-k) + Sky_low[1]*k)
            b = int(Sky_mid[2]*(1-k) + Sky_low[2]*k)
        else:
            k = (t - 0.75) / 0.25
            r = int(Sky_low[0]*(1-k) + Sky_hor[0]*k)
            g = int(Sky_low[1]*(1-k) + Sky_hor[1]*k)
            b = int(Sky_low[2]*(1-k) + Sky_hor[2]*k)
        for x in range(w):
            im.putpixel((x, y), (r, g, b, 255))

    # Fluffy Pixel Clouds
    clouds = [
        (80, 50, 45), (150, 60, 35), (40, 70, 30),
        (280, 40, 50), (350, 55, 40),
        (680, 70, 45), (740, 60, 35)
    ]
    for cx, cy, cr in clouds:
        for y in range(cy - cr, cy + cr + 1):
            for x in range(cx - cr*2, cx + cr*2 + 1):
                if 0 <= x < w and 0 <= y < 360:
                    d2 = ((x - cx) / 1.8)**2 + (y - cy)**2
                    if d2 <= cr*cr:
                        if y > cy + cr*0.4:
                            c = Cloud_d
                        elif y > cy:
                            c = Cloud_s
                        else:
                            c = Cloud_w
                        im.putpixel((x, y), c)

    # =========================================================================
    # 2. DISTANT CAMPUS BUILDINGS SILHOUETTE (y: 240 to 360)
    # =========================================================================
    # Left campus skyline
    fill_rect(im, 0, 260, 70, 360, Distant_bldg)
    fill_rect(im, 70, 280, 130, 360, Distant_roof)
    fill_rect(im, 130, 250, 200, 360, Distant_bldg)
    fill_rect(im, 200, 275, 270, 360, Distant_roof)
    # Tiny windows on distant buildings
    for by in range(265, 340, 12):
        for bx in range(10, 250, 14):
            if (bx + by) % 5 == 0:
                fill_rect(im, bx, by, bx + 6, by + 6, px("e0f2fe"))

    # =========================================================================
    # 3. ICONIC KOSEN-KMITL BUILDING (Angular Modern Architecture)
    # =========================================================================
    # Building Base Coordinates: (X: 300 to 760, Y: 40 to 370)
    
    # Left Sloping Wing (Angular Structural Truss)
    poly_left_wing = [(300, 370), (370, 70), (450, 40), (470, 370)]
    draw_polygon(im, poly_left_wing, B_metal)

    # Main Center-Right Glass Tower Body
    poly_tower = [(440, 40), (680, 100), (740, 370), (440, 370)]
    draw_polygon(im, poly_tower, B_dark)

    # Sloping Overhang Roof / Top Fin
    poly_roof_fin = [(350, 75), (450, 30), (690, 95), (660, 115), (440, 55), (370, 90)]
    draw_polygon(im, poly_roof_fin, B_frame)
    poly_roof_rim = [(450, 30), (690, 95), (690, 100), (450, 35)]
    draw_polygon(im, poly_roof_rim, B_light)

    # Large Diamond Glass Facade on Left Wing (y: 110 to 340, x: 340 to 450)
    for row in range(5):
        y_top = 110 + row * 45
        y_bot = y_top + 40
        for col in range(3):
            x_left = 340 + col * 35 + row * 8
            x_right = x_left + 30
            poly_glass = [
                (x_left + 15, y_top),
                (x_right, y_top + 20),
                (x_left + 15, y_bot),
                (x_left, y_top + 20)
            ]
            draw_polygon(im, poly_glass, G_mid)
            # Diagonal shine on glass
            poly_shine = [
                (x_left + 15, y_top),
                (x_left + 22, y_top + 10),
                (x_left + 8, y_bot - 10),
                (x_left, y_top + 20)
            ]
            draw_polygon(im, poly_shine, G_light)

    # Right Tower Glass Grid & Louvers (x: 470 to 710, y: 80 to 360)
    for floor in range(7):
        fy = 110 + floor * 36
        fill_rect(im, 480, fy, 700, fy + 4, B_light)
        # Vertical windows per floor
        for wx in range(490, 690, 35):
            fill_rect(im, wx, fy + 4, wx + 28, fy + 32, G_deep)
            fill_rect(im, wx + 2, fy + 6, wx + 26, fy + 30, G_mid)
            fill_rect(im, wx + 4, fy + 8, wx + 14, fy + 28, G_light) # Glass shine
            # Orange vertical wood accent panel on right side of windows
            fill_rect(im, wx + 24, fy + 4, wx + 28, fy + 32, B_terrace)

    # Left Ground Entrance Canopy & Giant Slanted Steel Pillars (x: 280 to 450, y: 280 to 370)
    poly_canopy = [(260, 300), (440, 290), (450, 310), (270, 320)]
    draw_polygon(im, poly_canopy, B_frame)
    fill_rect(im, 270, 318, 440, 322, B_terrace) # Warm wood underside

    # Giant V-shaped Slanted Support Columns
    poly_col1 = [(290, 315), (320, 315), (280, 370), (265, 370)]
    draw_polygon(im, poly_col1, B_frame)
    poly_col2 = [(350, 310), (375, 310), (350, 370), (335, 370)]
    draw_polygon(im, poly_col2, B_metal)
    poly_col3 = [(410, 305), (435, 305), (430, 370), (415, 370)]
    draw_polygon(im, poly_col3, B_frame)

    # Entrance Lobby Glass behind columns (Glowing warm indoor light)
    fill_rect(im, 310, 325, 430, 370, px("fef08a")) # Golden indoor light
    fill_rect(im, 315, 330, 425, 365, px("fef9c3"))
    fill_rect(im, 360, 340, 390, 370, px("0f172a")) # Automatic sliding door

    # Thai Flagpole on Building Roof (x: 520, y: 15 to 75)
    fill_rect(im, 520, 15, 522, 75, px("f8fafc")) # White pole
    # Waving Thai Flag (Red-White-Blue-White-Red stripes)
    flag_y = 20
    for fx in range(522, 570):
        wave = int(math.sin((fx - 522) * 0.2) * 3)
        y0 = flag_y + wave
        fill_rect(im, fx, y0, fx + 1, y0 + 4, px("dc2626"))      # Red
        fill_rect(im, fx, y0 + 4, fx + 1, y0 + 7, px("ffffff"))  # White
        fill_rect(im, fx, y0 + 7, fx + 1, y0 + 15, px("1e3a8a")) # Double Blue
        fill_rect(im, fx, y0 + 15, fx + 1, y0 + 18, px("ffffff")) # White
        fill_rect(im, fx, y0 + 18, fx + 1, y0 + 22, px("dc2626")) # Red

    # =========================================================================
    # 4. LUSH CAMPUS TREES & GARDENS (Left & Surrounding)
    # =========================================================================
    def draw_pixel_tree(base_x, base_y, radius):
        # Trunk
        fill_rect(im, base_x - 4, base_y - radius, base_x + 4, base_y, T_trunk)
        # Foliage blobs
        for y in range(base_y - radius * 2, base_y - int(radius * 0.4)):
            for x in range(base_x - radius, base_x + radius + 1):
                if 0 <= x < w and 0 <= y < h:
                    d2 = (x - base_x)**2 + (y - (base_y - radius*1.2))**2
                    if d2 <= radius*radius:
                        if y > base_y - radius*0.8:
                            c = T_dark
                        elif x > base_x + radius*0.2:
                            c = T_mid
                        elif y < base_y - radius*1.5:
                            c = T_bright
                        else:
                            c = T_light
                        im.putpixel((x, y), c)

    # Tree line on left side
    draw_pixel_tree(50, 360, 36)
    draw_pixel_tree(110, 355, 42)
    draw_pixel_tree(175, 360, 38)
    draw_pixel_tree(230, 365, 32)
    draw_pixel_tree(760, 365, 34) # Right edge tree

    # Green Hedges & Flowerbeds along the walkway
    fill_rect(im, 0, 355, 260, 375, T_mid)
    fill_rect(im, 0, 353, 260, 358, T_light)
    # Red & yellow flowers in hedge
    for fx in range(10, 250, 18):
        im.putpixel((fx, 354), px("f43f5e"))
        im.putpixel((fx + 6, 356), px("facc15"))

    # Campus Street Lamps (Retro Victorian/Modern Pole)
    for lx in [140, 260]:
        fill_rect(im, lx, 300, lx + 3, 365, px("1e293b"))
        fill_rect(im, lx - 4, 296, lx + 7, 302, px("0f172a"))
        fill_rect(im, lx - 2, 298, lx + 5, 304, px("fef08a")) # Glowing yellow bulb

    # =========================================================================
    # 5. FOREGROUND CAMPUS PLAZA, ROAD & CURBS (y: 365 to 450)
    # =========================================================================
    # Concrete Plaza
    fill_rect(im, 0, 365, w, 395, P_plaza)
    for y in range(365, 395, 10):
        fill_rect(im, 0, y, w, y + 1, P_plaza_d)

    # Asphalt Road
    fill_rect(im, 0, 395, w, 450, R_asphalt)
    # Yellow Dashed Center Line
    for x in range(0, w, 40):
        fill_rect(im, x, 420, x + 24, 423, R_line)

    # Red & White Checked Curb (y: 391 to 396)
    for x in range(0, w, 30):
        c_curb = R_curb_r if (x // 30) % 2 == 0 else R_curb_w
        fill_rect(im, x, 391, min(w, x + 30), 396, c_curb)
        fill_rect(im, x, 395, min(w, x + 30), 396, px("0f172a")) # Bottom shadow

    # =========================================================================
    # 6. ICONIC KOSEN KMITL MONUMENT SIGN (Foreground Right: x: 480 to 730, y: 340 to 395)
    # =========================================================================
    # Sign Base / Podium
    poly_sign = [(470, 392), (730, 392), (720, 342), (480, 342)]
    draw_polygon(im, poly_sign, S_black)
    fill_rect(im, 478, 340, 722, 343, px("64748b")) # Top metal rim
    fill_rect(im, 468, 390, 732, 394, px("334155")) # Bottom concrete footer

    # Red-white curb under the monument sign
    for sx in range(460, 740, 16):
        c = R_curb_r if (sx // 16) % 2 == 0 else R_curb_w
        fill_rect(im, sx, 393, min(740, sx + 16), 397, c)

    # "KOSEN" in Vibrant Cyan Blue (Large bold pixel font)
    # Letters K O S E N (y: 348 to 362)
    # K
    fill_rect(im, 495, 348, 498, 362, S_blue)
    fill_rect(im, 498, 353, 502, 356, S_blue)
    fill_rect(im, 502, 348, 506, 353, S_blue)
    fill_rect(im, 502, 356, 506, 362, S_blue)
    # O
    fill_rect(im, 510, 348, 521, 362, S_blue)
    fill_rect(im, 513, 351, 518, 359, S_black)
    # S
    fill_rect(im, 525, 348, 536, 351, S_blue)
    fill_rect(im, 525, 348, 528, 355, S_blue)
    fill_rect(im, 525, 353, 536, 356, S_blue)
    fill_rect(im, 533, 354, 536, 362, S_blue)
    fill_rect(im, 525, 359, 536, 362, S_blue)
    # E
    fill_rect(im, 540, 348, 543, 362, S_blue)
    fill_rect(im, 540, 348, 550, 351, S_blue)
    fill_rect(im, 540, 353, 548, 356, S_blue)
    fill_rect(im, 540, 359, 550, 362, S_blue)
    # N
    fill_rect(im, 554, 348, 557, 362, S_blue)
    fill_rect(im, 557, 350, 561, 357, S_blue)
    fill_rect(im, 561, 348, 564, 362, S_blue)

    # "KMITL" in Warm Vibrant Orange (y: 366 to 380)
    # K
    fill_rect(im, 495, 366, 498, 380, S_orange)
    fill_rect(im, 498, 371, 502, 374, S_orange)
    fill_rect(im, 502, 366, 506, 371, S_orange)
    fill_rect(im, 502, 374, 506, 380, S_orange)
    # M
    fill_rect(im, 510, 366, 513, 380, S_orange)
    fill_rect(im, 513, 368, 517, 374, S_orange)
    fill_rect(im, 517, 368, 521, 374, S_orange)
    fill_rect(im, 521, 366, 524, 380, S_orange)
    # I
    fill_rect(im, 528, 366, 531, 380, S_orange)
    # T
    fill_rect(im, 535, 366, 547, 369, S_orange)
    fill_rect(im, 540, 366, 543, 380, S_orange)
    # L
    fill_rect(im, 551, 366, 554, 380, S_orange)
    fill_rect(im, 551, 377, 561, 380, S_orange)

    # Giant Orange & Blue Chevron Arrow `>`
    poly_arrow_orange = [(580, 346), (620, 364), (580, 384), (595, 384), (635, 364), (595, 346)]
    draw_polygon(im, poly_arrow_orange, S_orange)

    poly_arrow_blue = [(630, 346), (670, 364), (630, 384), (645, 384), (685, 364), (645, 346)]
    draw_polygon(im, poly_arrow_blue, S_blue)

    return im

def generate():
    img = make_stylized_kosen_bg()

    dirs = [r'Assets/Art/Sprites', r'Assets/Resources/Sprites']
    for d in dirs:
        os.makedirs(d, exist_ok=True)
        img.save(os.path.join(d, 'background_stage2.png'))
        img.save(os.path.join(d, 'background_kosen.png'))
        print(f'Saved original stylized KOSEN campus background in {d}')

if __name__ == '__main__':
    generate()
