#!/usr/bin/env python3
"""Full-bleed 32x32 school-themed trap sprites for Level 2.

Each sprite paints every pixel so SpriteDrawMode.Simple stretched to the
transform matches the 1x1 local BoxCollider2D (the hitbox).
"""

import hashlib
import os

from PIL import Image

PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIRS = [
    os.path.join(PROJECT, "Assets", "Art", "Sprites"),
    os.path.join(PROJECT, "Assets", "Resources", "Sprites"),
]


def guid_for(seed: str) -> str:
    return hashlib.md5(("late-to-kosen::sprite:" + seed).encode()).hexdigest()


def px(h):
    h = h.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), 255)


def new_img():
    return Image.new("RGBA", (32, 32), (0, 0, 0, 0))


def fill(img, x0, y0, x1, y1, c):
    for y in range(y0, y1):
        for x in range(x0, x1):
            if 0 <= x < 32 and 0 <= y < 32:
                img.putpixel((x, y), c)


def outline_fill(img, body):
    """Paint a 1px dark frame on the 32x32 edge, then body on the interior."""
    O = px("0f172a")
    fill(img, 0, 0, 32, 32, O)
    fill(img, 1, 1, 31, 31, body)


O = px("0f172a")


def spr_trap_desk():
    """Long classroom desk — stretches well on wide hitboxes."""
    img = new_img()
    wood = px("b45309")
    wood_l = px("f59e0b")
    wood_d = px("78350f")
    metal = px("64748b")
    paper = px("f8fafc")
    blue = px("2563eb")
    outline_fill(img, wood)
    fill(img, 1, 1, 31, 8, wood_l)
    fill(img, 1, 8, 31, 12, wood_d)
    # legs
    fill(img, 3, 12, 7, 31, metal)
    fill(img, 25, 12, 29, 31, metal)
    fill(img, 4, 13, 6, 30, px("334155"))
    fill(img, 26, 13, 28, 30, px("334155"))
    # worksheet + pencil
    fill(img, 8, 2, 20, 7, paper)
    fill(img, 9, 3, 19, 4, px("94a3b8"))
    fill(img, 21, 2, 29, 5, blue)
    fill(img, 28, 2, 30, 5, px("facc15"))
    return img


def spr_trap_bag():
    """School backpack, edge to edge."""
    img = new_img()
    n = px("1e3a8a")
    nl = px("3b82f6")
    nd = px("172554")
    y = px("facc15")
    r = px("dc2626")
    c = px("f8fafc")
    outline_fill(img, n)
    fill(img, 1, 1, 31, 12, nl)
    fill(img, 1, 22, 31, 31, nd)
    fill(img, 4, 12, 28, 24, O)
    fill(img, 5, 13, 27, 23, nd)
    fill(img, 5, 13, 27, 16, y)
    fill(img, 14, 16, 18, 22, r)
    fill(img, 3, 1, 10, 8, nd)
    fill(img, 22, 1, 29, 8, nd)
    fill(img, 11, 1, 21, 6, c)
    fill(img, 11, 1, 13, 6, r)
    return img


def spr_trap_books():
    """Stack of textbooks."""
    img = new_img()
    outline_fill(img, px("1e293b"))
    bands = [
        (1, 1, 8, px("dc2626"), px("f8fafc")),
        (8, 8, 15, px("2563eb"), px("facc15")),
        (15, 15, 22, px("16a34a"), px("f8fafc")),
        (22, 22, 31, px("7c3aed"), px("fde68a")),
    ]
    for y0, _, y1, cover, label in bands:
        fill(img, 1, y0, 31, y1, cover)
        fill(img, 4, y0 + 2, 28, y0 + 4, label)
        fill(img, 1, y1 - 1, 31, y1, O)
    return img


