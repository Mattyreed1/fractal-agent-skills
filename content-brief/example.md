# Example: Agent Memory — Content Context Brief

> Ported example from the agent fleet's content-ideation skill. Demonstrates the level of specificity the brief format expects.

## File Saved
`projects/fractal-ai-content/2026-04-20-agent-memory/brief.md`

## Brief

# Content Context Brief — Agent Memory

**Date:** 2026-04-20
**Platform:** LinkedIn Post
**Status:** Draft

## Core Insight
AI agents lose all context between sessions. A 4-layer memory architecture (working → short-term → medium-term → long-term) gives agents persistent memory that compounds over time.

## Why This Matters
Every builder hitting agent limitations is fighting the same problem — agents that can't remember yesterday. This architecture is battle-tested in production with 5 concurrent agents sharing a knowledge graph.

## Proof & Artifacts
- 5 agents running 24/7 with shared memory for 3+ months
- Real Convex schema (kg_entities, kg_relations tables)
- Weekly consolidation cron extracting facts from memory files into KG
- MEMORY.md weekly buffer pattern with 8KB size limit
- Retrieval cascade: 6-step lookup order used in every session

## Source
Fractal AI agent team architecture

## Target Audience
Builders/developers working with AI agents, frustrated by context loss

## Lead Magnet
GitHub repo — fractal-agent-team-memory (templates, schemas, prompts, examples)

## Visual Suggestions
1. Architecture data flow diagram: 5 components as boxes, labeled arrows for write/read paths
2. KG visualization: circular nodes (the user, Fractal AI, agents, projects) with labeled relationship edges

## Related Links
- Convex schema: the board/convex/schema.ts
- KG functions: the board/convex/kg.ts

## Raw Context
[KG excerpts, memory notes, and project details go here — the writer mines this when drafting hooks/script]
