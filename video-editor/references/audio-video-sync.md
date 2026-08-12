# Audio/Video Sync (double-system sound)

Sync an external clean audio take to camera footage, then mute the camera's scratch audio so only the clean audio is audible, locked to picture. Efficient, verified replay of the manual procedure.

> **Fast path (try first): `sync_clips`** — the tool is named `sync_clips`, NOT `sync_audio` (that name appears in older notes and will fail). Call `sync_clips({referenceClipId: THE_VIDEO_CLIP, targetClipIds: [THE_CLEAN_AUDIO_CLIP], searchWindowSeconds: 30})`. It shifts the targets on the timeline and returns `offsetFrames`, `confidence` (0–1; refuses below `minConfidence`, default 0.5) and **`method`** per target.
>
> **Mode `auto` (the default) tries embedded source TIMECODE first** — when both files carry one, the align is exact at confidence 1.0 — and falls back to audio cross-correlation (seeded by capture dates when present). Force one with `mode: "timecode" | "audio"`. So on double-system footage from timecode-capable gear this is a solved problem: check `method` in the response to know which you got. **Refused on multicam clips** — a group's members are already aligned by its sync maps (`manage_multicam`).
>
> The reference clip stays put unless a target would land before frame 0, in which case the whole group shifts right together (reported as `shiftedFrames`) — so re-read frame numbers after syncing.
>
> Then mute the scratch track and gate with `scripts/eval_sync.py` as below. Fall back to the manual by-content procedure when `sync_clips` refuses (weak correlation) or the material lacks a scratch track.

## When
Two imported assets: a camera **video** (type video, hasAudio) and a separate **clean audio** take (type audio), recorded simultaneously (double-system). Names/durations usually close (within seconds).

## Procedure

**0. Read state.** `get_timeline` (fps — usually 30); `get_media` (grab the video and audio asset `id`s).

**1. Measure the offset by content — never assume frame 0.** `inspect_media` both assets at an **early** window with `wordTimestamps:true` (e.g. `startSeconds:0, endSeconds:75`). Cross-match scripted words (ignore the slate / "check check"). For each shared word compute `Δ = audio_time - video_time`. Take the **mode** over several clean words. (Example seen: a constant +0.84s.)

**2. Confirm no drift.** Repeat `inspect_media` at a **late** window (near the end).
- Same Δ -> constant offset, single-point sync works (continue).
- Δ grew -> clock drift: set the clean audio `speed = video_span / audio_span` via `set_clip_properties`, then re-measure. (Rare; flag to the user.)

**3. Compute trim.** `trimFrames = round(Δ * fps)` (e.g. 0.84 * 30 = 25).

**4. Lay down the video.** `add_clips [{ mediaRef: VIDEO, startFrame: 0, durationFrames: round(videoDurSec * fps) }]` — **omit `trackIndex`**. This creates V1 **and** a linked scratch-audio clip on a new audio track. Note the returned video clipId + scratch-audio clipId (or read them from `get_timeline`); the scratch audio shares the video's `linkGroupId`.

**5. Lay down the clean audio.** `add_clips [{ mediaRef: AUDIO, startFrame: 0, durationFrames: round(audioDurSec * fps) - trimFrames }]` — **omit `trackIndex`** (it inserts a fresh audio track; do not pass an out-of-range index).

**6. Sync + mute** (two `set_clip_properties` calls, can run in parallel):
- Clean audio clip: `trimStartFrame: trimFrames` — advances it to match (audio was late, so trim its head to pull it earlier). In-point only; timeline position unchanged.
- Scratch audio clip (the one sharing the video's `linkGroupId`): `volume: 0`. Per-clip, will not touch the video. Mute, do not delete (reversible; stays linked so it follows future video trims).

**7. Verify (required).** `inspect_media` the **video clip** and the **clean-audio clip** with their `clipId` (times then return as **project frames**), same early window, `wordTimestamps:true`. Cross-match unique shared words: median `|Δframe|` must be **<= 5** (several land dead-on). Confirm via `get_timeline` that scratch is `volume:0` and the clean clip carries `trimStartFrame`. Or just run `scripts/eval_sync.py`.

## Direction & gotchas
- **Audio late (Δ > 0)** -> trim the audio head (`trimStartFrame = +frames`). **Audio early (Δ < 0)** -> cannot trim a negative head; instead delay it: `startFrame = round(-Δ * fps)`, `trimStartFrame: 0`.
- `trim` is a **source in-point**, not a ripple — `startFrame`/`durationFrames` stay; content shifts.
- The clean audio is **independent** (no `linkGroupId`) — a later ripple-trim of the video will not move it. Trim both together or re-sync.
- 29.97 vs 30 fps: use `durationFrames = round(sourceSec * projectFps)`; the sub-frame rounding is inaudible.
- Clean audio often runs a few seconds longer than the video — harmless tail overhang; trim if wanted.
