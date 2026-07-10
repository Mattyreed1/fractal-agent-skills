---
name: agent-onboarding
description: >-
  Onboard a new AI agent onto a harness so it is genuinely operational — identity
  and persona, model and auth, skills, channels, integrations, and a completion
  checklist the new agent verifies itself. Worked runbook for Hermes (Nous
  Research's single-agent harness); the onboarding CONCEPT and the checklist are
  harness-portable. Use when creating, provisioning, or deploying a new agent and
  you want it to actually work, not just "reply once."
license: MIT
metadata:
  version: 1.4.0
  verified:
    hermes: "2026-06-07 (live deploy: Hermes v0.16.0)"
    hermes_desktop: "2026-07-10 (desktop app + Slack channel, full scope set incl. im:read, probe-verified; QuickBooks in its own integration reference; master + final-verification checklists baked in as the completion spine)"
---

# agent-onboarding

Onboard a new agent so it is genuinely operational. The worked runbook here is **Hermes** (Nous Research's single-agent harness); the concept, the discipline, and the completion checklist port to any harness — re-verify the mechanics against your runtime's current docs before you start, they drift.

## The completion contract — onboarding is done when the checklist says so

Onboarding is NOT "the agent replied in Slack." It is **every capability the agent's role requires, verified by the agent itself, from its own live runtime, with evidence** — plus a live test run of each core function. The spine is two files, and they are mandatory, not optional deep-dives:

- **[references/master-baseline-checklist.md](references/master-baseline-checklist.md)** — the per-agent **capability manifest** + the runtime / skills / tools / channel / model gates. You BUILD the manifest from this agent's mandate (Step 0), so the checklist **auto-fits the agent**: every app / integration / channel / tool it needs becomes a lane, and each lane must end `verified` / `verified-guarded` (or an owned, dated exception).
- **[references/final-verification-checklist.md](references/final-verification-checklist.md)** — the exhaustive A–M pre-acceptance sweep.

Three non-negotiables (the ones most often skipped):
1. **The new agent verifies itself** — it reads its own runtime and confirms what it has and can do. Onboarder-side "the config looks right" is not evidence.
2. **Every core function gets a live test run** — the real job executed, output captured. "Connected" ≠ "works."
3. **No completion language until every lane is green or an owned exception** — the completion-language lock in the checklist is a hard gate.

Everything below (operating discipline, governance, the Hermes runbook, the per-route references) is HOW you drive each lane to green. The checklist is WHAT "done" means. Build the manifest first; work it to green; sweep it at the end.

## Operating discipline (hard-won — read this before you touch anything)

These are the failure modes that turn an otherwise simple onboarding into an avoidable slog. Binding.

1. **Front-load the runtime's extension model before executing live.** Know up front how THIS harness adds each thing: capability (skill vs MCP vs native channel), where secrets live, how model + auth are set, how integrations attach. Don't discover it in front of the client. (Hermes: capabilities = skills at `~/.hermes/skills/<name>/` with `scripts/`; secrets = ONE file `~/.hermes/.env`; channels are native, not skills; model + auth live in `config.yaml` / desktop settings.)
2. **Build capabilities in the runtime's NATIVE form, never a side artifact.** A Hermes capability is a skill (a `SKILL.md` plus a helper script under its `scripts/`) in `~/.hermes/skills/`. Do NOT build a parallel project in some other repo and then work out how to bolt it on. Code the agent can't load is code in the wrong place.
3. **Let the agent diagnose itself.** The agent being onboarded reads its own logs and will name exactly what's wrong (e.g. "add Slack scopes `groups:read`, `mpim:*`; add event `message.mpim`; reinstall"). Ask it first; its self-diagnosis beats outside-in log-spelunking.
4. **Never narrate a third-party console (Slack, Intuit, etc.) from memory or docs.** You can't see their screen and the UI drifts. Name the section and have the user read back what they see, or actually look (screenshot / browser). Say "I can't see your screen" rather than confidently describing a button that may not exist.
5. **In a live build, hand the user the exact next action, not options or a parallel build.** "Send the agent THIS message." "Paste THIS there." Momentum beats completeness.
6. **Evidence is a live smoke through the runtime, never "config exists."** A token in a file or a config block proves nothing. Run the real read / write / route from the authoritative runtime and watch it pass.
7. **Prove the brain before plumbing the surface.** Get the agent's core job working in its own chat first, then wire the delivery channel. A silent channel is easy to debug once you already know the brain works.
8. **Probe, don't guess, for third-party config (scopes, tokens, endpoints).** When a channel/integration isn't working, call its API directly and read the exact error (`missing_scope` → `needed: <x>`), or have the agent do it. Guessing a scope set from memory is how a Slack `im:read` gap ships twice.

## Governance — lock, isolation, evidence gate

**Write a source-of-truth lock BEFORE building.** Name: runtime owner · host/location · channel/desktop owner · heartbeat/task owner · **secret store** · SOUL approval status · **model/auth path** · integration owner · final evaluator. Pick ONE runtime story and don't build two competing versions. **Hermes is its own harness** (`~/.hermes` + `hermes` CLI + gateway) — treat it as such; don't wrap a Hermes agent inside a different runtime unless the architecture is deliberately a bridge.

**Hard client isolation:** one client → one runtime home, scoped credentials, a scoped app per channel, a scoped OAuth app/credential per integration, scoped logs/backups. No shared credentials across clients, ever.

**Completion gate — role-owned access inventory (mandatory).** No "fully onboarded" wording until every lane passes a live smoke **from the agent's own runtime**. Track each lane `verified` / `verified-guarded` / `blocked` / `delegated`, each with exact evidence (command output, message id, screenshot, row id). Minimum lanes: runtime/doctor/model · durable supervisor · each channel's routing · task/wake/precheck · escalation-to-human · rule/state persistence · model/subagent/research · logs/backups — plus, only for bots that have them, each integration's READ path and GUARDED WRITE path. Config presence ≠ pass. **This inventory IS the capability manifest in [references/master-baseline-checklist.md](references/master-baseline-checklist.md) — build it there, work it to green, then run [references/final-verification-checklist.md](references/final-verification-checklist.md) as the last-mile sweep.**

## Channels & integrations — per-route references (pick the routes this agent needs)

Each onboarding "route" (the channel the agent is reached through, plus any external integration) has its OWN reference file. **Most bots need only a runtime + ONE channel; external integrations (QuickBooks, etc.) are per-bot and optional — pull that reference only for a bot that needs it.** Do not inline a route's full setup here — open its file.

| Route | Reference |
|---|---|
| **Discord** | [references/channel-discord.md](references/channel-discord.md) |
| **Slack** | [references/channel-slack.md](references/channel-slack.md) |
| **WhatsApp** | [references/channel-whatsapp.md](references/channel-whatsapp.md) |
| **Telegram** | [references/channel-telegram.md](references/channel-telegram.md) |
| _integration:_ **QuickBooks** | [references/integration-quickbooks.md](references/integration-quickbooks.md) |

**Home channel — ask every time.** Most agents want ONE home channel where they respond without being @mentioned; everywhere else stays mention-only (avoids bot noise/loops). During onboarding, ASK whether they want a home channel and which one. The usual mechanic: **have the user copy that channel's link and send it to the agent** ("this is your home channel — respond here without a mention"); the agent pulls the channel id from the link and sets its free-response config. How to copy the link + the config key are in each channel's reference. Invite the bot to that channel first (posting needs membership).

**Onboarding a route this skill doesn't cover yet** (Signal, Teams, Google Chat, Gmail, n8n, Stripe, …)? Add ONE new `references/channel-<x>.md` or `references/integration-<x>.md`, same pattern, and add a row here. Verify the mechanics against the live harness/console first — never write a route file from memory.

## Shared concept (any harness)

1. **Identity / persona** — a `SOUL.md`. **SOUL.md is identity-sacred: never create or edit one without the human's explicit approval of the exact content in the current conversation.**
2. **Model** — pick the LLM. Tool-calling agents need ≥64k context.
3. **Skills / capabilities** — give it the right skills for its role; least-privilege tools (don't cargo-cult a power agent's permissions onto a focused one).
4. **Channels** — Discord/Slack/Telegram/etc., mention-gated to avoid bot-to-bot loops.
5. **Registration / verification** — register where the harness expects, then verify it's live and healthy with a real test message.
6. **External-comms approval** — external sends (email, DMs) require explicit human approval. Draft-only by default for client-facing agents.

## Step 0 — The identity interview (ALWAYS first; never hardcode or template SOUL/AGENTS)

**Do not write `SOUL.md` or `AGENTS.md` from a template or from assumptions.** Every agent's identity is **elicited through a conversation with the owner**, then drafted, then written only on explicit approval (the SOUL lock). This is the bootstrap ritual — the answers, not a fixed template, produce the files. Run this interview, capture answers, draft, confirm:

1. **Name + id** — display name, agent id (`<id>`), channel handle.
2. **Mandate** — what is this agent FOR? single-client / domain / utility? Its core jobs (list).
3. **Reporting + escalation** — who is its boss (the owner? a lead agent?)? For operational issues, does it escalate to a lead first or straight to the owner? What's the escalation format?
4. **Peers + lanes** — its peers; what is explicitly NOT its lane.
5. **Communication style** — voice, tone, formality; audience-specific styles (client-facing vs internal); slop rules (em dashes, etc.); what the audience actually cares about.
6. **Personality** — buttoned-up or casual? formal or friend? quirks; what it optimizes for.
7. **Operating principles** — hard rules: draft-only vs send authority; testing constraints (never on production data? test targets only? where do test messages go?); data handling.
8. **Decision heuristics** — how it triages/decides/escalates; escalation format (options A/B + recommendation + links?).
9. **Anti-patterns** — what it must NEVER do.
10. **Channels + home channel** — Discord/Telegram/Slack/etc., exact channel IDs, mention-gating. **Ask explicitly: does it get a HOME channel** — one channel where it auto-responds WITHOUT a mention (its default place to report/answer)? If yes, capture which one and set it (see the per-channel reference; usual mechanic: copy that channel's link and give it to the agent). If no, it stays mention-only everywhere.
11. **Model + heartbeat** — LLM; cadence or event-driven.
12. **Tools / permissions** — least-privilege; elevated exec only if justified.
13. **Integrations** — which systems (n8n instance, email inbox, accounting, etc.).

Then draft `SOUL.md` (persona/voice/principles/role) and `AGENTS.md` (this agent's exact id/name/role/mention + the live roster + non-reply rule) **from the answers**, present for approval, and write only after sign-off (`~/.hermes/SOUL.md` on Hermes). The section *structure* is fixed; the *content* always comes from this interview.

---

## Hermes runbook (Nous Research) · VERIFIED against a live deploy (Hermes v0.16.0)

Hermes is a **single autonomous agent per install** — not a multi-agent gateway. "Another Hermes agent" = a separate install with its own `~/.hermes/`. It ships **batteries-included** (40–60+ built-in tools + an auto-seeded bundled skill catalog), so least-privilege means actively STRIPPING defaults — the opposite of an allowlist model.

**Config dir `~/.hermes/`:** `config.yaml` (settings), `.env` (secrets, chmod 600), `SOUL.md` (identity, slot #1), `skills/` (Hermes-format SKILL.md, auto-discovered), `logs/`, `sessions/`, `cron/`. Precedence: CLI args > `.env` > `config.yaml` > defaults. Code+venv install to `--dir`; binary at `~/.local/bin/hermes`.

**1. Install (least-privilege from the start):**
```bash
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash -s -- \
  --no-skills --skip-browser --non-interactive --skip-setup --dir /BIG/VOLUME/hermes-agent
```
- `--no-skills` = blank slate; writes a `.no-bundled-skills` marker that suppresses the bundled catalog on install AND every `hermes update`. **This is the skills least-privilege control.** Verify after: `hermes skills list` → 0 skills.
- `--skip-browser` skips Playwright/Chromium; `--non-interactive --skip-setup` skip the wizard (configure manually).
- `--dir` onto a roomy volume (code+venv is the bulk; `~/.hermes` config stays on home). **GOTCHA: do NOT pre-`mkdir` the `--dir`** — the installer refuses a pre-existing non-git directory.

**2. Model** (`config.yaml` `model.default` + `model.provider`; keys in `.env`):
```bash
hermes config set model.default openai/gpt-5.5
hermes config set model.provider openrouter   # auto | openrouter | openai-codex | gemini | anthropic | nous ...
```
`openrouter` accepts `OPENROUTER_API_KEY` *or* `OPENAI_API_KEY`. `openai-codex` = a ChatGPT/Codex subscription via `hermes auth` (no marginal per-token cost). View config with `hermes config show` (there is NO `config get`).

**3. SOUL** — write/copy the **approved** persona to `~/.hermes/SOUL.md` (identity-sacred, human-approved like any SOUL).

**4. Least-privilege TOOLS** — the default `platform_toolsets` uses presets (`hermes-discord`, `hermes-cli`) = the FULL toolset. Override per platform with an explicit minimal list:
```yaml
platform_toolsets:
  discord: [terminal, file, skills, todo]   # strips browser/web/image/tts/video/x_search
  cli:     [terminal, file, skills, todo]
```
Most heavy defaults are inert without their API keys, but scope explicitly anyway. `hermes doctor` shows active vs ⚠ missing-deps.

**5. Channel** — e.g. Discord token env var is **`DISCORD_BOT_TOKEN`** (NOT `DISCORD_TOKEN`). Scope it: `hermes config set discord.free_response_channels "<home-channel-id>"` (CSV; answers without a mention there) + `hermes config set discord.require_mention true`. Per-channel mechanics live in the `references/channel-*.md` files.

**6. Run as a service** — `hermes gateway install` creates a **systemd USER service** + enables **linger** (survives logout/reboot). It prompts interactively → `yes | hermes gateway install` for headless. Manage: `hermes gateway status`, `systemctl --user is-active hermes-gateway`, logs `journalctl --user -u hermes-gateway` or `~/.hermes/logs/`.

**7. Verify** — `hermes doctor` (model/tool connectivity); `hermes chat -q "one-line identity test"` (one-shot, confirms model+SOUL); the gateway log shows `[Discord] Connected as <Bot>#nnnn`.

**Skills are Hermes-format and auto-discovered** (`~/.hermes/skills/`, Hermes SKILL.md frontmatter, exposed as `/slash` commands, gated by the `skills` toolset). If you have a capability written for a different runtime, port it to Hermes format and drop it in `~/.hermes/skills/` — author the canonical version once and translate per-runtime rather than double-maintaining. Hermes does not scan other runtimes' skill directories.

Docs: <https://hermes-agent.nousresearch.com/docs> · Repo: <https://github.com/NousResearch/hermes-agent>

### Hermes DESKTOP app (Mac/Win/Linux) — the client-facing flow · learned live

The runbook above is the CLI/systemd server flow. A client (and their "Hermes desktop app") uses the **desktop app**, which runs a local Hermes (`~/.hermes/`) or connects to a remote gateway. What differs, and what bites in practice:

- **Onboarding path: choose "Full Setup," NOT "Quick Setup (Nous Portal)."** Quick Setup routes models through a metered Nous Portal subscription (no bring-your-own-OpenAI). Full Setup = your own OpenAI API key / Codex subscription. Token economics: riding your own ChatGPT/Codex subscription self-hosted is roughly an order of magnitude more tokens per dollar than metered Nous/API, and Nous Cloud cannot ride your subscription — for an always-on agent, self-host + subscription wins.
- **All secrets live in ONE file: `~/.hermes/.env` (chmod 600)** — model keys plus every channel/integration token. **It ships as a TEMPLATE with the keys COMMENTED OUT (`# SLACK_BOT_TOKEN=...`); you MUST uncomment them.** A value pasted after a `#` is invisible to the app (this alone can eat an hour). Verify a key is active, single, and well-formed with the value hidden: `grep -cE '^SLACK_BOT_TOKEN=' ~/.hermes/.env` (want `1`).
- **Model/auth mismatch = silent HTTP 400.** `openai-codex` (ChatGPT/Codex subscription) serves ONLY OpenAI models. Any Anthropic/Claude model on Codex auth throws `"model not supported when using Codex with a ChatGPT account"` and that component aborts. Audit EVERY model slot (main, auxiliary/vision, background/curator), not just the main one.
- **Platform deps lazy-install on first boot.** The first restart after adding channel config installs its libs (e.g. `slack-bolt`/`slack-sdk`) but may not start the listener that boot. **Restart once more** so the listener actually runs. A green "online" dot is not proof it's handling events.
- **The bare `hermes` CLI can crash** on a system-Python mismatch (`str | None` needs Python 3.10+). The desktop app bundles its own runtime and works — don't assume the CLI is the path.
- **Custom capabilities are skills.** A custom integration or tool is a Hermes skill (`~/.hermes/skills/<name>/`, helper in `scripts/`), not an MCP and not a side project. Hand the agent the helper script and let it author the skill, or drop a finished skill in — either way it lives in the runtime.
- **Per-route setup** (Slack, Discord, WhatsApp, Telegram, QuickBooks): see the **Channels & integrations** table above — one reference file per route.

---

## References
- Master + final-verification checklists: `references/master-baseline-checklist.md`, `references/final-verification-checklist.md` — the completion spine.
- Per-route mechanics: the `references/channel-*.md` and `references/integration-*.md` files.
- Hermes: <https://hermes-agent.nousresearch.com/docs> · <https://github.com/NousResearch/hermes-agent>

## Caveat
Harness mechanics change. Last-verified dates live in this skill's frontmatter (`metadata.verified`). Re-verify before each onboarding, and update this skill (and `metadata.verified`) when the mechanics shift.
