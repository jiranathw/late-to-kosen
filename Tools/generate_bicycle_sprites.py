#!/usr/bin/env python3
"""
Generates 32x32 retro 8-bit Anywheel Lime-Green Bicycle sprites:
1. bicycle.png             - Parked Anywheel green bicycle with front basket & lock
2. player_ride_1.png       - Student riding Anywheel bike (pedal frame 1)
3. player_ride_2.png       - Student riding Anywheel bike (pedal frame 2)
4. player_ride_3.png       - Student riding Anywheel bike (pedal frame 3)
5. player_ride_4.png       - Student riding Anywheel bike (pedal frame 4)
6. player_ride_idle.png    - Student idling on Anywheel bike
7. player_ride_jump.png    - Student bunny-hopping on Anywheel bike in mid-air
"""

import os
import uuid
from PIL import Image

def build_palette():
    return {
        '.': (0, 0, 0, 0),             # Transparent
        'k': (15, 23, 42, 255),         # Dark outline / frame black
        'g': (120, 204, 25, 255),       # Anywheel lime green
        'G': (154, 235, 45, 255),       # Anywheel bright green highlight
        'd': (85, 150, 15, 255),        # Anywheel dark green shadow
        'w': (240, 245, 250, 255),      # White / Silver spokes & uniform shirt
        's': (148, 163, 184, 255),      # Silver spoke highlight
        't': (30, 41, 59, 255),         # Tire dark charcoal
        'b': (15, 20, 30, 255),         # Saddle / Basket / Chaincase
        'r': (239, 68, 68, 255),        # Red rear reflector
        'y': (250, 204, 21, 255),       # Yellow wheel reflector
        # Student colors
        'H': (20, 20, 25, 255),         # Hair
        'S': (255, 218, 185, 255),      # Skin tone
        'U': (255, 255, 255, 255),      # Uniform shirt
        'P': (30, 45, 75, 255),         # Dark navy student shorts/pants
        'L': (220, 180, 150, 255),      # Shaded skin / legs
        'X': (10, 15, 25, 255),         # Shoes / student outline
    }

def parse_grid(lines, pal):
    im = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    for y, line in enumerate(lines):
        if y >= 32: break
        for x, ch in enumerate(line):
            if x >= 32: break
            im.putpixel((x, y), pal.get(ch, (0, 0, 0, 0)))
    return im

def make_bicycle_sprite(pal):
    # 32x32 Parked Anywheel Bicycle
    grid = [
        "................................", # 0
        "................................", # 1
        "................................", # 2
        "................................", # 3
        "................................", # 4
        "................................", # 5
        "................................", # 6
        "................................", # 7
        ".....................kbkb.......", # 8 Handlebar & basket top
        "..........kb.........kbkbbk.....", # 9 Saddle & basket
        "..........kb.........kbbbbk.....", # 10 Seatpost & basket
        "...........k.........kbkbbk.....", # 11
        "...........kg........kkgkk......", # 12 Fork & Head tube
        "...........kg........kg.........", # 13
        "...........kgg......kgk.........", # 14 Step-through frame curve
        "............kgg....kgg..........", # 15
        ".....kkkk....kgggggGk...kkkk....", # 16 Frame to bottom bracket & front fork
        "...kktbttkk...kggggk..kktbttkk..", # 17 Mudguards
        "..ktwwwwwwtk...kgbkg.ktwwwwwwtk.", # 18 Wheels
        ".ktwwwwywwwtk.kbbbbkktwwwwywwwtk", # 19 Chaincase & reflectors
        ".ktwwswwwswtk.kbgbgkktwwswwwswtk", # 20
        ".ktwwswwwswtk..kbbk..ktwwswwwswtk", # 21
        ".ktwwwwswwwtk...kk...ktwwwwswwwtk", # 22
        ".ktwwwwswwwtk........ktwwwwswwwtk", # 23
        "..ktwwwwwwtk..........ktwwwwwwtk.", # 24
        "...kttttttk............kttttttk.", # 25
        ".....kkkk................kkkk...", # 26 Tires bottom
        "................................", # 27
        "................................", # 28
        "................................", # 29
        "................................", # 30
        "................................", # 31
    ]
    return parse_grid(grid, pal)

