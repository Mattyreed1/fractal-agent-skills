---
name: content-brief
description: Stage 2 of the Content Engine. Starts from a locked concept (angle, audience, format already chosen) and produces a detailed Content Context Brief — gathers all relevant context, proof, links, and resources needed to write the piece. Hook-agnostic — does NOT propose hooks, headlines, or copy. Use after content-ideation, or when the user hands over a concept directly. Triggers — 'write a brief', 'brief for', 'build the brief on', 'gather context for', 'content brief'.
license: MIT
metadata:
  version: 2.2.0
  created: 2026-04-20
  updated: 2026-06-17
  author: the Content Engine (refactored from v1 — now hook-agnostic and starts from a locked concept; v2.1 mandates Notion cross-links — original page for reposts, Case Studies DB entry for case studies; v2.2 makes locking the core claim through real deliberation a blocking first step, adds a Core Substance section for posts that hinge on a non-obvious mechanism, and gates handoff on core-claim resolution)
  domains: ['content', 'research', 'brief-writing']
---

# Content Brief

## Precondition: concept must be locked

A **concept is already locked** — angle, audience, format, and core claim are decided. Now you need to assemble every piece of context, proof, and reference required to write the post.

If the concept is not yet locked (the user has a topic but no chosen angle), use `content-ideation` first.

## What this skill does NOT do

- Does NOT propose hooks, headlines, or post copy. The brief is hook-agnostic — `content-hooks` and `content-scripting` mine the brief later. **Even if the locked concept names a "hook" or includes a punchy opening line, do NOT carry it into the brief: relabel it as the angle/frame, write zero draft opening copy, and NEVER populate the Notion `Hook` property — Stage 3 (`content-hooks`) owns that field. A model-swap test, a provocative question, a bold claim — these are angles, not hooks.**
- Does NOT pick the angle. The concept must already exist.
- Does NOT choose visuals as creative direction — only suggests what artifacts/diagrams the writer might want to reference.

## Inputs

- A locked concept: angle name, core claim, audience, format
- **Brand** (required): `fractal-ai` or `founder-freedom`. If not provided, ask once before starting.
- Optional: Notion page ID (from `content-ideation`) to update in place
- Optional: existing research, prior content, KG entities to fold in

If concept inputs are missing, ask ONE question or fetch from the Notion page if `content-ideation` already created one.

### Brand routing

| Brand | Folder | Use for |
|---|---|---|
| `fractal-ai` | `projects/fractal-ai-content/` | Fractal AI agency content — AI agents, Claude Code, the agent runtime, skill chaining, technical pieces |
| `founder-freedom` | `projects/founder-freedom-content/` | Founder Freedom content — solo founder lifestyle, freedom-of-time pieces |

If brand is ambiguous, ask. Never silently default.

## Steps

### 1. Confirm the concept AND lock the core claim (deliberate — don't just transcribe)

**This is the highest-leverage step in the whole skill, and the one most often skipped.** A brief is not just gathered context — its spine is a **locked core claim**, and when the post hinges on a non-obvious idea or mechanism, the **actual substance of the argument**. Gathering links around a vague claim produces a brief that *looks* complete and is hollow. The brief author owns the first draft of the thinking — not the user.

Repeat the concept back in one line:

> Concept I'm building the brief on: "{angle}" — claim: "{one-sentence claim}" — audience: "{persona}" — format: {LinkedIn post / thread / carousel / ...}. Right?

Then **pressure-test the core claim with the user BEFORE gathering anything**:

- **Take real positions. Don't outsource the thinking back to the user.** If the claim involves a mechanism ("here's how I'd do X with AI," "here's why Y works"), work out the *actual* mechanism in specific, concrete, un-fakeable terms — propose it, defend it, let the user correct it. "An AI agent handles it" is not a locked claim; "a trade-rep agent per discipline negotiates clashes within deterministic rules, escalating only the genuine conflicts" is. Asking "what do you think the angle is?" when this is your job is a failure.
- **Drill until it's specific.** Vague nouns ("a system," "the bridge," "with AI," "a framework") are the tell that the claim isn't locked yet. Keep going — and keep correcting your own draft when the user pushes back — until the claim names the real thing and survives a "does this actually ring true?" challenge.
- **Match the format's capacity.** A 60–90s video or a single post carries ONE compressed idea, not a full architecture. Lock the *compressed* claim, and when a bigger idea surfaces that won't fit, explicitly park it as a separate content seed (add it to `projects/<brand>-content/_strategy/`) instead of cramming it in.
- **Surface and resolve missing info now.** List every fact, number, consent, or decision the post depends on. Resolve anything that affects the **core claim** before handoff; the rest become `[NEEDS INPUT]`. **Never re-ask something the user already answered** — check the current conversation, the existing Notion page, and the brief first. Re-asking answered questions erodes trust as fast as guessing does.

