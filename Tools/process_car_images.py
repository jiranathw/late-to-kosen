#!/usr/bin/env python3
"""
Processes uploaded car images into clean, high-resolution transparent sprites:
1. spr_car_white.png (White Honda Civic Sedan facing Left)
2. spr_car_green.png (Green Porsche GT3 RS Supercar facing Left)
"""

import os
import uuid
import numpy as np
from PIL import Image
from collections import deque

def remove_background(im_path, is_white_car=True):
    im = Image.open(im_path).convert('RGBA')
    w, h = im.size
    arr = np.array(im)

    visited = np.zeros((h, w), dtype=bool)
    queue = deque()

    # Add all border pixels to flood fill queue
    for x in range(w):
        queue.append((x, 0))
        queue.append((x, h - 1))
        visited[0, x] = True
        visited[h - 1, x] = True
    for y in range(h):
        queue.append((0, y))
        queue.append((w - 1, y))
        visited[y, 0] = True
        visited[y, w - 1] = True

    while queue:
        x, y = queue.popleft()
        r, g, b, a = arr[y, x]

        # Background condition
        is_bg = False
        if is_white_car:
            # White car studio background is pure white / near white (> 246, 246, 246)
            if r > 246 and g > 246 and b > 246:
                is_bg = True
        else:
            # Green car studio background is light gray / white (> 210 with low color variance)
            if r > 215 and g > 215 and b > 215 and max(abs(int(r)-int(g)), abs(int(g)-int(b)), abs(int(r)-int(b))) < 18:
                is_bg = True

        if is_bg:
            arr[y, x, 3] = 0
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < w and 0 <= ny < h and not visited[ny, nx]:
                    visited[ny, nx] = True
                    queue.append((nx, ny))

    out = Image.fromarray(arr)
    bbox = out.getbbox()
    if bbox:
        out = out.crop(bbox)
    return out

def get_meta(guid, ppu=120):
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
    filterMode: 1
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
  spritePixelsToUnits: {ppu}
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

def run():
    p_white = r'C:/Users/Lenovo/.gemini/antigravity/brain/7ebe0d78-c499-4e79-9ef9-273f120fe641/.user_uploaded/media_1788112928669.png'
    p_green = r'C:/Users/Lenovo/.gemini/antigravity/brain/7ebe0d78-c499-4e79-9ef9-273f120fe641/.user_uploaded/media_1788112992669.png'

    im_white = remove_background(p_white, is_white_car=True)
    im_green = remove_background(p_green, is_white_car=False)

    out_dirs = [r'Assets/Art/Sprites', r'Assets/Resources/Sprites']
    for d in out_dirs:
        os.makedirs(d, exist_ok=True)

    # Save spr_car_white.png and spr_car_green.png
    # Also save as spr_vehicle_car and spr_vehicle_motorbike so any default lookup uses the cars!
    cars = {
        'spr_car_white.png': im_white,
        'spr_car_green.png': im_green,
        'spr_vehicle_car.png': im_green,
        'spr_vehicle_pickup.png': im_green,
        'spr_vehicle_motorbike.png': im_white, # Replace motorbike with white car!
    }

    # PPU 150 gives car length ~ 632 / 150 = ~4.2 world units, height = 211 / 150 = ~1.4 world units (Big & Imposing!)
    ppu_map = {
        'spr_car_white.png': 150,
        'spr_car_green.png': 125,
        'spr_vehicle_car.png': 125,
        'spr_vehicle_pickup.png': 125,
        'spr_vehicle_motorbike.png': 150,
    }

    for name, img in cars.items():
        for d in out_dirs:
            p = os.path.join(d, name)
            img.save(p)
            g = uuid.uuid5(uuid.NAMESPACE_DNS, 'car_' + name + '_' + d).hex
            with open(p + '.meta', 'w', encoding='utf-8') as mf:
                mf.write(get_meta(g, ppu=ppu_map.get(name, 140)))
            print(f'Saved {name} ({img.size}) to {d}')

if __name__ == '__main__':
    run()
