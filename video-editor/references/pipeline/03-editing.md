# Pipeline 3 — Editing / fine cut (→ picture lock)

**Step 3 of 8** — trims, timing, transitions, B-roll. Ends at **picture lock**.
**Backend:** palmier-pro — the clearest case for it: Resolve's API cannot trim, move, slip, slide,
roll, or split a clip at all, nor add transitions.

**Goal:** tighten to final timing, then lock picture so finishing can begin.

- `split_clips` · `move_clips` · `set_clip_properties` (trim/speed/duration) · `remove_clips` · `undo`
- `ripple_delete_ranges` — cut ranges and close the hole · `remove_silence`
- `remove_words` ⚠️ — Descript-style cuts by transcript word index or filler `matches`

**Rules:** apply ripple deletes **right-to-left** (each cut shifts everything after it). Cut only in
true silence, anchored to the spoken word. **Never fill a gap by extending the preceding clip** —
that re-adds the dead air you removed.

**Picture lock is real** — captions and graphics are timed to cut frames, so a later ripple desyncs
all of them. Gate the cut before step 4.

Method + gates: [radio-edit.md](../radio-edit.md) · transitions (keyframe-built, no engine):
[palmier-transitions.md](../palmier-transitions.md).
