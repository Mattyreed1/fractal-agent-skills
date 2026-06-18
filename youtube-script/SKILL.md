---
name: youtube-script
description: >-
  Author long-form Founder Freedom YouTube video scripts in the user's voice. Covers the two scripted formats (Personal Founder-Journey and Founder Story), packaging-first workflow (title/thumbnail/hook before scripting), retention structure, and scene/doodle direction. Use when writing or scripting a Founder Freedom video, drafting a video hook/title/thumbnail, outlining a video, or turning a topic or another founder into a video. This is AUTHORING — to compress someone else's video into a report use yt-video-report instead. Triggers: "write the youtube script", "script my next video", "draft a founder story video", "personal journey video", "make a video about [founder]", "video hook/title/thumbnail", "outline this video", "founder freedom video".
license: MIT
metadata:
  version: 1.1.0
  author: the user
  type: authoring
  category: content-creation
  brand: founder-freedom
  tags: [youtube, video, script, founder-freedom, long-form]
---

# youtube-script — Founder Freedom Video Scripting

Write long-form YouTube scripts for the **Founder Freedom** channel in the user's voice, applying current retention best practices. This skill AUTHORS original videos. (To compress someone else's video into a report, use `yt-video-report`. To repurpose a finished video into LinkedIn/X posts, that's the `content-*` engine.)

The channel makes three things; this skill scripts the **two written formats**:

| Format | What it is | Reference | Storytelling arc |
|---|---|---|---|
| **Personal Founder-Journey** | Talking-head documentary of the user's own path. Memoir + manifesto + how-to. Builds the bond and the reason to subscribe. | [references/personal-journey.md](./references/personal-journey.md) | Hero's Journey / Personal Learning |
| **Founder Story** | A famous-or-niche founder's story used as the vessel to teach a stealable philosophy. The growth engine. | [references/founder-stories.md](./references/founder-stories.md) | Lesson From Others |
| _Podcast_ | Founder interview. Not scripted — out of scope for this skill. | — | — |

