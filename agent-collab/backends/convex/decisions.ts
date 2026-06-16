import { mutation, query } from "./_generated/server";
import { v } from "convex/values";

// Record a permanent decision. There is intentionally no delete mutation.
export const record = mutation({
  args: {
    title: v.string(),
    context: v.optional(v.string()),
    decision: v.string(),
    decidedBy: v.string(),
    approvedBy: v.optional(v.string()),
    impactAreas: v.optional(v.array(v.string())),
  },
  handler: async (ctx, args) => {
    const id = await ctx.db.insert("decisions", {
      title: args.title,
      context: args.context,
      decision: args.decision,
      decidedBy: args.decidedBy,
      approvedBy: args.approvedBy,
      impactAreas: args.impactAreas ?? [],
    });
    return { id, status: "recorded" };
  },
});

export const list = query({
  args: { limit: v.optional(v.number()) },
  handler: async (ctx, { limit }) => {
    const all = await ctx.db.query("decisions").order("desc").collect();
    return all.slice(0, limit ?? 20);
  },
});
