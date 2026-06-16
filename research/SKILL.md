---
name: research
description: Deep web research using Perplexity AI with automatic query routing across search, reasoning, and deep research models. Structures findings into actionable intelligence.
metadata:
  version: 1.0.0
  model: claude-opus-4-6
---

# Perplexity Research

Real-time web research powered by Perplexity AI. Routes queries to the right model tier automatically and delivers structured, citation-backed findings.

---

## Quick Start

```
/research What are the latest changes to the X API v2 media upload endpoints?
```

That's it. The skill picks the right Perplexity model, structures the query for maximum specificity, and returns findings with citations.

---

## Triggers

- `/research {topic}` - Run a research query
- `research this` - Research something from conversation context
- `look this up` - Quick factual lookup
- `deep dive into` - Comprehensive research with multiple angles
- `what's the latest on` - Current information search

---

## Quick Reference

| Need | Command | Perplexity Model |
|------|---------|-----------------|
| Quick fact / lookup | `/research {question}` | `sonar-pro` via `search` |
| Explain / compare / debug | `/research --reason {question}` | `sonar-reasoning-pro` via `reason` |
| Comprehensive report | `/research --deep {topic}` | `sonar-deep-research` via `deep_research` |
| Auto-detect complexity | `/research {anything}` | Auto-routed |

---

## How It Works

```
USER QUERY
    │
    ▼
┌─────────────────────────────────────────┐
│  1. QUERY CLASSIFICATION                │
│  • Simple factual → search              │
│  • Complex/analytical → reason          │
│  • Broad/comprehensive → deep_research  │
│  • Or: user specifies --reason / --deep │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│  2. QUERY ENRICHMENT                    │
│  • Add version numbers, dates, context  │
│  • Include error messages verbatim      │
│  • Specify platform/framework/language  │
│  • Add "as of 2026" for currency        │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│  3. PERPLEXITY MCP CALL                 │
│  • search / reason / deep_research      │
│  • Returns answer + citations           │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│  4. STRUCTURED RESPONSE                 │
│  • Key findings (bullet points)         │
│  • Relevant details                     │
│  • Citations with source links          │
│  • Confidence / caveats                 │
└─────────────────────────────────────────┘
```

### MCP Tools Used

| Tool | Server | Purpose |
|------|--------|---------|
| `mcp__perplexity__search` | perplexity | Quick lookups (sonar-pro) |
| `mcp__perplexity__reason` | perplexity | Complex analysis (sonar-reasoning-pro) |
| `mcp__perplexity__deep_research` | perplexity | Comprehensive reports (sonar-deep-research) |

---

## Commands

| Command | Action |
|---------|--------|
| `/research {query}` | Auto-detect complexity and route |
| `/research --quick {query}` | Force simple search (sonar-pro) |
| `/research --reason {query}` | Force reasoning model |
| `/research --deep {topic}` | Force deep research mode |
| `/research --deep {topic} --focus "area1, area2"` | Deep research with focus areas |

---

## Query Routing Rules

### Auto-Detection (Default)

When no flag is specified, classify the query:

| Signal | Route To | Example |
|--------|----------|---------|
| Simple who/what/when | `search` | "What version of Node.js supports ES modules natively?" |
| How/why/explain/compare/debug | `reason` | "Why does Next.js 15 App Router handle caching differently than Pages Router?" |
| Analyze/comprehensive/survey/landscape | `deep_research` | "Analyze the current state of AI code generation tools in 2026" |
| Error message or stack trace | `reason` | "CORS error when calling Supabase from Next.js middleware" |
| "Latest" / "current" / "new" | `search` | "What's the latest Tailwind CSS version?" |
| Multi-factor comparison | `reason` | "Compare Clerk vs NextAuth vs Supabase Auth for Next.js" |
| Market/industry/trend research | `deep_research` | "State of the creator economy platforms in 2026" |

### Override Flags

- `--quick` / `--q` : Force `search` (fastest, cheapest)
- `--reason` / `--r` : Force `reason` (analytical)
- `--deep` / `--d` : Force `deep_research` (comprehensive, slowest)

---

## Query Enrichment Protocol

Before sending to Perplexity, enrich the query with context. Perplexity performs better with specific, detailed queries.

### Always Include

| Context | Why | Example |
|---------|-----|---------|
| Current date context | Perplexity needs temporal grounding | "as of {current month year}" |
| Tech stack versions | Avoids outdated answers | "Next.js 15, React 19, Supabase" |
| Error messages verbatim | Exact matches find solutions | Include full error text |
| What you've already tried | Avoids obvious suggestions | "Already tried X, didn't work because Y" |
| Platform/OS | Platform-specific answers | "macOS, Vercel deployment" |

### Enrichment Template

```
Original: "how do I fix CORS errors?"

Enriched: "How to fix CORS errors when calling Supabase Edge Functions
from a Next.js 15 App Router application deployed on Vercel, as of
{current month year}. The error is: 'Access-Control-Allow-Origin header is
missing'. Already tried adding headers to next.config.js but the
preflight request still fails."
```

---

## Response Format

Structure all research responses consistently:

### For Quick Searches (`search`)

