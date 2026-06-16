### Stage 7: Action Plan

**Invoke the `action-plan` skill.** It owns the phased plan structure, target metrics, checkpoints, and flip conditions.

```
Skill tool call: skill="action-plan", args="Turn this verdict into a phased action plan.
Decision: {VERDICT.winner} — {winning option description}
Decision math: {winning option's decision math}
Hard constraints: {RESEARCH_BRIEF.hard_constraints}
Target metric + timeline: {from brief}
Flip conditions from judge: {VERDICT.flip_conditions}"
```

The `action-plan` skill returns:
- Week / Month / Quarter / Year horizons
- Specific actions + target metric per horizon
- Decision checkpoints with pivot triggers
- Flip conditions giving the user explicit permission to change course

**Display the final combined output to the user:**
```markdown
# Deep Deliberation: Final Output

{VERDICT — from Stage 6}

{ACTION_PLAN — from Stage 7}
```

**Pipeline complete.**
