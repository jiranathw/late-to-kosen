#!/usr/bin/env python3
"""
Generates 8-bit retro pixel art vehicle sprites for TrafficLane:
1. spr_vehicle_car.png (64x32)       - Pickup truck / Bangkok city car with headlights & wheels
2. spr_vehicle_motorbike.png (48x24) - Speeding motorbike with rider & helmet
"""

import os
import uuid
from PIL import Image

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

def make_car_pickup():
    # 64x32 Red Pickup Truck / City Vehicle facing LEFT
    pal = {
        '.': (0, 0, 0, 0),
        'k': (15, 23, 42, 255),         # Dark outline
        'R': (220, 38, 38, 255),        # Red body
        'r': (185, 28, 28, 255),        # Red shadow
        'H': (248, 113, 113, 255),      # Red highlight
        'G': (186, 230, 253, 255),      # Glass window
        'g': (125, 211, 252, 255),      # Glass shadow
        'W': (255, 255, 255, 255),      # White shine / roof
        'Y': (250, 204, 21, 255),       # Headlight bright yellow
        'y': (254, 240, 138, 255),      # Headlight flare
        'T': (30, 41, 59, 255),         # Tire dark
        't': (51, 65, 85, 255),         # Tire highlight
        'S': (226, 232, 240, 255),      # Silver rim / hubcap
        's': (148, 163, 184, 255),      # Rim shadow
        'B': (15, 20, 30, 255),         # Bumper / grill
        'E': (239, 68, 68, 255),        # Taillight red
    }

    grid = [
        "................................................................", # 0
        "................................................................", # 1
        "................................................................", # 2
        "................................................................", # 3
        "................................................................", # 4
        "................................................................", # 5
        "................................................................", # 6
        "................................................................", # 7
        "......................kkkkkkkkkkkkkkk...........................", # 8 Cabin roof
        "...................kkkHHHHHHHHHHHHHHHkk.........................", # 9
        "..................kGGGGGGGGGGGGGGGGGGGGk........................", # 10 Windshield / side glass
        ".................kGGGGGGGGGGGGGGGGGGGGGk........................", # 11
        "................kGGgGGGGGGGGgGGGGGGGGGgGk.......................", # 12
        ".............kkkkGGgGGGGGGGGgGGGGGGGGGgGkkkkkkkkkkkkkkkkk.......", # 13 Truck bed
        "............kHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHk.......", # 14 Hood & Body
        "...........kRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRk.......", # 15
        "..........kYRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRkE......", # 16 Headlight & Taillight
        ".........kYYkRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRkE......", # 17
        ".........kYYkrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrkE......", # 18
        ".........kBBkkkkkkkrrrrrrrrrrrrrrrrrrrrkkkkkkkkrrrrrrrrrkk......", # 19 Wheel wells
        "..........kBkTTTTTTkkkrrrrrrrrrrrrrrrkkkTTTTTTTkkkrrrrrkk.......", # 20
        "...........kTTtttttTTTkrrrrrrrrrrrrrkTTtttttTTTkrrrrrrk.........", # 21 Wheels
        "..........kTtssssssstTTkrrrrrrrrrrrkTtssssssstTTkkkkkk..........", # 22
        "..........kTtssSSSSsstTkBBBBBBBBBBTkTtssSSSSsstTkBBk............", # 23 Hubcaps & bumpers
        "..........kTtssSSSSsstTkBBBBBBBBBBTkTtssSSSSsstTk...............", # 24
        "..........kTtssssssstTTk..........kTtssssssstTTk................", # 25
        "...........kTTtttttTTTk............kTTtttttTTTk.................", # 26
        "............kTTTTTTTTk..............kTTTTTTTTk..................", # 27
        ".............kkkkkkkk................kkkkkkkk...................", # 28
        "................................................................", # 29
        "................................................................", # 30
        "................................................................", # 31
    ]

    im = Image.new('RGBA', (64, 32), (0, 0, 0, 0))
    for y, line in enumerate(grid):
        for x, ch in enumerate(line):
            im.putpixel((x, y), pal.get(ch, (0, 0, 0, 0)))
    return im

