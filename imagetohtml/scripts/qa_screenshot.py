#!/usr/bin/env python3
"""用 Playwright 截取 HTML 页面截图。"""

from __future__ import annotations

import argparse
from pathlib import Path

from playwright.sync_api import sync_playwright


def target_url(target: str) -> str:
    if target.startswith(("http://", "https://", "file://")):
        return target
    return Path(target).resolve().as_uri()


def main() -> None:
    parser = argparse.ArgumentParser(description="Capture a viewport screenshot for HTML QA.")
    parser.add_argument("target", help="HTML file path or URL")
    parser.add_argument("output", type=Path)
    parser.add_argument("--width", type=int, required=True)
    parser.add_argument("--height", type=int, required=True)
    parser.add_argument("--full-page", action="store_true", help="Capture the full page instead of the viewport.")
    args = parser.parse_args()

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": args.width, "height": args.height})
        page.goto(target_url(args.target), wait_until="networkidle")
        page.screenshot(path=str(args.output), full_page=args.full_page)
        browser.close()

    print(str(args.output))


if __name__ == "__main__":
    main()