**Decision:** Is the video about **the user's own lived experience** → Personal Journey. About **another founder's story used to teach** → Founder Story. If unsure which, ask the user (don't guess — the formats have different spines).

**Narrative craft is Founder-Freedom-specific.** Both arcs are executed FF-style in [references/storytelling.md](./references/storytelling.md) — read it before drafting. It replaces generic storytelling theory for this channel (the generic 10-format version in `writing/references/storytelling.md` is only an optional theory root).

---

## Phase 0 — Intake (gather before writing)

Required inputs. If any is missing or ambiguous, ask the user once (`AskUserQuestion`), don't assume:
- **Format**: Personal Journey or Founder Story.
- **Subject**: the topic/lesson (Personal) or the founder + the lesson to steal (Story).
- **Journey stage served**: considering the leap / building the side-gig / newly full-time / day-one founder. (Every FF video bridges to one of these.)
- **Where the script lives**: default `projects/founder-freedom-content/<YYYY-MM-DD-slug>/script.md`; mirror to Notion KBase if the user wants it in the video DB.

Read the matching format reference, [references/voice.md](./references/voice.md), and [references/storytelling.md](./references/storytelling.md) (Founder Freedom storytelling) before drafting.

**Founder Stories also require Phase 0.5 — Source Gathering** ([references/source-gathering.md](./references/source-gathering.md)): pull real footage, quotes, and artifacts into a `sources.md` BEFORE scripting. Real artifacts carry the format — don't script from memory.

**Founder Stories then run a post-draft Clip-Finding Pass** ([references/clip-finding.md](./references/clip-finding.md)): once the script is drafted, map a real supporting artifact — a **founder video clip, a tweet, or a quote card** — to each beat. The **video-clip** part calls the clip engine's clip finder (`clipengine.clips.find_in_video` / `clipengine.youtube.discover`); tweets and quote cards are produced here. _the clip engine capability is live — this pass now runs._

---

## Packaging-first — NON-NEGOTIABLE

FF strategy is packaging-first: **decide the idea → title → thumbnail BEFORE scripting or recording.** Confirm an idea is clickable before investing production time. Study current niche outliers and reverse-engineer proven packaging.

**Lock the thesis first.** One stealable lesson in one sentence. _If you can't write the thesis sentence, you don't have a video yet._ Use the page template in the format reference to lock: thesis → final title → thumbnail contradiction (3-5 words) → name-recognition mode (Founder Stories) → journey stage → FF angle.

Rule of both formats: **the click is earned by the packaging; the watch is earned by the non-obvious takeaway.**

---

## Universal video anatomy (both formats share this spine)

1. **Cold-open hook (first 15-30s).** Straight into tension. NO logo/intro card first. Personal Journey opens in 2nd person inside the viewer's pain ("You're stuck in a cushy but unfulfilling job"). Founder Story opens on a dramatic contradiction ("Pieter Levels built a startup empire by refusing to build a startup company").
2. **Open loop + stakes + who-it's-for bridge.** Name + credibility drop AFTER the hook. Tell them what they'll learn, why it matters to them right now, and the contract ("I won't sugar coat it"). Rotate the open frame every video (the cost / the payoff / the mirror question).
3. **[Intro card]** — channel intro plays here, not before the hook.
4. **Body beats** (format-specific):
   - Founder Story → the **4-beat Story Spine**: Story (incl. THE COST) → Philosophy Underneath → Practical Playbook → Identity Shift.
   - Personal Journey → the **teaching arc**: numbered Parts, each = a question → a reframe → tactics, mapped to the visual metaphor's stages.
5. **Identity shift.** Turn the lesson back on the viewer with 2-4 direct questions. Land on a motivating high note, not just information.
6. **CTA.** Point to a specific next FF asset (next video in the journey, Stay-Split-Commit quiz, runway calculator, Founder Frugal tools; soft Fractal AI mention only when automation naturally fits).

**Re-hook the viewer every ~60-90 seconds** — a new question, a stakes raise, a callback, a pattern interrupt. See [references/retention-and-packaging.md](./references/retention-and-packaging.md).

---

## Voice — the unique style (essentials; full doctrine + samples in [references/voice.md](./references/voice.md))

- **Open in the viewer's pain, in 2nd person, BEFORE you introduce yourself.** Identity drop comes after the emotional hook.
- **Short declarative sentences. Line breaks mid-thought** for spoken-word pacing. Pattern: Setup (2-3 lines) → pivot ("But" / "Then" / "And then") → one-line punch.
- **Specific vulnerability, never vague.** "Saved enough to buy a house, invested it instead. 20+ months to consistent cash flow." Not "it was hard."
- **Dry humor + deadpan callbacks** ("it's really not that cold once you're in"). Take the work seriously, not yourself.
- **Coin sticky terms** ("F*ck This money") and **contrarian aphorisms** ("Your plan B is someone else's plan A"; "The midwit waits for the perfect time. The founder jumps").
- **Specific reframes with real numbers** ("92% never even try"). Always cite real data; never fabricate a stat.
- **Visual language**: teal/cold = struggle, uncertainty, sacrifice; orange/warm = freedom, clarity, earned wisdom. Tag `[SCENE: ...]` (clip + camera + emotional function) and `[DOODLE: ...]` (Tim Urban-style; the doodle IS the teaching visual, not decoration). **Format split** (see storytelling.md): Personal Journey rides ONE sustained metaphor world; Founder Story is carried by REAL artifacts + re-enactment (metaphor only in doodles).

---

## Anti-AI-slop (BINDING — these are documented because they're frequent mistakes)

From the brand voice + writing skill. NEVER:
- "It's not just X, it's Y."
- "Here's why:" as a standalone line.
- "The truth is..." openers (note: "But the truth is?" as a rhetorical beat in the user's voice is fine — the banned version is the flat AI filler).
- Generic conclusions ("The bottom line?", "The lesson here?").
- Em dashes for pacing — the user's spoken style uses short lines and periods, not dashes. Max 1-2 in a whole script.
- Video throat-clearing: "In this video I'm going to...", "Let's dive in" (allowed ONCE, only as the deliberate post-intro opener), "Before we get started", "Make sure to like and subscribe" as filler.
- Vague hype, hustle jargon, corporate buzzwords, motivational-poster platitudes.

DO: direct confident statements, conversational rhythm, show-don't-tell, real specifics, earned levity.

---

## Production workflow

1. **Intake** (Phase 0). Confirm format, subject, journey stage.
2. **Lock thesis + packaging** using the format's page template — title candidates (5), final title, thumbnail contradiction. Pressure-test clickability against niche outliers.
2.5. **(Founder Stories) Source Gathering — REQUIRED.** Run the 3-pass sourcing ([references/source-gathering.md](./references/source-gathering.md)) → `sources.md` before outlining. Real artifacts carry Founder Stories; script them from memory and you'll fabricate.
3. **Outline the beats** for the chosen format. Pick the throughline (Personal Journey: the one metaphor world; Founder Story: the real-artifact spine + the philosophy).
4. **Draft in the user's voice** — read [references/voice.md](./references/voice.md), the format reference, and [references/storytelling.md](./references/storytelling.md) (Founder Freedom storytelling). Write the cold open last-ish once you know the payoff.
5. **Add `[SCENE]` / `[DOODLE]` direction** along the visual throughline (Personal Journey: teal→orange metaphor; Founder Story: real artifacts + re-enactment, ice/fire for tone). 8-16 scene tags; consolidate to ~10-15 reusable scenes.
6. **Self-check** against the verification checklist below + the retention checklist + anti-slop. Read it aloud; if a line doesn't sound like the user talking, cut it.
6.5. **(Founder Stories) Clip-Finding Pass — find supporting artifacts.** Once the draft passes self-check, map a real supporting artifact to each beat — a **founder video clip, a tweet, or a quote card**. For the **video clips**, hand the beats + source videos to the clip engine's clip finder: fan out one `clipengine.clips.find_in_video` subagent per source video **in parallel** (`clipengine.youtube.discover` first if you have no URLs; `clipengine.clips.render_windows` to cut files), then keep the highest-confidence clip per beat. Tweets come from the `sources.md` T-series and quote cards are styled here; the clip engine is **video-only**. **Add the chosen clip link inline into the single `script.md`** (a `> 🎬 CLIP: <source> <in–out> · conf · [▶ watch]` line under each founder-speaking beat) — never a separate `script-with-clips.md`; put the full per-beat candidate list in a sibling `clips.md` reference for the editor. **the clip engine owns the video brain — we don't rebuild it.** See [references/clip-finding.md](./references/clip-finding.md). _(Live; TDD at `<clip-engine-repo>/planning/TDDs/clip-finder.md`.)_
7. **Save** the single script (clip links inline) to `projects/founder-freedom-content/<YYYY-MM-DD-slug>/script.md` — one file; no separate `script-with-clips.md`. Mirror to Notion KBase if requested.
8. **Present to the user** for review (don't publish; this skill drafts).

---

## Verification checklist

- [ ] Thesis is ONE stealable sentence, written before the script
- [ ] Packaging locked before scripting (final title + 3-5 word thumbnail contradiction)
- [ ] Cold-open hook lands in the first 15-30s; no logo/intro-first
- [ ] Open loop set + who-it's-for bridge to a specific journey stage
- [ ] Re-hook / tension beat every ~60-90s
- [ ] THE COST is shown — real, specific, not glamorized
- [ ] Body follows the format spine (4-beat Story Spine, or numbered teaching Parts)
- [ ] Identity shift turns the lesson on the viewer (2-4 direct questions) + lands on a high note
- [ ] CTA points to ONE specific next FF asset
- [ ] Voice: 2nd-person pain-first open, short declaratives + line breaks, specific vulnerability, dry humor, a coined term / aphorism
- [ ] Teal→orange visual throughline; `[DOODLE]`s teach, not decorate
- [ ] No em dashes for pacing; zero AI-slop patterns
- [ ] Every stat/claim is real and sourced — no fabricated data
- [ ] (Founder Story) `sources.md` gathered via the 3-pass sourcing; every stat traces to it; **every on-screen quote verified verbatim against the raw primary source**; after the draft, the **Clip-Finding Pass** ([references/clip-finding.md](./references/clip-finding.md)) maps a supporting artifact — founder clip / tweet / quote card — to each beat (honor `none`; don't force a clip)

---

## Anti-patterns

| Avoid | Why | Instead |
|---|---|---|
| Logo/intro card before the hook | Kills the first-30s retention test | Cold-open straight into tension; intro card after |
| Scripting before packaging is locked | You build a video nobody clicks | Lock title + thumbnail + thesis first |
| Recapping a founder's biography | The founder isn't the point | Extract the stealable philosophy; founder is the vessel |
| Vague vulnerability ("it was hard") | No trust, no stakes | Specific numbers and real costs |
| Decorative b-roll / doodles | Wastes the visual; viewer tunes out | Doodles ARE the teaching illustration |
| Fabricating or rounding stats | Brand is data-honest; erodes trust | Cite real sources; if unknown, say so |
| Generic "subscribe for more" CTA | Dead air | One specific next asset in the founder journey |
| One open-loop frame reused every video | Predictable, stale | Rotate the open: cost / payoff / mirror |
| Writing it like an essay | It's spoken — reads stiff on camera | Short lines, spoken rhythm, read it aloud |