def make_motorbike():
    # 48x24 Speeding Motorcycle with Rider facing LEFT
    pal = {
        '.': (0, 0, 0, 0),
        'k': (15, 23, 42, 255),         # Outline
        'H': (249, 115, 22, 255),       # Orange helmet / jacket
        'h': (234, 88, 12, 255),        # Orange shadow
        'V': (15, 23, 42, 255),         # Helmet visor
        'S': (255, 220, 188, 255),      # Hands
        'J': (30, 58, 138, 255),        # Blue pants
        'T': (30, 41, 59, 255),         # Tire dark
        't': (51, 65, 85, 255),         # Tire highlight
        's': (226, 232, 240, 255),      # Silver spokes
        'Y': (250, 204, 21, 255),       # Headlight bright yellow
        'y': (254, 240, 138, 255),      # Headlight flare
        'B': (15, 20, 30, 255),         # Bike frame black
        'E': (239, 68, 68, 255),        # Taillight red
    }

    grid = [
        "................................................", # 0
        "...................kkkk.........................", # 1 Helmet
        "..................kHHHHk........................", # 2
        ".................kVVVHHk........................", # 3 Visor
        "..................kkkHHk........................", # 4
        "..................kHHHHHkk......................", # 5 Rider torso leaning
        "................kSkHHHHHHHk.....................", # 6
        "...............kYYkHHHHHHHk.....................", # 7 Headlight & Jacket
        "..............kYYYkJJJJHHHkE....................", # 8 Blue pants
        "..............kYYkJJJJJJkkkE....................", # 9
        "...............kkkJJkkkk........................", # 10
        "............kkkkkJJk...kkkkkkk..................", # 11 Bike frame & seat
        "..........kkTTTTkJk..kkTTTTTTTkk................", # 12 Wheels
        ".........kTTttttTBk.kTTtttttttTTk...............", # 13
        "........kTtsssstTTkkTtsssssssssTtkk.............", # 14 Spokes
        "........kTtsssstTTkkTtsssssssssTtkk.............", # 15
        "........kTtsssstTTkkTtsssssssssTtkk.............", # 16
        ".........kTTttttTBk.kTTtttttttTTk...............", # 17
        "..........kkTTTTTk...kkTTTTTTTkk................", # 18
        "............kkkkk......kkkkkkk..................", # 19
        "................................................", # 20
        "................................................", # 21
        "................................................", # 22
        "................................................", # 23
    ]

    im = Image.new('RGBA', (48, 24), (0, 0, 0, 0))
    for y, line in enumerate(grid):
        for x, ch in enumerate(line):
            im.putpixel((x, y), pal.get(ch, (0, 0, 0, 0)))
    return im

def generate():
    out_dir = r'Assets/Art/Sprites'
    res_dir = r'Assets/Resources/Sprites'
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(res_dir, exist_ok=True)

    car_img = make_car_pickup()
    bike_img = make_motorbike()

    # Save sprites
    sprites = {
        'spr_vehicle_car.png': car_img,
        'spr_vehicle_pickup.png': car_img,
        'spr_vehicle_motorbike.png': bike_img,
    }

    for filename, img in sprites.items():
        p1 = os.path.join(out_dir, filename)
        p2 = os.path.join(res_dir, filename)
        img.save(p1)
        img.save(p2)

        g1 = uuid.uuid5(uuid.NAMESPACE_DNS, 'art_' + filename).hex
        g2 = uuid.uuid5(uuid.NAMESPACE_DNS, 'res_' + filename).hex

        with open(p1 + '.meta', 'w', encoding='utf-8') as mf:
            mf.write(get_meta(g1))
        with open(p2 + '.meta', 'w', encoding='utf-8') as mf:
            mf.write(get_meta(g2))

        print(f'Generated {filename} -> GUID: {g1[:8]}')

if __name__ == '__main__':
    generate()
