# Delivery Gate — "ready for review" is a GATED CLAIM

**Never tell the user a video is ready / final / done — and never copy a render to the Drive
delivery folder — without a completed scorecard showing every hard gate PASS.** If any hard
gate fails, the video is not ready; fix it and re-gate. No exceptions, no "mostly done",
no delivering with a caveat in place of a fix. Presenting an ungated render caused three
consecutive user ERROR flags on 2026-07-20 (uncut silences → amputated words + sliver debris
→ unstyled hook + clipped tail). This gate exists so that failure mode is structurally
impossible: the claim "ready for review" may only be produced BY the gate.

Written evidence is mandatory per gate — a command output, a frame capture, or a table.
"I checked it" without an artifact is a FAIL. Save the filled scorecard to the piece folder
(`delivery-scorecard-YYYY-MM-DD.md`) and append one row to [eval-log.md](eval-log.md).

## ☠️ "UPDATE THE STATUS" MEANS THE NOTION STAGE (the user, 2026-08-12 — they had to ask twice)

**When the user says "update the status" on a video, they means the Notion Content DB page's `Stage`
property.** The markdown files (`build-progress.md`, `build-checklist.md`) are EA's bookkeeping — they
are not "the status." Updating them and reporting "status updated" while the board still reads
`Visual Editing` is the failure, and it happened on this build: the final was exported, mastered and
published while the Notion page sat stale until they asked a second time.

**Video editing complete → the piece moves to `Packaging/Posting`. Every time. That is gate G9, and
it fires on the FINAL EXPORT, not on delivery-gate completion** — the export is the trigger.

```
notion-update-page {command:"update_properties", page_id:<page>, properties:{"Stage":"Packaging/Posting"}}
# verify CHEAPLY — do NOT re-fetch the whole page (these pages run 20k+ tokens):
notion-query-data-sources {mode:"sql", data_source_urls:["collection://<CONTENT_DB_DATA_SOURCE_ID>"],
  query:'SELECT "Name","Stage" FROM "collection://8b56bff4-..." WHERE "Name" LIKE ?', params:["%<slug>%"]}
```

**Make it structural, not remembered.** The delivery tail — export → master (G16) → thumbnail (G18) →
Drive publish → **Notion Stage (G9)** — is ONE chained job. Every step EA has had to "remember" on this
build got skipped at least once. Chain it and the gates execute by construction.

## Fixed values — SET these, NEVER re-derive

- **Music bed = −25 dB = `0.056` in Palmier's 0–1 clip volume.** This is the user's standing
  number, given many times. Set the music track volume to 0.056 and move on. Do NOT re-derive
  it from LUFS, voice-to-music ratios, "perceptual loudness," or any measurement — that
  re-derivation is the exact overthinking that lands the wrong level and burns their time. If the
  music ever *sounds* too loud, the cause is a broken/quiet VOICE (fix the voice, e.g. a missing
  leveled-audio source), NOT the −25 dB bed. Keep the existing outro fade to 0.
  **Ship check — music MUST be audible (2026-07-21):** before EVERY render, confirm the music
  track is NOT muted/hidden and its clips read 0.056. A muted A5 renders a music-LESS video that
  still passes "audio stream present" (the voice carries the stream), so the defect is invisible
  to G7. It happens because muting the bed to isolate voice gaps is a natural debugging move —
  and then you forget to un-mute. Verify on the render, not the compositor: a talking-head pause
  must show a bed floor ≈ −25 dB under the voice, never digital silence.

- **CAPTIONS ARE MATTY'S — never restyle or re-word them unasked (the user flagged ERROR, 2026-07-29).**
  If a caption group already exists (they styled it, or another process created it), you may READ it and
  REPORT defects, but you may not change content, style, font size, animation preset, or wrapping
  without their explicit go **that names the style consequence**. `update_text` on `content` is
  **one-way**: it destroys that cue's karaoke word-timings and no call restores them, so "just fixing
  a word" silently changes how that cue animates. Approval to fix caption *text* is NOT approval to
  degrade caption *style* — if the only available fix costs style, say so and let them choose.
- **Anything that can flip project resolution INVALIDATES caption wrapping.** `add_clips` silently
  re-matches the timeline to the incoming clip's resolution (it reports
  `"Matched timeline resolution to clip: WxH"` in `notes` — read that field every time). Caption cues
  wrapped for one canvas width render wrapped differently at another, turning single-line cues into
  two-line cues with no style field changing anywhere — so a diff of the caption group's `shared`
  style will look CLEAN while the burned output is visibly wrong. Rules: (a) after EVERY `add_clips`,
  check `notes` for a resolution match and restore the intended resolution immediately;
  (b) never leave a project at a different resolution than when its captions were created;
  (c) after any bulk clip op on or near the caption track, re-verify both the per-clip
  `textAnimation.preset` AND the rendered line count (captures, not the data model — the data model
  cannot show a wrap).
- **NEVER declare an ANIMATED element defective from a single captured frame (self-inflicted, 2026-07-29).**
  Karaoke runs `perWordFrames: 6`, so a mid-transition frame legitimately shows a half-opacity highlight
  block, a block lagging the spoken word, or no highlight at all. One capture at f28 looked "washed out
  and broken" and was reported to the user as damage; f18 on the same cue showed a solid block tracking
  word 1 correctly — **the cue was fine and the damage report was false.** Rule: sample **≥3 frames
  spread across the element's life** (early / mid / late) before asserting ANY defect in a caption,
  karaoke highlight, fade, flash, or animated graphic — and compare against a known-good element of the
  same type elsewhere in the timeline as the control. A retraction costs more trust than the extra two
  captures. Corollary: when you *do* retract, say so plainly and show the evidence both ways.
- **Reproduce the reported defect before repairing it.** the user reports what they sees; that it's real is
  not in doubt, but *your theory of the cause* usually is. Two repair attempts here (content revert,
  animation re-apply) were fired at a misdiagnosed cause and both were no-ops — provable because the
  render came back **byte-identical** (`encodedByteSize` unchanged). Compare encoded byte size across
  captures to prove whether a repair changed anything at all before claiming it worked.

