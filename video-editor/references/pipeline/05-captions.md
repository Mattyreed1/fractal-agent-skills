# Pipeline 5 — Captions / subtitles

**Step 5 of 8** — finishing. **Backend:** palmier-pro. ✅ runtime-verified.

**Goal:** captions synced to the spoken words; styled, word-level/karaoke, editable.

- `add_captions` — styled auto-transcribed cues (`animation` karaoke presets, `maxWords`,
  `highlightColor`, `color`, `fontName`/`fontSize`, `centerX`/`centerY`, `textCase`, `language`)
- `update_text` — per-cue content (`clipIds`) or group-wide restyle (`captionGroupId`)
- `get_transcript` — word timings, for timing graphics to keywords

**Sequencing:** caption AFTER the cut is gated. Captions do not follow ripple/word cuts (not linked
partners), so a later cut orphans them and forces a full re-caption.

**Gate caption text against the SCRIPT, not the ASR** — the same ASR errors recur identically on
re-transcription.

v0.6.5 regressions (`update_text` clears word timings; main-audio-track only; `{clipIds}` duplicates
the whole set), the recut runbook, and the single-line character budget:
[palmier-captions.md](../palmier-captions.md).
