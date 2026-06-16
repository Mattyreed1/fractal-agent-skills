### Stage 1: Devil's Advocate

**Invoke the `devils-advocate` skill.** It owns the full protocol — challenging assumptions, asking constraint-revealing questions, and producing the Enriched Research Brief.

```
Skill tool call: skill="devils-advocate", args="{user's raw statement}"
```

The skill will:
1. Parse the statement for hidden assumptions and false dichotomies
2. Challenge at least one assumption directly
3. Ask 2–4 fact questions (burn rate, hours/week, traction, kill conditions)
4. Synthesize answers into a `RESEARCH_BRIEF` with hard constraints

**Wait for the `devils-advocate` skill to return the Research Brief before proceeding.** Store it as `RESEARCH_BRIEF` for all downstream stages.

**Display status:**
```
Stage 1 complete — assumptions challenged, research brief locked in.
Scanning what practitioners are saying now...
```

**HARD GATE:** Next action is invoking the `last30days` skill (Stage 2). Do not skip to debate; do not start reasoning on the topic yourself.
