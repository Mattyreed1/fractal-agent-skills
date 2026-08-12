---
name: video-editor
description: >
  Edit and create video programmatically. palmier-pro (an AI-native editor) is the primary
  backend and owns the whole pipeline: text-to-video/image/audio generation, transcript-driven
  and clip-level timeline editing, styled word-level captions, color grading, audio, and
  render/export. davinci-resolve is a narrow escape hatch, used ONLY for AI subject cutout
  (Magic Mask) and for projects that already live in Resolve. Use when the user wants to create,
  assemble, edit, caption, color, or render video; generate AI video/image/audio clips; or asks
  which tool can perform a given editing task. Knows each backend's tested capabilities, hard
  limits, and runtime prerequisites. Triggers: "edit this video", "make a video", "generate a
  clip", "add captions", "color grade", "render/export the timeline", "Palmier", "radio-edit /
  tighten a talking-head reel", "pick the best takes", "cut the pauses/filler", "sync my camera
  audio / double-system audio", "remove the background", "DaVinci Resolve".
license: MIT
metadata:
  backends: palmier-pro (primary), davinci-resolve (escape hatch)
  verified-on: "Palmier Pro v0.6.1 build 63 live-manifest audit, 49 tools (2026-07-05) + v0.6.5 production delta (2026-07-11); DaVinci Resolve Studio 21.0.0.48 / davinci-resolve-mcp 2.57.5 (2026-06-23, background removal only)"
---
# Video Editor

**palmier-pro is the backend. Default to it for every step of the pipeline.** It does AI
generation, fine clip editing, captions, color, audio, and render — all programmatically.

**Background removal / subject cutout goes to a HOSTED API first, NOT Resolve** — fal.ai
`bria/video/background-removal`, **$0.0042/sec** (a 178s source ≈ $0.75), key already on this Mac.
Palmier genuinely cannot do it (live v0.7.2 manifest: `key.chroma` only, needs a green screen), but
"Palmier can't" is NOT "impossible" — EA told the user there was no API path on 2026-08-11 and was flatly
wrong. See [davinci-background-removal.md](references/davinci-background-removal.md).

