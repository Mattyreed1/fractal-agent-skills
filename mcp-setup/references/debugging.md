# MCP Debugging Quick Reference

## When an MCP Server Fails in Claude Desktop

### Step 1: Check the Logs
```bash
tail -100 ~/Library/Logs/Claude/mcp-server-<name>.log
```

### Step 2: Look for These Common Errors

| Log Message | Problem | Solution |
|-------------|---------|----------|
| `npm does not support Node.js v16` | PATH has old Node first | Don't use npx, use direct node path |
| `Class extends value undefined` | Node version too old | Reinstall with Node 20 |
| `ENOENT` + file path | File doesn't exist | Check path, create file |
| `OAuth credentials not found` | Missing env var or wrong path | Verify GOOGLE_OAUTH_CREDENTIALS path |
| `Server transport closed unexpectedly` | Server crashed | Look above this line for actual error |

### Step 3: Test Manually
```bash
# Set any required env vars and run directly
MY_ENV_VAR="value" /usr/local/opt/node@20/bin/node /path/to/index.js
```

### Step 4: If Still Failing

1. Clear npm cache for the package:
```bash
rm -rf ~/.npm/_npx/*
```

2. Reinstall fresh:
```bash
/usr/local/opt/node@20/bin/npm install --prefix ~/.local <package-name>
```

3. Find entry point:
```bash
cat ~/.local/node_modules/<package>/package.json | grep -A5 '"bin"'
```

4. Update config with correct path and restart Claude Desktop

## Log Locations

- MCP logs: `~/Library/Logs/Claude/mcp-server-<name>.log`
- All MCP logs: `~/Library/Logs/Claude/mcp*.log`
- Claude Desktop config: `~/Library/Application Support/Claude/claude_desktop_config.json`

## Known Working Config Format

```json
{
  "mcpServers": {
    "server-name": {
      "command": "/usr/local/opt/node@20/bin/node",
      "args": [
        "~/.local/node_modules/@scope/package/build/index.js"
      ],
      "env": {
        "SOME_VAR": "/absolute/path/to/file"
      }
    }
  }
}
```

## Golden Rules

1. **Always use absolute paths** - no `~` or `$HOME` in JSON config
2. **Always use Node 20 directly** - not npx, not node without path
3. **Always check logs first** - don't guess at the problem
4. **Always test in terminal first** - before adding to config
5. **Always restart Claude Desktop** - after config changes
