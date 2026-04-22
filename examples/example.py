import pathlib
import sys

sys.path.append(
    str(pathlib.Path(__file__).parent.parent)
)  # Add parent directory to sys.path

from fcs import to_img

if __name__ == "__main__":
    sample_text = """Welcome to Console Snapshot!
This function converts text to a terminal-style image.
支持中英文混合显示 (Supports mixed Chinese and English).
Line 3: Testing special characters: @#$%^&*()
Line 4: More text to show how it works."""

    image = to_img.text2fake_console_snapshot(sample_text)
    image.show()
