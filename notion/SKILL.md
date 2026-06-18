---
name: notion
description: Notion operations via the Notion MCP server. CRITICAL — ALWAYS fetch your workspace's "instructions" page FIRST (the page that documents your DBs, property names, allowed values, and write rules) before any Notion write. Encodes MCP naming/auth setup, a schema-caching discipline, and a set of hard-won Notion API gotchas.
license: MIT
---

# Notion Operations

> **Template note:** this skill is written as a reusable pattern. Replace every `<...>` placeholder with your own workspace IDs, and keep a cached schema table for the databases you write to most. The engineering lessons (MCP setup, the API gotchas) apply to any Notion workspace.

## ⚠️ WORKSPACE ISOLATION — CRITICAL (if you run more than one workspace)

If you connect **more than one Notion workspace** (e.g. a personal one and a client one), keep them strictly separate. NEVER confuse them.

| Workspace | MCP Server | Access Method | Instructions Page |
|-----------|------------|---------------|-------------------|
| **Personal** | `my-notion` | MCP (Internal Integration Token) | `<INSTRUCTIONS_PAGE_ID>` |
| **Client / second** | `client-notion` | MCP (Internal Integration Token) | N/A — use that workspace's spec doc |

**Rules:**
- `my-notion` MCP tools (`mcp__my-notion__*`) connect to the **personal workspace ONLY**.
- `client-notion` MCP tools (`mcp__client-notion__*`) connect to the **client workspace ONLY**.
- Pages in one workspace CANNOT be accessed via the other server — they return 404.
- NEVER write one workspace's data into the other.
- When the user says "Notion" without qualifying, ask which workspace they mean if context is ambiguous.

**Per-workspace key resources (fill in your own):**

| Resource | ID |
|----------|-----|
| Projects DB | `<PROJECTS_DB_ID>` |
| Tasks DB | `<TASKS_DB_ID>` |
| Template page | `<TEMPLATE_PAGE_ID>` |
| n8n Notion credential ID (if you integrate n8n) | `<YOUR_N8N_NOTION_CREDENTIAL_ID>` |

***

## MCP Server Configuration

**Name the server with a short, owned prefix — e.g. `my-notion`.** The server MUST have a short name (not `notion` alone, and never a raw UUID).

### Why Short Names Matter
Claude Code prefixes MCP tool names as `mcp__<server-name>__<tool-name>`. The API has a **64-character limit** on tool names.

**Example calculation (why a UUID name breaks):**
- `mcp__` = 5 chars
- `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx` (a UUID) = 36 chars
- `__notion-query-database-view` = 27 chars
- **Total: 68 chars = API ERROR**

With `my-notion`:
- `mcp__my-notion__notion-query-database-view` = 43 chars ✓

### MCP Naming Rules
| Rule | Example |
|------|---------|
| Max server name length | 20 characters |
| Use a prefix for ownership | `my-` for personal, `client-` for a client workspace |
| No UUIDs as names | ❌ Auto-generated UUIDs will break the 64-char limit |
| Kebab-case | `my-notion` not `myNotion` |

### MCP Tool Resolution — CRITICAL

**When ANY Notion MCP tool fails, follow this exact sequence:**

1. **Read the config file FIRST** — `~/Library/Application Support/Claude/claude_desktop_config.json` (Claude Desktop) or your Claude Code MCP config.
2. Check if the `my-notion` entry exists in `mcpServers`.
3. If missing → add it (see config below), then restart the client.
4. If present but tools show with a wrong prefix (UUID) → rename in config, restart.
5. If present and correct → THEN it's an auth issue (token revoked / integration disconnected).

**Never blame auth without checking config. Never retry broken tool calls. Never tell the user to reconnect without reading the config first.**

### Required Config Entries

```json
"my-notion": {
  "command": "<path-to>/node",
  "args": [
    "~/.local/lib/node_modules/@notionhq/notion-mcp-server/bin/cli.mjs"
  ],
  "env": {
    "NOTION_TOKEN": "<YOUR_NOTION_INTERNAL_INTEGRATION_TOKEN>"
  }
}
```

**⚠️ Config uses `NOTION_TOKEN`, NOT `OPENAPI_MCP_HEADERS`.** The older `OPENAPI_MCP_HEADERS` format (a JSON-encoded header string) is no longer used — the server reads `NOTION_TOKEN` directly. If you try to read `OPENAPI_MCP_HEADERS` from the config it will not exist.

### Auth — Internal Integration Tokens (no expiry)

Use Notion Internal Integration Tokens via `@notionhq/notion-mcp-server`. These tokens do NOT expire — no OAuth, no re-auth, no restarts needed. Pages/databases must be **shared with the integration** in Notion to be accessible.

## Pre-flight rule (read before any write)

Your workspace **instructions page** (`<INSTRUCTIONS_PAGE_ID>`) is the source of truth for property names, allowed values, naming conventions, and voice rules. It is often **paginated** — the first call to `mcp__my-notion__API-get-block-children` can return `has_more: true` with the section you need buried on page 2+. Either fetch all pages or query by DB-specific markers (heading IDs, DB IDs). **Don't trust a first-page search to mean "not in the instructions."**

