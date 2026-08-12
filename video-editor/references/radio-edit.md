# Radio-edit a talking-head take-reel (Palmier Pro)

Cut a double-system talking-head recording (camera video + clean external audio) down to a
tight final cut: drop pauses/filler/dead-air, and for every repeated line keep the single best
take. Built + hardened on "Stay, Split, Commit" (2026-06-18/19). Load this when the user wants to
"radio edit", "cut the pauses/ums", "pick the best takes", or assemble a YouTube talking-head.

> **v0.6.1 fast path for the filler/flub layer: `remove_words`** ✅ (run for real 2026-07-05:
> 6 sentence-spans / 99 words / 1299 frames in one call, all seams verified clean) — cuts speech by `get_transcript`
> word indices/spans or exact `matches` (["um","uh"]), removes surrounding pauses, merges adjacent
> cuts, cuts linked A/V, closes gaps (`cutAggressiveness` tight/balanced/loose; one track per call;
> re-read the transcript after each call — indices shift). Use it for pauses/filler/flubbed spans;
> **best-take selection stays with this workflow** (remove_words doesn't judge takes). Also new:
> `split_clips` (batch, renamed from `split_clip`). Gates below still apply.

Prereq: the timeline is already double-system **synced** (see [audio-video-sync.md](audio-video-sync.md)):
V1 = camera video, A1 = clean audio advanced by the sync offset `TRIM` frames (here 25), A2 =
camera scratch audio, muted, linked to V1.

## Two layers — keep them separate
1. **WHICH to keep** = content. From the **script** (target wording/order) + the **clean-audio
   transcript** (what was actually said, source seconds). For each script line, find its take(s);
   pick the single best — **last + complete + closest to the script**. **For any repeated line,
   keep exactly ONE take.** Output = rough keep ranges in clean-audio *source seconds*.
2. **WHERE to cut** = silence. Never cut mid-waveform. `snap_keeps.py` snaps each range so both
   boundaries land in true silence **relative to the real noise floor** (~floor+12dB), not a fixed
   −30dB (which slices word tails). Use `--min-sil 0.05` to separate takes that butt together.

## Pipeline
0. **Check the app version FIRST** — `scripts/check_version.sh`. Palmier's MCP surface changes every
   release and several steps below have native replacements in newer builds (capability map in
   [SKILL.md](../SKILL.md)). If out of date, recommend updating before hand-rolling a workaround —
   it may delete the problem. Everything below is the **v0.3.2** baseline.
1. **Transcript**: on **v0.3.4+** use the native `get_transcript` MCP tool (words nested in v0.3.5,
   which also saves agent context). On older builds: `scripts/get_transcript.py`-style chunked
   `inspect_media` over the clean-audio source (a single 0–end call times out; window ~200s, save
   incrementally). Rows = `[text, start, end]`.
2. **Take selection** → rough ranges (source seconds), one per kept line, dupes collapsed to the best take.
3. **Silence-snap**: `snap_keeps.py --audio clean.mp3 --trim 25 --keeps-sec '[...]'` → project-frame keeps.
4. **Execute** (see "Reliability" — do NOT use hundreds of split_clips calls):
   - **v0.3.5+**: `add_clips` accepts `trimStartFrame/trimEndFrame` on placement → place each clip
     already-trimmed in ONE pass (no second `set_clip_properties` sweep). Use `insert_clips` /
     `ripple_delete_ranges` / timeline-wide ripple (with undo) instead of manual gap math.
   - **v0.3.2** (no trim-on-add): reset to pristine, then **rebuild each track with `add_clips` +
     batched `set_clip_properties`** — `add_clips` places at `[startFrame, dur]` (cumulative ripple
     positions) but **cannot set `trimStartFrame`**, so set `trimStartFrame` (V1: `fs`; A1: `fs+TRIM`)
     + `durationFrames` per clip afterward.
   - **For a few-clip fix, edit targeted — never rebuild the whole timeline** (see Reliability).
5. **Gates — ALL must pass** (run after every edit):

| Gate | Script | Catches |
|------|--------|---------|
| Cut safety | `eval_cuts.py --audio clean.mp3` | any cut not in silence = a clipped word (hard rule) |
| **Take dedup** | `eval_takes.py --transcript t.json` | **a clip that repeats a line / a restart, or two adjacent takes of one line** |
| **Clean onset** | `eval_onsets.py --audio clean.mp3` | **a pre-speech mouth-click / breath, or dead-air, at the head of a clip (waveform before the word)** |
| Edge/dead-air | `score_cuts.py --audio clean.mp3` | tight/long edges; internal pause >300ms left uncut |
| **Black hole** | union video-clip picture spans (all video tracks, exclude text/captions) → any frame in [0,total) covered by none | **a silent inter-clip gap that renders BLACK** — pre-existing pauses survive `remove_words`; word-seam checks are blind. **Fix = CLOSE the gap (ripple downstream clips left), never extend the prior clip to fill it — that re-adds the silence you cut** (2026-07-05) |
| Sync | `eval_sync.py` (or assert A1 trim == V1 trim + TRIM for all clips) | A/V drift |

`eval_takes` is the gate that was missing: cut-quality gates are blind to content, so a cut can
pass eval_cuts/score_cuts while the audio still says "Three paths lie before you. Three paths lie
before you." It assigns each transcript segment to ONE clip by **midpoint** (a segment spanning
two clips would otherwise double-count and fake a duplicate), then flags internal + adjacent repeats.

