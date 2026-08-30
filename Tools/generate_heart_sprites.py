#!/usr/bin/env python3
"""
Generates 32x32 retro 8-bit heart sprites:
1. heart_full.png  - Vibrant red heart with black outline and pixel shine
2. heart_empty.png - Hollow black outline heart frame with empty/dim center
"""

import os
import uuid
from PIL import Image, ImageDraw

def generate_hearts():
    out_dir = r'Assets/Art/Sprites'
    res_dir = r'Assets/Resources/Sprites'
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(res_dir, exist_ok=True)

    # 32x32 grid
    # Outline pixel mask for classic retro heart shape (centered around 16, 16)
    c_outline = (15, 23, 42, 255)      # Deep dark slate black
    c_red_bright = (248, 113, 113, 255) # Light red highlight
    c_red = (239, 68, 68, 255)          # Main ruby red
    c_red_dark = (185, 28, 28, 255)     # Deep red shading
    c_shine = (255, 255, 255, 255)      # Specular glint
    c_empty_inner = (15, 23, 42, 55)    # Translucent hollow interior

    # Pixel definition for 24x22 heart centered in 32x32
    # Y range: 5 to 26, X range: 4 to 27
    heart_pixels = [
        # Top arches
        "     XXXX    XXXX     ",
        "    XRRRRX  XRRRRX    ",
        "   XSRRRRRXXRRRRRRX   ",
        "  XSSRRRRRRXRRRRRRRX  ",
        "  XSRRRRRRRRRRRRRRRX  ",
        "  XRRRRRRRRRRRRRRRRX  ",
        "  XRRRRRRRRRRRRRRRRX  ",
        "  XRRRRRRRRRRRRRRRRX  ",
        "   XRRRRRRRRRRRRRRX   ",
        "   XRRRRRRRRRRRRDDX   ",
        "    XRRRRRRRRRRDDX    ",
        "    XRRRRRRRRRDDX     ",
        "     XRRRRRRRDDX      ",
        "      XRRRRRDDX       ",
        "       XRRRDDX        ",
        "        XRRDDX        ",
        "         XRDDX        ",
        "          XDX         ",
        "           X          "
    ]

    offset_x = 5
    offset_y = 6

    # 1. Full Heart
    img_full = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    for row_idx, row in enumerate(heart_pixels):
        for col_idx, ch in enumerate(row):
            x = offset_x + col_idx
            y = offset_y + row_idx
            if x >= 32 or y >= 32: continue
            
            if ch == 'X':
                img_full.putpixel((x, y), c_outline)
            elif ch == 'S':
                img_full.putpixel((x, y), c_shine)
            elif ch == 'R':
                # Upper gradient
                if row_idx < 4:
                    img_full.putpixel((x, y), c_red_bright)
                else:
                    img_full.putpixel((x, y), c_red)
            elif ch == 'D':
                img_full.putpixel((x, y), c_red_dark)

    # 2. Empty Heart (Only outline + dark translucent inside)
    img_empty = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    for row_idx, row in enumerate(heart_pixels):
        for col_idx, ch in enumerate(row):
            x = offset_x + col_idx
            y = offset_y + row_idx
            if x >= 32 or y >= 32: continue
            
            if ch == 'X':
                img_empty.putpixel((x, y), c_outline)
            elif ch in ('S', 'R', 'D'):
                img_empty.putpixel((x, y), c_empty_inner)

    # Save PNGs
    img_full.save(os.path.join(out_dir, 'heart_full.png'))
    img_full.save(os.path.join(res_dir, 'heart_full.png'))
    img_empty.save(os.path.join(out_dir, 'heart_empty.png'))
    img_empty.save(os.path.join(res_dir, 'heart_empty.png'))

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

    files = ['heart_full.png', 'heart_empty.png']
    for f in files:
        p1 = os.path.join(out_dir, f)
        p2 = os.path.join(res_dir, f)
        g1 = uuid.uuid5(uuid.NAMESPACE_DNS, 'art_' + f).hex
        g2 = uuid.uuid5(uuid.NAMESPACE_DNS, 'res_' + f).hex
        with open(p1 + '.meta', 'w', encoding='utf-8') as mf:
            mf.write(template.format(guid=g1))
        with open(p2 + '.meta', 'w', encoding='utf-8') as mf:
            mf.write(template.format(guid=g2))

    print('Generated heart_full.png and heart_empty.png with metadata!')

if __name__ == '__main__':
    generate_hearts()
