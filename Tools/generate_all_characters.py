#!/usr/bin/env python3
"""
Generates complete 8-bit sprite sets for all 3 KOSEN Student Characters:
- Character 0: Formal School Uniform (White shirt, Orange/Blue striped tie, Navy pants)
- Character 1: PE Sport Uniform (Orange polo, Blue collar, Black sweatpants with purple stripe)
- Character 2: Workshop / Shop Uniform (Dark Navy shirt with purple stripe & grey undershirt, Navy pants)

For each character (0, 1, 2):
  - idle.png (32x32)
  - run_1..4.png (32x32)
  - jump.png (32x32)
  - dead.png (32x32)
  - ride_1..4.png (32x32)
  - ride_idle.png (32x32)
  - ride_jump.png (32x32)
  - portrait.png (64x64 or 48x48)
"""

import os
import uuid
from PIL import Image

def get_character_palettes():
    # Common palette
    c_trans = (0, 0, 0, 0)
    c_black = (15, 23, 42, 255)         # Outline
    c_hair = (25, 20, 30, 255)          # Dark student hair
    c_hair_hl = (55, 45, 65, 255)       # Hair highlight
    c_skin = (255, 220, 188, 255)       # Skin
    c_skin_shadow = (225, 180, 150, 255)# Skin shadow
    c_shoe_black = (10, 15, 25, 255)    # Black shoe
    c_star_yellow = (250, 204, 21, 255) # Dizzy star yellow

    # Anywheel Bike colors
    c_bike_lime = (132, 204, 22, 255)
    c_bike_lime_hl = (163, 230, 53, 255)
    c_tire = (30, 41, 59, 255)
    c_spoke = (226, 232, 240, 255)
    c_spoke_dark = (148, 163, 184, 255)
    c_refl_yellow = (250, 204, 21, 255)
    c_refl_red = (239, 68, 68, 255)
    c_guard = (15, 20, 30, 255)

    palettes = {}

    # === Character 0: Formal Uniform ===
    palettes[0] = {
        '.': c_trans, 'k': c_black, 'H': c_hair, 'h': c_hair_hl,
        'S': c_skin, 's': c_skin_shadow, 'X': c_shoe_black, 'Y': c_star_yellow,
        # Shirt & Tie
        'T': (255, 255, 255, 255),       # White shirt
        't': (220, 225, 235, 255),       # Shirt shadow
        'O': (249, 115, 22, 255),        # Orange tie stripe
        'B': (2, 132, 199, 255),         # Blue tie stripe
        'e': (15, 23, 42, 255),          # Black belt
        # Pants
        'P': (30, 58, 138, 255),         # Navy trousers
        'p': (23, 37, 84, 255),          # Navy shadow
        # Bike
        'G': c_bike_lime_hl, 'g': c_bike_lime, 'M': c_tire, 'w': c_spoke,
        'D': c_spoke_dark, 'y': c_refl_yellow, 'r': c_refl_red, 'b': c_guard
    }

    # === Character 1: PE Sport (Orange Polo + Black/Purple sweatpants) ===
    palettes[1] = {
        '.': c_trans, 'k': c_black, 'H': c_hair, 'h': c_hair_hl,
        'S': c_skin, 's': c_skin_shadow, 'X': c_shoe_black, 'Y': c_star_yellow,
        # Shirt & Collar
        'T': (249, 115, 22, 255),        # Bright orange polo
        't': (234, 88, 12, 255),         # Orange shadow
        'O': (255, 255, 255, 255),       # White button / logo
        'B': (2, 132, 199, 255),         # Blue collar
        'e': (168, 85, 247, 255),        # Purple sleeve accent
        # Pants
        'P': (24, 24, 27, 255),          # Black sweatpants
        'p': (168, 85, 247, 255),        # Purple side stripe
        # Bike
        'G': c_bike_lime_hl, 'g': c_bike_lime, 'M': c_tire, 'w': c_spoke,
        'D': c_spoke_dark, 'y': c_refl_yellow, 'r': c_refl_red, 'b': c_guard
    }

    # === Character 2: Workshop Shop Shirt (Dark Navy with Purple line + Navy pants) ===
    palettes[2] = {
        '.': c_trans, 'k': c_black, 'H': c_hair, 'h': c_hair_hl,
        'S': c_skin, 's': c_skin_shadow, 'X': c_shoe_black, 'Y': c_star_yellow,
        # Shirt & Accents
        'T': (30, 41, 75, 255),          # Dark navy shop shirt
        't': (20, 28, 55, 255),          # Dark navy shadow
        'O': (240, 245, 250, 255),       # White button line / stitch
        'B': (156, 163, 175, 255),       # Grey undershirt at collar
        'e': (192, 38, 211, 255),        # Purple vertical chest stripe
        # Pants
        'P': (25, 35, 65, 255),          # Workshop pants
        'p': (18, 24, 48, 255),          # Dark pants shadow
        # Bike
        'G': c_bike_lime_hl, 'g': c_bike_lime, 'M': c_tire, 'w': c_spoke,
        'D': c_spoke_dark, 'y': c_refl_yellow, 'r': c_refl_red, 'b': c_guard
    }

    return palettes