**Onset anchoring (pre-speech clicks).** A cut can land in silence (eval_cuts OK) yet the clip
still *opens* with a faint mouth-click/breath sitting in a long silent lead-in — sound above the
noise floor but not speech, which shows as a waveform before the speaker talks. Root cause: anchoring
the clip start to "first sound above the floor." Fix: anchor to the **first SUSTAINED speech** (energy
that holds ≥150ms) minus a ~50ms lead, snapped to deep silence — the click/breath then falls on the
discard side. `eval_onsets.py` flags any clip whose lead-in is long or holds a pre-speech transient;
re-anchor those clips' in-points (keep out fixed). Aim for a ~50ms median lead-in across all clips.

## Take-selection rules (from the user)
- Cut pauses, filler ("um/uh"), dead air, **and every repeated take but the best one**.
- Best take ≈ **last** take and the one that **matches the verbatim script**.
- Gaze: eyes-off-camera only disqualifies a take on a genuine *to-camera* line. If the script marks
  the line `[SCENE]/[DOODLE]/[B-ROLL]/[MEME]/[ANIMATE]/[QUOTE]` (face not shown), pick the
  **better-sounding** take regardless of gaze.

## Reliability — the Palmier app is the bottleneck (hard-won, v0.3.2)
**Run `scripts/check_version.sh` first.** Most of this section is a workaround for v0.3.2 limits that
later releases retire — v0.3.4 (`ripple_delete_ranges`, `get_transcript`) and v0.3.5 (`add_clips`
trim-on-place, `insert_clips`, timeline-wide ripple **with undo**, three fatal-crash fixes). Prefer the
native primitive whenever it exists; treat the workarounds below as the fallback for an un-updated app.

- **It saturates** after ~90 rapid mutations (split/set_clip_properties) and goes unresponsive;
  it **drains in ~140s** then recovers. So: **batch ≤15–40 mutations, then wait for drain**
  (poll until a `get_media` returns in <3s) before the next batch. Make every batch resumable
  (recompute the to-do set each run; `set_clip_properties` is idempotent).
- **Batch into ONE call, and edit targeted — don't full-rebuild.** `add_clips`, `move_clips`,
  `remove_clips`, and `set_clip_properties` each accept an **array in a single undoable call**. The
  *only* thing that needs N calls is N **different** per-clip values — `set_clip_properties` applies one
  value-set to every clip in `clipIds`, so N unique `trimStartFrame`s cost N calls, but N position
  shifts cost **one** `move_clips`. To fix a few clips: change only those clips' trim/duration, then
  **one batched `move_clips` shifting the downstream suffix left** to re-close the gaps (~16 calls, 0
  drains). Rebuilding all ~334 clips for a ~7-clip change (~20× the calls, ~4 drains) is the mistake
  that caused the repeated ~30-min cycles. **Reserve full rebuild for the initial assembly only.**
