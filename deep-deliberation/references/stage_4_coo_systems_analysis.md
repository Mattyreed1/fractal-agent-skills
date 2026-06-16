### Stage 4: COO Systems Analysis

This stage applies operational systems thinking to the decision — structured constraints analysis, quantified tradeoffs, and control loops layered on top of practitioner reality (Stage 2) and verified facts (Stage 3).

#### Step 1: Invoke the COO Skill

**MANDATORY: You MUST invoke the `coo` skill using the Skill tool.** Pass it the full context:

```
Skill tool call: skill="coo", args="Analyze this decision through the COO lens.
Statement: {RESEARCH_BRIEF.clarified_question}
Hard constraints: {RESEARCH_BRIEF.hard_constraints}
Community findings: {COMMUNITY_FINDINGS summary}
Verified research: {VERIFIED_FINDINGS summary}

Apply: constraints mapping, value stream analysis, control loops, and risk tiers.
What are the operational realities that should shape the options?"
```

The COO skill will surface:
- Binding constraints (the things that actually limit options)
- Value stream analysis (where does the value — or cost — actually flow?)
- Control loops (how do you know if it's working?)
- Risk tiers (what's reversible vs irreversible?)

#### Step 2: Ask Operational Questions

After the COO analysis, ask the user 2-3 questions that target the operational gaps the COO analysis revealed. These are NOT strategy questions — they are fact questions about the user's constraints.

**Question types — ask the ones that fit this decision:**

| Type | Why | Example |
|------|-----|---------|
| **Decision-math inputs** | Can't compare options without the numbers that decide them | Economic: "At what price? How many customers for your target? Realistic conversion rate?" Technical: "What latency / throughput / cost are you optimizing for?" Effort: "How long does each path take, and what's the payback?" |
| **Resource reality** | Strategy means nothing without capacity | "How many hours/week can you actually ship? What's your monthly spend right now?" |
| **Traction signal** | Existing data > hypothetical strategy | "Do you have any signal that people want this? Waitlist, conversations, DMs?" |

**Wait for answers.**

#### Step 3: Surface 2-3 Options with Their Decision Math

After the COO analysis and user answers, synthesize ALL intelligence into **2-3 options** (not exactly 2 — allow 3 when a genuine third path exists that isn't a compromise of the first two).

**CRITICAL: Every option MUST quantify the tradeoffs the decision turns on.** When the decision is economic, that's revenue/expense math. Otherwise it's whatever dimension actually separates the options — time, cost, risk, performance, reach. Don't force money math onto a decision where money isn't the crux.

```markdown
## Stage 4 Complete — Top {2-3} Options

Based on community intelligence, verified research, COO analysis, and your constraints:

### Option A (Ranked #1): {Clear name}
{2-3 sentences: what it is, why it's ranked first}
- **Strongest evidence**: {key data point from Stages 2-3 — community + verified}
- **Best fit because**: {connection to user's constraints}
- **Risk**: {main downside}

**Decision Math** (quantify only the dimensions that matter for THIS decision):
- Key metric(s): {the numbers that decide it — e.g. economic: price, target customers, MRR, operating cost; technical: latency, throughput, infra cost; effort: hours to ship, payback period}
- Assumptions + source: {state each estimate and where it comes from}
- Timeline to target: {N} {units}

### Option B (Ranked #2): {Clear name}
{same structure as above, including Decision Math}

### Option C (Ranked #3, if applicable): {Clear name}
{same structure — only include if genuinely distinct from A and B}

Sending these to the debate arena...
```

**Rules for option generation:**
- Always generate at least 2 options, at most 3
- A third option is warranted when the best answer is a sequencing play that neither pure option captures (e.g., "do X first, then Y when condition Z is met")
- Do NOT generate 3 options just to have 3 — the third must earn its place
- Every option MUST carry its decision math. If you can't quantify the tradeoff that matters, the option isn't concrete enough.

**Store options with their full evidence and math packages.**
