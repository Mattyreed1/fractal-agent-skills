---
name: n8n-to-cc
description: Convert or replace an n8n automation with a Claude Code automation — webhook-triggered Claude Code Routine fires a session against a Claude Code project repo where a skill does the actual work. Use when migrating an existing n8n workflow to Claude Code, when building a new webhook → Claude Code automation from scratch, or when deciding whether something currently in n8n should move. Triggers on "convert this n8n to claude code", "replace this n8n workflow", "move this automation to a routine", "should this be in n8n or a skill", "build a webhook to claude code automation", "rebuild this n8n in claude code".
license: MIT
metadata:
  version: 1.0.0
---

# n8n → Claude Code conversion

Convert n8n workflows into Claude Code Routines + a project-side skill. The reference implementation is the MR.EA `meeting-notes` pipeline that replaced a 22-node n8n workflow with a 5-node forwarder + a versioned skill.

For n8n-side details (node configs, expression syntax, MCP tooling) defer to the `n8n` skill — load it alongside this one.

## The architecture

```
External service (Fathom / Calendly / Stripe / ...)
       │  webhook (existing URL — don't change it)
       ▼
n8n forwarder workflow (3-5 nodes)
  ├── Webhook node (receives POST)
  ├── Code node (compact + flatten the payload)
  ├── [Optional] HTTP node (upload large blobs / files to Drive/S3)
  ├── HTTP node (stage compact payload in Convex / Notion inbox / similar)
  └── HTTP node (POST /v1/claude_code/routines/{id}/fire with small reference text)
       │
       ▼
Claude Code Routine fires → CCR session clones the linked GitHub repo
       │
       ▼
Skill in the repo runs:
  1. Parse text, fetch staged payload from store
  2. Run LLM calls (categorize, transform, extract — verbatim prompts from old n8n)
  3. Write to all target systems (Notion, KG, Drive, Slack, etc.)
  4. Update dedup ledger on the staging entity (processed: true + side-effect-id)
```

**Why this shape:** the external service already knows the n8n webhook URL, so n8n stays as the ingress. Everything that USED to be n8n's responsibility (AI logic, structured writes, conditional branching) moves into a versioned, repo-tracked skill. n8n shrinks to ~3-5 nodes of plumbing.

See [`references/architecture-patterns.md`](references/architecture-patterns.md) for the full pattern catalogue.

## When to use this approach

| Scenario | Convert to CC routine? |
|---|---|
| n8n workflow has 5+ AI nodes with complex prompts | ✅ — versioned prompts win |
| Workflow needs branching logic and multi-system writes | ✅ — skill is more debuggable |
| Workflow is purely "if X then call API Y" with no AI | ❌ — keep in n8n |
| Need real-time webhook trigger | ✅ — routines support this |
| Need scheduled execution only | ⚠️ — use the `schedule` skill instead (cron-style routines) |
| Multi-tenant or customer-facing | ❌ — n8n is more isolatable |

## The 9-step migration checklist

1. **Get the existing workflow JSON.** Use the `n8n_get_workflow` MCP tool (the `mcp__<server>__` prefix matches your n8n MCP server name; defer to the `n8n` skill).
2. **Extract every AI prompt verbatim** into separate `prompts/<name>.md` files inside the new skill. Don't paraphrase — copy exactly. The same prompts that worked in n8n work in Claude Code.
3. **Extract every external system mapping** (Notion DB IDs + property keys, Drive folder IDs, Slack channels, etc.) into `references/<system>-mapping.md` files.
4. **Document the webhook payload shape** at `references/payload-schema.md`. Include both raw shape and any compaction that happens.
5. **Build the minimal n8n forwarder** (see [`references/n8n-side.md`](references/n8n-side.md) for the 3-5 node template). Reuse existing OAuth credentials. NO AI logic in n8n.
6. **Create the Claude Code Routine** at https://claude.ai/code/routines linked to your project repo. Static prompt: "Invoke the `<skill-name>` skill against this payload." Body shape: `{text}` template variable.
7. **Configure routine env** — set network allowlist to `Custom` with the hostnames the skill needs (Convex deployment, etc.). See [`references/ccr-constraints.md`](references/ccr-constraints.md).
8. **Test fire end-to-end** with a real payload. Verify side effects (Notion writes, KG entries) — don't trust HTTP 200, there's no session-status API. See [`references/migration-checklist.md`](references/migration-checklist.md) for the verification recipe.
9. **Swap the webhook path** on the new workflow to match the legacy path, then deactivate the old workflow. The external service keeps its existing URL with zero reconfig.