- **Avoid the split path for big cuts.** Splitting a clip per cut = ~2 calls/keep/track → ~670 calls
  for one track → it dies past the wall. **Rebuild with `add_clips` + per-clip `set_clip_properties`**
  (~5 adds + ~N trims) instead. On v0.3.2 `add_clips` rejects `trimStartFrame` ("unknown field") — set
  it after; **v0.3.5+ accepts it on placement** (one pass).
- **Ripple corruption (v0.3.2 `move_clips`; v0.3.5 `insert_clips`/timeline-wide ripple do this safely
  — prefer them).** Re-trimming clips then `move_clips`-rippling to close gaps can let a moved clip
  transiently overlap a neighbour, and the overlap-trim silently shaves a few frames off the
  neighbour's in-point — pushing it INTO speech (a mid-word cut that wasn't there before). Two safe
  ways on v0.3.2: (a) **targeted** — shift the downstream suffix in a *single* batched `move_clips`
  moving each clip LEFT into already-vacated space (each moves away from its right neighbour, so no
  transient overlap); (b) **full rebuild** — compute the final keep-list, `add_clips` at explicit
  cumulative positions WITH final durations, then set **trim only** (position/duration never change →
  no overlap). Either way, since this bug bit once, **offline-verify the result with `eval_cuts`
  before trusting it** — cheap, and it catches any in-point that slid into speech.
- **Make the rebuild resumable + saturation-resilient.** Re-init retries through HTTP 400 / hangs with
  backoff; set trims in small batches with a drain-wait between; a batch that saturates mid-way is
  retried after draining (idempotent), not fatal. Guard the "skip rebuild" resume check on clip
  *durations* matching the target — count alone matches a half-built timeline and skips the real work.
- **Never `get_timeline` while an edit is running** — the full timeline is large and concurrent reads
  contend, hanging both. Read only between edits; use windowed `get_timeline(startFrame,endFrame)` when
  you need just a region.
- **Pin the source audio locally**: `cp` it to `/tmp/clean.mp3`. Google Drive CloudStorage paths
  de-materialize to cloud-only and have irregular whitespace — a wrong path makes the gates analyze an
  **empty file** (floor −90dB, 0 cuts = a *vacuous* PASS). Always confirm `analyze` returns `dur_s > 0`.
- Keep the V1↔scratch link intact; edit V1 + the independent A1 and the scratch follows. Never
  `remove_tracks` the scratch (orphans the link → a remove can cascade the whole group).
- **Linked-delete asymmetry (when deleting a clip).** `remove_clips` takes the whole link group, so
  removing a V1 video clip also removes its muted camera-scratch partner — but the clean-audio **A1
  clip is a separate asset, NOT in that link group**, so it stays. To drop a take cleanly: `remove_clips`
  the V1 clip **and** the parallel A1 clip (two ids, one call), then close both gaps with one batched
  `move_clips` (the V1 scratch follows V1; A1 needs its own shift). Re-verify with `eval_cuts`.
- Identify tracks/clips by **stable id / sorted index**, re-find after every mutation (arrays reorder;
  emptied tracks auto-remove).

## Status (Stay, Split, Commit)
Mechanical cut + sync solved and gated (167 clips, ~10.8 min). `eval_takes` added after the subagent
EDL shipped duplicate takes the cut-quality gates missed; `eval_onsets` added for pre-speech clicks.
5 stutters fixed; ~7 stutters + 2 head-pauses remained flagged. Open: 27 clips hold an internal pause
>300ms (score_cuts).

**Two lessons hardened into this skill (2026-06-20):**
1. **Version-drift:** the running app was **v0.3.2** while latest was **v0.3.5** — and v0.3.4/0.3.5
   already shipped native `ripple_delete_ranges` / `insert_clips` / `add_clips` trim-on-place that
   obsolete the rebuild + two-pass workarounds. Lesson → `check_version.sh` at session start, always.
2. **Targeted-edit, not full-rebuild:** repeatedly rebuilding all 334 clips to change ~7 (the
   "30-min rebuild × 5" cost) was self-inflicted — `move_clips`/`set_clip_properties` batch in one
   call, so a few-clip fix is ~16 calls with no saturation. Full rebuild is for initial assembly only.

