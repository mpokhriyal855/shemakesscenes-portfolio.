import sys
import subprocess

try:
    from PIL import Image, ImageOps
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])
    from PIL import Image, ImageOps

def convert_to_transparent_black(img_path, out_path):
    try:
        img = Image.open(img_path).convert("L")
        alpha = ImageOps.invert(img)
        result = Image.new("RGBA", img.size, (0, 0, 0, 0))
        result.putalpha(alpha)
        result.save(out_path, "PNG")
        print(f"Processed {img_path} -> {out_path}")
    except Exception as e:
        print(f"Error processing {img_path}: {e}")

convert_to_transparent_black("assets/portrait_outline.png", "assets/portrait_transparent.png")
convert_to_transparent_black("assets/camera_outline.png", "assets/camera_transparent.png")
