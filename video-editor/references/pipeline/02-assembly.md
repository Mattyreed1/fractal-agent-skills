# Pipeline 2 — Assembly / rough cut

**Step 2 of 8** — selects → story order. **Backend:** palmier-pro.

**Goal:** place selected takes in story order. Structure over polish.

- `add_clips` (`startFrame`+`endFrame`, or `source:[startSeconds,endSeconds]`) · `insert_clips`
- `get_transcript` — transcript-driven selects · `manage_tracks` (use stable `trackId`, indexes shift)

**Units:** timeline positions are **frames**, source positions are **seconds**. The tools convert —
never multiply by fps yourself.

**Before moving on:** union the picture spans of every video/image clip across all video tracks
(EXCLUDE text/caption clips — transparent) and confirm no frame in `[0,totalFrames)` is uncovered.
An uncovered frame renders **black**. Then export a `.palmier` checkpoint.

**Call-shape traps** (source-seconds spans truncate rather than round → black gaps):
[palmier-pro.md](../palmier-pro.md).
