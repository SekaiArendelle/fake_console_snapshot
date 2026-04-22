# fake_console_snapshot

Generate a terminal-style image from plain text, with mixed English/Chinese font support.

## Requirements

- Python 3.10+
- Pillow

Install dependency:

```bash
pip install pillow
```

## CLI Usage (stdin -> image)

The CLI reads **all text from stdin** and writes an image to the path provided by `-o/--output`.

```bash
python -m fcs -o output.png
```

### Windows examples

Pipe file content:

```powershell
Get-Content .\input.txt -Raw | python -m fcs -o .\output\snapshot.png
```

Pipe inline text:

```powershell
"Hello from CLI`n中文测试" | python -m fcs -o .\snapshot.png
```

Use UTF-8 output path and auto-create parent folders:

```powershell
"line1`nline2" | python -m fcs --output .\artifacts\console\shot.png
```

## Python API

```python
from fcs.to_img import text2fake_console_snapshot

img = text2fake_console_snapshot("Hello\n中文")
img.save("snapshot.png")
```

## Notes

- Bundled fonts are loaded from `fcs/fonts`:
  - English: `UbuntuMonoNerdFontMono-Regular.ttf`
  - Chinese: `msyh.ttc`
- Empty stdin will raise an error.
