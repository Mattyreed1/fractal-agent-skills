---
name: gumroad
description: Publish products to Gumroad — create listings, upload digital files (workflows, ebooks, courses), attach cover images, set price, tags, and rich content, then publish. Uses the official Gumroad v2 API. Triggers on "publish to gumroad", "create gumroad product", "list on gumroad", "sell n8n workflow", "upload to gumroad", "gumroad listing".
---

# Gumroad Skill

Programmatically create, populate, and publish Gumroad products via the official v2 API.

## When to use

- "Publish this n8n workflow to Gumroad"
- "Create a Gumroad product for this ebook"
- "List my course on Gumroad"
- Anything that needs a draft → file upload → cover → publish flow

## Capabilities

| Operation | Endpoint | Implemented |
|-----------|----------|-------------|
| Create draft product | `POST /v2/products` | yes |
| Update product | `PUT /v2/products/:id` | yes |
| Upload digital file (multipart S3) | `POST /v2/files/presign` → S3 PUT → `POST /v2/files/complete` | yes |
| Attach cover image (URL) | `POST /v2/products/:id/covers` (url param) | yes |
| Attach cover image (file) | `POST /v2/products/:id/covers` (signed_blob_id) | partial — see "Thumbnails & cover files" below |
| Attach thumbnail | `POST /v2/products/:id/thumbnail` | partial — same caveat |
| Publish (enable) | `PUT /v2/products/:id/enable` | yes |
| Disable / delete | `PUT /v2/products/:id/disable`, `DELETE /v2/products/:id` | yes |
| Offer codes | `POST/PUT/DELETE /v2/products/:id/offer_codes` | yes |
| Get / list products | `GET /v2/products`, `GET /v2/products/:id` | yes |

## Authentication

Set `GUMROAD_ACCESS_TOKEN` in the environment. Get one from Gumroad → Settings → Advanced → Applications. Required scopes:

- `edit_products` — create/update products, files, covers, thumbnails, offer codes
- `view_sales` — optional, only needed to read sales data

## The 3 workflows

### 1. One-shot publish from a manifest (recommended)

Drop a YAML manifest next to your files and run:

```bash
export GUMROAD_ACCESS_TOKEN="<your token>"
python3 ~/.claude/skills/gumroad/scripts/publish_product.py path/to/manifest.yaml
```

Manifest schema is in `templates/manifest.yaml`. The orchestrator:

1. Validates the manifest.
2. Uploads each file via the 4-step S3 multipart flow.
3. Creates the draft product with all fields populated.
4. Attaches cover images (URLs work natively; local paths require the blob workaround — see below).
5. Optionally enables (publishes) the product.
6. Prints the product ID, edit URL, and public URL.

### 2. Manual scripted use (Python)

```python
from scripts.gumroad_client import GumroadClient

g = GumroadClient()  # reads GUMROAD_ACCESS_TOKEN from env

file_url = g.upload_file("./my-workflow.json")
product = g.create_product(
    name="Daily Report n8n Workflow",
    price=2900,                   # $29.00 in cents
    description="<p>Automated daily standup digest...</p>",
    native_type="digital",
    tags=["n8n", "automation", "workflow"],
    files=[{"url": file_url}],
)
g.add_cover(product["id"], url="https://example.com/preview.png")
g.enable_product(product["id"])
print(f"Live: https://gumroad.com/l/{product['custom_permalink'] or product['id']}")
```

### 3. Direct CLI for a single endpoint

The client module is also a CLI — see `python3 ~/.claude/skills/gumroad/scripts/gumroad_client.py --help`.

## Field reference (POST /v2/products)

| Field | Required | Notes |
|-------|----------|-------|
| `name` | yes | Product title |
| `price` | yes | Smallest currency unit (cents). `2900` = $29.00 |
| `native_type` | no | `digital` (default), `course`, `ebook`, `membership`, `bundle`, `coffee`, `call`, `commission`. Cannot be changed later. |
| `description` | no | HTML allowed |
| `custom_permalink` | no | Vanity slug; `/l/<slug>` |
| `price_currency_type` | no | ISO code (defaults to account currency) |
| `subscription_duration` | membership only | `monthly`, `quarterly`, `biannually`, `yearly`, `every_two_years` |
| `customizable_price` | no | `true` for pay-what-you-want |
| `suggested_price_cents` | no | Used with `customizable_price` |
| `max_purchase_count` | no | Inventory limit |
| `taxonomy_id` | no | Category ID |
| `tags` | no | Array of strings (full replacement on update) |
| `custom_summary` | no | Short tagline |
| `rich_content` | no | Array of `{id, title, description}` pages; description is a ProseMirror doc |
| `files` | no | Array of `{url}` from `/v2/files/complete` (full replacement on update) |

Products are created as **drafts** (`published: false`). Call `enable_product()` to publish.

## File upload flow (the non-obvious part)

Files don't upload directly to `POST /v2/products`. The flow:

1. `POST /v2/files/presign` with `filename` + `file_size` → returns `upload_id`, `key`, `file_url`, and one `presigned_url` per 100 MB part.
2. For each part: `PUT` the byte range to its `presigned_url`. Capture the `ETag` response header.
3. `POST /v2/files/complete` with `upload_id`, `key`, and `parts: [{part_number, etag}]` → returns the canonical `file_url`.
4. Pass `files: [{"url": file_url}]` to product create/update.

The client's `upload_file(path)` does all 4 steps and returns the canonical URL. Max 20 GB per file.

**Update gotcha:** sending `files` on `PUT /v2/products/:id` is a **full replacement**. To keep an existing file, resubmit its `id` AND its canonical `file_url` (not the signed URL `GET` returns — that's a download URL). The client's `update_product(..., keep_existing_files=True)` handles this.

## Thumbnails & cover files

Covers and thumbnails use ActiveStorage `signed_blob_id`, not the multipart S3 flow. There are two paths:

- **Cover via URL (easy):** `POST /v2/products/:id/covers` with `url=https://...` accepts oEmbed/image URLs (YouTube, hosted images). The client's `add_cover(product_id, url=...)` does this.
- **Cover/thumbnail via file (hard):** requires obtaining a Rails ActiveStorage `signed_blob_id`. The standard `POST /rails/active_storage/direct_uploads` endpoint may or may not be exposed publicly. The client has `add_cover_from_file()` and `set_thumbnail_from_file()` that try this; if they 404, fall back to hosting the image somewhere and using the URL form.

Practical recommendation for n8n workflow listings: host preview images on imgur/Cloudinary/your own S3 bucket and use the URL form. Square thumbnails only.

## Common pitfalls (caught by client)

- Forgetting that `price` is in cents, not dollars.
- Sending `files` on PUT and wiping existing files.
- Trying to `enable` a product with no files attached (Gumroad rejects publish on empty digital products — the client warns).
- Using the `url` field returned by `GET /v2/products/:id` as a file URL — that's a time-limited signed download URL, not the canonical one. Save the canonical URL from `/v2/files/complete` on your side.

## Files in this skill

- `SKILL.md` — this file
- `scripts/gumroad_client.py` — Python client + CLI
- `scripts/publish_product.py` — manifest-driven orchestrator
- `templates/manifest.yaml` — example product manifest

## References

- API docs: https://gumroad.com/api (Files, Products sections, shipped April 2026)
- Source PRs: antiwork/gumroad #4267 (create), #4313 (bundle_contents), #4311 (covers/thumbnails), #4557 (file upload docs), #4565 (product API docs)
