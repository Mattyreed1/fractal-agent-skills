# Core COO Frameworks

## Contents

- Value Stream
- Bottleneck Thinking
- Musk's Deletion Algorithm
- Three-Lens Model
- The Context Graph (Deep Dive)
- Composition

Deep reference for the four lenses the COO reaches for. Use this when the SKILL.md summary isn't enough — when the user wants to *apply* a framework, not just hear it named.

## A. Value Stream

Map how value flows through the system:

> Lead → Sale → Onboard → Deliver → Support → Retain / Expand

For each step, define four properties:

- **Owner** — who is accountable? (Singular. Not "the team.")
- **Cycle time** — duration from start to finish?
- **Failure modes** — how and why does it fail?
- **WIP** — what's the work in progress at this step right now?

If you can't fill in those four columns, you can't manage the step. The discipline of mapping the value stream is itself the intervention — most "operational problems" dissolve once the value stream is on paper, because handoffs and ownership gaps become obvious.

### Applying it
1. Have the user name the steps in their value stream — in their words, not yours.
2. Walk each step and fill in owner / cycle time / failure modes / WIP.
3. The first step where any column is empty or fuzzy is the place to focus.

---

## B. Bottleneck Thinking

Throughput is limited by the narrowest point in the system. Everything else is noise.

### The Five Steps
1. **Identify** — find where work accumulates or cycle time spikes. That step sets total system speed.
2. **Protect** — remove distractions, interruptions, and low-value work from the bottleneck.
3. **Feed** — keep inputs clean and ready so the bottleneck never waits.
4. **Elevate** — increase capacity (tools, automation, parallelization) only after stabilizing.
5. **Repeat** — constraints move. Re-scan and re-optimize continuously.

### The Critical Insight
> The bottleneck is almost always a **state or policy failure** before it is a capacity failure.

Don't add more agents or headcount until you've fixed the existing systemic issues. If the bottleneck is "review queue is 3 days long," the fix is rarely "hire more reviewers." It's usually:
- The review criteria are unclear (Process)
- One reviewer owns 80% of items by accident (People)
- Items arrive incomplete and bounce back (Data/State)

Apply the Three-Lens Model to the bottleneck before you elevate it.

---

## C. Musk's Deletion Algorithm

The bridge between *bottleneck thinking* (where to focus) and the actual work of improving. Order matters — each step depends on the one before it.

### The Five Steps
1. **Question every requirement** — each requirement should come attached to a *person*, not a department. If you can't identify who required it and why, it's a candidate for deletion.
2. **Delete** — remove any part, process, or step you can. *If you're not adding back at least 10% of what you deleted, you didn't delete enough.*
3. **Simplify** — only after deleting. Simplifying a process that shouldn't exist is waste.
4. **Accelerate** — speed up what remains. Reduce cycle time, parallelize, remove wait states.
5. **Automate** — and only as the last step.

> "The big mistake was that I began by trying to automate every step. We should have waited until all the requirements had been questioned, parts and processes deleted, and the bugs were shaken out." — Elon Musk

### Why This Order
Most teams skip to step 5. **Automating a broken process scales the breakage.** This is especially dangerous in the agent era — agents can scale a flawed process to 10,000 runs before anyone notices.

### When to Apply
- Before any agent deployment
- Before any "let's make this faster" project
- Whenever someone proposes adding a tool, role, step, or check
- During any cost-reduction effort

### The "Add Back 10%" Test
After deleting, you should be adding back 10% of what you deleted as you discover something genuinely necessary. If you delete and add nothing back, you didn't delete enough — you only removed obvious waste. Keep going.

---

## D. Three-Lens Model

Every operational failure is one of three things:

- **Process** — undefined, broken, or inconsistent. The work was never specified, the steps don't match reality, or different people do it differently.
- **People** — unclear ownership, missing capability, or misaligned incentives. The right person can't or won't do it.
- **Data / State** — missing, conflicting, or delayed truth in the context graph. The system's model of reality doesn't match reality.

### Why It Matters
Different lenses → different fixes. Adding training to a Data/State problem doesn't help. Adding documentation to a People problem doesn't help. Diagnose first, then prescribe.

### Applying it
When the user describes a failure, ask:
1. *Was the work defined?* (Process)
2. *Did someone own it, with the capability and incentive to do it right?* (People)
3. *Did everyone involved have the same picture of reality?* (Data/State)

The first "no" is your lens.

---

## E. The Context Graph (Deep Dive)

A coherent model of reality is non-negotiable in the agent era. The context graph is that model, made machine-readable.

### Structure
- **Entities** — customers, contracts, projects, budgets, schedules, agents, products, employees, vendors
- **Relationships** — *depends on, approved by, owned by, billed to, blocked by, supersedes, replaces, conflicts with*
- **Status** — current phase, risk tier, SLA class, budget remaining, deadlines, last-modified-by
- **Decisions** — what was decided, by whom/what, when, why, with what constraints, on what evidence

### What It Replaces
Manager-held context. The implicit knowledge living in someone's head about "oh, this client is sensitive about X" or "we always invoice this one differently." That works at 5 people. It catastrophically fails at scale and is *structurally impossible* with agents.

### What It Enables
- **Single Source of Truth** — routing and decision-making converge instead of forking
- **Selective context retrieval** — agents pull *relevant* state, not entire databases (cost + accuracy win)
- **Permissioning by relationship** — scope what each agent can see/write based on graph edges, not flat ACLs

### Failure Mode
If two agents see different "truth," the system oscillates and breaks. That's the agentic tarpit. The COO owns context graph integrity — *one canonical writer per entity attribute*. Other agents can read but not write.

### Practical Test
Pick any entity in the user's business (a deal, a project, a customer). Ask: *who or what is allowed to update this entity's status?* If the answer is more than one thing without a reconciliation rule, you've found a context split waiting to happen.

---

## Composition

These frameworks compose. A typical analysis:

1. **Value Stream** to map where work flows
2. **Bottleneck Thinking** to find where it's stuck
3. **Three-Lens** to diagnose *why* it's stuck
4. **Deletion Algorithm** to fix it (don't automate yet)
5. **Context Graph** to make the fix durable across agents and humans

Skip the order at your own risk.
