# palmier-pro backend

An **AI-native video editor**. Tool names are `mcp__palmier-pro__<tool>` (flat tools, not action-dispatch). This is the backend for AI generation and fine programmatic timeline editing.

> **Audited 2026-07-05 against the LIVE v0.6.1 (build 63) server** (`tools/list` straight off the localhost bridge, not a cached client manifest): **49 tools** — 18 new vs the previously documented surface, 1 rename (`split_clip` → `split_clips`). v0.6.1 closed every gap that used to force UI/computer-use workarounds: caption/text content editing (`update_text`), caption animation presets (`animation` on `add_captions`/`update_text`), project settings (`set_project_settings`), and audio denoise (`denoise_audio`) — plus full color grading (`apply_color`/`inspect_color`), an FX stack incl. chroma key (`apply_effect`), blend modes (`set_clip_properties.blendMode`), multi-clip layouts (`apply_layout`), multi-timeline (`create/duplicate/set_active_timeline`), project management (`get_projects`/`new_project`/`open_project`), export (`export_project`: H.264/H.265/ProRes render + XMEML/FCPXML/.palmier), audio auto-sync (**`sync_clips`** — this note originally recorded it as `sync_audio`, which is wrong and will fail), and Descript-style word removal (`remove_words`).

## v0.7.2 delta (ai-notetaker polish build, 2026-08-10 — all live-verified)

**Breaking + new surface.** Palmier auto-updates via Sparkle; check the version FIRST every session.

| Change | Detail |
|---|---|
| `set_clip_properties` **`volume` → `volumeDb`** | BREAKING rename. Linear→dB: `dB = 20*log10(v)` (0.5→−6.02, 0.32→−9.90, 0.18→−14.9, 0.056→−25.04). `get_timeline` reports `volumeDb` too. |
| New `set_clip_properties` fields | `fadeInFrames`, `fadeOutFrames`, `fadeInInterpolation`, `fadeOutInterpolation`, `edgeRounding`, `edgeSoftness` — use these instead of hand-rolled opacity keyframes for simple fades. |
| New tools | ⚠️ **CORRECTION 2026-08-10: there is NO `swap_clip_media` and no `manage_clip_links` on the live v0.7.2 manifest.** This row previously claimed both existed — written from a changelog, never checked against the running app, and it cost a wasted call mid-edit. **Re-rendering a graphic means `import_media` → `remove_clips` → `add_clips` → re-apply `set_keyframes`** (keyframes do NOT survive the swap; the new clip gets a new id). Read the manifest via ToolSearch before asserting a tool exists — a changelog is a claim, the manifest is the evidence. |
| `inspect_timeline` | ✅ WORKS again — the v0.6.5 stuck-at-frame-0 bug is gone. Distinct composited frames with correct burn-in. It is now the fastest transition/composite check; no render needed for spot checks. |
| `crop` keyframes | Mask WITHOUT rescaling → this is what makes the two-clip square wipe possible. See [palmier-transitions.md](palmier-transitions.md). |

### "Editor not available" does NOT mean the app is closed — check `manage_project` FIRST
A relaunch (e.g. after an auto-update) can leave Palmier on the Home screen with **no project loaded**,
and every editor tool then returns `Editor not available` while the MCP server itself answers fine.
**`manage_project {action:"list"}` → `openCount: 0` proves it, and `{action:"open", id}` fixes it
yourself — do not send the user to the app for this.** Only if the app process is genuinely absent
(`ps aux | grep PalmierPro`) is it a "start the app" problem. Cost 40 min on 2026-08-10.

### Escape hatch: the client caches the tool manifest — talk to the app directly
Claude Code caches the MCP tool schemas from session start, so after an app update **new tools and
renamed fields are invisible and get silently stripped from your calls** (`volumeDb` vanished →
"needs at least one property"). A client restart fixes it; when you can't restart, drive the app's own
JSON-RPC endpoint. The project binding is PER SESSION, so you must open the project in your curl
session too:
```bash
U=http://127.0.0.1:19789/            # the app's local MCP server (lsof -nP -iTCP -sTCP:LISTEN | grep -i palmier)
H=(-H 'Content-Type: application/json' -H 'Accept: application/json, text/event-stream')
SID=$(curl -s -D - -o /dev/null -X POST $U "${H[@]}" \
  -d '{"jsonrpc":"2.0","id":0,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"ea","version":"1"}}}' \
  | awk -F': ' '/MCP-Session-Id/{print $2}' | tr -d '\r')
curl -s -X POST $U "${H[@]}" -H "MCP-Session-Id: $SID" -d '{"jsonrpc":"2.0","method":"notifications/initialized"}'
curl -s -X POST $U "${H[@]}" -H "MCP-Session-Id: $SID" -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"manage_project","arguments":{"action":"open","id":"<PROJECT-UUID>"}}}'
# now any tools/call works, with the CURRENT schema
```
Responses are SSE: take the last `data: {...}` line, then `json.loads(r['result']['content'][0]['text'])`.
Same undo history as the normal path. Also the cheap way to run a big `get_timeline` through a script
without dumping it into context.

### Emptying a track DELETES it — never reuse a track index across a remove
`remove_clips` that empties a track drops the track and **shifts every index below it** (the response
says `Track indices shifted — re-read get_timeline`). On 2026-08-10 a music-bed `add_clips` at the
remembered index 7 landed on the SFX track and overwrote 41 tick/click clips. One `undo` restored it.
**Re-read `get_timeline` after any remove before an index-based call, or omit `trackIndex` and let
`add_clips` create a track.** (Companion to the Track-index safety section below.)

### `get_transcript` inherits CACHED source alignment across a trim
After trimming a clip's head, words whose cached source timestamps fall before the new trim point
**silently disappear from `get_transcript`** even though they are audible. So the timeline transcript
can show a line starting mid-sentence when the audio is fine. Two consequences: (1) never conclude a
word is missing from the timeline transcript alone; (2) **P7 duplicate scans run on RENDERED audio.**
To resolve any ambiguous take boundary, ffmpeg the candidate span to a NEW file and `import_media` +
`inspect_media` it — a fresh asset forces a real transcription. Windowed `inspect_media` on an
already-transcribed asset just replays the cached sentence alignment and cannot settle it.

## Linked-audio + track hazards (ai-notetaker hook build, 2026-08-11 — all live-hit)

**⚠️ B-roll linked audio must NOT share a track with your SFX.** `add_clips` auto-places a video
clip's linked audio on an existing audio track — on this build it chose **A3, the SFX track**. Adding
a 4-frame click that overlapped it trimmed the audio, and **the trim PROPAGATED to the linked VIDEO
partner: the b-roll split into 3 fragments and its crop keyframes were shredded.** `undo` recovered
it. The linked-timing propagation documented for `set_clip_properties` also fires on `add_clips`
overlap resolution — treat ANY overlap with a linked clip as a timing edit on its partner.
- **Fix A (preferred):** sequence placements so linked audio lands *adjacent*, never overlapping —
  move the existing clip to its final position FIRST, then add the neighbour.
