# Agent Operations

## Contents

- The Shift
- The Three Disciplines
- Team Structure in the AI Era
- The Agent Control Stack
- Autonomy & Risk Design
- Agent Unit Economics

Deep reference for the agent-operations sections of the COO skill: the three disciplines, team-structure math, the 6-layer Control Stack, risk design, and unit economics.

## The Shift

| Old system | Agent system |
|---|---|
| Humans execute work | Agents execute work |
| Managers route and coordinate | Orchestrators route and coordinate |
| Software supports humans | Humans supervise and support agents |

The COO stops managing people and starts designing control systems.

> Old COO: "How do I get 100 people to do this well?"
> New COO: "How do I design a system that does this correctly 99/100 times?"

> Designer of policies and architect of feedback loops for an autonomous operating system.

## The Three Disciplines

The AI era produced three disciplines, in sequence:

1. **Prompt Engineering** — individual, session-based. Craft an instruction, iterate the output. Personal skill, personal value. Table stakes.
2. **Context Engineering** — designing the entire information state an AI system operates within: RAG pipelines, MCP servers, structured organizational knowledge. Necessary but not sufficient.
3. **Intent Engineering** — encoding organizational purpose into agent infrastructure. Not prose in a system prompt, but **structured, actionable parameters** that shape how agents make decisions autonomously.

> Context tells agents what to know. Intent tells agents what to want.

Prompt craft is table stakes. Context engineering is infrastructure. **Intent engineering is the COO discipline** — it sits above both and determines whether agents optimize for what the organization actually needs.

When diagnosing an agent failure, ask:
- *Was this missing context?* → Context engineering fix
- *Was this missing intent?* → Intent engineering fix
- *Was this missing prompt craft?* → Probably not the real problem; symptom of missing intent.

## Team Structure in the AI Era

### The Math
Communication pathways in a group = `n(n−1)/2`.
- 5 people → 10 pathways
- 10 people → 45
- 20 people → 190

Grounded in Dunbar's 1992 research on cognitive limits:
- 5 — core group
- 15 — deep trust
- 50 — meaningful working relationships
- 150 — stable social connections

The US infantry fire team is 4 + a leader. Bezos arrived at the same conclusion.

> "Communication is a sign of dysfunction. We should be trying to figure out a way for teams to communicate less with each other, not more." — Jeff Bezos

### What AI Changed
**AI did not change the optimal coordination number. It made violating it catastrophically expensive.**

Before AI, a 5-person team produced X. After AI, the same team produces 5–10X. AI-native companies run **$2–3M+ revenue per employee** vs the SaaS benchmark of <$500K. At $2M per person, the coordination tax of a sixth hire is measured in millions of lost productivity.

### Two Archetypes

| Archetype | Size | Use for | Why it works |
|---|---|---|---|
| **Scout** | 1 person + full AI toolkit | High-ambiguity exploration where individual judgment dominates | Zero coordination overhead, maximum speed |
| **Strike Team** | 5 people (or agents) with shared context | Execution where correctness matters | Every output passes through ≥1 other brain that can catch meaningful errors |

Below 5: blind spots. Above 5: silos. Both fail loudly with AI in the mix.

### Ambition, Not Efficiency
The dominant framing of AI is cost reduction (same mission, fewer bodies). **This is a failure of imagination.** A team where each person is 5–10x more capable does not have a cost-reduction opportunity — it has the productive capacity of a team 5–10x larger.

The correct strategic question is not *"how small can we get"* but *"what was previously impossible that is now within reach."* You didn't get a cost reduction. You got an army.

When the user asks "should I hire," reframe: *what's the impossible thing your existing team could now do?*

## The Agent Control Stack

Six layers. Each has a characteristic failure mode. The COO owns integration of the entire stack.

### 0. Context Layer (Foundation)
The shared model of reality every other layer reads from and writes to. The context graph operationalized as infrastructure.

Every other layer depends on this:
- Intent reads context to know which goals apply to this entity
- Orchestration queries context to route work
- Execution pulls context into agent context windows
- Observability writes back to context (updating state after runs)
- Governance checks context for permissions and scope

**Failure mode:** Without a shared context layer, each agent builds its own model of reality. Two agents seeing different truth isn't a bug — it's a structural guarantee of contradictory output. *This is the agentic tarpit.*

