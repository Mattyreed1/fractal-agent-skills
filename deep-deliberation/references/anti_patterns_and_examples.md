## Anti-Patterns

| Avoid | Why | Instead |
|-------|-----|---------|
| Skipping Stage 1 challenges | Garbage in, garbage out — unchallenged assumptions produce bad options | Invoke `devils-advocate`; always challenge at least one assumption before proceeding |
| Asking strategy questions in Stage 1 | "Would you prefer X or Y?" doesn't expose constraints | Ask FACT questions: burn rate, hours/week, existing traction |
| Skipping Stage 2 (`last30days`) | Misses real-world practitioner experience. **Common failure mode.** | MUST call `Skill("last30days", ...)` — no exceptions |
| Skipping Stage 3 (`research`) | Community folklore goes into the debate unverified | MUST call `Skill("research", ...)` — no exceptions |
| Targeting pundits over practitioners | "X is dead" hot takes don't help operational decisions | Search for firsthand "how I actually did it" stories with real numbers, not thought-leader opinions |
| Running research before community scan | Research has nothing concrete to verify beyond the user's premise | Surface practitioner claims first, then verify them with authoritative sources |
| Generic Stage 3 research query | Wastes the specificity from Stage 2 | Build the research query FROM the top 3-5 specific community claims |
| Skipping `/coo` in Stage 4 | Misses constraints analysis and systems thinking | MUST call `Skill("coo", ...)` — no exceptions |
| Options with no decision math | A choice without numbers is fiction | Every option must quantify the dimension the decision turns on (cost, time, risk, performance — or revenue when it's an economic call) |
| Forcing revenue math onto a non-economic decision | Bolting MRR onto a technical or process call produces fake precision | Quantify only the dimensions that decide THIS question; revenue/expense math applies when money is the crux, not by default |
| Forcing exactly 2 options | Best answer is often a sequencing play (do X first, then Y) | Allow 2-3 options. Third must earn its place — not a filler. |
| Agents arguing without numbers | Debate stays philosophical instead of operational | MANDATORY decision-math section in every Stage 5 opening argument |
| Judge writing the action plan | Violates separation of concerns; scoring and planning are different skills | Judge scores and picks winner; `action-plan` skill builds the phased plan in Stage 7 |
| Action plan with soft metrics | "Month 1-2: explore options" is not actionable | Week/month/quarter/year with specific target metrics |
| Action plan without checkpoints | User has no escape hatch if conditions change | Always include decision checkpoints with pivot triggers |
| Agents refusing to concede | Makes arguments less credible, not more | Require concessions — judge scores this explicitly |
| Judge being wishy-washy | "Both options have merit" defeats the purpose | Judge MUST pick a winner with scores |
| Running debate rounds in wrong order | Round 2 needs Round 1 output | Round 1 parallel, Rounds 2-3 sequential |

---

## Customization Flags

| Flag | Effect |
|------|--------|
| `--quick` | Stage 3 uses `--quick`, Stage 4 skips COO (direct analysis), debate is 2 rounds |
| `--deep` | Stage 2 uses `--deep`, Stage 3 uses `--deep`, full 3 rounds everything |
| `--no-questions` | Skip Stage 1/4 Q&A — surface options from research only, then debate |
| `--no-debate` | Skip Stages 5+6 — jump from Stage 4 options directly to `action-plan` |
| `--stage {n}` | Start from a specific stage (if prior stages were already done in conversation) |
| `--3-options` | Force 3 options even if 2 would suffice |

---

## Examples

### Decision Validation
```
/deep-deliberation We should switch our auth from NextAuth to Clerk
```
Devil's-advocate: "Do you have an auth problem or a feature problem?" → last30days surfaces practitioner migration stories → research verifies migration cost claims → COO analysis with migration cost math → 2 agents debate with timeline/cost numbers → judge picks winner → action-plan delivers week-by-week.

### Business Strategy
```
/deep-deliberation Should I go MCP-first or web app for my SaaS?
```
Devil's-advocate: "Do you have paying users yet? If not, why are you debating distribution?" → last30days captures how solo devs are actually hitting $5K MRR → research verifies solo-dev revenue benchmarks → COO maps constraints → 3 agents debate (web app, MCP-only, hybrid sequencing) with revenue math → judge delivers verdict → action-plan gives week/month/quarter/year.

### Technical Claim
```
/deep-deliberation Server components are always faster than client components
```
Challenges the absolutism → last30days scans practitioner perf reports → research fetches benchmarks and docs → surfaces 2 options → debate with performance numbers → verdict → action-plan (if applicable).

---

## Verification Checklist

After running the full pipeline:

- [ ] Stage 1: `devils-advocate` was invoked, challenged at least one assumption, asked constraint-revealing questions
- [ ] Stage 1: Research Brief has HARD CONSTRAINTS (not just strategy preferences)
- [ ] Stage 2: `last30days` was invoked, targeted practitioner stories, not just pundit opinions
- [ ] Stage 3: `research` was invoked with a query built from Stage 2 community claims; results classified as VERIFIED / REFUTED / PARTIALLY TRUE / UNVERIFIABLE
- [ ] Stage 4: `coo` was invoked for systems thinking and constraints analysis
- [ ] Stage 4: 2-3 options surfaced (not forced exactly 2), every option has DECISION MATH with specific numbers on the dimensions that matter
- [ ] Stage 5: Every agent quantified the decision's stakes in opening arguments
- [ ] Stage 5: Agents attacked each other's numbers, not just philosophy
- [ ] Stage 5: Both/all agents conceded at least one point (good faith check)
- [ ] Stage 6: `judge` scored QUANTITATIVE RIGOR as a separate criterion
- [ ] Stage 6: Judge picked a clear winner (not a tie or "both are good")
- [ ] Stage 6: Judge did NOT write the action plan (that's Stage 7's job)
- [ ] Stage 7: `action-plan` produced FOUR time horizons: week, month, quarter, year
- [ ] Stage 7: Each time horizon has a specific TARGET METRIC
- [ ] Stage 7: Decision checkpoints exist with pivot triggers
- [ ] Stage 7: Flip Conditions give the user explicit permission to change course