**Lesson hardened 2026-07-20 (meeting-prep short — the user flagged ERROR: silences shipped):**
3. **Never derive dead-air cut margins from ASR word timestamps — they drift early into silence,**
   so every cut ends 15-20f short and a systematic ~0.6s pause survives after sentence-initial words.
   The sweep LOOKS complete (transcript word gaps ≈ margins) and captures can't reveal audio.
   Correct loop: render (or extract the voice), run energy-based detection with the threshold
   **clearly ABOVE the music bed** (bed at -25dB ⇒ `silencedetect=noise=-22dB:d=0.45`; a threshold
   at/below the bed level reports only the sub-threshold slivers of each pause and you'll cut 1/3 of
   the real gap — this exact mistake shipped twice on 2026-07-20). Convert [start,end] to frames and
   cut each gap to leave ~8-9f (4-5f head pad after the word tail, 8f+ pad before the energy-resume
   point — NOT the ASR next-word start). Protection: a gap that CONTAINS a mid-clip ASR word
   ("ask.", "type,") is a quiet trailing word — don't cut it.
   **Gate before delivering: silencedetect at bed+3dB on the FINAL render must show zero mid-sentence
   gaps ≥0.5s** (beat-boundary pauses and an intentional CTA hold are the only exceptions).

**Lessons hardened 2026-07-20, same short, THIRD the user-flagged ERROR (word amputation + sliver debris):**
4. **RETRACTION: an earlier draft of lesson 3 said "an ASR word stamped exactly at a clip head is
   usually a GHOST — trust energy." That heuristic is WRONG and caused the worst damage of the
   project.** Treating clip-head ASR words as ghosts (and cutting up to the energy-resume edge with
   thin pads) amputated ~12 real sentence-initial words ("If", "First", "Who's", "Each", "Context",
   "One", "I", "The") and fully deleted three load-bearing ones: "instructions. For" (broke the
   principle line), "loop" (broke the payoff), and "Comment" (broke the CTA). Direct ASR evidence of
   head-clipping: "Each one" transcribed as "E one". Rule: **an ASR word at a clip head is REAL until
   proven otherwise** — verify by listening/energy before cutting near it, and always leave pad on
   BOTH sides of a cut, landing in silence, never at an energy edge.
5. **Never iterate render → silencedetect → ripple as a repair loop.** Every global-ripple pass whose
   ranges don't exactly match existing clip boundaries strews 1-8-frame orphan slivers (visible
   jump-cut flashes; this short accumulated ~12, including a 2-frame pre-speech clip at frame 0) and
   re-cuts already-tight speech. Compute the keep-list ONCE from the SOURCE audio (energy-snapped,
   word-time cross-checked — snap_keeps.py) and assemble in one pass. That is this skill's original
   architecture; it exists precisely to prevent this failure.
6. **The gate table above is mandatory on EVERY project — no single-system / already-assembled
   exemption.** eval_cuts would have flagged every amputation in lesson 4; it was skipped because the
   timeline "wasn't the double-system setup the scripts were written for." Extract the render/timeline
   audio and run the gates anyway. Additionally, run this **final-timeline structural QC** before any
   delivery:
   (a) **Transcript diff** — ASR the final timeline (`get_transcript`) and diff word-by-word against
       the script; any missing or mangled word is a defect. This is the one gate that catches
       amputations, silencedetect can't.
   (b) **Sliver scan** — flag any video clip <8 frames that isn't fully covered by a flash/transition;
       every flagged clip is debris to remove (they read as glitch flashes and clutter the timeline).
   (c) **Head/tail contract** — first clip starts ≤6f before the first word's onset (zero pre-speech
       source frames); last clip ends ≥12f after the last word's energy tail (never clip the decay).
   (d) **Silencedetect gap gate** (lesson 3).
   A fix pass gated only against the PREVIOUS failure mode is how new failure modes ship — after any
   repair, re-run ALL gates, not the one that caught the last bug.
8. **LEVEL THE DIALOGUE FIRST — the root cause under the entire 2026-07-20 saga.** The speaker's
   sentence tails/pickups sat 8-25dB below their loud words; under a −25dB music bed they READ as
   silence on both the meter and the user's ear, while being uncuttable (they're words). Three
   tightening passes fought the symptom. The fix is the standard editor move skipped at step 1:
   compress/level the voice track before judging pacing (compand curve in
   [delivery-gate.md](delivery-gate.md) G0; Palmier's clip volume caps at 1.0, so level
   externally, import, mirror the V1 spans on a new track, mute the original linked audio).
   Also: silencedetect windows split by <0.15s clicks/breath blips are ONE perceived lull —
   always MERGE before applying any length spec (0.87s lulls hid as 0.4s window pairs).