## Hard gates (ALL must pass, in this order)

| # | Gate | Test | Pass condition |
|---|------|------|----------------|
| G1 | **Word fidelity** | `get_transcript` on the FINAL timeline, word-diff vs the script | Every audible script word present head-to-tail. Whisper words that flicker in ASR must be proven present by source-audio mapping (their source region survived into a clip). Any missing/mangled audible word = FAIL. This is the only gate that catches amputations. |
| G2 | **Cut safety** | every V1 cut boundary checked against the SOURCE envelope (`eval_cuts.py` or equivalent ≤ floor+13dB check) | Zero cuts landing on speech energy. Cut lists are computed from ASR word anchors + energy snap — never energy alone (energy misses quiet words), never ASR alone (stamps drift). |
| G3 | **No debris** | full `get_timeline` structural scan | No video clip <8 frames except intentional flash/transition assets; no phantom tracks; zero gaps in the base video track; linked A/V clips equal length. |
| G4 | **Head/tail contract** | first/last clip vs word map | First clip starts ≤6f before the first word's onset (zero pre-speech source). Last word's full decay included + ≥12f room before picture/audio end; end fade set. |
| G0 | **Dialogue leveling** (runs FIRST, before any pacing judgment) | compare loud-word vs quiet-tail peaks on the source (`volumedetect`) | If sentence tails/pickups sit >6dB below loud words, LEVEL THE VOICE before editing pacing: quiet speech under the music bed reads as silence, and no amount of cutting fixes it (cutting deletes words — forbidden). Recipe: extract full-rate audio → `highpass=f=70, compand=attacks=0.02:decays=0.15:points=-80/-80\|-50/-50\|-36/-27\|-26/-19\|-18/-16\|0/-11:soft-knee=6, alimiter` → import → mirror the V1 clip spans on a new audio track → mute the original linked audio (Palmier volume caps at 1.0, so in-app gain is impossible). Verify: quiet tails ≥6dB above bed, true gaps unchanged. |
| G5 | **Pacing** | `silencedetect` (bed+3dB, **d=0.30**) on the FINAL RENDER, then **MERGE windows separated by <0.15s** — clicks/breath blips split one perceived lull into several short windows that individually dodge any threshold (this exact artifact hid 0.87s lulls inside pairs of 0.4s windows across three renders) | **No MERGED non-designed lull ≥0.45s** (designed holds listed and excluded). Judged on the render meter — "if it reads as silence, it IS silence" (the user). Report merged count + max + designed-hold list. |
| G6 | **Visual composition** — execute the FULL overlay §5 15-item gate on the FINAL RENDER: `capture_frame` → `inspect_media` at every graphic (settled), every transition (±3f), every text/hook/CTA. NOT a "spot-check for stretch" — that framing shipped flag #6. | ALL of: (a) zero stretched text/media (text natural aspect; media BOTH dims from its own aspect); (b) **every screenshot / screen-recording is FULL-frame or split-screen (`top_bottom`) WITH motion — a small floating PIP is an automatic FAIL** (still image → baked Ken Burns; screen recording's own scroll counts); (c) **every diagram's concept is isomorphic to the narration AND its arrowheads actually RENDER** — arrowheads at node CENTERS hide under the node boxes, so place them at the box EDGE and confirm arrows on the settled frame (never assume `marker-end` in source = visible); (d) **every white flash peaks ON its graphic's cut (±1f); no graphic ends 1–3f before a transition (bare-face flash); no graphic FADES through the face** (adjacent fullscreens hard-cut under a flash or cross-fade on a new track — never fade-out-to-transparent); (e) zero collisions/clipped edges, all content in the central-82% safe zone, captions styled per brand. Attach the frame list. |
| G7 | **Render integrity** | `ffprobe` the delivered file | Duration == timeline duration, correct resolution/fps, audio stream present, file plays. |
| G8 | **Artifacts** | filesystem | `.palmier` checkpoint exported post-build; scorecard written to the piece folder; eval-log row appended. |
| G9 | **Pipeline-stage authority** | Notion | A final export, Drive replacement, hand-off, scorecard, or correction pass is **not** permission to change Stage. Keep the page at its freshly verified current stage. Advance only when the user explicitly directs it, then update the Notion status property and re-fetch to verify; mirror that confirmed value to the KG. |

