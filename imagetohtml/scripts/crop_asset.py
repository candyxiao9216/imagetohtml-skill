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


def expand_bbox(
    crop_box: tuple[int, int, int, int],
    image_size: tuple[int, int],
    pad: int,
    pad_percent: float,
) -> tuple[int, int, int, int]:
    if pad < 0:
        raise ValueError("pad must be non-negative")
    if pad_percent < 0:
        raise ValueError("pad-percent must be non-negative")

    left, top, right, bottom = crop_box
    width = right - left
    height = bottom - top
    pad_x = pad + round(width * pad_percent / 100)
    pad_y = pad + round(height * pad_percent / 100)
    image_width, image_height = image_size
    return (
        max(0, left - pad_x),
        max(0, top - pad_y),
        min(image_width, right + pad_x),
        min(image_height, bottom + pad_y),
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Crop an asset from a source image.")
    parser.add_argument("image", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--bbox", nargs=4, type=int, required=True, metavar=("X", "Y", "W", "H"))
    parser.add_argument("--pad", type=int, default=0, help="Add fixed padding in pixels around bbox.")
    parser.add_argument(
        "--pad-percent",
        type=float,
        default=0,
        help="Add padding as a percentage of bbox width/height around bbox.",
    )
    parser.add_argument("--quality", type=int, default=92)
    args = parser.parse_args()

    crop_box = parse_bbox(args.bbox)
    with Image.open(args.image) as img:
        left, top, right, bottom = crop_box
        if left < 0 or top < 0 or right > img.width or bottom > img.height:
            raise ValueError(f"bbox {args.bbox} is outside image bounds {img.width}x{img.height}")
        crop_box = expand_bbox(crop_box, (img.width, img.height), args.pad, args.pad_percent)
        cropped = img.crop(crop_box)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        save_kwargs = {}
        if args.output.suffix.lower() in {".jpg", ".jpeg", ".webp"}:
            save_kwargs["quality"] = args.quality
        cropped.save(args.output, **save_kwargs)

    print(str(args.output))


if __name__ == "__main__":
    main()
