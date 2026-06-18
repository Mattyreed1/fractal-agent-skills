# Clip-Finding Pass — supporting artifacts per beat (Founder Stories)

After the script draft is written, this pass finds the **real supporting artifact for each beat** and writes the clip link **directly into the single `script.md`** for the editor to pick from. There is one script file — `script.md` — never a separate `script-with-clips.md`.

> **Engine:** the **video-clip** part of this pass calls **the clip engine's** script-driven clip finder (shipped — an internal PR). We do **not** rebuild transcript→chunk→match→render in the Content Engine. the clip engine owns the video brain; this skill is the Founder-Freedom *adapter + caller* and owns the non-video artifacts (tweets, quote cards).
>
> **STATUS — LIVE.** The capability is built and validated. Tools (all stateless, no `run_id`): `clipengine.youtube.discover`, `clipengine.clips.find_in_video`, `clipengine.clips.render_windows`. TDD: [`<clip-engine-repo>/planning/TDDs/clip-finder.md`](#clip-engine-tdd).

---

## Why this exists

A Founder Story is the host's narration illustrated with **real footage of the subject** (the founder) speaking — across several different interviews/talks — plus tweets and quote cards. The editor needs, per beat: the right clip (which source video + exact in/out + the verbatim quote), or a tweet, or a quote card, or an honest "no good evidence." Doing this by hand across 5–8 hours of source video is the bottleneck this pass removes.

---

## Artifact-type routing — who owns what

Each beat routes to ONE artifact type. **the clip engine only finds video clips.** The other types stay with this skill:

| Artifact | Owner | Use when | Tag in script |
|---|---|---|---|
| **Founder video clip** | **the clip engine** (`clipengine.clips.find_in_video`) | The subject says it on camera and it lands better in their own voice/face. | `[CLIP: <source> @ts — "quote"]` |
| **Tweet** | **this skill** (from the T-series in `sources.md`) | The strongest evidence is a real post that reads better as an on-screen tweet. | `[CLIP: tweet — "…"]` |
| **Quote card** | **this skill** (styled text) | The quote is real but from text/audio that won't look good as footage (blog, audio pod, book). | `[TEXT:]` / quote-card callout |
| **Scene (re-enactment)** | this skill | No real artifact; we dramatize. | `[SCENE: …]` |
| **Doodle** | this skill | An abstract idea taught with a diagram. | `[DOODLE: …]` |
| **None** | — | No supporting evidence. Rewrite the beat or cut it — don't force a clip. | — |

So the decision flow per beat: **want the founder on camera? → send to the clip engine.** Tweet / quote card / scene / doodle are decided and produced here and are **not** sent to the clip engine. If the clip engine returns `none` for a beat, fall back to a tweet/quote-card/scene or rewrite the beat — don't force footage.

---

## The two video jobs the clip engine does

1. **Locate / verify** — for beats that already carry a hand-picked `[CLIP: <source> @ts — "quote"]` tag, snap the exact in/out and confirm the quote is verbatim (the `existingTag` fast-path).
2. **Discover** — for beats that want footage but have no clip yet, search all source transcripts and surface the best candidate(s) of the founder in their own words, with a confidence score.

---

## How to run it

### 1. Build `beats[]` from the script

Decompose `script.md` into beats. One beat ≈ one narration unit that wants footage. Send **only the beats that want a founder video clip** (per the routing table). FF tag → contract field:

| FF script | → `beat` field |
|---|---|
| narration line + its section header | `narration`, `section` |
| an editorial note on what the beat must prove | `intent` |
| `[CLIP: Lex #440 @00:02:14 — "I don't use VC funding…"]` | `existingTag: { sourceId:"lex440", approxTime:"00:02:14", quote:"…" }` |
| a beat that must be the founder speaking (not the host/interviewer) | `mustQuoteSubject: true` |

(No `preferredArtifact` / `tweetPool` — the engine is video-only now; tweets and quote cards never go to it.)

### 2. Assemble `sources[]` from `sources.md`

Each on-camera video in `sources.md`: `{ id, title, url: "<YouTube URL>", speaker: "<founder name>" }`. The `speaker` disambiguates multi-guest pods. **If you don't have the source URLs**, hand the clip engine the founder's name instead and let it discover them (next step).

### 3. (Optional) Discover sources — when you don't have URLs

If `sources.md` has no on-camera video URLs but you know the founder, call `clipengine.youtube.discover({ subject: "<founder>", count: 10 })` → up to 10 longform videos. Review the shortlist with the user before searching them.

### 4. Find — fan out ONE subagent per source video, **in parallel**

This is normative: **spawn one subagent per source video and run them concurrently — never a sequential loop.** Each subagent makes a single `clipengine.clips.find_in_video({ source, beats, config: { minSec: 6, maxSec: 45, candidatesPerBeat: 2 } })` call for its one video and returns that video's per-beat candidates (exact in/out, verbatim quote, confidence 0–1, and a free YouTube deep link). A failed/transcript-less video returns empty and does **not** block the others.

### 5. Synthesize — pick the best clip per beat across videos

For each beat, take the highest-confidence candidate across all videos. Keep it if it clears ~0.55; otherwise the beat is `none`. (the clip engine exposes `synthesizeDecisions` for this argmax, or just compare the confidences yourself.) Every candidate already carries a clickable `youtubeUrl` deep link — that alone is enough for the editor to pull footage.

### 6. (Optional) Render — only the winners, only on request

To hand the editor actual clip files, call `clipengine.clips.render_windows({ windows: [{ id, sourceUrl, startSec, endSec }], config: { quality: "720p" } })` on the chosen winners → playable clip URLs + thumbnails. Rendering costs credits, so default to map-only (deep links) and render only after the user approves the selection.

### 7. Add the clip links to `script.md` + present for selection

**The deliverable is ONE script file — `script.md` — with the clip links added directly inline.** Under each founder-speaking beat, insert the chosen clip as a blockquote line directly beneath it, e.g.:

```
> 🎬 **CLIP:** `lex440` 00:02:26–00:02:34 · conf 1.00 · [▶ watch](https://youtu.be/oFtjKbXKqbg?t=146)
```

Do **not** spin off a second annotated script (no `script-with-clips.md`). Write the full per-beat candidate list (all runners-up, for editor swap-outs) to a sibling **`clips.md`** — a selection-reference data file, not a script. (If the user prefers literally one file, append that candidate list as a `## Clip alternates` section at the bottom of `script.md` instead.) Then present `script.md` to the user/the editor and flag every `none` beat — those need a rewrite, a tweet/quote-card, or a cut.

---

## If inputs are missing — the clip engine will ask

You don't have to hand a perfect package. The clip engine clip-finder agent gathers what it needs (see `~/Code/the clip engine/HEADLESS.md` → *Script-Driven Clip Finder*): no script → it asks for one; a script but no videos → it asks for URLs or offers to discover them from the founder's name; before rendering → it confirms (cost). Hand it what you have; it fills the gaps conversationally.

---

## Where this sits in the production workflow

It runs **after** the script draft and `[SCENE]/[DOODLE]` pass, and **before** final hand-off — see the numbered workflow in `SKILL.md`. It does **not** replace Phase 0.5 Source Gathering: source-gathering finds *which* videos and key artifacts exist (so we can write a sourced script); this pass then does the systematic, exact-timestamp clip mapping over the full transcripts of those sources.

## Anti-patterns

| Avoid | Why | Instead |
|---|---|---|
| Rebuilding transcript/clip logic in the Content Engine | the clip engine already owns the video brain; duplication drifts | Call `clipengine.clips.find_in_video` |
| Running the source videos sequentially | Wall-clock = sum of all videos; one slow transcript blocks the rest | Fan out one subagent per video, in parallel |
| Sending tweet / quote-card / `[SCENE]/[DOODLE]` beats to the clip engine | The engine is video-only; those are produced here | Only send beats wanting a founder video clip |
| Forcing a clip onto every beat | Irrelevant footage erodes trust; brand is data-honest | Honor `none` — rewrite, use a tweet/quote-card, or cut |
| Rendering every candidate up front | Render costs credits; most candidates get cut in review | Map-only first (deep links); render only approved winners |
| Using a clip whose quote isn't verbatim | Founder Stories require verbatim on-screen quotes | Verify the returned `quote` against the raw source before locking |
| Spinning off a `script-with-clips.md` (a 2nd annotated script) | Two script files drift; nobody knows which is canonical | ONE script — `script.md` with clip links inline; runner-ups in a sibling `clips.md` data file |
