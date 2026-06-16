---
name: skillforge
description: "Intelligent skill router and creator for Claude Code skills. Use when users want to: (1) create a new skill, (2) update or improve an existing skill, (3) find which skill handles a task, (4) check for duplicate skills before creating one. Analyzes input, scans existing skills for overlap, then routes to recommend, improve, or create. Includes Phase 0 triage to prevent duplicates, deep analysis with 11 thinking models, and multi-agent synthesis panel for quality assurance."
license: MIT
metadata:
  version: 4.1.0
---
# SkillForge - Intelligent Skill Router & Creator

Analyze ANY input to find, improve, or create the right skill.

## Quick Start

```
SkillForge: create a skill for automated code review
→ Creates new skill (after checking no duplicates exist)

improve the testgen skill to handle React components better
→ Enters improvement mode for TestGen

do I have a skill for database migrations?
→ Recommends matching skills
```

## Triggers

* `SkillForge: {goal}` \- Full autonomous skill creation
* `create skill` / `design skill for {purpose}` \- Creation mode
* `do I have a skill for` / `which skill` \- Search existing
* `improve {skill-name} skill` \- Enhancement mode
* `skillforge --plan-only` \- Specification only\, no execution

| Input | Output | Quality Gate |
| ----- | ------ | ------------ |
| Any input | Triage → Route → Action | Phase 0 analysis |
| Explicit create | New skill | Unanimous panel approval |
| Task/question | Skill recommendation | Match confidence ≥60% |

***

## Core Principles

### Concise is Key

The context window is a public good. Skills share it with system prompt, conversation history, other skills, and user requests. **Claude is already very smart** — only add context it doesn't already have. Challenge each piece of information: "Does this paragraph justify its token cost?"

### Set Appropriate Degrees of Freedom

| Freedom Level | When to Use | Example |
| ------------- | ----------- | ------- |
| **High** (text instructions) | Multiple approaches valid, context-dependent | Style guides |
| **Medium** (pseudocode/params) | Preferred pattern exists, some variation OK | API workflows |
| **Low** (specific scripts) | Fragile operations, consistency critical | PDF manipulation |

### Progressive Disclosure

1. **Metadata** (name + description) — Always in context (\~100 words)
2. **SKILL.md body** — Loaded when skill triggers (keep under 500 lines)
3. **Bundled resources** — Loaded as needed by Claude (unlimited)

Keep SKILL.md lean. Move deep documentation to `references/`. Reference files should link directly from SKILL.md — avoid deeply nested references.

### What NOT to Include

Do NOT create: README.md, CHANGELOG.md, INSTALLATION\_GUIDE.md, QUICK\_REFERENCE.md, or any auxiliary documentation. A skill should only contain information needed for an AI agent to do the job.

***

## Process Overview

```
ANY INPUT → Phase 0: Triage → Route Decision
                                    │
        ┌──────────┬────────────┬───┴──────┬──────────┐
        USE        IMPROVE     CREATE      QUICK      COMPOSE
        (recommend)(enhance)   (full pipe) (lightweight)(chain)
                                │           │
                          Phases 1-4    6-step process
                          (deep)        (init → edit → validate)
```

**Key principles:**

* Phase 0 prevents duplicates — always check existing skills first
* Phase 0 picks the right creation path — full pipeline or lightweight
* Every decision announced to user with reasoning before proceeding

***

## Phase 0: Skill Triage

Before creating anything, classify input and scan existing skills.

| Action | When | Result |
| ------ | ---- | ------ |
| **USE\_EXISTING** | Match ≥80% | Recommend existing skill(s) |
| **IMPROVE\_EXISTING** | Match 50-79% | Load skill, enter enhancement mode |
| **QUICK\_CREATE** | Match <50% + simple skill | Lightweight 6-step process |
| **CREATE\_NEW** | Match <50% + complex skill | Full Phase 1-4 pipeline |
| **COMPOSE** | Multi-domain | Suggest skill chain |
| **CLARIFY** | Ambiguous or duplicate | Ask user to clarify |

### Creation Route: QUICK\_CREATE vs CREATE\_NEW

When a new skill is needed, Phase 0 decides the creation path:

| Signal | → QUICK\_CREATE | → CREATE\_NEW |
| ------ | -------------- | ------------ |
| **Workflows** | Single linear workflow | Multi-phase, branching logic |
| **Scripts** | None needed (SKILL.md only) | Needs automation/validation scripts |
| **Domain** | Single, well-understood domain | Cross-domain or novel territory |
| **References** | 0-1 reference files | Multiple reference files needed |
| **Scope** | User's request is clear and bounded | Ambiguous, needs deep analysis |
| **Agentic** | No autonomous operation needed | Self-verification, state mgmt |

**Overrides** — User can always force a route:

| Flag | Effect |
| ---- | ------ |
| `--quick` | Force QUICK\_CREATE regardless of complexity |
| `--full` or `ultimate skill` | Force CREATE\_NEW regardless of simplicity |

**Announce before proceeding:**

```
→ QUICK_CREATE: Simple single-domain skill, no scripts needed.
  Using lightweight 6-step process. Say "--full" to override.
```

```
→ CREATE_NEW: Multi-phase skill with automation scripts needed.
  Using full SkillForge pipeline. Say "--quick" to override.
```

```bash
# Run triage
python scripts/triage_skill_request.py "help me debug this error"

# Rebuild skill index
python scripts/discover_skills.py
```

***

## QUICK\_CREATE: Lightweight 6-Step Process

For simple, well-scoped skills. No synthesis panel, no XML spec, no 11-lens analysis.