def spr_trap_chalk():
    """Fallen chalk box / eraser strip — reads when flattened."""
    img = new_img()
    y = px("facc15")
    yd = px("ca8a04")
    k = px("111827")
    w = px("f8fafc")
    outline_fill(img, y)
    for x in range(1, 31):
        for yy in range(1, 31):
            img.putpixel((x, yy), y if ((x + yy) // 4) % 2 == 0 else k)
    fill(img, 6, 10, 26, 22, w)
    fill(img, 7, 11, 25, 21, px("e2e8f0"))
    fill(img, 8, 13, 24, 16, px("38bdf8"))
    fill(img, 10, 17, 22, 19, yd)
    return img


def spr_trap_globe():
    """Classroom globe on a stand."""
    img = new_img()
    ocean = px("1d4ed8")
    land = px("22c55e")
    stand = px("78716c")
    outline_fill(img, ocean)
    fill(img, 1, 24, 31, 31, stand)
    fill(img, 13, 20, 19, 25, px("a8a29e"))
    for yy in range(2, 24):
        for x in range(2, 30):
            dx, dy = x - 16, yy - 12
            if dx * dx + dy * dy <= 100:
                n = (x * 3 + yy * 5) % 7
                img.putpixel((x, yy), land if n < 3 else ocean)
            elif dx * dx + dy * dy <= 121:
                img.putpixel((x, yy), O)
    fill(img, 15, 11, 17, 13, px("f8fafc"))
    return img


def spr_trap_lunch():
    """Bento box and thermos."""
    img = new_img()
    red = px("dc2626")
    rd = px("7f1d1d")
    yel = px("facc15")
    rice = px("f8fafc")
    nori = px("14532d")
    outline_fill(img, red)
    fill(img, 1, 1, 31, 8, rd)
    fill(img, 10, 2, 22, 7, px("94a3b8"))
    fill(img, 2, 9, 30, 30, yel)
    fill(img, 4, 11, 15, 28, rice)
    fill(img, 5, 13, 14, 16, nori)
    fill(img, 17, 11, 28, 20, px("fb923c"))
    fill(img, 17, 21, 28, 28, px("4ade80"))
    return img


def spr_trap_cart():
    """Library book cart."""
    img = new_img()
    metal = px("94a3b8")
    md = px("334155")
    outline_fill(img, metal)
    fill(img, 1, 1, 31, 6, md)
    fill(img, 1, 14, 31, 18, md)
    fill(img, 1, 26, 31, 31, md)
    fill(img, 3, 6, 10, 14, px("dc2626"))
    fill(img, 12, 6, 20, 14, px("2563eb"))
    fill(img, 22, 6, 29, 14, px("16a34a"))
    fill(img, 3, 18, 14, 26, px("7c3aed"))
    fill(img, 16, 18, 29, 26, px("ea580c"))
    fill(img, 2, 28, 8, 31, O)
    fill(img, 24, 28, 30, 31, O)
    return img


def spr_trap_music():
    """Instrument case with a recorder on top."""
    img = new_img()
    case = px("1e3a8a")
    gold = px("eab308")
    cream = px("fef3c7")
    outline_fill(img, case)
    fill(img, 1, 10, 31, 31, case)
    fill(img, 4, 14, 28, 27, px("172554"))
    fill(img, 6, 16, 26, 20, gold)
    fill(img, 2, 1, 30, 11, cream)
    fill(img, 14, 1, 18, 28, px("f8fafc"))
    for yy in (4, 8, 12):
        fill(img, 13, yy, 19, yy + 2, O)
    fill(img, 15, 1, 17, 3, px("ef4444"))
    return img


def spr_trap_sports():
    """Basketball and gym cone."""
    img = new_img()
    orange = px("ea580c")
    od = px("9a3412")
    cone = px("f97316")
    outline_fill(img, orange)
    fill(img, 1, 22, 31, 31, px("64748b"))
    fill(img, 10, 8, 22, 23, cone)
    fill(img, 12, 4, 20, 10, px("f8fafc"))
    fill(img, 12, 5, 20, 9, px("111827"))
    for yy in range(1, 22):
        for x in range(1, 31):
            dx, dy = x - 16, yy - 12
            if dx * dx + dy * dy <= 90:
                col = od if (abs(dx) < 2 or abs(dy) < 2 or (dx + dy) % 6 == 0) else orange
                img.putpixel((x, yy), col)
    return img


def spr_trap_locker():
    """Hallway locker."""
    img = new_img()
    g = px("64748b")
    gd = px("334155")
    gl = px("cbd5e1")
    outline_fill(img, g)
    fill(img, 2, 2, 30, 30, gd)
    fill(img, 4, 4, 28, 14, g)
    fill(img, 4, 16, 28, 28, g)
    fill(img, 6, 6, 26, 8, gl)
    fill(img, 6, 10, 26, 12, gl)
    fill(img, 22, 18, 26, 24, px("facc15"))
    fill(img, 23, 19, 25, 23, px("111827"))
    fill(img, 8, 20, 14, 26, px("1e293b"))
    return img


def spr_trap_copier():
    """Photocopier with a paper jam."""
    img = new_img()
    beige = px("d6d3d1")
    bd = px("78716c")
    paper = px("f8fafc")
    outline_fill(img, beige)
    fill(img, 1, 1, 31, 10, bd)
    fill(img, 4, 3, 28, 8, px("1e293b"))
    fill(img, 6, 4, 26, 7, px("38bdf8"))
    fill(img, 1, 22, 31, 31, bd)
    fill(img, 8, 8, 24, 14, paper)
    fill(img, 10, 6, 26, 12, paper)
    fill(img, 18, 14, 28, 22, px("ef4444"))
    fill(img, 5, 24, 10, 28, px("22c55e"))
    fill(img, 22, 24, 27, 28, px("eab308"))
    return img


def spr_trap_tape():
    """Red/white exam-hall barrier."""
    img = new_img()
    r = px("dc2626")
    w = px("f8fafc")
    outline_fill(img, r)
    for yy in range(1, 31):
        for x in range(1, 31):
            img.putpixel((x, yy), r if ((x + yy) // 4) % 2 == 0 else w)
    fill(img, 8, 12, 24, 20, O)
    fill(img, 9, 13, 23, 19, px("111827"))
    fill(img, 11, 15, 21, 17, r)
    return img


def spr_trap_janitor():
    """Janitor mop bucket — pit."""
    img = new_img()
    y = px("eab308")
    yd = px("a16207")
    water = px("38bdf8")
    stick = px("78716c")
    outline_fill(img, y)
    fill(img, 14, 1, 18, 16, stick)
    fill(img, 8, 1, 24, 6, px("d6d3d1"))
    fill(img, 1, 14, 31, 18, px("fde68a"))
    fill(img, 4, 16, 28, 18, water)
    fill(img, 1, 22, 31, 31, yd)
    fill(img, 12, 20, 20, 26, O)
    fill(img, 13, 21, 19, 25, yd)
    return img


def spr_trap_stool():
    """Stacked classroom stools — pit."""
    img = new_img()
    seat = px("1d4ed8")
    leg = px("334155")
    outline_fill(img, seat)
    fill(img, 1, 1, 31, 8, px("60a5fa"))
    fill(img, 6, 8, 10, 16, leg)
    fill(img, 22, 8, 26, 16, leg)
    fill(img, 1, 16, 31, 22, seat)
    fill(img, 8, 22, 12, 31, leg)
    fill(img, 20, 22, 24, 31, leg)
    fill(img, 4, 3, 28, 6, px("f8fafc"))
    return img


def spr_trap_fake():
    """Looks like a kill pad: hazard stripes, spikes, skull. Harmless Ground."""
    img = new_img()
    y = px("facc15")
    k = px("111827")
    r = px("ef4444")
    bone = px("e2e8f0")
    outline_fill(img, y)
    for yy in range(1, 31):
        for x in range(1, 31):
            img.putpixel((x, yy), y if ((x + yy) // 3) % 2 == 0 else k)
    # fake spikes
    for cx in (6, 16, 26):
        for yy in range(2, 14):
            half = max(1, (yy - 2) // 3)
            fill(img, cx - half, yy, cx + half + 1, yy + 1, O)
            fill(img, cx - half + 1, yy, cx + half, yy + 1, bone)
        img.putpixel((cx, 2), r)
    # skull
    fill(img, 10, 15, 22, 28, O)
    fill(img, 11, 16, 21, 26, bone)
    fill(img, 13, 18, 16, 21, k)
    fill(img, 17, 18, 20, 21, k)
    fill(img, 14, 23, 19, 25, k)
    return img


def spr_trap_school():
    return spr_trap_bag()


META = """fileFormatVersion: 2
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
    flipGreenChannel: 0
  isReadable: 0
  streamingMipmaps: 0
  streamingMipmapsPriority: 0
  vTOnly: 0
  ignoreMipmapLimit: 0
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
  spriteExtrude: 0
  spriteMeshType: 0
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
  flipbookRows: 1
  flipbookColumns: 1
  maxTextureSizeSet: 0
  compressionQualitySet: 0
  textureFormatSet: 0
  ignorePngGamma: 0
  applyGammaDecoding: 0
  swizzle: 50462976
  cookieLightType: 0
  platformSettings:
  - serializedVersion: 4
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
  - serializedVersion: 4
    buildTarget: Standalone
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
    customData:
    physicsShape: []
    bones: []
    spriteID: 5e97eb03825dee720800000000000000
    internalID: 21300000
    vertices: []
    indices:
    edges: []
    weights: []
    secondaryTextures: []
    spriteCustomMetadata:
      entries: []
    nameFileIdTable: {{}}
  mipmapLimitGroupName:
  pSDRemoveMatte: 0
  userData:
  assetBundleName:
  assetBundleVariant:
"""

SPRITES = {
    "spr_trap_school.png": spr_trap_school,
    "spr_trap_desk.png": spr_trap_desk,
    "spr_trap_bag.png": spr_trap_bag,
    "spr_trap_books.png": spr_trap_books,
    "spr_trap_chalk.png": spr_trap_chalk,
    "spr_trap_globe.png": spr_trap_globe,
    "spr_trap_lunch.png": spr_trap_lunch,
    "spr_trap_cart.png": spr_trap_cart,
    "spr_trap_music.png": spr_trap_music,
    "spr_trap_sports.png": spr_trap_sports,
    "spr_trap_locker.png": spr_trap_locker,
    "spr_trap_copier.png": spr_trap_copier,
    "spr_trap_tape.png": spr_trap_tape,
    "spr_trap_janitor.png": spr_trap_janitor,
    "spr_trap_stool.png": spr_trap_stool,
    "spr_trap_fake.png": spr_trap_fake,
}


def main():
    for d in OUT_DIRS:
        os.makedirs(d, exist_ok=True)
    for name, fn in SPRITES.items():
        img = fn()
        for d in OUT_DIRS:
            path = os.path.join(d, name)
            img.save(path)
            meta_path = path + ".meta"
            if not os.path.exists(meta_path):
                seed = os.path.basename(d) + ":" + name
                with open(meta_path, "w", encoding="utf-8", newline="\n") as fh:
                    fh.write(META.format(guid=guid_for(seed)))
        print("wrote", name)
    print("done")


if __name__ == "__main__":
    main()
