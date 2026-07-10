# Final verification checklist — exhaustive pre-acceptance sweep

Do not mark an agent onboarded until every applicable item is checked or explicitly `N/A` with reason. `references/master-baseline-checklist.md` is the canonical baseline (manifest, runtime, skills, tools, channels, acceptance); this sweep expands it for the last mile. Items tagged _(fleet)_ apply to multi-agent fleet members; skip them for a single-install Hermes agent unless noted.

## A. Origin + governance

- [ ] Source-of-truth lock exists (Hermes / multi-agent gateway / approved bridge) with runtime owner, host, channel owner, heartbeat/task owner, secret store, SOUL approval status, final evaluator.
- [ ] If the architecture changed mid-onboarding, old-path teardown and new-path build are tracked as separate artifacts/tasks.
- [ ] Mandate + explicit non-goals documented; owner/accountability line documented.
- [ ] `SOUL.md` exact content/change approved by the human, or the blocker is recorded.
- [ ] `SOUL.md` holds identity/persona/high-level mandate ONLY; detailed job procedures, routing, heartbeat mechanics, escalation workflows live in `AGENTS.md`/skills.

## B. Identity + context files

- [ ] Workspace/home path exists.
- [ ] `SOUL.md` present only if approved; `USER.md`/`MEMORY.md`/`WORKING.md` initialized as the harness expects.
- [ ] Identity file (`AGENTS.md`/`IDENTITY.md`) has id / name / role / mention / user id / roster / silence-routing rules.
- [ ] `TOOLS.md` contains no secrets.
- [ ] Heartbeat file correct or intentionally omitted with reason; it points to procedure, doesn't duplicate it.
- [ ] _(fleet)_ Existing agents' rosters updated; the new agent appears in every current roster/context file carrying mentions, and its own roster lists every current agent with canonical mention ids.

## C. Session injection + hooks

- [ ] Runtime config points to the correct workspace/home.
- [ ] A fresh session sees `DNA.md` (if any) and the approved `SOUL.md`, and states correct identity, boss, role, origin, routing rules.
- [ ] Fresh behavioral smoke passes: the agent states its mention/silence rule, boss/escalation path, allowed lane, external-send policy, and available skills/tools — answers match the manifest.
- [ ] Live NEGATIVE routing smoke: when the human @mentions a DIFFERENT agent, this agent stays silent and emits no visible text.
- [ ] _(fleet)_ Any runtime-specific injection hooks (context-injection hooks, timezone sync) pass, and the workspace-dir env points at the agent's own workspace.

## D. Runtime config

- [ ] Authoritative runtime exists on the selected host; version/doctor/status saved from the actual runtime.
- [ ] Same runtime home used for ALL evidence commands — no mixing retired/staging/current paths.
- [ ] Durable supervision installed with auto-start/auto-restart verified; heartbeat/wake verified if task-capable.
- [ ] Task/comment/notification pickup verified with BOTH no-work and positive ready-work fixtures; heartbeat-green alone is insufficient.
- [ ] Precheck wrappers use valid serialized payloads + correct auth/token boundary (no invalid JSON, no retired API paths).
- [ ] Tool allowlist least-privilege; sessions/subagent visibility intentionally scoped; schema/config validation passes.
- [ ] Effective config re-checked for env/config shadowing after restart (wrapper scripts, service env, `.env`, token vars).
- [ ] Cutover + rollback steps documented; no unsupervised manual/background runtime remains in the accepted state (unless an owner-approved temporary exception with owner/expiry/monitoring/hardening-task exists).

## E. Isolation + secrets

- [ ] Mount/access allowlist documented; explicit non-mount list documented.
- [ ] Scoped auth/session path + scoped credential files only.
- [ ] No shared fleet config, no other agent workspaces/auth dirs, no unrelated customer credentials reachable.
- [ ] No Docker socket / broad host paths unless explicitly approved.
- [ ] Negative leak-scan output saved (proves non-required workspaces/creds are NOT reachable).

## F. Skills

- [ ] Baseline selected per `master-baseline-checklist.md` for the runtime; any missing standard skill/capability has a written exception (reason, owner, expiry/follow-up, evaluator approval).
- [ ] Role-specific skills selected; each core-job integration has its canonical integration skill/adapter; overlays are additive and name what they derive from.
- [ ] Written intended-skill manifest exists (standard / domain / integration / runtime-troubleshooting / exceptions).
- [ ] Hermes: bundled/default skills disabled unless approved; final `skills list` compared against the manifest; a single troubleshooting skill is NOT accepted for a domain agent.
- [ ] Every listed skill load-tested by exact name from the live runtime — directory basename matches `name:` where the runtime requires it.
- [ ] The new agent confirms, from its own live runtime, which skills it has, why each exists, and any missing standard capability/exception.
- [ ] No admin/power skills added by habit; new/changed skills security-scanned.

## G. Tools + integrations

