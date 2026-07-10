# Master baseline checklist — the onboarding spine

The canonical completion contract for onboarding ANY agent, on any harness. **Onboarding is not "done" until every applicable lane below is verified by the NEW AGENT, from its own live runtime, with real evidence.** Config / secret / skill presence is never proof — a live smoke through the exact runtime and env the agent uses in production is. The per-route references (`references/channel-*.md`, `references/integration-*.md`) add mechanics; they never weaken or replace this checklist.

## How this checklist works — it is per-agent and self-updating

You do not run a fixed list. You BUILD the list for THIS agent from its mandate, then verify it:

1. **Establish what the agent needs** (Step 0 identity interview + section 0 below): mandate → the exact channels, apps, integrations, tools, and core functions it must have. A finance agent needs QuickBooks; a content agent needs none of it. Derive the lanes from the role — never cargo-cult a power agent's access onto a focused one.
2. **Write those into the capability manifest** (section 0). Every required channel / app / integration / tool / function becomes a lane. **This is the "auto-update for this specific agent" step — the manifest IS the agent-specific checklist.**
3. **Verify every lane** — the agent proves, from its own live runtime, that the access is real AND the function works (a live test run), or the lane is an explicit owned exception.
4. **Complete only when every lane is `verified` / `verified-guarded`,** or an explicit `blocked` / `delegated` exception with owner + follow-up.

Three rules that are easy to skip and cost the most:

- **The new agent verifies itself.** "I (the onboarder) checked the config" does not count. The agent reads its own runtime and confirms what it has, what each thing is for, and what it can and cannot do. This is what catches the gap where a token sits in a file but the agent still can't use it.
- **Every core function gets a live test run.** Not "the integration is connected" — an actual run of the job (read this account, categorize this transaction, answer this query, route this message), output captured as evidence.
- **Access is established, then verified, per agent.** The manifest grows to fit the agent; the gate is that every lane it grew has passing evidence.

## 0A. Completion-language lock

Do not use completion language (`onboarded`, `complete`, `fully operational`, `done`, `accepted`, `live`) while any applicable lane is unverified — unless every incomplete lane has an explicit exception (owner, follow-up task/id, expiry/review date) and the status does NOT claim completion. If a missing lane blocks safe live use, status stays `blocked` / `not-live`, not `live-but-not-closed`.

For integrations, config/env/secret presence is not proof. Evidence is a live read-only (or safe-sink write) smoke through the **exact wrapper / runtime / env** the agent uses in production. A bare script that bypasses the agent's real `.env` / service env / scoped config / mounted secrets cannot be acceptance evidence.

## 0. Capability manifest — build this BEFORE wiring anything

Write a manifest with one row per required capability, derived from the mandate:

```
capability | required? | runtime implementation | permission level | verification evidence | exception/task id
```

- **capability** — a channel (Slack / Discord / Telegram / WhatsApp), an integration (QuickBooks / Notion / n8n / email / Drive / calendar / KG), a tool (exec / file / research / messaging), or a runtime gate (model+auth / supervision / wake).
- **permission level** — read / search / draft / write / send / admin. **Default is read / search / draft** until a write/send/admin lane is explicitly justified and guarded.
- **verification evidence** — the live-runtime proof (command output, message id, draft id/link, screenshot, row id). Blank = not done.

Exception format for any missing or narrowed lane:

```
Exception: <capability>
Reason:    <why this agent should not / cannot yet have it>
Owner: <person/agent>   Expiry/review: <date>   Follow-up: <task id, or N/A + approved reason>
```

## 1. Runtime + source-of-truth gate

