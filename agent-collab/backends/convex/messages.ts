import { mutation, query } from "./_generated/server";
import { v } from "convex/values";

// Append a turn. Participants are set on the first post of a conversation
// and inherited by every later post on the same conversationId.
export const post = mutation({
  args: {
    fromAgent: v.string(),
    toAgent: v.optional(v.string()),
    conversationId: v.optional(v.string()),
    participants: v.optional(v.array(v.string())),
    content: v.string(),
    type: v.optional(v.string()),
  },
  handler: async (ctx, args) => {
    let participants = args.participants;
    if (args.conversationId && !participants) {
      const first = await ctx.db
        .query("messages")
        .withIndex("by_conversation", (q) => q.eq("conversationId", args.conversationId))
        .order("asc")
        .first();
      participants = first?.participants ?? undefined;
    }
    const id = await ctx.db.insert("messages", {
      fromAgent: args.fromAgent,
      toAgent: args.toAgent,
      conversationId: args.conversationId,
      participants,
      content: args.content,
      type: args.type ?? "message",
      readBy: [],
    });
    return { id, status: "posted" };
  },
});

// Unread turns for an agent: directed to them, or a broadcast they participate in,
// excluding their own turns and anything they've already read.
export const getUnread = query({
  args: { agentId: v.string() },
  handler: async (ctx, { agentId }) => {
    const all = await ctx.db.query("messages").collect();
    return all.filter((m) => {
      if (m.fromAgent === agentId) return false;
      if (m.readBy.includes(agentId)) return false;
      if (m.toAgent) return m.toAgent === agentId;
      if (!m.conversationId) return true; // global broadcast
      return (m.participants ?? []).includes(agentId);
    });
  },
});

export const markRead = mutation({
  args: { messageId: v.id("messages"), agentId: v.string() },
  handler: async (ctx, { messageId, agentId }) => {
    const m = await ctx.db.get(messageId);
    if (m && !m.readBy.includes(agentId)) {
      await ctx.db.patch(messageId, { readBy: [...m.readBy, agentId] });
    }
    return { status: "ok" };
  },
});

// Full thread for reconstruction.
export const list = query({
  args: { conversationId: v.string() },
  handler: async (ctx, { conversationId }) => {
    return await ctx.db
      .query("messages")
      .withIndex("by_conversation", (q) => q.eq("conversationId", conversationId))
      .order("asc")
      .collect();
  },
});
