# palmier-pro transitions & compositing (verified)

Verified live on a real project (Palmier @ 24fps, 2026-06-25). **Updated 2026-07-05 for the live v0.6.1 surface: blend modes now exist** (see below); no-transition-engine still holds.

## ⭐ THE SQUARE WIPE — the house transition. Build it with animated `crop`, never with black panels (2026-08-10)

**A wipe is a boundary between TWO CLIPS, not a dip to black.** At every frame the outgoing clip is on
one side of the shape and the incoming clip is on the other. If you ever produce
iris-to-black → hard cut → iris-from-black, you have built TWO transitions with a black hole between
them; the user rejects it on sight ("the current and next clip should both be either inside or outside of
the square"). Do not build a black-panel overlay asset for this — the whole thing is native keyframes.

**Recipe (verified live, v0.7.2):** put the incoming/outgoing graphic on the track ABOVE the face, and
animate `crop` on that upper clip. `crop` masks WITHOUT rescaling, so the lower clip shows through the
cropped-away area — that IS the wipe. Insets are `[frame, top, right, bottom, left]`, 0–1 of the frame.

For a 1080x1920 canvas, apertures stepping through a **perfect 540x540 square**:

| aperture | top/bottom | left/right |
|---|---|---|
| 1080x1920 (full) | 0 | 0 |
| 760x1000 | 0.239583 | 0.148148 |
| **540x540 (square)** | 0.359375 | 0.25 |
| 240x240 | 0.4375 | 0.388889 |
| 0 (gone) | 0.5 | 0.5 |

```
entry (square grows, graphic appears):  f0=0.5/0.5 → f1 → f2 → f3 → f4=0/0     (linear)
exit  (square shrinks, graphic leaves): fD-4=0/0 → … → fD=0.5/0.5              (D = clip duration)
```
Both ramps go in ONE `set_keyframes` call (it replaces the whole property track). Generic formula for
a centred WxH aperture: `left=right=(1080-W)/2/1080`, `top=bottom=(1920-H)/2/1920`.

### Where the wipe SITS relative to the cut (gate P0 — get this wrong and the user flags it)

**The graphic is at FULL coverage on the cut frame. The wipe never straddles the cut.** A fullscreen
graphic exists to HIDE the talking-head cut, so the 4 moving frames live entirely on ONE side of it:

```
ENTRY   graphic starts at cut−4 · ramp [cut−4 … cut] runs over the OUTGOING clip
        frame `cut` is ALREADY fully covered  →  the cut happens behind the graphic
EXIT    graphic holds full coverage THROUGH frame `cut` · ramp [cut … cut+4] runs over the INCOMING clip
```

Both moving ranges sit on the far side of the cut from the clip being hidden. The wipe's first frame
is a cut only on the EXIT side; on the ENTRY side the wipe's **last** frame is the cut.
(the user, 2026-08-10: *"the transition should end before the start of the next talking head clip."*
The earlier version of this file said "entry ⇒ graphic starts ON the cut" — that was **wrong** and
produced exactly the defect: 4 frames of the new clip visible before the square swallowed it.)

### ⚠️ The wipe reveals the track BELOW — so name that clip before you key a single frame

A `crop` wipe is not a blend between neighbours. It shrinks the aperture on the UPPER clip and shows
whatever sits **underneath at those frames**. Two consequences, both learned the hard way 2026-08-11:

1. **A graphic→graphic wipe on ONE video track is structurally impossible.** The outgoing clip is a
   same-track neighbour, so it has already ended at the ramp's first frame. There is nothing left to
   wipe *from*, and the growing square reveals V1 — **the talking head — for the full ramp.** It looks
   like a 4-frame face flash in the middle of two full-screen visuals, and it passes every other P0
   clause because the ramp *was* anchored to the V1 cut correctly. You cannot fix it by extending the
   outgoing clip either: that overlaps the incoming one on the same track and Palmier resolves the
   overlap by trimming, which (on a linked clip) propagates into its partner.
2. So the check is: **for every entry ramp, name the clip that will be visible under it.** If the
   answer is "the talking head, and I am trying to hide the talking head", that is a straight cut.

**And do not decorate a cut that hides nothing.** Between two full-cover visuals the face is already
concealed on both sides, so a straight cut on the word is correct and a wipe is pure risk. The click
then lands **ON the cut frame** — the ramp-start+1 rule exists because a ramp's frame 0 shows nothing
yet, and with no ramp there is nothing to compensate for.

**Moving a graphic without disturbing its internal beats** — element pops stay glued to their ticks and
words only if every source frame keeps its absolute timeline frame:

```
earlier by D:  start −= D  AND  trimStartFrame −= D      (needs D frames of HEAD room)
later   by D:  start += D  AND  trimStartFrame += D      (needs D frames of source before the in-point)
```
Check head room with `get_media` → `durationSeconds × fps` vs `trimStartFrame + duration + trimEndFrame`
BEFORE moving; `set_clip_properties` has **no `startFrame`** (position is `move_clips`) and setting
`trimStartFrame` alone slides the content instead of the clip. Sequence: `trimStartFrame` → `move_clips`
→ `durationFrames` to restore the tail.

**No head room?** Re-render the graphic with a D-frame idle head pad — `TOTAL_FRAMES += D` and
`window.seek = F => inner(Math.max(0, F − D))`. Content then lands on the same absolute frames as before
and nothing downstream moves. Do **not** let the content slide early instead, and do **not** stretch it
with `speed` (drags every internal beat off its word). Same trick at the tail: bump `TOTAL_FRAMES` for a
longer settled hold. Verify a padded re-render numerically (mean-abs-diff of raw RGB frames: pad frames
hold ≈0, and `new[N+D]` ≈ `old[N]`) — **MD5 of decoded H.264 frames never matches, even for identical
source frames.**

**Move the transition SFX with its wipe — and land it on the ramp's first VISIBLE frame, which is
ramp-start + 1, NOT the ramp's first keyframe** (the user, 2026-08-11). At keyframe 0 nothing has visibly
changed yet: on an entry the aperture is still fully closed (`0.5/0.5`, graphic invisible), and on an exit
the graphic is still full-frame (`0/0`). The first frame a distinct BLOCK appears on screen is the second
keyframe. The transient belongs there, on the picture event, not one frame ahead of it.

```
entry ramp [cut−4 … cut]   →  click starts at cut−3     (ramp start + 1)
exit  ramp [cut … cut+4]   →  click starts at cut+1     (ramp start + 1)
```
Keep the click 4 frames long at `volumeDb −6.021`. Delete any element tick whose element now falls inside
a trimmed head; the wipe's own click covers it.

## Headline: Palmier has NO transition engine (still true on v0.6.1)

- No built-in transitions, no presets, no "apply transition" tool — confirmed against the live v0.6.1 manifest (49 tools, none transition-shaped). Nothing like CapCut's transition library or a Premiere/Resolve transition object. (`apply_effect` is a per-clip FX stack — blur/grain/vignette/glow/chroma-key — not transitions.)
- `import_media` imports **media only** (video / audio / image) — never effects or presets. There is **no transition-pack format to install.**
- So **every transition in Palmier is hand-built from keyframes** on clip properties: `opacity`, `position`, `scale`, `rotation`, **`crop` (the square wipe — see the top of this file, it is the house transition)** (+ track layering). Don't tell a user Palmier "has" a transition — it has the primitives to construct one.

## Blend modes — v0.6.1 ADDED them (supersedes the old "no blend modes" hard limit)

- `set_clip_properties.blendMode` (video/image clips): `normal`, `darken`, `multiply`, `colorBurn`, `lighten`, **`screen`**, `colorDodge`, `overlay`, `softLight`, `hardLight`, `difference`, `exclusion`, `hue`, `saturation`, `color`, `luminosity`. `normal` clears. Doesn't propagate to linked partners; rejected on text/audio clips. ⚠️ schema-verified, not yet composite-tested.
- Consequence: an "on-black" overlay (film burn, light leak, flare, glitch) should now composite directly with `blendMode:"screen"` — no ffmpeg pre-key. Until a live composite check confirms it, the alpha route below stays the ✅ verified path. (Pre-0.6 builds: `opacity` only — the alpha route is the ONLY way there.)
- `create_matte` (v0.6.1) makes solid-color frames in one call — the fade-to-white white frame no longer needs an imported PNG. ⚠️ **Not present on the tool manifest observed 2026-07-29** — it may have been renamed or removed after v0.6.1. Check the live manifest before relying on it; if it's gone, fall back to generating a solid-color PNG/MP4 and `import_media`.
- `apply_effect` `key.chroma` (v0.6.1) adds real chroma keying (keyHue/tolerance/softness/spill) — green-screen composites inside Palmier, ⚠️ schema-verified.

## Palmier honors an alpha channel (verified) — the pre-keyed overlay route

- A **ProRes 4444 `.mov` with a real alpha channel composites correctly** via plain opacity (verified: a 50%-alpha clip showed the layer beneath through it). Palmier import accepts `.mov`.
- Pipeline to use any CapCut-style overlay transition pack in Palmier:
  1. Download the overlay (on black), royalty-free.
  2. **ffmpeg: luma-key black → alpha**, encode ProRes 4444, fit to the timeline frame:
     ```
     ffmpeg -i in.mp4 -vf "scale=W:H:force_original_aspect_ratio=increase,crop=W:H,\
     format=yuva444p10le,lumakey=threshold=0.04:tolerance=0.22:softness=0.14" \
     -c:v prores_ks -profile:v 4444 -pix_fmt yuva444p10le -r FPS out.mov
     ```
  3. `import_media` (path) → `add_clips` on a top track over the cut → `set_keyframes` opacity for ignite/recede.
- On pre-0.6 builds this is the ONLY way to get a real burn/flare/glitch transition; on v0.6.1 try `blendMode:"screen"` first and keep this as the verified fallback.
- **Pick footage actually designed as a transition** (ignites and consumes the whole frame edge-to-edge). Do NOT key a generic clip (e.g. a campfire) and call it a transition — keyed flames just float over the shot. That mistake was made and called out this session.

## What Palmier does well (keyframe-native, no caveats)

- **Fade to black** — native. Ramp a clip's `opacity` 1→0 (or 0→1). With nothing beneath, Palmier's empty canvas is black, so it fades to black correctly. A fade *is* an opacity ramp — the genuine article, not a hack.
- **Fade to white** — same, but needs a **white frame** in the stack (fade the clip out to reveal white below, or fade a white frame in on top). Every editor composites white this way internally.
- **Crossfade / dissolve** — overlap two clips on **different tracks**, fade the top one's opacity (or the incoming in). Constraint: the two media must be on separate tracks during the overlap, so you need a free track in the overlap window (titles occupying upper tracks limit where the overlap can sit).
- **Push / slide / zoom / spin / wipe** — `position` / `scale` / `rotation` / `crop` keyframes across the cut.
- **Flash** — a white frame opacity-popped (~2-frame up, fade down). This is a *flash*, NOT a film burn (a flash has no texture). Don't conflate them.

## Audio transition SFX — fully supported, frame-exact

- Audio is just clips on audio tracks, and everything is frame-addressed → an SFX pins to the exact frame of any video transition.
- `import_media` the SFX → `add_clips` at the target `startFrame` → `trimStartFrame` to align the **transient** (a click's transient is at the file start; a whoosh/riser's impact is near the end) to the transition frame → `set_keyframes` volume to shape. Use `inspect_media` to locate the transient.
- Caveat: `inspect_timeline` is **visual only** — you cannot audition the mix from the MCP. Align by frame math + known transient position; the user does the final listen in Palmier.

## Generation gotchas (transitions rarely need it, but)

- `list_models` can return `loaded:true` while `get_timeline.canGenerate` is still **false** — catalog sync ≠ generation entitlement. If `canGenerate` is false, every `generate_*` call FAILS (and generation costs money + is not undoable). Don't attempt it.
- The only SFX generator is **`mirelo-sfx-v1.5-video-to-audio`** — it takes a **video span, not a text prompt** (scores SFX to footage). There is no text→SFX "make a click" model; TTS/music models won't produce a designed transition sound. For a specific click/whoosh, import a real SFX file (faster + tighter than AI).

## import_media notes

- `source.path` = absolute local file. **v0.6.1 changed this: the file is now COPIED into the project in the background** (a path may even be a directory, imported recursively) — the ≤v0.3.x referenced-in-place `/tmp` footgun is gone on current builds. On old builds, keep using a stable assets folder.
- `source.url` (HTTPS, ≤1 GB) downloads in the background (async, like `generate_*`); `source.bytes` (base64, ≤~11 MB binary) finalizes synchronously. Accepts video (mov/mp4/m4v), audio (mp3/wav/aac/m4a/aiff), image (png/jpg/jpeg/tiff/heic). **ProRes 4444 `.mov` preserves alpha.**

## Sourcing royalty-free assets (scriptable)

- **Mixkit CDN is scrapeable** (royalty-free, no attribution required): an SFX preview *is* the full sound at `assets.mixkit.co/active_storage/sfx/<id>/<id>-preview.mp3`; stock video at `assets.mixkit.co/videos/<id>/<id>-720.mp4`. Category pages: `mixkit.co/free-sound-effects/<cat>/` and `mixkit.co/free-stock-video/<cat>/`. Parse `<h2 class="item-grid-card__title">` titles + the `preview-url-value` / `-720.mp4` URLs and zip by order. Use a browser User-Agent — `urllib` gets blocked, `curl` works.
- **Pixabay and Pexels block scraping (403).** Use their APIs (keyed) or another source.
- Mixkit's free *film-burn* selection is thin (mostly light leaks + literal fire). For a clean celluloid burn, expect to source elsewhere or build procedurally.