A large instructions page can be 100k+ chars across several pages — too expensive to read on every write. **Route by what you're doing:**

| Situation | What to fetch |
|---|---|
| Writing to a DB **with a cached schema below** | Skip the instructions page. Use the cached schema. |
| Writing to a DB **not cached below** | Fetch all pages of instructions (paginate), find that DB's section, then **cache it here** for next time. |
| Making a voice / naming / policy decision the instructions govern | Fetch instructions (or the specific section). |
| Querying a known DB (read-only) | Skip instructions. Use cached IDs. |

**Caching discipline:** every time you fetch the instructions page to learn a new DB's schema, write a new entry under "DB Quick Reference" below. The next session won't pay for that lookup.

## Notion Formatting rules (cache your own formatting guide here)

When creating page bodies:
- Headers → `heading_1` / `heading_2` / `heading_3` blocks (NOT a paragraph with bold).
- Bullets → `bulleted_list_item` blocks (NOT a paragraph with a `-` prefix).
- Regular text → `paragraph` blocks.
- **No markdown syntax inside `rich_text` content** (no `**bold**`, no `# header`, no `- bullet`). Use block types and `annotations.bold` instead.
- Don't combine multiple sections in one paragraph block.

## DB Quick Reference (cached schemas — fill in for your workspace)

> Example of the shape to cache. Replace IDs/properties with your own.

### Content DB (example)
- **Data source ID:** `<CONTENT_DB_DATA_SOURCE_ID>`
- **Parent DB ID:** `<CONTENT_DB_ID>`
- **Title property:** `Name` (title)
- **Stage** (status, group: To-do / In progress / Complete):
  - To-do: `Idea`, `On Deck`
  - In progress: `Title/Thumb/Hook`, `Scripting`, `Recording`, `Visual Editing`, `Packaging/Posting`
  - Complete: `Published`, `Re-Published`
- **Format** (multi-select, content type — NOT platform): `Short Essay`, `Essay`, `Podcast`, `Long Video`, `Short Video`, `Thread`, `Tweet`
- **Platform** (multi-select, publishing destination): `LinkedIn`, `X`, `Threads`, `YouTube`, `Instagram`, `TikTok`, `Newsletter`
- **Type** (multi-select): `Credibility Hack`, `Concept Compression`, `Case Study`, `Helpful Hacks`, `Interview`, `Tutorial`, `Listicle`, `Educational`, `Story`
- **Topic Pillar** (multi-select): `AI Automation`, `AI Agents`, `Notion Systems`, `Founder Ops`, `Client Work`, `Personal Story`, `Product Build`
- **Other props:** `Hook` (rich_text), `Overview` (rich_text), `Post URL` (url), `Published Date` (date), `Tasks` (relation → Tasks DB)
- **Metrics props (number):** `Impressions`, `Likes`, `Comments`, `Shares/Reposts`, `Saves/Bookmarks`, `Profile Visits`, `Follows Gained`, `Link Clicks`, `Leads`
- **Parent format on create:** `{"type": "data_source_id", "data_source_id": "<CONTENT_DB_DATA_SOURCE_ID>"}`

### Other DB IDs (schemas not yet cached — fetch instructions section before writing)
- Tasks: db `<TASKS_DB_ID>`, data source `<TASKS_DATA_SOURCE_ID>`
- Meetings: db `<MEETINGS_DB_ID>`, data source `<MEETINGS_DATA_SOURCE_ID>`
- Contacts: db `<CONTACTS_DB_ID>`, data source `<CONTACTS_DATA_SOURCE_ID>`
- Companies: db `<COMPANIES_DB_ID>`, data source `<COMPANIES_DATA_SOURCE_ID>`
- Quotes: db `<QUOTES_DB_ID>`
- Quotable People: db `<QUOTABLE_PEOPLE_DB_ID>`
- Instructions page: `<INSTRUCTIONS_PAGE_ID>`

## MCP tool schema gotcha — `API-post-page` children

The `mcp__my-notion__API-post-page` tool's `children` parameter has `items: {type: "string"}` in its MCP schema, but the API rejects strings with "should be an object." **Workaround:** create the page with properties only, then append body blocks via `mcp__my-notion__API-patch-block-children` (whose `children` schema is `items: {}` and accepts real block objects). Don't waste a turn JSON-encoding children for `post-page`.

## MCP tool gotcha — `API-update-a-block`

`API-update-a-block` is **defective in `@notionhq/notion-mcp-server` ≤ 2.2.1**. The bundled Notion OpenAPI spec mis-defines `PATCH /v1/blocks/{block_id}`: it declares the body content under a single `type` object, but the live API wants the block-type key at the **top level** (`{"paragraph": {"rich_text": [...]}}`). The server forwards tool args verbatim into the body, so the tool can only ever send `{"type": {...}}`, which Notion rejects with `body.type should be not present`. **No caller-side arg shape fixes it on an unpatched build** — don't burn turns trying `type` wrappers. Also: the spec defaults `archived` to **true**, so a bare update call can DELETE the block — always pass `archived: false` on a text update.

