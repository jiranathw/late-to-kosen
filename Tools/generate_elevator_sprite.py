#!/usr/bin/env python3
"""
Generates 64x96 8-bit retro Building Elevator Door (ประตูลิฟต์ขึ้นตึก) sprite:
- Stainless steel modern elevator frame
- Digital floor indicator display ("▲ 4F" glowing green/gold)
- Call button panel with glowing UP/DOWN arrows
- Double sliding stainless steel doors with reflective brushed metal panels
- Floor threshold and safety indicator lights
"""

import os
import uuid
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

def fill_rect(img, x0, y0, x1, y1, c):
    for y in range(y0, y1):
        for x in range(x0, x1):
            if 0 <= x < 64 and 0 <= y < 96:
                img.putpixel((x, y), c)

def make_elevator():
    w, h = 64, 96
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))

    # Palette
    O = px("0f172a")         # Dark structural outline
    F_light = px("e2e8f0")   # Outer frame highlight
    F_mid = px("94a3b8")     # Outer steel frame
    F_dark = px("475569")    # Dark frame shadow
    F_deep = px("1e293b")    # Deep cavity shadow

    D_light = px("f8fafc")   # Brushed door shine
    D_mid = px("cbd5e1")     # Stainless steel door body
    D_dark = px("64748b")    # Door panel groove / shadow
    D_seam = px("0f172a")    # Center door seam

    Screen_bg = px("022c22") # LED display dark green/black
    LED_green = px("4ade80") # Glowing floor number "4F"
    LED_arrow = px("22c55e") # Green arrow
    Lamp_red = px("ef4444")  # Red in-use lamp

    Btn_panel = px("334155") # Call button plate
    Btn_glow = px("facc15")  # Glowing call button yellow

    # 1. Outer Steel Wall Frame (y: 2 to 94, x: 2 to 62)
    fill_rect(im, 2, 2, 62, 94, O)
    fill_rect(im, 4, 4, 60, 92, F_mid)
    fill_rect(im, 4, 4, 59, 7, F_light) # Top edge shine
    fill_rect(im, 4, 4, 7, 92, F_light)  # Left edge shine
    fill_rect(im, 57, 5, 60, 92, F_dark) # Right edge shadow

    # 2. Header Area: ELEVATOR SIGN & LED DISPLAY (y: 6 to 22, x: 6 to 58)
    fill_rect(im, 6, 6, 58, 22, F_dark)
    fill_rect(im, 8, 8, 56, 20, F_deep)

    # Digital LED Screen in center (y: 9 to 19, x: 22 to 42)
    fill_rect(im, 22, 9, 42, 19, O)
    fill_rect(im, 23, 10, 41, 18, Screen_bg)

    # LED Floor Number "4" + "F" and Up Arrow "▲"
    # Up Arrow (x: 25 to 29)
    for y in range(12, 16):
        hw = 15 - y
        fill_rect(im, 27 - hw, y, 28 + hw, y + 1, LED_arrow)
    fill_rect(im, 26, 16, 29, 17, LED_arrow)

    # Number "4" (x: 31 to 35)
    fill_rect(im, 31, 12, 33, 15, LED_green)
    fill_rect(im, 31, 14, 35, 16, LED_green)
    fill_rect(im, 34, 12, 36, 17, LED_green)

    # Letter "F" (x: 37 to 40)
    fill_rect(im, 37, 12, 39, 17, LED_green)
    fill_rect(im, 37, 12, 40, 14, LED_green)
    fill_rect(im, 37, 14, 40, 15, LED_green)

    # Indicator Lights (Green Arrival Light & Red Busy Light)
    fill_rect(im, 12, 12, 17, 16, O)
    fill_rect(im, 13, 13, 16, 15, LED_green) # Green ready
    fill_rect(im, 47, 12, 52, 16, O)
    fill_rect(im, 48, 13, 51, 15, Lamp_red)  # Red busy

    # 3. Door Cavity & Trim (y: 22 to 88, x: 6 to 58)
    fill_rect(im, 6, 22, 58, 88, O)
    fill_rect(im, 7, 23, 57, 87, F_deep)

    # 4. Left Sliding Stainless Door (y: 24 to 86, x: 8 to 31)
    fill_rect(im, 8, 24, 31, 86, D_mid)
    # Vertical shine band
    fill_rect(im, 12, 25, 17, 85, D_light)
    fill_rect(im, 25, 25, 29, 85, D_dark)
    # Horizontal panel grooves
    for gy in [38, 52, 66]:
        fill_rect(im, 9, gy, 30, gy + 2, O)
        fill_rect(im, 9, gy + 1, 30, gy + 2, D_dark)

    # 5. Right Sliding Stainless Door (y: 24 to 86, x: 33 to 56)
    fill_rect(im, 33, 24, 56, 86, D_mid)
    # Vertical shine band
    fill_rect(im, 37, 25, 42, 85, D_light)
    fill_rect(im, 50, 25, 54, 85, D_dark)
    # Horizontal panel grooves
    for gy in [38, 52, 66]:
        fill_rect(im, 34, gy, 55, gy + 2, O)
        fill_rect(im, 34, gy + 1, 55, gy + 2, D_dark)

    # Center Door Gap & Rubber Seal (x: 31 to 33)
    fill_rect(im, 31, 24, 33, 86, D_seam)

    # 6. Call Button Plate on Right Pillar (y: 48 to 62, x: 57 to 61)
    fill_rect(im, 57, 48, 61, 62, O)
    fill_rect(im, 58, 49, 60, 61, Btn_panel)
    fill_rect(im, 58, 51, 60, 53, Btn_glow) # UP button
    fill_rect(im, 58, 56, 60, 58, Btn_glow) # DOWN button

    # 7. Floor Threshold Plate (y: 86 to 92, x: 4 to 60)
    fill_rect(im, 4, 86, 60, 92, O)
    fill_rect(im, 5, 87, 59, 91, F_dark)
    for tx in range(6, 58, 4):
        fill_rect(im, tx, 88, tx + 2, 90, F_light)

    return im

def generate():
    im = make_elevator()

    dirs = [r'Assets/Art/Sprites', r'Assets/Resources/Sprites']
    for d in dirs:
        os.makedirs(d, exist_ok=True)
        # Save as spr_elevator.png and spr_goal.png
        p1 = os.path.join(d, 'spr_elevator.png')
        p2 = os.path.join(d, 'spr_goal.png')
        im.save(p1)
        im.save(p2)

        g1 = uuid.uuid5(uuid.NAMESPACE_DNS, 'elevator_' + d).hex
        g2 = uuid.uuid5(uuid.NAMESPACE_DNS, 'goal_' + d).hex

        with open(p1 + '.meta', 'w', encoding='utf-8') as mf:
            mf.write(get_meta(g1))
        with open(p2 + '.meta', 'w', encoding='utf-8') as mf:
            mf.write(get_meta(g2))

    print('Successfully generated spr_elevator.png & spr_goal.png (64x96)!')

if __name__ == '__main__':
    generate()