**davinci-resolve is now reached for exactly twice:** (1) a cutout the API's limits reject (>30s
chunks, >4000px) or one needing hand-refined subtract-clicks, and (2) a project that **already lives
in Resolve**. Resolve's Magic Mask route is ~4–6 clicks per shot plus ~1 fps tracking — budget ~90
minutes for a 5,400-frame source against ~$0.75 and a few minutes for the API. Never route color, captions, animation, assembly, audio, or delivery
to Resolve — Palmier does all of them, and its scripting surface is *wider* than Resolve's API for
grading and captions. See [The two DaVinci exceptions](#the-two-davinci-exceptions).

## 📋 STEP 0 — BINDING: write the two on-disk progress files BEFORE touching a frame

**The harness task list is NOT the system of record — it is in-memory and a session reset wipes it.**
Before `get_timeline`, before importing, before cutting, create BOTH files inside the piece's
content-project folder, from the templates in
[references/build-checklist.md](references/build-checklist.md).

### 📁 Where the project folder is — and it is the ONLY working home

**Every file this build produces lives in the piece's folder under the brand's content folder.
There is no second working location.** One of exactly two parents:

```
projects/fractal-ai-content/<YYYY-MM-DD>-<slug>/       ← Fractal AI pieces
projects/founder-freedom-content/<YYYY-MM-DD>-<slug>/  ← Founder Freedom pieces
```

Paths are relative to your content repo root (`<REPO_ROOT>`). The folder name **always
carries the date prefix** — e.g. `projects/fractal-ai-content/2026-06-17-tech-adoption-framework/`.

**Find an existing piece:** `ls projects/fractal-ai-content/ | grep -i <keyword>`. Content pieces are
a deliberate **no-KG-node bucket** ([projects/README.md](../../projects/README.md)), so don't search
the knowledge graph for a `folder` property that was never created — listing is correct here.

**No folder matches? CREATE IT — that is a real STEP 0 action, not an afterthought.**
`mkdir -p projects/<brand>-content/$(date +%F)-<slug>/{assets/src,assets/renders,gfx}`. Brand comes
from `content-engine`; if it isn't already established, **ask** — never default.

### The canonical layout (create these; put everything in them)

```
projects/<brand>-content/<YYYY-MM-DD>-<slug>/
├── build-progress.md     ← the user opens this          [tracked]
├── build-checklist.md    ← the agent's ledger        [tracked]
├── brief.md / script.md  ← inputs                    [tracked]
├── scorecard.md          ← delivery gate G8          [tracked]
├── build/                ← the cut derivation: EDL scripts + JSON (asr, keeps, cuts,
│                            ripple plans, snap/refine passes)      [tracked — small + text]
├── gfx/                  ← graphic SOURCE (HTML/CSS/JS/data/logo)  [tracked — small + text]
├── assets/
│   ├── src/              ← source footage, audio stems  [gitignored by extension, lives here]
│   └── renders/          ← every render incl. the final [gitignored by extension, lives here]
└── backups/              ← .palmier checkpoints         [gitignored: projects/**/backups/]
```

**Media is gitignored by extension (`*.mp4`, `*.mov`, `*.wav`…) but still LIVES here.** Gitignored is
not "belongs elsewhere" — it means the bytes don't go to GitHub while the file stays with its project.
This is already how every other content piece works.

### 🚫 Three places build files must NOT live

1. **The scratchpad** (`/private/tmp/claude-502/<session-id>/scratchpad/`) — session-scoped and
    **wiped**. Use it for throwaway intermediates ONLY. Source footage, graphic sources, and renders
    go in the project folder. (Copying source footage off CloudStorage still applies — copy it to
    `assets/src/`, not the scratchpad.)
2. **`~/Movies/`** (or anywhere else in `$HOME`) — renders go to `assets/renders/`. the user on finding
    one there: *"why the hell would it be here?"*
3. **Drive, as a working directory.** Drive is **delivery only** — the finished video and thumbnail
    are *published* there at step 8. The graphic sources stay in `gfx/` in the repo; do not maintain a
    parallel `<slug>-assets/` copy on Drive. (That workaround existed only to survive the scratchpad
    being wiped. Keeping sources in the project folder removes the need for it.)

**Why this is binding:** on the tech-adoption-framework build the project folder ended up holding
three markdown files while the footage sat in a temp scratchpad, the renders in `~/Movies/`, and the
sources on Drive — so the work was not where anyone would look for it. the user, 2026-07-30: *"I don't
see the … project files where they should be."* Before you finish, `ls` the folder and confirm the
build is actually in it.

### The two files

| File | Audience | Purpose |
|---|---|---|
| **`build-progress.md`** | **the user** | The doc they open to see **exactly how far along the video is**. Opens with an at-a-glance header (`N of M complete`, current phase, what's next, last-updated) and a status table with evidence per step. Written so it answers "where does this stand?" in the first 10 lines, without reading the ledger. |
| **`build-checklist.md`** | the agent | The mechanical ledger + system of record. Every gate item with `[ ]`/`[x]` and written evidence on the line. |

**Both are updated in the SAME turn an item is verified** — not batched, not at the end. A stale
`build-progress.md` is worse than none, because it reports a build as further along than it is.
Mark `[x]` only with written evidence on the line (`[x] PASS — 30/32 boundaries in true silence`,
never `[x] looks good`). **Re-read both FIRST after any context loss** (reset, compaction, resumed
session, `/clear`) — they tell you exactly where you are. The harness task list may mirror them;
if they disagree, the files win.

Created 2026-07-29 after a session reset erased a mid-build checklist on the
tech-adoption-framework video — the user: *"this should not be possible … make sure this never
happens again."*

### 🔗 Then the Notion content page — resolve it, confirm it, flip the Stage (BLOCKING)

**Every video build corresponds to a page in the Notion Content DB, and the build does not start
until you have that page's link and have moved it to `Visual Editing`.** Do this before
`get_timeline`, in this order:

1. **Find the link.** Check, in order: the pipeline hand-off that invoked this skill, the piece's
   `build-progress.md` / `build-checklist.md` (the `Notion:` field), then the piece's brief or
   script in its content-project folder.
2. **No link? ASK — do not proceed and do not guess.** Use **`AskUserQuestion`** (HARD RULE: never
   guess a required input) to get the page URL from the user. A video built against the wrong page
   flips the wrong row's Stage and leaves the real piece stranded. **Never create a Content DB page
   to fill the gap** — if no page exists, that's a pipeline-order problem for the user to resolve, not
   something to paper over.
3. **Confirm it exists** — `notion-fetch` the page and read its current `Stage`. A link that 404s or
   resolves to a different DB is the same failure as no link: stop and ask.
4. **Set `Stage` → `Visual Editing`** in the same turn, unless it's already there (then note that and
   move on). Re-fetch to verify the write landed.
5. **Record the URL and the flip** in both progress files, with evidence (previous stage → new stage).

| | |
|---|---|
| Property | **`Stage`** — a **status** property (NOT "Status"). Use the exact option name. |
| Content data source | `collection://<CONTENT_DB_DATA_SOURCE_ID>` |
| Stage chain | `Idea → On Deck → Title/Thumb/Hook → Scripting → Visual Editing → Packaging/Posting → Published` |
| Expected inbound stage | `Scripting` (video pieces pass through `content-video-tags` first) |
| Tools | `mr-notion` — `notion-fetch`, `notion-update-page`. Per the Notion HARD RULE, fetch the instructions page `<INSTRUCTIONS_PAGE_ID>` before any Notion action. |

**Stage authority gate (the user, 2026-08-10).** Setting `Visual Editing` at build start is authorized
by beginning this workflow. A final export, render, scorecard, delivery copy, or correction pass
does **not** authorize `Visual Editing → Packaging/Posting`. Keep the verified current Stage until
the user explicitly directs the transition; only then update Notion and the KG from a fresh fetch.

## 🚦 DELIVERY GATE — BINDING, read before ever saying "ready"

**"Ready for review" is a gated claim, not a feeling.** No render is presented to the user, called
ready/final/done, or copied to the Drive delivery folder until EVERY hard gate in
[references/delivery-gate.md](references/delivery-gate.md) passes with written evidence:
G1 word-diff (final-timeline ASR vs script), G2 cut-safety, G3 no-debris scan, G4 head/tail
contract, G5 render pacing map, G6 visual spot-captures (zero stretch), G7 render integrity,
G8 checkpoint + scorecard artifacts, **G16 delivery loudness (−14 LUFS / ≤−1.0 dBTP, master EVERY export)**, **G17 text inside the 107px platform safe zone** — **plus polish gates P0–P9** (P0 cut-anchored transitions · P1 transition integrity · P2 real-artifact/no-emoji-slop · P3 no attribution footers in video · P4 calendar-grid for weekly quantities · P5 diagram content discipline · P6 hook velocity · P7 duplicate-take scan · P8 tick-only-on-containers · P9 extendable music bed). Then score the video (0–100 rubric in the same file) and
append a row to [references/eval-log.md](references/eval-log.md) so quality is measured across
videos. A user ERROR flag on a delivered video = mandatory postmortem + rubric review.
This gate was created 2026-07-20 after three consecutive flagged deliveries; it supersedes any
softer "verify before delivering" language elsewhere in this skill.

## Editing pipeline (in order)

The standard post-production sequence — **all palmier-pro** unless a row says otherwise. Trailing
marks are **verification status, not capability**: ✅ = confirmed by running it; ⚠️ = capable per
schema but not yet runtime-verified.

| # | Step | Key tools | Notes |
|---|---|---|---|
| 1 | [Ingest & media](references/pipeline/01-ingest.md) | `import_media`, `organize_media`, `get_media`, `inspect_media` | `import_media` is **async** — a placeholder id becomes the real asset id. |
| 2 | [Assembly / rough cut](references/pipeline/02-assembly.md) | `add_clips`, `insert_clips`, `get_transcript` | Source spans are **seconds**; timeline positions are **frames**. |
| 3 | [Editing / fine cut → picture lock](references/pipeline/03-editing.md) | `split_clips`, `move_clips`, `set_clip_properties`, `ripple_delete_ranges`, `remove_words`, `remove_silence` | Transitions are **keyframe-built** — Palmier has no transition engine. |
| 4 | [VFX, motion graphics & titles](references/pipeline/04-motion-graphics.md) | `add_texts` + `set_keyframes`, `apply_layout` | ⚠️ **AI subject cutout is the DaVinci exception** — see step 4b. |
| 4b | [Background removal](references/davinci-background-removal.md) | **fal.ai `bria/video/background-removal`** ✅ ($0.0042/s, alpha out) · Resolve **Magic Mask 2** = fallback | Palmier has chroma key only (`apply_effect` `key.chroma`) — needs a keyable backdrop. ⚠️ VP9 alpha is a SEPARATE layer: decode with `-c:v libvpx-vp9` or the matte looks like it failed. |
| 5 | [Captions / subtitles](references/pipeline/05-captions.md) | `add_captions`, `update_text` | ✅ single-line 2–4-word cues + word timings; karaoke via `animation` presets. |
| 6 | [🎨 Color grading](references/pipeline/06-color.md) | `apply_color` ⚠️, `inspect_color` ✅, `apply_effect` | **Step 6, near the end** — finishing, never first. Conform to full-res first. |
| 7 | [Audio / sound mix](references/pipeline/07-audio.md) | `volume` via `set_clip_properties`/`set_keyframes`, `denoise_audio` ⚠️, `sync_clips`, `generate_audio` | Parallel with color. |
| 8 | [Render / export & delivery](references/pipeline/08-delivery.md) | `export_project` — H.264/H.265/ProRes ⚠️, fcpxml ✅ | fcpxml/xml is also the interchange out to Resolve/Premiere. |

Steps 1–3 are upstream (edit), 4–8 are finishing. Picture-lock sits between 3 and 4.

## Gotchas that change which call you make

There is one backend, so this is not routing — these are the four places where the obvious call is
the wrong one. Per-step traps live in the pipeline files; the deep findings live in the capability
references.

1. **Transitions have no engine.** No presets, nothing CapCut-like (still true on the live
    manifest), and `import_media` imports media only, never effects. Fade-to-black/crossfade =
    native opacity keyframes. On-black overlay packs (burn/flare/glitch): `blendMode:"screen"` ⚠️
    should composite directly; the **ffmpeg luma-key → ProRes 4444 alpha** route is the ✅ verified
    fallback. Audio SFX align **frame-exact** via `add_clips` + `trimStartFrame` so the transient
    lands on the cut. See [palmier-transitions.md](references/palmier-transitions.md).
2. **Multi-clip canvas arrangements** (split screen / PIP / grid) → **`apply_layout`**, never
    hand-set transforms.
3. **Caption text edits cost karaoke on v0.6.5** — `update_text` content edits CLEAR the cue's word
    timings. Correct text beats karaoke; ship the static cue. See
    [palmier-captions.md](references/palmier-captions.md).
4. **A fullscreen graphic exists to HIDE a cut — so it is at FULL coverage ON the cut frame and the
    wipe never straddles it** (gate **P0**, the rule the user has given the most times). Entry: the 4
    moving frames run over the OUTGOING clip and finish on the cut. Exit: they start on the cut and run
    over the INCOMING clip. A visual also never ends before the talking-head clip under it ends. The
    square wipe is an animated `crop` on the upper clip so outgoing sits inside the square and incoming
    outside — **never** a black-panel iris-to-black.
    Recipe + inset table + how to move a graphic without dragging its beats:
    [palmier-transitions.md](references/palmier-transitions.md).
5. **The transition click lands on the ramp's first VISIBLE frame — ramp-start + 1, never keyframe 0**
    (at keyframe 0 the aperture is fully closed on an entry / fully open on an exit, so the transient
    fires ahead of the picture). And **b-roll linked audio must never share a track with your SFX** —
    an overlapping add trims it and the trim PROPAGATES to the video partner, splitting the clip and
    destroying its keyframes. Both in [palmier-pro.md](references/palmier-pro.md).
6. **Cut, then decorate.** Captions and graphics are timed to cut frames and do NOT follow later
    ripples, and a ripple through a music bed splices the melody in a way transient checks pass.
    Gate the cut before any visual or music work.

## 🚧 SINGLE-WRITER GATE — check for a second editor BEFORE any mutation

**There is ONE Palmier app and ONE open project. Two agents editing it corrupt each other.** the user
may invoke `/video-editor` more than once; both runs land in the same project with no warning and no
locking. On 2026-07-29 a second run added captions + a music bed while this run was doing audio
analysis; the next `ripple_delete_ranges` **spliced the other run's continuous music bed** (melody
jump — transient checks pass it).