def render_grid(grid_lines, pal):
    im = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    for y, line in enumerate(grid_lines):
        if y >= 32: break
        for x, ch in enumerate(line):
            if x >= 32: break
            im.putpixel((x, y), pal.get(ch, (0, 0, 0, 0)))
    return im

def build_idle_grid():
    return [
        "................................", # 0
        "................................", # 1
        ".............kkkkk..............", # 2
        "............kHHHhkk.............", # 3
        "...........kHHHHHhkk............", # 4
        "...........kHHHSSSSk............", # 5
        "..........kHHHSSkSxk............", # 6
        "..........kHHSSSkSxk............", # 7
        "..........kHHSSSSSSk............", # 8
        "...........kHHSSBkk.............", # 9 Collar / Neck
        "..........kkkTTBTk..............", # 10 Shirt top with collar
        ".........kkPTTTOTTk.............", # 11
        "........kkkkTTTeTTk.............", # 12
        "........kkkkTTTOTkk.............", # 13
        "........kkkkTTTeTTk.............", # 14
        ".........kkkTTTTTkk.............", # 15
        "..........kkkeeeekk.............", # 16 Belt
        "............kPPPPk..............", # 17 Pants top
        "............kPpPPk..............", # 18
        "............kPpPPk..............", # 19
        "............kPpPPk..............", # 20
        "............kPk.kPk.............", # 21
        "............kPk.kPk.............", # 22
        "............kPk.kPk.............", # 23
        "............kSk.kSk.............", # 24 Ankle / sock
        "............kXk.kXk.............", # 25 Shoes
        "............kXXkkXXk............", # 26
        ".............kk..kk.............", # 27
        "................................", # 28
        "................................", # 29
        "................................", # 30
        "................................", # 31
    ]

def build_run_grid_1():
    return [
        "................................", # 0
        "................................", # 1
        ".............kkkkk..............", # 2
        "............kHHHhkk.............", # 3
        "...........kHHHHHhkk............", # 4
        "...........kHHHSSSSk............", # 5
        "..........kHHHSSkSxk............", # 6
        "..........kHHSSSkSxk............", # 7
        "..........kHHSSSSSSk............", # 8
        "...........kHHSSBkk.............", # 9
        "..........kkkTTBTk..............", # 10
        ".........kkkTTTOTTk.............", # 11
        "........kSSkTTTeTTk.............", # 12 Arm swinging forward
        "........kSSkTTTOTkk.............", # 13
        "........kkkkTTTeTTk.............", # 14
        ".........kkkTTTTTkk.............", # 15
        "..........kkkeeeekk.............", # 16
        "............kPPPPk..............", # 17
        "...........kPpPPk...............", # 18 Leg stride forward
        "..........kPpPk.kPpPk...........", # 19 Leg stride back
        "..........kPk....kPPk...........", # 20
        ".........kPk......kXk...........", # 21
        ".........kSk.......kk...........", # 22
        "........kXXk....................", # 23 Foot landing
        ".........kk.....................", # 24
        "................................", # 25
        "................................", # 26
        "................................", # 27
        "................................", # 28
        "................................", # 29
        "................................", # 30
        "................................", # 31
    ]

