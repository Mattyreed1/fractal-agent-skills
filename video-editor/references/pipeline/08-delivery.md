# Pipeline 8 — Render / export & delivery

**Step 8 of 8** — final master + platform exports. **Backend:** palmier-pro.

## 🚦 Gate first
**Nothing here happens until the [delivery gate](../delivery-gate.md) passes with written evidence.**
"Ready for review" is a gated claim, not a feeling.

- `export_project` modes: **`video`** ⚠️ (H.264/H.265/ProRes, 720p–4K or Match Timeline; background
  render — defaults to `~/Downloads` and **overwrites**, so set the target explicitly) ·
  **`fcpxml`** ✅ (`fcpxmlTarget: resolve|fcp` — the interchange path out) · **`xml`** (Premiere) ·
  **`palmier`** (project package, also the mid-build checkpoint format)
- `manage_exports` — track jobs · `capture_frame` — thumbnail from the FINAL render, not the timeline

### 📁 PUBLISH BY COPYING INTO THE MOUNTED DRIVE FOLDER — never via the API (2026-08-12)

**Destinations (Fractal AI) — these are LOCAL PATHS on the user's Mac, and Drive syncs them up:**
```
DRIVE="$HOME/Library/CloudStorage/GoogleDrive-<YOUR_GOOGLE_ACCOUNT>/My Drive/Business   Career/Entrepreneurship/Fractal AI Agency/marketing"
$DRIVE/video/<slug>-final.mp4                    # note: "Business   Career" has THREE spaces
$DRIVE/images/thumbnails/<slug>-thumbnail.png    # a SEPARATE folder, not beside the video
```
Use `scripts/publish_delivery.sh <slug> <master.mp4> <thumb.png>` — it copies both and verifies by
`stat` on the mounted paths.

**Why not `gws drive files update`:** the API writes the CLOUD copy. The mounted folder is a SECOND
copy, and it did not pick the change up — the user opened `marketing/video` in Finder and got the
three-cuts-old file while EA quoted API byte counts proving the new one was "there." Both were true.
**Write to the copy the human opens, and `stat` that path to verify.** Upward sync is reliable;
downward is not.

**Also: the canonical `<slug>-final.mp4` name must point at the CURRENT master.** EA left `-final.mp4`
holding an Aug-9 cut while the real master carried a working name (`-hook-v8-cutout-m14.mp4`). The
confident filename is what gets posted — promote the master into it, and keep old cuts under versioned
names.

**Verify the render itself with `ffprobe`** (duration / resolution / fps / audio stream) before
calling it delivered — `inspect_timeline` is unreliable on v0.6.5 (stuck at frame 0), so render-verify
with ffmpeg rather than trusting a timeline read. Then advance the Notion Stage in the SAME turn.

## 🔊 MASTER THE AUDIO — required step, every export (gate G16)

**Palmier exports at whatever the timeline sums to. That is never platform spec.** On the
ai-notetaker build the export measured **−20.2 LUFS / −3.3 dBFS**; social norm is **−14 LUFS with a
−1.0 dBTP ceiling**. Six dB down does not read to a viewer as "quiet", it reads as low-energy.

```bash
# 1 — measure
ffmpeg -hide_banner -nostats -i render.mp4 -af ebur128=peak=true -f null -
# 2 — master: constant gain + true-peak limiter, video copied bit-for-bit
ffmpeg -y -i render.mp4 -c:v copy \
  -af "volume=6.6dB,alimiter=limit=0.78:attack=5:release=60:level=disabled" \
  -c:a aac -b:a 256k -movflags +faststart render-m14.mp4
# 3 — verify (cite I / LRA / true peak in the checklist)
ffmpeg -hide_banner -nostats -i render-m14.mp4 -af ebur128=peak=true -f null -
```

**Do NOT reach for two-pass `loudnorm` on a finished mix.** When the gain needed to hit −14 exceeds
the true-peak ceiling — which it does on any already-compressed mix (LRA ≈ 3 LU) — loudnorm silently
switches to `normalization_type: dynamic` and applies **time-varying** gain, re-balancing a voice:bed
ratio that was already approved. Constant gain + limiter preserves the mix exactly; the limiter only
touches transients. If you do run loudnorm, read `normalization_type` out of its pass-1 JSON first.

**Log-level trap that will waste calls:** `volumedetect`, `astats` and `ebur128` print their summary
at *info* level, so `-v error` silently swallows the result and the grep returns empty. Use
`-hide_banner -nostats` and do **not** add `-v error` when the filter output IS the measurement.
