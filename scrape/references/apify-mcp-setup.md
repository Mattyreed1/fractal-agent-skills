# Apify MCP Setup with mcpc

Use this reference when the task requires Apify Actors through MCP.

## Prerequisites

- Apify account with access to required actors.
- `node` and `npm` available in PATH.
- `mcpc` installed.

## Install mcpc

```bash
npm install -g @apify/mcpc
```

## Connect to Apify MCP (Streamable HTTP)

```bash
mcpc mcp.apify.com login
mcpc mcp.apify.com connect @apify
mcpc @apify tools-list
```

Important:
- Use base URL `mcp.apify.com`.
- Legacy SSE endpoint `mcp.apify.com/sse` is deprecated and should not be used.

## Constrained Runtime Fallback (mcp-remote bridge)

If `mcpc` cannot run in the target runtime (for example missing system libraries in a container), configure Apify through your MCP host with `mcp-remote` and a bearer token header.

Example server entry:

```json
{
  "apify": {
    "command": "node",
    "args": [
      "/home/user/.npm-global/lib/node_modules/mcp-remote/dist/proxy.js",
      "https://mcp.apify.com",
      "--header",
      "Authorization:Bearer ${APIFY_TOKEN}",
      "--silent"
    ],
    "env": {
      "APIFY_TOKEN": "apify_api_..."
    }
  }
}
```

After writing config, restart the MCP host/gateway and verify logs before claiming readiness.

## Typical Actor Discovery and Execution

List available MCP tools:

```bash
mcpc @apify tools-list
```

Find candidate actors:

```bash
mcpc @apify tools-call search-actors keywords:="google maps" limit:=5 --json
```

Inspect required input fields before execution:

```bash
mcpc @apify tools-get call-actor
```

Run actor with a small pilot input:

```bash
mcpc @apify tools-call call-actor \
  actorId:="apify/google-search-scraper" \
  input:='{"queries":["site:example.com pricing"],"maxPagesPerQuery":1}' \
  --json
```

## JSON-Mode Automation Pattern

Use `--json` for machine-readable outputs and downstream parsing:

```bash
mcpc @apify tools-call search-actors keywords:="ecommerce" limit:=3 --json
```

## Optional: Install Apify Agent Skills

```bash
npx skills add apify/agent-skills
```

Includes:
- `apify-actor-development`
- `apify-ultimate-scraper`

## Troubleshooting

- `mcpc: command not found`
  - Reinstall globally and restart shell.
- `authentication required` or token errors
  - Run `mcpc mcp.apify.com login` again.
- No tools listed
  - Re-run `mcpc mcp.apify.com connect @apify` and then `mcpc @apify tools-list`.
- Old endpoint in config
  - Replace `mcp.apify.com/sse` with `mcp.apify.com`.
