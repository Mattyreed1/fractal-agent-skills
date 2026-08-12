# Visual story design — the editorial layer (plan the visuals BEFORE you cut)

The front-end of every talking-head build: read the script/transcript, classify every beat,
assign each one a visual treatment, and source the assets — **before authoring a single
graphic or placing a single clip**. This is the layer that decides *what* the viewer sees;
[palmier-talking-head-overlays.md](palmier-talking-head-overlays.md) decides *how* it's built.
Skipping this stage is why edits feel improvised: treatments picked at placement time optimize
each beat in isolation and miss the story-level cadence.

Sources: 4 production passes (2026-07) + creator-education/editor research (2026-07-12 —
Paddy Bird's anchor-point framework, OpusClip's 13.5M-clip TikTok study, Captions/522
Productions on authenticity, Hormozi/Abdaal-editor breakdowns, motion-design consensus).

## 0 · When it runs + what it outputs

Two passes, two deliverables:

1. **Script-time (BEFORE or at recording):** produce the **shot-request list for the user** (§3).
   Footage only they can capture needs lead time — handing them the list after the edit is built
   (the n8n-to-cc mistake) means their shots miss the video. If the script exists before shoot
   day, this list rides along with it.
2. **Transcript-time (after the radio edit):** produce the **visual beat sheet** (§1) + the
   **asset map** (what to pull/render/request per beat). Graphics are authored FROM this sheet;
   the placement pass executes it; the verify gate checks against it.

## 1 · The visual beat sheet (the paper edit)

Go through the transcript line by line and label every beat with its JOB, then assign the
treatment from the table. One row per beat: `[frames] [spoken line] [job] [treatment] [asset]
[interrupt? y/n]`. Professional editors for Hormozi/Abdaal-style channels all work this way —
beats classified by narrative function + energy, treatments assigned on paper, THEN the NLE.

| Beat job | How to spot it | Treatment | Why |
|---|---|---|---|
| **Hook** (first ~5-10s) | The opening claim | **THE ARTIFACT THE CLAIM IS ABOUT — not the face.** Frame-0 text hook over it; face enters after. | ⚠️ **This row said "FACE … never cover" until 2026-08-11 and it was WRONG** — it produced an 11.8s face-only open the user rejected. Frame-verified teardown of 8 outperforming AI-automation Shorts: **the face never owns the frame past 2.7s in 8/8, 3/8 show no face at all in the first 5s, and the real artifact is on screen by 0:05 in 8/8.** See §1b. |
| **Identity/credibility** | "who I am / why listen" lines | FACE, plain | Trust is built by eye contact; covering it reads as hiding. |
| **Show-the-thing** | The sentence names a visible artifact ("my notetaker was 22 steps", "the dashboard") | Split-screen panel with the REAL artifact (§2) | Proof beats illustration. Keyword-timed: panel lands ON the noun. |
| **Explain-the-concept** | Abstract relationship or framework (loop, trigger+skill, one fixed path) | Full-screen brand diagram | The concept IS the beat — viewer should "stop listening and start decoding." Diagram must be isomorphic to the spoken mental model (a loop visibly loops; parts spoken as inside render inside). |
| **Number/stat** | A count, price, delta | Float card echoing JUST the number | One element; the voice carries the nuance. |
| **Example/case** | "for example…", a mini-story with objects | B-roll burst (1–3s) or split-screen, keyword-timed | Descriptive lines are the safest b-roll real estate. |
| **Punchline/twist** | The line itself is the surprise; jokes; "aha" | FACE — always | The micro-expression sells the beat; b-roll here competes with the punchline (Bird: "do you want them to understand or to FEEL?"). |
| **Emotional beat** | Confession, pain point ("debugging at 11 p.m."), triumph | FACE on the line itself; mood b-roll may bracket it (just before/after), never during | The feeling lives in the face. |
| **Transition** | "So why is this better?", section turns | Cut/reframe/graphic-off — the scene change IS the visual event | Don't stack another interrupt on it. |
| **Connective tissue** | Setup sentences, breathing room | FACE, plain | Cadence comes from cuts + captions here. Clean frames give processing time — they make the decorated beats read as intentional. |
| **CTA** | The ask ("Comment KIT") | Full-screen brand card OR face + keyword text; never unrelated b-roll | Completion/CTR hinge on the ask feeling direct and human; visual noise at the CTA spikes swipe-aways. |

