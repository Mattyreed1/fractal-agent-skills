---
name: content-pipeline
description: Master orchestrator for the Content Engine. Routes content pieces through 7 stages — ideation, brief, hooks, scripting, visuals, packaging, publish — by reading the Notion Content DB Stage field and dispatching to the right sub-skill, with an optional content-strategy planning step (Stage 0) before ideation. Read this to determine which stage a content piece is at and which sub-skill to execute next.
license: MIT
metadata:
  version: 3.1.0
  created: 2026-03-27
  updated: 2026-06-16
  author: content-orchestrator
  domains: ['content', 'orchestration', 'routing']
---

# Content Pipeline — Master Orchestrator

## Overview

Routes content pieces through 7 stages. Each stage is its own skill. v3 splits ideation (diverge/converge) from brief (concept → context bundle).

1. `content-ideation`
2. `content-brief`
3. `content-hooks`
4. `content-scripting`
5. `content-visuals`
6. `content-packaging`
7. `content-publish`

**Optional Stage 0 — `content-strategy`:** when the user is planning at the portfolio / calendar level (pillars, editorial calendar, channel mix, founder positioning) rather than handing over a single seed, run `content-strategy` FIRST. It produces the pillars + a dated editorial calendar and **emits seeds into Stage 1 (`content-ideation`)**. It is optional and sits *outside* the per-piece flow — skip it whenever the user hands a single seed or a locked concept and go straight to ideation/brief. Currently **EA-only** (runs on the user's Mac); not yet synced to the remote workspaces (sync via `skill-translate` before any fleet agent can run it).

**Specialized entry — `content-case-study`:** for a piece with `Type = Case Study`, use `content-case-study` in place of Stages 1-2 (ideation + brief). It turns a REAL client engagement (a construction GC / a crypto OTC desk / a hospitality brand) into a structured case-study brief with one proprietary number, then hands to `content-hooks` (Stage 3). This is the proof-of-work artifact at the center of the 2026 LinkedIn authority strategy.

## How to use

1. Identify the content piece (Notion Content DB page or board task)
2. **Determine brand** — `fractal-ai` or `founder-freedom`. Check the Notion page's Brand property if present; otherwise ask the user once and carry it through every downstream skill.
3. Read the Notion **Stage** property
4. Execute the matching skill below — pass brand to it

## Brand routing

Every content piece lives under one of two brand buckets on disk:

| Brand | Folder | Use for |
|---|---|---|
| `fractal-ai` | `projects/fractal-ai-content/<YYYY-MM-DD-slug>/` | Fractal AI agency content — AI agents, Claude Code, the agent runtime, skill chaining, technical pieces |
| `founder-freedom` | `projects/founder-freedom-content/<YYYY-MM-DD-slug>/` | Founder Freedom content — solo founder lifestyle, freedom-of-time pieces |

All artifacts for one piece (brief, hooks, script drafts, visuals, packaging notes) sit in the same `<YYYY-MM-DD-slug>/` folder. Never split artifacts across folders by type.

If the brand isn't already clear from the Notion page or the user's request, **ask once** before invoking any sub-skill. Never silently default.

## Routing table

| Notion Stage | Current state | Execute Skill | Who |
|--------------|---------------|---------------|-----|
| *(no page)* | the user is planning at portfolio/calendar level — no single seed yet | `content-strategy` (optional Stage 0) → emits seeds into Stage 1 | EA / CC |
| *(no page)* | the user gave a fresh seed (no locked angle) | `content-ideation` (Stage 1) | CC (or any agent they delegated to) |
| *(no page)* | the user handed over a locked concept | `content-brief` (Stage 2) | The agent they handed it to |
| Idea | Concept locked, brief not yet written | `content-brief` (Stage 2) | Brief author |
| Idea | Brief drafted, awaiting CO eval | `content-brief` (Stage 2) | Brief author |
| On Deck | Brief approved, needs hooks | `content-hooks` (Stage 3) | CC |
| Title/Thumb/Hook | Hooks posted, the user hasn't picked yet — content-hooks owns the pick/grade interaction | `content-hooks` (Stage 3) | CC |
| Title/Thumb/Hook | Hook chosen → write the post | `content-scripting` (Stage 4) | CC |
| Scripting | Draft posted, awaiting the user's approval | `content-scripting` (Stage 4) | CC |
| Visual Editing | Visuals being created or awaiting the user's approval | `content-visuals` (Stage 5) | CC |
| Packaging/Posting | Lead magnet + Tally + landing page + final assembly | `content-packaging` (Stage 6) | CO |
| Published | Live — collect metrics at 7 days | `content-publish` (Stage 7) | CO + CC |

## Auto-route steps

```
1. Query Notion: GET content page → read Stage property
2. Match Stage to skill in table above
3. Read that skill's SKILL.md
4. Check content-brief/example.md for pattern reference (if present)
5. Execute
```

## Stale content check

If any piece sits at a stage >14 days, CO flags it in the #content thread and escalates to the user.

## Skill layout

Each stage is its own skill at `~/.claude/skills/<name>/SKILL.md` (+ an optional `example.md`). A single agent can run the whole pipeline, or you can split stages across a multi-agent fleet — the "Who" column in the routing table above is a suggested division of labor (an orchestrator role vs. a content-creator role), not a requirement.

`content-strategy` (the optional Stage 0) sits *outside* the per-piece flow: it does portfolio/calendar planning and emits seeds into Stage 1. Skip it whenever you hand over a single seed or a locked concept.
