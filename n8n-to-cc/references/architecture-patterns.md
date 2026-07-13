# Architecture patterns

## Contents

- Pattern 1: Webhook forwarder (canonical)
- Pattern 2: Direct API trigger (skip n8n)
- Pattern 3: Scheduled routine (no webhook)
- Sub-pattern A: Large-payload staging
- Sub-pattern C: Dedup ledger
- Sub-pattern D: Multi-target writes
- Sub-pattern E: Cross-skill composition

The three patterns you'll mix and match when converting n8n → Claude Code.

## Pattern 1: Webhook forwarder (canonical)

```
External service → n8n webhook → compact + stage → fire routine
                                                       ↓
                                                  CCR session runs skill
```

n8n is a thin proxy. 3-5 nodes. The skill does all the work.

**Use when:**
- Existing n8n workflow has the external service's webhook URL baked in.
- You don't want to reconfigure the external service.
- The work is bursty (webhook-driven) — no need for cron.

## Pattern 2: Direct API trigger (skip n8n)

```
Your code / external service → POST routine fire endpoint
                                       ↓
                                  CCR session runs skill
```

Skip n8n entirely. Useful when:
- You control the external service code (custom backend, internal tool).
- You don't need credential mediation (n8n's OAuth flows).
- The payload is small (< 60 KB) and doesn't need pre-processing.

Cost: you lose n8n's retry policies, queue, and visibility. The routine fire endpoint doesn't expose rate-limit headers, so you build your own backoff.

## Pattern 3: Scheduled routine (no webhook)

```
Cron in routine config → fires on schedule
                              ↓
                         CCR session runs skill (no payload)
```

For "every day at 6am, do X" workflows. The `{text}` is empty (or a fixed string per fire); the skill reads state from external systems.

**Use the `schedule` skill, not this one** — that's its specialty.

---

## Sub-pattern A: Large-payload staging

Triggered by the 65,536-char cap on `text`.

```
Compact payload (in n8n Code node)
       │  → strip metadata, flatten arrays
       ▼
POST {STAGING_URL}/api/run/<function>
  body: { "args": { "name": "stable-id", "notes": "<full payload>" }, "format": "json" }
       │  → returns entity_id
       ▼
Fire routine with text = JSON.stringify({ inbox_entity_id, recording_id })
       │
       ▼
Skill Step 0: fetch staged payload from STAGING_URL by entity_id
```

**Staging store options:**

| Option | Cap | Auth | Notes |
|---|---|---|---|
| Convex `kgPublic:addEntity` | 1 MB per doc | `KG_ACCESS_TOKEN` shared secret (`token` arg) | HTTP-reachable but gated — the n8n credential holds the token |
| Notion staging DB | 200KB per page (chunked across rich_text blocks) | Integration token | Reuses Matty's existing Notion access. Annoying chunking. |
| GitHub Gist API | ~10MB | PAT with `gist` scope | Easy to inspect. Public-by-URL. |
| S3 / R2 / similar | Unlimited | IAM creds | Most overhead. Best for binary blobs. |
| VPS endpoint on port 80 | Unlimited | Custom | CCR allows port 80 outbound; build a tiny HTTP server. |

**Sub-pattern B: Drive / file upload**

When n8n already has Google Drive OAuth and the skill needs a transcribed file in Drive:

```
n8n Code node: prepare file content
       │
       ▼
n8n Google Drive node: createFromText → returns drive_url
       │
       ▼
n8n: stitch drive_url into the compact payload before staging
       │
       ▼
Skill: reads drive_url from the staged payload, patches the target system (Notion, etc.)
```

**Why this beats doing it in CCR:**
- `~/.local/bin/gws` doesn't exist in CCR.
- n8n already has the OAuth credential.
- One less hop in the skill.

## Sub-pattern C: Dedup ledger

```
Skill Step 0:
  → fetch staged payload + entity properties
  → if properties.processed === true: exit with "already processed, page id <X>"
  → else: continue

Skill last step (after all writes succeed):
  → PATCH staging entity properties:
      processed: true
      processed_at: <ISO>
      <side-effect-id-1>: <value>
      <side-effect-id-N>: <value>
```

This makes the entire pipeline idempotent. n8n retries, manual re-fires, and Fathom's "did the webhook deliver?" double-sends all become safe no-ops.

**Resetting:** to reprocess a payload, clear `processed` and `<side-effect-id>` on the staging entity. The skill then runs end-to-end again.

## Sub-pattern D: Multi-target writes

When the skill writes to several systems (Notion + KG + Slack + Drive), establish ordering:

1. **Lookup / upsert reads first** — Contact upsert, Company resolve, Project resolve.
2. **Create the anchor record** — usually the Notion page or DB row that other things will reference.
3. **Side-channel writes** — Drive transcript upload, Slack notification, KG block append. These can fail independently without losing the anchor.
4. **Dedup ledger update last** — only marks "processed" if step 2 succeeded.

If any step fails:
- Step 2 fails → bail; nothing to dedup.
- Step 3 fails → log warning, keep going. The anchor exists; backfill manually.
- Step 4 fails → ledger doesn't update; next fire reprocesses (idempotent if step 2 is upsert-by-id).

## Sub-pattern E: Cross-skill composition

Bigger skills compose smaller ones. The MR.EA meeting-notes skill invokes:

- `notion` skill — for the mandatory "fetch instructions page" prelude before any Notion write.
- `knowledge-graph` skill — for KG conventions (entity types, relation types, wiki-link semantics).
- Custom helper scripts in the repo's `scripts/` directory.

Cross-skill references in CCR work only if all skills are REAL FILES in the linked repo. Symlinks pointing outside the repo are dangling. See [`ccr-constraints.md`](ccr-constraints.md).