**Binding rules on top of the table:**
- **One idea, one visual.** Each beat gets at most ONE treatment; never stack card + zoom +
  panel on the same line.
- **The never-cover list** (face stays fully visible): credibility lines, emotional peaks,
  punchlines, the CTA sentence. If a visual must touch one, it's a sub-2s echo or an overlay that
  keeps the face on screen — never full cover. **The HOOK LINE was removed from this list on
  2026-08-11** — it was the first entry and it was the defect: the opening is exactly where the
  artifact belongs and the face does not.
- **Keyword timing.** Every panel/card/diagram element lands ON the word that names it
  (cue-frame from `get_transcript`). B-roll that drifts off its keyword reads as filler.
- **A beat with no strong treatment stays plain.** Forced coverage is the amateur tell;
  in OpusClip's 13.5M-clip TikTok sample only ~6% of clips used b-roll at all — b-roll is a
  scalpel, not a baseline.

## 1b · The hook visual — SUBJECT ALIGNMENT, then the boring-artifact problem

**The opening image asserts authorship.** Whatever plays under "I built X" tells the viewer THAT is
what the speaker built. This is the single most expensive mistake available in the first 5 seconds,
and it is invisible to every mechanical gate.

**The grammatical-subject rule — the executable form.** Write the first spoken sentence. Circle its
subject/object noun. The opening visual may depict *only that noun*.
- "**I built an agent** that runs quietly in the background of my client's business" → licenses the
  agent and its output. Does NOT license the client's product, hardware, or premises.
- "**My client** runs crews laying out floor plans with robots like this" → licenses the robot.
Adjacent footage is legal only on the line whose grammatical subject owns it, and never at frame 0.

**Why it is worse than mere distraction** (evidence, 2026-08-11 research pass):
- **Coherence principle** — Mayer & Fiorella, *Cambridge Handbook of Multimedia Learning* Ch. 12:
  excluding extraneous material improved learning in **23 of 23 experimental tests, median effect
  size 0.86**. Their own worked example of a "seductive detail" is adding lightning-storm footage to
  a lesson on how lightning forms — exciting, topically adjacent, not the mechanism. That is exactly
  the failure shape.
- **Belongingness** — Grimes 1991, *Human Communication Research* 18(2): dissonant audio and video
  are processed as **two different messages**, exceeding attentional capacity. Supported.
- **Truthiness** — Newman et al. 2012: a *related but nonprobative* image raises the judged truth of
  a claim via processing fluency, persisting 48h. So a wrong-but-real visual does not merely
  distract — it lends felt-truth to the wrong proposition.