**Quiet words vs silence (G1×G5 — the user's two rulings, 2026-07-20, applied together):**
(1) "if it reads as silence, it IS silence" — no lull survives on the render meter; AND
(2) "…as long as you don't cut out any words." Resolve the tension by MEASURING each quiet word's
raw source peak (ffmpeg volumedetect on its zone) and triaging:
- **Audible** (within ~10dB of speech level): never cut; protect with pads.
- **Quiet-but-real** (raw peak ≈ −20…−35dB, e.g. a trailed-off "again."): KEEP or RESTORE it, and
  make it audible with an externally boosted overlay — Palmier's clip volume is hard-capped at
  1.0, so boost outside: ffmpeg extract from the ORIGINAL source (`volume=2.5`, 40/60ms afades,
  48kHz) → `import_media` → `add_clips` on a spare audio track aligned to the word. Junction then
  fills with audible speech: both rulings satisfied.
- **Off-mic** (raw peak below ~−40dB): there is no audible content to save — boosting only
  amplifies room noise into an artifact. The zone is silence in every practical sense and is
  cuttable, PROVIDED the sentence reads grammatically without the word in both audio and captions
  (check the caption text). Record the per-word measurements in the scorecard — that
  documentation is what distinguishes "cut a word" (forbidden) from "cut a zone that never
  contained recoverable audio."
**Word-END is a FLOOR question, not an energy question (the user flagged the SAME word twice,
2026-07-22):** a word ends where the waveform returns to the noise FLOOR (silencedetect −45 dB),
never where it drops below a speech-level threshold. Word-final consonant clusters (-xt, -st,
-k, the "t" release) live at −30…−45 dB and ARE the word — ending an extension at −30 dB
amputated "context" a second time after the first fix. Two sub-rules: (1) a <150 ms dip INSIDE
a word is a plosive stop-closure (silence before the release), NOT the word ending — bridge
through it; (2) pad = floor + 1–2 frames. If the junction lacks room for the full word, insert
REAL time (insert_clips ripples every sync-locked track in lockstep — remove the single-clip
music bed FIRST so it can't be spliced, re-add after, and re-bake its baked fade for the new
duration; cover the video gap by extending the same-take video clip so the mouth stays synced).
When the user demonstrates the needed extent by dragging a clip edge in the UI, match HIS shown
extent — never re-derive a shorter one from a threshold.

**the user's sentence-final words TRAIL OFF — sweep EVERY junction, not the flagged one (the user
flag ×3: "context" twice, then "posted", 2026-07-22 — "sometimes my last word trails off a bit
quieter"):** their end-of-sentence delivery decays through −35…−47 dB for up to 12 frames before
reaching floor, so ANY energy-threshold cut amputates sentence endings specifically. Binding
rules:
- **One flagged junction = audit the CLASS.** Script a full sweep (10 ms RMS envelope of the
  leveled source; for every voice-clip junction compare the outgoing clip's source-end against
  the −45 dB floor crossing; flag `at_cut > floor+3 dB` OR any post-cut block > −40 dB within
  300 ms). Fixing only the junction the user pointed at is how "context" was followed by "posted".
- **Per-frame + transcript eyes BEFORE extending — post-cut energy may be a REMOVED NEXT WORD,
  not the tail.** One sweep hit showed −22.9 dB "continuing energy" that was actually the next
  (deliberately cut) source word; the word itself floored at +3f. Blind floor-math extension
  would have spliced a stray word into the edit. Check the per-frame envelope shape (release
  burst within 150 ms = consonant; fresh onset after real silence = next word) and the source
  text before choosing N.
- **Fix menu, cheapest first:** (1) **J-cut bridge, zero ripple** — overwrite the INCOMING
  clip's silent head-slack with a source-continuing tail bridge (`add_clips` same track; the
  overwrite head-trims the incoming clip, sliding its source start forward, so every word onset
  stays at its absolute frame and no other track moves). The word tail plays over the incoming
  shot's pre-speech face = a standard J-cut (the user himself demonstrated exactly this by dragging
  the audio edge). Requires measured head slack ≥ N. (2) **Ripple insert** where tail > slack
  (bed out first, per the recipe above) — then extend the same-take video +N for lip-sync,
  RE-SEAT any graphic that ended on the old cut (move it right so it still ends ON the cut;
  never stretch it past its asset length), and extend the word's caption clip to the new cut.
- **Bridge rounding trap:** add/insert with source-seconds can start the bridge 1 source-frame
  EARLY = the outgoing clip's last frame plays twice (33 ms stutter at the junction). Verify the
  bridge's trimStartFrame equals the outgoing clip's exclusive source end; repair by setting
  trimStartFrame + durationFrames in ONE call.

The safe cut recipe (verified): render silencedetect windows (−22dB, d≥0.62) → cut
`[window_start+6f, window_end−8f]`, edges snapped to clip boundaries within 7f (no orphan
fragments); the 8f end-pad protects the audible onset wherever it truly is (trust render energy,
never ASR stamps, for onset location).

**Opening / exposed-section tightness — dead-air removal is a BUILD step, not just a gate (the user
flag, 2026-07-21):** dead air reads WORST where the music bed is quiet and the picture is a
near-static talking head — i.e. the first ~10–15 s hook, before the bed comes up. A 0.2–0.4 s
inter-sentence pause there, on a held face, reads as "the video froze" even though it clears the
0.45 s G5 threshold (which is calibrated for the music-masked body). The bed masks the same gap
later; the open has nothing to hide it. So:
- **On every exposed talking-head stretch, ripple out every TRUE inter-word bed gap**, not only
  the ≥0.45 s ones. For each candidate gap measure a 50 ms **mean+MAX** envelope: MAX at the bed
  floor = true silence (cut it); MAX within ~12 dB of speech = a quiet word (KEEP — that's the
  "don't cut the word" half). Cut only the frames whose MAX sits at the floor, padded 1–2 f off
  each neighbouring word's energy. This is how you satisfy "remove the silence" AND "don't cut a
  word" at once.
- **Split-track ripple works and stays in sync (verified 2026-07-21):** with the leveled voice on
  its own track (A4), unlinked from the picture (V1), `ripple_delete_ranges` anchored on the
  VIDEO track still removes the same span from the sync-locked voice, music, clicks AND captions
  and slides everything −N in lockstep. Confirm it landed: the returned `shifted` list shows every
  content track moving −N, and a transcript re-read shows the next word's frame dropped by N with
  no word lost.
- **Never ripple THROUGH a motion graphic mid-clip** — it jumps the pan/animation, a worse defect
  than the pause (all three opening gfx here were motion videos, not stills — check `get_media`
  type first). Only cut a gap that lies in a talking-head region, or align the cut to a graphic's
  in/out so it becomes an invisible head/tail-trim of a hard-cut graphic. Under a moving
  full-screen graphic the motion masks a short pause — leave those.
