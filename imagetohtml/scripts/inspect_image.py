#!/usr/bin/env python3
"""读取视觉稿基础信息，并推断源视口类型。"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image


def infer_viewport(width: int, height: int) -> dict[str, str | int]:
    ratio = width / height
    portrait_ratio = height / width
    if width >= 900 and ratio >= 1.2:
        viewport_type = "desktop"
        strategy = "desktop-first"
    elif height > width and (width <= 600 or portrait_ratio >= 1.6):
        viewport_type = "mobile"
        strategy = "mobile-first"
    elif 600 < width < 1200 and 0.65 <= ratio <= 1.4:
        viewport_type = "tablet"
        strategy = "source-viewport-first"
    elif 0.8 <= ratio <= 1.25:
        viewport_type = "square"
        strategy = "source-viewport-first"
    else:
        viewport_type = "needs-review"
        strategy = "ask-user"
    return {
        "type": viewport_type,
        "width": width,
        "height": height,
        "strategy": strategy,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Inspect a visual mockup image.")
    parser.add_argument("image", type=Path)
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()

    with Image.open(args.image) as img:
        width, height = img.size
        payload = {
            "source": str(args.image),
            "format": img.format,
            "mode": img.mode,
            "width": width,
            "height": height,
            "aspect_ratio": round(width / height, 4),
            "source_viewport": infer_viewport(width, height),
        }

    text = json.dumps(payload, ensure_ascii=False, indent=2)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)


if __name__ == "__main__":
    main()
