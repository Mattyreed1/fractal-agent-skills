# Template: Checklist / Cheat Sheet Lead Magnet

## What This Is
A downloadable checklist or cheat sheet (markdown or PDF) with 7-15 actionable items. Quick-reference format designed to be printed or bookmarked.

## When to Use
The conversation contains a sequential process, a set of best practices, or a collection of do/don't rules. Look for:
- Step-by-step setup or configuration processes
- Best practices for a specific tool or workflow
- Common mistakes with corrections
- Evaluation criteria or scoring rubrics
- "Things I wish I knew before..." lists

## Structure

```markdown
# {Title}: {Number}-Point {Type} for {Audience}

{1-2 sentence intro — what this solves and why it matters}

## The Checklist

- [ ] **{Action verb + specific task}**
  {One line — why this matters or what happens if you skip it}

- [ ] **{Action verb + specific task}**
  {One line — why this matters}

... (7-15 items)

## Quick Wins (start here)
Items marked with ⚡ can be done in under 10 minutes:
⚡ Item 3: {reason this is fast and high-impact}
⚡ Item 7: {reason this is fast and high-impact}

## Common Mistakes
- ❌ {Mistake} → ✅ {Correction}
- ❌ {Mistake} → ✅ {Correction}

---
Built by the user · fractalai.tech
```

## Title Formula
`[Number] [Action] [Type] for [Audience] to [Outcome]`

Examples:
- "12-Point Agent Workflow Checklist for Solo Founders"
- "MCP Server Setup Cheat Sheet: 9 Steps to Production"
- "The n8n Automation Audit: 15 Things to Check Before You Ship"

## Quality Checks

| Check | Pass | Fail |
|-------|------|------|
| Every item starts with action verb | "Configure", "Verify", "Remove" | "SSL certificates" (noun, not action) |
| Items are sequenced logically | Do this before that | Random order |
| 7-15 items | Enough to be comprehensive, not overwhelming | 3 (too thin) or 25 (too long) |
| Quick wins marked | 2-3 items flagged as fast + high-impact | No prioritization |
| No filler items | Each one makes you think "oh, I should check that" | Generic advice anyone knows |
| Companion post written | LinkedIn post using template | Checklist shipped without promotion |

## Notion Storage
Save to **Content DB** (`<CONTENT_DB_ID>`) with:
- Content type: Lead Magnet
- Format: Checklist
- Status: Draft
