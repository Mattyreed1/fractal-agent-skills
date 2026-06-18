---
name: content-strategy
description: The strategy layer ABOVE the Content Engine. Defines content pillars, editorial calendar, channel mix, audience, cadence, and founder thought-leadership positioning per brand (Fractal AI / Founder Freedom), then feeds seeds down into content-ideation. Use for quarterly/monthly content planning, "what should we be posting about", "build a content calendar", "refresh our content pillars", "what's our channel mix", "content strategy for [brand]", "plan a launch campaign". Does NOT generate the angle for one piece (that's content-ideation), write copy/hooks (content-hooks/content-scripting), or route a single piece through stages (content-pipeline).
license: MIT
metadata:
  version: 1.0.0
  created: 2026-06-16
  updated: 2026-06-16
  author: content-orchestrator
  adapted_from: "msitarzewski/agency-agents — marketing/marketing-social-media-strategist.md (MIT License)"
  domains: ['content', 'strategy', 'editorial-calendar', 'thought-leadership', 'channel-mix']
---

# Content Strategy — The Layer Above the Engine

## Where this sits

content-strategy is the **planning layer** that sits on top of the per-piece Content Engine. It answers **what themes, on which channels, how often, for whom, and why** — never how to write any single post.

```
content-strategy   ← pillars · editorial calendar · channel mix · positioning   (THIS skill — quarter / month)
      │ emits seeds + a calendar slot
      ▼
content-ideation   ← angle for one seed
content-brief → content-hooks → content-scripting → content-visuals → content-packaging → content-publish
content-metrics    ← performance feeds back UP into the next strategy refresh
```

If the angle for a single piece is what's needed, skip this skill and run `content-ideation`. If a piece already exists and just needs to move stages, run `content-pipeline`.

## Trigger

the user is thinking at the **portfolio / calendar level**, not the single-post level:
- "What should we be posting about this month/quarter?"
- "Build me a content calendar for [brand]."
- "Refresh our content pillars."
- "What's our channel mix / where should this brand show up?"
- "Plan the content campaign around [launch / event]."
- "Is our content actually pointed at the right audience?"

## Who

The agent the user told. CC primary, but any agent can run it. Strategy output is reviewed by the user before any piece is greenlit into ideation.

## Brand gate (BLOCKING)

Content is brand-routed — this is a HARD RULE, no exceptions. Before any planning, confirm which brand via the **AskUserQuestion** tool. Never assume.

| Brand | Folder | Audience (default) | Primary channel |
|-------|--------|--------------------|-----------------|
| **Fractal AI** | `projects/fractal-ai-content/` | Founders/operators buying AI agency + automation outcomes | LinkedIn |
| **Founder Freedom** | `projects/founder-freedom-content/` | Founders building lean/solo, founder-journey audience | LinkedIn + YouTube |
| **Both / portfolio** | both folders | — | produce a separate strategy per brand |

Strategy deliverables live at `projects/<brand>-content/_strategy/` (e.g. `projects/founder-freedom-content/_strategy/2026-Q3-strategy.md` and a living `pillars.md`). Per-piece work stays under `projects/<brand>-content/<slug>/` as usual.

## What this skill does NOT do

- Does NOT generate the angle for a single seed — that's `content-ideation`.
- Does NOT write hooks, titles, or copy — that's `content-hooks` / `content-scripting` / `writing`.
- Does NOT route a piece through stages or touch the Notion Stage field — that's `content-pipeline`.
- Does NOT report on past performance — that's `content-metrics` (but it CONSUMES those metrics as input).

## Inputs

- **Brand** (resolved at the gate above).
- **Horizon**: month, quarter, or campaign window.
- **Goal**: the business outcome this content serves (inbound leads, authority, audience growth, launch support, recruiting).
- Optional: latest `content-metrics` pull, current pillars (if any exist in `_strategy/pillars.md`), known launches/events on the calendar, competitor set.

## Steps

### 1. Brand + horizon + goal gate (BLOCKING)
Resolve brand (AskUserQuestion), the planning horizon, and the single primary business goal. One goal anchors the whole plan — if the user names several, ask which is primary.

### 2. Ground in reality (don't plan blind)
- Read `projects/<brand>-content/_strategy/pillars.md` if it exists.
- Pull recent performance via `content-metrics` (what's actually landing vs. flopping).
- Note upcoming launches/events that content should support.
- For a fresh brand with no history, scan 5–10 recent published pieces and 2–3 competitors to infer the starting position.

### 3. Define / refresh content pillars (3–5)
Each pillar sits at the **intersection of the user's genuine expertise and the audience's real need** — not generic topics. A pillar is defensible and repeatable. For each: name, one-line thesis, who it's for, the outcome it drives, and example seed directions (NOT hooks). Store in `_strategy/pillars.md`.

### 4. Set channel mix + content cascade
- **Primary channel** carries the original (LinkedIn for both brands; Founder Freedom also runs YouTube long-form via `youtube-script`).
- **Cascade**: primary piece → adapted derivatives (LinkedIn post → X thread, carousel, YouTube short, newsletter). Define which pillars cascade where.
- Set **cadence per channel** (e.g. LinkedIn 3–4×/week, YouTube 1×/week) calibrated to what the user can sustain — sustainable beats ambitious.

### 5. Build the editorial calendar
Map pillars × cadence × horizon into dated slots. Each slot = {date, channel, pillar, seed direction, goal tag}. Front-load nothing you can't staff. Leave ~20% open for reactive/timely content. Output as a table in `_strategy/<horizon>-strategy.md`.

### 6. Set the founder thought-leadership thread
the user is the founder voice. Across the calendar, ensure a through-line that builds their authority: recurring POV, a few "planted flag" opinion pieces per horizon, and tie-ins to speaking/podcast/inbound opportunities. Authority compounds; one-off posts don't.

### 7. Define success metrics + review cadence
Pick 3–5 metrics tied to the goal (see framework below). Set a review date (default: end of horizon) where `content-metrics` feeds back into step 2 of the next refresh. State the **flip condition** — what result would make us change pillars or channel mix.

### 8. Hand off
For each calendar slot the user greenlights, emit a **seed** into `content-ideation` (topic + pillar + audience + goal + channel). Strategy stops at the seed; ideation takes the angle from there.

## Frameworks

### Pillar test
A real pillar answers yes to all four: (1) Does the user have earned credibility here? (2) Does the target audience actively want it? (3) Can we produce it repeatedly without burning out? (4) Does it ladder to the business goal? If any answer is no, it's a topic, not a pillar.

### Channel cascade (default)
- **LinkedIn (primary, both brands):** the strategic home. Original long-form posts, carousels, founder POV. No external links in body (link in comments).
- **YouTube (Founder Freedom):** long-form founder-journey / founder-story via `youtube-script`; clips cascade back to LinkedIn/X.
- **X / other:** adapted derivatives of the LinkedIn original, never raw cross-posts.
- Rule: **one idea, platform-native everywhere** — adapt voice and format per platform, never paste identical copy across channels.

### Thought-leadership positioning
- Consistent, recognizable POV anchored in the pillars.
- A few defensible "planted flag" opinion pieces each horizon (acknowledge the counterargument, then hold the line).
- Leverage social proof for earned opportunities (podcasts, speaking, press).

### Success metrics (pick 3–5, tie to goal)
- **Engagement rate:** LinkedIn ~3%+ on brand/company posts, ~5%+ on founder personal posts (calibrate to actuals from `content-metrics`).
- **Audience growth:** target monthly % growth on the primary channel.
- **Inbound signal:** leads / DMs / replies / recruiter or partner interest — the outcome, not vanity likes.
- **Consistency:** % of planned calendar slots actually shipped (a strategy that doesn't ship is fiction).
- **Share of voice:** brand mention volume vs. competitor set over the horizon.

## Output

1. `projects/<brand>-content/_strategy/pillars.md` — living pillar doc (updated, not duplicated).
2. `projects/<brand>-content/_strategy/<horizon>-strategy.md` — the dated calendar + channel mix + metrics + review date + flip condition.
3. A list of greenlit **seeds** ready to feed into `content-ideation`.

Non-trivial output includes: the decision (pillars + channel mix chosen and why), key facts (goal, horizon, cadence), risks (capacity, untested pillars), and the recommended next action (which seed to ideate first).

## Attribution

Adapted from [`marketing-social-media-strategist`](https://github.com/msitarzewski/agency-agents/blob/main/marketing/marketing-social-media-strategist.md) in the MIT-licensed [msitarzewski/agency-agents](https://github.com/msitarzewski/agency-agents) collection. Reframed as the planning layer above the Content Engine, calibrated to the user's brands, channels, and existing content-* skill suite.
