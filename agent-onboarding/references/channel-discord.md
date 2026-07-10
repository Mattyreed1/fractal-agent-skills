# Channel: Discord

Reaching an agent via Discord. Core concept: one bot app per agent identity, a bot token, privileged intents, mention-gating, and the non-reply rule (a bot stays silent when another bot is mentioned). Bot tokens are secrets — live in `~/.hermes/.env`, never in chat or commits. If a token leaks, rotate it in the Developer Portal immediately.

## Discord Developer Portal
1. discord.com/developers → New Application → **Bot** → Reset Token, capture it.
2. **Enable intents:** Message Content **ON**; Server Members **ON** (required for some allowlist modes); Presence optional.
3. Private app? **Installation → Install Link: None** (else "Private application cannot have a default authorization link").
4. **OAuth2 → URL Generator** → scope `bot` (+ `applications.commands` if you want slash commands) → pick bot permissions → open the URL to invite it to the server.
5. Capture **Application ID**, **Guild (Server) ID**, and a **Channel ID** if binding to one channel.

## Hermes
- Token env var is **`DISCORD_BOT_TOKEN`** (NOT `DISCORD_TOKEN`) in `~/.hermes/.env`.
- Scope it: `hermes config set discord.free_response_channels "<home-channel-id>"` (CSV; answers without a mention there) + `hermes config set discord.require_mention true`.
- Least-privilege toolset: `platform_toolsets.discord: [terminal, file, skills, todo]`.
- Verify: the gateway log shows `[Discord] Connected as <Bot>#nnnn`; run a live mention test (only this bot replies).

## Home channel (respond without a mention)

By default the bot only replies when @mentioned. To give it a home channel where it auto-responds:
- **Get the channel link/id:** enable Developer Mode (User Settings → Advanced), then right-click the channel → **Copy Channel ID**; or right-click → **Copy Link** → `https://discord.com/channels/<guild_id>/<channel_id>`.
- **Hermes:** `hermes config set discord.free_response_channels "<channel-id>"` (CSV) — or just paste the channel link to the agent and tell it that's its home channel; it pulls the id from the link and sets the config.
- Everywhere else stays mention-only so the non-reply rule holds. **Invite the bot to the channel first** (posting needs membership).

## Common breaks
| Symptom | Cause | Fix |
|---|---|---|
| `Fatal Gateway error: 4014` | privileged-intents mismatch | enable Message Content (min) in the Dev Portal, restart |
| logs in but silent in a channel | not invited / wrong channel scope | invite the bot; check the free-response channel id |
| replies only when @mentioned | channel not in free-response set | add the channel id to `discord.free_response_channels` |

## Multi-agent hygiene
One app/token per identity — never reuse a bot token across identities. If multiple bots share a server, add each bot's user id to the others' rosters/allowlists so the non-reply rule holds and bots don't loop.