```markdown
## {Topic}

{Direct answer in 1-2 sentences}

**Key Details:**
- Point 1
- Point 2
- Point 3

**Sources:** [1] url, [2] url
```

### For Reasoning (`reason`)

```markdown
## {Topic}

### Summary
{2-3 sentence overview}

### Analysis
{Structured breakdown of the reasoning}

### Recommendation
{Clear actionable recommendation if applicable}

**Sources:** [1] url, [2] url
```

### For Deep Research (`deep_research`)

```markdown
## {Topic} - Research Report

### Executive Summary
{3-5 sentence overview of findings}

### Key Findings
1. **Finding 1** - detail
2. **Finding 2** - detail
3. **Finding 3** - detail

### Detailed Analysis
{Organized by focus areas if specified}

### Implications / Next Steps
{What this means for the user's context}

**Sources:** [1] url, [2] url, ...
```

---

## Anti-Patterns

| Avoid | Why | Instead |
|-------|-----|---------|
| Vague queries | Perplexity returns generic answers | Add versions, dates, context, error messages |
| Using `deep_research` for simple lookups | Slow and expensive | Let auto-routing pick, or use `--quick` |
| Ignoring citations | Perplexity's strength is sourced answers | Always surface source links |
| Asking about private/internal code | Perplexity searches the public web | Use codebase tools for internal questions |
| Skipping date context | Gets outdated answers | Always ground queries with "as of {current date}" |
| Multi-topic queries in one call | Dilutes answer quality | One topic per research call |
| Treating MCP error `-32001` as a Perplexity outage | It's a ~60s **client-side** timeout (broad `reason`/`search`/`deep_research` calls run long), not a server bug | Narrow the query scope, chain smaller searches instead of one broad call, and warn + retry **once** before escalating |

---

## Examples

### Quick Lookup
```
/research What is the current rate limit for X API v2 free tier?
```
→ Routes to `search`, returns specific numbers with source.

### Debugging Help
```
/research --reason Getting "Module not found: Can't resolve 'next/headers'"
after upgrading to Next.js 15.1. Using App Router with TypeScript.
Package.json shows next@15.1.0.
```
→ Routes to `reason`, analyzes the error in context.

### Deep Research
```
/research --deep Current state of MCP (Model Context Protocol) ecosystem
--focus "available servers, adoption trends, production readiness"
```
→ Routes to `deep_research` with focus areas, returns comprehensive report.

### Context-Aware Research
```
I'm getting a "JWT expired" error in my Supabase auth flow.

/research this
```
→ Picks up conversation context, enriches query, routes to `reason`.

---

<details>
<summary><strong>Deep Dive: Perplexity Model Tiers</strong></summary>

### sonar-pro (via `search`)
- **Speed:** Fast (1-3s)
- **Best for:** Factual lookups, current info, "what is X", version numbers, API docs
- **Token limit:** Standard
- **Cost:** Lowest tier

### sonar-reasoning-pro (via `reason`)
- **Speed:** Medium (3-10s)
- **Best for:** Multi-step reasoning, comparisons, debugging, "why does X happen", architectural decisions
- **Token limit:** Extended for chain-of-thought
- **Cost:** Mid tier

### sonar-deep-research (via `deep_research`)
- **Speed:** Slow (10-60s)
- **Best for:** Comprehensive analysis, market research, technology surveys, "analyze the landscape of X"
- **Token limit:** Largest
- **Cost:** Highest tier
- **Supports:** `focus_areas` parameter for targeted investigation

### Auto-Routing Logic

The Perplexity MCP server has built-in complexity detection. When `force_model: false` (default):
1. Simple patterns → stays on `sonar-pro`
2. Complex patterns (how, why, explain, compare, solve) → upgrades to `sonar-reasoning-pro`
3. Research patterns (analyze, comprehensive, detailed, in-depth) → upgrades to `sonar-deep-research`

The skill's own routing adds a layer on top: it selects which MCP tool to call based on user flags and query classification, giving you explicit control when needed.

</details>

<details>
<summary><strong>Deep Dive: Integration with your product Workflow</strong></summary>

### Common Research Scenarios

| Scenario | Query Pattern |
|----------|--------------|
| X API changes | `/research --reason Latest X API v2 changes affecting media upload, as of {date}` |
| Content strategy | `/research --deep Content repurposing best practices for creator economy 2026` |
| Tech stack decisions | `/research --reason Compare {option A} vs {option B} for {use case}` |
| Bug investigation | `/research {exact error message} in {framework} {version}` |
| Dependency evaluation | `/research --reason Is {package} actively maintained? Last release, open issues, alternatives` |

### Pairing with Other Skills

| Research Need | Then Use |
|--------------|----------|
| Research a topic → write about it | `/research` then `/writing` |
| Research best practices → build workflow | `/research` then n8n skills |

</details>

---

## Verification Checklist

After using this skill:

- [ ] Query was enriched with versions, dates, and context before sending
- [ ] Correct model tier was used (not over/under-powered for the question)
- [ ] Response includes citations / source links
- [ ] Findings are structured (not raw dump)
- [ ] Private/internal questions were NOT sent to Perplexity (use local tools instead)