- [ ] Standard tool baseline selected; allowlist documented (required / runtime impl / permission / evidence); missing standard tool has a written exception.
- [ ] The new agent confirms, from its own live runtime, which tools/toolsets are enabled and what it's allowed to do with them.
- [ ] MCP servers scoped + configured; client/dedicated agents use a scoped config with `imports: []` and only their own servers; install paths pinned (no `@latest` unless approved).
- [ ] **Every live integration has smoke-test output** (a real read, or safe-sink write, through the agent's production env).
- [ ] **Every core-job function has a captured live test run** — the actual job, output recorded — not just "the integration is connected."
- [ ] Every write/send/admin capability has explicit approval or a documented guardrail + negative test proving it can't fire unapproved.
- [ ] Every role-owned monitoring lane is listed and verified or tracked as a dependent task (mailbox polling, workflow triage, docs/Drive access, KG read/write, blocked-task scans, dashboards, external-send guards).
- [ ] Heartbeat/precheck reports EACH role-owned integration status distinctly — a green core heartbeat cannot mask `access: missing` for a lane the agent owns.
- [ ] Email/client-comms lane (if applicable): approved mailbox verified read-only; live wake/precheck actually scans the mailbox for the owned sender/domain and surfaces hits; if approval-ready replies are in scope, the runtime produces a full handoff (inbound summary, recommended handling + rationale, `DRAFT — not sent` body, provider draft id/link, approval boundary) and creates a REAL draft-only artifact; the effective helper points at the guarded wrapper; send/reply is disabled pending explicit human approval.

## H. Model / auth / subagent / research routing

- [ ] Written routing contract (primary / non-coding subagent / coding subagent / research / fallbacks), each with provider AND billing/auth path — not just model family.
- [ ] Effective config from the authoritative home shows intended primary + delegation provider/model.
- [ ] Provider auth status from the actual runtime shows logged-in/usable; no `missing access_token` remains; no shared/fleet auth copied without explicit approval.
- [ ] Gateway restarted after auth/config change; fresh logs show no auth failure / wrong-provider fallback.
- [ ] Model smoke passes from the actual runtime after restart; non-coding subagent smoke proves the child path; coding path verified or N/A.
- [ ] Research path verified with direct evidence, or marked unresolved/delegated with owner + follow-up. Fallback providers documented as fallback only — never counted as the intended subscription path.

## I. Collaboration / task system (if team-participating)

- [ ] Agent registered where the harness expects; task pickup/evaluation path works if task-capable; error-log path works.
- [ ] Scheduled wake/precheck cannot be starved by stale unread messages/notifications.
- [ ] _(fleet)_ Existing→new and new→existing agent-to-agent message smokes pass, message ids recorded; the onboarding evaluator stays assigned unless explicitly reassigned.

## J. Dashboard / frontend (if applicable)

- [ ] Agent appears in the roster/menu and its files folder expands to ACTUAL context files in production (empty folder fails).
- [ ] Backend/registry path used by the frontend verified for representative new-agent files + one control agent.
- [ ] UI changes carry build/typecheck + fresh production screenshot; any frontend dependency is a linked task, not embedded here.

## K. Docs / memory

- [ ] Team/infra/project/client docs checked + updated; existing rosters updated; decision/SPEC/task links recorded.
- [ ] Durable memory checkpoint written.
- [ ] Any post-approval responsibility change is applied to the source context file, reflected in any human-facing review doc, and delivered to the agent as an explicit task — not left to silent file drift.

## K2. Completion-claim gate

- [ ] Every manifest lane has a status: `verified` / `verified-guarded` / `blocked` / `delegated`.
- [ ] Every `verified` / `verified-guarded` lane has live evidence from the authoritative runtime wrapper/env — not config/secret/skill presence.
- [ ] Every `blocked` / `delegated` lane is named in the final report with owner, task id, expiry/review, and whether it blocks live use.
- [ ] The final report avoids completion language unless all required lanes are verified or explicitly accepted as non-blocking follow-ups.
- [ ] No personal / shared / retired / unrelated credential was used to satisfy a scoped role-credential requirement.

## L. Final report must include

Agent origin + identity · runtime boundary · file paths · config paths · skill/tool/integration summary · evidence links/outputs · frontend status · docs status · remaining blockers · remaining role-owned integration gaps (each with owner + dependent task) · latest status correction (no obsolete artifact still claiming completion) · link to the tracking task/doc.

If any required item is incomplete, status is `blocked` or `done-with-explicit-dependent-task` — never bare `done`. If the authoritative runtime doesn't exist, can't run live smokes, or runs only as an unsupervised manual process without an approved exception, onboarding is **not done**: build/harden the runtime first.

## M. Secret-handoff gate

- [ ] Every token/password/API key was handed off through a scoped secret store or a one-time secure-drop — never a chat/Discord paste, never a default raw-file-path handoff.
- [ ] If a one-time link was used (e.g. Password Pusher with human approval): short expiry (~1h), single view, passphrase lockdown on, passphrase delivered out-of-band, receiver consumed once and stored directly into the scoped secret store without printing it.
