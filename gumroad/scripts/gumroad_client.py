#!/usr/bin/env python3
"""
Gumroad v2 API client.

Usage as a library:
    from gumroad_client import GumroadClient
    g = GumroadClient()  # reads GUMROAD_ACCESS_TOKEN
    file_url = g.upload_file("./workflow.json")
    p = g.create_product(name="X", price=2900, files=[{"url": file_url}])
    g.add_cover(p["id"], url="https://example.com/cover.png")
    g.enable_product(p["id"])

Usage as a CLI:
    python3 gumroad_client.py list-products
    python3 gumroad_client.py get-product <id>
    python3 gumroad_client.py upload-file <path>
    python3 gumroad_client.py create-product --name X --price 2900 --file ./x.json
    python3 gumroad_client.py enable <id>
    python3 gumroad_client.py disable <id>
    python3 gumroad_client.py delete <id>
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

import urllib.request
import urllib.parse
import urllib.error
import mimetypes

try:
    import certifi
    os.environ.setdefault("SSL_CERT_FILE", certifi.where())
    os.environ.setdefault("REQUESTS_CA_BUNDLE", certifi.where())
except ImportError:
    pass

API_BASE = "https://api.gumroad.com/v2"
PART_SIZE = 100 * 1024 * 1024  # 100 MB, matches Gumroad's presign granularity
MAX_FILE_SIZE = 20 * 1024 * 1024 * 1024  # 20 GB


class GumroadError(RuntimeError):
    def __init__(self, message: str, status: int | None = None, body: Any = None):
        super().__init__(message)
        self.status = status
        self.body = body


class GumroadClient:
    def __init__(self, access_token: str | None = None, base_url: str = API_BASE):
        self.token = access_token or os.environ.get("GUMROAD_ACCESS_TOKEN")
        if not self.token:
            raise GumroadError(
                "GUMROAD_ACCESS_TOKEN not set. Get one at Gumroad → Settings → Advanced → Applications."
            )
        self.base_url = base_url.rstrip("/")

    # ---------------------------------------------------------------- internals

    def _request(
        self,
        method: str,
        path: str,
        params: dict | None = None,
        files_form: list[tuple[str, str]] | None = None,
    ) -> dict:
        """Form-encoded request. Token always sent as access_token."""
        url = f"{self.base_url}{path}"
        form: list[tuple[str, str]] = [("access_token", self.token)]
        if params:
            form.extend(_flatten_form(params))
        if files_form:
            form.extend(files_form)

        body = urllib.parse.urlencode(form).encode("utf-8")
        req = urllib.request.Request(
            url=url,
            data=body if method in ("POST", "PUT", "DELETE") else None,
            method=method,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        if method == "GET" and form:
            req = urllib.request.Request(
                url=f"{url}?{urllib.parse.urlencode(form)}",
                method="GET",
            )

        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                raw = resp.read().decode("utf-8")
                data = json.loads(raw) if raw else {}
                if not data.get("success", True) and "message" in data:
                    raise GumroadError(data["message"], status=resp.status, body=data)
                return data
        except urllib.error.HTTPError as e:
            raw = e.read().decode("utf-8", errors="replace")
            try:
                parsed = json.loads(raw)
                msg = parsed.get("message") or parsed.get("error") or raw
            except Exception:
                parsed, msg = raw, raw
            raise GumroadError(f"HTTP {e.code} on {method} {path}: {msg}", status=e.code, body=parsed)

    # ----------------------------------------------------------------- products

    def list_products(self, page_key: str | None = None) -> dict:
        params = {"page_key": page_key} if page_key else None
        return self._request("GET", "/products", params=params)

    def get_product(self, product_id: str) -> dict:
        return self._request("GET", f"/products/{product_id}")

    def create_product(
        self,
        *,
        name: str,
        price: int,
        native_type: str = "digital",
        description: str | None = None,
        custom_permalink: str | None = None,
        price_currency_type: str | None = None,
        subscription_duration: str | None = None,
        customizable_price: bool | None = None,
        suggested_price_cents: int | None = None,
        max_purchase_count: int | None = None,
        taxonomy_id: str | None = None,
        tags: list[str] | None = None,
        custom_summary: str | None = None,
        rich_content: list[dict] | None = None,
        files: list[dict] | None = None,
    ) -> dict:
        if not isinstance(price, int) or price < 0:
            raise GumroadError("price must be a non-negative integer (cents)")
        params: dict[str, Any] = {
            "name": name,
            "price": price,
            "native_type": native_type,
        }
        for k, v in {
            "description": description,
            "custom_permalink": custom_permalink,
            "price_currency_type": price_currency_type,
            "subscription_duration": subscription_duration,
            "customizable_price": _bool(customizable_price),
            "suggested_price_cents": suggested_price_cents,
            "max_purchase_count": max_purchase_count,
            "taxonomy_id": taxonomy_id,
            "custom_summary": custom_summary,
        }.items():
            if v is not None:
                params[k] = v
        if tags:
            params["tags"] = tags
        if rich_content:
            params["rich_content"] = rich_content
        if files:
            params["files"] = files
        resp = self._request("POST", "/products", params=params)
        return resp.get("product", resp)

    def update_product(
        self,
        product_id: str,
        *,
        keep_existing_files: bool = False,
        new_files: list[dict] | None = None,
        **fields: Any,
    ) -> dict:
        """Update a product. Pass only fields you want to change.

        files/tags/rich_content are full replacement on the API side. To keep
        existing files plus add new ones, set keep_existing_files=True and
        pass the new file URLs in new_files.
        """
        params = {k: v for k, v in fields.items() if v is not None}

        if keep_existing_files or new_files is not None:
            existing = self.get_product(product_id).get("product", {}).get("file_info") or []
            # API doesn't return canonical URLs, only signed download URLs.
            # The reliable way to "keep" files is to track canonical URLs in
            # your own store. If we don't have them, warn and skip the merge.
            if existing and keep_existing_files:
                print(
                    "WARNING: keep_existing_files=True but canonical file_urls aren't returned by GET. "
                    "Pass them explicitly via new_files=[{id, url}, ...] to preserve files.",
                    file=sys.stderr,
                )
            files = list(new_files or [])
            if files:
                params["files"] = files

        resp = self._request("PUT", f"/products/{product_id}", params=params)
        return resp.get("product", resp)

    def enable_product(self, product_id: str) -> dict:
        return self._request("PUT", f"/products/{product_id}/enable")

    def disable_product(self, product_id: str) -> dict:
        return self._request("PUT", f"/products/{product_id}/disable")

    def delete_product(self, product_id: str) -> dict:
        return self._request("DELETE", f"/products/{product_id}")

    # -------------------------------------------------------------- file upload

    def upload_file(self, path: str | Path, filename: str | None = None) -> str:
        """Run the full 4-step upload flow. Returns canonical file_url."""
        path = Path(path)
        if not path.is_file():
            raise GumroadError(f"File not found: {path}")
        size = path.stat().st_size
        if size == 0:
            raise GumroadError(f"File is empty: {path}")
        if size > MAX_FILE_SIZE:
            raise GumroadError(f"File exceeds 20 GB limit: {size} bytes")

        name = filename or path.name

        # 1. Presign
        presign = self._request(
            "POST",
            "/files/presign",
            params={"filename": name, "file_size": size},
        )
        upload_id = presign["upload_id"]
        key = presign["key"]
        canonical_url = presign["file_url"]
        parts = presign["parts"]

        # 2. PUT each part to S3
        etags: list[dict] = []
        with path.open("rb") as fh:
            for part in parts:
                pn = int(part["part_number"])
                presigned_url = part["presigned_url"]
                fh.seek((pn - 1) * PART_SIZE)
                chunk = fh.read(PART_SIZE)
                etag = _put_to_s3(presigned_url, chunk)
                etags.append({"part_number": pn, "etag": etag})

        # 3. Complete
        complete = self._request(
            "POST",
            "/files/complete",
            params={"upload_id": upload_id, "key": key, "parts": etags},
        )
        return complete.get("file_url", canonical_url)

    # -------------------------------------------------------- covers/thumbnails

    def add_cover(self, product_id: str, *, url: str | None = None, signed_blob_id: str | None = None) -> dict:
        if not (url or signed_blob_id):
            raise GumroadError("add_cover requires url= or signed_blob_id=")
        params: dict[str, Any] = {}
        if url:
            params["url"] = url
        if signed_blob_id:
            params["signed_blob_id"] = signed_blob_id
        return self._request("POST", f"/products/{product_id}/covers", params=params)

    def delete_cover(self, product_id: str, cover_id: str) -> dict:
        return self._request("DELETE", f"/products/{product_id}/covers/{cover_id}")

    def add_cover_from_file(self, product_id: str, path: str | Path) -> dict:
        """Best-effort upload via Rails ActiveStorage direct upload.

        Falls back gracefully if the endpoint isn't exposed publicly. In that
        case, host the image elsewhere and use add_cover(url=...).
        """
        blob_id = self._direct_upload_blob(path)
        return self.add_cover(product_id, signed_blob_id=blob_id)

    def set_thumbnail(self, product_id: str, *, signed_blob_id: str) -> dict:
        return self._request(
            "POST",
            f"/products/{product_id}/thumbnail",
            params={"signed_blob_id": signed_blob_id},
        )

    def delete_thumbnail(self, product_id: str) -> dict:
        return self._request("DELETE", f"/products/{product_id}/thumbnail")

    def set_thumbnail_from_file(self, product_id: str, path: str | Path) -> dict:
        blob_id = self._direct_upload_blob(path)
        return self.set_thumbnail(product_id, signed_blob_id=blob_id)

    def _direct_upload_blob(self, path: str | Path) -> str:
        """Try Rails ActiveStorage direct_uploads. Raises if unsupported."""
        path = Path(path)
        size = path.stat().st_size
        mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        import hashlib
        import base64
        with path.open("rb") as fh:
            md5 = hashlib.md5(fh.read()).digest()
        checksum = base64.b64encode(md5).decode("ascii")
        body = json.dumps({
            "blob": {
                "filename": path.name,
                "byte_size": size,
                "checksum": checksum,
                "content_type": mime,
            }
        }).encode("utf-8")
        req = urllib.request.Request(
            url="https://api.gumroad.com/rails/active_storage/direct_uploads",
            data=body,
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.token}",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = json.loads(resp.read())
        except urllib.error.HTTPError as e:
            raise GumroadError(
                "Direct blob upload endpoint isn't accessible. Host the image somewhere "
                "(imgur/Cloudinary/your S3) and pass the URL to add_cover(url=...) instead.",
                status=e.code,
            )
        # PUT the bytes to the returned upload URL
        upload_url = data["direct_upload"]["url"]
        upload_headers = data["direct_upload"]["headers"]
        with path.open("rb") as fh:
            put_req = urllib.request.Request(url=upload_url, data=fh.read(), method="PUT", headers=upload_headers)
            with urllib.request.urlopen(put_req, timeout=300) as _:
                pass
        return data["signed_id"]

    # ----------------------------------------------------------- offer codes

    def create_offer_code(
        self,
        product_id: str,
        *,
        name: str,
        amount_off: int | None = None,
        percent_off: int | None = None,
        max_purchase_count: int | None = None,
        offer_type: str = "cents",  # or "percent"
    ) -> dict:
        params: dict[str, Any] = {"name": name, "offer_type": offer_type}
        if amount_off is not None and percent_off is not None:
            raise ValueError("pass either amount_off or percent_off, not both")
        if amount_off is not None:
            params["amount_off"] = amount_off
        if percent_off is not None:
            params["offer_type"] = "percent"
            params["amount_off"] = percent_off  # API uses amount_off w/ offer_type=percent
        if max_purchase_count is not None:
            params["max_purchase_count"] = max_purchase_count
        return self._request("POST", f"/products/{product_id}/offer_codes", params=params)


# ------------------------------------------------------------------ helpers


def _bool(v: bool | None) -> str | None:
    if v is None:
        return None
    return "true" if v else "false"


def _flatten_form(params: dict) -> list[tuple[str, str]]:
    """Convert dict (with nested arrays/objects) to Rails-style form pairs."""
    out: list[tuple[str, str]] = []
    for key, value in params.items():
        out.extend(_flatten_kv(key, value))
    return out


def _flatten_kv(key: str, value: Any) -> list[tuple[str, str]]:
    if value is None:
        return []
    if isinstance(value, bool):
        return [(key, "true" if value else "false")]
    if isinstance(value, (int, float, str)):
        return [(key, str(value))]
    if isinstance(value, list):
        out: list[tuple[str, str]] = []
        for item in value:
            if isinstance(item, dict):
                for sub_k, sub_v in item.items():
                    out.extend(_flatten_kv(f"{key}[][{sub_k}]", sub_v))
            else:
                out.extend(_flatten_kv(f"{key}[]", item))
        return out
    if isinstance(value, dict):
        out = []
        for sub_k, sub_v in value.items():
            out.extend(_flatten_kv(f"{key}[{sub_k}]", sub_v))
        return out
    return [(key, str(value))]


def _put_to_s3(url: str, chunk: bytes) -> str:
    req = urllib.request.Request(url=url, data=chunk, method="PUT")
    with urllib.request.urlopen(req, timeout=600) as resp:
        etag = resp.headers.get("ETag", "").strip('"')
        if not etag:
            raise GumroadError("S3 PUT succeeded but no ETag header returned")
        return etag


# ------------------------------------------------------------------ CLI


def _cli() -> int:
    parser = argparse.ArgumentParser(prog="gumroad", description="Gumroad v2 API CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("list-products")
    p = sub.add_parser("get-product")
    p.add_argument("id")

    p = sub.add_parser("upload-file")
    p.add_argument("path")

    p = sub.add_parser("create-product")
    p.add_argument("--name", required=True)
    p.add_argument("--price", type=int, required=True, help="cents")
    p.add_argument("--description")
    p.add_argument("--native-type", default="digital")
    p.add_argument("--tag", action="append", dest="tags")
    p.add_argument("--file", action="append", dest="files", help="path; uploaded then attached")
    p.add_argument("--cover-url", action="append", dest="cover_urls")
    p.add_argument("--enable", action="store_true")

    p = sub.add_parser("enable")
    p.add_argument("id")
    p = sub.add_parser("disable")
    p.add_argument("id")
    p = sub.add_parser("delete")
    p.add_argument("id")

    args = parser.parse_args()
    g = GumroadClient()

    if args.cmd == "list-products":
        print(json.dumps(g.list_products(), indent=2))
    elif args.cmd == "get-product":
        print(json.dumps(g.get_product(args.id), indent=2))
    elif args.cmd == "upload-file":
        url = g.upload_file(args.path)
        print(url)
    elif args.cmd == "create-product":
        files = []
        for path in args.files or []:
            print(f"Uploading {path}...", file=sys.stderr)
            files.append({"url": g.upload_file(path)})
        product = g.create_product(
            name=args.name,
            price=args.price,
            description=args.description,
            native_type=args.native_type,
            tags=args.tags,
            files=files or None,
        )
        print(json.dumps(product, indent=2))
        for cover_url in args.cover_urls or []:
            g.add_cover(product["id"], url=cover_url)
        if args.enable:
            g.enable_product(product["id"])
            print(f"Enabled. Public URL: https://gumroad.com/l/{product.get('custom_permalink') or product['id']}", file=sys.stderr)
    elif args.cmd == "enable":
        print(json.dumps(g.enable_product(args.id), indent=2))
    elif args.cmd == "disable":
        print(json.dumps(g.disable_product(args.id), indent=2))
    elif args.cmd == "delete":
        print(json.dumps(g.delete_product(args.id), indent=2))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(_cli())
    except GumroadError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
