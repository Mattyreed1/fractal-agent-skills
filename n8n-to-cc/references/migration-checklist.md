# Migration checklist — converting an n8n workflow to a Claude Code routine

## Contents

- Phase 1: Extract from n8n (read-only)
- Phase 2: Build the new pieces
- Phase 3: End-to-end test
- Phase 4: Cut over
- Failure modes to watch for

Follow these in order. Each step has a verification gate before moving on.

## Phase 1: Extract from n8n (read-only)

### 1.1 — Get the workflow JSON

```
mcp__<n8n>__n8n_get_workflow({ id: "<workflow-id>", mode: "full" })
```

(Defer to the `n8n` skill for full MCP tooling.) The output is huge — for a 22-node workflow it can be 100K+ chars. Save the result file path.

**Verify:** you have the full JSON saved somewhere readable.

### 1.2 — Inventory the nodes

Categorize each node:

| Node type | Where it ends up |
|---|---|
| Webhook trigger | n8n forwarder (preserved) |
| Schedule Trigger | If the user wants real-time, drop. If scheduled, use the `schedule` skill, not this one. |
| Code / Set / Function | Skill, usually as part of Step 0 parsing |
| If / Switch / Merge | Skill, as conditional logic in the orchestration |
| LLM nodes (OpenAI, Anthropic, Gemini, langchain agent, etc.) | Skill — extract prompts verbatim into `prompts/*.md` |
| Output Parser nodes | Skill — structured output enforcement |
| Notion / Slack / Drive / Sheets | Skill — extract schemas into `references/*-mapping.md` |
| HTTP Request to external APIs | Skill, unless they require n8n's credential (then forwarder) |
| Wait nodes | Skill (just use sleep) |
| Sticky notes | Documentation — extract any value into your SKILL.md if relevant |

**Verify:** you can name what each non-trivial node becomes in the new architecture.

### 1.3 — Extract every AI prompt verbatim

For each LLM node:

- Open the node JSON in the workflow dump
- Find the `parameters.text` (or `parameters.messages[0].content`) field
- **Copy the prompt VERBATIM** — including all "Core Instructions", "Output Format", "Rules", "Examples", etc.
- Save to `<skill>/prompts/<descriptive-name>.md` with a header documenting source (workflow id + node name + model + output mode)
- Rewrite variable interpolations (`{{ $('Foo').item.json.x }}` → `{{TITLE}}` or similar) — those are the only allowed changes.

**Verify:** each prompt file starts with `> **Verbatim** from n8n workflow ...` and the body is byte-for-byte identical to what was in n8n (except for `{{VAR}}` substitutions).

### 1.4 — Extract every system mapping

For each Notion / Slack / Drive / etc. node:

- Note the database ID / channel ID / folder ID
- For Notion: retrieve the data source schema (`API-retrieve-a-data-source`) to get the EXACT property names + types + select option values
- Save to `<skill>/references/<system>-mapping.md`
- Include mapping tables when prompt outputs don't match live options 1:1 (e.g., prompt says `"WorkSync"` but Notion has `"Work Sync"` — document the rename)

**Verify:** every property name in the mapping doc matches what `API-retrieve-a-data-source` returned, not a paraphrase from memory.

### 1.5 — Document the webhook payload

- Save a real captured webhook payload from the n8n execution log (`n8n_executions` MCP tool) — find a successful past execution and dump its input
- Save to `<skill>/references/payload-schema.md`
- Document: top-level fields, nested structures, optional fields, types

**Verify:** you have a real-shape JSON sample, not a hypothetical schema.

## Phase 2: Build the new pieces

### 2.1 — Stand up the staging store

If using Convex:
- Confirm a deployment exists (`<deployment>.convex.cloud`)
- Confirm the n8n call passes the `KG_ACCESS_TOKEN` shared secret as a `token` arg — `kgPublic:*` is HTTP-reachable but gated (NOT public)
- If it's not public, add a deploy key to the routine's env

If using Notion as the inbox: create a "<Pipeline> Inbox" database with at minimum `Title`, `Recording ID`, `Status`, `Payload` (code block) properties.

If using GitHub Gists / S3 / VPS: provision and document.

**Verify:** you can `curl` the staging endpoint from outside the local Mac and write+read a test entity.

### 2.2 — Create the Claude Code Routine

1. Open https://claude.ai/code/routines
2. Click **New routine**
3. **Link the GitHub repo** that contains your skill (must be a repo your account has access to)
4. **Trigger: API**
5. **Static prompt** — write it to:
   - State the source service ("A new Fathom transcript has arrived")
   - Describe the `text` shape ("`text` is a JSON object with `inbox_entity_id` and `recording_id`")
   - Tell the session to invoke your skill ("Invoke the `<skill-name>` skill")
   - Embed `{text}` at the bottom
6. **Save** — Anthropic generates a `routine_id` and a bearer token. Copy both.

**Verify:** smoke-fire with curl returns a session URL.

### 2.3 — Configure the routine's cloud environment

In **Edit routine** → cloud icon below Instructions → settings icon:

- **Network access**: Custom
- **Allowed domains**: every hostname your skill calls (Convex deployment, custom APIs, VPS hostnames)
- **Also include default list**: checked (keeps GitHub / Notion / npm)
- **Environment variables**: any non-secret config the skill needs
- **Setup script**: usually empty; add `npm install` only if your repo has Node deps

**Verify:** the network policy lists every external host the skill calls. A missing entry will surface as a `Host not in allowlist` 403 inside the session.

### 2.4 — Build the n8n forwarder

In a new n8n workflow:
1. Add a Webhook node — note its production URL.
2. Add a Code node for compaction.
3. (Optional) Add Google Drive / etc. nodes for file uploads.
4. Add an HTTP Request node for staging.
5. Add an HTTP Request node for routine fire.
6. Wire them in order.
7. Run `n8n_validate_workflow` — fix any expression errors (no template literals, etc.).
8. Activate the workflow.

See [`n8n-side.md`](n8n-side.md) for the full templates.

**Verify:** firing the webhook with a captured payload yields HTTP 200 + a session URL from the Anthropic API.

### 2.5 — Build the skill

In your project repo:

1. Create `skills/<skill-name>/` with `SKILL.md`, `prompts/`, `references/`.
2. Write SKILL.md as a numbered orchestration (see [`skill-side.md`](skill-side.md) for the shape).
3. Drop the verbatim prompts into `prompts/*.md`.
4. Drop the system mappings into `references/*-mapping.md`.
5. Drop the payload schema into `references/payload-schema.md`.
6. (Optional) Add helper scripts at `scripts/`.
7. Commit + push.

**Verify:** `scripts/check_ccr_skills.sh` (or equivalent) finds no out-of-repo symlinks; CCR clone will see real files.

## Phase 3: End-to-end test

### 3.1 — Smoke test with captured payload

```bash
curl -sS -X POST \
  -H "Content-Type: application/json" \
  --data-binary @<captured-webhook-payload.json> \
  https://<n8n-host>/webhook/<your-test-path>
```

Then:
1. **Verify n8n succeeded** — check the latest execution via `n8n_executions`. Each node should be green.
2. **Verify staging worked** — fetch the staged entity from the store. Properties + notes should match what n8n built.
3. **Wait 3-5 min for CCR session.** No status endpoint exists; wait it out.
4. **Verify side effects landed:**
   - New Notion page in the target DB?
   - Tasks created with correct properties?
   - KG block appended?
   - Slack message posted?
   - etc.
5. **Verify dedup ledger** — staging entity's `properties.processed` should be `true` now.

If any of the above fail, **don't trust the HTTP 200 from the routine fire** — open the session URL in the Anthropic UI to see what the session actually did.

### 3.2 — Re-fire to verify dedup

Fire the same payload again. Expected behavior:

- n8n succeeds, stages, fires routine.
- Skill Step 0 reads `processed: true` on the staging entity.
- Skill exits cleanly with `"already processed"` message.
- No new Notion page, no new tasks, no new KG block, no new Slack message.

If a second page is created, the dedup check is broken — fix before going live.

## Phase 4: Cut over

### 4.1 — Swap the webhook path

The new workflow has a fresh webhook URL (the test path). The legacy n8n workflow has the URL the external service is already configured to call.

To cut over without reconfiguring the external service:

1. **Deactivate** the legacy workflow (don't delete — keep as rollback).
2. **Change** the new workflow's webhook node `path` to match the legacy URL.
3. **Test** by firing the legacy URL — should now hit the new workflow.

(In n8n, the webhook path is the suffix after `/webhook/`. Set it via the node config.)

### 4.2 — Monitor for the first 24 hours

Watch:
- n8n execution log for the new workflow — every fire should succeed.
- The staging store — entities should accumulate, all marked `processed: true`.
- Side-effect systems — Notion pages, Slack messages, etc. should land at the same rate as before.

If anything looks off, **reactivate the legacy workflow** (it still has the same node config) and investigate. The new workflow's webhook path can be reverted to the test path.

### 4.3 — Decommission the legacy workflow

After ~30 days of clean runs:
- Tag the legacy workflow's JSON for archive (`n8n_workflow_versions` if exposed, otherwise just save the JSON locally).
- Delete the legacy workflow.
- Update internal docs / runbooks to point at the new architecture.

## Failure modes to watch for

| Symptom | Likely cause | Fix |
|---|---|---|
| HTTP 400 `text: maximum string length is 65536` | Compact payload too big | Strip more metadata in the Code node; move file content to Drive |
| Session URL returned but no side effects | Skill failing mid-flow OR network allowlist missing a host | Open session URL in UI to see the error |
| `Host not in allowlist` 403 | Network policy missing the host | Add to Custom allowed domains |
| `notion skill symlink is broken` | Skill has out-of-repo symlinks | Reverse the symlink direction; commit real files |
| Duplicate side effects on re-fire | Dedup ledger not being set | Verify Step N (mark processed) is running last |
| Random failures on long calls | LLM timeout / token limit | Split the prompt into multiple sequential calls in the skill |
| Tasks all marked High priority | Old prompt didn't calibrate; copying verbatim preserved this | Update the prompt explicitly to set Medium default, High/Low edge cases |