def build_run_grid_2():
    return [
        "................................", # 0
        "................................", # 1
        ".............kkkkk..............", # 2
        "............kHHHhkk.............", # 3
        "...........kHHHHHhkk............", # 4
        "...........kHHHSSSSk............", # 5
        "..........kHHHSSkSxk............", # 6
        "..........kHHSSSkSxk............", # 7
        "..........kHHSSSSSSk............", # 8
        "...........kHHSSBkk.............", # 9
        "..........kkkTTBTk..............", # 10
        ".........kkPTTTOTTk.............", # 11
        "........kkkkTTTeTTk.............", # 12
        "........kkkkTTTOTkk.............", # 13
        "........kkkkTTTeTTk.............", # 14
        ".........kkkTTTTTkk.............", # 15
        "..........kkkeeeekk.............", # 16
        "............kPPPPk..............", # 17
        "............kPpPPk..............", # 18 Passing stride
        "............kPpPPk..............", # 19
        "...........kPk..kPk.............", # 20
        "...........kPk...kPk............", # 21
        "...........kSk...kSk............", # 22
        "..........kXXk...kXXk...........", # 23
        "...........kk.....kk............", # 24
        "................................", # 25
        "................................", # 26
        "................................", # 27
        "................................", # 28
        "................................", # 29
        "................................", # 30
        "................................", # 31
    ]

def build_run_grid_3():
    return [
        "................................", # 0
        "................................", # 1
        ".............kkkkk..............", # 2
        "............kHHHhkk.............", # 3
        "...........kHHHHHhkk............", # 4
        "...........kHHHSSSSk............", # 5
        "..........kHHHSSkSxk............", # 6
        "..........kHHSSSkSxk............", # 7
        "..........kHHSSSSSSk............", # 8
        "...........kHHSSBkk.............", # 9
        "..........kkkTTBTk..............", # 10
        ".........kkkTTTOTTk.............", # 11
        "........kSSkTTTeTTk.............", # 12
        "........kSSkTTTOTkk.............", # 13
        "........kkkkTTTeTTk.............", # 14
        ".........kkkTTTTTkk.............", # 15
        "..........kkkeeeekk.............", # 16
        "............kPPPPk..............", # 17
        "...........kPpPPk...............", # 18 Leg stride opposite
        "..........kPpPk..kPpPk..........", # 19
        ".........kPPk.....kPk...........", # 20
        ".........kXk.......kPk..........", # 21
        "..........kk.......kSk..........", # 22
        "..................kXXk..........", # 23
        "...................kk...........", # 24
        "................................", # 25
        "................................", # 26
        "................................", # 27
        "................................", # 28
        "................................", # 29
        "................................", # 30
        "................................", # 31
    ]

def build_jump_grid():
    return [
        "................................", # 0
        ".............kkkkk..............", # 1
        "............kHHHhkk.............", # 2
        "...........kHHHHHhkk............", # 3 Hair flowing
        "...........kHHHSSSSk............", # 4
        "..........kHHHSSkSxk............", # 5
        "..........kHHSSSkSxk............", # 6
        "..........kHHSSSSSSk............", # 7
        "...........kHHSSBkk.............", # 8
        "..........kkkTTBTk..............", # 9
        ".........kkkTTTOTTk.............", # 10
        "........kSSkTTTeTTk.............", # 11 Arms raised slightly
        "........kSSkTTTOTkk.............", # 12
        "........kkkkTTTeTTk.............", # 13
        ".........kkkTTTTTkk.............", # 14
        "..........kkkeeeekk.............", # 15
        "............kPPPPk..............", # 16 Legs tucked in air
        "...........kPpPPpPk.............", # 17
        "..........kPpPk.kPpPk...........", # 18
        "..........kPk.....kPk...........", # 19
        "..........kSk.....kSk...........", # 20
        ".........kXXk.....kXXk..........", # 21
        "..........kk.......kk...........", # 22
        "................................", # 23
        "................................", # 24
        "................................", # 25
        "................................", # 26
        "................................", # 27
        "................................", # 28
        "................................", # 29
        "................................", # 30
        "................................", # 31
    ]

