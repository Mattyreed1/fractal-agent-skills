# Common Failure Patterns

## Contents

- The Intent Gap
- The Spec Gap
- The Context Split
- The Silent Compound
- The Escalation Flood
- The Interface Mismatch (Multi-agent specific)
- Diagnostic Flowchart
- Mapping to Three-Lens Model

Deep reference for diagnosing operational and agent failures using COO Playbook patterns. Six patterns, each with a real or representative case study, root cause, control-stack layer, fix pattern, and detection method.

## 1. The Intent Gap

**Case study (Klarna, 2024–2025):** Klarna deployed an AI support agent in early 2024. It handled 2.3M conversations in month one across 23 markets and 35 languages. Resolution time dropped from 11 minutes to 2. The company projected $40M in savings and reported $60M by early 2025. It also destroyed brand trust — generic answers, zero judgment on edge cases. By mid-2025, the CEO called the result "lower quality" and started rehiring the humans they'd cut.

**What went wrong:** The agent optimized for *resolution speed* — a metric — not *customer lifetime value* — the actual organizational goal. A veteran human knows when to bend a policy or spend extra time because a customer's tone signals churn risk. The AI had a prompt. It had context. It did not have intent.

**Root cause:** Intent layer failure. The wrong objective was encoded.

**Control stack layer:** Intent (Layer 1) — specifically the value-hierarchy and decision-boundary parameters were missing or wrong.

**Fix pattern:** Encode the *actual* organizational goal as the agent's optimization target, not a proxy metric. Add explicit value hierarchies ("when speed conflicts with customer trust, trust wins"). Define escalation triggers based on customer signals (tone, history, account size), not just confidence scores.

**Detection:** Lagging customer-trust metrics (NPS, churn) eventually surface this — but too late. The leading indicator is qualitative output review by humans who know what good service looks like.

**Distinguishing from Spec Gap:** Spec Gap = "we said the wrong thing." Intent Gap = "we said the right thing but optimized for the wrong outcome of it."

---

## 2. The Spec Gap

**What happens:** An agency deploys an invoicing agent. The spec says "generate invoices for completed projects." The agent invoices every project marked "complete" — including test projects and internal ones. 40 bogus invoices go out before anyone notices.

**Root cause:** Intent layer failure. "Completed" was never scoped to billable client projects. The spec was literal; the agent took it literally.

**Control stack layer:** Intent (Layer 1)

**Fix pattern:** Tighten the spec. Define exactly what qualifies. Add explicit exclusions. Test with edge cases before deploying. Add a pre-launch dry run that surfaces what the agent *would* do without acting.

**Detection:** Pre-launch dry run, or a human-in-the-loop approval step for the first N runs.

---

## 3. The Context Split

**What happens:** Two agents share a CRM. One updates deal stage based on email activity. Another updates it based on meeting outcomes. A deal shows "Closed Won" and "Needs Follow-up" simultaneously. Downstream agents send conflicting messages to the client.

**Root cause:** No single owner of deal-stage truth in the context graph. Two writers, no reconciliation.

**Control stack layer:** Context (Layer 0) + Orchestration (Layer 2). Three-Lens: Data/State.

**Fix pattern:** Assign one canonical writer per entity attribute. Other agents read but don't write. *Or:* implement a reconciliation agent whose explicit job is to resolve conflicts before downstream consumers see them.

**Detection:** Context graph integrity checks — periodic scans for entities in inconsistent states.

**Note:** This is the fingerprint of the **agentic tarpit** at small scale. At large scale you don't get neat conflicts — you get systemic chaos. Same root cause.

---

## 4. The Silent Compound

**What happens:** A content agent publishes social posts with a subtle formatting error. No trace inspection is configured. The error runs for 3 weeks across 90+ posts before a human spots it.

**Root cause:** No observability. No feedback loop. Slow detection = compounding damage.

**Control stack layer:** Observability (Layer 4)

**Fix pattern:** Instrument traces on all agent outputs. Sample and review outputs on a cadence (daily or hourly depending on blast radius). Set quality thresholds that trigger alerts when output drifts.

**Detection:** Any trace inspection or output sampling would have caught this in the first run. The fix is *cheap*. The cost of skipping it is what makes this pattern dangerous.

---

## 5. The Escalation Flood

**What happens:** An agent handles support tickets with a rule: "escalate if confidence is below 80%." In practice, 60% of tickets hit that threshold. The human team drowns in escalations — *worse than no automation at all.*

**Root cause:** Permission boundaries too tight. Error budget not calibrated against actual distribution. Confidence threshold set without seeing the data.

**Control stack layer:** Governance (Layer 5) + Orchestration (Layer 2)

**Fix pattern:** Calibrate confidence thresholds against real data distribution before deploying. Use error budgets: start with tight bounds, measure actual error rates on a shadow run, then expand autonomy where error is low.

**Detection:** A dashboard showing escalation rate vs resolution rate would immediately reveal the imbalance — usually within hours.

---

## 6. The Interface Mismatch (Multi-agent specific)

**What happens:** An agent tries to invoke a skill called "COO" (uppercase, matching user input). The Skill tool is case-sensitive and returns "Unknown skill." The agent then wastes cycles investigating the skills directory instead of normalizing the input and retrying.

**Root cause:** The calling agent treated user input as a valid interface parameter without normalizing it to the canonical form. The interface contract (case-sensitive lowercase name) was not enforced at the orchestration layer.

**Control stack layer:** Orchestration (Layer 2). The routing policy failed to map user intent to canonical tool parameters.

**Fix pattern:** All inter-agent and tool invocation interfaces need a normalization step. *User keywords are inputs; canonical names are outputs.* The mapping is owned by the orchestrating agent, not by the user or the downstream tool.

**Detection:** A simple contract documented at the orchestration layer — "skill names are always lowercase, mapped from user keywords by the agent" — would have prevented it.

See [multi-agent-protocols.md](multi-agent-protocols.md) for the full set of interface-contract rules.

---

## Diagnostic Flowchart

When something breaks, walk this in order:

```
1. Was the spec correct?
   NO → Spec Gap (Intent layer)
   YES ↓

2. Did the spec encode the actual goal, or just a metric?
   METRIC ONLY → Intent Gap (Intent layer, value hierarchy)
   YES ↓

3. Was the interface contract honored?
   NO → Interface Mismatch (Orchestration)
   YES ↓

4. Was system state consistent across agents?
   NO → Context Split / agentic tarpit (Context + Orchestration)
   YES ↓

5. Were autonomy boundaries calibrated to real distributions?
   NO → Escalation Flood (Governance + Orchestration)
   YES ↓

6. Was the failure detected quickly?
   NO → Silent Compound (Observability)
   YES → Walk Three-Lens (Process / People / Data-State)
```

## Mapping to Three-Lens Model

| Failure Pattern | Process | People | Data/State |
|---|---|---|---|
| Intent Gap | Wrong optimization target | Wrong assumptions about what "good" means | N/A |
| Spec Gap | Incomplete spec | Wrong assumptions | N/A |
| Interface Mismatch | No normalization step | Agent passed raw input | Contract not documented |
| Context Split | No write ownership | N/A | Conflicting truth |
| Escalation Flood | Bad threshold design | Team overwhelmed | Confidence not calibrated |
| Silent Compound | No review process | No one watching | Invisible errors |
