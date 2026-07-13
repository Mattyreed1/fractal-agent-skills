# Skill side — how to structure the processing skill

## Contents

- Canonical layout
- SKILL.md shape (the orchestration)
- Prompt files (verbatim from old n8n)
- Reference files (system mappings)
- Payload schema doc
- Helper scripts
- What NOT to put in the skill
- The 7-step pattern (the MR.EA reference)

The skill lives in the GitHub repo that the routine clones at session start. This file documents the canonical layout, the orchestration shape, and the file types you'll want.

## Canonical layout

```
<repo>/skills/<skill-name>/
├── SKILL.md                            # Orchestration (10-step flow)
├── prompts/
│   ├── categorize.md                   # Verbatim from old n8n node
│   ├── transform-discovery.md          # Verbatim from old n8n node
│   └── transform-misc.md               # Verbatim from old n8n node
└── references/
    ├── payload-schema.md               # What `text` looks like + how to fetch the staged payload
    ├── <system>-mapping.md             # Notion DB IDs / property keys / block templates
    ├── company-linking.md              # (optional) Domain-specific upsert rules
    ├── project-linking.md              # (optional) Cross-DB linking rules
    └── kg-write.md                     # (optional) Knowledge-graph block templates
```

Helper scripts that the skill calls live at `<repo>/scripts/` — NOT inside the skill directory. The skill references them with paths like `bash ~/<repo>/scripts/kg-meeting-write.sh ...`.

## SKILL.md shape (the orchestration)

Write SKILL.md as a numbered step sequence. Each step does one thing. Each step references one or more `references/*.md` files for the details. The orchestration file should be scannable in under 60 seconds.

```markdown
---
name: <skill-name>
description: <when-to-use trigger; loaded into context always>
---

# <Skill name>

One paragraph: what this skill does end-to-end.

## Inputs

The routine fires with `text = {"inbox_entity_id": "...", "recording_id": "..."}`. Step 0 fetches the staged payload.

## Step 0: Parse + fetch staged payload + dedup check

[Python or bash snippet that parses text, fetches the payload, and exits early if `properties.processed === true`.]

## Step 1: <LLM call 1, e.g. categorize>

Read `prompts/categorize.md` (verbatim from old n8n node). Substitute placeholders. Send to <model> with structured output.

## Step 2: <LLM call 2, branch on category>

| Category | Prompt file |
|---|---|
| <A> | prompts/transform-<a>.md |
| <B> | prompts/transform-<b>.md |

## Step 3: Write to <system 1>

Read `references/<system-1>-mapping.md` for DB IDs and property keys. Create / update.

## Step 4: Write to <system 2>

...

## Step N: Mark inbox entity as processed

PATCH the staging entity with `processed: true`, `processed_at: <iso>`, and the side-effect ids.

## Cross-references

- `prompts/<name>.md` — verbatim prompts from the old n8n workflow
- `references/<system>-mapping.md` — system-specific schemas

## Verification

End-to-end test: ...
```

Keep SKILL.md under 500 lines. Move deep details to `references/`.

## Prompt files (verbatim from old n8n)

The MOST important rule: **copy prompts verbatim**. The same prompt that worked in n8n works in Claude Code. No paraphrasing. No "improving the wording." Stale-looking prompts often have years of subtle tuning.

```markdown
# <Original n8n node name>

> **Verbatim** from n8n workflow `<workflow-id>`, node `<node-name>`.
> Model: <model>. <Output format constraints>.
> Substitute `{{TITLE}}`, `{{TRANSCRIPT}}`, `{{INVITEES}}`, `{{NOW}}` before sending. No other changes.

---

[PASTE THE PROMPT BODY VERBATIM]
```

Only change the variable interpolations (`{{ $('NodeName').item.json.x }}` → `{{TITLE}}` etc.) so the skill can fill them in. Everything else stays identical.

## Reference files (system mappings)

For each external system (Notion DB, Slack workspace, Drive folder, etc.), write a `references/<system>-mapping.md` with:

- The DB / channel / folder ID
- Every property name + type the skill writes
- Any LIVE option values (e.g., a `Status` select's allowed values)
- Mapping tables when the prompt outputs don't match the live options 1:1
- Body block templates (for Notion pages)
- Filter rules (e.g., "only create tasks where assignee === 'Matty Reed'")

Retrieve these by calling the live API once (`API-retrieve-a-data-source` for Notion) — don't paraphrase from memory.

## Payload schema doc

`references/payload-schema.md` captures:

1. **What `text` contains** (the small reference object the routine receives)
2. **How to fetch the staged payload** (the Convex / Notion / etc. call)
3. **The full shape of the staged payload** (every field, what each means)
4. **Fallback for local invocation** (when running the skill locally outside the routine — useful for testing)

Example structure:

```markdown
# Payload schema

## What the routine receives in `text`
[json snippet]

## How the skill fetches the full payload
[bash or python snippet using curl / the convex CLI]

## Full payload shape (after fetch)
[json snippet with every field]

## Local invocation (testing)
[how to pass a payload directly without n8n]
```

## Helper scripts (one level up, in repo `scripts/`)

When the skill needs to call something multiple times with slightly different args, write a small Bash or Python helper in `<repo>/scripts/`:

```bash
# scripts/kg-meeting-write.sh — wraps Convex calls for the KG step
#
# Usage:
#   kg-meeting-write.sh upsert-person <name> <email> <role> <summary> <page-id>
#   kg-meeting-write.sh append-by-id <entity-id> <block-file>
```

The skill invokes these as `bash ~/<repo>/scripts/<helper>.sh ...`. Auto-detect environment (local Mac vs CCR) and fall back to raw HTTPS if a local CLI isn't available.

## What NOT to put in the skill

- Anything that needs a local-Mac binary (`gws`, custom CLIs) — push to n8n or use raw HTTPS.
- Long instruction blocks that duplicate `references/*.md` content — link to the reference instead.
- Hard-coded credentials — read from the routine's environment vars.
- Multi-line bash scripts with complex logic — extract to `scripts/`.

## The 7-step pattern (the MR.EA reference)

The MR.EA meeting-notes skill uses this exact shape — adapt as needed:

1. **Parse + fetch** (Step 0)
2. **Categorize** (LLM call)
3. **Transform** (LLM call, branching)
4. **Upsert lookups** (Contacts, Companies, Projects)
5. **Create anchor** (the Notion meeting page)
6. **Side-channel writes** (Drive transcript URL, Slack notification)
7. **Tasks** (filter to assignee, create rows)
8. **KG block append** (structured Obsidian-style markdown)
9. **Mark inbox processed** (dedup ledger)

If your workflow doesn't need all of these, drop the steps you don't need. If you need more, add them in the right place — but keep each step focused on one thing.
