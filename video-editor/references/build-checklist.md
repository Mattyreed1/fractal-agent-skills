# Build progress + checklist — the on-disk system of record for every video project

**The harness task list is NOT the system of record. It is in-memory and a session reset,
compaction, or crash wipes it.** That happened on the tech-adoption-framework build
(2026-07-29): the whole sequenced checklist vanished mid-build and had to be reconstructed
from conversation context. the user: *"this should not be possible … make sure this never
happens again."*

## Where the files live (exact — do not guess)

```
projects/fractal-ai-content/<YYYY-MM-DD>-<slug>/build-progress.md    ← the user opens this
projects/fractal-ai-content/<YYYY-MM-DD>-<slug>/build-checklist.md   ← the agent works from this
```

…or `projects/founder-freedom-content/…` for Founder Freedom pieces. Paths are relative to the
the project repo root (`~/the project`), and the folder name **always carries the date
prefix**: `projects/fractal-ai-content/2026-06-17-tech-adoption-framework/`.

**Finding an existing piece's folder:** `ls projects/fractal-ai-content/ | grep -i <keyword>`.
Content pieces are a deliberate **no-KG-node bucket** (projects/README.md), so don't search the
knowledge graph for a `folder` property that was never created — listing is correct here.

## The binding rule

**Before touching a single frame of any video build, write BOTH files from the templates
below.** Together they are the source of truth for what is done, what is verified, and what is
next.

- **Instantiate them FIRST** — before `get_timeline`, before importing, before cutting. This is
  step 0, not documentation written afterward.
- **Update BOTH the moment an item is verified**, in the same turn as the verification. Not
  batched, not at the end. **A stale `build-progress.md` is worse than none** — it reports the
  build as further along than it is, which is exactly the false-completeness failure the
  CLAUDE.md evidence gate exists to stop.
- **An item is `[x]` only with written evidence** on the line — a number, a command result, a
  gate verdict. `[x] looks good` is not a completion; `[x] PASS — 30/32 boundaries in true
  silence, 3 exceptions at local minima −69.7/−69.3/−59.6 dB` is.
- **On ANY context loss** (reset, compaction, resumed session, `/clear`), re-read both files
  BEFORE doing anything else. They tell you exactly where you are.
- The harness task list may **mirror** them for live UI, but never replaces them. If they
  disagree, the files win.

## Division of labor

| File | Audience | Answers |
|---|---|---|
| `build-progress.md` | **the user** | "How far along is this video?" — in the first 10 lines, without reading the ledger. Phase, count complete, what's next, blockers, runtime math. |
| `build-checklist.md` | the agent | "What exactly is verified, with what evidence, and what is the next dependency-ordered step?" |

## Template — `build-progress.md` (the user's view)

The header must be readable at a glance: **status line, count, current phase, next action,
last-updated.** The status table carries one row per phase with an emoji state and the evidence
that earned it. Keep `⬜ not started` rows visible — what is NOT done is the point of the doc.

```markdown
# Video build progress — <title>

**Brand:** <Fractal AI | Founder Freedom> · **Platform:** <> · **Format:** <>
**Notion:** [Content DB page](<url>) · Stage: `Visual Editing` ← REQUIRED, never blank. No link
means the build hasn't legitimately started: ask the user for it (AskUserQuestion), confirm the page
exists, flip Stage to `Visual Editing`, then fill this line.
**Editor:** Palmier Pro <version> (latest <version> — <update decision + who made it>)
**Last updated:** <YYYY-MM-DD HH:MM TZ>

---

## Where it stands: <one-sentence plain-language status>

**<N> of <M> phases complete.** <What is locked, and what is still ahead.>
**Next:** <the single next action>
**Blocked on:** <the user decision / missing asset / nothing>

| # | Step | Status | Evidence |
|---|------|--------|----------|
| 1 | <step> | ✅ done | <measured evidence — numbers, not adjectives> |
| 2 | <step> | 🔄 in progress | <what has run so far> |
| 3 | <step> | ⬜ not started | <dependency, if it is waiting on something> |
| 4 | <step> | ⛔ blocked | <what is needed to unblock> |

---

## Runtime: <actual> (target was <target>)

| Selection | Runtime |
|---|---|
| Everything recorded, flubs removed | <> |
| <intermediate selection> | <> |
| **Shipping cut** | **<>** |

## Decisions + directives on this build
- <YYYY-MM-DD> — <the user's directive, quoted, and how it was applied>
```

