#!/usr/bin/env python3
"""
Generates 800x450 8-bit retro Indoor School Building Background (ภายในตึกเรียน KOSEN)
for Level 2 (Stage 2: Inside the KOSEN):
- High-ceiling Japanese/Modern KOSEN university corridor & classrooms
- Classrooms with room nameplates ("ROOM 201: ROBOTICS", "ROOM 202: PROGRAMMING", "LAB 203")
- Windows looking into classrooms with whiteboards, math formulas, and desks
- Large corridor windows with morning sunlight beams
- Digital & analog wall clock showing 07:55 AM (countdown to class!)
- School bulletin boards with timetables, posters, and engineering diagrams
- Modern fluorescent ceiling light fixtures and green EXIT emergency signs
- Polished corridor floor with subtle light reflections
"""

import os
import math
from PIL import Image, ImageDraw

def px(h):
    h = h.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), 255)

def fill_rect(img, x0, y0, x1, y1, c):
    for y in range(max(0, int(y0)), min(450, int(y1))):
        for x in range(max(0, int(x0)), min(800, int(x1))):
            img.putpixel((x, y), c)

def make_indoor_classroom_bg():
    w, h = 800, 450
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))

    # --- PALETTE ---
    # Wall colors (Modern Japanese academic architectural palette: Soft off-white / light birch wood / slate)
    C_wall_top = px("e2e8f0")     # Light upper wall
    C_wall_mid = px("cbd5e1")     # Mid wall
    C_wall_base = px("94a3b8")    # Wall dado / lower panel
    C_wood_trim = px("b45309")    # Warm birch wood molding
    C_wood_trim_l = px("d97706")
    C_wood_trim_d = px("78350f")

    # Ceiling & Lighting
    C_ceiling = px("f1f5f9")
    C_ceiling_grid = px("cbd5e1")
    C_light_glow = px("ffffff")
    C_light_rim = px("94a3b8")

    # Classroom Interior (Seen through door & hallway glass)
    C_room_bg = px("e0e7ff")      # Soft classroom ambient
    C_board_green = px("166534")  # Green chalkboard
    C_board_frame = px("92400e")  # Board wood frame
    C_chalk_white = px("f8fafc")  # Chalk formulas
    C_desk_wood = px("d97706")    # Student desks
    C_chair_blue = px("2563eb")

    # Windows & Glass
    C_glass_sky = px("bae6fd")    # Morning light through window
    C_glass_hl = px("f0f9ff")     # Sunlight reflection
    C_sunbeam = px("fffbeb")      # Warm morning sunbeam

    # Floor & Baseboard
    C_baseboard = px("334155")
    C_floor_tile1 = px("e2e8f0")
    C_floor_tile2 = px("cbd5e1")
    C_floor_refl = px("ffffff")

    # Details: Signs, Clock, Posters
    C_exit_green = px("22c55e")
    C_clock_frame = px("0f172a")
    C_clock_face = px("ffffff")
    C_poster_gold = px("fef08a")
    C_poster_blue = px("60a5fa")
    C_poster_red = px("f87171")
    C_banner_navy = px("1e3a8a")

    # =========================================================================
    # 1. CEILING & FLUORESCENT LIGHTS (y: 0 to 70)
    # =========================================================================
    for y in range(0, 70):
        c = C_ceiling if y % 20 != 0 else C_ceiling_grid
        for x in range(w):
            im.putpixel((x, y), c)

    # Fluorescent Light Fixtures (Long LED panels across corridor)
    for lx in [60, 220, 380, 540, 700]:
        fill_rect(im, lx - 40, 15, lx + 40, 32, C_light_rim)
        fill_rect(im, lx - 38, 17, lx + 38, 30, C_light_glow)
        # Soft light beam downward
        for by in range(32, 100):
            spread = (by - 32) * 0.4
            for bx in range(int(lx - 38 - spread), int(lx + 38 + spread)):
                if 0 <= bx < w:
                    if (bx + by) % 4 == 0:
                        im.putpixel((bx, by), px("f8fafc"))

    # Green Emergency EXIT Signs
    for ex in [180, 580]:
        fill_rect(im, ex - 18, 42, ex + 18, 58, px("0f172a"))
        fill_rect(im, ex - 16, 44, ex + 16, 56, C_exit_green)
        fill_rect(im, ex - 10, 47, ex + 10, 53, px("ffffff")) # Running stickman / EXIT

    # =========================================================================
    # 2. UPPER CORRIDOR WALL (y: 70 to 200)
    # =========================================================================
    fill_rect(im, 0, 70, w, 200, C_wall_top)

    # Wood Molding Divider Bar
    fill_rect(im, 0, 195, w, 205, C_wood_trim)
    fill_rect(im, 0, 195, w, 197, C_wood_trim_l)
    fill_rect(im, 0, 203, w, 205, C_wood_trim_d)

    # KOSEN Faculty Banners on upper wall
    for bx, b_title in [(120, "KOSEN-KMITL"), (500, "ENGINEERING DEPT")]:
        fill_rect(im, bx, 80, bx + 160, 110, C_banner_navy)
        fill_rect(im, bx + 2, 82, bx + 158, 108, px("1e40af"))
        # Gold header stripes & text simulation
        fill_rect(im, bx + 10, 86, bx + 150, 89, px("facc15"))
        fill_rect(im, bx + 15, 94, bx + 145, 99, px("ffffff"))
        fill_rect(im, bx + 25, 101, bx + 135, 103, px("93c5fd"))

    # Wall Clock (07:55 AM - Late to Kosen!)
    cx, cy, cr = 350, 130, 26
    for y in range(cy - cr, cy + cr + 1):
        for x in range(cx - cr, cx + cr + 1):
            d2 = (x - cx)**2 + (y - cy)**2
            if cr*cr - 14 <= d2 <= cr*cr:
                im.putpixel((x, y), C_clock_frame)
            elif d2 < cr*cr - 14:
                im.putpixel((x, y), C_clock_face)
    # Clock hands: Hour pointing to 8, Minute pointing to 11 (07:55 AM)
    for i in range(14): # Hour hand
        im.putpixel((int(cx - i*0.5), int(cy - i*0.8)), C_clock_frame)
    for i in range(20): # Minute hand
        im.putpixel((int(cx - i*0.4), int(cy - i*0.9)), px("dc2626")) # Red minute hand!
    fill_rect(im, cx - 2, cy - 2, cx + 3, cy + 3, C_clock_frame)

    # Bulletin Board with Exam Notices & Schedule (x: 680 to 780, y: 90 to 180)
    fill_rect(im, 680, 90, 780, 185, C_wood_trim)
    fill_rect(im, 684, 94, 776, 181, px("fef3c7")) # Cork board
    # Pinned notices
    fill_rect(im, 690, 100, 725, 135, C_poster_blue)
    fill_rect(im, 735, 105, 770, 140, C_poster_gold)
    fill_rect(im, 695, 145, 730, 175, C_poster_red)
    fill_rect(im, 740, 148, 772, 178, px("ffffff"))

    # =========================================================================
    # 3. CLASSROOM DOORS & WINDOWS (y: 195 to 370)
    # =========================================================================
    # Mid Wall background
    fill_rect(im, 0, 205, w, 370, C_wall_mid)

    # 3 Large Classrooms along the corridor
    rooms = [
        (40,  "201 ROBOTICS LAB"),
        (300, "202 PROGRAMMING 7"),
        (560, "203 CIRCUIT THEORY"),
    ]

    for rx, r_label in rooms:
        # Classroom Door (Width 80, Height 160)
        fill_rect(im, rx, 205, rx + 80, 370, C_wood_trim)
        fill_rect(im, rx + 4, 209, rx + 76, 366, px("d97706")) # Wooden door
        # Door Window (Look into classroom)
        fill_rect(im, rx + 14, 220, rx + 66, 280, px("0f172a"))
        fill_rect(im, rx + 16, 222, rx + 64, 278, C_room_bg)
        # View of chalkboard through window
        fill_rect(im, rx + 20, 226, rx + 60, 255, C_board_green)
        fill_rect(im, rx + 22, 232, rx + 58, 235, C_chalk_white)
        # Silver Door Handle
        fill_rect(im, rx + 10, 290, rx + 18, 305, px("f8fafc"))
        fill_rect(im, rx + 12, 292, rx + 16, 303, px("64748b"))

        # Room Signboard Plaque on top of door
        fill_rect(im, rx - 6, 178, rx + 86, 200, px("0f172a"))
        fill_rect(im, rx - 4, 180, rx + 84, 198, px("f8fafc")) # White acrylic plaque
        fill_rect(im, rx + 4, 184, rx + 76, 194, px("1e3a8a"))  # Blue text simulation

        # Large Corridor Window next to door (Looking into classroom / campus courtyard)
        wx0, wx1 = rx + 95, rx + 240
        if wx1 <= w - 10:
            fill_rect(im, wx0, 205, wx1, 330, C_wood_trim)
            fill_rect(im, wx0 + 4, 209, wx1 - 4, 326, C_room_bg)

            # Blackboard in classroom (Width 110, Height 55)
            fill_rect(im, wx0 + 15, 218, wx1 - 15, 275, C_board_frame)
            fill_rect(im, wx0 + 18, 221, wx1 - 18, 272, C_board_green)

            # Math formulas & Circuit diagrams on board: E=mc², sum, integr, logic gates
            fill_rect(im, wx0 + 24, 228, wx0 + 50, 231, C_chalk_white)
            fill_rect(im, wx0 + 24, 236, wx0 + 65, 239, C_chalk_white)
            fill_rect(im, wx0 + 24, 244, wx0 + 55, 247, px("fef08a")) # Yellow chalk formula
            # Logic gate / flowchart diagram
            fill_rect(im, wx0 + 75, 228, wx1 - 26, 260, px("0f172a"))
            fill_rect(im, wx0 + 77, 230, wx1 - 28, 258, C_board_green)
            fill_rect(im, wx0 + 80, 235, wx1 - 32, 238, C_chalk_white)
            fill_rect(im, wx0 + 80, 248, wx1 - 32, 251, C_chalk_white)

            # Student Desks & Chairs visible in foreground of classroom window
            for dx in range(wx0 + 20, wx1 - 25, 40):
                fill_rect(im, dx, 290, dx + 30, 315, C_desk_wood)
                fill_rect(im, dx + 2, 292, dx + 28, 296, px("fef08a")) # Desk top shine
                fill_rect(im, dx + 8, 305, dx + 22, 325, C_chair_blue) # Blue chair

            # Glass diagonal light reflection streak
            for gy in range(210, 325):
                gx = wx0 + int((gy - 210) * 0.9)
                if wx0 < gx < wx1 - 4:
                    fill_rect(im, gx, gy, min(wx1 - 4, gx + 8), gy + 1, px("ffffff"))

    # =========================================================================
    # 4. LOWER WALL DADO & BASEBOARD (y: 360 to 390)
    # =========================================================================
    fill_rect(im, 0, 360, w, 380, C_wall_base)
    fill_rect(im, 0, 380, w, 390, C_baseboard)

    # =========================================================================
    # 5. POLISHED TERRAZZO CORRIDOR FLOOR (y: 390 to 450)
    # =========================================================================
    for y in range(390, 450):
        for x in range(w):
            # Checkered polished tiles
            tx = (x + int((y - 390) * 0.5)) // 40
            ty = (y - 390) // 15
            c = C_floor_tile1 if (tx + ty) % 2 == 0 else C_floor_tile2

            # Soft vertical light reflections from fluorescent lights above
            for lx in [60, 220, 380, 540, 700]:
                if abs(x - lx) < 25:
                    c = C_floor_refl if (x + y) % 3 == 0 else c

            im.putpixel((x, y), c)

    return im

def generate():
    im = make_indoor_classroom_bg()

    dirs = [r'Assets/Art/Sprites', r'Assets/Resources/Sprites']
    for d in dirs:
        os.makedirs(d, exist_ok=True)
        # Save as background_stage2.png and background_kosen.png
        p1 = os.path.join(d, 'background_stage2.png')
        p2 = os.path.join(d, 'background_kosen.png')
        im.save(p1)
        im.save(p2)
        print(f'Saved indoor classroom background in {d}')

if __name__ == '__main__':
    generate()
