---
name: action-plan
description: Turn a decision, verdict, or analysis into a phased action plan with week/month/quarter/year horizons, target metrics at each checkpoint, pivot triggers, and flip conditions. Use when the user says "turn this into an action plan", "give me a phased plan", "what do I do next", or as the terminal stage of deep-deliberation after the judge has issued a verdict. Produces actionable, metric-anchored next steps — not vague roadmaps.
metadata:
  version: 1.0.0
  model: claude-opus-4-6
  domains: [planning, operations, execution]
  type: generator
  inputs: [decision, verdict, constraints, goals]
  outputs: [phased-plan, target-metrics, checkpoints, flip-conditions]
---

# Action Plan

Convert a committed decision into a phased execution plan. Every horizon has specific actions and a measurable target metric. Every plan includes decision checkpoints with pivot triggers so the user has escape hatches if reality diverges.

## When to Invoke

- Terminal stage of `deep-deliberation` (after `judge`)
- User has made a decision and needs to operationalize it
- User asks "what's next?", "how do I roll this out?", "phased plan for…"
- After any analysis that produced a recommendation without execution steps

## Inputs Required

- The decision or winning option (with its decision math if applicable)
- User's hard constraints (burn, hours/week, runway, traction)
- Outcome targets + timeline (revenue when the decision is economic; otherwise the metric that defines success)
- Any known risks, kill conditions, or alternative options

If the target metrics or constraints are missing, ask before producing the plan. A plan without target metrics is fiction.

## Output Format

```markdown
## Action Plan: {decision name}

### Next Week (Days 1–7)
- [ ] {Specific action 1}
- [ ] {Specific action 2}
- [ ] {Specific action 3}
- **Target metric**: {measurable outcome by end of week}

### Next Month (Days 8–30)
- [ ] {Specific action 1}
- [ ] {Specific action 2}
- [ ] {Specific action 3}
- **Target metric**: {e.g., "5 paying users at $X/mo", "landing page at 10% conversion"}

### Next Quarter (Months 2–3)
- [ ] {Specific action 1}
- [ ] {Specific action 2}
- [ ] {Specific action 3}
- **Target metric**: {e.g., "$X MRR", "Y% conversion rate", "p95 latency under 200ms", "Z active users"}

### Next Year (Months 4–12)
- [ ] {Specific action 1}
- [ ] {Specific action 2}
- [ ] {Specific action 3}
- **Target metric**: {e.g., "$X MRR", "sustainable growth rate of Y%", or the non-financial outcome that defines success}

### Decision Checkpoints
- **Week 2**: If {condition/metric}, pivot to {alternative}
- **Month 1**: If {metric} < {threshold}, reconsider {option}
- **Quarter 1**: If {condition}, the plan flips to {alternative path}

### Flip Conditions
- If {condition}, the committed option is wrong — switch to {alternative} because {reason}
- If {condition}, accelerate to the next phase because {reason}
- If {condition}, pause everything because {reason}
```

## Rules

- **Every horizon has a target metric.** "Explore options" / "get traction" / "build community" are not metrics. "5 paying users at $49/mo" is.
- **Actions must be specific.** "Talk to customers" is vague. "Book 5 customer calls via cold outreach to [list]" is specific.
- **Four horizons, not three.** Week, month, quarter, year. The week is usually what matters most — make it real.
- **Checkpoints are mandatory.** The user needs explicit pivot triggers. Plans without checkpoints become sunk-cost traps.
- **Flip conditions give the user permission to change their mind.** Name the specific conditions under which the plan is wrong.
- **Anchor to the decision math from the upstream analysis.** If the verdict quantified the target (e.g. "$5K MRR at $49/mo = 102 customers," or "p95 latency under 200ms"), each horizon's target should be a credible step toward it.
- **Respect the user's hard constraints.** If they have 10 hrs/week, don't plan 40 hrs/week of work.

## Anti-Patterns

- Soft metrics ("make progress on X", "explore Y") instead of numbers
- Three horizons instead of four (missing the week, or missing the year)
- No checkpoints — plan becomes a commitment device with no escape
- Actions that don't ladder to the target metric for that horizon
- Ignoring the user's hours/week capacity — planning 40 hrs when they have 8
- Generic templates that could apply to any business — the plan must reference THIS decision's specifics