Detect a second writer on EVERY `get_timeline` / `get_media`, not just at session start:

* **Media you didn't import** (`get_media` assets with unfamiliar names) = another writer. This is the
    loudest signal — check it first.
* **Tracks/clips you didn't create** (a caption group, a music bed, graphics) appearing mid-session.
* **`totalFrames` changed** since your last read without an edit of yours.
* **`currentFrame` moved** between reads = a human is scrubbing, or another agent is capturing.

On detection: **STOP mutating. Report it and resolve ownership with the user** (who owns the timeline;
what to keep). Never "merge" two agents' work by guessing. Re-read state fully after they answer —
your cached frame numbers are stale. Then keep the other run's good assets and own the rest.

## Always do first

Call `get_timeline` once at session start — returns fps, resolution, tracks, clips, `canGenerate`,
and (when >1) the project's `timelines` (multiple timelines + nested sequences are supported; edits
target the *active* one). If `canGenerate` is false, generation/upscale will fail → tell the user to
sign in to Palmier and subscribe. Call `get_media` before referencing any asset; `list_models`
before any generate/upscale.

**Then check canvas vs footage orientation.** Vertical source on the default 1920×1080 canvas must be
fixed BEFORE captioning: `set_project_settings({aspectRatio:"9:16"})` ⚠️ auto re-fits clips and
re-wraps caption groups. Verify with `inspect_timeline`; note `add_clips` can auto-flip project
resolution, so re-check after placing clips.

