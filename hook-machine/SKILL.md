---
name: hook-machine
description: Data-driven hook engine. Analyzes the owner's top vs. bottom-performing content to extract winning hook principles, banks them as a persistent grading rubric calibrated to the owner's audience, then generates and grades hooks for new topics. Source-agnostic ingestion (paste, CSV export from LinkedIn/X analytics, or fetch X posts via the scrape skill) with no third-party data platform required. Use when building or refreshing a hook rubric, analyzing why hooks win or lose, generating data-backed hooks for a topic, or grading and rewriting a draft hook. For a quick one-off hook that needs no performance data or grading, use the writing skill instead. Triggers - 'build my hook rubric', 'refresh the hook rubric', 'analyze my best hooks', 'hook machine', 'why do my hooks win', 'generate hooks for', 'grade this hook', 'rewrite this hook'.
license: MIT
metadata:
  version: 1.0.0
  created: 2026-06-07
  author: assistant
  domains: ['content', 'copywriting', 'hooks']
---

# Hook Machine

A data-driven engine that learns what makes the owner's hooks win, banks it as a reusable rubric, and uses that rubric to generate and grade new hooks. Pure Claude Code: every step is reading and reasoning over content the owner already has. No paid data platform, no MCP dependency.

Two universal layers sit under the data. **How to write** a hook (the 6 opener types + structural patterns) lives in the `writing` skill's `references/hooks.md`. **How to grade** a hook (the 8 universal principles, anti-patterns, and grade scale) lives in [references/grading-rubric.md](references/grading-rubric.md). This skill is the *data layer* on top: it discovers which patterns actually win for *this* owner and turns that into a calibrated, gradeable rubric.

## Medium-agnostic

A "hook" here is the **opener of any piece**: a LinkedIn post, an X thread, a blog intro, an email subject line, or the first lines of a video script. The engine analyzes openers and their performance metric and does not care about the medium. The source-data examples lean LinkedIn/X because that is the owner's main content, but any opener + metric works.

## When to use this vs. the `writing` skill

Not competitors. The `writing` skill's `references/hooks.md` is the **craft** (how to write a good hook from first principles). This skill is the **data layer** on top (what actually wins for *this* owner, plus grading). They chain: if no rubric exists yet, this skill falls back to the writing craft principles.

| Use `writing` / hooks.md (craft, lite) | Use `hook-machine` (data, heavy) |
|---|---|
| One-off hook or fast draft | Generating hooks to be **graded** against what's proven to win |
| No rubric exists yet | **Building or refreshing** the rubric from performance data |
| Brainstorming variety (the 6 opener types) | "Analyze my best hooks", "why do my hooks win" |
| The hook is one part of a bigger writing task | **Grading or rewriting** a draft against the rubric |

**One-line rule:** does the task need the owner's performance data, the rubric, or a grade? Then `hook-machine`. Just need a good hook now? Then `writing`.

## Three modes

| Mode | When | Reads | Writes |
|------|------|-------|--------|
| **1. Build / refresh rubric** | Periodically, or when hooks keep missing | Top + bottom performers | `assets/hook-rubric.md` |
| **2. Generate hooks** | Have a topic, want options | The rubric | Graded hook options |
| **3. Grade & rewrite** | Have a draft hook | The rubric | Grade + 3 rewrites |

Modes 2 and 3 require a rubric. If `assets/hook-rubric.md` does not exist, run Mode 1 first.

---

## Mode 1 — Build / refresh the rubric

### Step 1: Ingest (source-agnostic)

Get the owner's **top** performers and a matched set of **bottom** performers. Use whichever source is available, in priority order:

1. **Owner pastes them** — fastest, works for any platform. Ask for ~10-20 top posts and ~10-20 weak ones.
2. **CSV export** from LinkedIn or X analytics — read it directly (Read tool or a one-off `python3`). Columns needed: post text/opener + one engagement metric.
3. **X / Twitter** — fetch posts via the `scrape` skill (xAI API).

Each item needs only two things: the **hook** (the opener) and **one comparable metric** (impressions, engagement rate, or saves — pick one and use it consistently).

**Identifying the hook.** It is not a fixed sentence count. The hook ends where the piece shifts from *getting the reader to stay* to *delivering the content*. Some hooks are one line, some are three or four. Don't grab extra body sentences, and don't miss setup sentences that are part of the hook.

**Screen out before analyzing:**
- Off-topic posts (personal updates unrelated to the content lane).
- **Boosted / paid posts.** A post with high reach but anomalously low engagement rate was likely promoted; it inflates the data and gives a false signal. This is the written-content analog of screening brand deals. Flag and drop them.

More data = sharper rubric. A handful of posts gives a rough rubric; 50+ gives a precise one.

### Step 2: Sort winners vs. losers (find the breakpoint)

Per source (do **not** merge sources — styles differ), rank items by the chosen metric. Find the natural **breakpoint**: the gap where the top performers clearly separate from the pack (content is usually 80/20 — a few big winners). Everything above the line = winners; below = losers. Keep each source segmented.

### Step 3: Analyze winners vs. losers across 4 dimensions

