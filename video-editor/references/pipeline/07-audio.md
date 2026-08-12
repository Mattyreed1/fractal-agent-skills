# Pipeline 7 — Audio / sound mix

**Step 7 of 8** — finishing, usually in parallel with color. **Backend:** palmier-pro. (Resolve has
**no** Fairlight control via API — no volume, pan, EQ, automation. Mixing there is UI work.)

**Goal:** level/balance dialogue, music, SFX; clean and sweeten. Plus lay a music bed.

- **Arrange:** `add_clips` / `move_clips` / `split_clips` / `set_clip_properties` — per-clip
  `startFrame`/`trimStartFrame` is how SFX land frame-exact on a cut.
- **Level:** `volume` static via `set_clip_properties`, animated via `set_keyframes` (setting a static
  **clears** the keyframe track — statics first).
- **Clean:** `denoise_audio` ⚠️ · **Sync:** `sync_clips` (timecode-first, see step 1)
- **Generate:** `generate_audio` (TTS/music/SFX — subscription-gated) · `detect_beats`

## G0 — level the dialogue BEFORE take selection
Quiet sentence-tails read as silence and make you cut pacing that isn't there. If tails sit >6 dB
down, level them (raise tails, don't slam a limiter — keep the noise floor and gaps intact). Compute
cut boundaries on the **raw** audio (the true silence structure); the leveled track is only the
delivered voice.

## Music bed — Fractal AI standard
ONE clip, **static `volume` 0.056 (−25 dB), zero keyframes**, lowpass ~6500 Hz, own track under the
voiceover. Ship-check: audible but ≥18 dB below voice peaks. Source pool:
`…/Grow Audience/audio-assets/bg-music/` (currently `Sakura Trees.mp3`, 1:40).

**Longer than the track? THE SAKURA SPLICE — exact, non-negotiable (the user, 2026-07-30).**
No loop/auto-extend exists. Butt-join copies at these EXACT source times, same every video:

- **Copy 1: source `0 → 99.083s`** — cut BEFORE the file's end (file runs 100.075s; the last
  ~1s is decay tail — including it makes the seam sound like a restart after a fade-out).
- **Every subsequent copy: source `9.083s → onward`** (skips the soft intro; at 99.083 the
  outgoing energy matches the 9.083 entry point, so the song just continues).
- **Butt splice: zero gap, zero overlap, no crossfade.** Last copy trimmed to content end.

Ground truth read directly from the user's own edit (DaVinci project **"Apple Park Agents"**,
Audio 2, 24fps: clip 1 = source frames 0–2378 [0→99.0833s], clip 2 = source start frame 218
[9.0833s], adjacent at one frame — verified via `timeline_item get_source_*_time`, 2026-07-30).
Do NOT re-derive, estimate, or "improve" these numbers. ffmpeg build:
`atrim=0:99.0833` ++ `atrim=9.0833:<fill>` → one wav → ONE timeline clip.
Source spans are seconds; timeline positions are frames.

⚠️ **Never ripple-cut across a continuous music bed** — it splices the melody. The jump is obvious to
a listener but transient/energy checks pass it clean. Cut picture first, then lay music.
