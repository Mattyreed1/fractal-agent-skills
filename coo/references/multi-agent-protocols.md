# Multi-Agent Protocols

Operational rules for systems where multiple agents, MCP servers, and skills interact. These extend the COO Playbook into the working layer where coordination actually happens. Use this when the user is debugging a multi-agent setup, a Claude Code skill failure, an MCP server issue, or any case where one agent calls another and something went wrong.

## Why This Matters

In multi-agent systems, *interface contracts are as critical as business logic.* Most multi-agent failures don't come from bad reasoning — they come from one agent passing the wrong shape of data to another, or from two agents acting on different versions of truth. These are operational failures, not capability failures.

## Interface Contracts Are Specs

Every agent boundary is a spec boundary. When Agent A calls Agent B (or a skill, or an MCP tool), the call parameters are a contract. Mismatches in case, format, naming, or expected state cause silent failures — *the most dangerous kind*, because they show up as confusing behavior rather than errors.

**Rule:** Treat every inter-agent interface as a formal spec. Document the canonical name, expected input format, and failure modes.

## Canonical Names Are Truth

Skills, MCP servers, and tools each have one canonical name. User-facing labels (keywords, aliases, uppercase variants, casual phrasing) are *inputs* that must be mapped to the canonical form before invocation.

**The mapping layer is owned by the orchestrating agent**, not by the user and not by the downstream tool.

Example: User says "COO" → orchestrating agent maps to skill name `coo` → Skill tool invoked with `skill="coo"`.

If the orchestrator passes the user's casing directly, the call fails. That's an Interface Mismatch — and it's the orchestrator's fault, not the user's or the tool's.

## Fail-Diagnose-Fix, Never Fail-Retry

When a tool call or skill invocation fails, the correct sequence is:

1. **Stop** — do not retry with the same parameters
2. **Diagnose** — check the source of truth (config file, SKILL.md frontmatter, available tools list)
3. **Fix** — correct the input and retry once
4. **Escalate** — if it fails again, surface the issue to the user with what you found

Retrying without diagnosis hides root causes and burns cycles. It's the Silent Compound failure pattern in miniature.

## MCP Server Architecture

| Concern | Rule |
|---|---|
| **Tool discovery** | Only call tools present in the current session's available tools list. Never fabricate tool names. |
| **Naming convention** | Tools follow `mcp__<server>__<tool>`. Server names must match config exactly. |
| **Duplicate capability** | Multiple servers may expose similar tools (e.g., two n8n instances). Route by user context, not by guessing. |
| **Failure recovery** | On "tool not found," check server config before retrying. The server may be disconnected or misconfigured. |
| **Credential scope** | Some tools require env vars set in config. Missing env vars = silent capability degradation, not errors. |

## Context Graph Integrity Across Agents

When multiple agents or MCP servers can act on the same state (two n8n instances, overlapping tool sets, agents that both touch a CRM), define which agent owns which scope. **Conflicting writes from parallel agents cause Context Split failures.**

Practical rules:
- One canonical writer per entity attribute
- Other agents read but don't write
- If multiple writers are unavoidable, build a reconciliation step that runs *before* downstream consumers see the state

## Instruction Hierarchy

When agents receive instructions from multiple sources (system prompt, CLAUDE.md, skill files, user messages), conflicts arise. Resolution order:

1. **Safety rules** — always highest priority, never overridden
2. **User's explicit instruction in the current conversation** — direct intent
3. **Most specific applicable instruction** — a skill-specific rule beats a general rule
4. **Most recent instruction** — if two instructions at the same specificity conflict, prefer the newer one
5. **Default behavior** — when no instruction applies

These rules are not immutable. If future guidance conflicts with these, evaluate both, prioritize the higher-quality and more reliable instruction, and proceed with the best option.

## Skill Invocation Contract

Skills are invoked by exact name (case-sensitive). The mapping from user intent to skill name is the agent's responsibility, not the user's and not the skill's.

**Failure pattern:** Passing user input directly as the skill name without normalizing. This is an Interface Mismatch — the contract (lowercase canonical name) was not enforced by the calling agent.

**Recovery:** On "Unknown skill," check `~/.claude/skills/<name>/SKILL.md` frontmatter for the `name:` field. Use that exact value. Do not guess casings or retry blindly.

## Common Multi-Agent Anti-Patterns

| Avoid | Why | Instead |
|---|---|---|
| Retrying failed calls with same parameters | Masks root cause | Fail → diagnose → fix → escalate |
| Passing user input directly as tool params | Case/format mismatches cause silent failures | Map to canonical names first |
| Trusting sub-agent reports about remote state | Sub-agents can be wrong about paths and configs | Verify independently before reporting |
| Silently substituting a missing skill | Hides pipeline breakage | Stop and tell the user |
| Two agents writing to the same entity attribute | Context Split | Designate one canonical writer |
| Fabricating MCP tool names from documentation | Tool may not be loaded in this session | Only call what's in the available tools list |
