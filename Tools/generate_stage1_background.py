#!/usr/bin/env python3
"""
Generates the rich, atmospheric 8-bit Stage 1 Background (800x450):
"LATE TO KOSEN: Dormitory to Campus Rush"
- Left: Student Dormitory with messy bedroom window, ringing alarm clock, balconies with clothes
- Middle: Thai soi/streetscape, shophouses, utility poles & wires, canal bridge, trees
- Right: Distant KOSEN-KMITL campus gates & rising morning sun
"""

import os
import uuid
from PIL import Image, ImageDraw

def hex_to_rgba(h, a=255):
    h = h.lstrip('#')
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), a)

def draw_rect(draw, x0, y0, x1, y1, color):
    draw.rectangle([int(x0), int(y0), int(x1), int(y1)], fill=color)

def generate_stage1_background():
    W, H = 800, 450
    img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # 1. Sky Gradient (Morning Dawn - Golden Orange to Soft Sky Blue)
    c_sky_top = hex_to_rgba('7cb9e8')      # Morning blue
    c_sky_mid = hex_to_rgba('bae6fd')      # Soft cyan-blue
    c_sky_horizon = hex_to_rgba('fed7aa')  # Golden morning glow
    
    for y in range(H):
        t = y / (H * 0.7)
        if t < 0.5:
            factor = t / 0.5
            r = int(c_sky_top[0] * (1 - factor) + c_sky_mid[0] * factor)
            g = int(c_sky_top[1] * (1 - factor) + c_sky_mid[1] * factor)
            b = int(c_sky_top[2] * (1 - factor) + c_sky_mid[2] * factor)
        else:
            factor = min(1.0, (t - 0.5) / 0.5)
            r = int(c_sky_mid[0] * (1 - factor) + c_sky_horizon[0] * factor)
            g = int(c_sky_mid[1] * (1 - factor) + c_sky_horizon[1] * factor)
            b = int(c_sky_mid[2] * (1 - factor) + c_sky_horizon[2] * factor)
        draw.line([(0, y), (W, y)], fill=(r, g, b, 255))

    # 2. Rising Morning Sun (East / Right side)
    c_sun = hex_to_rgba('ffedd5', 220)
    c_sun_glow = hex_to_rgba('fdba74', 80)
    draw.ellipse([640, 60, 760, 180], fill=c_sun_glow)
    draw.ellipse([660, 80, 740, 160], fill=c_sun)

    # 3. Fluffy Pixel Clouds
    c_cloud = hex_to_rgba('ffffff', 180)
    c_cloud_shadow = hex_to_rgba('cbd5e1', 160)
    clouds = [
        (80, 50, 110, 35),
        (260, 35, 140, 40),
        (480, 65, 120, 35),
        (680, 40, 90, 30)
    ]
    for (cx, cy, cw, ch) in clouds:
        draw.ellipse([cx, cy, cx + cw, cy + ch], fill=c_cloud_shadow)
        draw.ellipse([cx + 5, cy - 5, cx + cw - 5, cy + ch - 8], fill=c_cloud)
        draw.ellipse([cx + 20, cy - 15, cx + cw - 25, cy + ch - 12], fill=c_cloud)

    # 4. Far Distant City & Campus Skyline (Silhouette)
    c_dist_bldg = hex_to_rgba('94a3b8', 150)
    c_dist_bldg_dark = hex_to_rgba('64748b', 180)
    for bx, bw, bh in [
        (150, 45, 180), (210, 60, 140), (285, 40, 200),
        (340, 70, 160), (430, 50, 220), (500, 80, 170),
        (600, 90, 240), (710, 85, 210)
    ]:
        draw_rect(draw, bx, H - bh, bx + bw, H - 40, c_dist_bldg)
        # Windows
        for wy in range(H - bh + 15, H - 55, 20):
            for wx in range(bx + 8, bx + bw - 8, 12):
                draw_rect(draw, wx, wy, wx + 6, wy + 10, hex_to_rgba('fef08a', 90))

    # 5. LEFT: Student Dormitory Complex (หอพักนักศึกษา 7 ชั้น)
    c_dorm_wall = hex_to_rgba('e2e8f0')        # Concrete white/grey
    c_dorm_trim = hex_to_rgba('0284c7')        # Ocean blue trim
    c_dorm_roof = hex_to_rgba('0369a1')        # Dark blue roof
    c_dorm_shadow = hex_to_rgba('94a3b8')      # Shadow side
    c_balcony_rail = hex_to_rgba('475569')     # Metal railing
    c_curtain = hex_to_rgba('f43f5e')          # Red/pink curtains
    c_room_glow = hex_to_rgba('fef08a')        # Waking room light

    # Main Dorm Block
    draw_rect(draw, 10, 80, 190, H - 25, c_dorm_wall)
    draw_rect(draw, 10, 80, 30, H - 25, c_dorm_shadow) # Left shadow
    draw_rect(draw, 5, 70, 195, 85, c_dorm_roof)       # Roof ledge
    
    # Dorm Rooftop Water Tank & Antenna
    draw_rect(draw, 40, 45, 80, 70, hex_to_rgba('64748b'))
    draw_rect(draw, 130, 30, 134, 70, hex_to_rgba('334155'))
    draw.line([(132, 30), (120, 50)], fill=hex_to_rgba('334155'), width=2)
    draw.line([(132, 30), (144, 50)], fill=hex_to_rgba('334155'), width=2)

    # Dorm Windows and Balconies
    for floor in range(5):
        wy = 100 + floor * 45
        # Left Window (Student's Bedroom - WAKE UP & RUSH!)
        if floor == 1:
            # The famous messy student room with alarm clock
            draw_rect(draw, 40, wy, 80, wy + 32, c_room_glow) # Golden morning light
            # Window frame
            draw_rect(draw, 38, wy - 2, 82, wy + 34, hex_to_rgba('0f172a', 120))
            draw_rect(draw, 40, wy, 80, wy + 32, c_room_glow)
            # Bed & alarm clock silhouette
            draw_rect(draw, 45, wy + 18, 75, wy + 30, hex_to_rgba('3b82f6')) # Blue blanket
            draw_rect(draw, 42, wy + 12, 50, wy + 20, hex_to_rgba('ef4444')) # Alarm clock!
            # ZZZ / Ringing lines
            draw.line([(44, wy + 8), (41, wy + 4)], fill=hex_to_rgba('dc2626'), width=2)
            draw.line([(48, wy + 8), (51, wy + 4)], fill=hex_to_rgba('dc2626'), width=2)
        else:
            draw_rect(draw, 40, wy, 80, wy + 32, hex_to_rgba('38bdf8', 180)) # Blue window
            draw_rect(draw, 42, wy + 2, 52, wy + 28, c_curtain) # Curtain

        # Right Balcony (Clothes drying in typical Thai dorm style!)
        draw_rect(draw, 105, wy + 15, 175, wy + 34, c_dorm_wall)
        draw_rect(draw, 105, wy + 12, 175, wy + 16, c_balcony_rail) # Railing
        for rx in range(110, 175, 12):
            draw.line([(rx, wy + 14), (rx, wy + 34)], fill=c_balcony_rail, width=1)
        
        # Colorful clothes on the drying rack!
        cloth_colors = [hex_to_rgba('ef4444'), hex_to_rgba('3b82f6'), hex_to_rgba('eab308'), hex_to_rgba('10b981')]
        draw_rect(draw, 115, wy + 8, 128, wy + 22, cloth_colors[floor % 4])
        draw_rect(draw, 140, wy + 10, 155, wy + 24, cloth_colors[(floor + 1) % 4])

    # Dorm Ground Floor Entrance & Sign "KOSEN DORM"
    draw_rect(draw, 60, H - 90, 140, H - 25, hex_to_rgba('1e293b')) # Lobby glass door
    draw_rect(draw, 50, H - 110, 150, H - 92, c_dorm_trim)         # Signboard
    # Sign text line
    draw_rect(draw, 60, H - 105, 140, H - 97, hex_to_rgba('ffffff'))

    # 6. MIDDLE: Thai Streetscape / Shophouses & Road to KOSEN
    # Shophouse 1 (7-Eleven / Grocery store look)
    draw_rect(draw, 220, 160, 350, H - 25, hex_to_rgba('f8fafc'))
    draw_rect(draw, 215, 150, 355, 162, hex_to_rgba('ea580c')) # Orange awning top
    # Colorful Shophouse Awning (Stripe roof)
    for ax in range(220, 350, 16):
        draw_rect(draw, ax, 230, ax + 8, 255, hex_to_rgba('16a34a')) # Green stripe
        draw_rect(draw, ax + 8, 230, ax + 16, 255, hex_to_rgba('ea580c')) # Orange stripe
    # Storefront windows & door
    draw_rect(draw, 235, 265, 335, H - 25, hex_to_rgba('0284c7', 160))

    # Shophouse 2 (Thai Commercial Building with Iron Grilles)
    draw_rect(draw, 365, 130, 480, H - 25, hex_to_rgba('fed7aa')) # Peach concrete
    draw_rect(draw, 360, 120, 485, 132, hex_to_rgba('c2410c'))
    for wy in [150, 200, 250]:
        draw_rect(draw, 385, wy, 420, wy + 35, hex_to_rgba('64748b'))
        draw_rect(draw, 435, wy, 465, wy + 35, hex_to_rgba('64748b'))

    # 7. Thai Utility Poles & Tangled Power Lines (Iconic Thai Road scenery!)
    pole_x1 = 205
    pole_x2 = 495
    c_pole = hex_to_rgba('334155')
    c_wires = hex_to_rgba('1e293b', 200)

    for px in [pole_x1, pole_x2]:
        draw_rect(draw, px - 3, 110, px + 3, H - 20, c_pole)
        # Crossbars & transformers
        draw_rect(draw, px - 16, 125, px + 16, 130, c_pole)
        draw_rect(draw, px - 12, 140, px + 12, 145, c_pole)
        draw_rect(draw, px - 8, 150, px + 8, 170, hex_to_rgba('475569')) # Transformer box

    # Tangled Sagging Power Lines connecting dorm to street
    draw.line([(10, 115), (pole_x1, 125)], fill=c_wires, width=2)
    draw.line([(pole_x1, 125), (pole_x2, 125)], fill=c_wires, width=2)
    draw.line([(pole_x2, 125), (W, 140)], fill=c_wires, width=2)
    # Lower drooping lines
    for dy in [8, 16, 24]:
        draw.line([(pole_x1, 125 + dy), ((pole_x1 + pole_x2)//2, 140 + dy), (pole_x2, 125 + dy)], fill=c_wires, width=1)

    # 8. RIGHT: Distant KOSEN-KMITL School Building & Gate (Destination ahead!)
    draw_rect(draw, 520, 150, 780, H - 25, hex_to_rgba('cbd5e1')) # School complex
    draw_rect(draw, 570, 95, 730, H - 25, hex_to_rgba('94a3b8'))  # Main Building 12
    draw_rect(draw, 620, 60, 680, 95, hex_to_rgba('b45309'))     # Clock Tower
    # Clock face
    draw.ellipse([635, 68, 665, 90], fill=hex_to_rgba('ffffff'))
    draw.line([(650, 79), (650, 72)], fill=hex_to_rgba('0f172a'), width=2)
    draw.line([(650, 79), (658, 83)], fill=hex_to_rgba('dc2626'), width=2) # 8:25!
    # School Windows
    for wy in range(120, 280, 30):
        for wx in range(585, 715, 25):
            draw_rect(draw, wx, wy, wx + 15, wy + 18, hex_to_rgba('38bdf8', 190))

    # School Entrance Gate
    draw_rect(draw, 530, H - 90, 545, H - 25, hex_to_rgba('78350f'))
    draw_rect(draw, 595, H - 90, 610, H - 25, hex_to_rgba('78350f'))
    draw_rect(draw, 530, H - 95, 610, H - 85, hex_to_rgba('9a3412')) # Gate Arch

    # 9. Campus Palm Trees & Street Foliage
    c_trunk = hex_to_rgba('78350f')
    c_leaf_dark = hex_to_rgba('15803d')
    c_leaf_light = hex_to_rgba('22c55e')

    for tx in [195, 355, 505, 785]:
        draw_rect(draw, tx - 3, H - 110, tx + 3, H - 25, c_trunk)
        draw.ellipse([tx - 25, H - 160, tx + 25, H - 100], fill=c_leaf_dark)
        draw.ellipse([tx - 20, H - 155, tx + 20, H - 105], fill=c_leaf_light)

    # 10. Foreground Road / Sidewalk Base (Pavement)
    draw_rect(draw, 0, H - 35, W, H, hex_to_rgba('334155'))     # Asphalt road
    draw_rect(draw, 0, H - 38, W, H - 32, hex_to_rgba('64748b')) # Curb line
    # Road dashed yellow/white lines
    for rx in range(20, W, 60):
        draw_rect(draw, rx, H - 18, rx + 35, H - 14, hex_to_rgba('facc15', 220))

    # Save to both Sprites directories
    out_dir = r'Assets/Art/Sprites'
    res_dir = r'Assets/Resources/Sprites'
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(res_dir, exist_ok=True)

    p1 = os.path.join(out_dir, 'background_stage1.png')
    p2 = os.path.join(res_dir, 'background_stage1.png')
    img.save(p1)
    img.save(p2)

    # Generate meta files with custom GUIDs
    template = '''fileFormatVersion: 2
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
  isReadable: 0
  streamingMipmaps: 0
  streamingMipmapsPriority: 0
  vTOnly: 0
  ignoreMasterTextureLimit: 0
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
  spriteExtrude: 1
  spriteMeshType: 1
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
  maxTextureSizeSet: 0
  compressionQualitySet: 0
  textureFormatSet: 0
  ignorePngGamma: 0
  platformSettings:
  - serializedVersion: 3
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
  spriteSheet:
    serializedVersion: 2
    sprites: []
    outline: []
    physicsShape: []
    bones: []
    spriteID: 
    vertices: []
    indices: 
    edges: []
    weights: []
  spritePackingTag: 
  pSDRemoveMatte: 0
  pSDShowRemoveMatteOption: 0
  userData: 
  assetBundleName: 
  assetBundleVariant: 
'''
    g1 = uuid.uuid5(uuid.NAMESPACE_DNS, 'background_stage1.png').hex
    g2 = uuid.uuid5(uuid.NAMESPACE_DNS, 'res_background_stage1.png').hex
    with open(p1 + '.meta', 'w', encoding='utf-8') as f:
        f.write(template.format(guid=g1))
    with open(p2 + '.meta', 'w', encoding='utf-8') as f:
        f.write(template.format(guid=g2))

    print(f'Successfully generated Stage 1 Dorm-to-School Background (800x450)!')

if __name__ == '__main__':
    generate_stage1_background()
