---
name: content-packaging
description: Stage 6 of the Content Engine. Build lead magnet, create Tally email-capture form, update Notion landing page, and assemble the final post package with CTA link. CO handles infrastructure (GitHub repo, Tally form via API, landing page). CC assembles the final post text.
license: MIT
metadata:
  version: 3.0.0
  created: 2026-03-27
  updated: 2026-04-28
  author: content-orchestrator
  domains: ['content', 'infrastructure', 'lead-generation']
---

# Content Packaging

## Trigger

the user approves visuals. CC sends board message to CO that content is ready for packaging, OR CO receives a `Package Content — {name}` task.

## Who

CO (`content-orchestrator`) — all packaging tasks.

## Inputs

- Approved script (Notion page `## Final Script` — fetch via `notion` read mode)
- Approved visuals (Notion page or Discord thread)
- Lead magnet spec (from brief's `## Lead Magnet` section)
- Landing page (should already exist in Resources teamspace; create if missing)

## CRITICAL — URL rules

### Notion links

**ALWAYS use the published public URL format:**
- ✅ `https://your-workspace.notion.site/{page-slug}-{page-id}`
- ❌ `https://www.notion.so/your-workspace/{page-slug}-{page-id}`
- ❌ `https://notion.so/your-workspace/{page-slug}-{page-id}`

The `notion.so/your-workspace/` URL is the private editor link. It requires login. The `your-workspace.notion.site/` URL is the published public link. Every redirect, CTA, and landing page link MUST use the public format.

### Tally webhook

**ALWAYS use the n8n webhook — never Convex:**
- ✅ `https://<your-n8n-instance>/webhook/tally-lead-magnet`
- ❌ `https://your-deployment.convex.site/tally/webhook`

This URL is constant across all forms. It triggers the n8n workflow that logs the lead.

**Webhook must be configured manually** in Tally dashboard (Integrations → Webhooks). The Tally API does not support webhook creation.

## Steps

### 1. Build lead magnet

If not already done:
- Create GitHub repo (or finalize existing one)
- Ensure README, setup instructions, all files complete
- Add visuals from CC to the repo if applicable

For Gumroad-distributed lead magnets, see the `gumroad` skill.

### 2. Create Tally form (automated via API)

```
1. GET template form 44L2DA blocks + settings
2. Create new form: name = "Access to {lead magnet name}"
3. Set redirect URL → published public Notion page (your-workspace.notion.site format)
4. Publish form
5. MANUAL: Configure webhook in Tally dashboard → Integrations → Webhooks → https://<your-n8n-instance>/webhook/tally-lead-magnet
```

### 3. Update landing page

Notion page in Resources teamspace:
- Embed Tally form
- Add visuals
- Update copy to match final script angle
- Sections: Headline, Who it's for, What this is, Why it matters, How it works, Get it, About Fractal AI + cal.com link

### 4. Assemble final post

Combine approved script + CTA with landing page link. Post in Discord thread:

```
## Final Package — {content piece name}

**Post text:**
{full post with CTA link}

**Images:** {list attached files}
**Landing page:** {URL — must be your-workspace.notion.site format}
**Tally form:** {URL}
**Lead magnet:** {GitHub URL}

---
@user — final review. Approve to publish.
```

### 5. Move Notion Stage

Stage: `Visual Editing` → `Packaging/Posting`

## Output Format (handoff to content-publish)

Once the user approves:

1. **board task**: title=`Publish — {name}`, assignedTo=`content-creator`, priority=P2
2. **board message to CC**: `Final package approved for {name}. Publish to LinkedIn. Post text + images in thread. Read content-publish skill.`
3. Provide CC with: post text, image files, landing page URL

## Edge cases

- **No lead magnet specified in brief**: skip Tally form. Post without gated content. Note in thread.
- **Tally API fails**: retry once. If still fails, create form manually in dashboard and document the URL.
- **Landing page doesn't exist**: create one in Resources teamspace following the template.
- **Visuals not uploaded to Notion yet**: pull from Discord thread. Upload before proceeding.
- **Brief's Lead Magnet section is `[NEEDS INPUT]`**: bounce back to CC/the user before packaging — the gate is open and you don't have an artifact to package.
