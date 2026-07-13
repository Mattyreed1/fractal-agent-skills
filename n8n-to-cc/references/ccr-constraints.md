# CCR (Claude Code Remote) constraints

What works and what doesn't in the cloud sandbox that runs a fired routine.

## Filesystem

- The routine's linked GitHub repo is **cloned fresh** at session start.
- Branch = whatever the routine config says (default `main`).
- Files written during the session are ephemeral — they don't persist beyond the session unless the skill commits them back to the repo.
- Absolute home-directory paths, `~/.local/bin/...`, project-local `node_modules`, and any other local-machine paths **don't exist**.

### Symlink rule

Any symlink in the repo pointing OUTSIDE the clone is dangling. Common breakage: a skill at `skills/<a>` that depends on `skills/notion`, but `skills/notion` is a symlink to `~/.claude/skills/notion`. That link is dead in CCR.

**Fix:** reverse the symlink direction.

```
Local Mac:                          CCR clone:
~/.claude/skills/notion             skills/notion/SKILL.md  ← real file
       │ symlink →                          ↑
       ▼                                    │
~/your-repo/skills/notion/SKILL.md  ───────────┘
       (real file, tracked in git)
```

Local Claude Code resolves through the reverse symlink. CCR sees the real file directly. No drift.

Guard rail: add a small CI script that fails on any out-of-repo symlink under `skills/`.

## Network access

Each routine has a cloud environment with one of three Network access settings:

| Setting | Effect |
|---|---|
| `Default` | Anthropic's allowlist — GitHub, npm, common public services |
| `Custom` | You list specific hostnames (`*` wildcards supported); check "Also include default list" to keep the defaults |
| `Full` | Unrestricted outbound |

**Symptom of a missing allowlist entry:** the session gets HTTP 403 `Host not in allowlist` on the request and bails. The skill's hardening should detect this and exit with a clean error rather than guess.

UI path: claude.ai/code/routines → Edit routine → cloud icon below Instructions → settings icon on the environment → set Network access → add Allowed domains → Save.

Common domains you'll need:
- Convex deployment: `<your-deployment>.convex.cloud`
- Notion: already in Default
- GitHub: already in Default
- npm: already in Default
- VPS hosts: bare IP or hostname (HTTPS preferred, port 80 also works)

## Local-Mac binaries are unavailable

| Binary | Use case | Alternative |
|---|---|---|
| `~/.local/bin/gws` | Google Workspace CLI (Drive, Gmail, Calendar) | Move the file upload to n8n; use Notion / Calendar MCP if available; call Google APIs directly via HTTPS |
| Custom CLIs | Project-specific tooling | Reimplement in the skill as Python / Bash invoking only public HTTPS |
| `psql`, `redis-cli`, etc. | Database CLIs | Call the database via HTTPS API or use the relevant MCP server |

## What IS available

- Python 3 with stdlib + common packages (`requests`, etc.)
- Node + npm (any package via `npm install`)
- Standard Unix tools (curl, grep, jq, sed, awk, find, etc.)
- Git (cloned repo at session start)
- Configured MCP servers that the routine has access to (Notion, Google Calendar, etc.)

## MCP servers in CCR

Routines can use MCP servers, but they have to be configured for that environment. Default MCP set is more limited than what your local Claude Desktop has. Verify before relying on a specific MCP tool:

- Test with `mcp__<server>__<tool>` invocation in a smoke-fire.
- If unavailable, fall back to raw HTTPS via the underlying API (e.g., `mcp__mr-notion__API-post-page` → raw `POST https://api.notion.com/v1/pages` with your integration token).

## Env vars

Set in the routine's cloud environment settings. Plain `.env` format.

- Visible to anyone with access to the routine — don't share secrets that wouldn't be shared with collaborators.
- Available as standard process env vars during the session.
- For secrets: prefer the routine's bearer token + per-domain allowlist + public-namespace endpoints (like `kgPublic:*`) over leaking deploy keys into env.

## CCR-specific gotchas Matty has hit

- **Convex `kg:*` (private) returns silent empty values without auth** — looks like "0 hits" but is actually a permission error. Use `kgPublic:*` for cross-environment work. See `reference_convex_kgpublic_open.md`.
- **`updatedBy` on Convex entities is the last writer string** — useful as a signal that the skill ran past a step, but stale `updatedBy` values can mislead. Pair with explicit `processed_at` timestamps.
- **Per-routine network allowlist changes apply on the NEXT fire**, not retroactively to in-flight sessions.
