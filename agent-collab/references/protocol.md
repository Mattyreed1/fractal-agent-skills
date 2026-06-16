# agent-collab protocol spec

The protocol is backend-agnostic. `board.py` implements it twice (local JSONL, Convex); this file is the contract both honor.

## Records

### message (turn delivery)

| Field | Type | Notes |
|---|---|---|
| `id` | string | unique turn id |
| `ts` | number | created-at timestamp |
| `fromAgent` | string | sender id |
| `toAgent` | string? | recipient id; omit for broadcast |
| `conversationId` | string? | thread scope (a slug); the discussion-scoping mechanism |
| `participants` | string[]? | set on the FIRST post of a conversation, inherited thereafter |
| `content` | string | the turn body |
| `type` | string | `message` \| `question` \| `review` \| `decision` \| `status_update` |
| `readBy` | string[] | agent ids that have read this turn |

A turn is "for" agent X when: `toAgent == X` (directed), OR `toAgent` is absent and either there is no `conversationId` (global broadcast) or X is in the conversation's `participants` (scoped broadcast). An agent never receives its own turn. "Unread" = X not in `readBy`.

### decision (immortal outcome)

| Field | Type | Notes |
|---|---|---|
| `id` | string | unique decision id |
| `title` | string | short title |
| `context` | string? | what conversation produced this, and why |
| `decision` | string | the actual call |
| `decidedBy` | string | agent or human id who made the call |
| `approvedBy` | string? | human in the loop |
| `impactAreas` | string[] | tags for findability |

**Decisions are never deleted.** Messages are prunable after a retention window; decisions are the permanent record. If someone asks "what did we decide about X?", the answer comes from the decisions store, not from re-reading the thread.

## Turn lifecycle

```
  A: post (from=A, to=-, conversation=X, participants=[A,B,C])
        │ append message
        ▼
  message is now "unread" for B and C
        │
        ▼  B/C discover it via inbox (poll) or wait (block)
  B: read  (marks B into readBy)  →  B: post (reply, conversation=X)
        │
        ▼  A discovers B's reply via wait
  ... iterate until convergence ...
        │
        ▼
  someone: decide (title, decision, decidedBy, approvedBy, impactAreas)
```

In the **local** backend, "discovery" is polling the JSONL file (good for one machine). In the **Convex** backend, a write can trigger a real-time subscription or a notification row that a worker delivers to agents on other machines.

## Multi-party patterns

**1:1 directed** — `post --from A --to B`. Only B's inbox sees it.

**Broadcast to a panel** — `post --from A --to - --conversation X --participants A,B,C`. Every participant except the sender sees it; participants are inherited by later posts on slug `X`.

**Global broadcast** — `post --from A --to -` with no conversation. Every agent sees it until they read it. Use sparingly (announcements, all-hands questions); don't broadcast work that needs a single owner.

## Identity & auth

`fromAgent`/`toAgent` are plain strings — name agents however your roles run (`planner`, `critic`, `researcher`, `ops`, or `agent-1`/`agent-2`). There is no per-agent signing in the reference implementation; trust is the trust boundary of whatever runs `board.py`. For the Convex backend, the deployment's auth (admin key or scoped tokens) is the gate. A human participates with their own id.

## Retention & cleanup

| Record | Retention | Mechanism |
|---|---|---|
| messages | as long as you want; prune on your own schedule | local: rotate/trim the JSONL; convex: a scheduled cleanup |
| decisions | forever | none — never delete |

The local board grows append-only; for long-running setups, periodically archive `messages.jsonl`. Decisions stay.

## Failure modes

| Failure | Symptom | Recovery |
|---|---|---|
| Agent never wakes | turn posted but recipient idle | local: ensure the recipient actually runs `wait`/`inbox`; convex: confirm your wake mechanism (subscription/cron) is live |
| Two agents claim a broadcast | race on who responds | don't broadcast single-owner work — direct it |
| Orchestrator dies mid-thread | replies sit unread | a fresh session resumes via `inbox`/`read` — full history is on the board |
| Thread concludes, no decision recorded | the call is lost in history | always `decide` at the end |
