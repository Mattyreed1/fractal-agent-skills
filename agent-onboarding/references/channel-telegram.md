# Channel: Telegram

The simplest channel — a single BotFather token.

1. In Telegram, message **@BotFather** → `/newbot` → give it a name + username → copy the **HTTP API token**.
2. **Hermes:** put it in `~/.hermes/.env` → `TELEGRAM_BOT_TOKEN=...` (Telegram is a native Hermes channel; confirm the exact key with `hermes config show` if unsure). Group-gate with `hermes config set telegram.require_mention true` if wanted.
3. Restart the gateway, DM the bot to verify it replies.

**Privacy mode:** BotFather `/setprivacy` controls whether the bot sees all group messages or only mentions/commands. Turn privacy OFF only if the agent genuinely needs to read all group traffic; default to mention/command gating.

**Home channel:** on Telegram the "home" is simply the group/chat the bot is added to. Add it to that group, then use privacy mode (above) to decide whether it reads everything or only mentions/commands. For DMs it just responds to the allowed user directly.

Token is a secret — `.env`/secret ref only, never chat or commits. Rotate via BotFather (`/revoke`) if leaked.