- [ ] Source-of-truth lock written before implementation (Hermes-harness / multi-agent-gateway origin / explicitly-approved bridge). Pick ONE runtime story; don't build two competing versions.
- [ ] Lock names: runtime owner · host/location · channel owner · heartbeat/task owner · **secret store** · `SOUL.md` approval status · **model/auth path** · integration owner · **final evaluator**.
- [ ] The authoritative runtime actually exists on the selected host before any evidence is treated as acceptance evidence.
- [ ] Runtime version / doctor / status output captured from the actual runtime home (e.g. `hermes doctor`, `hermes config show`).
- [ ] Effective loaded config/env audited after startup/restart — wrapper scripts, service env, `.env`, and token vars do not shadow the intended source-of-truth config.
- [ ] Durable supervision installed and verified (systemd/launchd/container/compose/managed service, auto-start + auto-restart). Manual `nohup` / tmux / ad-hoc gateway runs are incident workarounds, not accepted completion. If durable supervision is unavailable, capture an owner-approved temporary exception (owner, expiry, monitoring, hardening task) — otherwise onboarding is not accepted.

## 1A. Wake / task pickup (task-capable agents only)

- [ ] Scheduled/manual wake runs from the authoritative runtime home.
- [ ] Heartbeat alone is NOT task readiness — a positive ready-work fixture proves task/comment/notification pickup.
- [ ] Wake/precheck payloads are valid serialized inputs with the correct auth/token scope for the current API boundary.
- [ ] Canonical ready-work lookup outranks stale unread/message/notification backlog; stale backlog is capped/summarized before it reaches prompts.
- [ ] No-work fixture exits cleanly without blocking future ready work; ready-work fixture selects the intended item and records live evidence.

## 1B. Model / auth / subagent / research routing gate

- [ ] Written model-routing contract before launch: primary provider/model/billing path, default non-coding subagent path, coding subagent path (if coding is in scope), research path, allowed fallbacks.
- [ ] Contract distinguishes **provider from model**. `openai-codex / gpt-5.5 via ChatGPT-Codex OAuth subscription` ≠ `openrouter / openai/gpt-5.5` ≠ OpenAI API-key billing. (Codex/ChatGPT auth serves ONLY OpenAI models — an Anthropic model on Codex auth throws HTTP 400 and that component silently aborts. Audit EVERY model slot: main, vision/auxiliary, background/curator.)
- [ ] Effective config from the authoritative home shows the intended primary provider/model AND the delegation/subagent provider/model.
- [ ] Provider auth status from the actual runtime shows the intended path logged-in/usable (no `missing access_token`, no stale env, no silent fallback to the wrong provider). Secrets not exposed.
- [ ] Gateway/service restarted after config/auth changes; fresh logs show no provider-auth failure or wrong-provider fallback.
- [ ] **Real model smoke passes from the live runtime after restart.** A raw API/CLI test outside the agent runtime does not satisfy this.
- [ ] Non-coding subagent/delegation smoke proves the configured child path; coding-subagent path verified if coding is in scope, else explicit N/A.
- [ ] Research path verified with direct evidence (Perplexity/MCP/API), or explicitly marked unresolved/delegated with owner + follow-up. A `research` skill adapter alone is not proof of live search access.

## 2. Skills / capability baseline

Select exactly one baseline for the runtime and list it in the manifest.

**Client / Hermes agent (default for a new client agent):** Hermes ships batteries-included and does NOT inherit any other fleet's skills. Start blank (`--no-skills` / `.no-bundled-skills`), verify `hermes skills list` == 0, then add ONLY the skills the mandate requires. Each core-job integration needs its own real skill/adapter (a QuickBooks job needs a `quickbooks` skill, not a generic "finance" note). Load-test every listed skill by exact name from the live runtime — discovery-by-list is not proof.

**Multi-agent fleet member:** if you run a fleet of task-capable agents, define a shared standard baseline once (e.g. task-system · plan-mode · research · notion · session-logs · summarize · task-evaluate · task-execute · messaging · memory-consolidation · agent-collab · error-logging · secret-intake), plus role/domain overlays and any canonical integration skill (`n8n`, `notion`, calendar, email). Narrowing the baseline requires a written reason + evaluator approval. Do not create parallel/renamed duplicates of a standard skill — adapters must keep the canonical name and only carry runtime-specific loading notes.

