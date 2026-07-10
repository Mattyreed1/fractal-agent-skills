# Channel: Slack

A **native Hermes channel** (not a skill), over Socket Mode (no public URL). When something's wrong, **ask the agent to read its own logs** — it will name the exact missing scope/event.

Secrets go in `~/.hermes/.env`, **uncommented** (the file ships with them commented; a value after a `#` is ignored):
```
SLACK_BOT_TOKEN=xoxb-...      # Bot User OAuth Token (sends + reads)
SLACK_APP_TOKEN=xapp-...      # App-Level Token for Socket Mode — REQUIRED; the bot token alone won't connect
SLACK_ALLOWED_USERS=U...      # member IDs, comma-separated — REQUIRED or the gateway denies EVERYONE
```

## Create the app from a manifest
api.slack.com/apps → Create New App → **From a manifest**. This one covers public channels, private channels, DMs, and group DMs so nothing is silently ignored:

```json
{
  "display_information": { "name": "<Bot Name>" },
  "features": { "bot_user": { "display_name": "<Bot Name>", "always_online": true } },
  "oauth_config": { "scopes": { "bot": [
    "app_mentions:read", "chat:write", "users:read",
    "channels:read", "channels:history", "groups:read", "groups:history",
    "im:read", "im:history", "mpim:read", "mpim:history"
  ] } },
  "settings": {
    "event_subscriptions": { "bot_events": [
      "app_mention", "message.channels", "message.groups", "message.im", "message.mpim"
    ] },
    "interactivity": { "is_enabled": true },
    "socket_mode_enabled": true,
    "org_deploy_enabled": false,
    "token_rotation_enabled": false
  }
}
```

## Getting the scopes right (probe — don't guess)

**Include BOTH `:read` and `:history` for every conversation type** (channels / groups / im / mpim). The `:read` scope is what Slack needs for conversation + DM discovery (`users.conversations`); `:history` reads messages. Having `im:history` but NOT `im:read` breaks discovery with `missing_scope`. The manifest above is the complete verified set (incl. `im:read`, added 2026-07-10 after it shipped missing twice).

**Don't guess which scope is missing — ask Slack.** Call the API directly (the agent can do this itself) and read the `needed:` field:
```
auth.test                 # is the bot token valid?
apps.connections.open     # app-level token + Socket Mode OK? (returns a wss:// URL)
users.conversations       # -> error: missing_scope, needed: <scope>, provided: <...>
```
Add whatever `needed:` reports, **Reinstall to Workspace**, restart the gateway, re-probe until clean. Trial-and-error in the Slack dashboard is slower and keeps missing scopes.

## Tokens (the manifest can't mint these)
- **Bot token (`xoxb-`):** OAuth & Permissions → **Install to Workspace** → copy Bot User OAuth Token.
- **App-level token (`xapp-`):** Basic Information → **App-Level Tokens** → Generate, scope `connections:write`.

## The gotchas that cost real time (2026-07-09)
- **Both tokens required.** `xoxb` alone won't open the connection; `xapp` establishes Socket Mode.
- **`SLACK_ALLOWED_USERS` is required** or the gateway silently denies every message. Use the human's member ID (Slack profile → More → **Copy member ID**).
- **Invite the bot to the channel** — plain `chat:write` only posts where it's a member.
- **Missing `message.channels`** = ignores public-channel messages. Missing `message.mpim`/`mpim:*` = group DMs fail. Missing `message.groups`/`groups:*` = private channels fail.
- **DMs disabled** ("Sending messages to this app has been turned off"): App Home → **Show Tabs** → toggle **Messages Tab** ON → then check "Allow users to send Slash commands and messages from the messages tab" (the checkbox only appears once the tab is on).
- **Reinstall after ANY scope/event change** (yellow banner → **Reinstall to Workspace**) or it doesn't take.
- **Restart the gateway twice on first setup** — Slack libs lazy-install on the first boot; the listener may only start on the next one. A green "online" dot is not proof it's handling events.
- Socket Mode needs **no public URL**, so it works identically on a laptop and a VPS.

## Home channel (respond without a mention)

By default the bot only replies when @mentioned. To give it a home channel where it auto-responds:
- **Get the channel link/id:** in Slack, hover the channel in the sidebar → ⋮ **Copy link** → `https://<workspace>.slack.com/archives/C0XXXXXXX`. The `C0…` is the channel id.
- **Tell the agent (easiest):** paste that link to the agent — "this is your home channel, respond here without a mention." It extracts the `C0…` id and sets its free-response config itself.
- **Or set it directly:** put the channel id in Hermes' Slack free-response config (run `hermes config show` for the exact key; it mirrors Discord's `free_response_channels`).
- **Invite the bot to that channel first** — `chat:write` only posts where it's a member. Everywhere else stays mention-only.
