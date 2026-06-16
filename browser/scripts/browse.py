#!/usr/bin/env python3
"""
Playwright browser automation script for screenshots and web navigation.

Usage:
    python browse.py <url> [output_path] [--full-page] [--mobile] [--width W] [--height H]

Examples:
    python browse.py https://example.com
    python browse.py https://example.com /tmp/shot.png --full-page
    python browse.py https://example.com --mobile
"""

import argparse
import sys


def take_screenshot(url, output='/tmp/screenshot.png', full_page=False, mobile=False, width=1280, height=720):
    """Navigate to URL and take screenshot."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as e:
        print(f"ERROR: Playwright not installed ({e}). Run: pip install playwright && playwright install chromium")
        return False

    try:
        with sync_playwright() as p:
            if mobile:
                device = p.devices['iPhone 14']
                browser = p.webkit.launch(headless=True)
                page = browser.new_page(**device)
            else:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page(viewport={'width': width, 'height': height})

            page.goto(url)
            page.wait_for_load_state('networkidle')
            page.screenshot(path=output, full_page=full_page)

            title = page.title()
            browser.close()

            print(f"Screenshot saved to {output}")
            print(f"  URL: {url}")
            print(f"  Title: {title}")
            return True

    except Exception as e:
        print(f"ERROR: {str(e)}")
        return False


def main():
    parser = argparse.ArgumentParser(description='Take screenshots of web pages using Playwright')
    parser.add_argument('url', help='URL to navigate to')
    parser.add_argument('output', nargs='?', default='/tmp/screenshot.png', help='Output path (default: /tmp/screenshot.png)')
    parser.add_argument('--full-page', action='store_true', help='Capture full scrollable page')
    parser.add_argument('--mobile', action='store_true', help='Use mobile viewport (iPhone 14)')
    parser.add_argument('--width', type=int, default=1280, help='Viewport width (default: 1280)')
    parser.add_argument('--height', type=int, default=720, help='Viewport height (default: 720)')

    args = parser.parse_args()

    success = take_screenshot(
        url=args.url,
        output=args.output,
        full_page=args.full_page,
        mobile=args.mobile,
        width=args.width,
        height=args.height
    )

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
