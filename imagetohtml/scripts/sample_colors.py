#!/usr/bin/env python3
"""生成颜色统计和可视化色板。"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from PIL import Image, ImageDraw


def to_hex(rgb: tuple[int, int, int]) -> str:
    return "#{:02X}{:02X}{:02X}".format(*rgb)


def main() -> None:
    parser = argparse.ArgumentParser(description="Sample exact RGB colors from an image.")
    parser.add_argument("image", type=Path)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--top", type=int, default=96)
    parser.add_argument("--max-unique-output", type=int, default=4096)
    args = parser.parse_args()

    args.out_dir.mkdir(parents=True, exist_ok=True)
    with Image.open(args.image) as img:
        rgb = img.convert("RGB")
        pixels = list(rgb.getdata())

    total = len(pixels)
    counts = Counter(pixels)
    unique_count = len(counts)
    include_all = unique_count <= args.max_unique_output
    selected = counts.most_common(None if include_all else args.top)

    payload = {
        "source": str(args.image),
        "total_pixels": total,
        "unique_color_count": unique_count,
        "truncated": not include_all,
        "top_limit": args.top if not include_all else None,
        "colors": [
            {
                "hex": to_hex(color),
                "count": count,
                "pixels_ratio": round(count / total, 6),
            }
            for color, count in selected
        ],
    }
    (args.out_dir / "raw-colors.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    swatch_width = 80
    swatch_height = 64
    palette_count = min(args.top, len(selected))
    palette = Image.new("RGB", (swatch_width * palette_count, swatch_height), "white")
    draw = ImageDraw.Draw(palette)
    for index, (color, _count) in enumerate(selected[:palette_count]):
        left = index * swatch_width
        draw.rectangle([left, 0, left + swatch_width, swatch_height], fill=color)
    palette.save(args.out_dir / "palette.png")

    print(str(args.out_dir / "raw-colors.json"))
    print(str(args.out_dir / "palette.png"))


if __name__ == "__main__":
    main()
