---
name: content-ideation
description: Stage 1 of the Content Engine. Diverge then converge on a content seed — generate multiple distinct angles, evaluate them, narrow to one (or a few) winning concept(s). Does NOT write the full brief (that's content-brief). Use when the user has a topic / pain / observation / vague "we should post about X" and the angle is not yet locked.
license: MIT
metadata:
  version: 3.0.0
  created: 2026-03-27
  updated: 2026-04-28
  author: content-orchestrator
  domains: ['content', 'ideation', 'divergence-convergence']
---

# Content Ideation — Divergence & Convergence

## Trigger

the user hands any agent a **seed** — topic, pain point, observation, recent learning, or vague "we should post about X." Angle not yet locked.

If concept is already locked (the user has framing, audience, takeaway), skip this skill and run `content-brief` directly.

## Who

The agent the user told. CC primary, but any agent can run it.

## What this skill does NOT do

- Does NOT write the full Content Context Brief — that's `content-brief`.
- Does NOT propose hooks, headlines, or copy. An angle's framing (a model-swap test, a provocative question, a bold claim) is NOT a hook — name it as the angle, never write opening copy, and never fill the Notion `Hook` property here. That's Stage 3 (`content-hooks`).
- Does NOT exhaustively gather proof — only enough context to inform divergence.

## Inputs

- A seed: topic / pain / observation / "we should post about X"
- Optional constraints (platform, audience, business goal)

## Steps

### 1. Clarification gate (BLOCKING)

Before any context probe or divergence, ask the user the questions needed to understand the seed. Hard-blocking — do not skip, do not assume.

Three required dimensions:

1. **What is it?** — articulate the topic / observation / pain in one or two sentences.
2. **Who is it for?** — specific audience (e.g. "solo founders building agents," "n8n operators"). Not "entrepreneurs."
3. **What's the purpose?** — drive lead-magnet sign-ups, build authority, change someone's mind, recruit, sell, mark a position. Specific.

Optional spark questions if needed: what triggered this? unfair advantage? stakes/urgency? contrarian angle? format constraints?

Ask via Discord #content thread (or chat with the user). Concise, batched.

If the user says "you decide" on a dimension, record the delegated choice and continue.

Do not proceed to step 2 until the three dimensions are answered.

### 2. Lightweight context probe (≤2 minutes)

Just enough to inform divergence — not the full retrieval cascade.

- KG: `cd <your-board-dir> && npx convex run kg:search '{"query":"<seed>"}'`
- Quick scan of memory (MEMORY.md + memory/) and any prior content briefs in the project
- Skim recent board activity on the content project (`<your-board-project-id>`) for adjacent pieces

Stop as soon as you have enough to generate distinct angles.

### 3. Divergence — generate 5–7 distinct angles

Each angle is a different **way into the seed** — different framing, audience, or claim. Numbered list. Each entry has:

- **Angle name** (3–6 words)
- **Core claim** (one sentence — what the reader walks away believing)
- **Audience** (specific persona)
- **Format hypothesis** (LinkedIn post / thread / carousel / blog)
- **Why this angle works** (one phrase: novelty, contrarian, proof-rich, timely, etc.)

Push for genuine variety — contrarian, technical-deep, story-driven, framework, prediction, autopsy, hot-take. If two angles collapse, replace one.

### 4. Convergence — evaluate and rank

Score each angle 1–5 on:

- **Originality** — said-to-death or fresh?
- **Proof availability** — can the user back it up from their own work / KG / projects?
- **Audience fit** — does it land with the people they want to reach?
- **Business fit** — pulls toward Fractal AI / agent ops / lead magnets that exist or could be built?

Compute total. Recommend top 1–3.

### 5. the user picks

Post the ranked finalists in the Discord #content thread (`your-content-channel-id`) with one-sentence rationale each. Ask him to pick one (or "you decide").

- "you decide" → take the top-ranked angle, note the choice was delegated
- He picks a different angle from the rejected list → fine, use it
- None fit → diverge again with new constraints

### 6. Save the chosen concept to Notion

Create a Notion Content DB page (DB id: `<CONTENT_DB_ID>`). Use the `notion` skill (mode: `append`) to write the concept block.

Notion page properties:
- **Name:** angle name (concise, descriptive)
- **Stage:** `Idea`
- **the agent fleet:** ☑️
- **Type:** matches format hypothesis
- **Overview:** core claim (one sentence)
- **Hook:** leave EMPTY — never set the `Hook` property at ideation; `content-hooks` (Stage 3) fills it

Append to the page body:

```markdown
## Concept

**Angle:** [name]
**Core Claim:** [one sentence]
**Audience:** [persona]
**Format:** [LinkedIn post / thread / carousel / ...]

## Considered & Rejected

- [angle 2] — [one-line why not]
- [angle 3] — [one-line why not]
```

### 7. Hand off to `content-brief`

Create board task and message:

1. **board task** (project `<your-board-project-id>`):
   - title: `Content Context Brief — {angle name}`
   - assignedTo: the agent who will write the brief (yourself, or the agent the user assigns)
   - evaluator: `content-orchestrator`
   - priority: P2
   - description: Notion page URL + locked concept block

2. **board message**:
   - toAgent: brief author
   - content: `Concept locked: "{angle}". Brief next. Read content-brief skill. Notion: {url}.`

Stage stays at `Idea` — `content-brief` advances it to `On Deck` when the brief is approved.

## Edge cases

- **Seed is already a locked concept** (audience, claim, format clear): skip ideation, run `content-brief`. Tell the user.
- **Seed too vague to diverge from**: ask ONE clarifying question (audience? business goal?) before generating angles.
- **All angles collapse into one idea**: seed is too narrow. Confirm with the user — maybe `content-brief` is what's needed.
- **KG/memory empty**: fine — diverge from first principles + the seed alone.
- **Notion API fails**: retry once; if still fails, save concept to workspace file (`projects/<brand-content>/YYYY-MM-DD-<slug>/idea.md` where `<brand-content>` is `fractal-ai-content` or `founder-freedom-content` — ask the user if unclear) and notify CO via board.

## Output

- Notion page at Stage=`Idea` with locked concept + rejected alternatives
- board task `Content Context Brief — {angle name}` assigned to brief author, evaluator=CO
- Discord thread updated with the ranked angles + the user's pick
