### Stage 3: Research & Verify

**MANDATORY: Invoke the `research` skill using the Skill tool before proceeding.** Do NOT substitute your own knowledge base. The community findings from Stage 2 must be verified with authoritative sources.

```
Skill tool call: skill="research", args="{enriched query built from COMMUNITY_FINDINGS — lead with the clarified question, then ask Perplexity to verify or refute the top 3-5 specific community claims}"
```

**Query Construction Rules:**

1. **Lead with the clarified question** from the Research Brief
2. **Include the top 3-5 community claims** from Stage 2 — the things that need verification (especially specific numbers, rates, and benchmarks — revenue/cost figures where the topic is economic)
3. **Ask specifically**: "verify or refute the following claims from recent community discussion"
4. **Include temporal grounding**: "as of {current month/year}"
5. **Prioritize verifying any quantitative claims** — whatever numbers the decision turns on (benchmarks, rates, timelines, costs, market sizes, pricing)

**Compare and classify each finding:**

| Finding | Status | Evidence |
|---|---|---|
| Claim 1 | VERIFIED / REFUTED / PARTIALLY TRUE / UNVERIFIABLE | Source |
| Claim 2 | ... | ... |

**Store as `VERIFIED_FINDINGS`.**

**Display status:**
```
Stage 3 complete — {n} claims verified, {n} refuted, {n} need more context.
Entering COO systems analysis...
```
