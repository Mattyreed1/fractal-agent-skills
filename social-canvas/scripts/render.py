#!/usr/bin/env python3
"""render.py — Playwright HTML→PNG renderer for social-canvas (Claude Code / Mac).

Local-runtime mirror of render.js (which targets the agent runtime container).
Uses the Python Playwright install this Mac already has (same engine as the
browser skill). Forces device_scale_factor=1 to prevent 2x output; waits for
networkidle + document.fonts.ready so Google Fonts @imports finish.

Usage:
    python3 render.py input.html output.png --width 1080 --height 1350
"""
import argparse
import pathlib
import sys

from playwright.sync_api import sync_playwright


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input_html")
    ap.add_argument("output_png")
    ap.add_argument("--width", type=int, default=1080)
    ap.add_argument("--height", type=int, default=1350)
    args = ap.parse_args()

    src = pathlib.Path(args.input_html).resolve()
    if not src.exists():
        sys.exit(f"input not found: {src}")
    out = pathlib.Path(args.output_png).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(
            viewport={"width": args.width, "height": args.height},
            device_scale_factor=1,
        )
        page.goto(src.as_uri(), wait_until="networkidle")
        page.evaluate("document.fonts.ready")
        page.screenshot(path=str(out), clip={"x": 0, "y": 0, "width": args.width, "height": args.height})
        browser.close()
    print(f"rendered {out} ({args.width}x{args.height})")


if __name__ == "__main__":
    main()