**Local fix:** patch the bundled `notion-openapi.json` so that operation's `requestBody` exposes the real block-type properties (`paragraph`, `heading_1`–`heading_4`, `bulleted_list_item`, `numbered_list_item`, `to_do`, `toggle`, `code`, `quote`, `callout`) and defaults `archived` to false. Re-run after any npm install/upgrade of the package, then reconnect/restart so the server reloads the spec — the spec is read once at startup.

**Fallback when unpatched:** to change block text, `API-patch-block-children` to insert the corrected block + `API-delete-a-block` to remove the old one. Insert before delete, anchor inserts to a stable sibling that won't be deleted, and re-fetch to verify.

## Verify page identity after create (CRITICAL)

`API-post-page` can return the **ID of an existing page** if Notion matches by title within the same parent — the response looks like a successful create even though no new page was made. **Always re-read the returned `id` via `API-retrieve-a-page` (or check `created_time` vs. now) before patching it.** Patching the wrong ID has clobbered the wrong page before. If the returned page already existed, decide whether to update in place, archive and recreate, or use a disambiguated title — don't blindly patch.

## Source of Truth

The instructions page defines: which databases to use for each content type; required and optional properties per database; property names and allowed values; naming conventions and formatting rules; write permissions and guardrails; and validation requirements (block writes if not met).

## Workflow

1. **Pick a path** using the "Pre-flight rule" table above.
2. **If using a cached schema:** write directly. **If fetching instructions:** fetch, validate, then add the DB schema to "DB Quick Reference" before writing.
3. **If validation fails:** stop and explain what's missing.
4. **If validation passes:** execute the Notion operation.
5. **Return:** created/updated page IDs and URLs.

## Notion API Gotchas (learned the hard way)

### Relation PATCHes to archived/trashed pages fail silently
PATCHing a page's `<relation>.relation` array with an ID that points to an archived/trashed page returns **HTTP 200** with **empty relation** in the response. No error, no warning. Notion treats the archived ID as invalid and drops it.

**Impact:** workflows that cache a `pageId` and PATCH it later (e.g., a webhook sets a relation at time T, the page gets archived at T+1, a downstream PATCH at T+2 silently drops the link) will silently fail.

**Mitigation:** before PATCHing a relation that references a page held across time, GET that page first and verify `archived !== true && in_trash !== true`. DB queries default-exclude archived pages, so name/email/phone lookups won't return them — but any code path that passes a known ID through needs an explicit guard.

### `phone_number` field stores arbitrary strings
The `phone_number` property type is just a string. Notion does NOT normalize on write. `555-867-5309`, `(555) 867-5309`, `+15558675309`, `555.867.5309` are all stored verbatim.

The `phone_number.equals` filter is exact-string match — there is no "digit-only equality" or canonicalization. To match across formats:
- **Best:** backfill stored phones to a canonical format (E.164: `+1XXXXXXXXXX`) and normalize all writes going forward.
- **OR:** at query time, build an `or` filter enumerating common variants (E.164, 10-digit, dashed, parens, dotted, spaced, with/without leading `1`).

### DB title property names vary per database
The "title" property in a Notion DB can be named anything — **don't assume `Name`**. Verify per DB before writing query filters. For example, a People DB's title might be `Name`, a Companies DB's might be `Company`, a Meetings DB's might be `Meeting Title`. Using the wrong name returns `Could not find property with name or id: <X>`.

### `archived` vs `in_trash`
Both fields exist on a page object. `archived: true` is the older "removed" flag; `in_trash: true` is the newer Trash state. Treat both as "do not use this page" — check both when verifying a referenced page is still active.

### No `notion://` resources — never call ReadMcpResourceTool for Notion
The Notion MCP exposes **no resources**. `ReadMcpResourceTool` on any `notion://` URI returns `Server "..." does not support resources`. The enhanced-markdown spec is embedded in the **`notion-create-pages` / `notion-update-page` tool descriptions themselves** — read those, don't fetch a resource URI.

### `database_id` vs `data_source_id` (2025-09-03 API)
The Notion API distinguishes between databases (which can have multiple data sources / views) and the underlying data sources. `API-query-data-source` requires the data source ID, not the database ID. If you have a database ID and get a 404, retrieve the database first to get its data source ID.

## Error Handling

If the instructions page cannot be retrieved: stop immediately, inform the user that Notion MCP access is required, and do not proceed with cached/assumed knowledge.

## Troubleshooting

### Any tool failure → READ CONFIG FIRST
`~/Library/Application Support/Claude/claude_desktop_config.json`
1. Is `my-notion` in the config? If not, add it.
2. Are tools loading with a UUID prefix? Fix the config name.
3. Config looks correct? Then it's auth — restart the client.

### "tool_name: String should have at most 64 characters"
Server name is too long. Edit config, rename to a short kebab-case name (max 20 chars).

### "Authentication required"
If the config is correct, the Internal Integration Token may be invalid. Check the `NOTION_TOKEN` value (env key is `NOTION_TOKEN`, not `OPENAPI_MCP_HEADERS`). Tokens do not expire — if auth fails, the token was revoked or the integration was disconnected from the workspace.
