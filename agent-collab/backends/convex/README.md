# Convex backend

Use this when agents run on **different machines** and need sub-second wake-ups, rather than the single-machine local file board. [Convex](https://convex.dev) has a free tier that's more than enough.

## Deploy

1. Create a Convex project (if you don't have one):
   ```bash
   npm create convex@latest agent-board
   cd agent-board
   ```
2. Copy the three files in this directory into the project's `convex/` folder:
   ```bash
   cp schema.ts messages.ts decisions.ts /path/to/agent-board/convex/
   ```
3. Deploy:
   ```bash
   npx convex deploy
   ```

## Point board.py at it

```bash
export AGENT_BOARD_BACKEND=convex
export CONVEX_PROJECT_DIR=/path/to/agent-board    # where `npx convex run` should execute
```

Then every `board.py` command runs against your deployment:

```bash
python3 board.py post --from planner --to - --content "..." --conversation X --participants planner,critic
python3 board.py inbox --agent critic
python3 board.py decide --title "..." --decision "..." --by planner
```

## Functions exposed

| Function | Type | Purpose |
|---|---|---|
| `messages:post` | mutation | append a turn (inherits participants within a conversation) |
| `messages:getUnread` | query | unread turns for an agent |
| `messages:markRead` | mutation | mark a turn read |
| `messages:list` | query | full thread by `conversationId` |
| `decisions:record` | mutation | record a permanent decision |
| `decisions:list` | query | recent decisions |

## Real-time wake-ups

`board.py wait` polls `getUnread`. For true push delivery (wake an idle agent the instant a turn lands), add a Convex [scheduled function](https://docs.convex.dev/scheduling) or a client subscription that triggers your agent runner. That wiring is environment-specific and intentionally left to you — the protocol doesn't require it, polling works fine for most setups.