- **Fix B:** `add_clips` with `trackIndex` **omitted** creates a fresh audio track for the new clip.
- **`manage_tracks` CANNOT create tracks** — it only reorders, sets (`hidden`/`muted`/`syncLocked`)
  and removes. There is no add-track tool; `add_clips` is the only way to make one.

**✅ Closing a cutout without splicing the music bed — the verified recipe.** To ripple gaps closed
across every track while leaving a full-length music bed untouched:
```
ripple_delete_ranges {trackIndex: <V1>, ranges: [[start,end]], units: "frames",
                      ignoreSyncLockedTracks: [<music track index>]}
```
Everything else shifts left; the excluded track is neither cut nor shifted, so the melody is never
spliced (the documented music-bed hazard). The bed is then 11-ish frames long — fix with
`set_clip_properties {durationFrames: <new total>}`, i.e. TRIM the tail, never ripple through it.
The call returns a `shifted` report (`{track, by, count, fromFrame}`) — that report is authoritative
for recomputing downstream frame numbers, so you do not need a full re-read to do the arithmetic.

**Exact argument names — sibling tools disagree, so read this instead of recalling (2026-08-11, 4 wasted calls):**
| Tool | Correct shape |
|---|---|
| `set_clip_properties` | `{clipIds:[...], durationFrames, volumeDb, ...}` — **`clipIds`**, not `clips` |
| `add_clips` | `{entries:[{mediaRef, trackIndex, startFrame, endFrame}]}` — **`entries`**, not `clips` |
| `move_clips` | `{moves:[{clipId, toFrame, toTrack}]}` — **`toFrame`**, not `startFrame` |
| `import_media` | `{source:{path}|{url}|{bytes}, name}` — a single **`source` object**, not `paths[]` |
| `set_keyframes` | `{clipId, property, keyframes:[[frame, v1, v2, ...]]}` — **arrays**, not `{frame,value}` objects |
| `capture_frame` | exactly ONE of `timelineFrame` **or** `mediaRef`+`sourceSeconds` (a number); no `frames[]` |
| `ripple_delete_ranges` | `{trackIndex, ranges:[[a,b]], units:"frames", ignoreSyncLockedTracks:[idx]}` |
Clearing an animated property: pass a single keyframe at frame 0 holding the neutral value
(`crop [[0,0,0,0,0]]`) — the read-back then returns the clip with no `keyframes` block.

**`inspect_timeline` is the cheapest visual verification available and it renders the REAL composite**
(all tracks, captions included) at ~288x512 for a sampled set of frames in a range. Use a narrow range
to pin exact frames. It is heavy: two calls in quick succession timed out the bridge with
`Server palmier-pro unavailable`, which clears on its own — do useful work and retry, don't restart the app.

**✅ Cutout-PIP z-order recipe (verified 2026-08-11).** Target stack, top → bottom:
**captions → cutout → graphics → face.** Do NOT build it by creating a new track (see the hazard
below). Instead put the cutout on an EXISTING top track with `trackIndex` set, then promote the
caption track above it:
```
add_clips {entries:[{mediaRef:<cutout>, trackIndex:0, startFrame:0, endFrame:N}]}
set_clip_properties {clipIds:[<id>], transform:{width:.5,height:.5,centerX:.25,centerY:.75}}
manage_tracks {reorder:[{trackId:"<captions>", to:0}]}     // trackId, never index
```
`manage_tracks reorder` **by `trackId` was clean every time**; it is `add_clips` without a
`trackIndex` that does the damage. Verify with `inspect_timeline` over a short range (a 100+ frame
range intermittently times out — sample 3–6 frames).

**Alpha into Palmier:** ProRes 4444 (`yuva444p10le`) imports and composites correctly, and
`transform` (a single-clip tweak) is the right tool for a free-floating cutout — **not** `apply_layout`,
whose PIP presets crop to a rectangle and would destroy the cutout silhouette. `set_clip_properties`
says PIP belongs to `apply_layout`; that guidance is for multi-clip canvas arrangements, not for one
transparent clip floating over a background.

**🚨 `add_clips` WITHOUT `trackIndex` is destructive — always pass an explicit `trackIndex` (2026-08-11).**
Omitting it to "let Palmier make a new track" created the track *and* reassigned existing clips across
tracks: the hook graphic jumped from the graphics track onto V1 (so it rendered UNDER the face), and
the first talking-head clip landed alone on a brand-new track. The response's own
`notes:["Track indices shifted — re-read get_timeline before the next index-based call."]` is the
warning; treat it as an ERROR, not a note. **And `undo` does not reliably revert it** — four undos left
the track scramble and a 28-frame timeline-length change in place, and a clip that had been undone
reappeared in a later frame report as a duplicate. Recovery is forward-only: re-read `get_timeline`,
`move_clips {toTrack}` / `remove_clips` the strays, and re-add with an explicit `trackIndex`.
**Checkpoint before any track-structure change** — `backups/*.palmier` was 2h stale when this hit.
Placing on an EXISTING track with `trackIndex` set was clean every time.

**Small traps hit the same session:**
- `add_clips` rejects `source` AND `endFrame` together — "set source OR endFrame, not both". `source`
  is SECONDS of the asset; `endFrame` is an exact timeline length.
- `import_media` **timed out when asked to create a NEW folder** and no folder was created. Retrying
  without the `folder` arg succeeded instantly. Import first, organise after.
- `set_clip_properties` has **no `startFrame`** — position is `move_clips`. Setting `trimStartFrame`
  alone slides the CONTENT inside a fixed clip, it does not move the clip.
- **`trimEndFrame` in read output is not always self-consistent** with `trimStart + duration + source
  length` on graphic clips. Do not compute source headroom from it — get the real length from
  `get_media` `durationSeconds × fps`.
- `set_keyframes` frames are **clip-relative and follow the clip**, so they survive `move_clips` — but
  they do NOT survive remove+re-add (a new clip id starts with an empty keyframe track), and any
  change to the clip's HEAD length re-indexes every later keyframe.

## v0.6.5 production delta (n8n-to-cc build, 2026-07-11 — schema shifts + NEW bugs vs the v0.6.1 audit)

