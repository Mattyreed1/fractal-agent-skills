# palmier-pro — Color grading

**REVERSED 2026-07-05 (live v0.6.1 audit): palmier-pro now HAS a full color-grading path via MCP** — `apply_color` (grade) + `inspect_color` (scopes) + `apply_effect` (looks/FX). The 2026-06-22 "no color grading" finding was true of the old surface and is dead as of v0.6.1.

Marks: ✅ = live-verified · ⚠️ = live-validated (server validates the call; a real grade not yet applied).

## The colorist loop
`apply_color` → `inspect_color(clipId[, reference])` → read the gap → adjust → repeat.

- **`apply_color`** ⚠️ — author/refine a grade on video/image clips with named controls. **MERGES** with the clip's current grade (only passed params change; `reset:true` starts from neutral). Applies as live, editable `color.*` effects; non-color effects untouched; undoable. Knobs:
  - **Primaries:** `exposure` (−3…3 EV, linear light), `contrast` (0.5…1.5), `highlights`/`blacks` (−1…1).
  - **Wheels, per tonal zone:** hue (0–360°) + amount — `shadowsHue`/`shadowsAmount`, `midsHue`/`midsAmount` (+ `midsGamma` 0.5…2), `highsHue`/`highsAmount` (+ `highsGain` 0.5…1.5). E.g. teal shadows: `shadowsHue:180, shadowsAmount:0.15`.
  - **Curves:** `masterCurve` (luma, chroma-preserving) + `redCurve`/`greenCurve`/`blueCurve`, each `[x,y]` control points in 0–1. Per-channel curves are tone-selective (pull blue only in the highlights to tame a sky).
  - **Hue curves (secondaries, Resolve Hue-vs-Hue/Sat/Lum style):** `hueCurves.targets[]` — `targetHue` (0–360°) + `hueShift` (±30°) / `satScale` (0–2) / `lumShift` (±0.5), selectivity ~±22°. Desaturate greens, warm skin, no mask needed. Pair with `inspect_color`'s hueHistogram to find present hues.
  - **LUT:** `lut.path` — a real `.cube` file (copied into project storage), `strength` 0–1 blend; replaces any prior LUT.
- **`inspect_color`** ✅ (live-run on a real clip) — measures a timeline clip's GRADED look (`clipId`) or a RAW asset (`mediaRef`): meanRGB, luma black/white points + clip %, 16-bin luma histogram, 12-bin saturation-weighted hueHistogram, per-zone RGB (shadows/mids/highs), white/black RGB, saturation, warm-cool + green-magenta balance — **plus the rendered frame**. Optional `reference` image/video id returns the subject−reference **gap** with hints mapped onto `apply_color` knobs. Grade by the numbers, not by eyeballing.
- **`apply_effect`** ⚠️ — the looks/FX path (distinct from grading): `detail.clarity` (clarity/dehaze), `blur.gaussian`/`blur.sharpen`/`blur.noiseReduction`/`blur.motion`, `stylize.grain`/`stylize.vignette`/`stylize.glow`, `key.chroma` (chroma key). Merge semantics: passed effects add/update by type, `enabled:false` bypasses, `remove:[types]` deletes; params clamp; fixed canonical render order.

Text color (`update_text.color`) remains a separate, text-only field — unrelated to grading.

## Targets to grade AGAINST (backend-agnostic, Rec.709 — verified community standard)

`inspect_color` gives you the measurements; these are the numbers to aim them at. Grade to targets,
not to taste.

- **Skin hue:** sits on the vectorscope skin-tone line ≈ **123°**. Find the actual hue with
  `inspect_color`'s `hueHistogram`, then correct with `hueCurves` (`targetHue` + `hueShift`).
- **Skin saturation:** **20–40%** out from center (light 20–30, medium 25–40, dark 30–50).
  Interview/talking-head work stays low/mid — oversaturated skin is the #1 amateur tell.
- **Face luminance:** light skin **55–70 IRE**, medium **45–60**, dark **35–50**. Read it off the
  luma histogram / per-zone RGB, adjust with `exposure` then `midsGamma`.
- **Black/white points:** deepest intentional blacks **0–3 IRE** (don't crush below), diffuse
  highlights **80–95 IRE**, only speculars near 100. Broadcast-safe = luma **0–100 IRE**.
  `inspect_color` reports black/white points + clip % directly — use the clip % as the guardrail.
- **White balance:** at a neutral (white/gray card, a wall), R/G/B should sit level. `inspect_color`'s
  warm-cool and green-magenta balance are exactly this reading.

### Verified talking-head look (flat indoor footage, light skin)

The intent: **warmer healthier skin, deeper blacks, gentle contrast, modest saturation.** Originally
derived and A/B-verified as a CDL; expressed in `apply_color` knobs:

- `contrast` slightly up (~1.05–1.10) and `blacks` slightly down (~−0.05) — kills the milky lifted
  black and the cool cast in one move.
- `midsHue` ≈ 30° with a small `midsAmount` (~0.08–0.12) — warms skin without going orange.
- Keep saturation modest; the safe-natural skin range is a **±10–15% nudge**. Past ~+25% it reads
  "video-y."
- **Apply the SAME grade to every clip of the same subject/setup** — consistency across cuts matters
  more than any single clip's look.

**Dial looks back.** A LUT or preset look at full strength almost always reads heavy-handed. Apply
it, then pull toward ~50%: `lut.strength` 0.4–0.6, or scale the manual knobs toward neutral. Grading
lighter from the start beats grading hard and regretting it at delivery.

## When to leave for Resolve

**For grading a Palmier timeline, stay in Palmier** — its MCP exposes *more* grading control than
Resolve's scripting API, which is CDL/LUT/DRX whole-grade only (per the verified api_truth ceiling;
per-parameter wheels, curves, qualifiers and power windows are Resolve-**UI** only). Go to Resolve
only when the **project already lives there** or the job needs the full colorist environment
(node graph, qualifier UI, HDR delivery) — never because Palmier can't grade. Interchange:
`export_project({mode:"fcpxml", fcpxmlTarget:"resolve"})`.

## History
- 2026-06-22: pre-0.6 surface verified to have NO color tools (closed schemas + runtime probe `text-only fields 'color' rejected on non-text clips`). Correct then, superseded by v0.6.1.
