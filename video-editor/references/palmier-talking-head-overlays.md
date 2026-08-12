# Enrich a vertical talking-head cut — b-roll, brand graphics, transitions, pacing (Palmier)

Take a finished vertical (1080×1920) captioned talking-head cut and turn it into a paced short:
split-screen b-roll with white-flash + whoosh transitions, floating stat cards over the face,
full-screen animated brand diagrams synced to the transcript, and zoom punch-ins on emphasis lines.
Built + hardened across THREE full production passes on the "intention engineering" video
(2026-07-05/06, ✅ live-verified on v0.6.1). v1 (floating cards) and v2 (everything-full-screen)
were rejected outright; v3's structure was right but shipped 10 polish defects the user itemized —
v4 below encodes all of them. Read §0 and the BRAND CONTRACT in §2 before touching anything.

> **STEP 0.5 — the editorial layer runs FIRST: [visual-story-design.md](visual-story-design.md).**
> Before authoring or placing anything, that reference produces the **visual beat sheet**
> (every transcript beat classified → treatment assigned → asset sourced), the **shot-request
> list for the user** (emitted at build START, not as an afterthought), the sourcing ladder
> (b-roll = evidence; real-data re-renders > screen recordings > recreations > diagrams;
> stock banned), and the coverage budgets (face majority, 2–4 major graphics per 30–60s,
> diagram read-time by element count, never-cover beats). THIS file is the mechanics that
> execute that plan.

## 0 · GATE — audit the base cut: mid-word cuts AND dead air (hard requirement)

**Never build overlays on an unverified cut.** the user caught clips "cut off mid-word" as a CRITICAL
error — and the audit found the video's very first word ("Your"), the thesis word ("Context"), and
a section-opening word ("Three") all clipped mid-word, plus 2-frame orphan sliver clips (one held an
audible speech blip) and a sentence left dangling ("…in the first month across—").

Method (energy + transcript + source ground truth):
1. Pin the source locally (`cp` off CloudStorage), extract mono 16 kHz wav.
2. RMS-scan every V-track clip boundary: speech energy (> floor+14 dB) within ±30 ms of an
   in/out point = mid-speech cut. Flag every clip with `durationFrames ≤ 4` (orphan slivers = edit
   artifacts; remove them, they are never intentional).
3. `get_transcript` (timeline) + `inspect_media` windows on the SOURCE around suspect in-points —
   the timeline transcript can't show words that were cut off; the source transcript can
   ("Context" 148.98–150.36s vs clip in-point at 149.90s = starts mid-word).
4. Semantic pass: a clip tail whose last transcript word leaves the sentence unfinished is a bad
   cut even when the audio energy is clean at the boundary.