7. **Quiet-word triage (the user's paired rulings, 2026-07-20): no perceived silence AND no cut
   words.** Judge lulls on the render meter (no non-designed window ≥0.8s at bed+3dB); before
   cutting a lull zone, MEASURE each contained word's raw source peak: audible → protect;
   quiet-but-real (−20…−35dB) → keep/restore + externally-boosted audio overlay (Palmier volume
   caps at 1.0 — ffmpeg-boost outside, import, overlay on a spare track); off-mic (<−40dB) → no
   recoverable audio exists, cuttable if the sentence reads grammatically without it (verify
   captions) and the measurement is documented. Tightening recipe: cut `[window_start+6f,
   window_end−8f]` per render silencedetect window (d≥0.62), edges snapped to clip boundaries
   within 7f; the 8f end-pad protects the audible onset wherever it truly is — trust render
   energy, never ASR stamps. Full gate + scorecard: [delivery-gate.md](delivery-gate.md).

**Lessons hardened 2026-07-29 (construction-tech-adoption build — 2 flub-bleed defects caught at G1):**

9. **`snap_keeps.py --per-phrase` selects phrases by MIDPOINT and emits the WHOLE phrase** — it does
   NOT clamp to your requested range. When your editorial range is *tighter* than the ASR phrase
   (because you're cutting a line that butts against a keeper with no silence between), it overshoots
   and **splices the cut content back in** (asked for 242.76–249.24, got 243.7–254.33, which swallowed
   a line meant to be dropped). It also *skips* ranges whose phrase straddles the range start
   (`NO speech in range`). **When ranges are hand-set editorial boundaries, write a clamped snapper**:
   clip candidate speech regions to `[a0,b0]` first, then split at gaps ≥ SPLIT_GAP, then snap each
   boundary with two hard guards — (1) never end BEFORE the current word's own energy ends
   (anti-amputation), (2) never end AT/AFTER the next speech region's onset (anti-bleed) — and sit at
   the quietest point inside that window. A `+1 frame` pad applied blindly re-crosses guard (2); only
   pad if the padded frame is still ≤ silence threshold.
10. **`--merge-gap` silently merges a good take with the flub that follows it.** A 0.50s pause sat
    under the 0.60s merge-gap, so "…ask them why," and the flubbed "continue interviewing users and"
    became ONE phrase and 2.5s of flub shipped into the cut. Boundary-quality gates are blind to this
    (every cut was in true silence). **Gate CONTENT per kept range, not just cut quality**: probe each
    range's audio and read the transcript back (below). Any pause ≥0.35s inside a kept range is a
    candidate take boundary — check what's on both sides before trusting the merge.
11. **G1 must run on a CONTINUOUS transcript of the assembled audio — per-clip ASR is unusable.**
    Palmier's per-clip `get_transcript` **systematically drops the first word of every clip** (16
    false "amputation" alarms in one pass: Using / I / If / Step / Once / Compare / Then / This / Now /
    Plan / Gate / Ideally / Final / New / Rollout / Present — all actually present). Reliable method:
    build the cut's audio locally **sample-exact** (slice the leveled wav by
    `samples = round(frames*SR/30)` and concatenate — ffmpeg `concat` with inpoint/outpoint drifts
    ~1.5s over 30 clips and won't map to frames), `import_media` it, then `inspect_media` → one
    continuous segment list. That is what caught both real defects here. To pin an intra-phrase
    boundary, extract a 2–4s probe window, import it, and inspect it — the returned segment text tells
    you exactly which words live in that span (probe `[355.60,358.30]` returned
    "Continue interviewing users and", proving the keeper ended 2.5s earlier).
12. **ASR *segment* start times drift EARLY into the preceding silence** — the reel's ASR said a line
    began at 1.26s when the speech onset was 2.43s. Never derive a clip head from a segment stamp;
    derive it from the energy envelope and use the stamp only to identify *which* words are in range.
