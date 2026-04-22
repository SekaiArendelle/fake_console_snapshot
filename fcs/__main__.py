import argparse
import sys
from pathlib import Path
from typing import Tuple

from .to_img import text2fake_console_snapshot


def _rgb_color(value: str) -> Tuple[int, int, int]:
    parts = value.split(",")
    try:
        color = tuple(int(part.strip()) for part in parts)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            "Color values must be integers in range 0-255."
        ) from exc

    if any(channel < 0 or channel > 255 for channel in color):
        raise argparse.ArgumentTypeError(
            "Color values must be integers in range 0-255."
        )
    if len(color) != 3:
        raise argparse.ArgumentTypeError(
            "Color must be in R,G,B format, e.g. 40,44,52."
        )
    return color


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="python -m fcs",
        description="Read text from stdin and render it as a console-style image.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        required=True,
        help="Output image path, e.g. output.png",
    )
    parser.add_argument(
        "--bg-color",
        type=_rgb_color,
        default=(40, 44, 52),
        metavar="R,G,B",
        help="Background color as R,G,B (0-255), default: 40,44,52",
    )
    parser.add_argument(
        "--text-color",
        type=_rgb_color,
        default=(255, 255, 255),
        metavar="R,G,B",
        help="Text color as R,G,B (0-255), default: 255,255,255",
    )
    parser.add_argument(
        "--font-size",
        type=int,
        default=16,
        help="Font size in pixels, must be a positive integer (default: 16)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    text = sys.stdin.read()
    if text == "":
        raise ValueError("No input received from stdin.")
    if args.font_size <= 0:
        raise ValueError("Parameter '--font-size' must be a positive integer.")

    output_path: Path = args.output
    output_path.parent.mkdir(parents=True, exist_ok=True)

    image = text2fake_console_snapshot(
        text,
        bg_color=args.bg_color,
        text_color=args.text_color,
        font_size=args.font_size,
    )
    image.save(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
