#!/usr/bin/env python3
"""
Generates 32x32 seamlessly tileable sharp metal spike trap (กับดักหนาม) sprite:
- Heavy dark steel base plate at the bottom
- Sharp silver gleaming spikes pointing up with red danger tips
- Perfectly tileable horizontally for pit gaps of any width
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
    wrapU: 0
    wrapV: 0
    wrapW: 0
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

def make_pit_spikes():
    w, h = 32, 32
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))

    O = px("0f172a")         # Dark metal outline
    S_light = px("f1f5f9")   # Gleaming silver shine
    S_mid = px("cbd5e1")     # Steel blade
    S_dark = px("475569")    # Steel shadow
    S_deep = px("1e293b")    # Base dark steel
    R_tip = px("ef4444")     # Blood/danger red tip
    R_dark = px("991b1b")    # Dark red
    Rivet = px("94a3b8")     # Metal rivet

    # 1. Base Plate at bottom (y: 22 to 31)
    for y in range(22, 32):
        for x in range(32):
            if y == 22 or y == 31 or x == 0 or x == 31:
                im.putpixel((x, y), O)
            elif y == 23:
                im.putpixel((x, y), S_mid if x % 8 != 0 else O)
            elif y > 27:
                im.putpixel((x, y), S_deep)
            else:
                im.putpixel((x, y), S_dark)

    # Rivets on base
    for rx in [4, 12, 20, 28]:
        im.putpixel((rx, 26), Rivet)
        im.putpixel((rx + 1, 26), O)

    # 2. 4 Sharp Triangular Spikes rising up (Centers at cx = 4, 12, 20, 28)
    # Each spike is 8px wide, rising from y=24 up to y=2
    for cx in [4, 12, 20, 28]:
        top_y = 2
        for y in range(top_y, 23):
            # Width widens as y goes down
            half_w = max(0, int((y - top_y) * 0.22) + 1)
            for x in range(cx - half_w, cx + half_w + 1):
                if 0 <= x < 32:
                    if x == cx - half_w or x == cx + half_w:
                        im.putpixel((x, y), O)
                    elif y <= top_y + 3:
                        # Red tip
                        im.putpixel((x, y), R_tip if x <= cx else R_dark)
                    elif x < cx:
                        # Left side: Gleaming light shine
                        im.putpixel((x, y), S_light if x == cx - 1 else S_mid)
                    elif x == cx:
                        im.putpixel((x, y), S_light)
                    else:
                        # Right side: Steel shadow
                        im.putpixel((x, y), S_dark)

    return im

def generate():
    im = make_pit_spikes()

    dirs = [r'Assets/Art/Sprites', r'Assets/Resources/Sprites']
    for d in dirs:
        os.makedirs(d, exist_ok=True)
        # Save as spr_pit_spikes.png and spr_spike_floor.png
        p1 = os.path.join(d, 'spr_pit_spikes.png')
        p2 = os.path.join(d, 'spr_spike_floor.png')
        im.save(p1)
        im.save(p2)

        g1 = uuid.uuid5(uuid.NAMESPACE_DNS, 'pit_spikes_' + d).hex
        g2 = uuid.uuid5(uuid.NAMESPACE_DNS, 'spike_floor_' + d).hex

        with open(p1 + '.meta', 'w', encoding='utf-8') as mf:
            mf.write(get_meta(g1))
        with open(p2 + '.meta', 'w', encoding='utf-8') as mf:
            mf.write(get_meta(g2))

    print('Successfully generated spr_pit_spikes.png & spr_spike_floor.png (32x32)!')

if __name__ == '__main__':
    generate()