Fix recipes (all preserve every word's absolute timeline position, so captions stay synced):
- **Tail borrow** — A's word tail clipped, B has head silence: `B.trimStartFrame += N`,
  `B.durationFrames -= N`, `move_clips B → +N`, then `A.durationFrames += N`. Shrink/move B FIRST
  (never extend A into B — overlap auto-trim corrupts B's head).
- **Net-zero swap** — A needs tail frames AND B opens with a pre-word blip: shave B's blip
  (`trimStartFrame += N`, `move B → +N`) and give the freed frames to A. No ripple.
- **Head capture via ripple** — B starts mid-word ("Context"): move every clip+caption ≥ boundary
  right by N (park-and-place, below), then `B.trimStartFrame -= N, durationFrames += N`. B's
  existing content lands exactly on the rippled captions.
- **Semantic dangle** — dangling word with no room to complete the phrase: keyframe the linked
  AUDIO clip's volume to 0 across the word (video keeps rolling) and cover the silent mouth-flap
  with a b-roll panel. Check the captions first — the captioner had usually already dropped the word.
- **Ripple mechanics** — `move_clips` is batched but rightward batch moves can transiently overlap →
  **park-and-place**: batch-move everything to +5000 first, then batch-move to final. Move captions
  in the same ripples (grab every caption clip id+frame from `get_timeline` once). Execute multiple
  boundary fixes RIGHT-TO-LEFT so earlier frame numbers stay valid.
- Re-run the energy audit + `get_transcript` after; the fresh transcript is the beat map for
  everything downstream.

**Tightness gates (v4 — a 1.2s head silence and a 1.1s dead gap each got a build rejected):**
1. **Hook immediately**: the first word must land within ~5 frames of frame 0. A head-capture
   ripple fix can leave lead-in silence — trim it back after.
2. **No dead air**: sweep the whole timeline for speech gaps ≥ 18f (0.6s) and tighten each to
   8–12f. Leave 15–17f pauses alone (natural beats — e.g. the pre-punchline pause before a
   zoom emphasis). "Cut out this empty time. This is video editing 101." — the user.
   **⚠ HOOK-ZONE EXCEPTION (the user 2026-07-12: "The first 10 seconds are BY FAR the most
   important part of the video — spend extra close attention to polishing them"):** in the
   first ~10s (300f) the 15–17f natural-beat exemption does NOT apply — run a dedicated
   stricter sweep (report ≥12f, cut ≥15f down to ~10–12f; the only pause that may keep ~16f
   is a deliberate full-stop beat between two hook sentences). A 15f pause I exempted as
   "natural" in the hook got flagged and hand-cut by the user. Same zone also gets a
   frame-stepped render review (probe the card, seams, and karaoke frame-by-frame) before
   sign-off.
3. Do the sweep with `ripple_delete_ranges {trackIndex: <baseTrack>, units: "frames"}` —
   verified semantics: it anchors on the given track, cuts the range across every sync-locked
   track (captions straddling a cut get head-trimmed — fine, their pre-roll just shrinks),
   shifts everything after, and **splits mid-clip cuts while REBASING keyframes flat on the
   right halves** (no zoom-replay bug — verified). Emptied tracks get pruned: track indices
   shift, re-read before the next index-based call.
4. Order ranges right-to-left; never leave a <4f sliver (if a gap straddles a clip boundary,
   align the cut start to the next clip's head). **Remove all replaceable overlays BEFORE
   rippling** — graphics that span a cut get sliced; panels/flashes/zoom-keyed clips that
   merely shift can stay.

## 1 · Rhythm (the accepted v3 structure + researched numbers)

Web research (creator-education consensus, 2025-26) that matched the user's notes — treat as defaults:
- **Face is the anchor**: return to the talking head every **3–7 s**; never leave a static face
  un-broken longer than ~3 s (that's what floats/zooms are for).
- **Cutaways 2–6 s**; graphic animates in **0.3–1.0 s** then **lingers 1.5–3.5 s** after the last
  element settles so the viewer can read it. A diagram that vanishes when its animation ends is a
  bug (the user flagged exactly this).
- **One surprise at a time**: one visual change + at most one SFX per beat. Never stack
  flash + zoom + slide on one cut.
- **White flash 2–4 frames, 1–3×/min, reserved for REAL footage entrances**; graphics get plain
  crossfades (7f opacity). SFX impact lands ON the cut frame, ~-10 dB under dialog (volume 0.3).
- **Zoom punch-ins**: 1.15–1.30×, instant (hold interp), on emphasis lines, max ~1 per 5–10 s,
  zoom back out before the next scene change.
- **the user's transition rule — BOTH DIRECTIONS (re-taught "for the fiftieth time" 2026-07-30)**: a
  transition must COMPLETE before the underlying take changes — no fade may straddle a base-cut
  frame (base cuts UNDER a fully-opaque fullscreen are fine, they're invisible). This binds
  ENTRIES as hard as exits: **a fullscreen must be at 100% opacity AT-OR-BEFORE the frame a new
  talking-head clip starts. Never fade a graphic in over the head of a fresh take** — the viewer
  sees a fraction-of-a-second face sliver, then the visual: rejected every time it shipped.
  Legal entries: (a) hard pop to 100% exactly ON the cut (the cut swallows it); (b) fade-in over
  the CONTINUING outgoing take, completing at the cut; (c) fade-in INVISIBLY under an outgoing
  opaque graphic/title that hard-ends at the cut (the dissolve pattern). Check every fade zone
  against the V1 cut list, entries and exits both.
- **Chapter beat structure (the pattern that finally passed, 2026-07-30):** flash + click ON the
  spoken chapter announcement → full-screen title frame alone (1.5–2.5s, flat opacity, entry
  covered by the flash) → title hard-ends WITH the chapter graphic already at 100% underneath
  (graphic fades in under the title) → graphic holds 3–5s → face. Never leave a face sliver
  between title and graphic, never stack two card-style visuals back-to-back, and never let a
  graphic play underneath a title card.

**Opening hook — the first 60 frames (researched 2026-07-06; a "slow zoom-out reveal" opening
was rejected as stale):**
- **Motion on the LITERAL frame 0.** An idle face warming up is a scroll-past; so is a gentle
  reveal. Editor consensus: the first second is motion / camera move / on-screen change, and a
  new visual or sound cue lands every ~3 s starting immediately.
- **Punch-IN is the talking-head hook direction, not zoom-out.** Zoom-out reveals are a
  context-reveal device (show where you are), not a face-hook. Standard recipe: open with a
  live push-in (~115→122% across the first phrase), **hard zoom-jump to ~125-130% ON the first
  key word**, release to 100% at the phrase end; later beats alternate ~115↔130% jump cuts.
  Ceiling ~130% on 1080 footage. Micro-impact variant: a 1-2 frame 105-110% jolt.
- **Text hook from frame 0**: 4-10 high-contrast words, up 2-3 s, near but not on the face.
  A float card's first row may ENTER AT FRAME 0 pre-empting its spoken cue — text leads voice.
- Palmier mechanics: animated zoom = linear-interp scale+position keyframe PAIRS
  (`[[0,1.15,1.15,"linear"],[N,1.22,1.22,"hold"]]` + matching position `-(s-1)/2`); zoom-jump =
  hold-interp pairs (existing punch recipe) with the jump keyframe ON the word's frame.
- **Approved implementation (2026-07-06, THIRD pass — v1 too timid, v2 nauseating):** exactly ONE
  camera move: quick punch-in `scale [[0,1.0,…,"linear"],[10,1.18,…,"hold"]]` (+ matching
  position), HOLD the punched framing for the whole first clip, and let the zoom release happen
  naturally ON the first base cut (the next clip is at default 1.0 — no release keyframe at all).
  Opening card FULLY VISIBLE ON FRAME 0 (opacity 1 at f0, 5f pop-settle from scale 1.12,
  `transform-origin: center` so nothing clips off-canvas).
- **Timidity is a rejection mode — and so is overcorrection.** v1's 6%-over-28f "push" was
  imperceptible ("some dumb slow zoom"); v2 stacked zoom-in + jump-in + jump-out inside 2s and
  was "making me nauseous… very unprofessional." The rules that survive all three passes:
  (a) quick zoom = 15-25% scale in ~10-15 frames, (b) **max ONE camera move in the opening
  seconds** — the every-≈3s cue cadence is fed by TEXT/graphics/cuts, not by more camera moves,
  (c) **mid-take zoom-OUT jumps read as edit errors** — punch-ins land mid-take, but releases
  happen ON a cut (or animate out at a phrase end, never pop), (d) frame-0 text hook means the
  text is ON frame 0. Verify by stepping f0 (card fully on screen), f5-12 (visibly tighter than
  f0), then confirm the framing does NOT change again until the first cut.

**Caption cue fill (the user 2026-07-06: "captions should fill this space — the caption goes
faster than the audio"):** ASR cue durations end at the last word's ASR end, which runs SHORT
of the real audio tail — the gaps read as captions outrunning the voice. After captioning (and
after any recut), butt-join the cues: extend every cue's `durationFrames` to the next cue's
`startFrame` (fill gaps >1f; karaoke word timing is unaffected — the settled line just holds).
Enumerating cues: `get_timeline` splits them between plain `mediaType:"text"` track clips AND a
row-capped `captionGroups` view — collect BOTH and dedup by id (101 cues showed as 87+14; the
group view alone silently hides most of them). Note the active-word POP SCALE of
`highlightPop` is NOT MCP-tunable (`perWordFrames` read-only, no scale param) — the pop
intensity knob exists only in the UI inspector.

**CAPTIONS: ONE LINE, ONE SIZE — for the WHOLE video (the user, HARD RULES 2026-07-29 + 2026-07-30).**
Two rules that interact:
1. *Never two lines* (07-29): a wrapped cue orphans a word onto line 2 and jumps the band height.
2. *Never mixed sizes* (07-30: "caption text must be the same size for the whole video" — per-cue
   downsizing got rejected as "caption text is changing size randomly"): the per-cue-shrink fix
   for wraps is BANNED. **Font size is ONE number for every cue, chosen so the LONGEST cue fits
   a single line.** Fit empirically (never char-count arithmetic): restyle the whole caption
   group (`update_text {captionGroupId, style:{fontSize}}` — one call restyles all cues and
   absorbs any per-cue overrides), then verify the longest cues' `transform.height` (single line
   ≈0.063–0.075; ≥0.10 = wrapped) and render-probe over an OPAQUE GRAPHIC (skin/shirt/logo in
   the band contaminates ink-detection). Tech-adoption build (2026-07-30): 46px cleared every
   cue including 23-char lines; the approved 54 standard applies only when no cue exceeds ~20
   chars. Also: `update_text` takes `style.outline` but reports it back as `border`; thick
   outlines swallow glyphs (keep ≈3 if used at all — Fractal standard is NO outline) and set
   `style.color` explicitly (default inactive fill is near-black).

**CHAPTER TITLE FRAMES — STANDARD PRACTICE, EVERY VIDEO (the user, 2026-07-30: "Whenever we go to
a new chapter, a new part, or a new phase, we should have a title frame that covers the whole
screen for just that specific title, just that heading, without all the other shit").**
- Every chapter/phase/step transition gets a FULL-SCREEN title card: brand bg + kick line
  (e.g. "STEP 1", teal mono ~46px) + the name (~118px, 800 weight) + a small teal underline
  bar. NOTHING else — no subs, no chips, no diagrams.
- Land it ON the spoken announcement (the "step one," frame from the transcript), hold
  ~1.2–2.5s. 4f fade-in; exit HARD if the end sits on a base cut (the cut swallows it),
  else 4f fade-out. Never straddle a base cut with a fade.
- **Hide the captions underneath (the user, same day): a caption that repeats the title card is
  redundant — remove the announcement cues** ("Step one, discovery.") that fall inside the
  title window; resume captions on the first content cue after it.
- Build: static PNG via Playwright → `ffmpeg -loop 1` → H.264 mp4 → place on the graphics track.

**IN-VIDEO TITLE BOX IS BANNED — THE BOX BELONGS ON THE THUMBNAIL (the user, 2026-07-30: "why are
you even including this box in the video at all? shouldnt you add the box on top of the
thumbnail image?").** The big mid-frame video-title box (the thumbnail-style card) never
appears in the video itself — it covers captions and reads as a stale thumbnail. It goes on
the exported THUMBNAIL image instead. **And before adding ANY frame-0 hook text, apply the
redundancy test (the user, 2026-07-30: "consider whether you need this text box at all"):**
on-screen hook text earns its place ONLY if it shows information the viewer can't get in the
first second otherwise. A caption-burned talking head whose captions land the hook line by
~f13 already communicates sound-off — an extra text box duplicates the captions, reads as a
second caption, and is CLUTTER. Default for this format: NO hook box; the hook is motion on
frame 0 (the punch-in) + face mid-sentence + captions. A hook card is for cold opens whose
first caption arrives late or doesn't state the contrarian point.

**THE 3-SECOND RULE IS ENFORCED, not aspirational (the user, 2026-07-30: "shouldn't we be changing
scenes every three seconds?").** After graphics placement, sweep V1 for face stretches with no
visual event (cut, graphic, title, punch) for >3s ≈ 90f. Standard fix: `split_clips` at a
phrase boundary from the transcript + a static 1.07 scale step on the alternating half
(`scale [[0,1.07,1.07,"hold"]]` + `position [[0,-0.035,-0.035,"hold"]]`) — a jump cut, not an
emphasis punch, so it doesn't count against the ≤2-punch budget.

Treatment picker per beat (their face fills the upper-center; captions burn at centerY 0.8):
| Treatment | When | Recipe |
|---|---|---|
| Plain face | hook, connective tissue, 2-4s breathers between graphics | nothing, or a zoom punch |
| **Float** (alpha ProRes over face) | one stat / two-line echo of the spoken words | full-canvas render, card in TOP zone (y≈100-430); baked entrance AND exit fades |
| **Split-screen** (b-roll top / face bottom) | real footage or an article-headline screenshot | `apply_layout top_bottom`, `anchorY:0.4` keeps their face; white flash + SFX on entry |
| **Full-screen brand diagram** | data moments, thesis lines, CTA | opaque render on brand bg (§2 contract), content **vertically centered filling the frame**, eyebrow ≥40px, 7f opacity crossfades |
| **Float over a panel** | stat that belongs to the b-roll beat | bake the card at the **exact canvas center** (straddles the panel/face seam, covers neither the b-roll subject nor their eyes) — NOT the panel's lower third (v3's centerY 0.77 landed on the b-roll subject and was rejected: "it's literally covering the b-roll. place it in the exact center") |

**Float content rules (v4):** ONE element per card. No sub-lines — a 32-33px muted subline is
unreadable at vertical-video size ("remove all the subtext that noone can even read"). If a
subline is load-bearing (the number means nothing without it), it's ≥40px solid white — else
delete it. If the spoken words already say it, delete it.

**Lists count 1→N TOP-DOWN. Always.** Even a "layer stack" metaphor never counts bottom-up
(no `flex-direction: column-reverse`, no 3-2-1 DOM order). Reveal order rides the spoken
enumeration, which now also runs top-down.

**Linger is decided BEFORE rendering** (floats bake their exit fades, so clip duration is a
render-time decision): budget = animation-settle + **≥45f (1.5s)** hold. When the beat is too
tight for that, use one of these (in preference order):
1. **Exit ON the cut** — hard end exactly at the base-cut frame; the cut swallows the pop-off.
2. **Flash-covered exit** — card holds to the cut, the white flash peaks there, no baked fade.
3. **Static across the cut** — card holds THROUGH a jump cut (stable overlay reads fine),
   then fades during the next take. The FADE still must never straddle a cut frame.
Never solve it by letting the card vanish when the animation stops — that is the rejected v3 bug.

**Long b-roll panels (canvas/app screen tours): CONTINUOUS motion + a jump-cut every ~3s
(the user 2026-07-11).** A camera path that stalls into a barely-perceptible slow zoom halfway
through the panel's life reads as "the visual just stops" and got rejected. Rules: (a) every
camera segment is a real scroll/pan for its whole duration — never park on a slow push;
(b) cut to a NEW region (or a second real artifact — e.g. the other workflow) every ~3s,
matching the things-change-every-3s pacing rule; (c) each jump-cut may also change zoom level.
Implement as a segment table in the HTML ({f0,f1,scale,cx[],cy[]} lerps) so every segment
scrolls edge-to-edge.

**Diagram CONCEPT accuracy beats visual polish (the user 2026-07-11: "the 'loop' diagram is not
a loop and it doesnt even make sense. the skills are part of the agent loop").** Two binding
rules from that rejection: (a) a graphic named/spoken as a LOOP must visibly loop — closed
ring, directional arrowheads, and a closing arc back to the first station; four boxes on an
invisible circle don't read as a loop. (b) Architecture relationships must be drawn where they
live: skills render INSIDE the agent-loop container (chips inside the bordered box), never as
a separate downstream chain item (`trigger → loop → skills` is wrong; `trigger → [LOOP: skills]`
is right). (c) **arrowheads must RENDER, not just exist in the source** — an SVG `marker-end`
(or any arrowhead shape) placed at a node's CENTER draws UNDERNEATH that node's box and is
invisible: flag #6's "loop" read as a plain teal oval because all four arrowheads were present
in `loop.html` yet buried under the node boxes. Terminate each arc at the destination box's
EDGE (walk `getPointAtLength` back from the center until the point exits the box, orient the
head along the tangent) so it sits just outside the box pointing IN — then CONFIRM the arrows on
the settled render; never treat "the marker is in the source" as "the arrow shows."
Sanity-check every diagram against the spoken mental model before rendering.

**Fullscreen graphics are CAPTION-SAFE only above y≈1400** (captions burn at centerY 0.8 =
y1536 center, band ≈1440–1640 on 1080×1920). A diagram whose content reaches into that band
gets covered by the captions (d-fixedpath shipped with steps at y1570 under "An agent runs a
loop." and was rejected). Keep ALL diagram content — labels, break text, list bottoms — above
y≈1400, and use the freed width: spread elements edge-to-edge instead of stacking a thin
column.

**Article-headline b-roll must MOVE and linger ≥3.5s** (a 2s static screenshot was rejected —
"static and doesnt show on screen long enough for anyone to understand"). Recipe: crop tight on
the headline block (keep the crop aspect = slot aspect, 1080×960 top slot → 1.125:1), bake a slow
push with ffmpeg — supersample 3× then
`zoompan=z='min(1+0.00095*on,1.12)':x='0':y='0.20*(ih-ih/zoom)':d=<frames>:s=1080x960:fps=30`
(`x='0'` pins the left edge so the headline never clips; drift the focal point only if the
headline doesn't hug an edge). To hold the panel past its base clip: clear any conflicting zoom
keys, `split_clips` the take at the panel's end, add the head segment to the bottom slot — the
panel-off then reads as an intentional reframe jump on a word boundary.

Aim splits + floats at existing radio-edit clip boundaries; a panel that spans a WHOLE base clip
needs zero splits (slow-mo stretch b-roll to fit: `speed = srcFrames/targetFrames` +
`durationFrames`). One `split_clips` cut for a mid-clip window is fine when the app is idle.
An opaque end-card clip may extend PAST the last base clip — the timeline lengthens to the
furthest clip, giving the CTA a held tail (~2s) without any base footage under it.

## 2 · Graphics: frame-stepped HTML → clip (`scripts/anim/`)

**BRAND CONTRACT (v4 — read social-canvas brand rules BEFORE authoring any video graphic; the
videos follow the SAME rules as the infographics — the user: "did you not look at the fractal ai
brand rules?"):**
- **Background** (every opaque fullscreen): `#09090b` + the 24px dot-grid (2×2px white squares,
  fill-opacity 0.14, `background-position: 12px 12px`) + a **subtle teal radial glow from the
  top** — `radial-gradient(circle at 50% 0%, rgba(0,198,162,0.16), transparent 52%)` layered
  over the grid. The glow is the "slight gradient" from fractalai.agency's own hero
  (`radial-gradient(circle at top, rgba(0,198,162,0.18), transparent 45%)`). Flat near-black
  with dots alone was rejected twice.
- **Danger/error/failure/cost-up = RED `#ef4444`. NEVER pink `#ec4899`.** Pink in the Fractal
  palette means human/emotion/creative. Six graphics shipped with pink ✕-marks/bars/≠ and got
  "you used some random pink color" — the palette's semantic table (in
  `social-canvas/references/fractal-ai-visual-style.md`) already had red for exactly this.
- Verdict/tag lines: ≥60px, `--text` (never muted grey); the key symbol may carry the red.
- **TITLE-SAFE ZONE — all graphic content within the central 82% horizontally (the user 2026-07-12,
  iPhone 15 Pro).** Tall phones (19.5:9) are TALLER than 9:16, so LinkedIn/TikTok/Reels
  fullscreen players COVER-fit the video and **crop ~9% off EACH side**. Captions (centered,
  narrow) survive, but fullscreen diagrams with content near the edges get sliced — a loop's
  side boxes vanished, a before/after's third chip ("CRM") was cut off entirely, a red verdict
  line lost its last word. Rule: **no graphic content (titles, eyebrows, boxes, chip rows,
  verdict lines, wide diagram elements) may sit outside x ∈ [97, 983] on the 1080 canvas** (9%
  margin each side). Cleanest implementation: wrap ALL foreground content in a
  `#safe{position:absolute;inset:0;transform:scale(0.82);transform-origin:center}` div while the
  brand bg stays on `body` (full-bleed) — the bg fills to the edges (no border) and only the
  content insets. **Verify EVERY fullscreen graphic by cropping its render to the central 82%**
  (`ffmpeg -vf "crop=886:1920:97:0"`) and reading the result — if any label/box/word is clipped,
  it fails. Panels (b-roll canvases) are exempt (cropping just shows slightly less texture);
  centered captions are exempt. This is a HARD requirement, same tier as the red-not-pink rule.

Same renderer as before (`render_anim.py`, `common.css`, `common.js` + `common2.css` patterns:
`.fs` centered fullscreen, `.float-zone`/`.frow` face floats, `.float-center` dead-center
panel floats). Key contract per graphic:
`TOTAL_FRAMES` (= timeline duration), `MOTION_RANGES` (holds get file-copied), `seek(f)` pure.
- **Time every internal cue to the post-fix transcript**: cue rel-frame = spokenFrame − placement
  start. Bars grow ON the number, slabs land ON "number two", the ≠ pops right before the punch word.
- Floats bake their own entrance + exit (whole-stage opacity); fullscreens leave fades to Palmier
  opacity keyframes (h264 has no alpha).
- Review one settled frame per graphic as a contact sheet BEFORE rendering the set; render in the
  background and **never touch Palmier while Playwright renders** (CPU contention wedges the bridge).

**PRE-RENDER DESIGN REVIEW (mandatory contact-sheet questions — every miss below shipped once
and got flagged; catching them here is free, catching them in the user's review costs a full
re-render + re-place):** for each graphic's settled frame ask:
1. **Concept**: does the visual literally match the spoken mental model? (A "loop" must loop;
   parts spoken as *inside* something render inside it.) Say the narration line out loud against
   the frame.
2. **Fill**: does content use the full caption-safe canvas (width AND height), or is it a thin
   column floating in dark space? Spread edge-to-edge.
3. **Caption clearance**: is every pixel of content above y≈1400? Check the LOWEST element
   (break labels, list bottoms), not the boxes.
4. **Motion**: does anything animated keep moving for its whole clip life (panels), and does
   every animated element have somewhere to settle ≥45f before exit (or an exit hatch)?
5. **Brand**: teal glow + dot grid bg, red (never pink) for danger, lists 1→N top-down,
   no sub-40px text.

## 3 · Transitions & SFX (verified recipes)

- **White flash**: 6f clip at `cut−2` on the graphics track, opacity keys
  `[[0,0],[2,1],[3,1],[6,0]]` — peak sits on the cut.
  ⚠️ **Two corrections to the original recipe, both later production learnings — read before using:**
  (1) the flash source must be an **opaque H.264 VIDEO clip, not an image clip** (image clips are
  banned for flashes per the build checklist — they did not render reliably); (2) this recipe was
  written around `create_matte {hex:"#FFFFFF"}`, which is **absent from the tool manifest observed
  2026-07-29**. Generate a 6-frame solid-white MP4 with ffmpeg and `import_media` it instead, and
  confirm against the live manifest before assuming `create_matte` exists.
- **Adjacent fullscreens CROSS-fade — never fade the outgoing to transparent (the user, 2026-07-06):**
  when two graphic scenes touch with no face beat between them, fading the first one out shows
  the face through the gap for ~14f ("fade them into each other rather than fade the first one
  to transparent"). Recipe: put the INCOMING clip on a new top track (`add_clips` omitting
  trackIndex), keep its 7f fade-in, and hold the OUTGOING fully opaque underneath through the
  overlap — kill its fade-out keys and create the overlap by slow-stretching it
  (`set_clip_properties {speed: src/target, durationFrames: target}`, ≤3% so internal cues drift
  only a few frames). ⚠️ `add_clips` validates `durationFrames` against the SOURCE length —
  add at source length first, then stretch via `set_clip_properties` (speed + duration together).
- **A graphic whose end sits ON a base cut exits HARD — never add a fade-out there (relearned
  2026-07-30 the expensive way: six 7f fade-outs added "for polish" all ended exactly on base
  cuts and got rejected as broken transitions).** The fade-out treatment is ONLY for exits that
  land mid-take. Before adding any exit fade, check the graphic's end frame against the V1 cut
  list: on a cut → hard end; mid-take → 7f fade (4f for quick title stingers).
- **Re-check exit-on-cut seams after ANY manual edit pass:** a graphic exit designed to land ON a
  base cut reopens a face-flash if the cut gets nudged (their +3f nudge turned a clean hard-out
  into 3 frames of face) — re-read the cut frames and stretch each exiting graphic to the new
  cut before calling it done.
- **Transition SFX — SHORT and SUBTLE** (the 1.8s Mixkit-1490 whoosh at vol 0.3 was rejected as
  "way too intense" — retired). Verified quiet picks, both from Mixkit previews
  (`assets.mixkit.co/active_storage/sfx/<id>/<id>-preview.mp3`):
  | SFX | id | dur | transient | place at | volume |
  |---|---|---|---|---|---|
  | subtle whoosh | 1485 | 0.48s | file f3 | `cut−3` | 0.22 |
  | soft click | 1133 | 0.35s | file f5 | `cut−5` | 0.6 |
  ⚠️ **HEAD-TRIM the SFX before placing — never do transient-offset math (the user, 2026-07-30:
  "You didn't align the click sound with the white flash… Do not ever make this mistake
  again").** The cut−N placement puts the clip's visible left edge BEFORE the cut, so the
  timeline LOOKS misaligned even when the audio lands right — and any error in the offset is
  invisible. Instead: `ffmpeg -af "atrim=start=<attack>,asetpts=PTS-STARTPTS"` the SFX so its
  transient is at the FILE HEAD (click-1133 attack starts at 0.1944s → trim at 0.185), import
  that (e.g. `click-tight.wav`), and place the clip start EXACTLY ON the cut frame. Clip edge
  == audio hit == flash peak, verifiable at a glance in the UI.
  Locate any candidate's transient by per-frame RMS peak, and profile candidates before picking
  (peak dB + attack frames — pick short attack, low peak). **the user's standing pick (2026-07-06,
  after an in-video A/B): the soft CLICK on every b-roll transition — "to keep it simple, lets
  stick with the click." Default to it; whooshes only if they ask.** The A/B pattern (different
  variants on different cuts in one build) is the way to offer a new sound.
  One shared audio track via one `add_clips` (omit trackIndex).
- **Background music (standing setup, 2026-07-06):** the user's bg-music library lives at
  `'~/Library/CloudStorage/GoogleDrive-<YOUR_GOOGLE_ACCOUNT>/My Drive/Business   Career/Entrepreneurship/Fractal AI Agency/marketing/audio/bg-music'`
  (note the triple-space in "Business   Career") — currently ONE track ("Sakura Trees", ~100s)
  reused across videos. Recipe: `cp` it off CloudStorage first (materialize before import), then
  **pre-process with ffmpeg before import** — a gentle low-pass keeps the music out of the
  speech band: `-af "lowpass=f=6500"`. One clip spanning the whole timeline (loop only if the
  video outruns it), on its own audio track. **FLAT `set_clip_properties volume` — NO volume
  keyframes** (fade/duck keys on the music got rejected hard: "you fucked up the volume by
  adding a bunch of pointless keyframes. just keep the volume low at the same db for the whole
  video"). **Level: −25 dB fader = `volume 0.056` — THE STANDARD (the user 2026-07-11: "lower
  volume of bg music to -25. that should be the standard from now on." Supersedes the earlier
  −22 dB/0.079 pick).** Calibration lesson:
  the RMS-matched calc (music ~19 dB under dialog RMS → 0.012) landed 16 dB QUIETER than their
  pick — raw dialog RMS understates perceived speech loudness, so treat measurement as a floor
  for a first pass and let their ears set the number; record each new track's approved fader dB
  here when they tunes it.
  interp: `scale [[0,1,1],[in,s,s],[out,1,1]]` + `position [[0,0,0],[in,−(s−1)/2,−(s−1)/2],[out,0,0]]`.
  Verified NO blowup on full-frame video (the v0.6.1 blowup bug is images-with-transform-box only).
  Always set BOTH tracks — scale without its position offset renders anchored top-left.
- **Punch EDGE-BUFFER rule (the user, 2026-07-06 — three of four punches violated it):** a punch-in
  never fires right after the viewer's scene changes, and never releases right before it changes
  again. Concretely: (a) zoom IN ≥ ~30f (1s) after the face becomes VISIBLE — count from the
  viewer-visible reveal (a cut, a panel-off reframe, or an opaque graphic clearing), not the
  clip's technical start; the punch highlights a stress word MID-take. (b) zoom OUT either
  ≥ ~30f before the next visible change, or don't key a release at all — **hold the punch to the
  clip end and let it release invisibly under the next opaque fullscreen or ON the cut itself**
  (dropping the release keyframe is the cleanest fix when a graphic covers the tail).
  (c) The video's frame-0 opening punch-in is the ONE deliberate exception (there is no prior
  scene — motion on frame 0 is the hook doctrine).
  (d) **Legibility beats compliance — when in doubt, DELETE the punch (the user, 2026-07-06):** a
  punch that satisfies (a)-(b) can still read as "zooming in and out randomly" if the viewer
  can't attribute it to a beat. A punch is intentional only when it lands ON a clearly stressed
  word AND its release sits on a phrase boundary, cut, or graphic — a release on some mid-
  sentence word ("already") reads as an error. Special case: a take that just returned from a
  fullscreen graphic usually gets NO punch at all — the scene-return IS that beat's visual
  event; punch only if the line is a major thesis moment. Fewer intentional zooms always beat
  more rule-compliant ones.
  (e) **Default budget: ≤2 punches per short — the frame-0 opening hook + ONE thesis-word
  punch (the user 2026-07-11: four rule-compliant punches still read as "totally random rather
  than intentionally trying to emphasize something").** Rule-compliance doesn't make a punch
  legible; scarcity does. Pick the single strongest thesis line for the second punch and
  delete the rest.
- **Animated zoom (linear interp) ✅ — and the OPENING HOOK rule**: the same scale+position pair
  with `"linear"` on the first keyframe animates smoothly. **The video must OPEN with motion** —
  a static face at frame 0 got rejected as "stale, doesn't have enough visual hook" even with the
  first word landing at frame 4. Verified opening reveal: fast zoom-out on the first base clip,
  `scale [[0,1.35,1.35,"linear"],[16,1,1,"hold"]]` + `position [[0,-0.175,-0.175,"linear"],[16,0,0,"hold"]]`
  (~0.5 s, settles right as the first caption lands). Captions live on their own track so they
  stay fixed while the footage moves — correct look.

## 4 · SAVE DISCIPLINE (the hardest-won lesson — data loss happened twice)

- **Palmier autosaves on a timer only. Quitting does NOT flush recent edits. There is no in-place
  MCP save tool** (re-checked the live 49-tool manifest 2026-07-06). A wedge/crash/reopen rolls the
  project back to the last autosave — one rollback ate a whole placement pass (fixes survived only
  because they'd sat idle long enough to autosave).
- **DEFAULT checkpoint = `export_project {mode:"palmier"}` — NEVER computer-use while the user may
  be at the machine.** Computer-use Cmd+S steals app focus and keystrokes from whatever they's
  doing (`open_application` yanks PalmierPro to the front). He shut it down hard 2026-07-06:
  "Stop running computer use. Just use the app. I need to use my computer." Cmd+S-via-computer-use
  is a last resort ONLY when the user has explicitly OK'd driving the UI in that session; otherwise
  every checkpoint is the MCP export (below). If a checkpoint verify is needed, use the export's
  returned `status:"exported"` + `ls` the output path — not app-focus tricks.
- **MCP-only checkpoint = `export_project {mode:"palmier", outputPath:".../backups/<name>.palmier"}`**
  ✅ — snapshots the live editor state (all timelines) to a self-contained package; recovery =
  `open_project {path}`. Returns in ~0.1s; caveat: self-contained means it embeds ALL project media
  (~1.7 GB for a 4-min-source project), so it's the before-risky-phase / no-computer-use fallback,
  not an every-five-minutes habit. Point outputPath at a gitignored/backups dir.
- **NEVER author graphic sources in the scratchpad — it gets cleaned between sessions.**
  (Bit 2026-07-12: had to reconstruct 3 diagrams' HTML from conversation context to re-margin
  them; `render_anim.py` survived in the skill dir but `common.css`/`common.js`/`logo.png`/the
  `.html` files were gone.) The `.palmier` checkpoints embed the RENDERED media only, not the
  source. **Author `gfx/` directly in the piece's project folder**
  (`projects/<brand>-content/<YYYY-MM-DD>-<slug>/gfx/` — HTMLs + common.css/js + data files +
  logo), where it is git-tracked and durable, so a future margin/label/timing fix re-renders from
  real source instead of a reconstruction. **The old "copy `gfx/` to `<slug>-assets/` on Drive"
  step is RETIRED** — it existed only to survive the scratchpad being wiped, and authoring in the
  project folder removes the need for a parallel copy. Reconstruct-from-context works
  (self-contained HTML with inlined brand vars + JS helpers + the documented bg recipe) but risks
  font/color drift.
- **The bridge wedges under sustained call volume** (connection-reset on localhost, app process
  still alive): pace scripted calls ~0.5–1 s apart; on reset, retry with backoff; if `initialize`
  itself resets, `osascript quit` + `open -a PalmierPro` + `open_project {id}` (app reopens to the
  launcher — "Editor not available" means call `open_project` first).
- **After any reload, re-verify EVERYTHING you assumed**: timeline state (totalFrames), and the
  media library — a rollback resurrects deleted same-name assets whose files are gone; a name-based
  lookup then grabs the stale one (symptom: "durationFrames exceed the source length"). Distinguish
  by duration; purge + re-import.
- **Keep every mutation phase in a re-runnable script** (drive the bridge over HTTP for bulk work).
  Recovery from a rollback is then mechanical: re-run, checkpoint, verify.

## 4b · Cleaning up after the user's own UI edits (revision passes)

the user edits in the Palmier UI between passes — plan for it. Verified recipe (2026-07-11):
- **A UI delete of a pause is usually NON-ripple**: it leaves a cross-track HOLE (base video +
  music + linked dialog all show the same `gaps:[[a,b]]`; captions/graphics after it don't move).
  Fix = ONE call: `ripple_delete_ranges {trackIndex:<baseTrack>, ranges:[[a,b]], units:"frames"}`
  — it closes the hole across every sync-locked track (captions, graphics, flashes, SFX all
  shift together; the delta reports per-track shift counts). Check first that nothing SPANS the
  hole (a spanning clip gets sliced); caption cue-fill means the cue before the hole ends AT the
  hole start, so the butt-join survives the shift.
- **Music bed after the close**: the downstream music clip keeps its old trim → source skip at
  the join. Remove both halves and re-add ONE clip over the new full length, re-set volume.
- **A UI tail-trim can strand keyframes**: a punch whose keyframe sat past the new clip end
  simply disappears from the returned keyframes — re-read `get_timeline` and re-derive the punch
  list rather than trusting the pre-edit map.
- **"Captions seem off" after a dead-air complaint is usually the SAME bug**: cue-fill
  butt-joins stretch a cue across the uncut silence, so the last word's highlight sits frozen
  while the audio is dead — the karaoke isn't desynced, the dead air is. Cut the gap and the
  cue shortens back onto the voice. Verify with the energy sweep + render probes, don't chase
  caption timings first (2026-07-12).
- **Dead-air fixes on a graphics-laden timeline**: cut ranges that land INSIDE a long b-roll
  panel split it (visible stutter in a continuous scroll) — after the ripples, replace the
  panel pieces with ONE fresh clip over the shortened window (trim the render's tail). Mid-cue
  caption splits + music fragments: see palmier-pro.md v0.6.5 delta (duplicate-cue merge +
  karaoke clear-and-restore repair; enumerate music fragments fresh).
- After ANY revision pass, re-run the affected verify-gate items (esp. exit-on-cut seams — their
  nudges move cuts) and re-checkpoint before + after your own surgery
  (`export_project {mode:"palmier"} → backups/<slug>-pre-revisionN.palmier`).

## 5 · Verify gate (before telling the user it's done)

**v0.6.5+: `inspect_timeline` is BROKEN for this (always renders frame 0)** — run the visual
checks on an actual export instead: render to a local file, then extract one frame per
checkpoint beat (`ffmpeg -vf "select=eq(n\,F)" -frames:v 1`) — gap seams, each graphic settled
mid-linger, caption-overlap suspects, punch takes, the thumbnail frame — and READ the frames.

From the rendered samples: (1) every graphic fully built at a mid-beat frame AND still on
screen ≥1.5 s after its last element settles, (2) splits show b-roll top / face-framed bottom with
captions intact, (3) panel floats sit at the exact canvas center covering neither the b-roll
subject nor their eye-line; face floats in the top zone, (4) no fade straddles a base cut, (5) 2–4 s
of plain face between consecutive graphics, (6) zooms present on the emphasis lines and released
before the next scene change, (7) **first word ≤5f from frame 0, and the §0 gap sweep reports no
speech gap >0.6 s**, (8) every enumerated list counts 1→N top-down, (9) danger elements are red
`#ef4444` (grep the HTMLs for `ec4899`/pink — zero hits on semantic-danger elements), (10) every
fullscreen bg carries the teal glow + dot grid, (11) the headline panel is moving (zoompan) and
readable ≥3.5 s, (12) **captions fill**: no inter-cue gap >1f anywhere speech continues (cues
butt-joined — a cue ending before its audio tail reads as "captions faster than the audio"),
(13) **caption style verified per-clip**: every text clip's `textAnimation.preset` matches the
approved style (`highlightBlock`) in a fresh `get_timeline` read — bulk clip ops can silently
revert it, (14) zoom punches respect the edge buffer (in ≥1s after the visible reveal, out ≥1s
before the next change or invisibly under a graphic/cut), (15) **no face-flash at any
graphic→graphic seam** — inspect every boundary ±5f (adjacent fullscreens must cross-fade), and
every exit-on-cut still lands exactly on its (possibly nudged) cut. Re-run the §0 energy audit if any
trims changed. Then **checkpoint via `export_project {mode:"palmier"}`** (computer-use Cmd+S
only with the user's explicit session OK), and leave the export for the user's call.

**Final export (on the user's word):** destination convention = Drive
`…/Fractal AI Agency/marketing/video/<slug>-final.mp4` (finished videos sit FLAT in that folder,
kebab-case with `-final`; source material lives in `<slug>-assets/` beside them). The
**thumbnail goes to a SEPARATE folder**: `…/marketing/images/thumbnails/<slug>-thumbnail.png`
(NOT the video folder — the user 2026-07-12).
`export_project {mode:"video", codec:"H.264", resolution:"Match Timeline"}` returns
`status:"started"` immediately and renders in the BACKGROUND — render to a LOCAL path first,
poll the file until size is stable, `ffprobe`-verify (dimensions, nb_frames, audio stream),
then `cp` to Drive and `cmp` the copy. A ~97s 1080×1920 timeline rendered in ~2 min / ~106 MB.
(The bridge client's 120s HTTP timeout doesn't matter for video mode since the call returns
instantly — but call it with a long timeout anyway in case that changes.)

**ALWAYS deliver a THUMBNAIL still alongside the final video (the user 2026-07-11: "you should
always export an image at the right time").** Pick the strongest hook moment — opening title
card fully settled + the hook line's key caption word highlighted (e.g. the frame where the
strikethrough/reveal card and "officially obsolete." are both on screen) — and extract it
full-res from the FINAL RENDER (not inspect_timeline):
`ffmpeg -i final.mp4 -vf "select=eq(n\,<frame>)" -frames:v 1 <slug>-thumbnail.png`.
**Deliver to the THUMBNAILS folder, NOT the video folder (the user 2026-07-12):**
`…/Fractal AI Agency/marketing/images/thumbnails/<slug>-thumbnail.png`. The finished video goes
to `…/marketing/video/<slug>-final.mp4`; the thumbnail lives separately under
`marketing/images/thumbnails/`. Keep them split.

## 6 · 2026-07-30 rulings (tech-adoption v8) — BINDING

**Overlays NEVER cover eyes or mouth.** the user, verbatim intent: "you shouldn't have
overlays covering up my eyes and mouth." Chest zone floats start ~y1020 (their manual
placement, centerY 0.629 on a y770-baked render = +248px). Check EVERY framing the
overlay spans — 1.07 jump-cut takes sit the face lower; a row that clears the chin in
one take covers the mouth in the next (the versus card needed y850→y1030).

**List/question floats carry a context heading.** Small mono teal eyebrow above the
stack ("ASK THESE 3 QUESTIONS") — a bare list floating on the shirt lacks context.

**Diagram data is TRANSCRIBED from the current script/source doc at build time and
diffed line-by-line — never from memory, never from a previous diagram.** Three
sequencing/naming flags in one session, all from building off the retired 4-phase
construction diagram: gates rendered BEFORE the phase they judge (a gate always comes
AFTER its phase: eval report→GATE 1, plan greenlight→GATE 2 during pilot, pilot
report→FINAL GATE); "IMPLEMENTATION" instead of the script's 5 phases (it splits into
ROLL OUT + ADOPTION); "PILOTING" instead of the script's "PILOT". Station data lives in
ONE shared gwdata.js; the overview header must state the true counts ("5 phases · 3
go/no-go gates" — never contradict the spoken "5-step playbook").

**Chapter title cards enter when the announcement STARTS being spoken** ("step
five…" — the word "step", or the take cut carrying it), span cut-to-cut where cuts
exist, and NO caption cue may overlap a title card — trim the previous cue to end at
the title start ("begin" bleeding under "STEP 5" was the flag) and end the card before
the next cue. Flash (2f before) + head-trimmed click move WITH the title entry.

**Emoji flair 1–3× per video.** Big system emoji (~230px), alpha ProRes pop
(overshoot scale + settle wiggle), chest zone, on an emphasis word (💀 on "dies",
🏆 on "recognize your champion"). Hard out on a cut; fade only mid-take.

**Render-side junction-tail audit is part of the polish pass.** ASR gives word STARTS
only — a word's tail truncating into a cut is invisible to transcript-based audits and
audible to the user ("workflow" chopped at f2401). Measure the RENDER: for every base cut,
RMS of the last 2 frames vs the 4 frames after; pre>0.025 && post<0.012 = truncated
decay → extend the outgoing take into the incoming clip's pre-speech silence
(non-ripple: butt-continue the same take via add_clips source-seconds, verify the next
clip's in-point advanced). Script pattern: build/junction-tail-audit.py in the
tech-adoption project.

**Live co-editing protocol (the user in the app while the agent edits — THE collision
session).** (a) Palmier has ONE shared undo stack: their Cmd+Z pops YOUR most recent ops
silently — re-verify your recent clips exist before building on them. (b) He adds
tracks mid-flight (flash tracks): EVERY indexed add_clips re-reads get_timeline
seconds before, or lands on the wrong track — one stale index put 4 clips on the
CAPTIONS track and deleted 19 cues (delta showed a captionGroup + removedClipIds →
`undo` IMMEDIATELY restores; the delta is the tripwire, read it every time).
(c) His UI edits between your reads are ground truth — take positions/trims from a
fresh read, never re-assert your cached plan over their moves. (d) Checkpoint
(`export_project {mode:"palmier"}`) after each verified batch.

## §7 · 2026-07-30 rulings round 2 (tech-adoption v10) — measured from the user's own polish edits, BINDING

These were measured by diffing their live edits against the v9c checkpoint. Apply them
as defaults on every future build/polish pass.

- **Transition sound design (their final mix):** exit click (visual→face) stays vol 0.6
  ON the cut; **entry clicks are quieter — vol 0.5** at the title/graphic entry frame;
  **fullscreen graphic/reel entries ALSO get a short "tick" riser (0.2s) at vol 0.25,
  ~10f after entry** (their placements: entry+11, +11, +12, +5). Flash template
  unchanged: 6f clip, opacity keys [[0,0],[2,1],[3,1],[6,0]], start ≈ cut−3 so the
  peak lands on the cut.
- **Music bed: bounce the splice to ONE file.** He replaced the two-copy butt-join
  with a single bounced asset (`bg-sakura-splice-v3`), volume 0.056, `fadeOutFrames`
  9 at the very end. When a music edit is stable, render it to one file and re-import —
  one clip, no join to maintain.
- **Outro redesign (their pattern, keep for future Fractal videos):** captions END
  before the logo (no cue overlaps the outro). Entry into the logo uses a SLOWED
  flash — white-flash clip at speed 0.25, 12f, opacity [[0,0],[2,1],[8,1],[12,0]] —
  gentler than the 6f body flash. Logo animation plays small (transform height ~0.295,
  centered) with its own audio, then FREEZES ~40f: two 20f copies of the last ~2
  source frames at speed 0.1, audio vol 0 (0.1 is the floor speed; 2 src frames ×0.1
  = 20f max per clip, hence two). Music fades out over the freeze.
- **The logo-animation lockup is NEVER rearranged (corrected 2026-07-31).** "Move the
  text up above the fractal logo" meant the CAPTIONS above their SHIRT's tree — EA
  misread it as the outro and crop-split the brand animation (reverted on their flag:
  "make sure it's back to how I had it"). The outro plays the logo-animation asset
  exactly as authored: tree mark top, FRACTAL AI typing below. (The crop-split
  technique itself is documented above under position semantics — valid tool, wrong
  target.)
- **Palmier position semantics (measured, non-obvious):** crop insets mask IN PLACE
  (no reframe), but the moment a clip has a `position` keyframe its anchor switches to
  ABSOLUTE top-left: y × frameHeight = the clip box's top edge (x likewise). A
  letterboxed clip's "natural" y is (1−transformHeight)/2, NOT 0 — compute from that
  or the clip jumps to the top. Also: the black background of an opaque source stays
  opaque after cropping — crop BOTH edges down to the exact band you want visible, or
  the kept black covers layers below.
- **Pacing: their taste is TIGHT.** In their own pass they re-cut mid-video takes to 40–70f
  and asked for more ("tighten up the cuts so it goes faster paced"). Default polish:
  map the source speech through every base clip's trims, find intra-take pauses
  >13f (0.43s), ripple-delete down to ~9f (0.3s), keeping ≥4f decay pad in front,
  ≥6f clearance from cuts/flashes, and never through overlay pop-in zones, emoji, or
  caption-critical beats. Script: build/pacing-audit.py (tech-adoption).

- **Captions sit ABOVE the shirt logo (the user, 2026-07-31).** On this wardrobe the tee's
  fractal tree reads as part of the frame — the caption block must clear it on NORMAL
  framings (punch-ins exempt, their call). Tech-adoption final: captions centerY 0.8 →
  0.771 (−55px; their ask was "~30px", the extra clears lean-in takes). And the earlier
  misread is the lesson: when the user says "the text" with a logo on screen AND on their
  shirt, CONFIRM which surface they means before building — the captions are the likelier
  referent.

## §8 · 2026-07-31 caption + pacing rulings (tech-adoption v13/v14 fail-set) — BINDING

- **RMS floor tests are DEAF to fricative onsets — never trim a take head up to a
  measured "silence" boundary.** The pacing audit's floor (0.011 on raw speech) read
  the /s/ of "Step four" and "Step five" as silence, and the head-tighten ripples ate
  the word "Step" — twice, caught by the user, fixed by them in the UI. Words opening with
  s/f/sh/h/th sit at or below noise floor for their first ~3-6 frames. Rules: (a)
  head-silence deletions keep ≥10f (not 3-4f) between the delete end and the
  RMS-detected onset; (b) cross-check every head-tighten against the ASR word START
  from get_transcript — if the ASR start is EARLIER than the RMS onset, trust the ASR;
  (c) after ANY ripple that touches a take head, render-verify the first word of that
  take audibly intact (chapter announcements "Step N" are the highest-blast-radius
  case — a chopped announcement breaks the video's spine).
- **Caption placement is COMMON SENSE, not a canonical number (the user, 2026-07-31).**
  His general rule, near-verbatim: captions all at the same height throughout the
  video, always in the bottom third, and they must never cover anything important
  (their face, the shirt logo, a CTA button, a card's text). Pick the one height that
  satisfies that across the whole video — snug above whatever it must clear in the
  worst framing, not maximally high. A caption covering something important is by
  definition in the wrong place; no rule lookup needed. Per-cue nudges are fine
  exactly where coverage forces them.
- **After ANY caption-height change, sweep EVERY fullscreen graphic + overlay beat for
  collisions at the new height** — the two that bit: "these questions," landed ON the
  question-cards overlay (fixed by end-trimming the overlay to exit before the cue),
  and the CTA block cues landed ON the ADOPT button (the user fixed by moving the CTA
  cues DOWN — the ONE sanctioned uniformity exception: over the CTA screen, cues may
  take a different height to keep the button clear — a per-cue nudge is what
  "cover nothing important" requires there).
  Sweep list: every full-screen card/reel span, CTA screen, overlay card spans, emoji.
- **His fix pattern is per-cue `update_text` transform overrides** (clipIds +
  transform.centerY) — per-cue transforms override the group default and survive group
  restyles. When replicating a "move these captions" ask, match scope to their: group
  transform for global, per-cue for exceptions.
