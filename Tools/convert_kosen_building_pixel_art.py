#!/usr/bin/env python3
"""
Converts the user's real KOSEN-KMITL building photo (media_1788115799511.png)
into a vivid 800x450 16:9 retro pixel art background for Level 2:
- Expands composition to 16:9 widescreen (800x450) with matching blue sky & campus horizon
- Pixelates into authentic 8-bit / 16-bit color quantization
- Crisp pixel details for the iconic angular KOSEN building, glass windows, Thai flags, and "KOSEN KMITL >" landmark sign
- Saves to background_stage2.png and background_kosen.png in Assets/Art/Sprites and Assets/Resources/Sprites
"""

import os
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter

def make_pixel_art_kosen_bg():
    src_path = r'C:/Users/Lenovo/.gemini/antigravity/brain/7ebe0d78-c499-4e79-9ef9-273f120fe641/.user_uploaded/media_1788115799511.png'
    src = Image.open(src_path).convert('RGB')

    # Target 16:9 widescreen canvas (800x450)
    target_w, target_h = 800, 450
    canvas = Image.new('RGB', (target_w, target_h), (90, 160, 230))

    # 1. Generate seamless 16:9 Sky & Clouds gradient for the wide panorama
    for y in range(target_h):
        t = y / float(target_h)
        # Blue sky gradient (Top deep sky blue -> bottom light horizon)
        r = int(50 * (1 - t) + 190 * t)
        g = int(140 * (1 - t) + 215 * t)
        b = int(230 * (1 - t) + 245 * t)
        for x in range(target_w):
            canvas.putpixel((x, y), (r, g, b))

    # Soft background clouds on left side
    cloud_color = (240, 248, 255)
    for y in range(40, 200):
        for x in range(0, 450):
            d = (math_sin := (math := __import__('math')).sin(x * 0.03) * 15 + math.cos(y * 0.05) * 10)
            if abs(y - 100) < 30 + d:
                orig = canvas.getpixel((x, y))
                blend_r = int(orig[0] * 0.4 + cloud_color[0] * 0.6)
                blend_g = int(orig[1] * 0.4 + cloud_color[1] * 0.6)
                blend_b = int(orig[2] * 0.4 + cloud_color[2] * 0.6)
                canvas.putpixel((x, y), (blend_r, blend_g, blend_b))

    # 2. Resize and place the KOSEN building onto the widescreen canvas
    # Scale building to fit 450 height nicely
    scale_factor = target_h / float(src.height)
    new_w = int(src.width * scale_factor)
    scaled_src = src.resize((new_w, target_h), Image.Resampling.LANCZOS)

    # Position building at center-right (e.g. x offset 180..380)
    paste_x = (target_w - new_w) // 2 + 60
    
    # Blend the left sky edge smoothly
    for y in range(target_h):
        for x in range(new_w):
            cx = paste_x + x
            if 0 <= cx < target_w:
                src_px = scaled_src.getpixel((x, y))
                if x < 40: # Blend seam
                    alpha = x / 40.0
                    bg_px = canvas.getpixel((cx, y))
                    blended = tuple(int(bg_px[i]*(1-alpha) + src_px[i]*alpha) for i in range(3))
                    canvas.putpixel((cx, y), blended)
                else:
                    canvas.putpixel((cx, y), src_px)

    # Ground pavement on the left
    ground_color = (210, 218, 225)
    for y in range(360, target_h):
        for x in range(0, paste_x + 30):
            canvas.putpixel((x, y), ground_color if (x + y) % 4 != 0 else (195, 205, 215))

    # 3. Apply Retro Color Enhancement & Contrast
    enhancer = ImageEnhance.Contrast(canvas)
    canvas = enhancer.enhance(1.25)
    enhancer = ImageEnhance.Color(canvas)
    canvas = enhancer.enhance(1.35)

    # 4. Pixelation Downsampling (266 x 150 grid -> authentic 8-bit chunky pixels!)
    pixel_w, pixel_h = 266, 150
    small = canvas.resize((pixel_w, pixel_h), Image.Resampling.BOX)

    # 5. Palette Quantization (Reduce to 48 rich retro colors for authentic arcade pixel art look)
    quantized = small.quantize(colors=64, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.FLOYDSTEINBERG).convert('RGBA')

    # 6. Upscale back to 800x450 using Nearest Neighbor (Point) so every pixel is razor sharp!
    pixel_art = quantized.resize((800, 450), Image.Resampling.NEAREST)

    return pixel_art

def generate():
    img = make_pixel_art_kosen_bg()

    dirs = [r'Assets/Art/Sprites', r'Assets/Resources/Sprites']
    for d in dirs:
        os.makedirs(d, exist_ok=True)
        img.save(os.path.join(d, 'background_stage2.png'))
        img.save(os.path.join(d, 'background_kosen.png'))
        print(f'Saved pixel art KOSEN building background in {d}')

if __name__ == '__main__':
    generate()
