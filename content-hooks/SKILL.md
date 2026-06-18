---
name: content-hooks
description: Stage 3 of the Content Engine. Write title and 3 hook options for an approved content brief. Use when CO hands off an approved brief or you receive a 'Write Title + Hooks' task. Creates Discord thread in #content, writes 3 hooks graded A-F against a 4-dimension rubric (psychology / framing / grammar / non-obvious) with reasoning and target emotion, posts for the user to pick or paste his own for a grade-and-rewrite.
license: MIT
metadata:
  version: 3.0.0
  created: 2026-03-27
  updated: 2026-04-28
  author: content-orchestrator
  domains: ['content', 'copywriting', 'linkedin']
---

# Content Hooks & Title

## Trigger

CO marks a `Content Context Brief` task as `done` and creates a `Write Title + Hooks` task for CC, with a board message linking to the Notion page.

## Who

CC (`content-creator`)

## Inputs

- Notion content page URL (from CO's handoff message)
- Approved Content Context Brief on that page (written by `content-brief` v2.0.0+, includes: Core Claim, Why This Matters, Target Audience, Proof & Artifacts, Relevant Quotes, Resources, Related Prior Work, Lead Magnet, Visual Suggestions, Raw Context)

## Steps

### 1. Read the brief

Use the `notion` skill (read mode) to fetch the Notion page as clean markdown. Mine **all** sections — particularly:
- **Core Claim** + **Why This Matters** → set the angle for hooks
- **Target Audience** → set the voice / pain trigger
- **Relevant Quotes** → potential opener material
- **Proof & Artifacts** → punchy data points to hook with

### 2. Create Discord thread

In #content (`your-content-channel-id`):
- Thread name: `{content piece name}`

### 3. Generate, grade, and post hook options

Generate candidates with the **`hook-machine`** skill (Mode 2) using the brief's topic. It loads the rubric calibrated to the user's data, runs the format-topic fit screen, writes candidates, and grades each A-F across four dimensions (psychology / trigger words & framing / grammar / non-obvious). hook-machine cuts List A below C and iterates List B to B+; surface the 3 strongest hooks (B or higher).

If no rubric exists yet, run hook-machine Mode 1 first (it builds one from the user's top performers), or fall back to the universal craft principles in the `writing` skill's `references/hooks.md`.

Post in the Discord thread using **this exact format:**

```
## Hook Options for: {content piece name}

### Option 1 (Grade: {A | A- | B+ | B})
> {hook text — first 1-2 lines of the post}

**Why it works:** {tag the strongest dimension(s): psychology / framing / grammar / non-obvious}
**Target emotion:** {curiosity | recognition | fear of missing out | aspiration | pain}

### Option 2 (Grade: {...})
> {hook text}

**Why it works:** {reasoning}
**Target emotion:** {emotion}

### Option 3 (Grade: {...})
> {hook text}

**Why it works:** {reasoning}
**Target emotion:** {emotion}

---
@user — pick a hook, or paste your own and I'll grade and rewrite it.
```

### 4. Move Notion Stage

Stage: `On Deck` → `Title/Thumb/Hook`

### 5. Wait for the user — pick, or grade-and-rewrite

the user either picks a hook in the thread, or pastes their own draft. If they paste their own, run it through the **`hook-machine`** skill (Mode 3): an honest line-by-line A-F grade against the rubric (no auto-reject), and 3 structural rewrites that keep his angle (add a two-sentence amplifier, swap a question for a declarative, add an outcome+constraint). the user picks a rewrite or refines further.

## The hook rubric

The rubric that Steps 3 and 5 grade against is built and maintained by the **`hook-machine`** skill, from the user's own top vs. bottom performers — not generic best practice, and never another creator's trigger words (they don't transfer across audiences). Refresh it periodically, or whenever hooks keep missing, by invoking hook-machine Mode 1.

## Output Format (handoff to content-scripting)

Once the user picks:

1. **Add to Notion page**: Use `notion` skill (mode: `append`) to write a `## Chosen Hook` section with the selected hook text
2. **board task**: title=`Write Post — {name}`, assignedTo=`content-creator`, evaluator=`content-orchestrator`, priority=P2, description=Notion page URL
3. **Update existing task**: mark "Write Title + Hooks" as `done`

## Edge cases

- **Brief is unclear or missing sections**: message CO via board asking for clarification. Do NOT write hooks from incomplete context. The brief should have all 11 sections per `content-brief` v2.0.0+.
- **Brief has `[NEEDS INPUT: ...]` markers**: those are open gaps — flag them in your message back to CO before writing hooks.
- **the user doesn't respond in 7 days**: post a reminder in the thread. If 14 days, escalate to CO.
- **the user rejects all 3 hooks**: ask for direction ("what angle feels right?"), write 3 new options.
- **Content overlaps a published piece**: the brief's "Related Prior Work" section should already note this. Differentiate the angle in the hook reasoning.