def make_player_ride_1(pal):
    # Frame 1: Right pedal down, left pedal up
    grid = [
        "................................", # 0
        "................................", # 1
        "................................", # 2
        "........HHHHX...................", # 3 Student Hair
        ".......HHHHHXX..................", # 4
        ".......HHHSSSXX........kbkb.....", # 5 Student Face & Basket top
        ".......HHSSSXSX........kbkbbk...", # 6
        ".......HHSSSSXX........kbbbbk...", # 7
        ".......XXXXSSSSXX......kbkbbk...", # 8
        "......XXXXXXUSSSUXX....kkgkk....", # 9 Uniform Shirt & Arms holding bars
        "......XXXXXXUUUUUUUXX..kg.......", # 10
        ".......XXXXXUUUUUUUUXXkgk.......", # 11
        "........XXXXPPPPPUUUUUXg........", # 12 Navy Shorts
        ".........XXPPPPPPPXXXXg.........", # 13
        "..........XPPXXPPPXXkg..........", # 14 Right leg down
        "..........XPX..XPPX.kgggggGk....", # 15
        ".....kkkk.XLSX..XLSX..kggk..kkkk", # 16 Frame & Mudguards
        "...kktbttkkXLSX..XLSX......kktbttkk", # 17 Legs pedaling down
        "..ktwwwwwwtkXHX...XHX.....ktwwwwwwtk", # 18 Shoe on pedal
        ".ktwwwwywwwtXXXX..XXXX...ktwwwwywwwtk", # 19
        ".ktwwswwwswtk.kbgbgk.....ktwwswwwswtk", # 20
        ".ktwwswwwswtk..kbbk......ktwwswwwswtk", # 21
        ".ktwwwwswwwtk...kk.......ktwwwwswwwtk", # 22
        ".ktwwwwswwwtk............ktwwwwswwwtk", # 23
        "..ktwwwwwwtk..............ktwwwwwwtk.", # 24
        "...kttttttk................kttttttk.", # 25
        ".....kkkk....................kkkk...", # 26
        "................................", # 27
        "................................", # 28
        "................................", # 29
        "................................", # 30
        "................................", # 31
    ]
    return parse_grid(grid, pal)

def make_player_ride_2(pal):
    # Frame 2: Pedals passing horizontal
    grid = [
        "................................", # 0
        "................................", # 1
        "................................", # 2
        "........HHHHX...................", # 3
        ".......HHHHHXX..................", # 4
        ".......HHHSSSXX........kbkb.....", # 5
        ".......HHSSSXSX........kbkbbk...", # 6
        ".......HHSSSSXX........kbbbbk...", # 7
        ".......XXXXSSSSXX......kbkbbk...", # 8
        "......XXXXXXUSSSUXX....kkgkk....", # 9
        "......XXXXXXUUUUUUUXX..kg.......", # 10
        ".......XXXXXUUUUUUUUXXkgk.......", # 11
        "........XXXXPPPPPUUUUUXg........", # 12
        ".........XXPPPPPPPXXXXg.........", # 13
        "..........XPPPPPPPXXkg..........", # 14 Legs midpoint
        "..........XPXX.XPPX.kgggggGk....", # 15
        ".....kkkk.XLSX..XLSX..kggk..kkkk", # 16
        "...kktbttkkXLSX.XLSX.......kktbttkk", # 17
        "..ktwswswwtkXHX.XHX.......ktwswswwtk", # 18 Rotating spokes
        ".ktwswywwswtkXXXXXXX.....ktwswywwswtk", # 19
        ".ktwwwwwwwwtk.kbgbgk.....ktwwwwwwwwtk", # 20
        ".ktwswswswwtk..kbbk......ktwswswswwtk", # 21
        ".ktwwwwwwwwtk...kk.......ktwwwwwwwwtk", # 22
        ".ktwswswswwtk............ktwswswswwtk", # 23
        "..ktwwwwwwtk..............ktwwwwwwtk.", # 24
        "...kttttttk................kttttttk.", # 25
        ".....kkkk....................kkkk...", # 26
        "................................", # 27
        "................................", # 28
        "................................", # 29
        "................................", # 30
        "................................", # 31
    ]
    return parse_grid(grid, pal)

