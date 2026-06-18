# Format Selection Guide

This is the Phase 2 (CLASSIFY) decision tree. Given the extracted insights from Phase 1, determine which output formats they best serve.

## Output Format Catalog

### Social Content

| Format | Best For | Minimum Insights |
|--------|----------|-----------------|
| **LinkedIn Post** | 1 strong insight (gravity ≥4) with personal angle, or 1 principle + 1 war story | 1-3 insights |

### Functional Lead Magnets

| Format | Best For | Minimum Insights | Template |
|--------|----------|-----------------|----------|
| **Workflow (n8n)** | Conversations containing automation logic, multi-step processes, integration patterns | 1 framework + tool/tactics showing implementation | `lead-magnet-workflow.md` |
| **Resource DB (Notion)** | Conversations containing structured collections, tracking systems, evaluation criteria | 1 framework that maps to rows/columns | `lead-magnet-notion-db.md` |
| **Agent Skill (Claude)** | Conversations containing repeatable processes, specialized knowledge, decision trees | 1 framework with clear phases + verification | `lead-magnet-skill.md` |

### Written Lead Magnets

| Format | Best For | Minimum Insights | Template |
|--------|----------|-----------------|----------|
| **Checklist** | Sequential processes, best practices, do/don't rules | 1 framework with 7-15 discrete steps | `lead-magnet-checklist.md` |
| **Mini-Guide** | Deep frameworks with examples and case studies | 1 framework + 2 war stories/data points | `lead-magnet-mini-guide.md` |

## Decision Tree

```
START: Review the Insight Map from Phase 1
  │
  ├─ Does the source contain a WORKFLOW PATTERN?
  │   (multi-step automation, integration logic, n8n nodes)
  │   YES → Recommend: Workflow Lead Magnet + Companion LinkedIn Post
  │
  ├─ Does the source contain a STRUCTURED COLLECTION?
  │   (tool lists, tracking systems, evaluation criteria)
  │   YES → Recommend: Notion DB Lead Magnet + Companion LinkedIn Post
  │
  ├─ Does the source contain a REPEATABLE AGENT PROCESS?
  │   (skill-shaped: triggers, phases, verification)
  │   YES → Recommend: Agent Skill Lead Magnet + Companion LinkedIn Post
  │
  ├─ Does the source contain a SEQUENTIAL PROCESS with 7+ steps?
  │   (setup guide, audit checklist, implementation steps)
  │   YES → Recommend: Checklist Lead Magnet + Companion LinkedIn Post
  │
  ├─ Does the source contain a DEEP FRAMEWORK with case studies?
  │   (methodology + war stories + data)
  │   YES → Recommend: Mini-Guide Lead Magnet + Companion LinkedIn Post
  │
  └─ Does the source have 1+ insights with gravity ≥ 4?
      YES → Recommend: LinkedIn Post (standalone)
      NO  → Source lacks enough publishable material. Tell user.
```

## Scoring Matrix

For each candidate format, score 1-5 on these criteria:

| Criterion | Question |
|-----------|----------|
| **Insight fit** | Do the extracted insights naturally map to this format? |
| **Audience value** | Would the target audience find this genuinely useful? |
| **Buildability** | Can this be built from the source material without major gaps? |
| **Promotability** | Does this have a clear companion post angle? |

**Threshold**: Only recommend formats scoring ≥ 3 on ALL criteria.

## Multi-Output Rule

One conversation can (and often should) produce MULTIPLE outputs:
- A **lead magnet** (the artifact) + a **LinkedIn post** (the promotion)
- Multiple LinkedIn posts from different insight clusters
- A checklist AND a workflow from the same framework

Present all viable options ranked by total score. Let the user choose.

## Companion Post Rule

**Every lead magnet MUST have a companion LinkedIn post.** A lead magnet without promotion content is a tree falling in an empty forest. The companion post:
- Leads with the PROBLEM the lead magnet solves
- Tells a personal story related to the topic
- CTA drives to the lead magnet

## Phase 2 Gate
- At least 1 format recommended with reasoning
- Each recommendation tied to specific extracted insights (by number)
- User confirmation received before proceeding to Phase 3
