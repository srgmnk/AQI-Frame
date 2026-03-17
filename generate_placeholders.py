from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

WIDTH = 800
HEIGHT = 480
OUTPUT_DIR = Path("images")

BG_COLOR = "#D9D9D9"
TEXT_COLOR = "black"

START = 0
END = 301  # inclusive


def load_font(size: int):
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/Library/Fonts/Arial Bold.ttf",
        "/Library/Fonts/Arial.ttf",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def fit_font(draw: ImageDraw.ImageDraw, text: str, max_width: int, max_height: int):
    for size in range(280, 20, -4):
        font = load_font(size)
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        if text_width <= max_width and text_height <= max_height:
            return font, text_width, text_height
    font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), text, font=font)
    return font, bbox[2] - bbox[0], bbox[3] - bbox[1]


def generate_image(value: int):
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)

    text = str(value)
    font, text_width, text_height = fit_font(
        draw,
        text,
        max_width=int(WIDTH * 0.8),
        max_height=int(HEIGHT * 0.6),
    )

    x = (WIDTH - text_width) / 2
    y = (HEIGHT - text_height) / 2

    draw.text((x, y), text, font=font, fill=TEXT_COLOR)

    output_path = OUTPUT_DIR / f"{value}.png"
    img.save(output_path, format="PNG")


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for value in range(START, END + 1):
        generate_image(value)

    print(f"Done: generated {END - START + 1} images in '{OUTPUT_DIR}'")


if __name__ == "__main__":
    main()
