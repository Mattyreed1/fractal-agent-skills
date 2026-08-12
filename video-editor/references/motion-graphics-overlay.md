# Motion-graphics overlays — designed graphic → transparent ProRes → top track

**Empirically verified end-to-end (2026-06-23):** built an animated 7-step numbered list in Fractal AI brand style, rendered it to a transparent ProRes 4444 clip, and placed it on a timeline synced to narration. This is the path for **branded animated text / lower-thirds / numbered lists / callouts** when you want full typographic control.

## When to use this vs native `add_texts`
- **Native Palmier text first** for plain animated text: `add_texts` + `set_keyframes` is a couple of calls and needs no render step. See [palmier-animation.md](palmier-animation.md).
- **This overlay pipeline** when the graphic needs real design — brand fonts, gradients, multi-element layouts, numbered lists, staged reveals, anything you'd build in CSS. Full control of brand font/color/animation, frame-accurate.
- Either way the output is **a clip on a top video track**. Palmier reads ProRes 4444 alpha via `import_media` → `add_clips`; Resolve reads it natively too if the project lives there.
- Related: the [talking-head overlays](palmier-talking-head-overlays.md) playbook uses this same render approach for full-screen brand diagrams (frame-stepped HTML → MP4) and alpha float cards.

## Render pipeline (verified, fast)
This Mac has Playwright in **Python 3.9** (`/Library/Frameworks/Python.framework/Versions/3.9/bin/python3.9`) + managed Chromium; ffmpeg has ProRes.
1. **Author `overlay.html`** at timeline resolution (e.g. 1080×1920), `html,body{background:transparent}`, with a deterministic **`window.setTime(t)`** (t = seconds) that sets EVERY element's state from `t` — do NOT rely on CSS animations/wall-clock (not frame-deterministic). Have `setTime` **return a short signature string** of the frame's visual state.
2. **Capture frames** (Playwright): for `n` in `0..TOTAL`, call `setTime(n/fps)`, screenshot with **`omit_background=True`** → transparent PNG. If the signature == previous frame's, **copy the previous PNG** instead of re-screenshotting — static holds become file copies (≈110 real shots for 1080 frames → ~12s total).
3. Wait for webfonts before the first shot: `page.evaluate("async () => { await document.fonts.ready }")`.
4. **Encode** PNG seq → ProRes 4444 with alpha:
   `ffmpeg -y -framerate <fps> -start_number 0 -i frame_%05d.png -c:v prores_ks -profile:v 4444 -pix_fmt yuva444p10le -r <fps> out.mov`
   Resolve reads ProRes 4444 alpha natively (ffmpeg may store as `yuva444p12le` — fine).

A self-contained `render.py` (Playwright capture + ffmpeg in one script, relative paths) should live next to each project's `overlay.html`.

## Sync to narration
Get word timings from **`get_transcript`** (source seconds per word). Convert to overlay-relative seconds: `t = word_start - overlay_start_seconds`. Drive each reveal in `setTime` off those `t` values, so a reveal lands on the word that names it. Time reveals to the **keyword**, not the sentence.

## Place on the timeline (Palmier)
1. `import_media` the rendered `.mov` — **async**: it returns a placeholder asset id with status `downloading`, which becomes the real id. Poll `get_media({ids:[...]})` before referencing it.
2. `add_clips` with the asset and a `startFrame` — **omit `trackIndex` to auto-create an isolated top track**, which is what you want for an overlay.
3. Verify: `get_timeline(startFrame,endFrame)` for placement, then a rendered spot-check (`capture_frame`) to confirm the alpha composites over the footage rather than onto black.
4. **Confirm no higher track covers the overlay's range** or it won't be visible.

<details>
<summary>If the project lives in Resolve instead</summary>

1. `media_storage.import_to_pool({items:[path]})` → returns a COUNT, not an id. Get the id via `project_settings.project_summary(include_clips=true)` and match by name.
2. `timeline.add_track("video")` → new top track (leaves existing tracks untouched).
3. `media_pool.append_to_timeline({clip_infos:[{media_pool_item_id, startFrame:0, endFrame:N-1, recordFrame:<abs>, record_frame_mode:"absolute", trackIndex:<top>, mediaType:1}]})`.
   - **`recordFrame` is an ABSOLUTE timeline frame** — include the timeline start offset (`timeline.get_start_frame()`, e.g. 86400 = 01:00:00:00). `mediaType:1` = video.
4. Verify: `timeline.clip_where({name_contains:...})`. NOTE: `timeline_item` item_index is **0-based**.
5. Narration timings there come from the subtitle track: `timeline.get_items(track_type="subtitle", index=1)` → each cue's `start`/`end` in timeline frames; `t = (cue_start - overlay_start_frame) / fps`.

</details>

## 🚨 Hard-won gotchas (each cost real time, 2026-06-23)
- **NEVER overwrite a media file the editor is already using.** Replacing a file in place (`cp`/`ffmpeg` over the same path) swaps the inode; the editor loses the clip (Resolve flags it **"Media Offline"**). **Render each revision to a NEW filename** and re-import. In Resolve, recover an offline clip via Media Pool → right-click → **Clip Operations ▸ Reload Clips** (or **Relink Selected Clips** → point at the file) — these live in the **Clip Operations submenu**, NOT the top level of the right-click menu.
- **Render OUTPUT belongs in the project, never `~/Movies` and never the scratchpad.** Rendered overlay clips go to `projects/<brand>-content/<YYYY-MM-DD>-<slug>/assets/renders/`, and the source (`overlay.html`, `render.py`, css/js/data) to `gfx/` in the same folder so it's reproducible. Both are the canonical layout in SKILL.md STEP 0. (Dumped a clip in `~/Movies` once — "why the hell would it be here?")
- **On-screen size/position is a clip transform, not a render decision — non-destructive. Don't bake it into the render** unless asked. Palmier: `set_clip_properties.transform` (center-based) or `set_keyframes` `position` (top-left). Resolve: the Inspector Transform.
- **Preview the design in chat first** (visualize `show_widget`) before the heavy render+import — a cheap approval loop. Compress the preview's timing for watchability; render at the true narration timings.
- Transparent renders show **black on V1** (nothing below) — expected; it's an overlay, so it goes on a top track over the footage.

## Fractal AI brand (for the graphic)
Source of truth: `~/.claude/skills/social-canvas/brand-config.json` + `references/fractal-ai-visual-style.md`.
- **Signature accent = the teal→blue GRADIENT** `linear-gradient(135deg, #00c6a2, #0077ff)` on hero fills (active badge, accent strips, key-word backgrounds). Use **solid `#00c6a2` only for thin strokes/borders**. Flat teal where the brand uses the gradient is the #1 "that's not our color" miss.
- **Sharp corners** (`border-radius:0`) — Fractal is sharp, never rounded/pill.
- bg `#09090b`, surface `#111113`, border `#1c1c22`, text `#fafafa`. **White text + ONE accent; color in small doses** (default is monochrome — white hierarchy carries most of it).
- Font **Geist** per brand-config.json (the visual-style doc lists Outfit Bold / Instrument Sans / JetBrains Mono — confirm per piece). Eyebrow/label = all-caps mono, letter-spaced, and **put any title in its own solid box** so it stays readable over bright footage.
- Load webfonts via Google Fonts `@import`; the renderer waits for `document.fonts.ready`.