Call-shape changes (all live-validated; when a call rejects, trust the error's "Allowed:" list):
- **`add_clips`**: `entries[]` each take `mediaRef` + `startFrame` + `source:[startSec,endSec]` (SOURCE SECONDS, not frames) + optional per-entry `trackIndex` ✅. `trimStartFrame`/`durationFrames` are REJECTED at placement — place by source span, then adjust via `set_clip_properties`/`set_keyframes`. ⚠️ **`add_clips` can AUTO-FLIP the timeline resolution to match the incoming clip** (bit twice: adding a 1080×960 panel flipped a 1080×1920 project) — re-read `get_timeline` width/height after adds and re-set via `set_project_settings` if flipped.
- **`import_media`**: ONE asset per call, `source:{path|url|bytes|matte:{hex}}` (an `items` array is rejected). Import returns `status:"downloading"` — poll `get_media {ids}` until it clears.
- **`add_clips` trackIndex is all-or-nothing across `entries[]`**: either set `trackIndex` on EVERY entry or omit it on every entry (mixed → "Mixed trackIndex: N of M entries omitted" rejection). Placing several graphics on a known track + one auto-track clip in the same call fails — split into two calls.
- **`set_clip_properties`**: takes `clipIds:[...]` + top-level props (NOT a `clips:[]` array).
- **`set_keyframes`**: `{clipId, property, keyframes}` one property per call; **`keyframes: []` CLEARS that property's keyframes** ✅ (the clean way to delete a punch-in — clear `scale` AND `position`).
- **`manage_tracks`** reorder = `[{index, to}]`; **`move_clips`** = `[{clipId, toFrame, toTrack}]`.
- **`update_text` requires ≥1 text property in EVERY call** — targeting alone (`clipIds` / `captionGroupId`) is rejected with `update_text needs at least one text property to apply` (3× repeat in the error log, July 2026). Always pass the property being changed (`text`, typography/color fields, or `animation`) alongside the targeting; there is no "touch"/no-op form.

New v0.6.5 bugs (workarounds inline):
- **`inspect_timeline` IGNORES its frame params — always renders frame 0.** Any mid-timeline visual verification must run on an actual export: render, then `ffmpeg -vf "select=eq(n\,F)" -frames:v 1` per checkpoint frame. Do NOT trust inspect_timeline for anything but frame 0.
- **`update_text` content edits CLEAR the cue's word timings** (karaoke `highlightBlock`/`highlightPop` degrades to static text on that cue; a `wordTimings` param is silently ignored). REGRESSION vs the v0.6.1-verified "changing word count is safe" claim. Accept static text on fixed cues (correct text beats karaoke; each cue <1s) or fix text before captioning.
- **`add_captions` transcribes ONLY the main audio track** — clips whose audio sits on a second audio track are SILENTLY skipped (5 clips lost their captions this way). Consolidate all dialog audio onto one track BEFORE captioning (trim 1-frame overhangs, `move_clips` to the main track), then caption once.
- **`add_captions` with `clipIds` DUPLICATES the whole caption set** instead of captioning just the targets — never use it to patch missing cues; remove all caption clips and re-caption in one clean pass.
- ASR head-word artifacts: first-word timestamps drift early into silence, and a fresh ASR pass can swallow a clip-head word entirely (~1-2f lead) even though the audio contains it — verify disputed words with syllable-level energy analysis on the extracted wav, not by re-transcribing.
- After `ripple_delete_ranges` closes a hole that a MUSIC clip spanned, the downstream music clip keeps its old `trimStartFrame` → the bed SKIPS source material at the join. Rebuild the bed as ONE fresh clip spanning the new timeline length — and **enumerate the fragments from a FRESH `get_timeline`, not from remembered ids**: every successive ripple splits the bed again, and a stale id list left a stray fragment that silently DOUBLED the music over a third of the timeline (caught 2026-07-12).
- **A ripple cut through the MIDDLE of a caption cue SPLITS it into two clips with the same text** (duplicate cue), and the kept fragment's karaoke word timings come out mangled (highlights lag the voice ~10-15f). Repair recipe (✅ 2026-07-12): (1) remove one fragment, extend the other back to the full span; (2) **karaoke clear-and-restore** — `update_text` with the SAME content is a NO-OP (mangled timings survive), so make a real change then change back: edit content to a variant (add a period), then edit back to the exact text. The first edit clears the bad timings; the restore re-seeds fresh evenly-distributed word timings that track the voice correctly. This makes mangled karaoke REPAIRABLE — better than accepting a static cue. Render-probe the cue after. ⚠️ **`update_text` with the SAME content string is a NO-OP** (won't clear timings, won't re-seed) — the clear-and-restore REQUIRES a real change first (add/remove a char, e.g. append a period), THEN restore the exact text; two calls, not one.

## v0.6.13 delta (construction-tech-adoption build, 2026-07-29 — all live-verified)

- **`add_clips` `source:[startSec,endSec]` TRUNCATES the frame count, it does not round.** A span of
  exactly 169.0 frames computed in float arrives as 168.99999 and lands as **168** → the clip ends one
  frame short of the next clip's `startFrame` → a **1-frame gap that renders BLACK** (fails G3, and
  `gaps:[[2460,2461]]` is the only clue). Three of 32 clips hit this in one pass. **Fix: add ~0.0006s
  epsilon to the source END** (`e = s + n/30 + 0.0006`) so truncation lands on the intended integer —
  verified to produce exact durations across 32 clips. Always diff the returned `frames` against your
  intended cumulative layout and close any gap with `set_clip_properties {durationFrames}`.
  Corollary: quantize spans to whole frames (`e = s + round((e-s)*30)/30`) before adding, or float
  drift compounds.
- **`add_clips` re-matches the timeline resolution to the incoming clip and only tells you in `notes`**
  (`"Matched timeline resolution to clip: 2160×3840"`). It fired twice unnoticed here, silently
  undoing a `set_project_settings` 9:16. **Read `notes` after EVERY `add_clips`** and restore the
  intended resolution immediately; a wrong canvas invalidates caption wrapping and graphic safe-areas.
- **`set_project_settings` is a no-op when settings already match** (`{"changed":[]}`) — so it is NOT
  a way to force a caption re-wrap or clip re-fit. Don't reach for it as a repair.
- **`manage_tracks` shapes:** mute = `set:[{trackId, muted:true}]`; reorder = `reorder:[{trackId, to:N}]`
  (`to`, not `index`; a bare id string is rejected). New video tracks from `add_clips` land at index
  **0 (top)** — after adding graphics, reorder the caption track back to 0 or captions render *under*
  the graphics.
- **`set_keyframes` takes `clipId` (singular string), not `clipIds`** — no batching; one call per clip
  per property.
- **`update_text` content edits PRESERVE karaoke on v0.6.13** — the v0.6.5 "clears word timings"
  regression appears fixed. The response still prints the "cleared word timings" note, but
  frame-sampling proved per-word tracking alive (block on word 1 at f18, word 2 at f28). **Trust the
  render, not the note.**