Status vocabulary — use these five, nothing else: `✅ done` · `🔄 in progress` ·
`⬜ not started` · `⛔ blocked` · `n/a` (with the reason).

## Template — `build-checklist.md` (the mechanical ledger, in dependency order)

**Do not reorder the phases.** Phases 1–4 are the audio/edit foundation. **Everything visual comes
after the cut is gated**, because any later ripple moves every cut and desyncs every overlay
(delivery-gate meta-rule #2). Never start graphics on an ungated cut. The `## N ·` phase numbers
here are what `build-progress.md`'s status table rows map to — keep the two in step.

```markdown
# Build checklist — <title>
Brand: <Fractal AI | Founder Freedom> · Platform: <> · Format: <> · Slug: <>
Notion: <url> · Palmier version: <> · Target runtime: <>
Started: <YYYY-MM-DD> · Last updated: <YYYY-MM-DD HH:MM TZ>

## 0 · Intake
- [ ] **Project folder exists** at `projects/<brand>-content/<YYYY-MM-DD>-<slug>/` with `assets/src/`, `assets/renders/`, `gfx/` created (evidence: path )
- [ ] **Notion content page link resolved** — asked via AskUserQuestion if absent, NEVER guessed, NEVER created (evidence: url )
- [ ] **Page confirmed to exist** via `notion-fetch`; previous Stage recorded (evidence: was `<stage>` )
- [ ] **Stage set to `Visual Editing`** in the same turn + verified by re-fetch (evidence: )
- [ ] Brief/script read; runtime target confirmed with the user (evidence: )
- [ ] Ambiguous inputs resolved via AskUserQuestion — never guessed (evidence: )
- [ ] `check_version.sh` run; update-or-proceed decision recorded (evidence: )
- [ ] Assets inventoried: source footage, diagrams, b-roll bank ls'd LIVE, music (evidence: )
- [ ] Shot-request list emitted to the user if any footage is missing (evidence: )

## 1 · Source + G0 leveling
- [ ] Source `cp`'d off CloudStorage into **`assets/src/`** in the project folder — NOT the scratchpad (evidence: )
- [ ] Probed: duration, WxH, rotation metadata, fps, audio rate (evidence: )
- [ ] G0: loud-word vs sentence-tail peaks measured (evidence: )
- [ ] G0: leveled if tails >6 dB down; floor unchanged, no limiter slam (evidence: )

## 2 · Take selection → EDL
- [ ] One best take per script line; every repeat dropped (evidence: )
- [ ] Editorial cuts to hit runtime listed explicitly for the user (evidence: )
- [ ] Every boundary energy-snapped into true silence (evidence: )
- [ ] Runtime projected vs target (evidence: )

## 3 · Assembly
- [ ] Canvas set to 9:16 1080x1920 (evidence: )
- [ ] Clips placed; **resolution re-checked after add_clips** (it auto-flips) (evidence: )
- [ ] Zero gaps in the base video track (evidence: )
- [ ] Leveled voice mirrored on its own track; camera audio MUTED (evidence: )
- [ ] `.palmier` checkpoint exported (evidence: )

## 4 · Cut gates — ALL pass before any visual work
- [ ] **G1** word fidelity: continuous ASR of assembled audio vs script (evidence: )
- [ ] **G2** cut safety: no boundary lands on speech energy (evidence: )
- [ ] **G5** pacing: merged lulls, none >=0.45s non-designed (evidence: )
- [ ] **G3** debris: no clip <8f, no phantom tracks, linked A/V equal (evidence: )
- [ ] **G4** head/tail: first word <=6f from 0; last decay + >=12f room (evidence: )

## 5 · Captions
- [ ] `add_captions` applied; style matches brand (evidence: )
- [ ] Cues butt-joined, no inter-cue gap >1f (evidence: )
- [ ] Caption text gated against the SCRIPT, not the ASR (evidence: )

## 6 · Visual beat sheet (editorial layer — before authoring anything)
- [ ] Every beat classified by job; ONE treatment each (evidence: )
- [ ] Never-cover list marked: hook, credibility, punchline, CTA (evidence: )
- [ ] Assets mapped per beat via the sourcing ladder; stock banned (evidence: )
- [ ] Coverage budget checked: face majority, 2-4 major graphics per 30-60s (evidence: )

## 7 · Graphics authoring
- [ ] Brand contract applied: #09090b + dot grid + teal glow; red #ef4444 never pink (evidence: )
- [ ] All content in central 82% (x 97-983) AND above y1400 (evidence: )
- [ ] Pre-render design review on contact sheet: concept / fill / clearance / motion / brand (evidence: )
- [ ] Each render crop-verified at central 82% and READ (evidence: )
- [ ] `gfx/` source dir copied to the durable `<slug>-assets/` folder (evidence: )

## 8 · Placement
- [ ] Graphics on keyword cues from a fresh transcript (evidence: )
- [ ] Flashes are opaque H.264 VIDEO (image clips are banned), peak ON the cut (evidence: )
- [ ] SFX: soft click, cut-3, vol 0.22 (evidence: )
- [ ] <=2 zoom punches total (evidence: )
- [ ] Music: ONE clip, lowpass 6500, STATIC volume 0.056, zero keyframes (evidence: )
- [ ] No fade straddles a base cut (evidence: )

## 9 · Delivery gate (re-run ALL from scratch on the final render)
- [ ] **G6** visual composition, 15-item sweep on rendered frames (evidence: )
- [ ] **G7** render integrity: ffprobe duration/res/fps/audio (evidence: )
- [ ] Music ship-check: bed audible, >=18 dB below voice peaks (evidence: )
- [ ] **G8** checkpoint + scorecard written + eval-log row appended (evidence: )
- [ ] Thumbnail extracted from the FINAL render (evidence: )
- [ ] Video -> `marketing/video/<slug>-final.mp4` (evidence: )
- [ ] Thumbnail -> `marketing/images/thumbnails/<slug>-thumbnail.png` (evidence: )
- [ ] **G9** Stage authority checked: no stage change without the user's explicit direction; if directed, Notion re-fetch recorded (evidence: )
```

## Why the order is what it is

- **G0 before take selection** — quiet tails read as silence and make you cut pacing that
  isn't there. Leveling first prevents three wasted tightening passes.
- **All cut gates before captions and graphics** — captions are timed to word frames and
  graphics to cut frames. A ripple after either invalidates both.
- **Beat sheet before authoring** — treatments picked at placement time optimize each beat in
  isolation and miss story-level cadence.
- **Delivery gate re-runs everything** — a fix pass gated only against the previous failure
  mode is how new failure modes ship.

## FINAL POLISH PASS (added 2026-07-30 — run as its own checklist block before "ready")

Copy into every build's `build-checklist.md` as the last phase. Every line needs evidence.

```
### Phase FP — Final polish (delivery-gate G10–G15 + refresh)
- [ ] FRESH get_timeline taken AFTER the last human edit (timestamp: ___)
- [ ] G10 content parity: every graphic string diffed vs CURRENT script (names/counts/order) — list checked files
- [ ] G11 face clearance: every overlay captured in every framing it spans; nothing over eyes/mouth
- [ ] G12 anchor freshness: every word-timed element re-verified against current cue frames (post-ripple)
- [ ] G13 chapter alignment: title spans cover spoken announcements; zero cue-over-card overlaps
- [ ] G14 junction tail: junction-tail-audit on the FINAL RENDER — PASS output pasted
- [ ] G15 exit flashes: every visual→face reveal has flash+click (list of junctions + evidence)
- [ ] Full G1–G9 re-run on the final render (Meta-rule: any repair invalidates prior passes)
- [ ] Checkpoint .palmier exported + scorecard + eval-log row
```

## Final Polish Pass additions (2026-07-30 v10, from the user's own edits)
- [ ] Entry sound design: entry clicks 0.5 / exit clicks 0.6 / tick riser 0.25 ~10f after fullscreen-graphic entries
- [ ] Music bed is ONE bounced file (no butt-join left in the timeline), bed ~0.056, 9f fade at tail
- [ ] Outro: captions end before logo; slowed 12f flash into logo; logo small (h≈0.295) + ~40f freeze (2×20f @0.1 speed, muted)
- [ ] Outro lockup: wordmark ABOVE tree (crop-split per overlays §7)
- [ ] Pacing audit run (pacing-audit.py): no intra-take pause >13f unless protected/intentional; junction audit re-run AFTER any ripple
- [ ] Head-tighten safety (overlays §8): ≥10f margin before RMS onsets, ASR word-start cross-check (fricatives read as silence — "Step" got chopped 2×), render-listen the first word of every rippled take head
- [ ] Captions: same height throughout, bottom third, covering nothing important (face/shirt logo/CTA button/card text) — common-sense check on every framing + every graphic/overlay/CTA beat; per-cue nudge only where coverage forces it
