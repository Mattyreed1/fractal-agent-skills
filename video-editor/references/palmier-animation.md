# palmier-pro — Animation (keyframes & motion)

**Empirically verified on Palmier (fps 30 project) 2026-06-22.** Confirmed by both storage readback (`get_timeline`) and visual render (`inspect_timeline`) of an animated test clip. Unlike DaVinci, palmier has **native, first-class keyframe animation** — this is the backend to reach for when the task is "animate."

## TL;DR
One tool — `set_keyframes` — animates `position` (2D), `scale`, `rotation`, `opacity`, `volume`, `crop`, each with per-keyframe interpolation. Everything the DaVinci API *couldn't* do (Edit-page keyframes, 2D position, easing) works here directly.

## What works (verified by running it)
| Capability | How | Evidence |
|---|---|---|
| **Zoom** | `set_keyframes(clipId, "scale", [[0,0.5,0.5],[99,1,1]])` | clip grew across rendered frames 3010→3090 |
| **Fly-in / pan / 2D move** | `set_keyframes(clipId, "position", [[0,0,0.25],[99,0.5,0.25]])` | clip slid left→right on screen |
| **Rotation** | `set_keyframes(clipId, "rotation", [[0,0],[99,90]])` | clip rotated clockwise |
| **Fade** | `set_keyframes(clipId, "opacity", [[0,0],[99,1]])` | clip faded 0→1 |
| **Easing / interpolation** | per-row 4th element: `linear` \| `hold` \| `smooth` (default `smooth`) | readback stored `linear` explicitly; `smooth` omitted as default |
| **Path trace** | N position rows (≥3) trace a multi-point path | 2-point verified; N-point is the same mechanism |
| Read back / verify | `get_timeline(startFrame,endFrame)` shows stored keyframe tracks; `inspect_timeline(startFrame,endFrame,maxFrames)` renders the composited result | used for all of the above |

## set_keyframes reference
- **One property per call.** Each call **replaces** that property's whole track; pass `[]` to clear it.
- **Frames are CLIP-RELATIVE** (0 = first frame of the clip), so keyframes follow the clip when it moves. (DaVinci/Fusion used comp/timeline frames — different.)
- **Row shape:** `[frame, ...values, interp?]`, `interp ∈ {linear, hold, smooth}`, default `smooth`.
- **Value layouts (mind the units — these bit-traps differ from `set_clip_properties`):**
  - `opacity` / `volume`: `[frame, value]` — 0.0–1.0
  - `rotation`: `[frame, degrees]` — clockwise
  - `position`: `[frame, topLeftX, topLeftY]` — **TOP-LEFT** corner, 0–1 normalized (NOT center; a centered full-canvas clip's top-left is (0,0))
  - `scale`: `[frame, width, height]` — normalized canvas size 0–1 (1.0 = fills that axis; **NOT a scale multiplier**)
  - `crop`: `[frame, top, right, bottom, left]` — source insets 0–1
- Motion keyframes (position/scale/rotation) **override** the clip's static `transform` while active.

## Working recipe (end-to-end, verified)
1. `get_timeline` — fps, tracks, clips, `canGenerate`. Get a `clipId` (or `import_media` → `add_clips`; omit `trackIndex` to auto-create an isolated track).
2. `set_keyframes` once per property (examples above). Frames are clip-relative to that clip's length.
3. Verify: `get_timeline(startFrame,endFrame)` (windowed) for stored tracks; `inspect_timeline(startFrame,endFrame,maxFrames=5)` to *see* it animate.
4. Undo/cleanup: `undo` (last edit), or `remove_clips` (also auto-prunes an emptied track), or `delete_media`.

## Gotchas
- **`position` is top-left; `set_clip_properties.transform` is center.** Switching between static and keyframed positioning means converting coordinates.
- **`scale` is normalized size, not a factor.** 0.5 = half-canvas, not "50% of current."
- **Easing is `smooth` (symmetric ease-in-out) only** — there is no distinct ease-in vs ease-out option. Use `hold` for steps, `linear` for constant rate.
- **`set_clip_properties` with `opacity`/`volume` CLEARS that property's keyframe track.** Set statics first, animate second.
- **Generation is gated:** this project had `canGenerate:false` (not signed in/subscribed). Keyframing/editing does NOT need it, but `generate_*`/`upscale_media` will fail until signed in.

## Animation is Palmier's, full stop

One tool, one call per property, native easing. Resolve is not an alternative here: its Edit-page
keyframe API is broken on R21, 2D-position keyframes are a silent no-op, and easing requires
hand-written Fusion expressions — so motion there means building a Fusion graph per clip. Animate
in Palmier. For **branded** animated text (lower-thirds, numbered lists, callouts) where you want
full typographic control, the alternative is a designed overlay rendered to transparent ProRes —
see [motion-graphics-overlay.md](motion-graphics-overlay.md).
