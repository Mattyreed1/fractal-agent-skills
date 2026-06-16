### Stage 5: Adversarial Debate

## Contents

- Agent Setup
- Debate Rules
- Round 1 — Opening Arguments
- Round 2 — Rebuttals (with Research)
- Round 3 — Closing Arguments

2-3 Opus agents argue in good faith — each championing one option. The debate is structured across 3 rounds.

#### Agent Setup

| Agents | Count | Assignment |
|--------|-------|------------|
| 2 options | 2 agents (ALPHA, BETA) | One per option |
| 3 options | 3 agents (ALPHA, BETA, GAMMA) | One per option |

**Launch all agents using the Task tool** with `subagent_type: general-purpose` and `model: opus`. Each agent receives:
- The original statement/topic
- Full community findings (Stage 2)
- Full verified findings (Stage 3)
- COO analysis and user constraints (Stage 4)
- Their assigned option (with its decision math) and ALL opposing options

#### Debate Rules (included in each agent's prompt)

1. **Good faith only** — argue honestly for your option's genuine strengths
2. **Evidence-grounded** — every claim must reference findings from Stages 1-3
3. **Must concede** — if an opponent has a genuinely stronger point, acknowledge it. Refusing to concede weakens your credibility
4. **No strawmanning** — represent opponents' positions accurately before attacking
5. **User context matters** — arguments must be relevant to THIS user's specific situation
6. **MANDATORY DECISION MATH** — every opening argument must quantify the option's real stakes on the dimensions that decide it:
   - The key metric(s) for THIS decision (economic: pricing × customers = target, acquisition → conversion → customers, operating cost, time-to-target; technical: latency / throughput / cost; effort: hours, payback) — skip the dimensions that don't apply
   - State each assumption and its source
   - If the numbers don't favor the option, you must acknowledge it and explain why it's still worth pursuing

#### Debate Structure

**Round 1 — Opening Arguments**

Each agent presents their strongest case (run in parallel via Task tool):

```
Agent prompt template:
"You are arguing FOR Option {X}: {description}. Present your opening
argument — your 3-4 strongest points for why this is the best choice
for this user given their context: {user context + constraints summary}.

MANDATORY: Include a DECISION MATH section:
- Quantify the dimensions that actually decide this (economic: pricing × conversion × traffic = timeline; technical: latency/throughput/cost; effort: hours/payback) — skip the ones that don't apply
- Use specific numbers, not ranges
- If a number is unknown, state your assumption and justify it
- Show your timeline to the target metric
- Include the relevant costs

Ground every point in evidence from the research:
- Community findings: {COMMUNITY_FINDINGS}
- Verified research: {VERIFIED_FINDINGS}
- COO analysis: {COO_ANALYSIS}

You are debating against {N-1} other options: {other option summaries}.
Be persuasive but honest. You must acknowledge where opponents have
legitimate strengths."
```

**Display Round 1 to user** with all agents' arguments.

**Round 2 — Rebuttals (with Research)**

Each agent reads ALL opponents' Round 1 arguments, then **performs targeted research** to find evidence that strengthens their rebuttal before responding. For 2 agents: run in parallel. For 3 agents: run all 3 in parallel, each responding to both opponents.

**Research phase**: Before writing the rebuttal, each agent gets ONE research call (`mcp__perplexity__search` or `mcp__perplexity__reason`) to find real-world evidence that counters their opponents' claims. The query should target the weakest point in an opponent's argument — e.g., if an opponent claims "80% conversion rate from free to paid," the agent researches actual freemium conversion benchmarks.

```
Agent execution steps:
1. Read opponents' Round 1 arguments
2. Identify the most attackable claim (especially the quantitative claims / decision math)
3. Run ONE `mcp__perplexity__search` or `mcp__perplexity__reason` query to find counter-evidence
4. Write rebuttal incorporating the fresh evidence

Agent prompt template (after research completes):
"Your opponents argued: {all other agents' Round 1 outputs}

You researched their weakest claim and found: {research results}

Write your rebuttal. Attack their weakest points — especially their
numbers / decision math. Use the evidence you just found. If their
assumptions are unrealistic, prove it with data. Concede where they
made genuinely strong points. Reinforce your strongest remaining
argument."
```

**Display Round 2 to user** (include what each agent researched).

**Round 3 — Closing Arguments**

Each agent reads the full debate history and delivers their final case:

```
Agent prompt template:
"Here is the full debate so far: {Round 1 + Round 2 transcript}

Deliver your closing argument. This is your last chance to persuade.
Summarize: what has been conceded, what remains contested, why your
numbers are more realistic than opponents', and why your option
is ultimately the better choice for this specific user."
```

**Display Round 3 to user.**

**After the debate**, display status:

```
Debate complete — 3 rounds, {N} champions heard.
Sending to the judge...
```
