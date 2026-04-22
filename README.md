# fake_console_snapshot

Generate a terminal-style image from plain text, with mixed English/Chinese font support.

## Requirements

- Python 3.10+
- Pillow

Install dependencies with uv:

```bash
uv sync
```

## CLI Usage (stdin -> image)

The CLI reads **all text from stdin** and writes an image to the path provided by `-o/--output`.
It also supports `--bg-color`, `--text-color` (both in `R,G,B`) and `--font-size`.

```bash
uv run python -m fcs -o output.png
```

```bash
uv run python -m fcs -o output.png --bg-color 40,44,52 --text-color 255,255,255 --font-size 16
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

Custom colors and font size:

```powershell
"Hello`n彩色输出" | python -m fcs -o .\snapshot.png --bg-color 25,25,25 --text-color 0,255,180 --font-size 20
```

## Python API

see [examples](./examples/)

## Notes

- Bundled fonts are loaded from `fcs/fonts`:
  - English: `UbuntuMonoNerdFontMono-Regular.ttf`
  - Chinese: `msyh.ttc`
- Empty stdin will raise an error.
