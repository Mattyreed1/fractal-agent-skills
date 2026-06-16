---
name: agent-collab
description: A protocol and toolkit for multi-agent collaboration. Agents post turns to a shared board, get each other's messages, challenge each other's work, and record the outcome as a permanent decision. Use when two or more agents (or an agent and a human) need genuine back-and-forth before producing an answer — "have agent X weigh in", "get a second agent to review this", "let the agents confer", "run this by the panel". Ships a zero-infra local backend and a Convex backend for real-time, multi-machine setups.
license: MIT
---

# agent-collab

Multi-agent collaboration over a shared board. One agent opens a thread, others reply, they converge, and the outcome is recorded as a durable decision. The whole thing runs through one script, `board.py`, with two interchangeable backends.

This is the collaboration half of the panel-of-models idea: a single model answering alone is weaker than several agents that see each other's reasoning, push back, and synthesize. `agent-collab` gives those agents a place to talk.

## When to use it

- "Have a conversation with <agent> about <X>"
- "Get <agent>'s take, then reconcile it with <other agent>'s"
- "Let the panel weigh in before you answer"
- "Two agents disagree — make them argue it out and record the call"

Skip it for one-shot questions a single agent can answer, or for assigning a unit of work (that's a task, not a discussion).

## The 6 primitives

Every primitive is a `board.py` subcommand. (Run `python3 board.py --help`.)

| Primitive | What it does | Command |
|---|---|---|
| **start** | Open a thread: first `post` with a `--conversation` slug + `--participants`. Participants are set once and inherited by every later post on the same slug. | `post --conversation <slug> --participants a,b,c` |
| **post** | Append a turn. Directed (`--to b`) or broadcast (`--to -`). | `post --from a --to - --content "..."` |
| **inbox** | List unread turns for an agent (read-only). | `inbox --agent a` |
| **wait** | Block until an unread turn arrives, then print it. Polls. | `wait --agent a` |
| **read** | Print the full thread and mark it read for that agent. | `read --agent a --conversation <slug>` |
| **decide** | Record the outcome as a permanent decision. **Always do this when a thread concludes** — it is the durable artifact. | `decide --title "..." --decision "..." --by a` |

## Standard flow

```
Agent A opens a thread
  → post --from A --to - --content "<opener>" --conversation feature-x --participants A,B,C
  → B and C see it (inbox / wait)
  → they reply: post --from B --to - --content "<reply>" --conversation feature-x   (participants inherited)
  → A polls: wait --agent A
  → ... iterate until convergence ...
  → whoever concludes: decide --title "..." --decision "..." --by A --approved-by <human> --impact "tag1,tag2"
  → surface the decision to the human + keep the thread for posterity
```

In practice the agents are usually subagents (spawned via your harness's task/agent tool) or separate sessions; each one calls `board.py` to post and read. A human participates with their own agent id (e.g. `--from human`).

## Backends

Pick with `--backend` or `AGENT_BOARD_BACKEND`.

### `local` (default) — zero infrastructure

Append-only JSONL under `./.agent-board/`. Works the instant you clone the repo. Perfect for a single machine: subagents and sessions on one box sharing a board. `wait` polls the file.

```bash
python3 board.py post --from planner --to - --content "Ship Friday or wait?" \
  --conversation ship --participants planner,critic,researcher
python3 board.py wait  --agent critic
python3 board.py decide --title "Ship date" --decision "Hold to Tuesday." --by planner --impact release
```

Override the location with `AGENT_BOARD_DIR`.

### `convex` — real-time, multi-machine

For agents on different machines that need sub-second wake-ups, point `board.py` at your own [Convex](https://convex.dev) deployment (free tier is plenty). The schema and functions are in [`backends/convex/`](backends/convex/) — deploy them, set `CONVEX_PROJECT_DIR`, and run with `--backend convex`. Same commands, same payloads.

### A2A

The protocol is deliberately shaped to map onto Google's [Agent2Agent](https://github.com/a2aproject/A2A) standard. See [`references/a2a-mapping.md`](references/a2a-mapping.md) if you want to expose this as an A2A gateway or interoperate with external agents.

## Data model

Two record types (full spec in [`references/protocol.md`](references/protocol.md)):

- **message** — `fromAgent`, optional `toAgent` (omit for broadcast), optional `conversationId` + `participants` (thread scope), `content`, `type`, `readBy[]`.
- **decision** — `title`, `context`, `decision`, `decidedBy`, optional `approvedBy`, `impactAreas[]`. **Never deleted.** Messages are prunable; decisions are the permanent record.

## Anti-patterns

| Don't | Why | Instead |
|---|---|---|
| Append turns to an ad-hoc markdown/scratch file | No identity, no unread tracking, no multi-party fan-out. It rots and nobody can find it. | Use `board.py post` |
| Conclude a thread without recording a decision | The conclusion gets buried in chat history; next week nobody can find what was decided. | Always end with `decide` |
| Scope a discussion as a "task" | A task is a unit of work with an owner and a deliverable. A discussion is many-to-many. Conflating them makes one agent try to "execute" the conversation. | Use a `--conversation` slug + `--participants` |
| Send the same message once per recipient | Fragments the thread and breaks reconstruction. | One broadcast post with `--participants` listing everyone |
| Broadcast a task that needs a single owner | Multiple agents race to claim it. | Direct it (`--to`) or assign it as a task |
