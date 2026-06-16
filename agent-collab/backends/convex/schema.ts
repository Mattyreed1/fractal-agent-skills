import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

// agent-collab Convex schema. Copy this file (and messages.ts / decisions.ts)
// into your Convex project's `convex/` directory, then `npx convex deploy`.
export default defineSchema({
  messages: defineTable({
    fromAgent: v.string(),
    toAgent: v.optional(v.string()),           // omit for broadcast
    conversationId: v.optional(v.string()),    // thread scope (a slug)
    participants: v.optional(v.array(v.string())),
    content: v.string(),
    type: v.string(),                          // message|question|review|decision|status_update
    readBy: v.array(v.string()),
  })
    .index("by_toAgent", ["toAgent"])
    .index("by_conversation", ["conversationId"]),

  // Immortal outcomes. No delete mutation — by design.
  decisions: defineTable({
    title: v.string(),
    context: v.optional(v.string()),
    decision: v.string(),
    decidedBy: v.string(),
    approvedBy: v.optional(v.string()),
    impactAreas: v.array(v.string()),
  }),
});
