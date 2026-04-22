from pathlib import Path
from typing import TypeAlias, Tuple, List
from PIL import Image, ImageDraw, ImageFont

RGBColor: TypeAlias = Tuple[int, int, int]
TextBBox: TypeAlias = Tuple[float, float, float, float]


def _is_chinese_char(ch: str) -> bool:
    code = ord(ch)
    return (
        0x4E00 <= code <= 0x9FFF
        or 0x3400 <= code <= 0x4DBF
        or 0x20000 <= code <= 0x2A6DF
        or 0x2A700 <= code <= 0x2B73F
        or 0x2B740 <= code <= 0x2B81F
        or 0x2B820 <= code <= 0x2CEAF
        or 0xF900 <= code <= 0xFAFF
    )


def text2fake_console_snapshot(
    text: str,
    bg_color: RGBColor = (40, 44, 52),
    text_color: RGBColor = (255, 255, 255),
    font_size: int = 16,
) -> Image.Image:
    if not isinstance(text, str):
        raise TypeError(f"Parameter 'text' must be a string, got {type(text).__name__}")

    if (
        not isinstance(bg_color, tuple)
        or len(bg_color) != 3
        or not all(isinstance(c, int) and 0 <= c <= 255 for c in bg_color)
    ):
        raise ValueError(
            "Parameter 'bg_color' must be a tuple of three integers (R, G, B) each in the range 0-255."
        )

    if (
        not isinstance(text_color, tuple)
        or len(text_color) != 3
        or not all(isinstance(c, int) and 0 <= c <= 255 for c in text_color)
    ):
        raise ValueError(
            "Parameter 'text_color' must be a tuple of three integers (R, G, B) each in the range 0-255."
        )

    if not isinstance(font_size, int) or font_size <= 0:
        raise ValueError("Parameter 'font_size' must be a positive integer.")

    fonts_dir = Path(__file__).resolve().parent / "fonts"
    en_font_path = fonts_dir / "UbuntuMonoNerdFontMono-Regular.ttf"
    zh_font_path = fonts_dir / "msyh.ttc"

    en_font = ImageFont.truetype(str(en_font_path), font_size)
    zh_font = ImageFont.truetype(str(zh_font_path), font_size)

    # Calculate image dimensions based on text
    lines: List[str] = text.split("\n")

    # Calculate dimensions more accurately
    max_width: int = 0
    max_height: int = 0

    temp_img = Image.new("RGB", (1, 1))
    temp_draw = ImageDraw.Draw(temp_img)

    for line in lines:
        line_width: int = 0
        line_height: int = 0

        for ch in line:
            current_font = zh_font if _is_chinese_char(ch) else en_font
            bbox: TextBBox = temp_draw.textbbox((0, 0), ch, font=current_font)
            char_width = int(bbox[2] - bbox[0])
            glyph_height = int(bbox[3] - bbox[1])
            line_width += char_width
            line_height = max(line_height, glyph_height)

        if line_height == 0:
            bbox = temp_draw.textbbox((0, 0), "A", font=en_font)
            line_height = int(bbox[3] - bbox[1])

        max_width = max(max_width, line_width)
        max_height = max(max_height, line_height)

    # Add padding
    padding: int = 10
    char_height: int = max_height if max_height > 0 else 20
    img_width: int = max_width + 2 * padding
    img_height: int = len(lines) * char_height + 2 * padding

    # Create image with black background
    img = Image.new("RGB", (img_width, img_height), color=bg_color)
    draw = ImageDraw.Draw(img)

    # Draw text line by line
    y_offset: int = padding
    for line in lines:
        x_offset: int = padding  # Left align
        for ch in line:
            current_font = zh_font if _is_chinese_char(ch) else en_font
            draw.text((x_offset, y_offset), ch, fill=text_color, font=current_font)
            bbox = draw.textbbox((0, 0), ch, font=current_font)
            x_offset += int(bbox[2] - bbox[0])
        y_offset += char_height

    return img
