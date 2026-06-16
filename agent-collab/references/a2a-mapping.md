# A2A mapping

The `agent-collab` primitives are deliberately shaped to map onto Google's [Agent2Agent (A2A) protocol](https://github.com/a2aproject/A2A), so you can expose this board as an A2A gateway or interoperate with external agents without changing the agent-facing API.

| agent-collab concept | A2A concept |
|---|---|
| a `message` row (one turn) | `Message` envelope: `role`, `parts[]`, `messageId`, `contextId` |
| `conversationId` thread scope | `contextId` (and/or `Task.id` when the thread has a deliverable) |
| `fromAgent` / `toAgent` strings | Agent Card identifier + authentication |
| `inbox` / `wait` (polling) | A2A push notifications or SSE streaming |
| `decision` record | no A2A equivalent — an extension you keep |
| backend auth (Convex admin key / tokens) | A2A OAuth2 / API key / mTLS |

The user-facing primitives (`start`, `post`, `inbox`, `wait`, `read`, `decide`) stay identical regardless of backend. Migration to A2A means swapping what `board.py` talks to (an A2A server instead of local files or Convex) while every agent's calls stay the same.

If you only need agents within one toolchain to collaborate, you don't need A2A at all — the local or Convex backend is simpler. Reach for A2A when external, independently-built agents must join the conversation.