Don't proceed to retrieval until the core claim is genuinely locked. If the user says "you decide," record the delegated decision and proceed.

### 2. Full retrieval cascade

This is the heavy context pass — go wide. Run in parallel where possible:

1. **Knowledge Graph** — `bash "$CLAUDE_PROJECT_DIR/scripts/kg-search.sh" "<topic>"` and follow up on connected entities
2. **Memory files** — grep `memory/` for related decisions, prior posts, learnings, autopsies
3. **Notion — related pages** — `mcp__mr-notion__API-post-search` for related projects, research docs, prior content
4. **Notion — Quotes DB** (`<QUOTES_DB_ID>`) — query for quotes whose topic/tags overlap the concept. Pull 2–4 of the most resonant.
5. **Notion — Quotable People DB** (`<QUOTABLE_PEOPLE_DB_ID>`) — scan for figures whose worldview maps to the concept. If the Quotes DB didn't already cover them, surface 1–2 candidates the writer can quote from public material (link the source — never fabricate the quote).
6. **Projects folder** — `ls projects/` and skim relevant subdirs for artifacts, code, screenshots, metrics
7. **Prior briefs** — `ls projects/fractal-ai-content/ projects/founder-freedom-content/` for adjacent pieces; note any overlap
8. **Source links — REQUIRED cross-links (never skip these):**
   - **If this is a REPOST** of an existing post: find the original page in the Notion **Content DB** AND its live **Post URL** property; link BOTH in Resources & Links, and state exactly what's changing (new hook, new format, or both).
   - **If this is a CASE STUDY or cites one:** find the source entry in the Notion **Case Studies DB** (`<CASE_STUDIES_DB_ID>`) and link it; also link the client **project folder** and the client/company **KG entity**.
   - Link every related prior **Content DB** page, **Meetings DB** page, research doc, lead-magnet asset, and KG entity you reference, **by URL**. A brief that names a Notion page without linking it is incomplete.
9. **External research** — only if the brief needs framing/data the user doesn't already have. Invoke the `research` skill (Perplexity).

Always run the `notion` skill setup (fetch instructions page `<INSTRUCTIONS_PAGE_ID>` FIRST) before querying the Quotes / Quotable People DBs so you have the current schema and field names.

Pull every concrete artifact you find: data points, code snippets, metrics, screenshots, links, quotes from past conversations, KG entries.

### 3. Write the brief

Save to `projects/<brand-content>/YYYY-MM-DD-<slug>/brief.md` where `<brand-content>` is `fractal-ai-content` or `founder-freedom-content`. Create the per-piece folder if missing — all downstream artifacts (hooks, script drafts, visuals, packaging) live alongside the brief in the same `YYYY-MM-DD-<slug>/` directory.

Use this exact format:

