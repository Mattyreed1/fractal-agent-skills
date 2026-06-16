### Stage 2: Community Scan

**MANDATORY: Invoke the `last30days` skill using the Skill tool before proceeding.** Do NOT substitute your own reasoning or web searches. This stage surfaces the specific, numeric practitioner claims that Stage 3 will then verify.

```
Skill tool call: skill="last30days", args="{RESEARCH_BRIEF.clarified_question} — context: {RESEARCH_BRIEF.hard_constraints summary}"
```

**CRITICAL: Target practitioners, not pundits.**

Bias toward:
- Firsthand "how I actually did it" stories with real numbers
- The communities where practitioners for THIS topic gather (Indie Hackers / r/SaaS / r/startups / HN for business; the relevant subreddit, forum, or thread otherwise)
- Specific numbers, timelines, and tactics — including revenue/cost where the topic is economic
- Failure stories with lessons learned

Bias AWAY from:
- Thought leader hot takes ("X is dead", "Y is the future")
- Generic trend pieces with no concrete data
- Hype cycles and influencer opinions

**Extract:**
- Top community consensus (what most agree on)
- Dissenting voices (contrarian takes with substance)
- Specific numbers and timelines (revenue/cost where relevant)
- Warnings and firsthand failure stories
- Engagement signals (highly upvoted = strong signal)

**Store as `COMMUNITY_FINDINGS`:**

| Category | Content |
|---|---|
| **Consensus** | What most people agree on |
| **Dissent** | Substantive contrarian views |
| **Hard numbers** | Specific quantitative claims (timelines, benchmarks; revenue/cost where the topic is economic) |
| **Warnings** | Pitfalls and failure stories |
| **Signal strength** | Highest-engagement findings |

**Display status:**
```
Stage 2 complete — {n} practitioner findings captured.
Verifying claims with research...
```

**HARD GATE:** Next action is invoking `research` (Stage 3) with a query built FROM these community findings. Do not skip ahead.
