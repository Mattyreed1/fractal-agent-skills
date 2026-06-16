#!/usr/bin/env python3
"""Publish a Gumroad product from a manifest file (YAML or JSON).

Usage:
    python3 publish_product.py path/to/manifest.yaml [--dry-run] [--no-publish]

The manifest schema is documented in templates/manifest.yaml. Paths inside the
manifest are resolved relative to the manifest's directory.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

# Make sibling import work when run as a script.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from gumroad_client import GumroadClient, GumroadError  # noqa: E402


REQUIRED_FIELDS = {"name", "price"}
ALLOWED_NATIVE_TYPES = {
    "digital", "course", "ebook", "membership", "bundle", "coffee", "call", "commission",
}


def load_manifest(path: Path) -> dict:
    raw = path.read_text(encoding="utf-8")
    if path.suffix.lower() in (".yaml", ".yml"):
        try:
            import yaml  # type: ignore
        except ImportError:
            raise SystemExit("PyYAML required for .yaml manifests. Install: pip3 install pyyaml")
        return yaml.safe_load(raw)
    return json.loads(raw)


def validate(manifest: dict) -> None:
    missing = REQUIRED_FIELDS - set(manifest)
    if missing:
        raise SystemExit(f"Manifest missing required fields: {sorted(missing)}")
    if not isinstance(manifest["price"], int) or manifest["price"] < 0:
        raise SystemExit("price must be a non-negative integer (cents). $29.00 → 2900")
    nt = manifest.get("native_type", "digital")
    if nt not in ALLOWED_NATIVE_TYPES:
        raise SystemExit(f"native_type {nt!r} not in {sorted(ALLOWED_NATIVE_TYPES)}")
    if nt == "membership" and not manifest.get("subscription_duration"):
        raise SystemExit("membership products require subscription_duration")


def resolve_path(base: Path, p: str) -> Path:
    candidate = Path(p)
    return candidate if candidate.is_absolute() else (base / candidate).resolve()


def run(manifest_path: Path, *, dry_run: bool, publish: bool) -> int:
    manifest = load_manifest(manifest_path)
    validate(manifest)

    base = manifest_path.parent
    file_paths = [resolve_path(base, f) for f in (manifest.get("files") or [])]
    cover_specs = manifest.get("covers") or []  # each: {"url": "..."} or {"file": "..."}
    thumbnail_path = manifest.get("thumbnail")

    print(f"Manifest: {manifest_path}")
    print(f"  name:    {manifest['name']}")
    print(f"  price:   {manifest['price']} ({manifest['price']/100:.2f} {manifest.get('price_currency_type','usd')})")
    print(f"  type:    {manifest.get('native_type','digital')}")
    print(f"  files:   {[str(p) for p in file_paths]}")
    print(f"  covers:  {cover_specs}")
    print(f"  thumb:   {thumbnail_path}")
    print(f"  publish: {publish}")
    if dry_run:
        print("DRY RUN — no API calls made.")
        return 0

    g = GumroadClient()

    # 1. Upload files
    file_urls: list[dict] = []
    for fp in file_paths:
        if not fp.is_file():
            raise SystemExit(f"File not found: {fp}")
        print(f"Uploading {fp.name} ({fp.stat().st_size:,} bytes)...")
        url = g.upload_file(fp)
        file_urls.append({"url": url})
        print(f"  → {url}")

    # 2. Create product
    create_kwargs: dict[str, Any] = {
        "name": manifest["name"],
        "price": manifest["price"],
        "native_type": manifest.get("native_type", "digital"),
    }
    for k in (
        "description", "custom_permalink", "price_currency_type",
        "subscription_duration", "customizable_price", "suggested_price_cents",
        "max_purchase_count", "taxonomy_id", "custom_summary",
    ):
        if k in manifest and manifest[k] is not None:
            create_kwargs[k] = manifest[k]
    if manifest.get("tags"):
        create_kwargs["tags"] = manifest["tags"]
    if manifest.get("rich_content"):
        create_kwargs["rich_content"] = manifest["rich_content"]
    if file_urls:
        create_kwargs["files"] = file_urls

    print("Creating product...")
    product = g.create_product(**create_kwargs)
    pid = product["id"]
    print(f"  → product id: {pid}")
    print(f"  → edit URL:   https://app.gumroad.com/products/{pid}/edit")

    # 3. Covers
    for spec in cover_specs:
        if "url" in spec:
            print(f"Adding cover (url): {spec['url']}")
            g.add_cover(pid, url=spec["url"])
        elif "file" in spec:
            cover_path = resolve_path(base, spec["file"])
            print(f"Adding cover (file): {cover_path}")
            try:
                g.add_cover_from_file(pid, cover_path)
            except GumroadError as e:
                print(f"  WARNING: file-based cover upload failed: {e}", file=sys.stderr)
                print("  Host the image somewhere and add it as a URL cover instead.", file=sys.stderr)

    # 4. Thumbnail
    if thumbnail_path:
        tp = resolve_path(base, thumbnail_path)
        print(f"Setting thumbnail: {tp}")
        try:
            g.set_thumbnail_from_file(pid, tp)
        except GumroadError as e:
            print(f"  WARNING: thumbnail upload failed: {e}", file=sys.stderr)

    # 5. Offer codes
    for code in manifest.get("offer_codes") or []:
        print(f"Creating offer code: {code['name']}")
        g.create_offer_code(pid, **code)

    # 6. Publish
    if publish:
        if not file_urls and create_kwargs.get("native_type") == "digital":
            print("WARNING: digital product has no files attached; Gumroad may reject publish.", file=sys.stderr)
        print("Publishing (enable)...")
        g.enable_product(pid)
        slug = manifest.get("custom_permalink") or pid
        check = g.get_product(pid)
        prod = check.get("product", check)
        if prod.get("published") is False:
            print(f"\nWARNING: enable call returned but product does not show as published — verify in the Gumroad dashboard. https://gumroad.com/l/{slug}", file=sys.stderr)
        else:
            print(f"\n✅ Live: https://gumroad.com/l/{slug}")
    else:
        print("\nDraft created (not published). Call enable when ready.")
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", help="Path to manifest YAML or JSON")
    parser.add_argument("--dry-run", action="store_true", help="Validate and print plan only")
    parser.add_argument("--no-publish", action="store_true", help="Create draft, don't enable")
    args = parser.parse_args()

    manifest_path = Path(args.manifest).resolve()
    if not manifest_path.is_file():
        raise SystemExit(f"Manifest not found: {manifest_path}")

    try:
        rc = run(manifest_path, dry_run=args.dry_run, publish=not args.no_publish)
    except GumroadError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
    sys.exit(rc)


if __name__ == "__main__":
    main()