- ⚠️ Do NOT repeat the popular hook stats ("70–85% 3-second retention → 2.2× views", "TikTok
  viewers decide in 3 seconds 70% of the time"). They trace to marketing blogs citing each other
  with no primary source. Keep them out of client decks.

### The boring-artifact problem — the reframe

> **The interesting thing is never the software. It's the change the software caused.**

A workflow canvas, a node graph, an admin panel: these are the MECHANISM, and mechanisms are dull.
Shoot the **evidence** instead. Ranked techniques:
1. **Outcome substitution** — the output, not the system. Notion tasks materialising one by one at
   6:02 AM with no human present.
2. **Before/after contrast** — split frame, 1s each: 90-minute recording + blank doc | the same
   meeting as 11 tasks.
3. **Make the number the picture** — claim "7.5 hours" → a week grid deleting 7.5 hours of blocks.
4. **The receipt** — one artifact of proof: a notification reading "8 tasks created from Tuesday standup".
5. **Scale/aggregation** — one node is dull; 340 processed rows scrolling fast is not.
6. **Motion design ON the correct artifact** — zoom-to-click, smoothed cursor, 1.5–2× speed ramps.
   **This is how you fix low energy. Never by swapping the subject.**
7. **Human reaction shot** — the client's face reading the output; still the right subject.
8. **Kinetic typography** — text has no referent ambiguity, so zero misattribution risk.

### ⚠️ The empirical answer, which OVERTURNS the "don't open on the mechanism" instinct

The reframe above ("shoot the change, not the mechanism") is sound general theory. But a frame-verified
teardown of self-built-software Shorts (2026-08-11, view counts pulled live with `yt-dlp`) found the
opposite in *this* niche, and the empirical result wins:

**A titled, full-frame system map AS the literal first frame — 5 of 5 winners.** Not a shot of a
diagram: the diagram *is* the frame, edge to edge, big title naming the system, zero face. The top
performer opened on a hand-drawn "AI Financial Operating System" map and did **74,721 views against a
3,673 channel median — 20×**.

So an architecture/workflow canvas is the **strongest** opening in this category, not a risk. It fails
only under three observed conditions:
- **No title, small in frame, browser chrome visible** → reads as someone's screenshot (0.56× baseline).
- **Right visuals, hypothetical script.** Same title, same diagram, same dashboard overlay, and it lost
  at **0.46× baseline** because the VO said "*could* work" and "*say* your sales team" instead of "I
  built" plus a number. **The diagram buys attention; the first sentence has to spend it.**
- **Cutting to your face at ~5s** instead of ~9s.

The other winning mechanics, ranked by recurrence:
1. **Hold the map — no cut for 6–11s (4/5).** Winners' first cuts: 9.17s, 9.67s, 6.6s, 10.83s. Fast
   cutting is not the win; letting the viewer *read the map* is.
2. **Real UI windows IN over the still map at 2–5s, map dimming behind it (5/5)** — proof the map is a
   running thing, not a drawing, without ever cutting away. This is how the theory above and the data
   reconcile: **map first, output layered on top.**
3. **Recognisable product logos instead of abstract boxes (4/5)** — Stripe, Gmail, HubSpot, Yelp.
4. **A number spoken in the first sentence (4/5)** — 500 hours, $35,000, $15,000/month.
5. **Visible tool chrome as authenticity (2/5)** — Excalidraw's toolbar left deliberately in frame.
6. **Face as a small persistent PIP, never the frame (1/5 — and that one was the ~150× outlier).**

**Our own error, independently confirmed in the sample:** a video about an n8n workflow that opened on
**stock humanoid-robot footage** and withheld the real canvas until 0:10 returned channel-median on a
153K channel. Borrowed adjacent-domain imagery bought nothing.

**Honest limits:** four of the winners cluster in one publishing week, so channel-level distribution is
a confound that cannot be separated from hook quality here; the sample is YouTube Shorts only; and
audio was judged from timed captions plus scene detection, not by listening.

**Frame-0 order is fixed by processing limits, not taste: comprehension → curiosity → credibility.**
The viewer must be able to *name* what they are looking at in under ~0.5s; any time spent resolving
"what is this?" is stolen from the claim.

**The mute test — run it before every export.** Mute the first 5 seconds, watch, and say aloud what
the speaker built. Wrong answer = recut. It costs nothing and the user caught this failure with it in
one sentence.

**Table stakes vs levers (do not confuse them).** Karaoke captions, a text headline by 1s, and
artifact-on-screen recur in the winners AND in the dead videos (+1 view and +0.6% in 24h in the
sampled set). They are entry requirements. Neither fast cutting nor elaborate layout separated
winner from loser either. Do not claim a lever you have not demonstrated.

## 1c · The presenter-cutout layout contract (background-removed PIP over a full-frame graphic)

the user's preferred hook shape as of 2026-08-11: **they are on camera from frame 0**, background removed,
bottom-left, with the graphic running full-frame above and behind them. Route + cost:
`skills/video-editor/references/davinci-background-removal.md` (fal.ai, ~$0.004/sec).

**Four rules, all learned the hard way in one session:**

1. **A graphic that will carry a cutout must leave the cutout's quadrant EMPTY — design it that way
   from the start.** The v5 hook put its claim block bottom-centre; the cutout landed on top of it and
   the text was simply lost. *Text under a cutout is text that does not exist.* Sketch the cutout box
   before laying out the graphic, not after.
2. **The claim moves to the empty quadrant and lands ON the spoken word.** Here it went above their head
   over the diagram — "7.5 hours / SAVED EVERY WEEK" easing in at f138 with the VO speaking "7.5" at
   f140. A number the viewer hears and reads in the same beat is the whole point.
3. **Z-order is fixed: captions → cutout → graphics → face.** Captions must be IN FRONT of the cutout
   (the user, explicitly). In Palmier that means the caption track sits at index 0 — see the reorder
   recipe in `palmier-pro.md`.
4. **Placement that worked:** `transform {width: 0.5, height: 0.5, centerX: 0.25, centerY: 0.75}` on a
   1080×1920 canvas — a half-scale clip anchored bottom-left. Because the source framing puts their head
   near the top of frame, a half-scale bottom-left placement lands their head around mid-frame; that is
   why the graphic's mid/lower-left must stay clear. Do not "fix" the collision by shrinking them — that
   just makes them tiny. Re-lay-out the graphic.

**Camera rule for map/graph animations carrying a cutout:** a camera that follows a lit execution path
all the way to the end will drive the frame into the graph's sparse linear tail and leave the shot
nearly empty. Cap the pan (**45%** toward the path head worked) and keep the push gentle (0.58→0.70).
The map has to stay populated for the whole hold, because it is the entire background of the shot.

## 2 · Sourcing ladder — b-roll is EVIDENCE, not decoration

For founder/expert content the viewer is subconsciously auditing: *has this person actually
done the thing?* Every b-roll choice either deposits or withdraws trust. The ladder (take the
highest rung available):

1. **The real artifact, re-rendered from real data** — the house specialty. Pull the actual
   thing via API and render it with a camera path: n8n workflow JSON → HTML canvas
   (`X-N8N-API-KEY` + the workflow endpoint), the live KG via
   `npx convex run --prod dashboard/kgPublicTest:getGraph`, real dashboards, real file trees.
   Better than a screen recording: deterministic, brand-composable, re-renderable, and the
   REAL node names/labels do the persuading. (The n8n-to-cc panels with "Sales Call Notetaker"
   / "Check if in CRM" visible — that's the proof layer.)
2. **Screen recording of the real thing** — real product, real account, real cursor. Ask
   the user (§3) when it needs their session.
3. **Honest recreation** — a real task re-performed for the camera (real flows, real assets,
   better framing). Authentic if it truthfully represents how the work happens.
4. **Authored brand diagram** — for concepts, not for faking evidence (§1 explain-the-concept).
5. **the user-shot mood/environment footage** — desk, hands, 11pm-office; only they can shoot it (§3).
6. **AI-generated: conceptual ONLY** — abstract metaphors in brand palette; NEVER as fake
   documentary evidence (fake office, fake team, fake screens). That's where the trust cost is
   maximal.
7. **Stock: effectively banned.** Viewers recognize popular stock clips; a generic
   typing-hands shot under an expert claim reads as "template guru" and *withdraws* trust.
   Narrow exception: non-claim atmospherics you genuinely can't capture (a city aerial) —
   and even then prefer rung 5 or nothing.

**Mismatch is worse than absence:** b-roll that loosely fits the audio (stressed-face stock
under "we work fast") erodes credibility faster than staying on the face. When in doubt, face.

## 3 · The shot-request list for the user (standard early deliverable)

Emit this at build START (script-time). Format per request: **beat/line it serves ·
description · orientation (vertical) · framing (wide/med/close) · ~10–15s per angle**. Batch
so they can capture in one sitting.

**The b-roll bank (CHECK IT BEFORE REQUESTING — the user, 2026-07-12):**
`'~/Library/CloudStorage/GoogleDrive-<YOUR_GOOGLE_ACCOUNT>/My Drive/Business   Career/Entrepreneurship/Grow Audience/video-assets/the user_B-roll'`
(triple space in "Business   Career"; CloudStorage → `cp` a clip local to materialize before
import). Naming convention: `YYYY-MM-DD_slug_v.MP4` (`_v` vertical / `_w` wide). During asset
mapping, `ls` the folder LIVE (it grows) — never assume from this snapshot. As of 2026-07-12:
33 self-shot lifestyle/mood clips covering **morning routine** (wake-up, snooze, brush-teeth,
morning scroll), **doomscroll/phone** (bedtime scroll, toilet scroll, picking up phone at
desk), **at work** (planning at desk, working from behind/side, typing/drawing on iPad),
**chores** (cooking, fridge, microwave, laundry, mop, vacuum), **leisure/social**
(tv-binge, friends party, concert, pickleball, friend cooking, girlfriend hug, baby stroll),
**wellness** (meditate ×2, tea), and **driving**. New the user-shot clips get filed here in the
same convention.

Note what the bank does NOT cover: it's all rung-5 mood/lifestyle footage — zero screen
recordings, product shots, or over-shoulder work shots. So shot-request lists should spend
their asks on the EVIDENCE rungs (screen recordings of the real product/tool, POV of the
actual workflow), and pull mood beats from the bank instead of re-requesting them.

Standard founder shot menu (research-consensus + what our videos keep needing):
- **Screen recordings**: real product/tool in use — the actual n8n canvas scrolling, a Claude
  Code session running a skill, the Notion output page appearing, dashboards with real data.
  Cursor motion matched to what the script claims.
- **POV desk shots**: hands on keyboard, writing/sketching a diagram, phone-in-hand scrolling
  the real app. No face needed — intimate and authentic.
- **Over-shoulder**: them working at the laptop/whiteboard; viewer-in-the-room feel.
- **Environment/establishing**: workspace wide, sitting down to work, opening the laptop;
  the 11pm-desk mood shot for late-night story beats.
- **Detail shots**: hands + objects, shallow depth, uncluttered background, brand-adjacent
  props.

## 4 · Coverage + cadence budgets (the numbers)

- **Face majority.** Over half the runtime is their face; in high-performing shorts b-roll is
  the strategic minority. Full-cover b-roll bursts run **1–3s** (max 3–5s) then return to face.
  **Split-screen panels are exempt from the return-to-face clock** — the face stays visible in
  the bottom slot, which is exactly why `top_bottom` is the house b-roll layout and why a
  panel may run 10s+ while full-cover may not.
- **Graphic budget: 2–4 major graphic moments per 30–60s** (≈4–7 per 90–120s), where "major" =
  full-screen diagram or panel. Past that, graphic fatigue: a new visual event every 1–2s
  stops reading as clarity and starts reading as noise. The n8n-to-cc build (94s: 6 fullscreens
  + 2 panels + 1 float) sits at the ceiling — treat it as the max, not the norm.
- **Clean intervals are part of the design**: 2–4s of plain face between decorated beats;
  after a dense diagram, give processing time before the next visual event.
- **Diagram read-time (element-count → hold after settle):** 2–4 elements → ≥2–4s; 5–7
  elements → 4–7s with progressive reveal (sequential highlighting when >3 labels — never dump
  all at once). **If a beat can't give a diagram ~3s of settled visibility, it's not a diagram
  beat — demote to a text card.** Hard cap ~7 meaningful elements per vertical diagram; a
  6+-step process shows 3 at a time.
- **Every change is motivated.** ~3s visual-change cadence (cut, caption burst, graphic,
  reframe) but each change attributable to a beat — motion for flair is the #1 amateur tell
  per motion-design consensus. This is the same law as the ≤2-punch budget.

## 5 · Wiring into the build pipeline

1. Script locked → **shot-request list to the user** (§3).
2. Radio edit done, transcript fresh → **beat sheet + asset map** (§1): every beat labeled,
   every treatment assigned, every asset named (pull/render/bank/the user).
3. Author graphics FROM the sheet (overlays ref §2 + pre-render design review).
4. Place per the sheet (overlays ref §1 rhythm mechanics).
5. Verify gate: rendered-frame checks **against the beat sheet** — every planned treatment
   present ON its keyword, never-cover beats actually uncovered, budgets respected.

The beat sheet is also the review artifact: when the user wants to adjust the visual story,
edit the sheet and re-derive, don't improvise on the timeline.
