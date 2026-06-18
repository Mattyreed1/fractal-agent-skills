---
name: content-scripting
description: Stage 4 of the Content Engine. Write the full LinkedIn post from an approved hook. Runs an execute-evaluate loop (max 3 iterations), posts the draft in the Discord thread for the user review, handles up to 2 revision rounds.
license: MIT
metadata:
  version: 3.0.0
  created: 2026-03-27
  updated: 2026-04-28
  author: content-orchestrator
  domains: ['content', 'copywriting', 'linkedin']
---

# Content Scripting

## Trigger

the user picks a hook in the Discord thread, OR you receive a `Write Post — {name}` task from `content-hooks`.

## Who

CC (`content-creator`)

## Inputs

- Chosen hook (from Discord thread, or from the `## Chosen Hook` section on the Notion page)
- Content brief (on Notion page — use `notion` read mode to fetch as markdown)

The brief (written by `content-brief` v2.0.0+) contains everything you need: Core Claim, Why This Matters, Target Audience, Proof & Artifacts, Relevant Quotes, Resources, Lead Magnet, Visual Suggestions, Open Questions / Gaps, Raw Context. Mine it fully.

## Steps

### 1. Write full LinkedIn post

Use the execute-evaluate loop (writer subagent + evaluator subagent, max 3 iterations).

Post structure:
- **Hook**: chosen by the user (do not modify without permission)
- **Body**: insight + proof + explanation. Short paragraphs. Real data > theory. Pull from brief's Proof & Artifacts and Raw Context sections.
- **CTA**: lead magnet teaser (from brief's Lead Magnet section) + clear action (e.g. "Comment MEMORY to get the starter kit")

If the brief has a Relevant Quotes section, consider using one as a payoff line or punctuation — don't force it.

### 2. Post draft in Discord thread

Use **this exact format:**

```
## Draft v1 — {content piece name}

{full post text}

---
**Word count:** {count}
**Read time:** ~{minutes} min
**CTA:** {what the reader does}

@user — review when ready. I can revise up to 2x.
```

### 3. Move Notion Stage

Stage: `Title/Thumb/Hook` → `Scripting`

### 4. Handle the user's feedback

If the user requests changes:
- Post revised draft as `## Draft v2` in the thread
- Max 2 revision rounds. If still not approved, escalate to CO.

## Output Format (handoff to content-visuals)

Once the user approves:

1. **Add to Notion page**: Use `notion` skill (mode: `append`) to write a `## Final Script` section with the approved text
2. **board task**: title=`Create Visuals — {name}`, assignedTo=`content-creator`, evaluator=`content-orchestrator`, priority=P2
3. **Mark scripting task**: done

## Edge cases

- **Hook doesn't lead naturally into the body**: adapt the transition but keep the hook intact. Note adaptation in thread.
- **Brief lacks enough proof for a full post**: flag to CO via board. Request additional research or artifacts before writing — don't fabricate.
- **Brief has `[NEEDS INPUT]` markers**: those are gaps. Decide if you can write around them or if you need to bounce back to CO.
- **Post exceeds 3000 characters (LinkedIn limit)**: trim. Prioritize proof density over explanation.
- **the user rewrites significant portions**: accept. Update the Final Script on Notion with the user's version.
- **Execute-evaluate loop exceeds 3 iterations**: ship the best version, post it, note which iteration in the thread.