- After any such cut, EVERY downstream cut/flash/graphic shifted −N frames — re-run the full
  visual gate from scratch (per Meta-rule #2), don't assume the head-cut alignments held.

**v10 fail-set (2026-07-21 evening — 4 the user ERRORs on one render). The ripple's hidden victims:**
- **NEVER let a ripple cut the music bed.** A sync-locked `ripple_delete_ranges` SPLICES the
  continuous music — the melody jumps at each splice (an audible skip that is NOT a click:
  transient checks pass it). A spliced/exposed bed also *reads as "music too loud"* even at a
  measured-correct 0.056 (−24.5 dB) — fix the splice/voice, never the number. The bed must be ONE
  continuous clip [0,end] at 0.056 + outro fade. After ANY structural edit verify: single music
  clip, source-contiguous, unmuted, 0.056. If a ripple removed frames, rebuild the bed continuous
  afterward — never ship a mid-song splice.
- **`set_clip_properties` is a SLIP, not a trim/roll** — it moves the source window
  (trimStart/EndFrame) and IGNORES startFrame/endFrame. There is no roll edit. To complete a
  guillotined word with NO ripple: split the NEXT clip at word-end+pad → remove the freed silent
  head → `add_clips` a bridge continuing the prior clip's source
  (`source:[priorSrcEndFrame/30, wordEndFrame/30]`) — seamless join, zero downstream shift.
  (`add_clips` shape: `entries:[{trackIndex, mediaRef, startFrame, source|endFrame}]` — source OR
  endFrame never both; OMIT trackIndex to CREATE a new track — audio media creates an audio track.)
- **Emptying a track DELETES it** (remove all its clips → track gone, indices shift — re-read the
  timeline). `manage_tracks` cannot add tracks; only add_clips/add_texts with omitted trackIndex can.
- **G1 needs BOTH transcript tracks + word-END coverage.** Diff the muted camera transcript (idx 7)
  against the audible leveled track (idx 10): a word on camera but absent on the audible track is
  amputated in the mix ("context" @1804 was). And check each clip's LAST word can FINISH inside the
  clip (clip end ≥ word start + articulation) — onset-presence alone passed a mid-word guillotine.
- **A quiet word can be IN the audio but MISSING from the captions** — ASR skips soft words ("me"
  at −16 dB → no cue → captions visibly "chop the last word"). Gate caption cues against the
  SCRIPT, not the ASR. `update_text` takes `content`; a content change clears that cue's karaoke
  word-timings (plain-text fallback on one cue is acceptable).
- **Sliver check, fast:** extract render frames across every graphic↔face transition — graphic
  frames compress ~250 KB, face frames ~2 MB, so the file-size sequence pinpoints the transition
  frame; a lone large frame among small = a face sliver. Verify small→large flips exactly on the
  intended cut.
- **Palmier renders audio volume KEYFRAMES at ~unity — only the STATIC clip `volume` property
  attenuates (verified across 2 renders, caught by the user on v11).** v10's static-0.056 body clips
  rendered a perfect −25 bed while its one keyframed clip (the outro) rendered hot; v11's single
  keyframed bed played wall-to-wall at ~0 dB gain (bed-only window @4.2s: max −0.1 dB vs −25 spec).
  NEVER carry the bed level (or its fade) in volume keyframes: bake fades into the audio FILE
  (ffmpeg `afade`), place one clip, set STATIC `volume: 0.056`. **New hard check (part of the music
  ship-check): on EVERY render measure a voice-peak reference window AND ≥2 voice-free windows —
  the bed must sit ≥18 dB BELOW the voice peaks (ratio, not absolute).** On an unmastered render
  the bed reads ≈ −25 ± 4 dB absolute; after mastering everything shifts up together — the RATIO is
  the invariant. A "music present" differential is NOT a pass — v10's −8.7 dB outro was this exact
  defect misread as presence-proof.
- **A Palmier app restart can flip the export loudness processing.** v1–v11 rendered
  loudness-normalized (mean ≈ −12 dB, voice peaks 0.0 dBFS); after a restart, v12 rendered RAW
  (mean −25.6, peaks −4.3) from the identical voice timeline. the user's 0.056 calibration was made
  on normalized renders — so compare whole-file mean/max against the previously approved render, and
  run the bed ratio-check on the MASTERED file. Never ship a −25-mean master because "the timeline is
  right." **Mastering is NOT conditional on noticing a quiet render — see gate G16, which runs on every
  export.** This bullet used to be the only loudness instruction in the file and it was written as a
  contingency ("*if* a render comes out raw/quiet"), so a −20.2 LUFS master shipped for review
  unflagged: nothing looked broken, so the condition never fired. **A rule that only applies when you
  already noticed the problem is not a rule.** It also prescribed two-pass `loudnorm`, claiming linear
  gain preserves the voice:bed ratio — on this material loudnorm selects **dynamic** mode and does not.
  G16 carries the corrected method.

**v13 fail-set (2026-07-22 — 4 more the user flags; each is now a hard check):**
- **Source-boundary audit — the REAL cause of "the visual goes transparent right before the
  cut."** For EVERY video-graphic clip: last-used source frame MUST be < asset frame count
  (trimStart + duration ≤ assetFrames − 1). A source window that touches/overruns the asset end
  renders BLANK on its final frame(s) → the face peeks through 1–2 frames before the cut (the
  classifier needed src frame 276 of a 276-frame asset). Corollary: in the file-size transition
  sweep, a flip landing 1 frame BEFORE the expected cut IS this defect — never write it off as
  seek imprecision.
- **set_clip_properties trims are NOT a slip/roll — never arithmetic-edit trims.** Setting
  trimStartFrame alone can SHRINK the clip and even drag the whole timeline shorter (the CTA
  clip went [2840,2988]→[2840,2971] and the music bed auto-trimmed to match). To retime a
  graphic clip: remove + re-add with startFrame + source(seconds), then pin exact length with
  durationFrames — source-seconds rounding drifts ±1, so ALWAYS check the returned `frames` and
  correct with durationFrames. A ±1 drift left unfixed = a 1-frame gap (face flash) or overlap.
- **IMAGE clips are banned from delivery timelines — they fail BOTH pipelines (final ruling
  2026-07-22, supersedes the alpha-ProRes recipe below):** (a) API-created image clips never
  render in EXPORT (proved v13/v15, and again on an old 2-frame flash that exported zero wash);
  (b) NO image clip composites in the APP PREVIEW — the user scrubbed an old flash that renders
  fine in export and saw their talking head, no white ("white flash is not working in the
  preview"). the user reviews in the preview, so export-only correctness is still BROKEN. Standard
  flash recipe: an OPAQUE WHITE H.264 VIDEO (`ffmpeg -f lavfi -i color=c=white:s=WxH:r=30:d=0.2
  -c:v libx264 -crf 10 -pix_fmt yuv420p`) placed `[cut−2, cut+3)` with clip opacity KEYFRAMES
  `[[0,0],[2,0.85],[5,0]]` — peak lands ON the cut frame. Both legs are independently proven:
  video clips render in export and preview; opacity keyframes on VIDEO clips render (the float
  cards). The earlier alpha-ProRes flash worked in export but was never proven in preview — do
  not reuse it. Sweep the timeline for ANY remaining image clip (stills included — freeze
  frames become 1-frame-looped VIDEOS) before calling a cut done. EYEBALL one flash frame on
  every render — file sizes lie about washes.
- **A flash that peaks BEFORE its cut is a missing flash:** one old flash sat [2631,2636] with
  its 0.85 peak 6 frames ahead of the 2639 cut (fully faded by cut time) and another was a
  2-frame sliver whose ramp never reached peak inside its own span. When placing or auditing
  flashes, assert peak-frame == cut-frame, not just overlap.
- **Diagram choreography contract (the user):** arcs draw the FULL circuit in tight sequence (no
  inter-motion gap >10 frames — a mid-build stall reads as broken), the line ENDS AT the
  arrowhead (cap the draw at the head's path-fraction; head fades in as the line arrives),
  center icon/text appears only AFTER the circuit closes, then settled hold. Arrowhead placement
  must be viewport-scale-proof (convert node rects into SVG coords via getScreenCTM().inverse()
  — getBoundingClientRect in CSS pixels against viewBox units misplaces heads when the render
  viewport isn't 1:1). Verify by EYEBALLING four states: mid-draw, circuit-complete-no-center,
  center-in, settled. Rebuild pipeline: `~/Downloads/mp-fix/loop-rebuild/render_loop.py`
  (playwright frame-stepper, 1080×1920 DSF1 → ffmpeg assemble).

**On-screen text policy — captions are the ONLY floating text (the user rule, 2026-07-22):**
- **Never two sets of floating text.** If any text besides the captions floats over the
  talking head ("You're not gonna make it" in red over their face; a static "+1 rule" label),
  it's a defect — "it's very confusing what we're trying to do there." Every non-caption
  statement must be one of: (a) a **full-screen or half-screen card** (opaque brand
  graphic), or (b) an **animated visual element with a sound cue** (e.g. a "+1 rule" badge
  that pops in with a bing) — a designed object, never raw floating type. The opening hook
  title is included: it gets a standardized Fractal-AI title treatment (branded band/card,
  face still visible) because the opening frame doubles as the thumbnail.
- **Bold or humorous spoken statement ⇒ full-screen visual moment.** When the VO makes a
  punchy claim or joke ("you're not gonna make it"), give it the whole screen for its beat:
  full-frame brand card, big type, and a humor element (emoji/GIF energy — 💀 etc.).
  Word-timed: card spans exactly the spoken phrase, flash+click on both cuts.
- **Any "steal my skill" / lead-magnet mention ⇒ show the artifact.** Every time the VO
  offers the skill/lead magnet ("you can steal my skill at the end", "grab my template"),
  put a visual of the thing on screen — full-page card with a concrete representation
  (file-card UI with the skill filename, an image, or an emoji) — never let the line play
  over unrelated b-roll or a bare face. Sweep the TRANSCRIPT for every such mention; the
  end-CTA card alone does not cover earlier mentions.

**Named-concept ⇒ shown-concept (the user flag, 2026-07-21 — "closed feedback loop" said to a bare
face):** if the narration NAMES a concept/object/diagram the piece owns a visual for ("the loop",
"closed feedback loop", a product screen, a chart), that visual must be ON SCREEN during those
words — INCLUDING CALLBACKS: naming it again later re-shows it (a settled hold of the earlier
diagram; 1–1.5 s is enough for recognition on a re-show). Remove any competing text overlay that
just repeats the same words — the diagram IS the message (one clean point per beat). **Gate:
sweep the final transcript for every noun-phrase that matches an existing visual asset/beat and
confirm the visual overlaps those words on the timeline; a named-but-not-shown beat = FAIL.**
This should have been caught at the beat-sheet stage AND at G6 — it is now an explicit check in
both.

**Meta-rule (how the 2026-07-20 failures shipped):** after ANY repair pass, re-run ALL gates,
not the one that caught the last bug. Each fix tool can create a new defect class the previous
gate is blind to (global ripples → slivers + amputations; lead-trimming → quiet-word loss).

**Meta-rule #2 — a recut/ripple INVALIDATES the visual gate, not just the audio gates (how flag
#6 shipped, 2026-07-20):** a recut fixes audio timing but the visual composition is NOT
automatically still-correct. Every `ripple_delete_ranges` MOVES cuts — desyncing white flashes
from the entrances they're supposed to cover — and the composition may carry defects INHERITED
from the pre-recut build that the audio pass never looked at: floating-panel screenshots that
should be full-screen, a "loop" diagram whose arrowheads never render, graphics that fade through
the face. Auditing only G0–G5 (leveling / silence / words) and assuming "the visuals were fine
before" is exactly the miss that drew flag #6 (four visual defects in a delivered recut:
no-arrow diagram, two floating screen panels, cuts before transitions). After ANY recut, re-run
the FULL G6 / overlay §5 visual gate from scratch on the new render.

## Scorecard (0–100) — measures quality; gates decide readiness

Score AFTER all gates pass (a gated-FAIL video is not scored — it's not done). Purpose:
comparable number per video so improvement is measurable in [eval-log.md](eval-log.md).

| Category | Max | Scoring |
|----------|-----|---------|
| Word fidelity | 25 | 25 = every word bit-perfect incl. whisper fringes; −1 per documented whisper-fringe trim; −5 per audible word lost (should be impossible past G1) |
| Cut cleanliness | 20 | 20 = zero debris/stutters ever reached a render; −1 per structural defect caught only at final gate; −5 per defect that reached a delivered render |
| Pacing | 15 | 15 = all junctions 0.2–0.7s; −1 per junction lull 0.7–1.2s; −2 per lull >1.2s (excl. designed holds); floor 0 |
| Visual polish | 20 | 20 = every spot-check clean on first capture; −1 per issue caught and fixed in the loop; −5 per visual defect delivered |
| Brand compliance | 10 | fonts, colors (teal/red contract), caption style, safe areas, thumbnail rule |
| Delivery hygiene | 10 | checkpoints each phase, notes/postmortems updated, evidence attached, eval-log row |

**Improvement metric:** score trend + "user ERROR flags" column (target: 0) + "renders until
delivery" column (target: 1). A delivered render that draws an ERROR flag triggers a mandatory
postmortem AND a rubric review (did a gate fail to catch it? add/repair the gate).

**v8/v9 fail-set (2026-07-30 — six the user flags in one review round). Each is now a hard gate;
run ALL of them in the FINAL POLISH PASS before any "ready" claim:**

| # | Gate | Test | Pass condition |
|---|------|------|----------------|
| G10 | **Content parity (script is the ONLY source of truth)** | For EVERY graphic: extract every text string (names, counts, order) and diff line-by-line against the CURRENT script/source doc — at build time AND again at gate time | Zero mismatches in names ("PILOT" not "PILOTING", "ROLL OUT" not "IMPLEMENTATION"), counts ("5 phases" when the VO says "5-step"), and ORDER (a gate always renders AFTER the phase it judges). Three separate flags shipped in one session because the rail was built from a retired diagram in memory. Never trust a previous generation of the same graphic. |
| G11 | **Face clearance** | Capture every overlay at ≥2 frames in EACH distinct framing it spans (base + every 1.07/1.18 punch state) | No overlay pixel over eyes or mouth, ever (the user rule). Chest-zone floats start ~y1020. A row clearing the chin in one framing covered the mouth in the next (versus card y850→y1030). |
| G12 | **Anchor freshness** | Immediately before placing ANY word-timed element (emoji, float, flash, click), re-read the CURRENT cue/transcript frames; after ANY ripple by anyone, re-verify every timed element downstream of the ripple point | Element overlaps its spoken word on the CURRENT timeline. The 🏆 landed on "framework from" because the user ripple-deleted 101 frames upstream between plan and placement. Planned frame numbers go stale the moment anyone edits. |
| G13 | **Chapter alignment** | For each chapter: title card span vs announcement words vs neighboring cues | Title visible for the WHOLE spoken announcement (enters at "step…", or the take cut carrying it); NO caption cue overlaps any title card (trim the previous cue to end at title start); flash+click sit on the title entry. |
| G14 | **Junction tail (render-side)** | `junction-tail-audit.py` pattern on the FINAL RENDER: per base cut, RMS last 2f vs next 4f | No cut with pre>0.025 && post<0.012 (truncated word decay). ASR word-starts CANNOT catch this. Fix = butt-continue the outgoing take into the incoming clip's pre-speech silence (non-ripple), verify in-point advance. |
| G19 | **Published files verified ON THE MOUNTED PATH** | `stat` the file inside `~/Library/CloudStorage/GoogleDrive-…/marketing/…` and compare byte size to the local master | An API upload response is NOT proof the file the user opens has changed — cloud and mounted folder are two copies. Verify the one in their Finder. Also confirm `<slug>-final.mp4` holds the CURRENT master's bytes, not an older cut wearing the canonical name. |
| G18 | **Thumbnail is re-extracted from the FINAL master and published** | `stat` the thumbnail vs the master; confirm the Drive copy's byte size equals the local file | The thumbnail is a **hook frame of the master that shipped**, not a survivor of an earlier cut. **A thumbnail older than the master is a FAIL** — and the dangerous case is that it silently keeps sitting in the delivery folder, so the video changes and the published still does not. Hit live 2026-08-11: the intro was rebuilt twice while an Aug-9 thumbnail (a mid-video "10 meetings every week" beat) stayed in Drive `marketing/images/thumbnails/`. **Update the existing Drive file by `fileId` rather than uploading a new one**, so links stay stable, then verify by size. Destinations: video → `marketing/video/<slug>-final.mp4`, thumbnail → `marketing/images/thumbnails/<slug>-thumbnail.png` (Drive folder id `1TqTdQQAyobReLInTz_3viUH9E7_LCKSb`). |
| G17 | **Text inside the platform safe zone** | Check every text element's x-extent against the project safe zone — `common.css .safe` = **x ∈ [107, 973]** on a 1080-wide frame (~10% each side) | LinkedIn and most vertical feeds **crop the left/right edges**. Backgrounds and texture may bleed full-width; **TEXT may not.** Caught by the user 2026-08-11 on a graphic whose chrome bar used `padding: 0 44px` and carried a top-right pill — both sat outside the zone and would have been clipped in-feed. Fix is one CSS value; the cost of missing it is an unreadable title on the most-viewed frame of the video. |
| G16 | **DELIVERY LOUDNESS — master to platform spec. UNCONDITIONAL, every export, no exceptions.** | `ffmpeg -hide_banner -nostats -i <render> -af ebur128=peak=true -f null -` on the FINAL file | **Integrated −14 LUFS (±0.5) and true peak ≤ −1.0 dBTP.** Palmier exports at whatever the timeline sums to — on the ai-notetaker build that was **−20.2 LUFS**, i.e. ~6 dB quieter than every other video in the feed, which reads to a viewer as low-energy, not quiet. Master the delivered file; do NOT chase it with per-clip gain (Palmier's volume caps at 1.0 and there is no limiter, so you cannot both raise level and control peaks in-app). **Method — constant gain + true-peak limiter, NOT `loudnorm` alone:** measure first, then `-c:v copy -af "volume=<Δ>dB,alimiter=limit=0.78:attack=5:release=60:level=disabled" -c:a aac -b:a 256k`. `-c:v copy` keeps the picture bit-identical, so mastering is free and repeatable. **Why not two-pass `loudnorm`:** on an already-compressed mix (LRA ≈ 3 LU) the required gain exceeds the TP ceiling, so loudnorm silently selects `normalization_type: dynamic` and applies time-varying gain — it re-balances a voice:bed ratio the user already approved. Constant gain preserves that ratio exactly and the limiter only touches transients. Check `normalization_type` in loudnorm's pass-1 JSON before ever trusting it. Re-measure the mastered file and cite I / LRA / true peak. |
| G15 | **Exit flash coverage** | List every fullscreen-visual/b-roll → talking-head transition; check each for flash+click | EVERY image/b-roll/card → face reveal carries white flash ([cut−3,cut+3], peak on cut) + click ON the cut (vol 0.6) — the user rule 2026-07-30. Floats (chest cards) exempt. Respect any junction the user hand-built differently (e.g. their fade-out on their own clip). |

**Co-editing note (binding):** when the user is live in the app, gates G10–G15 must run against a
FRESH `get_timeline` taken after their last edit — and any agent clip missing from that read was
likely eaten by the shared undo stack, not "already done". See overlays §6 for the full protocol.

## Polish gates P1–P9 — BINDING, added 2026-08-10 after a 10-defect the user review (ai-notetaker v5)

**Meta-rule that triggered this section: a checked gate with stale or low-resolution evidence is
worse than an unchecked one.** Every gate row must cite evidence generated from the CURRENT
timeline/render in the same pass. Contact sheets at reduced zoom are NOT evidence for composition
gates — the unit of evidence is a per-graphic FULL-RESOLUTION crop plus a written judgment line per
checklist item. Ten defects shipped to review under gates marked PASS; every one was findable.

| # | Gate | How | Pass bar |
|---|------|-----|----------|
| P0b | **A wipe exists to hide a FACE cut — no face cut, no wipe. And two clips on the SAME video track can never wipe between each other.** If the outgoing clip is b-roll or another graphic, there is no cut to hide: use a straight cut on the beat and put the click ON the cut frame (not ramp-start+1, which is the ramped-transition convention). The same-track case is a hard mechanical limit, not a style call: the incoming clip's crop ramp opens over whatever is BELOW it, and the outgoing clip on that same track **has already ended** when the ramp starts — so the ramp reveals the talking head underneath for exactly the ramp's length. That is the 4-frame face flash the user flagged 2026-08-11 at the Dusty→Meeting-Volume cut. To wipe between two full-frame visuals you would need the outgoing one on a lower track; usually not worth it — straight-cut instead. |
| P0 | **THE CUT-HIDING RULE — the rule the user has given the most times. Read it twice.** A fullscreen graphic exists to HIDE a talking-head cut. Therefore: **the graphic is at FULL coverage on the cut frame, and the wipe NEVER straddles the cut.** Everything below is a consequence of that one sentence. | Per graphic: its start/end + every V1 cut frame; per wipe: the abs frame range of its keyframe ramp vs the cut | ALL of: (a) **ENTRY — the wipe runs on the OUTGOING clip and is DONE by the cut.** Graphic starts at `cut − D`; ramp occupies `[cut−D, cut]`; the frame numbered `cut` is already fully covered. A wipe that STARTS on the cut is the defect — the viewer sees the new clip for D frames and then it gets swallowed. (b) **EXIT — the wipe starts ON the cut and runs into the INCOMING clip.** The graphic holds full coverage through the cut frame, then opens across `[cut, cut+D]`, revealing the new clip already underway. (c) **A fullscreen visual NEVER ends before the talking-head clip under it ends.** Ending 6–15f early exposes a sliver of face and then cuts. (d) An edge within ~20f of a cut but not ON it is a FAIL, not a rounding error. Move it and keep every internal beat on its original absolute frame: `start −= D` **with** `trimStartFrame −= D` (needs D frames of head room — check `get_media` duration first). **No head room? Re-render the graphic with a D-frame idle head pad** (`TOTAL_FRAMES += D`, `seek = F => inner(max(0, F−D))`) — do NOT let the content slide D frames early instead. (e) Move the transition SFX with its wipe, landing it on the ramp's **first VISIBLE frame = ramp-start + 1**, never on keyframe 0 (at keyframe 0 the aperture is fully closed on an entry / fully open on an exit, so nothing has appeared yet and the transient fires ahead of the picture). Entry ⇒ click at `cut−3`; exit ⇒ click at `cut+1`; 4 frames, −6.021 dB. (f) Graphic→graphic handoffs are exempt (no face is visible), but list them explicitly rather than letting them hide a violation. (g) **A square wipe REQUIRES a clip underneath it ON THE SAME TRACK for the whole ramp — so a graphic→graphic wipe on ONE video track is structurally impossible.** The ramp reveals whatever is on the track BELOW; if the outgoing clip is a neighbour on the same track it has already ended, and the ramp exposes V1 — the talking head — for D frames. That is the defect P0 exists to prevent, arriving through the back door: the wipe was anchored to the V1 cut perfectly and still flashed the face. **Before keying any entry ramp, name the clip that will be visible under it during the ramp.** Can't name one? Then it is a straight cut. (h) **Corollary — do not decorate a cut that hides nothing.** The wipe's only job is to conceal a face cut; between two full-cover visuals a straight cut is correct, and the click goes ON the cut frame (the ramp-start+1 rule in (e) applies only where a ramp exists). **Zero tolerance: one straddling wipe, one early-ending visual, or one ramp with nothing under it fails the gate.** (2026-08-11: a 4-frame face flash at the Dusty→Meeting Volume cut, shipped under a P0 that every existing clause passed.) |
| P1 | **Transition integrity** | Frame-step EVERY transition on the final render: capture [cut−4, cut+4] for every wipe, flash, and graphic entry/exit; view full-res | **A wipe is a boundary between TWO CLIPS, never a dip to black.** At every frame of the wipe the outgoing clip is on one side of the square and the incoming clip is on the other — one inside, one outside. Iris-to-black + hard cut + iris-from-black is TWO transitions with a black hole between them and is a FAIL. Build it as an animated `crop` on the upper clip (insets shrink/grow through a PERFECT SQUARE) so the lower clip is revealed directly — no black frame, no fade. Every transition COMPLETES: wipes fully close/open; flash peaks on the cut; the incoming graphic is FULLY OPAQUE the frame it lands behind a wipe/flash — an opacity fade-in that shows the face through a fullscreen graphic is a partial transition and FAILS; nothing from the outgoing shot bleeds through. ONE partial or wrong transition = the video does not ship. (2026-08-10: "partial transitions and incorrect transitions everywhere … a total mess.") |
| P2 | **Real-artifact rule — REAL IS NOT ENOUGH, IT MUST BE THE RIGHT REAL THING** | Beat-sheet time AND gate time. Per beat, write the VO line beside the asset and read them together as a viewer would | NEVER a static emoji (🤖 etc.) as the visual for AI or a product — AI-slop pattern, automatic FAIL. When the VO says "I built X", **SHOW X — not something adjacent to X, however real.** (a) **The visual asserts authorship.** Footage playing under "I built…" tells the viewer THAT is what the speaker built. Real footage of a *client's* product, a *partner's* hardware, or a neighbouring domain under that line is a false claim, not b-roll. (b) **The trap is the boring-artifact trap:** when the true subject is software (a workflow, an agent, a dashboard) it is visually dull, and some adjacent real footage is visually thrilling. That asymmetry is exactly when this gate gets broken — the pull toward the exciting asset IS the failure mode, so treat "this looks so much better" as the alarm, not the justification. (c) **Adjacent footage is legal only where the VO names its owner** ("a construction GC, a robotic field layout startup…") — put it on that line, never on the claim line. (d) No asset? ASK the user at beat-sheet time or capture the real system yourself — never substitute silently, and never upgrade a substitution to the hook because it is prettier. **Test to apply: mute the video, watch the opening, and say aloud what the speaker built. Wrong answer = FAIL.** (Broken 2026-08-11: opened on a client's Dusty Robotics FieldPrinter under "I built an agent that runs quietly in the background of my client's business." the user: *"It looks like I'm talking about literally building the robot that you're showing on screen."* The correct artifact — a render of the real 31-node notetaker workflow — was already built and sitting unused.) |
| P3 | **No attribution footers inside video graphics** | Scan every gfx source + settled frame | "FRACTAL AI" / "fractalai.agency" watermark lines belong to social-canvas STATICS (posts/carousels) only. In-video animations carry no attribution. Sole exception: a CTA card whose content IS the URL. |
| P4 | **Calendar-grid for weekly quantities** | Design review at beat-sheet time | Any "N per week" / "hours per week" / "meetings per week" claim renders as a 7-column week grid (no times/numbers needed) with event blocks placed like real calendar events; growth = MORE blocks appearing on the SAME grid. People parse calendars instantly; abstract card/stat layouts lose to them. |
| P5 | **Diagram content discipline** | Per-graphic full-res crop + text inventory | (a) A graphic with a title gets NO eyebrow/kicker line. (b) No phrase repeated across elements. (c) Every chart renders COMPLETE — a clipped donut/bar/axis = automatic FAIL. (d) The diagram must show something the spoken words don't already carry; when the VO names a concrete artifact (a task, a workflow), render the real thing, not labeled boxes that restate the narration. |
| P6 | **Hook velocity — and FRAME 0 IS A FRAME** | Frame-step f0–f15 of the final render; separately assert every track's first clip starts at 0 and `gaps` is empty on every track | The opening move SNAPS: punch-in completes in ≤6 frames (0.2 s) or is a cut/whip. A 10f+ eased zoom is a slow push, not a hook — FAIL. Motion AND payoff visible inside the first 0.5 s. **PLUS: frame 0 is fully composed — picture, captions, voice and music all present on it.** Any blank/black/partial opening frame is an automatic FAIL, and so is a timeline whose clips all start at frame N>0: that is not "a small offset", it is dead air in the single most expensive half-second of the video. **Check it FIRST, before any other polish gate** — it is invisible in a contact sheet, survives every structural check (no gaps *between* clips), and costs the hook. Fix by rippling the head range closed across ALL tracks; a head range that sits entirely before the music bed's first frame can include the bed safely, since nothing is spliced. (2026-08-11, the user: *"0.5 seconds starting off the video is a big no-no. Make sure you don't ever make this mistake again."*) |
| P7 | **Duplicate-take scan (render ASR)** | ASR the FINAL render; flag any ≥3-word n-gram repeating within an 8 s window | Any repeat = an outtake left in (FAIL) unless listed in the beat sheet as a scripted rhetorical repeat. (v4 shipped "if your … if your".) **Run on RENDERED audio, never the timeline transcript** — a trimmed clip inherits its source's cached word alignment, so words before the new trim point silently vanish from `get_transcript` while remaining audible. **When the user names a phrase, grep the transcript for THAT phrase and report its occurrence frames** — never infer which defect they meant from timeline structure. **Gaps are not the only shape an outtake takes:** it may be an isolated clip they split out and left in place, and the audible dialogue may live on a different track than the one carrying the hole — a "no gaps" structural check is blind to both. Confirm any ambiguous take boundary by exporting the candidate span to a NEW file and forcing a fresh transcription; windowed ASR of an already-transcribed asset returns cached sentence alignments and cannot resolve it. |
| P8 | **SFX semantics** | Inventory every tick/click vs what appears on that frame | `tick` fires ONLY when a box/container/card APPEARS. Text-only reveals are SILENT. `click` belongs to transitions (wipe/flash) only. Sound marks structure, not motion — a tick on every reveal is noise. |
| P9 | **Music bed durability** | Timeline + beat check | The bed is placed from the FULL-LENGTH processed source, trimmed on the timeline, with ≥5 s of source headroom past the final frame so the end is EXTENDABLE in the UI. The out lands on a beat (verify with detect_beats) under the fade. A bounced exact-length bed = FAIL. |