- **`capture_frame {timelineFrame}` → `inspect_media` works on v0.6.13** and is the cheap way to verify
  a placement without a full render.

## v0.6.6+ delta (meeting-prep build, 2026-07-20 — post-crash app update; all live-verified)

Toolset changed across an app restart mid-session (Palmier auto-updated): **never trust cached tool schemas after a restart** — re-discover.
- **`manage_project` replaces `get_projects`/`open_project`/`new_project`/`close_project`** — one tool, `action: list|open|create|close`. `list` shows isOpen/isActive per project.
- **`capture_frame {timelineFrame}` → `inspect_media {mediaRef}` = WORKING mid-timeline visual verification.** Returns the fully composited frame (transforms, text, captions, effects) as a viewable image. This SUPERSEDES the render+ffmpeg workaround for the broken `inspect_timeline` — verify every placement this way (caught 3 real layout bugs in one session). Captures become media assets — ignore them in library scans.
- **`manage_exports` (list/cancel)** — poll checkpoint/render job status.
- **Transform trap: `width`/`height` are INDEPENDENT canvas fractions.** Auto-fit sets only ONE; setting the other alone leaves the stale auto value → distortion/cropping (a 1180×2556 card kept auto `width:0.821` under `height:0.56` → clipped; a face `height:1.35` zoom left width at 1.0 → black side band). Always set BOTH, computed from the media aspect.
- **`set_keyframes` formats:** `scale` = `[frame, sx, sy, easing]` (4-element); `opacity`/`volume` = `[frame, value, easing]`. Frames CLIP-RELATIVE. ⚠️ Passing a linked-audio id (`clip.audio.id`) silently keyframes the AUDIO side — always use the video `clip.id`.
- **`add_captions` ignores `fontSize`** (renders 48) — fix after with `update_text {captionGroupId, style:{fontSize:60}}`.
- **`add_texts`**: `entries[]` with `content` (not `text`), nested `style` (`bold` not `isBold`; `shadow` is an object, not bool; `fontName` works — "Geist"), `transform` must be `{centerX,centerY}` both or all four.
- `add_clips` entries accept `endFrame` (exact timeline length) OR `source` span — never both. Oversize `endFrame` vs source duration is rejected with the source's frame count (useful for measuring).
- **Crash recovery:** a reopened Palmier window can have a DEAD MCP endpoint (accepts TCP, never answers) — only full Cmd+Q + reopen revives it. Checkpoint with `export_project mode:"palmier"` (~1min, portable .palmier to ~/Downloads) after each build phase; an autosave rollback ate an hour of edits. Don't touch the app UI while an MCP session is editing.

