# Deep Dive: SkillForge Phases 1-4

Detailed reference for each phase of the SkillForge creation pipeline.

## Phase 1: Deep Analysis

### 1A: Input Expansion

Transform user's goal into comprehensive requirements:

| Category | What to Identify |
|----------|-----------------|
| **Explicit** | What the user literally asked for |
| **Implicit** | What they probably expect but didn't say |
| **Unknown unknowns** | Expert-level considerations they'd miss |
| **Domain context** | Related skills, patterns from similar skills |

Check for overlap with existing skills:
```bash
ls ~/.claude/skills/
# Grep for similar triggers in existing SKILL.md files
```

| Match Score | Action |
|-------------|--------|
| >7/10 | Use existing skill instead |
| 5-7/10 | Clarify distinction before proceeding |
| <5/10 | Proceed with new skill |

### 1B: Multi-Lens Analysis

Apply all 11 thinking models systematically:

| Lens | Core Question |
|------|---------------|
| **First Principles** | What's fundamentally needed? |
| **Inversion** | What guarantees failure? |
| **Second-Order** | What happens after the obvious? |
| **Pre-Mortem** | Why did this fail? |
| **Systems Thinking** | How do parts interact? |
| **Devil's Advocate** | Strongest counter-argument? |
| **Constraints** | What's truly fixed? |
| **Pareto** | Which 20% delivers 80%? |
| **Root Cause** | Why is this needed? (5 Whys) |
| **Comparative** | How do options compare? |
| **Opportunity Cost** | What are we giving up? |

**Minimum requirement:** All 11 lenses scanned, at least 5 applied in depth.

See: [multi-lens-framework.md](multi-lens-framework.md)

### 1C: Regression Questioning

Iterative self-questioning until no new insights emerge. Each round ask:
- "What am I missing?"
- "What would an expert in {domain} add?"
- "What would make this fail?"
- "What will this look like in 2 years?"
- "What's the weakest part of this design?"

**Termination:** Three consecutive rounds with no new insights.

See: [regression-questions.md](regression-questions.md)

### 1D: Automation Analysis

For each operation in the skill, determine if scripts are needed:

| Create Script When | Skip Script When |
|-------------------|------------------|
| Operation is deterministic | Requires human judgment |
| Output can be validated | One-time setup |
| Will be reused across invocations | Simple text output |
| Enables autonomous operation | No verification needed |

See: [script-integration-framework.md](script-integration-framework.md)

---

## Phase 2: Specification

Capture all analysis insights in XML format. See: [specification-template.md](specification-template.md)

**Validation before proceeding to Phase 3:**
- All sections present with no placeholders
- Every decision includes WHY
- Timelessness score ≥ 7 with justification
- At least 2 extension points documented
- Scripts section complete (if applicable)

---

## Phase 3: Generation

**Context:** Fresh, clean (no analysis artifacts polluting)

### Generation Order

1. **Initialize skill** — Run `scripts/init_skill.py <name> --path ~/.claude/skills`
2. **Write SKILL.md** — Frontmatter, title, triggers, quick reference, process, anti-patterns, verification, extension points
3. **Generate references** (if needed) — Deep documentation for complex topics
4. **Create assets** (if needed) — Templates for skill outputs
5. **Create scripts** (if needed) — Use script-template.py as base, test before finalizing

### Quality Checks

| Check | Requirement |
|-------|-------------|
| Frontmatter | Only allowed properties — open standard: name, description, license, allowed-tools, metadata, version, compatibility; Claude Code extensions: when_to_use, argument-hint, arguments, disable-model-invocation, user-invocable, disallowed-tools, model, effort, context, agent, hooks, paths, shell |
| Name | Hyphen-case, ≤64 chars |
| Description | ≤1024 chars, no angle brackets, includes when-to-use |
| SKILL.md body | Under 500 lines; deep content in references/ |
| Triggers | 3-5 distinct, natural language |
| No forbidden files | No README.md, CHANGELOG.md, INSTALLATION_GUIDE.md, etc. |
| Scripts tested | Actually run scripts to verify they work |

---

## Phase 4: Multi-Agent Synthesis

**Panel:** 3-4 Opus agents with distinct evaluative lenses
**Requirement:** Unanimous approval

### Panel Composition

| Agent | Focus | When Active |
|-------|-------|-------------|
| **Design/Architecture** | Structure, patterns, correctness | Always |
| **Audience/Usability** | Clarity, discoverability, completeness | Always |
| **Evolution/Timelessness** | Future-proofing, extension, ecosystem | Always |
| **Script/Automation** | Agentic capability, verification, quality | When scripts present |

### Consensus Protocol

- All agents APPROVED → Finalize, validate, complete
- Any CHANGES_REQUIRED → Return to Phase 1 with feedback
- 5 iterations without consensus → Flag for human review

See: [synthesis-protocol.md](synthesis-protocol.md)

---

## Evolution/Timelessness Scoring

| Score | Description | Verdict |
|-------|-------------|---------|
| 1-3 | Transient, will be obsolete in months | Reject |
| 4-6 | Moderate, depends on current tooling | Revise |
| **7-8** | **Solid, principle-based, extensible** | **Approve** |
| 9-10 | Timeless, addresses fundamental problem | Exemplary |

**Requirement:** All skills must score ≥7.

See: [evolution-scoring.md](evolution-scoring.md)

---

## Architecture Pattern Selection

| Pattern | Use When |
|---------|----------|
| **Single-Phase** | Simple linear tasks |
| **Checklist** | Quality/compliance audits |
| **Generator** | Creating artifacts |
| **Multi-Phase** | Complex ordered workflows |
| **Multi-Agent Parallel** | Independent subtasks |
| **Multi-Agent Sequential** | Dependent subtasks |
| **Orchestrator** | Coordinating multiple skills |