The MCP only responds while the **Palmier desktop app is running** (it bridges to a localhost
server) — a timeout or "unavailable" means the app is closed. Details:
[palmier-pro.md § Always do first](references/palmier-pro.md).

## Palmier Pro repeatable workflows (talking-head / take-reel)

Hard-won multi-step workflows with scripted verification gates. Scripts live in
[`scripts/`](scripts/) and drive the `palmier-pro` MCP directly.

> **Run every script in `scripts/` with `/usr/bin/python3`** (Apple's arm64 3.9). The Framework
> `python3` on this Mac is an **x86\_64 build** and its `numpy`/`PIL` imports die with
> `incompatible architecture (have 'arm64', need 'x86_64')` — `audio_env.py` and every gate script
> need numpy, so a bare `python3` wastes a cycle on an import traceback. `playwright` (for
> `scripts/anim/render_anim.py`) is also on `/usr/bin/python3`. For image dimensions prefer `sips`
> over PIL. Network note: the Groq ASR API is blocked from this sandbox — use Palmier's own
> `import_media` → `inspect_media` for transcription instead (see radio-edit lesson 11).

* **Check the app version FIRST** — `scripts/check_version.sh` prints installed vs latest
    (GitHub Releases for `palmier-io/palmier-pro`) + the changelog delta. Palmier ships
    multiple releases/week via Sparkle and its **MCP tool surface changes between versions**,
    so a stale build silently makes these workflows' workarounds wrong. If out of date,
    recommend the update to the user *before* building a workaround (it may delete the problem);
    updating needs an **app relaunch + reopen the project** AND a **full Claude Desktop quit +
    reopen** (the client caches the tool manifest), then re-verify the new tool via ToolSearch.
    Saturation caveat on old builds (\~v0.3.2): \~90 rapid mutations hang the app \~140s — batch
    array-calls and edit targeted, don't rebuild. `check_version.sh` tells you which
    workarounds a newer build retires.
* **Double-system audio/video sync** → [references/audio-video-sync.md](references/audio-video-sync.md).
    **Fast path: try `sync_clips` first** — mode `auto` aligns by embedded **source timecode** when
    both files carry one (exact, confidence 1.0) and falls back to audio cross-correlation;
    returns offsetFrames + confidence + method per target and refuses weak matches. Fall back to
    the manual by-content workflow when it refuses or the material lacks a scratch track. Either
    way, verify no drift and mute the camera scratch audio. Gate with `scripts/eval_sync.py`
    (median \|Δframe\| ≤ 5).
* **Radio-edit a take-reel → tight cut** → [references/radio-edit.md](references/radio-edit.md).
    Cut a synced talking-head reel down: pick the best take per line (drop repeats/false starts),
    cut only in true silence, anchor each clip start to the spoken word (not a pre-speech click),
    rebuild via `add_clips` + batched trims. **`remove_words`** ⚠️ (transcript-index cuts
    with pause handling + gap closing) is the fast path for filler words and flubbed spans; the full
    best-take workflow still owns take selection. Gate with `scripts/eval_cuts.py` (no mid-word cuts),
    `scripts/eval_takes.py` (no duplicate takes), `scripts/eval_onsets.py` (no pre-speech
    click/dead-air at heads), `scripts/score_cuts.py` (edges/dead-air), plus `scripts/snap_keeps.py`
    and `scripts/audio_env.py` helpers.
* **Plan the visual story (editorial layer — runs BEFORE authoring/placing anything)** →
    [references/visual-story-design.md](references/visual-story-design.md).
    Produces the **visual beat sheet** (every transcript beat classified by job — hook /
    show-the-thing / explain-the-concept / number / punchline / emotional / CTA — with ONE
    treatment each and a never-cover list for face beats), the **shot-request list for the user**
    (standard deliverable at build START: screen recordings, POV desk, over-shoulder,
    environment, detail shots → reusable b-roll bank), the **sourcing ladder** (b-roll =
    evidence: real artifact re-rendered from real data > screen recording > honest recreation >
    brand diagram > the user mood footage > AI-conceptual-only; stock banned), and the **coverage
    budgets** (face majority; 2–4 major graphics per 30–60s; full-cover b-roll 1–3s but
    split-screen exempt; diagram hold ≥3s by element count, ≤7 elements). Load for "plan the
    video", "what b-roll do we need", "make a shot list", or at the start of ANY talking-head
    build.
* **Enrich a talking-head cut → b-roll + graphics + transitions + pacing** →
    [references/palmier-talking-head-overlays.md](references/palmier-talking-head-overlays.md).
    The finishing pass on a captioned vertical cut — executes the visual-story-design beat
    sheet. **GATE FIRST: audit the base cut** — every
    clip boundary for mid-word cuts (`scripts/audit_cut_boundaries.py` + source-transcript ground
    truth), **first word ≤5 frames from frame 0**, and **no dead-air gap >0.6 s** (tighten via
    `ripple_delete_ranges`, right-to-left) — never build overlays on an unverified cut. Brand
    contract before authoring graphics: social-canvas rules apply to video (bg = dot grid + teal
    radial glow; danger = red #ef4444 never pink; lists count 1→N top-down). Then the rhythm:
    face anchor every 3–7 s · floats (alpha ProRes cards): top zone over the face, **exact canvas
    center over b-roll panels**, one element, no sub-lines ·
    split-screen b-roll (`apply_layout top_bottom`) with **white-flash + short subtle SFX** entries
    (article headlines get a baked zoompan push + ≥3.5 s linger) ·
    **full-screen brand diagrams** (frame-stepped HTML → `seek(f)` → MP4, cues timed to
    `get_transcript`, content in the **title-safe zone — central 82% horizontally (x∈[97,983])
    AND above the caption band y≈1400** so tall-phone cover-crop (\~9%/side) never slices a box,
    chip, or word; bg stays full-bleed; concept must match the spoken mental model — a "loop"
    visibly loops, 1.5–3.5 s linger after the animation settles; verify each render by cropping
    to central 82% and reading it) ·
    long canvas/app panels scroll CONTINUOUSLY with a jump-cut every \~3 s (never stall into a
    slow push) ·
    zoom punch-ins (scale+position hold-keyframe pairs, 1.15–1.3×) budget ≤2 per short: frame-0
    hook + ONE thesis word · no fade may
    straddle a base cut · bg music flat at **−25 dB (`volume 0.056`) — the standard** · final
    delivery = video to `marketing/video/<slug>-final.mp4` + a **thumbnail still** (hook frame,
    extracted from the render) to `marketing/images/thumbnails/<slug>-thumbnail.png` (separate
    folder, NOT beside the video).
    **Save discipline is mandatory** (Cmd+S checkpoints via computer-use;
    autosave-timer-only persistence — see reference §4). Load this for "add b-roll / overlays /
    diagrams / animations / transitions to my video" or "fix the pacing".

## The two DaVinci exceptions

Everything else Resolve's scripting API offers, Palmier does better or does at all. Resolve is
**not** the color backend, **not** the caption backend, **not** the delivery backend, and cannot
trim, split, or transition a clip at all. Reach for it only here:

1. **AI subject cutout on a real background** (behind a head, normal room) → **Magic Mask 2**,
    verified. 100% Color-page **UI/computer-use** — not scriptable. Palmier has chroma key only
    (`apply_effect` `key.chroma`, confirmed on the live manifest as the sole keying effect), which
    needs a keyable backdrop. Runbook:
    [davinci-background-removal.md](references/davinci-background-removal.md).
2. **The project already lives in Resolve** (a client `.drp`, or the footage is already conformed
    there) → assemble/mark/render in place, or bring it into Palmier. Interchange out of Palmier:
    `export_project({mode:"fcpxml", fcpxmlTarget:"resolve"})` ✅. Prerequisites, the api_truth
    ceiling, and what the API can still do: [davinci-resolve.md](references/davinci-resolve.md).

**Never claim a Resolve UI-only step was done programmatically.** If a task needs the UI, say so.

## Reference

**Pipeline steps (in order):** the 8 `references/pipeline/NN-*.md` files, linked from the pipeline
table above — the workflow spine. The capability files below hold the verified tool-level findings
each step draws on.

* **[Build checklist](references/build-checklist.md)** — STEP 0, BINDING: the on-disk sequenced checklist that is the system of record for every video build (the harness task list is in-memory and does NOT survive a reset). Template, phase ordering, and the evidence rule.
* **[Delivery gate + eval](references/delivery-gate.md)** — the BINDING pre-delivery gate (8 hard gates w/ evidence) + 0–100 scorecard; running scores in [eval-log.md](references/eval-log.md).
* [palmier-pro backend](references/palmier-pro.md) — the full 49-tool live v0.6.1 surface (audited 2026-07-05) **+ the v0.6.5 production delta (2026-07-11): call-shape changes (`add_clips` source-seconds spans, single-asset `import_media`, `set_keyframes []`-to-clear) and NEW bugs (`inspect_timeline` stuck at frame 0 → render-verify with ffmpeg; `add_clips` auto-flips project resolution; main-track-only `add_captions`; `update_text` kills word timings)**, AI generation flow, multi-timeline/project model, export, prerequisites.
* [palmier-pro captions](references/palmier-captions.md) — rich captioning ✅ runtime-verified (single-line cues, karaoke); content edits via `update_text` + animation presets; the v0.6.5 word-timing regression and the recut runbook.
* [palmier-pro color](references/palmier-color.md) — full grading via `apply_color` (primaries/wheels/curves/hue-secondaries/LUT) ⚠️ + `inspect_color` scopes ✅, plus the backend-agnostic **skin-tone / exposure targets** and the verified talking-head look.
* [palmier-pro animation](references/palmier-animation.md) — verified keyframe/motion findings (native position/scale/rotation/opacity/crop + interp) and the top-left vs center / normalized-scale traps.
* [palmier-pro transitions](references/palmier-transitions.md) — no transition engine; fades/dissolves keyframe-built; blend modes ⚠️ (`screen` for on-black overlays) with the ✅ ffmpeg luma-key → ProRes 4444 alpha route as verified fallback; frame-exact audio-SFX alignment; royalty-free sourcing (Mixkit CDN).
* [palmier-pro radio-edit](references/radio-edit.md) — cut a synced take-reel to a tight final cut (best-take-per-line, silence-only cuts, word-anchored starts); gated by `scripts/eval_cuts.py` / `eval_takes.py` / `eval_onsets.py` / `score_cuts.py`.
* [palmier-pro audio/video sync](references/audio-video-sync.md) — double-system sync (`sync_clips` fast path, then external clean audio → camera footage by content, mute scratch, verify no drift); gated by `scripts/eval_sync.py`.
* [Visual story design](references/visual-story-design.md) — the EDITORIAL layer, run before overlays: beat-sheet paper edit (beat jobs → treatments, never-cover list, one-idea-one-visual, keyword timing), b-roll-as-evidence sourcing ladder (real-data re-renders first, stock banned), the shot-request-list practice + b-roll bank, and coverage/cadence budgets (face majority, graphic-moment caps, diagram read-time by element count). Research-backed 2026-07-12 (Bird anchor points, OpusClip 13.5M-clip data, motion-design consensus) + 4 production passes.
* [palmier-pro talking-head overlays](references/palmier-talking-head-overlays.md) — the full enrichment playbook: base-cut audit gate (mid-word cuts + head silence + dead-air sweep) with caption-safe fix recipes, the brand contract for video graphics (teal-glow bg, red-for-danger, top-down lists), the v4 pacing rhythm (face anchor / centered floats without sub-lines / split-screen b-roll / full-screen diagrams with enforced linger + the 3 tight-beat exit hatches), zoompan headline panels, white-flash + subtle-SFX transitions, zoom punch-ins (edge-buffer rule: in ≥1s after the visible reveal, out on a cut/under a graphic), the opening-hook doctrine (motion + text hook ON frame 0, ONE camera move), caption cue-fill + per-clip style-verify gates, the pre-render design review (concept/fill/caption-clearance/motion/brand — §2), the post-the user-UI-edit cleanup recipe (§4b: non-ripple hole close + music-bed rebuild), render-based verification (§5 — inspect\_timeline broken on v0.6.5), the −25 dB music standard, the ≤2-punch budget, the thumbnail-still delivery rule, and the Palmier save-discipline (export\_project checkpoints; computer-use only with explicit OK) + bridge-recovery runbook. ✅ four production passes (v0.6.1–v0.6.5).
* [Motion-graphics overlays](references/motion-graphics-overlay.md) — the HTML/CSS → transparent ProRes 4444 render pipeline for branded animated text/lower-thirds/numbered lists, placed on a top track. Frame-deterministic `setTime` capture, webfont waiting, and the never-overwrite-a-file-in-use gotcha.
* [DaVinci background removal](references/davinci-background-removal.md) — **exception 1**: AI Magic Mask 2 → transparent cutout, with a \~7-action fast-path runbook. Color-page UI/computer-use only (not scriptable).
* [DaVinci Resolve backend](references/davinci-resolve.md) — **exception 2**: prerequisites, what the scripting API can still do on a project that lives in Resolve, the verified api_truth ceiling, and the fcpxml interchange.
