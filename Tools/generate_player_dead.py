#!/usr/bin/env python3
"""
Generates the 32x32 8-bit knocked-out death pose sprite: player_dead.png
- Student lying flat on the ground
- 'X X' dizzy knockout eyes
- Splayed out arms and legs
- Floating dizzy stars
"""

import os
import uuid
from PIL import Image, ImageDraw

def generate_dead_sprite():
    img = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Color Palette (matching player_idle.png)
    c_outline = (15, 23, 42, 255)
    c_skin = (255, 215, 168, 255)
    c_skin_shadow = (240, 179, 126, 255)
    c_hair = (39, 28, 25, 255)
    c_hair_hl = (74, 51, 45, 255)
    c_shirt = (255, 255, 255, 255)
    c_shirt_shadow = (203, 213, 225, 255)
    c_tie = (220, 38, 38, 255)
    c_pants = (30, 58, 138, 255)
    c_pants_shadow = (23, 37, 84, 255)
    c_shoes = (24, 24, 27, 255)
    c_star = (250, 204, 21, 255) # Yellow dizzy stars

    # 1. Dizzy Stars floating above knocked out student (y = 8..13)
    # Star 1 (x=6, y=10)
    draw.point((6, 10), fill=c_star)
    draw.point((5, 11), fill=c_star)
    draw.point((7, 11), fill=c_star)
    draw.point((6, 12), fill=c_star)
    # Star 2 (x=12, y=8)
    draw.point((12, 8), fill=c_star)
    draw.point((11, 9), fill=c_star)
    draw.point((13, 9), fill=c_star)
    draw.point((12, 10), fill=c_star)
    # Star 3 (x=18, y=11)
    draw.point((18, 11), fill=c_star)
    draw.point((17, 12), fill=c_star)
    draw.point((19, 12), fill=c_star)
    draw.point((18, 13), fill=c_star)

    # 2. Knocked-out Body lying flat on ground (Ground level around y=24..28)

    # Hair / Head on Left (x=3..10, y=20..27)
    draw.rectangle([3, 20, 10, 27], fill=c_hair)
    draw.rectangle([4, 21, 8, 22], fill=c_hair_hl)
    
    # Face (x=5..11, y=22..27)
    draw.rectangle([5, 22, 11, 26], fill=c_skin)
    draw.rectangle([5, 25, 11, 26], fill=c_skin_shadow)

    # 'X X' Knockout Eyes (x=7, 9)
    # Eye 1 'X'
    draw.point((6, 23), fill=c_outline)
    draw.point((8, 23), fill=c_outline)
    draw.point((7, 24), fill=c_outline)
    draw.point((6, 25), fill=c_outline)
    draw.point((8, 25), fill=c_outline)
    # Eye 2 'X'
    draw.point((9, 23), fill=c_outline)
    draw.point((11, 23), fill=c_outline)
    draw.point((10, 24), fill=c_outline)
    draw.point((9, 25), fill=c_outline)
    draw.point((11, 25), fill=c_outline)

    # Dizzy open mouth
    draw.point((8, 26), fill=c_tie)

    # Torso / White School Shirt (x=11..19, y=21..27)
    draw.rectangle([11, 21, 19, 26], fill=c_shirt)
    draw.rectangle([11, 25, 19, 26], fill=c_shirt_shadow)
    # Red student tie on chest
    draw.rectangle([13, 23, 16, 24], fill=c_tie)

    # Splayed out Limp Arm (x=12..17, y=19..21)
    draw.rectangle([13, 19, 17, 21], fill=c_shirt)
    draw.rectangle([11, 19, 13, 21], fill=c_skin)

    # Navy Student Shorts (x=19..24, y=22..27)
    draw.rectangle([19, 22, 24, 26], fill=c_pants)
    draw.rectangle([19, 25, 24, 26], fill=c_pants_shadow)

    # Legs & Shoes (x=24..30, y=23..27)
    draw.rectangle([24, 23, 28, 25], fill=c_skin)
    draw.rectangle([27, 23, 30, 26], fill=c_shoes)
    draw.point((30, 24), fill=c_outline)

    # Dark Outline around body on the floor for crisp pixel art look
    draw.line([(3, 27), (30, 27)], fill=c_outline, width=1)

    out_dir = r'Assets/Art/Sprites'
    res_dir = r'Assets/Resources/Sprites'
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(res_dir, exist_ok=True)

    p1 = os.path.join(out_dir, 'player_dead.png')
    p2 = os.path.join(res_dir, 'player_dead.png')
    img.save(p1)
    img.save(p2)

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
    g1 = uuid.uuid5(uuid.NAMESPACE_DNS, 'player_dead.png').hex
    g2 = uuid.uuid5(uuid.NAMESPACE_DNS, 'res_player_dead.png').hex
    with open(p1 + '.meta', 'w', encoding='utf-8') as f:
        f.write(template.format(guid=g1))
    with open(p2 + '.meta', 'w', encoding='utf-8') as f:
        f.write(template.format(guid=g2))

    print('Successfully generated player_dead.png (32x32 knockout pose with dizzy stars)!')

if __name__ == '__main__':
    generate_dead_sprite()
