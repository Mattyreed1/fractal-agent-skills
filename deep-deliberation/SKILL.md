---
name: deep-deliberation
description: Multi-stage operational deliberation for decision validation, strategy, or technical claims (e.g., "stress test this idea", "should I use X or Y"). Orchestrates devil's-advocate challenge, research verification, community scan, COO constraints analysis, Opus adversarial debate grounded in the decision's real stakes, judge verdict, and phased action plan.
metadata:
  version: 5.0.0
  model: claude-opus-4-6
  domains: [decision-making, strategy, critical-thinking, operations]
  type: orchestrator
  inputs: [statement, user-goal, claim, constraints]
  outputs: [research-brief, verified-findings, community-findings, debate-transcript, verdict, action-plan]
---

# Deep Deliberation

Put any statement, claim, belief, or decision through rigorous deliberation. This skill is a thin orchestrator — it chains other specialized skills in order and ensures nothing gets skipped.

## Pipeline

| # | Stage | Delegates To | Methodology Reference |
|---|---|---|---|
| 1 | Devil's Advocate | `devils-advocate` skill | [stage_1](references/stage_1_devils_advocate.md) |
| 2 | Community Scan | `last30days` skill | [stage_2](references/stage_2_community_scan.md) |
| 3 | Research & Verify | `research` skill | [stage_3](references/stage_3_research.md) |
| 4 | COO Systems Analysis | `coo` skill | [stage_4](references/stage_4_coo_systems_analysis.md) |
| 5 | Adversarial Debate | Opus Task agents (2–3) | [stage_5](references/stage_5_adversarial_debate.md) |
| 6 | Judge | `judge` skill | [stage_6](references/stage_6_judge.md) |
| 7 | Action Plan | `action-plan` skill | [stage_7](references/stage_7_action_plan.md) |

## Why This Order

- **Community before research** — `last30days` surfaces specific, numeric practitioner claims (a conversion rate, a benchmark, a cost figure, a timeline — whatever the decision turns on). Stage 3 research then verifies *those specific claims* with authoritative sources. If you flip the order, research has nothing concrete to verify beyond the user's premise — and community sentiment arrives later as raw signal with no fact-check pass.
- **COO after both research stages** — the operator's lens needs practitioner reality AND verified facts to map real constraints.
- **Debate after options are grounded in math** — philosophy without numbers is noise.
- **Judge before action plan** — you need a committed winner before you can operationalize it.

## Automation Scripts

- `python scripts/orchestrator.py` — prints the stage scaffold (print-only stub — it does not invoke skills)
- `python scripts/validate_verdict.py` — validates the combined Stage 6 verdict + Stage 7 action-plan output structure

## Execution Requirements — DO NOT SKIP STAGES

1. **Stage 1:** Invoke `devils-advocate` skill. Produces `RESEARCH_BRIEF` with challenged assumptions + HARD CONSTRAINTS.
2. **Stage 2:** Invoke `last30days` skill. Practitioner stories only — no pundits. Produces `COMMUNITY_FINDINGS`.
3. **Stage 3:** Invoke `research` skill with a query built FROM the community findings. Produces `VERIFIED_FINDINGS` (claims marked VERIFIED / REFUTED / PARTIALLY TRUE / UNVERIFIABLE).
4. **Stage 4:** Invoke `coo` skill. Every resulting option MUST be grounded in the decision's real stakes — the concrete numbers that separate the options (cost, time, risk, performance, reach, and, when the decision is economic, revenue/expense math). Quantify only the dimensions the decision actually turns on; don't bolt money math onto a question where money isn't the crux.
5. **Stage 5:** 2–3 Opus debate agents, 3 rounds (opening → rebuttals with research → closing). Each opening argument MUST quantify the decision's real stakes — the numbers that actually decide it. Agents MUST concede where appropriate.
6. **Stage 6:** Invoke `judge` skill with the full debate transcript. Returns scorecard + winner + reasoning. Judge does NOT produce the action plan.
7. **Stage 7:** Invoke `action-plan` skill with the winning option + constraints + target metrics. Returns week/month/quarter/year plan with checkpoints and flip conditions.

## Anti-Patterns and Examples

See [Anti-Patterns & Examples](references/anti_patterns_and_examples.md) for common failure modes, customization flags (`--quick`, `--deep`, `--no-debate`, etc.), and the verification checklist.