1. **Understand** — Gather concrete examples. Ask: "What would a user say that should trigger this?" Conclude when usage patterns are clear.
2. **Plan resources** — Identify what scripts, references, and assets are needed (often: none).
3. **Initialize** — Run `scripts/init_skill.py <name> --path ~/.claude/skills` to scaffold.
4. **Edit** — Write SKILL.md following template. Implement any resources. Test scripts.
5. **Validate** — Run `python scripts/quick_validate.py <skill-dir>`. Fix any errors.
6. **Iterate** — Use on real tasks, improve based on experience.

**Quality bar:** Frontmatter valid, description includes when-to-use, 3-5 triggers, under 500 lines, no forbidden files, scripts tested.

***

## CREATE\_NEW: Full Pipeline

For complex, multi-phase, or agentic skills. Deep analysis → specification → generation → panel review.

* **Phase 1:** Deep analysis (11 thinking lenses, regression questioning, automation analysis)
* **Phase 2:** XML specification with all decisions documented + WHY
* **Phase 3:** Generation (fresh context, zero errors, init\_skill.py → edit → verify)
* **Phase 4:** Multi-agent synthesis panel (3-4 agents, unanimous approval)
* **Phase 5 (optional):** Hand off to `skill-creator` for eval-driven iteration — subagent test runs, benchmark viewer, description optimization via `run_loop.py`. Invoke when the user wants data-driven quality assurance beyond panel approval.

**Quality bar:** Everything in QUICK\_CREATE + timelessness score ≥7, extension points documented, unanimous panel approval.

See: [references/deep-dive-phases.md](references/deep-dive-phases.md) for full phase details.

### Writing SKILL.md

**Frontmatter** — Write `name` and `description`. The description is the primary trigger mechanism — include both what the skill does AND when to use it. Do not put "When to Use" sections in the body; the body only loads after triggering.

**Body** — Use imperative/infinitive form. Prefer concise examples over verbose explanations. Use tables over prose for structured information.

### Frontmatter Requirements

| Property | Required | Constraints |
| -------- | -------- | ----------- |
| `name` | Yes | Hyphen-case, ≤64 chars |
| `description` | Yes | ≤1024 chars, no `<` or `>`, includes when-to-use |
| `license` | No | MIT, Apache-2.0, etc. |
| `allowed-tools` | No | Restrict tool access |
| `metadata` | No | Custom fields (version, model, etc.) |

No other top-level frontmatter properties are allowed.

***

## Skill Output Structure

```
~/.claude/skills/{skill-name}/
├── SKILL.md                    # Main entry point (required)
├── references/                 # Deep documentation (loaded as needed)
├── assets/                     # Templates, images, fonts (used in output)
└── scripts/                    # Automation scripts (executed directly)
```

**Scripts** enable agentic operation. Include when operations are deterministic, repeatable, or need self-verification. Requirements: Python 3.x, standard library only, `Result` dataclass pattern, documented exit codes.

See: [references/script-integration-framework.md](references/script-integration-framework.md)

***

## Validation & Packaging

**Validation mechanics are canonical in `skill-creator`** (decision 2026-06-10): `scripts/quick_validate.py` here is a symlink to `skill-creator/scripts/quick_validate.py`. Edit the frontmatter allowlist and validation rules THERE only — never fork a second copy. skillforge's role is routing (Phase 0 triage, dedup, recommend/improve/create); skill-creator owns validation + evals.

```bash
# Quick validation (symlink → skill-creator's canonical validator)
python scripts/quick_validate.py ~/.claude/skills/my-skill/

# Full validation
python scripts/validate-skill.py ~/.claude/skills/my-skill/

# Package for distribution
python scripts/package_skill.py ~/.claude/skills/my-skill/ ./dist
```

***

## Anti-Patterns

| Avoid | Why | Instead |
| ----- | --- | ------- |
| Duplicate skills | Bloats registry | Run Phase 0 triage first |
| Single trigger | Hard to discover | 3-5 varied trigger phrases |
| No verification | Can't confirm success | Measurable outcomes |
| Over-engineering | Complexity without value | Start simple, iterate |
| Missing WHY | Can't evolve | Document rationale for decisions |
| Invalid frontmatter | Can't package | Use only allowed properties |
| SKILL.md over 500 lines | Context bloat | Move deep content to references/ |
| Forbidden aux files | Clutter | No README, CHANGELOG, etc. |
| "When to use" in body | Never triggers | Put in description field |

***

## Verification Checklist

* [ ] Frontmatter valid (only allowed properties)
* [ ] Name is hyphen-case, ≤64 chars
* [ ] Description ≤1024 chars, no `<>`, includes when-to-use
* [ ] 3-5 trigger phrases defined
* [ ] SKILL.md under 500 lines
* [ ] No forbidden files (README.md, CHANGELOG.md, etc.)
* [ ] Scripts tested by actually running them
* [ ] `python scripts/quick_validate.py <skill-dir>` passes

***

## Extension Points

1. **Additional Lenses** — Add thinking models to `references/multi-lens-framework.md`
2. **New Synthesis Agents** — Extend panel for specific domains
3. **Domain Templates** — Add to `assets/templates/`
4. **Script Patterns** — Add to `references/script-patterns-catalog.md`

***

## References

* [Deep Dive: Phases 1-4](references/deep-dive-phases.md) — Full phase details, analysis, generation, synthesis
* [Regression Questions](references/regression-questions.md) — Complete question bank (7 categories)
* [Multi-Lens Framework](references/multi-lens-framework.md) — 11 thinking models guide
* [Specification Template](references/specification-template.md) — XML spec structure
* [Evolution Scoring](references/evolution-scoring.md) — Timelessness evaluation
* [Synthesis Protocol](references/synthesis-protocol.md) — Multi-agent panel details
* [Script Integration Framework](references/script-integration-framework.md) — When and how to create scripts
* [Script Patterns Catalog](references/script-patterns-catalog.md) — Standard Python patterns