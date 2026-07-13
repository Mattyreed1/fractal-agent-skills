# Claude Code Routines API — full spec

## Contents

- Fire endpoint
- What you CAN'T do via the API
- Required beta header
- Common error responses
- Routine configuration (UI-only)
- Cloud environment settings (network, env vars, setup script)
- Filesystem / repo behavior
- Triggering from common sources (n8n / curl / Python)

Routines let an external service fire a cloud Claude Code session against a GitHub-linked project. Configure at https://claude.ai/code/routines.

## Fire endpoint

```
POST https://api.anthropic.com/v1/claude_code/routines/{routine_id}/fire

Headers:
  Authorization: Bearer <routine_token>
  anthropic-version: 2023-06-01
  anthropic-beta: experimental-cc-routine-2026-04-01
  Content-Type: application/json

Body:
  { "text": "<string up to 65,536 chars>" }

Response (HTTP 200):
  {
    "claude_code_session_id":  "session_01...",
    "claude_code_session_url": "https://claude.ai/code/session_01...",
    "type": "routine_fire"
  }
```

The static prompt configured in the routine UI runs every fire. The `{text}` payload is injected into that prompt wherever the user writes the `{text}` template variable.

> **⚠️ SINGLE braces. `{text}`, never `{{text}}`.** The platform substitutes only the exact
> `{text}` token. A double-brace `{{text}}` is NOT recognized and passes through **literally** —
> the session receives the raw string `{{text}}` with no payload. This silently breaks any
> routine that consumes an input (it fired, but there's nothing to act on). If a session reports
> receiving a literal `{{text}}`/`{text}` placeholder, the fix is in the routine's Instructions
> in the UI (single braces), not in code. (Broke meeting-notes on 2026-07-09.)

## What you CAN'T do via the API

- **No `GET /routines/{id}`** — 404. Can't fetch the current prompt programmatically.
- **No `PATCH /routines/{id}`** — 404. Can't update the prompt via API; UI only.
- **No `GET /sessions/{id}`** — 404. Can't poll session status. Detect success/failure via side effects.
- **No batch fire / no rate-limit headers exposed** — fire one at a time, expect occasional 429s.

## Required beta header

`anthropic-beta: experimental-cc-routine-2026-04-01` is mandatory. Without it the fire endpoint returns HTTP 400. Update the date when Anthropic ships a newer beta.

## Common error responses

| HTTP | Body | Cause |
|---|---|---|
| 400 | `text: maximum string length is 65536` | Payload too big — stage externally |
| 400 | `anthropic-version: header is required` | Missing version header |
| 400 | `invalid routine ID: <id>` | Routine ID typo or wrong account |
| 401 | (auth failure) | Token wrong or expired |
| 403 | `Host not in allowlist` (returned to the SESSION, not the fire) | CCR network policy — see Network access below |
| 404 | `page not found` | Wrong endpoint URL |

## Routine configuration (UI-only at claude.ai/code/routines)

Open a routine and click **Edit routine**. Configurable:

| Setting | Notes |
|---|---|
| **Instructions (static prompt)** | The system prompt that runs every fire. Use `{text}` to inject the body. |
| **Linked GitHub repo + branch** | The repo CCR clones at session start. Cloned fresh per fire. |
| **Cloud environment** | Click the cloud icon below Instructions to manage. |
| **Triggers** | API (this skill's path), Schedule (cron — see `schedule` skill), GitHub event |

## Cloud environment settings (Edit routine → cloud icon → settings)

### Network access

- `Default` — Anthropic's curated allowlist (GitHub, npm registry, common public services).
- `Custom` — add specific hostnames (no URLs, no protocols, no paths; `*` wildcards supported). Check **Also include default list** to keep the defaults.
- `Full` — unrestricted outbound. Use sparingly.

For staging payloads in Convex, add `<deployment>.convex.cloud` to the Custom list. For hitting the VPS on port 80 (one of the patterns from Matty's setup), add the bare IP / hostname.

### Environment variables

Plain `.env` format. Visible to anyone with access to the routine. **Don't put secrets in here that you wouldn't share with collaborators** — Anthropic's UI explicitly warns about this.

### Setup script

Bash script that runs at session start before Claude Code launches. Use for `npm install` or other dependency setup. CCR has Python 3, Node, common Unix tools by default; install anything else here.

## Filesystem / repo behavior

- The linked GitHub repo is cloned fresh per fire into the session's working directory.
- Branch is fixed at routine config (default: `main`).
- Symlinks pointing outside the clone are dangling — see [`ccr-constraints.md`](ccr-constraints.md).
- Files written during the session are ephemeral — they live only for that session.

## Triggering from common sources

### From n8n (the canonical pattern)

HTTP Request node:
- Method: POST
- URL: `https://api.anthropic.com/v1/claude_code/routines/{ROUTINE_ID}/fire`
- Headers: `Authorization: Bearer {TOKEN}`, `anthropic-version: 2023-06-01`, `anthropic-beta: experimental-cc-routine-2026-04-01`, `Content-Type: application/json`
- Body: keypair `text` = `={{ $json.compact_reference }}` (n8n expression)

### From curl (smoke test)

```bash
curl -sS -X POST https://api.anthropic.com/v1/claude_code/routines/$ROUTINE_ID/fire \
  -H "Authorization: Bearer $ROUTINE_TOKEN" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: experimental-cc-routine-2026-04-01" \
  -H "Content-Type: application/json" \
  -d '{"text":"smoke test"}'
```

### From a Python script

```python
import requests, os
r = requests.post(
    f"https://api.anthropic.com/v1/claude_code/routines/{os.environ['ROUTINE_ID']}/fire",
    headers={
        "Authorization": f"Bearer {os.environ['ROUTINE_TOKEN']}",
        "anthropic-version": "2023-06-01",
        "anthropic-beta": "experimental-cc-routine-2026-04-01",
    },
    json={"text": payload_string},
    timeout=30,
)
r.raise_for_status()
session = r.json()
print(session["claude_code_session_url"])
```

## Docs

Official: https://code.claude.com/docs/en/routines

The fire endpoint, headers, and constraints above are verified live (2026-05-17 / 2026-05-18) against a live production routine.
