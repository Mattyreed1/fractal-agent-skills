# Pipeline 4 — VFX, motion graphics & titles

**Step 4 of 8** — **finishing begins** (after picture lock).
**Backend:** palmier-pro, with ONE exception (below).

**Goal:** animated text/titles, PIP moves, fly-ins, keyframed motion, simple compositing.

- `set_keyframes` ✅ — `position`/`scale`/`rotation`/`opacity`/`volume`/`crop`, one property per call
- `add_texts` — titles, lower-thirds, callouts · `apply_layout` — split screen / PIP / grid
  (**use this, never hand-set transforms**) · `apply_effect` — blur/sharpen/grain/vignette/glow/key

Coordinate + unit traps (top-left vs center, normalized scale, clip-relative frames):
[palmier-animation.md](../palmier-animation.md).

**Branded** animated text (brand fonts, gradients, staged reveals) → design in HTML/CSS, render
transparent ProRes 4444 onto a top track: [motion-graphics-overlay.md](../motion-graphics-overlay.md).

## ⚠️ The one exception — AI background removal
**Palmier cannot cut a subject out of a real background** (`key.chroma` is its only keying effect and
needs a keyable backdrop). Normal room behind a talking head → Resolve **Magic Mask 2** (Color-page
UI), render an alpha codec, import back into Palmier:
[davinci-background-removal.md](../davinci-background-removal.md).
