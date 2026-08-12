# Pipeline 6 — Color grading (+ conform/online)

**Step 6 of 8** — finishing, **near the end**: after VFX/titles, before delivery. **Conform/online**
(relink the locked edit to full-res media) precedes the grade. **Backend:** palmier-pro.

**Why here:** grade the *finished, locked* image so you don't grade shots you later cut, and the look
lands on what ships. (Light correction/matching happens throughout; the creative **grade** is here.)

- `apply_color` ⚠️ — exposure/contrast/highlights/blacks, per-zone wheels, master + R/G/B curves,
  hue-qualified secondaries, `.cube` LUT + strength. **MERGES** with the current grade (`reset:true`
  starts neutral).
- `inspect_color` ✅ — scopes, histograms, per-zone RGB, balance, **plus the rendered frame**;
  optional `reference` returns the gap mapped onto `apply_color` knobs.
- `apply_effect` — looks/FX: grain, vignette, glow, clarity/dehaze.

**The loop:** `apply_color` → `inspect_color` → read the gap → adjust → repeat. **Grade to numeric
targets, not by eye** — skin-hue/saturation/IRE targets, the verified talking-head look, and the
"dial looks back to ~50%" rule: [palmier-color.md](../palmier-color.md).