def build_dead_grid():
    return [
        "................................", # 0
        "................................", # 1
        "................................", # 2
        "................................", # 3
        "..................YYY...YYY.....", # 4 Dizzy stars
        "...................Y.....Y......", # 5
        ".................YYYYY.YYYYY....", # 6
        "...................Y.....Y......", # 7
        "..................YYY...YYY.....", # 8
        "................................", # 9
        "................................", # 10
        "................................", # 11
        "................................", # 12
        "................................", # 13
        "................................", # 14
        "................................", # 15
        "................................", # 16
        "................................", # 17
        "................................", # 18
        "................................", # 19
        "................................", # 20
        "................................", # 21
        "................................", # 22
        "................................", # 23
        ".....kkkkkkkk...................", # 24 Hair & Face flat
        "...kkHHHHHhSSkk...kkk...........", # 25 X X eyes
        "..kHHHkXkSSkXkSkkTTTTkkk.kk.....", # 26 Shirt on floor
        "..kHHHkXkSSkXkSkkTTBOTTkPPPPkk..", # 27 Tie / Shirt / Pants
        "...kkkSSSSSSSSkkkTTTeTTkPpPPpPkk", # 28
        ".....kkkSSSSkk...kkeeekkkXXXXXXk", # 29 Shoes flat
        "........kkkk.......kkk....kkkk..", # 30
        "................................", # 31
    ]

def build_ride_grid_1():
    # Student riding Anywheel green bicycle
    return [
        "................................", # 0
        "................................", # 1
        "................................", # 2
        "........HHHHk...................", # 3 Student Head
        ".......HHHHHkk..................", # 4
        ".......HHHSSSkk........kbkb.....", # 5 Face & Basket
        ".......HHSSSkSxk.......kbkbbk...", # 6
        ".......HHSSSSkk........kbbbbk...", # 7
        ".......kkkkSSSSkk......kbkbbk...", # 8
        "......kkkkkkTSSSTkk....kkgkk....", # 9 Uniform Shirt & Arms holding bars
        "......kkkkkkTTBTTTTkk..kg.......", # 10
        ".......kkkkkTTTeTTTTkkgk........", # 11
        "........kkkkPPeePTTTTkg.........", # 12 Belt & Shorts
        ".........kkPPPPPPPkkkkg.........", # 13
        "..........kPpkkPpPkkkg..........", # 14 Leg pedaling down
        "..........kPk..kPpkkgggggGk.....", # 15
        ".....kkkk.kSk...kSk...kggk..kkkk", # 16
        "...kktMttkkSk...kSk........kktMttkk", # 17
        "..kMwwwwwwMkXk..kXk.......kMwwwwwwMk", # 18 Shoe on pedal
        ".kMwwwwywwwMkk..kk.......kMwwwwywwwMk", # 19
        ".kMwwDwwwDwwMk.kbgbgk....kMwwDwwwDwwMk", # 20
        ".kMwwDwwwDwwMk..kbbk.....kMwwDwwwDwwMk", # 21
        ".kMwwwwDwwwDk....kk......kMwwwwDwwwDk.", # 22
        ".kMwwwwDwwwDk............kMwwwwDwwwDk.", # 23
        "..kMwwwwwwMk..............kMwwwwwwMk.", # 24
        "...kMtttttMk................kMtttttMk.", # 25
        ".....kkkk....................kkkk...", # 26
        "................................", # 27
        "................................", # 28
        "................................", # 29
        "................................", # 30
        "................................", # 31
    ]

