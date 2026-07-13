# n8n side — minimal forwarder template

## Contents

- Target shape (3-5 nodes)
- Compact Payload Code node template
- Stage in Convex (HTTP Request node)
- Fire the routine (HTTP Request node)
- n8n expression gotchas
- Reusing existing credentials
- Retries + error handling
- Validation & anti-patterns

Defer to the `n8n` skill for workflow JSON, node configs, expression syntax, and MCP tooling. This file documents the **minimal forwarder shape** you build when converting an n8n workflow.

## Target shape (3-5 nodes)

| # | Node type | Purpose |
|---|---|---|
| 1 | `n8n-nodes-base.webhook` | Receives the external POST |
| 2 | `n8n-nodes-base.code` | Compacts the payload (flatten arrays, strip metadata) |
| 3 | `n8n-nodes-base.httpRequest` (optional) | Uploads files to Drive / S3 if needed |
| 4 | `n8n-nodes-base.httpRequest` | Stages the compact payload in Convex / Notion inbox |
| 5 | `n8n-nodes-base.httpRequest` | Fires the Claude Code routine |

No AI nodes. No Switch nodes. No conditional logic. If you're tempted to add one, push it into the skill instead.

## Compact Payload Code node template

```js
// Compact the incoming webhook body. Strip metadata you don't use,
// flatten arrays of objects into a single string, expose only what
// the skill needs. Goal: stay well under the 65,536-char `text` cap.

const body = $input.item.json.body ?? $input.item.json ?? {};

const segments = Array.isArray(body.transcript) ? body.transcript : [];
const transcript = segments
  .map(s => `${s.speaker?.display_name ?? 'Unknown'}: ${s.text ?? ''}`.trim())
  .join('\n');

const recordingId = String(
  body.recording_id ?? body.share_url ?? body.url ?? `untagged-${Date.now()}`
);

const compact = {
  title: body.title ?? body.meeting_title ?? null,
  share_url: body.share_url ?? body.url ?? null,
  recording_start_time: body.recording_start_time ?? new Date().toISOString(),
  recording_id: body.recording_id ?? null,
  calendar_invitees: (body.calendar_invitees ?? []).map(p => ({
    name: p.name ?? p.matched_speaker_display_name ?? '[Unknown]',
    email: p.email ?? null,
  })),
  transcript, // already flattened to a string
};

const compactText = JSON.stringify(compact);

return [{
  json: {
    compact: compactText,
    compactSize: compactText.length,
    recordingId,
    // For downstream nodes (Drive upload, staging):
    transcript_text: transcript,
    drive_filename: `${(body.recording_start_time ?? '').slice(0,10)}_${recordingId}.txt`,
  }
}];
```

Adapt the field names to whatever your source service sends.

## Stage in Convex (HTTP Request node)

```
Method: POST
URL:    https://<your-deployment>.convex.cloud/api/run/kgPublic/addEntity
Headers:
  Content-Type: application/json
Body (Specify Body: JSON):
```

`kgPublic` is gated by a shared token — pass `KG_ACCESS_TOKEN` as the `token` arg (store it as an n8n env var / variable, referenced as `{{ $env.KG_ACCESS_TOKEN }}`, NOT inline — n8n exports embed inline values). While the deployment's token is unset the gate is a no-op.

```json
={
  "args": {
    "token": "{{ $env.KG_ACCESS_TOKEN }}",
    "name": "inbox-{{ $('Compact Payload').item.json.recordingId }}",
    "entityType": "concept",
    "summary": "Staged payload — auto-staged by n8n forwarder",
    "notes": {{ JSON.stringify(JSON.stringify(Object.assign(JSON.parse($('Compact Payload').item.json.compact), { drive_url: $json.webViewLink || null }))) }},
    "properties": {
      "recording_id": "{{ $('Compact Payload').item.json.recordingId }}",
      "compact_size": {{ $('Compact Payload').item.json.compactSize }},
      "staged_at": "{{ $now.toISO() }}",
      "processed": "false"
    },
    "createdBy": "n8n-forwarder",
    "source": "<your-source>:{{ $('Compact Payload').item.json.recordingId }}"
  },
  "format": "json"
}
```

The double `JSON.stringify` is intentional — the outer one produces a properly-escaped JSON string literal so the inner JSON survives in the `notes` field. Returns `{status, value: {action, id, wikiLinks}}`. The `value.id` is the Convex entity ID.

## Fire the routine (HTTP Request node)

```
Method: POST
URL:    https://api.anthropic.com/v1/claude_code/routines/{ROUTINE_ID}/fire
Headers:
  Authorization: Bearer {ROUTINE_TOKEN}
  anthropic-version: 2023-06-01
  anthropic-beta: experimental-cc-routine-2026-04-01
  Content-Type: application/json
Body (Specify Body: Using Fields Below):
  Name:  text
  Value: ={{ JSON.stringify({ inbox_entity_id: $json.value.id, recording_id: $('Compact Payload').item.json.recordingId }) }}
```

The body is `{"text": "<JSON-stringified small reference>"}`. The routine's static prompt parses this in the skill's Step 0.

## n8n expression gotchas

| Gotcha | Fix |
|---|---|
| Template literals `` `${var}` `` NOT supported in n8n expressions | Use string concatenation: `'foo' + var + 'bar'` |
| `$json.body` is where the webhook POST body lives | Use `$json.body || $json` defensively in case the body is at top level |
| HTTP node `bodyParameters` is the easiest for simple key/value | Use `jsonBody` (expression mode) only when you need complex structures |
| Drive node returns `id` but `webViewLink` is sometimes missing | Fall back: `'https://drive.google.com/file/d/' + $json.id + '/view'` |
| Notion property names use the DISPLAY name in MCP responses | Cross-check against `API-retrieve-a-data-source` schema — display names can drift |
| `JSON.stringify` in `jsonBody` inside `={ ... }` needs careful quote escaping | Test with a minimal payload first; n8n's validation will flag template-literal use |

## Reusing existing credentials

Don't create new OAuth flows. Look at the OLD workflow's credentials and reuse:

- Google Drive: `googleDriveOAuth2Api` credential id
- Notion: `notionApi` credential id (or the integration token if direct)
- HTTP Header Auth: any custom service tokens

The forwarder rewrite is just shrinking the node count; the credential plumbing stays the same.

## Retries + error handling

On the Fire Routine node:
- `retryOnFail: true`
- `maxTries: 3`
- `waitBetweenTries: 3000` (3 seconds)

Routine fire is the most likely failure point (Anthropic rate limits, transient 5xx). Three retries with a 3-second wait handles most transient cases.

Don't retry the Stage Payload node aggressively — Convex upsert by name is idempotent so one retry is fine.

## Validation

After building the workflow, run the MCP validator:

```
mcp__mr-n8n__n8n_validate_workflow({ id: "<workflow_id>", options: { profile: "runtime" } })
```

Common errors:
- `Template literal syntax ${} found` → replace with string concatenation
- `Webhooks should always send a response` → ignore unless you actually need to respond to the caller synchronously
- `HTTP Request node without error handling` → add `retryOnFail`

## Anti-patterns

| Avoid | Why |
|---|---|
| Adding a Switch node to route by category | Push it into the skill — the LLM categorizes there |
| Adding multiple HTTP nodes that each write to a different system | All multi-system writes belong in the skill |
| Inlining the full payload in `text` | Will hit the 65k cap on long inputs |
| Trying to do retries with exponential backoff in n8n | Three retries is enough; the skill is the durable retry surface (via dedup) |
| Adding an n8n credential JUST to call the routine fire endpoint | Use HTTP Header Auth inline; the routine token IS the credential |
