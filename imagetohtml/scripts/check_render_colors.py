#!/usr/bin/env python3
"""对比母图和最终截图的关键区域均色。"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from PIL import Image


def parse_region(value: str) -> tuple[str, tuple[int, int, int, int], float]:
    parts = value.split(":")
    if len(parts) not in {2, 3}:
        raise ValueError("region must be NAME:X,Y,W,H[:MAX_DELTA]")
    name = parts[0].strip()
    if not name:
        raise ValueError("region name must not be empty")
    coords = [int(item) for item in parts[1].split(",")]
    if len(coords) != 4:
        raise ValueError("region bbox must contain X,Y,W,H")
    x, y, width, height = coords
    if width <= 0 or height <= 0:
        raise ValueError("region width and height must be positive")
    max_delta = float(parts[2]) if len(parts) == 3 else 12.0
    if max_delta < 0:
        raise ValueError("max delta must be non-negative")
    return name, (x, y, width, height), max_delta


def crop_average(img: Image.Image, bbox: tuple[int, int, int, int]) -> tuple[int, int, int]:
    x, y, width, height = bbox
    if x < 0 or y < 0 or x + width > img.width or y + height > img.height:
        raise ValueError(f"bbox {bbox} is outside image bounds {img.width}x{img.height}")
    crop = img.crop((x, y, x + width, y + height)).convert("RGB")
    pixels = list(crop.getdata())
    count = len(pixels)
    return tuple(round(sum(pixel[i] for pixel in pixels) / count) for i in range(3))


def color_delta(left: tuple[int, int, int], right: tuple[int, int, int]) -> float:
    return math.sqrt(sum((left[i] - right[i]) ** 2 for i in range(3)))


def to_hex(rgb: tuple[int, int, int]) -> str:
    return "#{:02X}{:02X}{:02X}".format(*rgb)


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare sampled region colors between source and screenshot.")
    parser.add_argument("source", type=Path)
    parser.add_argument("screenshot", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument(
        "--region",
        action="append",
        required=True,
        help="Region spec: NAME:X,Y,W,H[:MAX_DELTA]. Bbox uses source image pixels.",
    )
    args = parser.parse_args()

    regions = [parse_region(region) for region in args.region]
    with Image.open(args.source) as source_img, Image.open(args.screenshot) as screenshot_img:
        source_rgb = source_img.convert("RGB")
        screenshot_rgb = screenshot_img.convert("RGB")
        size_match = source_rgb.size == screenshot_rgb.size
        results = []
        for name, bbox, max_delta in regions:
            source_avg = crop_average(source_rgb, bbox)
            screenshot_avg = crop_average(screenshot_rgb, bbox)
            delta = round(color_delta(source_avg, screenshot_avg), 2)
            results.append(
                {
                    "name": name,
                    "bbox": list(bbox),
                    "source_avg": to_hex(source_avg),
                    "screenshot_avg": to_hex(screenshot_avg),
                    "delta": delta,
                    "max_delta": max_delta,
                    "status": "pass" if delta <= max_delta else "fail",
                }
            )

    payload = {
        "source": str(args.source),
        "screenshot": str(args.screenshot),
        "source_size": [source_rgb.width, source_rgb.height],
        "screenshot_size": [screenshot_rgb.width, screenshot_rgb.height],
        "size_match": size_match,
        "regions": results,
        "status": "pass" if size_match and all(item["status"] == "pass" for item in results) else "fail",
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(str(args.out))


if __name__ == "__main__":
    main()