def make_player_ride_3(pal):
    # Frame 3: Left pedal down, right pedal up
    grid = [
        "................................", # 0
        "................................", # 1
        "................................", # 2
        "........HHHHX...................", # 3
        ".......HHHHHXX..................", # 4
        ".......HHHSSSXX........kbkb.....", # 5
        ".......HHSSSXSX........kbkbbk...", # 6
        ".......HHSSSSXX........kbbbbk...", # 7
        ".......XXXXSSSSXX......kbkbbk...", # 8
        "......XXXXXXUSSSUXX....kkgkk....", # 9
        "......XXXXXXUUUUUUUXX..kg.......", # 10
        ".......XXXXXUUUUUUUUXXkgk.......", # 11
        "........XXXXPPPPPUUUUUXg........", # 12
        ".........XXPPPPPPPXXXXg.........", # 13
        "..........XPPPXXPPXXkg..........", # 14 Left leg down
        "..........XPPX..XPX.kgggggGk....", # 15
        ".....kkkk..XLSX.XLSX..kggk..kkkk", # 16
        "...kktbttkk.XLSXXLSX.......kktbttkk", # 17
        "..ktwwwwwwtk.XHX.XHX......ktwwwwwwtk", # 18
        ".ktwwwwywwwtkXXXX.XXXX...ktwwwwywwwtk", # 19
        ".ktwwswwwswtk.kbgbgk.....ktwwswwwswtk", # 20
        ".ktwwswwwswtk..kbbk......ktwwswwwswtk", # 21
        ".ktwwwwswwwtk...kk.......ktwwwwswwwtk", # 22
        ".ktwwwwswwwtk............ktwwwwswwwtk", # 23
        "..ktwwwwwwtk..............ktwwwwwwtk.", # 24
        "...kttttttk................kttttttk.", # 25
        ".....kkkk....................kkkk...", # 26
        "................................", # 27
        "................................", # 28
        "................................", # 29
        "................................", # 30
        "................................", # 31
    ]
    return parse_grid(grid, pal)

def make_player_ride_4(pal):
    # Frame 4: Pedals passing horizontal opposite
    return make_player_ride_2(pal)

def make_player_ride_jump(pal):
    # Mid-air jump / bunny hop pose
    grid = [
        "................................", # 0
        "................................", # 1
        "........HHHHX...................", # 2
        ".......HHHHHXX..................", # 3 Hair windblown
        "......HHHHHHXXX........kbkb.....", # 4
        ".......HHHSSSXX........kbkbbk...", # 5
        ".......HHSSSXSX........kbbbbk...", # 6
        ".......HHSSSSXX........kbkbbk...", # 7
        ".......XXXXSSSSXX......kkgkk....", # 8
        "......XXXXXXUSSSUXX....kg.......", # 9 Leaning forward intensely
        "......XXXXXXUUUUUUUXX..kgk......", # 10
        ".......XXXXXUUUUUUUUXX.kg.......", # 11
        "........XXXXPPPPPUUUUUXg........", # 12
        ".........XXPPPPPPPXXXXg.........", # 13
        "..........XPPPPPPPXXkg..........", # 14 Legs tucked for jump
        "..........XPXX..XPX.kgggggGk....", # 15
        ".....kkkk.XLSX..XLSX..kggk..kkkk", # 16
        "...kktbttkkXHX...XHX.......kktbttkk", # 17
        "..ktwswswwtkXXXX.XXXX.....ktwswswwtk", # 18
        ".ktwswywwswtk.kbgbgk.....ktwswywwswtk", # 19
        ".ktwwwwwwwwtk..kbbk......ktwwwwwwwwtk", # 20
        ".ktwswswswwtk...kk.......ktwswswswwtk", # 21
        ".ktwwwwwwwwtk............ktwwwwwwwwtk", # 22
        ".ktwswswswwtk............ktwswswswwtk", # 23
        "..ktwwwwwwtk..............ktwwwwwwtk.", # 24
        "...kttttttk................kttttttk.", # 25
        ".....kkkk....................kkkk...", # 26
        "................................", # 27
        "................................", # 28
        "................................", # 29
        "................................", # 30
        "................................", # 31
    ]
    return parse_grid(grid, pal)

def save_sprites():
    pal = build_palette()
    out_dir = r'Assets/Art/Sprites'
    res_dir = r'Assets/Resources/Sprites'
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(res_dir, exist_ok=True)

    sprites = {
        'bicycle.png': make_bicycle_sprite(pal),
        'player_ride_1.png': make_player_ride_1(pal),
        'player_ride_2.png': make_player_ride_2(pal),
        'player_ride_3.png': make_player_ride_3(pal),
        'player_ride_4.png': make_player_ride_4(pal),
        'player_ride_idle.png': make_player_ride_1(pal),
        'player_ride_jump.png': make_player_ride_jump(pal),
    }

    meta_template = '''fileFormatVersion: 2
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

    for filename, img in sprites.items():
        p1 = os.path.join(out_dir, filename)
        p2 = os.path.join(res_dir, filename)
        img.save(p1)
        img.save(p2)

        g1 = uuid.uuid5(uuid.NAMESPACE_DNS, 'art_' + filename).hex
        g2 = uuid.uuid5(uuid.NAMESPACE_DNS, 'res_' + filename).hex

        with open(p1 + '.meta', 'w', encoding='utf-8') as mf:
            mf.write(meta_template.format(guid=g1))
        with open(p2 + '.meta', 'w', encoding='utf-8') as mf:
            mf.write(meta_template.format(guid=g2))

        print(f'Generated {filename} -> GUIDs: {g1[:8]} / {g2[:8]}')

if __name__ == '__main__':
    save_sprites()
