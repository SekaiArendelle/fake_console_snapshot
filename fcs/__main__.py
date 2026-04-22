from __future__ import annotations

import argparse
import sys
from pathlib import Path
from .to_img import text2fake_console_snapshot


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
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    text = sys.stdin.read()
    if text == "":
        raise ValueError("No input received from stdin.")

    output_path: Path = args.output
    output_path.parent.mkdir(parents=True, exist_ok=True)

    image = text2fake_console_snapshot(text)
    image.save(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