- [ ] Every intended baseline skill resolves in every layer the runtime uses (disk, workspace/symlink, per-agent config, registry, file index — whichever apply).
- [ ] Core-job integrations have their canonical integration skill; domain overlays are additive, never substitutes.
- [ ] The new agent confirms its skill surface from its own live runtime (not onboarder-side inspection).
- [ ] Any narrowed/missing baseline skill has the section-0 exception block.

## 3. Tool baseline (least-privilege)

Minimum surface, scoped by runtime + role:

```
skills/read-skill    # list + load its own skills from the live runtime
file/read            # scoped context/runbooks only; no broad unrelated workspaces
status/diagnostic    # inspect own runtime/config to debug routing/auth/model
todo/working-memory  # track local multi-step work where supported
<channel>/messaging  # only if that channel is enabled; obey primary/mention routing
task/collab          # if task-capable or team-participating
research/search      # if it answers factual/domain questions
external-write/send  # DISABLED by default — needs explicit role need + guardrail + smoke
```

- [ ] Allowlist is least-privilege and documented (required / runtime impl / permission / evidence / exception).
- [ ] Broad tools (`exec`, elevated shell, admin/config mutation, GitHub write, email/message send, credentials) have explicit justification, guardrails, and a smoke + negative test.
- [ ] The new agent confirms its enabled tools — and what it may/may-not do with them — from its own live runtime.

## 4. Identity, context, roster gate

- [ ] Required identity/context files exist or are explicit N/A (`SOUL.md`, and per harness: `AGENTS.md`/`IDENTITY.md`/`DNA.md`/`TOOLS.md`/`HEARTBEAT.md`/`USER.md`/`MEMORY.md`/`WORKING.md`).
- [ ] `SOUL.md` exact content/change is human-approved BEFORE it is created/edited/synced. Identity is sacred.
- [ ] Fresh live-runtime identity smoke: the agent states its correct name, boss, lane, source-of-truth, external-send policy, mention/NO_REPLY routing, and escalation path.
- [ ] Rosters + mention ids updated in the new agent AND in existing peers where the harness routes between agents.

## 5. Channel gate (run per channel the agent uses)

For each channel in the manifest (mechanics: the matching `references/channel-*.md`):

- [ ] Bot/app is private + least-privilege; token handed off through a scoped secret store, **never a chat/Discord paste**.
- [ ] Exactly one **home channel** (auto-respond, no mention) if the agent owns one; everywhere else stays mention-only (prevents bot-to-bot loops). If multi-agent, peers don't auto-respond in this agent's home channel and this agent stays silent when a peer is mentioned.
- [ ] Bot invited to every channel it must post in (posting needs membership).
- [ ] Live smokes pass: home-channel unmentioned response · mention response elsewhere · non-home unmentioned ignore · (multi-agent) peer non-response + peer-mention silence.
- [ ] Scopes/events proven by probing the API for the exact `needed:` error, not guessed (see `channel-slack.md`).

## 6. Frontend / dashboard gate (only if the agent appears in one)

- [ ] Agent shows correct id/name/role/display metadata in the roster/menu.
- [ ] Its files/workspace expand to show ACTUAL files in production — an empty or label-only render fails onboarding.
- [ ] Backend list/read APIs used by the frontend return representative new-agent files.
- [ ] UI changes carry build/typecheck + a fresh production screenshot; incomplete frontend work is a linked follow-up task, not buried in this skill.

## 7. Final acceptance gate

- [ ] Every applicable item in `references/final-verification-checklist.md` is checked or `N/A` with reason.
- [ ] Scripted preflight passes where one exists.
- [ ] Integration smoke + negative tests attached.
- [ ] Every core-job **function** has a captured live test run (not just "connected").
- [ ] Final report includes: origin · runtime boundary · file/config paths · skill/tool/integration summary · evidence links · frontend status · remaining blockers/tasks · any status correction.
- [ ] No superseded artifact still claims completion.

**Acceptance rule:** if any applicable lane lacks passing evidence, an approved exception, or a linked follow-up task, onboarding is **not** complete.
