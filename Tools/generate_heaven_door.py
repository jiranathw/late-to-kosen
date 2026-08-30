#!/usr/bin/env python3
"""
Generates 64x96 8-bit retro Heaven's Gate (ประตูสวรรค์) sprite for Teleporter:
- Golden heavenly arch with winged crest and halo
- Radiant blinding light / divine portal aura
- Fluffy heavenly clouds at the base
- Open pearly golden gates with sparkles
"""

import os
import uuid
import math
from PIL import Image

def px(h):
    h = h.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), 255)

def get_meta(guid):
    return f'''fileFormatVersion: 2
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

def make_heaven_gate():
    w, h = 64, 96
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))

    # Palette
    O = px("0f172a")         # Dark outline
    G_bright = px("fef08a")  # Pure Gold Highlight
    G_gold = px("eab308")    # Heavenly Gold
    G_dark = px("a16207")    # Deep Gold Shadow
    P_white = px("ffffff")   # Pure Holy Light
    P_light = px("fef9c3")   # Light Beam
    P_sky = px("bae6fd")     # Cyan Heavenly Tint
    P_purp = px("e9d5ff")    # Divine Lavender
    C_cloud = px("f8fafc")   # Cloud White
    C_cloud_d = px("cbd5e1") # Cloud Shadow
    Star = px("facc15")      # Star Gold

    # 1. Divine Radiant Portal Interior (Y: 10 to 88, X: 10 to 54)
    # Generates a radiant arched vortex of pure divine light
    for y in range(10, 88):
        for x in range(10, 54):
            dx = (x - 32) / 20.0
            dy = (y - 38) / 26.0
            dist_top = dx * dx + dy * dy

            if y <= 38:
                inside = (dist_top <= 1.0)
            else:
                inside = (abs(x - 32) <= 20)

            if inside:
                # Radial beam gradient
                rad = math.sqrt((x - 32)**2 + (y - 50)**2)
                angle = math.atan2(y - 50, x - 32)
                ray = (math.sin(angle * 8) + 1.0) * 0.5

                if rad < 12:
                    c = P_white
                elif rad < 24:
                    c = P_white if ray > 0.4 else P_light
                elif rad < 36:
                    c = P_light if ray > 0.3 else P_sky
                else:
                    c = P_sky if (x + y) % 2 == 0 else P_purp
                im.putpixel((x, y), c)

    # 2. Golden Archway & Greek Pillars
    # Golden Arch Top (Curved)
    for y in range(4, 40):
        for x in range(6, 58):
            dx = (x - 32) / 22.0
            dy = (y - 38) / 28.0
            d_outer = dx * dx + dy * dy

            dx_i = (x - 32) / 19.0
            dy_i = (y - 38) / 25.0
            d_inner = dx_i * dx_i + dy_i * dy_i

            if y <= 38:
                if 0.95 <= d_outer <= 1.25:
                    im.putpixel((x, y), O if (d_outer > 1.2 or d_outer < 0.98) else G_gold)
                elif 0.98 <= d_inner <= 1.08:
                    im.putpixel((x, y), G_bright if (x + y) % 3 == 0 else G_gold)

    # Winged Crest / Halo at Very Top (y: 2 to 14, x: 20 to 44)
    for y in range(2, 14):
        for x in range(20, 44):
            dx = abs(x - 32)
            if dx <= 10 - abs(y - 7):
                im.putpixel((x, y), G_bright if y < 7 else G_gold)
                if dx == 10 - abs(y - 7) or y == 2:
                    im.putpixel((x, y), O)
    # Divine Cross / Sun in center
    for y in range(4, 11):
        im.putpixel((32, y), P_white)
    for x in range(29, 36):
        im.putpixel((x, 7), P_white)

    # Left & Right Golden Pillars (Y: 34 to 88)
    for y in range(34, 88):
        # Left Pillar (x: 4 to 12)
        for x in range(4, 12):
            if x == 4 or x == 11:
                im.putpixel((x, y), O)
            elif x in (5, 6):
                im.putpixel((x, y), G_bright if (y % 4 < 2) else G_gold)
            elif x in (7, 8):
                im.putpixel((x, y), G_gold)
            else:
                im.putpixel((x, y), G_dark)

        # Right Pillar (x: 52 to 60)
        for x in range(52, 60):
            if x == 52 or x == 59:
                im.putpixel((x, y), O)
            elif x in (53, 54):
                im.putpixel((x, y), G_bright if (y % 4 < 2) else G_gold)
            elif x in (55, 56):
                im.putpixel((x, y), G_gold)
            else:
                im.putpixel((x, y), G_dark)

    # Pillar capitals & bases (Fluted gold)
    for cap_y in [32, 33, 34, 84, 85, 86]:
        for x in range(2, 14):
            im.putpixel((x, cap_y), O if (x in (2, 13) or cap_y in (32, 86)) else G_bright)
        for x in range(50, 62):
            im.putpixel((x, cap_y), O if (x in (50, 61) or cap_y in (32, 86)) else G_bright)

    # 3. Open Golden Pearly Gates (Pickets swung open)
    # Left Gate open inwards
    for y in range(42, 82):
        for bar_x in [13, 17, 21]:
            im.putpixel((bar_x, y), G_gold if (y % 2 == 0) else G_bright)
            im.putpixel((bar_x + 1, y), G_dark)
    # Right Gate open inwards
    for y in range(42, 82):
        for bar_x in [42, 46, 50]:
            im.putpixel((bar_x, y), G_bright if (y % 2 == 0) else G_gold)
            im.putpixel((bar_x + 1, y), G_dark)

    # 4. Fluffy Heavenly Clouds at Base (y: 80 to 95, x: 0 to 63)
    cloud_centers = [(10, 88, 12), (24, 90, 10), (38, 89, 11), (54, 88, 12), (32, 92, 14)]
    for y in range(78, 96):
        for x in range(0, 64):
            in_cloud = False
            for cx, cy, cr in cloud_centers:
                d2 = (x - cx)**2 + (y - cy)**2 * 1.5
                if d2 <= cr * cr:
                    in_cloud = True
                    if d2 >= (cr - 1.5)**2:
                        im.putpixel((x, y), O if y > 82 and (x == 0 or x == 63) else C_cloud_d)
                    elif d2 <= (cr - 4)**2:
                        im.putpixel((x, y), C_cloud)
                    else:
                        im.putpixel((x, y), C_cloud_d if y > 88 else C_cloud)
                    break

    # 5. Sparkling Holy Stars dancing around the gate
    star_locs = [(18, 22), (46, 20), (8, 48), (56, 46), (32, 42), (28, 64), (36, 68)]
    for sx, sy in star_locs:
        im.putpixel((sx, sy), P_white)
        im.putpixel((sx - 1, sy), Star)
        im.putpixel((sx + 1, sy), Star)
        im.putpixel((sx, sy - 1), Star)
        im.putpixel((sx, sy + 1), Star)

    return im

def generate():
    im = make_heaven_gate()

    dirs = [r'Assets/Art/Sprites', r'Assets/Resources/Sprites']
    for d in dirs:
        os.makedirs(d, exist_ok=True)
        # Save as spr_heaven_door.png and spr_teleporter.png
        p1 = os.path.join(d, 'spr_heaven_door.png')
        p2 = os.path.join(d, 'spr_teleporter.png')
        im.save(p1)
        im.save(p2)

        g1 = uuid.uuid5(uuid.NAMESPACE_DNS, 'heaven_' + d).hex
        g2 = uuid.uuid5(uuid.NAMESPACE_DNS, 'teleport_' + d).hex

        with open(p1 + '.meta', 'w', encoding='utf-8') as mf:
            mf.write(get_meta(g1))
        with open(p2 + '.meta', 'w', encoding='utf-8') as mf:
            mf.write(get_meta(g2))

    print('Successfully generated spr_heaven_door.png & spr_teleporter.png (64x96)!')

if __name__ == '__main__':
    generate()
