# davinci-resolve — the escape hatch (2 jobs only)

Controls **DaVinci Resolve Studio** through its official Python scripting API. Tools are
`mcp__davinci-resolve__<group>`; each is **action-dispatch** — call with `action` (string) and
`params` (object). Verified live on Resolve Studio 21.0.0.48, davinci-resolve-mcp 2.57.5.

**Palmier is the backend for video work.** Resolve is reached for exactly two things:

1. **AI subject cutout** on a non-green-screen background → **Magic Mask 2**, the one capability
   Palmier lacks. 100% Color-page UI/computer-use. Runbook:
   [davinci-background-removal.md](davinci-background-removal.md).
2. **A project that already lives in Resolve** — a client `.drp`, or footage already conformed
   there. Work in place (below), or bring it into Palmier.

Do **not** route color, captions, animation, fine editing, audio mixing, or delivery here. Palmier
does all of them, and for grading and captions its MCP surface is *wider* than Resolve's API.

## Prerequisites
- DaVinci Resolve **Studio** installed, ideally already open.
- Resolve → **Preferences → System → General → External scripting using = Local**.
- Tools auto-launch Resolve if closed (first call up to ~60s). A connection error means Studio
  isn't running or scripting is disabled. Force with `resolve_control(action="launch")`.
- Connect + orient: `resolve_control(action="get_version")`, then
  `project_settings(action="project_summary")` for a live structural readout.

## What the API CAN do on a Resolve project

Enough to assemble, annotate, grade coarsely, and deliver — not to edit.

| Job | Tools |
|---|---|
| Import + organize media | `media_storage.import_to_pool`, `media_pool` folders, `media_pool_item` |
| Build a timeline | `media_pool.create_timeline`, `create_timeline_from_clips` (positioned `clip_infos` + `recordFrame`), `append_to_timeline` |
| Read timeline state | `timeline.get_items` / `clip_where`, `timeline_item` getters (transform/crop/composite/opacity are settable) |
| Review markers | `timeline_markers.add` + `export_review_report` |
| Coarse grade | `timeline_item_color` — `grade_evidence_base` (pre-flight) → `safe_set_cdl` / `safe_apply_drx` / `safe_copy_grade`; `graph.set_lut` |
| Auto-subtitles | `timeline_ai.create_subtitles` (plain track; not editable/styleable via API) |
| Fusion / DCTL | `fusion_comp` (full node graph), `dctl`, `fuse_plugin` |
| Render + deliver | `render` — `set_format_and_codec` or `load_preset` → `prepare_render_job(target_dir)` → `start`; or `safe_quick_export`. 23 formats, 38 presets |

Full group list is discoverable from the MCP itself; `resolve_control(action="api_truth")` returns
~32 verified facts (bugs + missing methods) with workarounds — query it before assuming anything.

## API ceiling (verified — UI only, even in Studio)

**Not bugs in the MCP** — the Blackmagic scripting API does not expose these. Confirmed live on
Resolve 21.0.0. Don't attempt them; do the work in Palmier, or tell the user to finish in the
Resolve UI and **say so explicitly — never claim a UI-only step was done programmatically.**

* ❌ Trim / move / slip / slide / roll a timeline item (no position setters)
* ❌ Razor / blade / **split** a clip
* ❌ Insert / overwrite / replace / fit-to-fill edit modes (only `AppendToTimeline` + `recordFrame`)
* ❌ **Transitions** — add / read / copy (cross-dissolve etc. invisible to scripts)
* ❌ Per-parameter grading — lift/gamma/gain wheels, curves, qualifiers, power windows (only CDL,
    whole-grade DRX/LUT, copy)
* ❌ **Fairlight audio** — volume/pan/EQ/automation/FairlightFX (audio surface is read-only)
* ❌ Clip **speed / retime ratio / speed ramps** (only retime *quality* settable)
* ❌ Proxy / optimized-media **generation** (only link/unlink existing)
* ❌ Subtitle **text/timing/style** editing, SRT import; native multicam clip creation; media-pool
    folder rename; smart/power bins
* ❌ **Magic Mask** — not in the object model at all (hence the UI runbook)

## Safety model (three layers)
1. **MCP confirm-tokens** — catastrophic ops (`delete_timelines`, `delete_folders`, grade resets)
   return `CONFIRMATION_REQUIRED` with a `confirm_token` (300s TTL) + preview; re-call with
   `params.confirm_token`.
2. **Claude Code auto-mode classifier** — independently blocks destructive ops on objects the agent
   didn't create this session. If blocked, stop and ask — don't work around it.
3. **Version-on-mutate** — destructive timeline ops auto-archive first (`<name>_archived_vNN`).
   Group multi-step work with `timeline_versioning.begin_run`/`end_run` for one archive, not N.

Prefer `safe_*` / `probe_*` / `*_capabilities` / `dry_run` variants over raw mutators.

## Interchange
Palmier → Resolve: `export_project({mode:"fcpxml", fcpxmlTarget:"resolve"})` ✅ live-verified
(carries text/transforms/crop/opacity/keyframes).

## Two traps that waste a verification loop
- **`item_index` is 0-BASED.** First clip on a track = `0`. Grading "the first clip" with
  `item_index: 1` silently grades the *second* and returns `success: true`.
- **Still-export reflects ONLY the clip under the playhead.** `export_frame_as_still` and
  `get_thumbnail_image` capture wherever the playhead sits — grade one clip, park on another, and
  every still shows ungraded footage, which reads as "grades don't render." Park the playhead
  inside the target clip first (`timeline_markers.set_current_timecode`), *then* export. Stills also
  do **not** composite subtitles, so caption styling can't be pixel-verified via the API.