For each source, contrast the winners against the losers across the four dimensions (full criteria in [references/analysis-dimensions.md](references/analysis-dimensions.md)):

1. **Psychology** — the emotional mechanism (curiosity gap, tension, recognition, stakes).
2. **Trigger words & framing** — the specific language and framing winners use that losers don't.
3. **Grammar / structure** — sentence construction (declarative vs. hedged, payoff position).
4. **Non-obvious** — patterns only visible by reading the full text, not the metrics.

Produce **winner-vs-loser contrasts**, not descriptions. "Winners name a concrete outcome in the first line; losers open with category branding" beats "winners are specific."

### Step 4: Cross-source synthesis

Find patterns that appear in **2+ sources** — those are strong, transferable signals. Note divergences too (style-specific quirks that should NOT be generalized).

### Step 5: Assemble and save the rubric

Combine three layers into the rubric ([assets/templates/rubric-template.md](assets/templates/rubric-template.md) is the structure):

1. **Universal principles** — the 8 grading principles in [references/grading-rubric.md](references/grading-rubric.md) (always active), with the `writing` skill's opener types + structural patterns as the generation craft.
2. **Custom principles** — derived from this analysis, each tagged with its source and the win/loss delta (e.g., "outcome-first openers: +X% vs. category-first, confirmed in 2 sources").
3. **Trigger-word bank** — the specific words/framings that won, *for this owner*.

Save to `assets/hook-rubric.md`. On refresh, append a dated revision rather than clobbering the prior version.

> **Hard rule:** never seed the trigger-word bank or custom principles by copying another creator's hooks. The whole reason this engine exists is that hook psychology does **not** transfer across niches — a word that wins in one audience flops in another. Derive everything from the owner's own data.

---

## Mode 2 — Generate hooks for a topic

Load `assets/hook-rubric.md` (if missing, run Mode 1), then produce two lists. Grade everything against [references/grading-rubric.md](references/grading-rubric.md).

### List A — Format-matched (up to 5 per source)

Run this per source — don't blend formats from different sources into one list. For each winning format, run the 3-test compatibility screen (Structural / Tone / Word-substitution, in [references/analysis-dimensions.md](references/analysis-dimensions.md)); cut any format that fails any test. For survivors, write a hook that **re-skins** the format with the rubric's principles (close to the proven structure, not a copy). Rank by rubric fit, take the top 5, and **cut anything that grades below C**. If fewer than 5 survive, present only what's clean and say so. Show each hook's source format and grade.

### List B — Originals (5, source-agnostic)

Written from scratch on the universal + custom principles, not any one source's style. Internally iterate: generate, grade, rewrite anything below B+, repeat until all 5 are **B+ or above**. Show grades; explanations only if asked.

If the user asks for more, generate more the same way.

---

## Mode 3 — Grade & rewrite a hook

For the user's own draft hook.

1. Load `assets/hook-rubric.md`.
2. **Grade it honestly, line by line**, against the universal + custom principles (grade scale in [references/grading-rubric.md](references/grading-rubric.md)). Quote each line and name what's working and what's weak (soft open, no specificity, missing credibility anchor, hedged question, buried payoff, em-dash). Don't inflate, and don't reject — it's the user's hook; the value is accurate feedback. Show where it lands relative to the B+ bar.
3. **Offer 3 rewrites, each taking a different approach** — one fixes the structure, one reframes the value promise, one adds specificity or proof. Keep the owner's angle, and note why each is stronger.

---

## Integration

- **`content-hooks`** (content engine Stage 2) calls Mode 2 with the brief's topic to produce options, and Mode 3 when the user pastes his own draft. It owns the Discord thread and the pick/handoff; this skill owns the rubric and the grading.
- **`writing` / `references/hooks.md`** supplies the universal craft principles that Mode 1 Step 5 builds on. Keep that file as the craft source of truth; this skill never duplicates it.

---

## Anti-patterns

| Avoid | Why | Instead |
|-------|-----|---------|
| Importing another creator's trigger words | Psychology doesn't transfer across niches | Derive every custom principle from the owner's own data |
| Merging all sources before analysis | Muddies the signal toward the average | Keep sources segmented; synthesize after |
| Forcing an incompatible format onto a topic | Produces a flat, off-key hook | Run the format-topic fit screen first |
| Ranking by reach / views alone | Boosted posts mislead | Use engagement rate; screen anomalies |
| Generating or grading without the rubric | Inconsistent, ungrounded output | Always load (or build) the rubric first |
| Clobbering the rubric on refresh | Loses the trend over time | Append a dated revision |

## Verification checklist

- [ ] Mode 1: sources kept segmented; winners/losers split at a real breakpoint
- [ ] Mode 1: every custom principle tagged with source + win/loss delta
- [ ] Mode 1: no trigger words copied from other creators
- [ ] Mode 1: boosted/off-topic posts screened out
- [ ] Rubric saved to `assets/hook-rubric.md` (dated revision on refresh)
- [ ] Mode 2: format-topic fit screen applied; only B+ surfaced
- [ ] Mode 3: honest line-by-line grade; 3 rewrites offered (no auto-reject)
