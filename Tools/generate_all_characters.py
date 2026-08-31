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

# ---------------------------------------------------------------------------
# RIDING FRAMES
#
# These used to be hand-typed grids, and the bike rows had drifted out to 38
# characters - six columns wider than the canvas. render_grid() clips at x >= 32,
# so the front wheel was sliced off in every ride sprite the game shipped: the
# player mounted an Anywheel bike and half of it vanished.
#
# Composing them from stamps instead makes that class of bug impossible. _put()
# refuses to write outside 32x32, the wheel is one 9x9 stamp placed twice, and
# the whole bike is laid out from named coordinates (rear hub, bottom bracket,
# head tube) so the geometry stays consistent across frames.
#
# Layout, all in canvas pixels: wheels are radius 4 at (6, 25) and (25, 25),
# bottom bracket at (15, 25), saddle at y=16, handlebar at y=14. The rider sits
# on top of that, head at rows 4-9. Nothing reaches column 31 or row 30.
# ---------------------------------------------------------------------------

RIDE_SIZE = 32

def _ride_blank():
    return [['.'] * RIDE_SIZE for _ in range(RIDE_SIZE)]

def _put(g, x, y, ch):
    if 0 <= x < RIDE_SIZE and 0 <= y < RIDE_SIZE:
        g[y][x] = ch

def _stamp(g, x0, y0, rows):
    for dy, row in enumerate(rows):
        for dx, ch in enumerate(row):
            if ch != '.':
                _put(g, x0 + dx, y0 + dy, ch)

def _pixels(g, points, ch, dy=0):
    for x, y in points:
        _put(g, x, y + dy, ch)

def _limb(g, a, b, ch, dy=0):
    # Two-pixel-wide Bresenham. Thighs and shins read as sticks at one pixel.
    x0, y0 = a[0], a[1] + dy
    x1, y1 = b[0], b[1] + dy
    dx, dyy = abs(x1 - x0), abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dyy
    while True:
        _put(g, x0, y0, ch)
        _put(g, x0 + 1, y0, ch)
        if (x0, y0) == (x1, y1):
            break
        e2 = 2 * err
        if e2 > -dyy:
            err -= dyy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy

# Two spoke patterns, alternated between frames so the wheels visibly turn.
_WHEEL_CROSS = [
    "...MMM...",
    ".MM.w.MM.",
    ".M..w..M.",
    "M...w...M",
    "MwwwDwwwM",
    "M...w...M",
    ".M..w..M.",
    ".MM.w.MM.",
    "...MMM...",
]
_WHEEL_DIAG = [
    "...MMM...",
    ".MM...MM.",
    ".Mw...wM.",
    "M..w.w..M",
    "M...D...M",
    "M..w.w..M",
    ".Mw...wM.",
    ".MM...MM.",
    "...MMM...",
]

# Chainstay, seat tube, seat stay, down tube, top tube, fork, head tube.
_BIKE_FRAME = (
    [(x, 25) for x in range(7, 15)]
    + [(15, 24), (14, 23), (14, 22), (13, 21), (13, 20), (12, 19), (12, 18)]
    + [(7, 24), (8, 23), (9, 22), (10, 21), (10, 20), (11, 19), (11, 18)]
    + [(16, 24), (17, 23), (17, 22), (18, 21), (19, 20), (19, 19), (20, 18)]
    + [(x, 18) for x in range(12, 15)]
    + [(x, 17) for x in range(15, 20)]
    + [(20, 16), (21, 16), (21, 15)]
    + [(21, 17), (22, 18), (22, 19), (23, 20), (23, 21), (24, 22), (24, 23), (25, 24)]
)

_HEAD = [
    "..kkkk..",
    ".kHhHHk.",
    ".kHHHSSk",
    ".kHHSSkk",
    "..kHSSSk",
    "...kSSk.",
]

# Shoulders down to the hips. The last row is the seat of the shorts, which is
# where both legs are hung from.
_TORSO = [
    ".....kkTTTkk....",
    "....kTTTTTTkk...",
    "...kTTTTTTTTk...",
    "..kTTTTTTTTTkk..",
    "..kTTTTTTTSSSSk.",
    ".kkPPPPPkkkkkk..",
]

# Crank positions, clockwise from top, with the knee that goes with each.
_PEDAL_POSES = {
    0: ((15, 22), (17, 20)),
    1: ((18, 25), (18, 20)),
    2: ((15, 28), (17, 22)),
    3: ((12, 25), (16, 21)),
}
_HIP = (12, 16)

def _build_ride(phase, lift=0, tuck=False):
    g = _ride_blank()
    dy = -lift

    _stamp(g, 2, 21 + dy, _WHEEL_CROSS if phase % 2 == 0 else _WHEEL_DIAG)
    _stamp(g, 21, 21 + dy, _WHEEL_DIAG if phase % 2 == 0 else _WHEEL_CROSS)

    _pixels(g, _BIKE_FRAME, 'g', dy)
    _pixels(g, [(20, 14), (21, 14), (22, 14)], 'g', dy)   # handlebar
    _pixels(g, [(23, 14)], 'G', dy)                        # grip
    _pixels(g, [(24, 15)], 'y')                            # front reflector
    _pixels(g, [(10, 16), (11, 16), (12, 16), (13, 16)], 'k', dy)  # saddle
    _pixels(g, [(15, 25)], 'G', dy)                        # crank

    # Far leg first in the darker trouser shade, so the near leg reads in front.
    if tuck:
        poses = [((13, 24), (15, 20), 'p'), ((17, 24), (18, 20), 'P')]
    else:
        far = _PEDAL_POSES[(phase + 2) % 4]
        near = _PEDAL_POSES[phase % 4]
        poses = [(far[0], far[1], 'p'), (near[0], near[1], 'P')]

    for pedal, knee, ch in poses:
        _limb(g, _HIP, knee, ch, dy)
        _limb(g, knee, pedal, ch, dy)
        _put(g, pedal[0], pedal[1] + dy, 'X')
        _put(g, pedal[0] + 1, pedal[1] + dy, 'X')

    _stamp(g, 10, 10 + dy, _TORSO)
    _stamp(g, 15, 4 + dy, _HEAD)
    _pixels(g, [(23, 14)], 'G', dy)   # grip again, over the hand

    return [''.join(row) for row in g]

def build_ride_grid_1():
    return _build_ride(0)

def build_ride_grid_2():
    return _build_ride(1)

def build_ride_grid_3():
    return _build_ride(2)

def build_ride_grid_4():
    return _build_ride(3)

def build_ride_jump_grid():
    # Bike lifted three pixels off the road with the legs tucked - a bunny hop,
    # not a pedal stroke.
    return _build_ride(0, lift=3, tuck=True)


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
        'ride_4': build_ride_grid_4(),
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