Recut-v2 additions (2026-07-20, all live-verified during the clean rebuild):
- **`search_media {query}` returns ASR sentence spans in SOURCE seconds** — the word-anchor ground truth for cut planning (segments butt: each `endSeconds` = next segment's start, so starts may include leading pause). Use it to locate every script line + repeated takes before cutting.
- **`create_timeline {name}` → new empty ACTIVE timeline.** No tracks until first `add_clips` (auto-creates V1+A1). ⚠️ The first clip on an empty timeline RESETS project resolution to the clip's ("Matched timeline resolution") — re-run `set_project_settings` after, and again if you re-create the track.
- **`manage_tracks` cannot CREATE tracks.** `add_clips` with `trackIndex` omitted creates a NEW track ABOVE existing ones (index 0 renders on top) — that's how you build the overlay stack bottom-up. With `trackIndex` set, the clip must fit that existing track.
- **`source:[sec,sec]` rounding trap:** linked audio can come out 1 frame LONGER than its video (video floor, audio round) → the next clip's audio can't fit and spawns a phantom audio track. Fix: `set_clip_properties {durationFrames}` on the long audio id, then `move_clips [{clipId, toTrack}]` to consolidate. Pick source spans whose duration×fps is near-integer to avoid it. Also check for 1-frame GAPS after add (one clip floored short) — extend with durationFrames.
- **`add_texts` color must be a HEX STRING** ("#00C6A2"), not an RGB object. ⚠️ Two entries sharing a time range in ONE call: only one lands (silently) — add time-overlapping texts in SEPARATE calls.
- **Text wraps at the ~0.82-canvas-width default box** — a two-line `\n` hook at fontSize 72 re-wrapped to 4 lines half off-screen. Anti-stretch pattern that works: ONE text clip per line, fontSize sized to fit unwrapped (≤46 for ~17 chars), transform ONLY `{centerX, centerY}` → natural aspect box. Never pass width/height on text.
- **`add_captions {style:{fontSize}, animation:"highlightBlock", transform:{centerX,centerY}}`** — animation is a bare string enum; fontSize IS respected at add-time in v0.6.6+. Highlight color after: `update_text {captionGroupId, highlightColor:"#00C6A2"}`.
- `set_keyframes` is per-clip: `{clipId, property:"opacity"|"volume"|"scale"|…, keyframes:[[...]]}`; `set_clip_properties` does NOT accept keyframes (silently ignored).
- `export_project` modes: `video` (H.264 render → ~/Downloads), `xml`, `fcpxml`, `palmier` (checkpoint).
- Z-order is still add-order (reorder no-op): build bottom-up — base video → cards/graphics → text accents → captions LAST.
- **`ripple_delete_ranges` is GLOBAL across ALL tracks** — `trackIndex` only anchors the ranges; every track shifts in lockstep, so overlays/captions/SFX stay aligned with the voice (no per-track passes needed). Overlay clips spanning a cut are **auto-split at the cut point with fade keyframes correctly re-derived per fragment** (an out-fade lands exactly at the new fragment end). Two cleanups after: (1) splits can leave 1-frame text-orphan fragments — remove them; (2) a split mid-graphic makes the animation JUMP the removed frames — fine in idle/slow zones, avoid cutting through entrances. Music beds still need remove-before/re-add-after (join bug). Captions: REMOVE the caption track before rippling and re-run `add_captions` after — rippling through cues splits/mangles karaoke (documented), and re-captioning is one call.
- **`manage_tracks` remove syntax: `{remove:[{index:N}]}`** (objects, not bare indices; no `action` param).

## Prerequisites & gotchas
- The **Palmier desktop app must be running** — the MCP bridges to a localhost server (`127.0.0.1:19789/mcp`, streamable HTTP; Claude Desktop reaches it via `mcp-remote`). If calls time out or return "Server palmier-pro unavailable", the app is closed → ask the user to open Palmier.
- **AI generation + upscale require a signed-in subscription.** `get_timeline` returns `canGenerate`; if false, `generate_*` / `upscale_media` fail — tell the user to sign in and subscribe. `inspect_media` transcription runs on-device and works regardless. Note: `list_models` can return `loaded:true` while `canGenerate` is still false (catalog sync ≠ entitlement) — trust `canGenerate`, not `loaded`.
- **Connection:** the bridge is the running desktop app's localhost server. If the app wasn't up when the session's MCP clients initialized, `palmier-pro` fails to register and **won't auto-retry** — opening the app afterward isn't enough; reconnect MCP or restart the session. (Fallback: the bridge speaks plain MCP over HTTP — a small script can `initialize` + `tools/list`/`tools/call` against `http://127.0.0.1:19789/mcp` directly, which is also how to audit the live surface without a client manifest.)
- **`send_feedback` sends a report to the Palmier team immediately, with NO user confirmation step.** Sending externally is an explicit-permission action — never call it without the user's approval, and never include verbatim project content (its own description forbids that too).
- **SAVE DISCIPLINE (data loss happened twice, 2026-07-06): Palmier autosaves on a timer only — quitting does NOT flush recent edits, and there is no in-place MCP save tool.** A crash/wedge/reopen rolls the project back to the last autosave (one rollback ate a full placement pass). Checkpoint after every editing phase: Cmd+S via **computer-use** (`request_access` PalmierPro → `key cmd+s`; plain `osascript` keystrokes are blocked), then verify on disk via the package's `project.json` mtime. **MCP-only fallback ✅: `export_project {mode:"palmier"}`** snapshots the live editor state to a standalone package (recovery: `open_project {path}`) — but it embeds ALL media (GBs), so use before risky phases, not per-edit. The localhost bridge also **wedges under sustained call volume** (connection resets while the app process lives): pace scripted calls ≥0.5 s, retry with backoff, and if `initialize` itself resets → `osascript quit` + `open -a PalmierPro` + `open_project {id}` ("Editor not available" after reopen = project not loaded yet). After ANY reload, re-verify timeline AND media: rollbacks resurrect deleted same-name assets whose files are gone — a name lookup then grabs the stale one ("durationFrames exceed the source length"); distinguish by duration, purge, re-import. Keep every mutation phase in a re-runnable script so rollback recovery is mechanical. Full workflow: [palmier-talking-head-overlays.md](palmier-talking-head-overlays.md) §4.

## Core model
- Timeline has a fixed **fps** and **resolution**. All timing is in **frames**: `frame = seconds × fps`.
- A **project** (`.palmier` package) can hold **multiple timelines** (v0.6.1): `create_timeline` / `duplicate_timeline` / `set_active_timeline`. All read/edit tools target the *active* timeline; `get_timeline` lists `timelines` whenever there's more than one. A timeline can be **nested** inside another as a single clip (`mediaType:"sequence"`, `mediaRef` = timelineId) — to edit its contents, `set_active_timeline` to that mediaRef. After any switch/duplicate, **re-read `get_timeline`** — old clip/track ids are invalid (duplicates get all-new ids).
- Tracks are ordered and typed (video / audio). Video clips, images, and text overlays all live on video tracks.
- A clip references a media asset by ID and occupies `[startFrame, startFrame + durationFrames)`. Clips have `trimStartFrame`/`trimEndFrame` (source offsets), `speed`, `volume`, `opacity`, and (video/image) `blendMode`.
- Media assets live in a project library, referenced by ID (user-imported or AI-generated).

## Always do first
1. `get_timeline` once per session → fps, resolution, tracks, clips, `canGenerate`, and (if >1) the `timelines` list. The `clipId`/`trackId` values it returns are what every other tool accepts. (Don't re-read between your own edits — mutation tools return what changed. Re-read only after an out-of-band change or a timeline switch.)
2. `get_media` before referencing any asset — every `mediaRef` comes from here; also shows `generationStatus`.
2b. **Canvas/aspect check.** Compare the primary footage's orientation (`sourceWidth`×`sourceHeight` from `get_media`) to the canvas (`width`×`height` from `get_timeline`). Vertical footage on the default 1920×1080 canvas = pillarboxed export — wrong for LinkedIn/Shorts/Reels (target 1080×1920). Giveaways: `settingsConfigured:false` and a fitted clip transform (e.g. `width:0.316` = portrait fitted into landscape). **Fix via MCP (v0.6.1+): `set_project_settings`** — `aspectRatio` preset (`16:9`/`9:16`/`1:1`/`4:3`/`2.4:1`/`9:14`), explicit `width`+`height`, `fps`, and/or `quality` (`720p`–`4K`); aspectRatio and width/height are mutually exclusive (live-validated). It re-fits clips automatically (auto-fit transforms recalc; frame positions/durations rescale on fps change) and is undoable. ⚠️ setter not yet run for real — verify a frame with `inspect_timeline` after the first live use. UI fallback (✅ this is how the 2026-07-05 flip actually ran; also the path on a stale manifest): project panel, right side → Resolution / Aspect Ratio dropdowns — the user's click, or computer-use with granted access to `PalmierPro`. **Runtime-verified on that flip:** the app auto re-fits video clips AND re-wraps caption groups — flipping *after* captioning is safe; on **≤v0.3.5** assume no auto-refit (flip before captioning, re-check `transform`s). Hand-placed `add_texts` clips don't re-wrap well on an aspect flip (auto-fit box → one-word lines): give them explicit `\n` line breaks. (History: through the *cached-manifest* view of ≤v0.6.1 this looked MCP-immutable and needed the UI — that claim is dead; the live v0.6.1 manifest has the tool. General lesson: **trust the live error's "Allowed:" list over a cached schema** — mid-session drift shows up as unknown-field rejections.)
2c. **Denoise (v0.6.1+) — OPT-IN ONLY, never apply unprompted.** The agent cannot audition audio: it can verify the processing *finished*, not what it did to the sound. At the default 60% strength on already-clean speech (AirPods/lav in a quiet room) it produces audible warble/underwater artifacts — the user caught exactly this on 2026-07-05 after an unrequested "polish" application. Apply only when the user asks or names a noise problem, start ~30%, and tell them which spots to audition. **MCP path (live v0.6.1): `denoise_audio`** — on-device DeepFilterNet3, `strength` 0–100 dry/wet (100 can sound thin/over-gated), `enabled:false` removes it; bake runs in the background and the timeline updates itself — no polling; undoable and non-destructive (removing the effect restores the original exactly). ⚠️ not yet run for real (live-validated: bogus clipId errors correctly). State is readable as `effects:[{type:"audio.denoise",params:{amount}}]`. UI fallback: clip → Audio tab → Denoise toggle + Strength; right-click first clip → **Select Forward on Track** → one toggle covers the selection (a MIXED selection toggles to uniform-ON first, then OFF on the second click — verify the end state via `get_timeline` clip `effects`, not the toggle pixel).
3. `list_models` before `generate_video` / `generate_image` / `generate_audio` / `upscale_media` — confirm the model supports the duration, aspect ratio, references, or voice you need. `loaded:false` means the catalog hasn't synced (e.g. not signed in) — retry after sign-in.
4. `inspect_media` before describing any user-supplied asset — describe what you actually see, never paraphrase the filename. Work coarse→fine on long media (overview, then transcript segments, then a zoomed window).

## Tool surface (49 tools, live v0.6.1 — audited 2026-07-05)

Marks: ✅ = live-verified (ran it for real) · ⚠️ = live-validated (server accepted/validated a probe; not yet run to completion) · plain = schema-read only.

- **Project management (new in 0.6):** `get_projects` ✅, `open_project` ✅ (**params: `id` or `path`** — `projectId` is rejected; needed after every app relaunch, which opens to the launcher: "Editor not available" = call this first), `new_project`.
- **Timelines (new in 0.6):** `create_timeline`, `duplicate_timeline` ✅ (the versioning primitive — copy, edit the copy; run for real 2026-07-05 backing up a cut before a recut: copies all tracks/clips/settings, switches to the copy, ALL ids are new). `set_active_timeline` ⚠️. No delete-timeline tool. **Always duplicate before a destructive recut** — the original stays as the rollback.
- **Read/inspect:** `get_timeline` ✅ (now takes optional startFrame/endFrame window), `inspect_timeline`, `get_media`, `search_media`, `inspect_media`, `get_transcript`, `list_models`, `list_folders`, `inspect_color` ✅ (new — scopes: black/white points, clipping %, per-zone RGB, saturation, warm-cool/green-magenta balance, 12-bin hueHistogram + rendered frame; optional `reference` asset returns the subject−reference gap with knob hints).
- **Timeline editing:** `add_clips` (trackIndex now optional — auto-creates tracks; video with audio auto-creates a linked audio clip), `insert_clips`, `move_clips`, `remove_clips`, `split_clips` ⚠️ (**renamed from `split_clip`**; batch: explicit `{clipId,atFrame}` list OR `trackIndex`+`frames`; multiple cuts per clip in one call; linked A/V split together; one bad point rejects the whole call; the result message lists the NEW right-half clip ids — video AND linked audio, e.g. "New right-half clip(s): A, B"; the left half keeps the original id), `ripple_delete_ranges` ✅ (run for real 2026-07-06, 7 cuts incl. head-trim + mid-clip cuts: two modes — `trackIndex` project-frame ranges spanning clips, or single-`clipId` ranges. Verified semantics in trackIndex mode: cuts the range across every sync-locked track (a caption clip straddling the cut is head-trimmed — its pre-roll just shrinks), shifts everything downstream, **splits mid-clip cuts and REBASES keyframes flat on the right halves** (no zoom-replay), and PRUNES a track the cut empties — track indices shift, re-read `get_timeline` before the next index-based call. Order multi-range work right-to-left, one range per call; never leave a <4f sliver — align the range start to a clip head when a gap straddles a cut), `remove_words` ✅ (run for real 2026-07-05: 6 sentence-spans / 99 words / 1299 frames cut in ONE call on a 13-clip timeline — linked A/V stayed in sync, gaps closed, every seam verified clean via `get_transcript` re-read. Descript-style: cut speech by `get_transcript` word indices/spans or exact `matches` like ["um","uh"]; removes surrounding pause, merges adjacent cuts, cuts linked partners, closes gaps; `cutAggressiveness` tight/balanced/loose; one track per call; re-read transcript after. ⚠️ caption clips are NOT linked partners — delete the caption group BEFORE cutting and re-`add_captions` after, else cues desync. ⚠️⚠️ **`remove_words` only closes gaps IT creates — a PRE-EXISTING inter-clip gap survives and becomes a BLACK HOLE.** If the source timeline already has two separate clips with a silent pause between them (a natural beat between takes/sentences), the cut shifts that gap left but never closes it, and a `get_transcript` seam check is BLIND to it (no words live in a silent gap). ALWAYS run a black-hole scan after cutting — see palmier-captions.md "Gap scan". **CLOSE the hole, NEVER fill it.** The silence was removed ON PURPOSE — the fix is to butt the downstream clips against the preceding one: `ripple_delete_ranges({trackIndex, ranges:[[holeStart,holeEnd]], units:'frames'})` deletes the empty span and shifts everything after it left (linked A/V + sync-locked tracks follow). **DO NOT extend the preceding clip's `durationFrames` to "fill" the gap — that re-adds the exact silence/pause you just cut** (the user caught this 2026-07-05: I "filled" a removed-silence hole by extending the prior clip, re-introducing the dead air they'd deliberately removed — the opposite of the goal). Extending-to-fill is ONLY right when you deliberately want a held beat on footage; in a radio-edit / tightening pass, dead air is the enemy, so always close.), `set_clip_properties` ⚠️ (duration/trims/speed/volume/opacity/transform incl. flipH/flipV + **`blendMode`** — 16 Photoshop-style modes: normal/darken/multiply/colorBurn/lighten/screen/colorDodge/overlay/softLight/hardLight/difference/exclusion/hue/saturation/color/luminosity; video/image only; **text fields are GONE** → use `update_text`), `set_keyframes`, `remove_tracks`.
- **Layout (new in 0.6):** `apply_layout` ⚠️ — split screen / PIP / grid templates (`full`, `side_by_side`, `top_bottom`, `pip_bottom_right/left`, `pip_top_right/left`, `grid_2x2`, `main_sidebar`, `three_up`), computes transform+crop per slot (cover-crop, `fit` letterboxes), `anchor`/`anchorX`/`anchorY` bias which part of the source survives the crop. Use this — NOT hand-set transforms — for multi-clip canvas arrangements.
- **Text & captions:** `add_texts` (overlays), `add_captions` (transcribe + styled caption groups; now also `animation` preset, `maxWords`, `highlightColor`, `isBold`/`isItalic`, `borderColor`, `backgroundColor`; omit clipIds to caption the main spoken track), `update_text` ✅ (runtime-verified 2026-07-05: one `captionGroupId` call restyled 156 caption cues — `color` + `highlightColor` — plus per-cue `content` and `fontSize` via `clipIds`) (**the text editor**: `content` (supports `\n`), `fontName`/`fontSize`/`color`/`alignment`/bold/italic, `borderColor`/`backgroundColor`/`highlightColor`, `animation` preset, text-box `transform`; targets `clipIds` or a whole `captionGroupId`). Animation presets (both tools): `off`, `fadeIn`, `popIn`, `slideUp`, `typewriter`, `wordReveal`, `wordSlide`, `wordPop`, `wordCycle`, `highlightPop`, `highlightBlock`. Per-word timing (`perWordFrames`) is visible in `get_timeline` but **not settable** (preset default, e.g. 6).
- **Color & FX (new in 0.6):** `apply_color` ⚠️ — a real colorist path: exposure (EV), contrast, highlights/blacks, per-zone color wheels (hue 0–360° + amount for shadows/mids/highs, plus midsGamma/highsGain), master + per-channel R/G/B tone curves, Resolve-style hue curves (targetHue → hueShift/satScale/lumShift secondaries), and `.cube` LUT with strength; MERGES with the current grade, `reset:true` starts neutral; loop with `inspect_color(clipId, reference)`. `apply_effect` ⚠️ — live editable FX stack, merge semantics (`enabled:false` bypasses, `remove` deletes): `detail.clarity` (clarity/dehaze), `blur.gaussian`, `blur.sharpen`, `blur.noiseReduction`, `blur.motion`, `stylize.grain`, `stylize.vignette`, `stylize.glow`, **`key.chroma`** (keyHue/tolerance/softness/spill — green screen INSIDE Palmier). `create_matte` — solid-color PNG matte into the library (hex + aspect) — fade-to-white white frames are now one call.
- **Audio (new in 0.6):** `denoise_audio` ⚠️ (see 2c), **`sync_clips`** — align targets to a `referenceClipId` and shift them on the timeline (dual-system sound / multicam). **Named `sync_clips`, not `sync_audio`** (the older name in these notes will fail). Mode `auto` prefers embedded **source timecode** (exact, confidence 1.0) and falls back to audio cross-correlation; returns per-target `offsetFrames` + `confidence` + `method`, refuses weak matches (`minConfidence` default 0.5, `searchWindowSeconds` ±30). Refused on multicam clips.
- **AI generation (subscription-gated, costs money, NOT undoable):** `generate_video` (now with start/end-frame refs, reference audio/video/image, sourceClipId), `generate_image`, `generate_audio` (TTS: elevenlabs-tts-v3, gemini-3.1-flash-tts; music: lyria3-pro, minimax-music-v2.6, elevenlabs-music; **video-to-audio**: sonilo-v1.1-video-to-music, mirelo-sfx-v1.5-video-to-audio — score a timeline span via videoSourceStartFrame/EndFrame or an asset), `upscale_media`.
- **Media management:** `import_media` (⚠️ **ASYNC**: returns immediately with a *placeholder asset id* + status `downloading`; the placeholder id becomes the real asset id, and local-file copies resolve in ~1s — one paced `get_media` re-read before `add_clips` is enough. ⚠️ **behavior change v0.6.1: local `path` is now COPIED into the project in the background** — the old ≤v0.3.x referenced-in-place footgun is gone; url = HTTPS ≤1 GB background download; bytes = base64 ≤ ~11 MB binary; a path may be a directory, imported recursively as folders), `rename_media`, `delete_media` ✅ (**param is `assetIds` (array)** — `mediaIds`/`mediaId` are rejected; deleting also removes clips referencing the assets), `create_folder`, `rename_folder`, `delete_folder`, `move_to_folder`.
- **Export (new in 0.6):** `export_project` ✅ (fcpxml live-verified: wrote a valid FCPXML 1.10 file) — modes: `video` (H.264/H.265/ProRes, resolution presets or Match Timeline; background render, returns `status:started` + system notification on completion), `xml` (XMEML → Premiere), `fcpxml` (`fcpxmlTarget` resolve|fcp — carries text/transforms/crop/opacity/keyframes that XMEML can't), `palmier` ✅ (self-contained package, all timelines, snapshots the LIVE editor state incl. unsaved edits — the MCP-only save checkpoint; embeds all media so expect GBs). Omit outputPath → unique file in ~/Downloads; overwrites by default (`overwrite:false` to refuse).
- **Feedback:** `send_feedback` — reports a limitation/bug to the Palmier team. **Sends immediately, no confirm — treat as an external send: never without the user's approval.**
- **Safety:** `undo` — reverts the assistant's most recent edit this session, most-recent-first; refuses if the latest change was the user's manual edit. After undo, ids/frames from the undone edit are invalid — re-read.

## Field notes — first production overlay build on v0.6.1 (2026-07-05, ✅ all live-verified)

> **The full talking-head enrichment workflow (b-roll + full-screen animated brand diagrams +
> transitions) now lives in [palmier-talking-head-overlays.md](palmier-talking-head-overlays.md)** —
> read that first for any "add b-roll / overlays / graphics to my talking-head video" task. The v1
> **floating-card recipe in the last bullet below was rejected on the redo** (cards over a centered
> face read as a mess): a vertical selfie fills the upper-center with the face and captions at the
> bottom, so there's no gap to float a readable card into. Use **full-screen cutaways** + **split-screen
> b-roll** instead (see the reference). The API facts in this section are all still true.

Learned building 15 b-roll/overlay clips (Klarna b-roll + branded stat cards) on a real 1080×1920 talking-head timeline:

- **Image clips have a hard 150-frame (5 s) source cap** — `add_clips`/`durationFrames` beyond 150 is rejected ("exceed the source length"). To hold a still longer: place ≤150f, then `set_clip_properties({speed: 150/target, durationFrames: target})` — visually identical for stills, works to at least 442f.
- **Do NOT put `scale` keyframes on an image clip that has a `transform` box** — the scale track fights the transform and renders the clip ~2× oversized (clipped edges, overlaps everything). Clips with only opacity keyframes + transform render pixel-correct. Animate overlay cards with **opacity fades only** (`[[0,0],[6,1],[dur-6,1],[dur,0]]`); clear a bad scale track with `keyframes: []`. (`scale` value layout is `[frame, x, y]`.)
- **`add_clips` with trackIndex omitted creates the new track ABOVE the captions track** (topmost); each such call creates ONE new shared track — call once per simultaneous-overlay layer (e.g. 3 calls for a 3-row stacked list). Overlays above captions are fine when spatially disjoint from the caption band (captions live at centerY 0.8; keep cards ≤0.77).
- **`import_media` copy semantics differ by mode:** single-file `path` → **copied** into the project package (`source.project.relativePath` — durable). **Directory** `path` → children **referenced in place** (`source.external.absolutePath`) — the pre-0.6 footgun is still alive in directory mode; only import directories from durable locations, never /tmp.
- **Video-with-audio placed on a video track auto-spawns a linked audio clip** (new audio track if needed). Mute b-roll: `set_clip_properties({clipIds:[audioPartnerIds], volume: 0})` — one call, volume doesn't propagate across the link.
- **The active timeline can flip out from under you when the user has the app open** (a UI tab click re-asserts it). Symptom: mutations start failing "Clip not found" mid-batch — your calls are resolving against the wrong timeline. Re-assert `set_active_timeline` before every mutation batch in a shared session, keep batches small/sequential, and verify with `get_timeline` `timelines[].active` after anomalies. Mutations that succeeded before the flip land on the correct (previously active) timeline.
- **Overlay card recipe (v1 — SUPERSEDED for talking-head video):** render transparent PNGs (Playwright `omit_background=True`, body `background:transparent`; card = `rgba(9,9,11,0.80)` + 1px `rgba(255,255,255,0.16)` border) at natural pixel size for a 1080-wide canvas → `import_media` → `add_clips` → `set_clip_properties` transform → opacity-fade keyframes. Still valid for a static card on non-face footage, but for a talking head use the full-screen/split-screen approach in [palmier-talking-head-overlays.md](palmier-talking-head-overlays.md).

### v2 addendum — the redo (2026-07-05/06, ✅ live-verified)
- **`apply_layout top_bottom` in clipIds mode = split-screen b-roll with no math and no split.** Place b-roll on a new top track, then `apply_layout({layout:"top_bottom", slots:[{slot:"top",clipIds:[broll]},{slot:"bottom",clipIds:[head],anchorY:0.4}]})`. It cover-crops each source to fill its half (16:9 b-roll fills the top edge-to-edge; `anchorY:0.4` keeps the presenter's face). **Align windows to existing sentence cuts and you never call `split_clips`.**
- **`split_clips` is the crash-prone call** — it timed out and took the app down (under render CPU load). Avoid it via existing boundaries (above). **Never run heavy local Playwright renders concurrently with Palmier mutations** — CPU contention starves the localhost bridge; a "server unavailable"/timeout mid-edit is usually that, not a logic bug. Render first (background), then edit.
- **A crash reverts unsaved MCP edits** — the project reloaded a pre-edit state (a prior `remove_clips` was undone; the timed-out split never applied). Clip IDs persist, so re-`get_timeline` and redo. Never assume an edit landed just because the call returned before the crash.
- **ProRes 4444 alpha `.mov` composites correctly over live video** (a stat card over the Klarna app reel, b-roll showing through the transparent areas) — ✅ the verified solid-card-overlay route. Import shows `duration:0` while finalizing; re-`get_media` for real dims before `add_clips`.
- **Full-screen animated brand graphics beat Palmier-keyframed overlays** — bake the motion into a 1080×1920 MP4 (frame-stepped HTML → `window.seek(f)` → PNG seq → h264; `scripts/anim/`), one clip on a top track, crossfade with an opacity track. No keyframe saturation, motion synced to `get_transcript` word frames.

## Transitions, blend modes & alpha
- **Palmier still has no transition engine** (v0.6.1-confirmed: no transition tool in the live manifest) — no presets/effects to apply or import. Every transition is keyframe-built (`opacity`/`position`/`scale`/`rotation`/`crop`).
- **Blend modes now EXIST (v0.6.1):** `set_clip_properties.blendMode` with 16 modes incl. `screen` — an on-black overlay pack (burn/flare/glitch) should now composite directly with `blendMode:"screen"`, no ffmpeg pre-key. ⚠️ schema-verified only — the ffmpeg luma-key → **ProRes 4444 alpha** route stays the ✅ verified fallback (Palmier honors alpha). `create_matte` supplies white/black frames (fade-to-white). Audio transition SFX align frame-exact on an audio track.
- Full playbook + ffmpeg recipe + royalty-free sourcing: [palmier-transitions.md](palmier-transitions.md).

## palmier-pro is the backend — the only two Resolve exceptions

Palmier owns the whole pipeline. Resolve's scripting API cannot trim, move, split, or transition a
clip at all, has no Fairlight control, and exposes *less* grading and captioning than Palmier does.
There are exactly two reasons to open it:

1. **AI subject cutout on a real (non-green-screen) background** → Magic Mask 2, Color-page
   UI/computer-use. The one thing Palmier can't do — `apply_effect` `key.chroma` is its only keying
   effect and needs a keyable backdrop. Render an alpha codec out, `import_media` it back in.
2. **A project that already lives in Resolve** — plus the deep colorist/VFX environment that comes
   with it (node graph, qualifier UI, Fusion, DCTL, HDR delivery), all UI.

Interchange: `export_project({mode:"fcpxml", fcpxmlTarget:"resolve"})` ✅.
See [davinci-resolve.md](davinci-resolve.md).

## Track-index safety (2026-07-30 — three destructive wrong-track writes in one session)

- **Track indexes are UNSTABLE**: an emptied track auto-culls; `add_texts` (omit trackIndex)
  creates a new TOP video track (the ONLY track-creation path — `manage_tracks` cannot create,
  `add_clips` rejects index == count). Every cull/create shifts every index below/after it.
- **NEVER `add_clips` by a remembered index after any remove/create.** Re-read `get_timeline`
  and match the target by trackId/label first. Three same-day failures: a bed re-add wiped the
  ticks track; a graphic re-add landed on the FACE track and cut base footage; a second bed
  attempt wiped A3.
- `add_clips` into an occupied range silently OVERWRITES (full-cover → clip removed;
  partial → trimmed). Removing one side of a linked A/V clip removes BOTH sides.
- **`undo` reliably reverses a bad add/remove** — use it immediately, then re-read.
- To REPLACE a clip's media on a one-clip track: add the new clip ONTO the same track over the
  old one (overwrite-in-place) — never remove-then-add (the remove culls the track and the
  re-add lands somewhere else).

## Codec gate (2026-07-30 — the "Cannot Decode" day)

- **Palmier's renderer cannot decode VP9.** Google Drive serves VP9-in-mp4 transcodes; one such
  b-roll import killed EVERY export (silently dying jobs) and capture_frame ("Cannot Decode")
  for hours. `ffprobe` every externally-sourced file BEFORE import; only H.264/yuv420p goes in
  (`-c:v libx264 -pix_fmt yuv420p -r 30`).
- Diagnose a poisoned timeline by binary-searching ASSETS: `capture_frame {mediaRef,
  sourceSeconds}` per suspect — the broken one errors ("Cannot Open"), the timeline error
  ("Cannot Decode") never names the culprit.
- Video exports write `.partial.mp4` next to the target path mid-encode — watch for the rename,
  don't declare a hung export from the missing final name.

## Placed-graphic content verification (2026-07-30)

Asset NAME + DURATION prove nothing about content: same-length re-renders of stale HTML sat in
the pool masquerading as current ("gw-b1" showed retired 5-phase/YOU language while the updated
station data existed on disk). After placing ANY graphic asset, capture one frame of it and
LOOK. Root cause of the drift: per-file copies of `window.ST` — shared station/label data lives
in ONE shared JS file consumed by every burst HTML, never copy-pasted.
