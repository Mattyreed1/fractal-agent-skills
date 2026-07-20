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
  → [Round 1] post --from A --to - --content "[Round 1 — Context] <problem + resources + A's thinking + open questions>" --conversation feature-x --participants A,B,C
  → B and C see it (inbox / wait)
  → [Round 2] B pushes back: post --from B ... --content "[Round 2 — Pushback] <holes, blind spots, failure modes>"   (participants inherited)
  → [Round 3] all research: post --from A/B/C ... --content "[Round 3 — Research] <answers + evidence from real lookups>"
  → A polls between rounds: wait --agent A
  → [Round 4] converge: post ... --content "[Round 4 — Converge] <the clean spec / task list / next steps>"
  → whoever concludes: decide --title "..." --decision "..." --by A --approved-by <human> --impact "tag1,tag2"
  → surface the decision to the human + keep the thread for posterity
```

In practice the agents are usually subagents (spawned via your harness's task/agent tool) or separate sessions; each one calls `board.py` to post and read. A human participates with their own agent id (e.g. `--from human`).

## The collaboration structure — 4 rounds

`board.py` moves the turns; this is how a collab actually produces good thinking. A substantive collab runs through four rounds, and the opener names each round with a `[Round N — <name>]` prefix so every participant knows their job that turn. Don't skip rounds, and don't converge early — the value is in the pushback and research that happen *before* agreement. (A one-shot question a single agent can answer doesn't need any of this.)

**Round 1 — Full context (initiator).** The opening post carries *everything*: the problem stated plainly, all the resources (links, files, data, prior decisions), the constraints, and the initiator's own current thinking — the options considered, which way they lean and why, the open questions, what they're unsure about. The goal is that every other participant starts from the initiator's complete mental model, not a thin brief. A stingy Round 1 wastes the whole collab: the others can only push on what they can see. Over-share.

**Round 2 — Pushback (responder).** The next agent does *not* agree and does *not* start building. Its one job is to poke holes: find the blind spots, challenge the assumptions, surface missing context, name the failure modes, ask "what about X?" Play devil's advocate even when the plan looks strong — exposing what Round 1 couldn't see about itself is the entire point of the round. Make the challenges concrete ("this breaks on empty input", "you assumed X but the data says Y"), not vibes. A pushback round that finds nothing usually means the responder didn't try.

**Round 3 — Research (all).** Each agent answers the Round 2 challenges *and* goes and does real research to close the gaps — read the file, run the query, check the actual state, look up the thing nobody knew. Come back with evidence, not just opinion. If a challenge genuinely can't be resolved, say so and carry it forward as a named risk instead of papering over it. Round 3 can loop once (a "3b") if the research surfaces something big enough to re-challenge.

**Round 4 — Converge (all).** Everyone agrees on *one* clean artifact: the spec, the task list, the next steps — crisp and executable. No new objections here; those belonged in Rounds 2–3. This artifact is exactly what becomes the `decide` record, and any agreed work is cut as separate tasks.

Rounds may **extend** (a 2b, a 3b) when a challenge opens a genuinely new thread, but they never **collapse**. Skipping Round 2 — jumping from "here's my plan" straight to "great, let's do it" — is the failure this structure exists to prevent. The pushback round is not politeness; it is the mechanism that catches blind spots before they reach the output. This is the panel-of-models idea in practice: several agents that see each other's reasoning, push back, and synthesize beat one agent answering alone.

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
| Open Round 1 with a thin brief and expect the others to fill it in | Round 1 is the shared mental model. Withheld context, resources, or thinking means the others can only push on what they can see — blind spots survive untouched. | Dump everything in Round 1: problem, resources, your own thinking, open questions. Over-share. |
| Jump from "here's my plan" straight to "great, let's do it" (skip Round 2) | The pushback round is the whole mechanism for catching blind spots before the output. Skipping it means agreeing with an unexamined plan. | Force a real Round 2 — poke holes, play devil's advocate, name failure modes, even when the plan looks strong. |
| Treat Round 3 as "post more opinions" | Round 3 is where uncertainty becomes evidence; opinions without lookups just re-litigate Round 2. | Actually go research — read the files, run the queries, check real state — then answer with evidence. |
| Scope a discussion as a "task" | A task is a unit of work with an owner and a deliverable. A discussion is many-to-many. Conflating them makes one agent try to "execute" the conversation. | Use a `--conversation` slug + `--participants` |
| Send the same message once per recipient | Fragments the thread and breaks reconstruction. | One broadcast post with `--participants` listing everyone |
| Broadcast a task that needs a single owner | Multiple agents race to claim it. | Direct it (`--to`) or assign it as a task |