Detailed walkthrough: [`references/migration-checklist.md`](references/migration-checklist.md).

## Hard constraints to design around

| Constraint | Implication |
|---|---|
| Routine `text` body capped at **65,536 chars** | Stage large payloads externally; pass a reference id |
| No GET / PATCH on routines | Prompt + env vars are UI-only at claude.ai/code/routines |
| No session-status endpoint | Detect success via side effects, not API polling |
| CCR has a per-routine network allowlist | Default blocks arbitrary HTTPS — add custom domains via UI |
| CCR clones the repo from GitHub at session start | Symlinks pointing outside the repo are dangling; real files only |
| No local-Mac binaries available in CCR | No `gws`, no `~/.local/bin`, no project-local `node_modules`. Move that step to n8n or call public HTTPS |

Full breakdown: [`references/ccr-constraints.md`](references/ccr-constraints.md).

## Sizing the n8n vs skill split

| Belongs in n8n | Belongs in the skill |
|---|---|
| Webhook ingress (preserves external service's URL) | Every LLM call |
| Credential-bearing nodes (Google Drive OAuth, Notion writes that have to happen before routine fires) | Every prompt |
| Payload compaction (Code node) | Every conditional write (Notion / KG / Drive / Slack) |
| External staging (HTTP node → Convex / inbox) | Multi-step branching logic |
| Routine fire (HTTP node) | Dedup ledger updates |
| **NO AI logic** | **All AI logic** |

If you're tempted to add a Switch node or an LLM call in n8n, push it into the skill instead. n8n's job is forwarding.

## Every AI/LLM node becomes a Claude call — pick the model deliberately

When migrating, **drop every OpenAI / Gemini / Anthropic-API node** and replace it with a Claude call inside the skill. The CCR session running the routine IS Claude — it reads the prompt and emits the output natively. No external LLM provider needed. This means:

- Delete the `langchain.agent` / `langchain.openAi` / `langchain.lmChatGoogleGemini` nodes entirely.
- Delete the API-key credentials (`OpenAi account`, `MR - Gemini`, etc.) — the routine doesn't need them.
- The prompt body from those nodes lives at `prompts/<name>.md`. The skill reads it and Claude responds.
- Anywhere the old workflow said `model: "gpt-5-mini"` or `model: "models/gemini-3.1-pro-preview"`, the migrated skill says "Claude runs this prompt" — see the model table below for which Claude.

### Two execution surfaces in a Claude Code session

| Surface | What runs it | When to use it |
|---|---|---|
| **The session itself** (the routine's main loop) | The model configured on the routine at claude.ai/code/routines | Multi-step orchestration: read SKILL.md, call MCP tools, chain decisions, write to systems. ONE model per routine. |
| **Sub-agents** (via the `Task` / `Agent` tool from inside the session) | A model you pick PER sub-agent call | Per-step model tuning: spin up Haiku for cheap classification, Opus for important reasoning, Sonnet as the middle ground. |

The session model is the floor for what the routine can do — pick it for the most complex step. Within that session, delegate cheap sub-tasks to smaller models via `Agent({model: "haiku"})` so you don't burn Opus budget on classification.

### Model selection table

| Old n8n node looked like | Claude model | Why |
|---|---|---|
| Small model classifying meeting type / lead source / status into a fixed enum | **Haiku** (latest) | Single-label classification, low latency, cheap. Verbatim n8n prompt is already minimal — Haiku handles it. |
| Gemini / GPT agent extracting structured JSON from a transcript or document | **Sonnet** (latest) | Long context + structured output + decent reasoning. Sonnet is the workhorse here. |
| Agent doing complex multi-step analysis (e.g. discovery-call notetaker producing 15 fields including inferred cost estimates) | **Opus** (latest) | Multi-field reasoning, nuanced judgment, output feeds a real client document. Use Opus. |
| Customer-facing / client-facing text generation (proposals, emails, follow-ups, public posts, marketing copy) | **Opus** (latest) | Voice and judgment matter; never default to a smaller model for anything a human external to you reads. |
| Internal writing for KG / notes (Obsidian-style blocks, internal summaries) | **Sonnet** or **Opus** | Sonnet is fine if structured; Opus if you need synthesis across many sources. |
| Agent / orchestration step that picks among tools and writes to multiple systems | **Opus** (latest) | This IS the agent — give it the best model. |
| Trivial transformations a regex / Python one-liner could do | **No LLM at all** | Move to JS in the n8n Code node or to a Python script in the skill. |

**"Latest" = whichever Opus / Sonnet / Haiku is current at session time.** Don't pin a specific version (e.g. `claude-opus-4-7-20260101`) unless you have a documented reason — the unversioned alias auto-rolls forward. The Task / Agent tool's `model` parameter takes `"opus"` / `"sonnet"` / `"haiku"` and resolves to current.

### How this maps to SKILL.md orchestration

```
Routine model = Opus (latest)          ← set this in routine config at claude.ai/code/routines
  │
  ├── Step 1: Categorize
  │     → Agent({model: "haiku", prompt: "<prompts/categorize.md with substitutions>"})
  │     → returns one of 6 labels in ~1s
  │
  ├── Step 2: Notetake (branch on category)
  │     → If discovery: Agent({model: "opus",   prompt: "<prompts/discovery-notetaker.md>"})
  │     → Else:         Agent({model: "sonnet", prompt: "<prompts/misc-notetaker.md>"})
  │     → returns structured JSON with all the fields
  │
  ├── Step 3–5: Notion / Drive / Task writes
  │     → Main session (Opus) decides which DBs, looks up existing entities, writes
  │     → No additional LLM calls — just MCP tool invocations
  │
  └── Step 6: KG block append
        → Main session (Opus) generates the Obsidian block inline; no sub-agent needed
          since this is templating-heavy work the session is already doing
```

**Rule of thumb:** the session model runs the orchestration (always Opus for non-trivial pipelines). Delegate cheap, well-bounded sub-tasks to Haiku/Sonnet via `Agent`. Never spend Opus on "is this email A or B" — that's a Haiku call. Never compromise output quality on client-facing writing — always Opus.

### Why not just always use Opus

Cost + latency. A pipeline that fires 10 times a day with Haiku categorize + Sonnet notetaker + Opus orchestration is a few dollars/day. Same workload all-Opus is 5–10x that. For client-facing work the spend is justified; for internal classifications it's wasteful.

### Anti-patterns

| Avoid | Why |
|---|---|
| Keeping the OpenAI / Gemini API calls in the skill "for parity" | The session is already Claude — external calls add latency, cost, and a second auth surface for no benefit |
| Setting the routine to Haiku to save money | Haiku can't do the orchestration. Set routine to Opus; delegate down to Haiku for sub-tasks |
| Calling Opus for trivial classification | Use Haiku via Agent tool |
| Calling Haiku for client-facing writing | Use Opus — never compromise output quality on the work humans see |
| Hardcoding a dated model version (e.g. `claude-opus-4-7-20260101`) in prompts | The unversioned alias auto-rolls forward — don't pin unless you have a reason |

## Cross-references

- **`n8n` skill** — authoritative for n8n-side: workflow JSON, node configs, expression syntax, MCP tooling. Always load alongside this skill when doing the conversion.
- **`schedule` skill** — for cron-style routines (no webhook). Different mental model.
- **`notion` skill** — when the target writes are to Notion.
- **`knowledge-graph` skill** — when the skill should also update Matty's shared KG.
- **`skill-translate` skill** — different concern (porting a Claude Code skill TO Molty/Codex). Don't conflate.

## References

| File | Purpose |
|---|---|
| [`references/architecture-patterns.md`](references/architecture-patterns.md) | Pattern catalogue — webhook forwarder, direct API trigger, scheduled routine, plus staging/dedup/multi-write/cross-skill sub-patterns |
| [`references/ccr-constraints.md`](references/ccr-constraints.md) | CCR sandbox constraints — filesystem/symlink rules, network allowlist, unavailable local binaries, env vars, known gotchas |
| [`references/claude-code-routines-api.md`](references/claude-code-routines-api.md) | Full Routines API spec — fire endpoint, auth + beta headers, error responses, UI-only config surface, n8n/curl/Python trigger examples |
| [`references/migration-checklist.md`](references/migration-checklist.md) | Detailed 4-phase migration walkthrough with verification gates (extract → build → test → cut over) |
| [`references/n8n-side.md`](references/n8n-side.md) | Minimal 3-5 node forwarder template — compact-payload Code node, Convex staging, routine-fire HTTP node, expression gotchas |
| [`references/skill-side.md`](references/skill-side.md) | How to structure the processing skill in the repo — canonical layout, SKILL.md orchestration shape, prompt files, mapping files, helper scripts |

## Worked example: MR.EA meeting-notes

The MR.EA `meeting-notes` skill replaced a legacy 22-node n8n workflow (2 LLM providers, sticky-note documentation). The new shape:

- **n8n forwarder** — 5 nodes: Webhook → Compact Payload (Code) → Upload to Drive → Stage in Convex → Fire Routine.
- **Routine** — points at the project repo; custom network allowlist includes the project's Convex deployment.
- **Skill** at `skills/meeting-notes/` in the repo: SKILL.md (7-step orchestration) + 3 prompt files (categorize, misc-notetaker, discovery-notetaker — all verbatim from n8n) + 5 reference files (notion-mapping, company-linking, project-linking, kg-write, payload-schema).
- Live as of 2026-05-18; verified with real 414-segment Fathom payload.

## Verification checklist

After conversion:

- [ ] All prompts in `prompts/*.md` are verbatim from the n8n workflow
- [ ] All DB IDs + property keys in `references/*-mapping.md` retrieved from the live data sources (not paraphrased)
- [ ] Network allowlist includes every host the skill calls (Convex, custom APIs)
- [ ] Skill files are real (no symlinks pointing outside the repo) — `scripts/check_ccr_skills.sh` passes if you have it
- [ ] Dedup ledger pattern in place (Step 0 of skill checks `processed`)
- [ ] Real-shaped payload fires end-to-end with side effects landing
- [ ] Old workflow can be deactivated as a safe rollback (keep it for 30 days)

## Anti-patterns

| Avoid | Why | Instead |
|---|---|---|
| Paraphrasing prompts during the move | Loses years of tuning; introduces drift | Copy verbatim into `prompts/*.md` |
| Adding AI logic back into n8n | Splits the source of truth | All AI in the skill |
| Creating a new webhook URL the user has to register | Forces external-service reconfig | Swap the path on the new workflow at the end so the old URL keeps working |
| Treating HTTP 200 from routine fire as success | The routine session might fail silently | Verify side effects |
| Inlining the full payload in `text` | Will hit the 65k cap on long inputs | Stage externally, pass a reference id |
| Calling local-Mac binaries (`gws`, etc.) from the skill | They don't exist in CCR | Move to n8n or call public HTTPS |
| Symlinks pointing outside the project repo | Dangling in CCR clones | Real files only; reverse the symlink direction at the local Mac boundary |
