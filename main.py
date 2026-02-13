from PIL import Image
import sys
import os

# ========= SETTINGS =========
WIDTH = 160
HEIGHT = 120
# ============================

def convert_image(input_path, rotate_90=False):
    # Load image
    img = Image.open(input_path)

    # Rotate 90 degrees if requested
    if rotate_90:
        img = img.transpose(Image.ROTATE_90)

    # Resize to TFT resolution
    img = img.resize((WIDTH, HEIGHT))
    img = img.convert("RGB")

    # Output file name
    output_path = os.path.splitext(input_path)[0] + ".bin"

    with open(output_path, "wb") as f:
        for y in range(HEIGHT):
            for x in range(WIDTH):
                r, g, b = img.getpixel((x, y))

                # Convert RGB888 → RGB565
                rgb565 = ((r & 0xF8) << 8) | \
                         ((g & 0xFC) << 3) | \
                         (b >> 3)

                # Write little-endian
                f.write(rgb565.to_bytes(2, "little"))

    print("Done!")
    print("Output file:", output_path)
    print("Size should be:", WIDTH * HEIGHT * 2, "bytes")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python convert.py image.jpg [--rotate-90]")
    else:
        input_file = sys.argv[1]
        rotate_90 = "--rotate-90" in sys.argv
        convert_image(input_file, rotate_90)