### 1. Intent Layer (Intent Engineering)
Encoding organizational purpose as structured, actionable parameters:
- **Strategy** — what the system optimizes for
- **Risk tolerance** — how much downside is acceptable
- **Economic rules** — spend and margin constraints
- **Quality standards** — what "good enough" means
- **Definitions of done** — when work is actually complete
- **Value hierarchies** — when goals conflict, which wins
- **Decision boundaries** — what the agent is empowered to decide vs escalate

**Failure mode:** Agents execute what you specify, not what you meant. Bad spec + automation = perfect failure at scale. *Context without intent is a loaded weapon with no target.*

### 2. Orchestration Layer
- Task queues — what runs and in what order
- Priority rules — which work wins when resources conflict
- Routing policies — who or what handles each task type
- Escalation logic — when to bump work to a human
- Context graph queries — how agents retrieve relevant state

**Failure mode:** Conflicting truth causes oscillation. Two agents seeing different reality breaks the system.

### 3. Execution Layer
- AI agents — autonomous workers
- Tools — capabilities agents call
- APIs — external services
- Automations — rule-based flows that don't need reasoning

**Failure mode:** Unclear autonomy limits trigger constant escalations. Every edge case requires human intervention.

### 4. Observability Layer
End-to-end traces of every workflow run: inputs, decisions, tool calls, outputs, timing, cost.

Traces power the feedback loop:
- **Error budgets** — cap acceptable failure rates
- **Debugging** — pinpoint where runs broke
- **Auditing** — verify decisions after the fact
- **Evaluation** — score agent performance over time
- **Spec improvement** — feed failures back into the intent layer

**Failure mode:** Without fast error detection, agents compound mistakes. Slow feedback = expensive failures.

### 5. Governance Layer
- Permissions — what each agent can access and modify
- Spend limits — hard caps per run or per period
- Audit trails — decision logs derived from traces
- Kill switches — instant shutdown when thresholds breach
- Human overrides — manual intervention points baked into the flow

**Failure mode:** Agents escalate in milliseconds. Humans respond in hours. Response time becomes the constraint.

## Autonomy & Risk Design

> Autonomy is granted within a bounded loss function.

Every agent action must have:
- Maximum credible downside
- Confidence threshold
- Human escalation path

### Risk Tiers
| Tier | Impact | Autonomy | Oversight |
|------|--------|----------|-----------|
| 1 | Low | High | Low |
| 2 | Medium | Bounded | Human approval |
| 3 | High | Analysis only | Humans decide |

Routing policies assign tiers automatically via context graph state.

### Error Budgets
Define tolerable schedule slip and budget overrun per client or project tier.
- Low error → expand autonomy
- Rising error → restrict autonomy

Error budgets govern how much the system acts on its own. Without them, you're either over-restricting (escalation flood) or under-restricting (silent compound).

### SLAs (Service Level Agreements)
Performance promises that turn "should work" into enforceable constraints inside routing logic:
- "Invoices generated within 10 minutes, <1% error rate"
- "Enterprise leads escalated to humans within 1 hour"

### Scope Examples
- Money → spend caps
- Customers → tier-based permissions
- Data → scoped writes
- Code → sandbox → canary → production
- Legal → template-only → human signs contract

This is **risk envelope design**, not "AI vs human."

## Agent Unit Economics

Every agent operation has a cost. The COO optimizes value delivered / cost incurred.

### Cost Components
- **Token costs** — input/output per LLM call
- **API costs** — external service calls per workflow
- **Compute costs** — hosting, orchestration, storage
- **Error costs** — rework, customer impact, human intervention time

### Key Metrics
- Cost per workflow completion
- Cost per unit of value delivered (cost per invoice processed, cost per lead qualified)
- Agent cost vs human equivalent cost
- Error cost as percentage of total operating cost

### Optimization Levers
- **Cache** frequently retrieved context
- **Batch** operations where latency tolerance allows
- **Route** simple tasks to cheaper models, complex tasks to capable models
- **Reduce rework** by improving spec quality (intent layer)

The operating budget is a constraint. Continuously improve efficiency to reduce cost per unit of output. *Error cost is usually the dominant line item — and the one most ignored.*