```markdown
# Content Context Brief — {Title}

**Date:** YYYY-MM-DD
**Concept (locked):** {angle name}
**Format:** {LinkedIn Post | Thread | Carousel | Blog | ...}
**Status:** Draft

## Core Claim
[one sentence — copied from the locked concept]

## Why This Matters
[2-3 sentences — why this audience should care RIGHT NOW. Tie to a live shift, pain, or trend.]

## Core Substance (INCLUDE when the post hinges on a non-obvious claim or mechanism — else omit)
The actual argument, worked out in concrete, un-fakeable terms — this is what `content-scripting` turns into the piece. It is substance, NOT a hook (no opening copy). Required whenever the post's value is a "how" or "why" that had to be reasoned out (a technical approach, a framework, a contrarian mechanism). Capture:
- The locked claim's mechanism, specifically (named tools/steps/structure — not "with AI").
- The compressed version that fits the format (e.g. the ~3-sentence on-camera beat), separated from the deeper version.
- What is deliberately LEFT OUT and parked as a separate seed (so the next stage doesn't try to cram it).
- For video: a short narrative beat skeleton (hook → … → lesson) as structure for scripting — NOT the script, NOT the hooks.

## Target Audience
[specific persona — e.g. "solo founders building AI agents," not "entrepreneurs"]

## Proof & Artifacts
Concrete evidence the writer can cite. Each item should be self-contained — the writer should not need to re-research it.

- [Artifact #1: data point with source / metric with date / code snippet with file path / screenshot path / quote with attribution]
- [Artifact #2: ...]
- [Artifact #3: ...]

## Relevant Quotes
2–4 quotes that resonate with the concept. The writer can use these for openings, payoff lines, or punctuation.

Pull from (in priority order):
1. **Notion Quotes DB** (`<QUOTES_DB_ID>`) — existing curated quotes
2. **Notion Quotable People DB** (`<QUOTABLE_PEOPLE_DB_ID>`) — figures whose worldview maps to the concept; only use a quote you can attribute to a real public source

Format each as:

- "{quote}" — {Person}, {Source/Year}. [Notion: {URL or DB record link}]
  - Why it fits: {one phrase tying it to the concept}

Never fabricate a quote. If nothing in either DB fits, leave the section as `[NEEDS INPUT: no resonant quote found in DBs]` rather than inventing one.

## Resources & Links
Everything the writer might want to reference. Links + brief description of what each contains. **The relevant Notion page links are REQUIRED, not optional:**

- **Original content page (REPOSTS):** [Notion Content DB page URL] + the live **Post URL** — and what's changing (new hook / new format / both).
- **Source case study (CASE STUDIES):** [Notion Case Studies DB entry URL] — the documented build + its proprietary number.
- **Client project / KG:** [project folder path] · [company/person KG entity link].
- **Lead-magnet asset:** [GitHub / Notion landing / Gumroad URL] if the piece has one.
- [other link #N] — [what it is, what's useful in it]

If a referenced page exists, link it. A brief that names a page without its link is incomplete.

## Related Prior Work
Past content, projects, or KG entries that overlap or build on this. **Link each one (Notion page URL, Drive link, or repo path) — never reference a prior piece without its link.**

- [prior brief or post + URL] — [how it relates / how this differs]
- [project or KG entity + link] — [...]

## Lead Magnet
The asset that will accompany this content. Name + format + status.

[e.g. "Agent Memory Starter Kit — GitHub repo with templates and schemas. Status: needs to be built." OR `[NEEDS INPUT]` if undecided.]

## Visual Suggestions
What artifacts/diagrams could support the piece. Hook-agnostic — describe the *substance* to render, not the headline framing.

- [diagram/graphic #1: specific description of what to show]
- [diagram/graphic #2]

## Open Questions / Gaps
Anything still missing that the writer or the user needs to fill in.

- [NEEDS INPUT: specific question]

## Raw Context
Paste verbatim excerpts the writer should mine — KG entries, memory snippets, conversation transcripts, research output. Long is fine; this is reference material.

[paste here]
```

### 4. Push to Notion

If `content-ideation` created a Notion page, update that page in place — append the brief sections under the existing Concept block. Otherwise create a new Content DB page (use the `notion` skill, fetch instructions page `<INSTRUCTIONS_PAGE_ID>` FIRST).

Stage stays at `Idea` until the brief is approved.

### 5. Submit for the user's approval

Post a short summary in chat:

- Notion page URL
- One-line summary of the brief
- Flagged gaps (anything `[NEEDS INPUT]`)
- Lead magnet status

Wait for approval or revisions.

### 6. On approval

- Update Notion **Stage:** `Idea` → `On Deck`
- **Gate (blocking):** do NOT hand off to `content-hooks` until the **core claim is locked** and every `[NEEDS INPUT]` that affects the core claim (not merely nice-to-haves like an optional lead magnet) is resolved. A brief whose central argument still has an open hole is not ready for Stage 3 — finish the deliberation first.
- Hand off: "Brief approved. Next: `content-hooks`. Notion: {url}"

## Edge Cases

- **Concept not yet locked**: stop. Tell the user to run `content-ideation` first or supply the missing pieces (angle, claim, audience, format).
- **Missing proof**: flag every gap as `[NEEDS INPUT: specific question]`. Never fabricate numbers, quotes, or case studies.
- **Topic overlaps existing brief**: grep `projects/fractal-ai-content/ projects/founder-freedom-content/` first (look for `*/brief.md`). If overlap, note it under "Related Prior Work" and clarify the differentiation in "Why This Matters."
- **KG/memory empty**: fine — use Perplexity via the `research` skill. Note in the brief that proof is external-sourced rather than from the user's own system.
- **Notion update fails**: keep the markdown file; tell the user the Notion step failed; don't retry silently.

## Handoff

Brief approved → Stage=On Deck → invoke `content-hooks`.

Brief can also be consumed standalone (without going through the full pipeline) by:
- `writing` — for hooks, headlines, or full post drafts
- `lead-magnet` — to build the lead magnet artifact named in the brief
- `social-canvas` — to render the visual suggestions