def build_ride_grid_2():
    return [
        "................................", # 0
        "................................", # 1
        "................................", # 2
        "........HHHHk...................", # 3
        ".......HHHHHkk..................", # 4
        ".......HHHSSSkk........kbkb.....", # 5
        ".......HHSSSkSxk.......kbkbbk...", # 6
        ".......HHSSSSkk........kbbbbk...", # 7
        ".......kkkkSSSSkk......kbkbbk...", # 8
        "......kkkkkkTSSSTkk....kkgkk....", # 9
        "......kkkkkkTTBTTTTkk..kg.......", # 10
        ".......kkkkkTTTeTTTTkkgk........", # 11
        "........kkkkPPeePTTTTkg.........", # 12
        ".........kkPPPPPPPkkkkg.........", # 13
        "..........kPPPPPPPkkkg..........", # 14 Midpoint
        "..........kPkk.kPpkkgggggGk.....", # 15
        ".....kkkk.kSk...kSk...kggk..kkkk", # 16
        "...kktMttkkSk...kSk........kktMttkk", # 17
        "..kMwDwDwwMkXk..kXk.......kMwDwDwwMk", # 18 Rotating spokes
        ".kMwDwywwDwwkk..kk.......kMwDwywwDwwMk", # 19
        ".kMwwwwwwwwwMk.kbgbgk....kMwwwwwwwwwMk", # 20
        ".kMwDwDwDwwwMk..kbbk.....kMwDwDwDwwwMk", # 21
        ".kMwwwwwwwwwk....kk......kMwwwwwwwwwk.", # 22
        ".kMwDwDwDwwwk............kMwDwDwDwwwk.", # 23
        "..kMwwwwwwMk..............kMwwwwwwMk.", # 24
        "...kMtttttMk................kMtttttMk.", # 25
        ".....kkkk....................kkkk...", # 26
        "................................", # 27
        "................................", # 28
        "................................", # 29
        "................................", # 30
        "................................", # 31
    ]

def build_ride_grid_3():
    return [
        "................................", # 0
        "................................", # 1
        "................................", # 2
        "........HHHHk...................", # 3
        ".......HHHHHkk..................", # 4
        ".......HHHSSSkk........kbkb.....", # 5
        ".......HHSSSkSxk.......kbkbbk...", # 6
        ".......HHSSSSkk........kbbbbk...", # 7
        ".......kkkkSSSSkk......kbkbbk...", # 8
        "......kkkkkkTSSSTkk....kkgkk....", # 9
        "......kkkkkkTTBTTTTkk..kg.......", # 10
        ".......kkkkkTTTeTTTTkkgk........", # 11
        "........kkkkPPeePTTTTkg.........", # 12
        ".........kkPPPPPPPkkkkg.........", # 13
        "..........kPpkkPpPkkkg..........", # 14
        "..........kPp..kPkkkgggggGk.....", # 15
        ".....kkkk..kSk..kSk...kggk..kkkk", # 16
        "...kktMttkk.kSk.kSk........kktMttkk", # 17
        "..kMwwwwwwMk.kXkkXk.......kMwwwwwwMk", # 18
        ".kMwwwwywwwMk.kk.kk......kMwwwwywwwMk", # 19
        ".kMwwDwwwDwwMk.kbgbgk....kMwwDwwwDwwMk", # 20
        ".kMwwDwwwDwwMk..kbbk.....kMwwDwwwDwwMk", # 21
        ".kMwwwwDwwwDk....kk......kMwwwwDwwwDk.", # 22
        ".kMwwwwDwwwDk............kMwwwwDwwwDk.", # 23
        "..kMwwwwwwMk..............kMwwwwwwMk.", # 24
        "...kMtttttMk................kMtttttMk.", # 25
        ".....kkkk....................kkkk...", # 26
        "................................", # 27
        "................................", # 28
        "................................", # 29
        "................................", # 30
        "................................", # 31
    ]

