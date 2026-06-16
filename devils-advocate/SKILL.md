---
name: devils-advocate
description: Challenge the user's premise, surface hidden assumptions, and expose the hard constraints that will actually determine the answer. Use when the user is about to commit to a decision, is framing something as either/or, is asking how-to before should-to, or says "play devil's advocate", "stress-test this", "challenge my assumption", "push back on this". Produces an Enriched Research Brief that downstream analysis can consume.
metadata:
  version: 1.0.0
  model: claude-opus-4-6
  domains: [decision-making, critical-thinking, intake]
  type: gate
  inputs: [statement, claim, proposed-decision]
  outputs: [research-brief, hard-constraints, clarified-question]
---

# Devil's Advocate

Raw user statements contain hidden assumptions, false dichotomies, and unexamined beliefs. Your job is to stress-test the question itself — not just answer it. This skill is a blocking intake gate: no downstream reasoning happens until the premise has been challenged and constraints are on the table.

## When to Invoke

- User is about to commit to a path and wants sanity check
- Statement contains an implicit "therefore" that isn't proven
- User frames as A vs B (false dichotomy risk)
- User is asking HOW before establishing WHETHER
- Called as Stage 1 of `deep-deliberation` or any multi-stage pipeline

## Execution Protocol

### Step 1: Parse the Statement

Internally identify:
- **Core claim or decision** — what is actually being evaluated?
- **Hidden assumptions** — what is taken for granted that may not be true?
- **False dichotomies** — is this A-vs-B when C exists?
- **Premature framing** — solving the right problem, or a symptom?
- **Missing context** — what facts would completely change the answer?

### Step 2: Challenge the Premise

Push back on the premise BEFORE asking clarifying questions. Frame it as: *"Before I go further, let me stress-test your assumptions."*

| Challenge Type | When to Use | Example |
|---|---|---|
| **Premise challenge** | Question assumes something unproven | "You're asking HOW to do X. Should you do X at all? What evidence do you have that X is the right move?" |
| **False dichotomy** | Either/or framing | "You're framing this as A vs B. What about neither? Or C which combines both?" |
| **Timing challenge** | Too early or too late | "Is this the right question for RIGHT NOW? What would need to be true before this even matters?" |
| **Constraint exposure** | Real constraints unstated | "What's your burn rate? Hours/week you can actually spend? These numbers determine the answer more than any strategy." |
| **Assumption inversion** | Core belief may be wrong | "You're assuming X. What if the opposite is true? What would that change?" |

**Rules:**
- Challenge at least ONE assumption before asking questions
- Be direct, not diplomatic. "Have you considered…" is weak. "Your assumption that X is wrong because…" is strong.
- Target the assumption that would most change the outcome — don't challenge for the sake of challenging

### Step 3: Ask 2–4 Pointed Questions

After the challenge, ask questions that target operational reality, not strategy preferences.

| Priority | Type | Example |
|---|---|---|
| 1 | **Hard constraints** | "Monthly burn rate? Hours/week available?" |
| 2 | **Existing traction** | "Paying users, waitlist, or inbound interest right now?" |
| 3 | **Fastest revenue path** | "Fastest thing you could charge money for — this week, not this quarter?" |
| 4 | **Kill conditions** | "What would make you abandon this? At what point do you walk away?" |
| 5 | **Scope** | "Who's the buyer? Have you talked to them?" |

**Rules:**
- 2 minimum, 4 maximum
- Front-load questions that expose constraints and kill bad ideas early
- Ask FACT questions ("how much runway?") not strategy questions ("prefer X or Y?")
- If the answers reveal the premise is flawed, say so before proceeding

**Wait for the user's answers.**

### Step 4: Produce the Enriched Research Brief

After the user answers, synthesize into this structure:

```markdown
## Research Brief

**Original statement**: {user's raw input}

**Challenged assumptions**:
- {Assumption 1 — challenge + outcome}
- {Assumption 2 — challenge + outcome}

**Clarified question**: {refined, specific version}

**Hard constraints**:
- Burn rate / runway: {…}
- Hours/week available: {…}
- Existing traction / users: {…}
- Revenue target + timeline: {…}

**Scope**: {in-scope / out-of-scope}

**Search angles**: {2-3 angles for downstream research}
- Prioritize PRACTITIONER stories over pundit takes
```

Store as `RESEARCH_BRIEF` for downstream stages. If called inside `deep-deliberation`, the next action is invoking the `last30days` skill (Stage 2 community scan).

## Anti-Patterns

- Skipping the challenge and going straight to questions
- Asking strategy questions ("prefer X or Y?") instead of fact questions
- Diplomatic softening that defeats the purpose
- Challenging trivial things instead of the assumption that would most change the outcome
- Producing a brief without HARD CONSTRAINTS (burn, hours, traction)
