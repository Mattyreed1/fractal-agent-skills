### Stage 6: Judge

**Invoke the `judge` skill.** It owns the full scoring rubric and verdict format.

```
Skill tool call: skill="judge", args="Score this debate and pick a winner.
Original question: {RESEARCH_BRIEF.clarified_question}
User constraints: {RESEARCH_BRIEF.hard_constraints}
COO analysis: {COO_ANALYSIS summary}
Options with their decision math: {options from Stage 4}
Full debate transcript: {Round 1 + Round 2 + Round 3}"
```

When invoked inside deep-deliberation, launch the judge as an independent Task agent (`subagent_type: general-purpose`, `model: opus`) so its evaluation is not biased by the main orchestrator's context.

The `judge` skill returns:
- 5-criterion scorecard (Evidence, Logic, Quantitative Rigor, Practical Applicability, Concession Handling)
- Clear winner with 3–5 sentence reasoning
- Key debate moments (strongest point, best concession, weakest argument, most credible math)
- What the loser(s) got right
- Conditions that would flip the verdict

**The judge does NOT produce an action plan.** Store the verdict as `VERDICT` and proceed to Stage 7.

**Display status:**
```
Stage 6 complete — Option {X} wins ({score}/50).
Building the action plan...
```
