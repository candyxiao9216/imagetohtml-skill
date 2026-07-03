#!/usr/bin/env python3
"""按原图坐标裁切资产。bbox 使用 x y width height。"""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image


def parse_bbox(values: list[int]) -> tuple[int, int, int, int]:
    if len(values) != 4:
        raise ValueError("bbox must contain exactly four integers: x y width height")
    x, y, width, height = values
    if width <= 0 or height <= 0:
        raise ValueError("bbox width and height must be positive")
    return x, y, x + width, y + height


def main() -> None:
    parser = argparse.ArgumentParser(description="Crop an asset from a source image.")
    parser.add_argument("image", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--bbox", nargs=4, type=int, required=True, metavar=("X", "Y", "W", "H"))
    parser.add_argument("--quality", type=int, default=92)
    args = parser.parse_args()

    crop_box = parse_bbox(args.bbox)
    with Image.open(args.image) as img:
        left, top, right, bottom = crop_box
        if left < 0 or top < 0 or right > img.width or bottom > img.height:
            raise ValueError(f"bbox {args.bbox} is outside image bounds {img.width}x{img.height}")
        cropped = img.crop(crop_box)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        save_kwargs = {}
        if args.output.suffix.lower() in {".jpg", ".jpeg", ".webp"}:
            save_kwargs["quality"] = args.quality
        cropped.save(args.output, **save_kwargs)

    print(str(args.output))


if __name__ == "__main__":
    main()