def build_ride_jump_grid():
    return [
        "................................", # 0
        "................................", # 1
        "........HHHHk...................", # 2
        ".......HHHHHkk..................", # 3
        "......HHHHHHkkk........kbkb.....", # 4
        ".......HHHSSSkk........kbkbbk...", # 5
        ".......HHSSSkSxk.......kbbbbk...", # 6
        ".......HHSSSSkk........kbkbbk...", # 7
        ".......kkkkSSSSkk......kkgkk....", # 8
        "......kkkkkkTSSSTkk....kg.......", # 9 Leaning forward
        "......kkkkkkTTBTTTTkk..kgk......", # 10
        ".......kkkkkTTTeTTTTkk.kg.......", # 11
        "........kkkkPPeePTTTTkg.........", # 12
        ".........kkPPPPPPPkkkkg.........", # 13
        "..........kPPPPPPPkkkg..........", # 14 Tucked jump
        "..........kPkk..kPkkgggggGk.....", # 15
        ".....kkkk.kSk...kSk...kggk..kkkk", # 16
        "...kktMttkkXk....Xk........kktMttkk", # 17
        "..kMwDwDwwMkkk..kkk.......kMwDwDwwMk", # 18
        ".kMwDwywwDwwMk.kbgbgk....kMwDwywwDwwMk", # 19
        ".kMwwwwwwwwwMk..kbbk.....kMwwwwwwwwwMk", # 20
        ".kMwDwDwDwwwMk...kk......kMwDwDwDwwwMk", # 21
        ".kMwwwwwwwwwk............kMwwwwwwwwwk.", # 22
        ".kMwDwDwDwwwk............kMwDwDwDwwwk.", # 23
        "..kMwwwwwwMk..............kMwwwwwwMk.", # 24
        "...kMtttttMk................kMtttttMk.", # 25
        ".....kkkk....................kkkk...", # 26
        "................................", # 27
        "................................", # 28
        "................................", # 29
        "................................", # 30
        "................................", # 31
    ]

def make_meta(guid):
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

def generate_all():
    palettes = get_character_palettes()
    out_dir = r'Assets/Art/Sprites'
    res_dir = r'Assets/Resources/Sprites'
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(res_dir, exist_ok=True)

    grids = {
        'idle': build_idle_grid(),
        'run_1': build_run_grid_1(),
        'run_2': build_run_grid_2(),
        'run_3': build_run_grid_3(),
        'run_4': build_run_grid_2(),
        'jump': build_jump_grid(),
        'dead': build_dead_grid(),
        'ride_1': build_ride_grid_1(),
        'ride_2': build_ride_grid_2(),
        'ride_3': build_ride_grid_3(),
        'ride_4': build_ride_grid_2(),
        'ride_idle': build_ride_grid_1(),
        'ride_jump': build_ride_jump_grid(),
    }

    for char_idx in [0, 1, 2]:
        pal = palettes[char_idx]
        for name, grid in grids.items():
            img = render_grid(grid, pal)

            filename = f"char_{char_idx}_{name}.png"
            p1 = os.path.join(out_dir, filename)
            p2 = os.path.join(res_dir, filename)
            img.save(p1)
            img.save(p2)

            g1 = uuid.uuid5(uuid.NAMESPACE_DNS, 'art_' + filename).hex
            g2 = uuid.uuid5(uuid.NAMESPACE_DNS, 'res_' + filename).hex

            with open(p1 + '.meta', 'w', encoding='utf-8') as mf:
                mf.write(make_meta(g1))
            with open(p2 + '.meta', 'w', encoding='utf-8') as mf:
                mf.write(make_meta(g2))

        # Also overwrite the default player sprites with character 0 by default!
        if char_idx == 0:
            default_map = {
                'player_idle.png': grids['idle'],
                'player_run_1.png': grids['run_1'],
                'player_run_2.png': grids['run_2'],
                'player_run_3.png': grids['run_3'],
                'player_run_4.png': grids['run_4'],
                'player_jump.png': grids['jump'],
                'player_dead.png': grids['dead'],
                'player_ride_1.png': grids['ride_1'],
                'player_ride_2.png': grids['ride_2'],
                'player_ride_3.png': grids['ride_3'],
                'player_ride_4.png': grids['ride_4'],
                'player_ride_idle.png': grids['ride_idle'],
                'player_ride_jump.png': grids['ride_jump'],
            }
            for d_name, d_grid in default_map.items():
                d_img = render_grid(d_grid, pal)
                d_img.save(os.path.join(out_dir, d_name))
                d_img.save(os.path.join(res_dir, d_name))

    print("Successfully generated all 3 characters and their complete animation suites!")

if __name__ == '__main__':
    generate_all()
