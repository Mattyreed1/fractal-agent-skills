# Integration Handoffs

This documents the exact mechanics of chaining to other skills during Phase 4 (DELIVER).

## Skill Chain Order

```
Phase 3 output (structured draft)
    │
    ▼
1. WRITING SKILL — polish hooks, headlines, rhythm, anti-slop
    │
    ▼
2. USER REVIEW — present polished draft for approval/edits
    │
    ▼
3. NOTION SKILL — save to correct DB with proper properties
    │
    ▼
4. ARTIFACT CREATION (if lead magnet) — build the actual workflow/DB/skill
```

## 1. Writing Skill Chain

### When to Invoke
ALWAYS. Every piece of content passes through the writing skill before delivery. No exceptions.

### How to Invoke
Use the `Skill` tool with `skill: "writing"`.

### What to Pass
Provide the full structured draft and request specific polish:

**For LinkedIn posts:**
- Request: hook optimization (reference `hooks.md`), headline options (reference `headlines.md`), rhythm check (reference `blogs.md`)
- Ask for 2-3 hook variations
- Request anti-slop verification

**For lead magnet titles:**
- Request: 3-5 title options using headline formulas from `headlines.md`
- Specify the format: "[Number] [Action] [Type] for [Audience] to [Outcome]"

**For lead magnet body content:**
- Request: rhythm check, paragraph structure, anti-slop scan
- Flag any sections that feel generic or AI-generated

### What to Check After
- No anti-slop violations (per writing skill lines 82-119)
- Hook creates genuine curiosity gap
- Specific numbers, names, and outcomes preserved (not genericized)
- Voice matches brand profile

## 2. Notion Skill Chain

### Critical: Fetch Instructions First
**BEFORE any Notion operation**, you MUST:
1. Invoke the `notion` skill OR directly fetch page `<INSTRUCTIONS_PAGE_ID>`
2. Read the "MR Assistant Instructions" page completely
3. Only then proceed with saves

This is non-negotiable. The instructions page defines required properties, allowed values, and validation rules.

### Notion Databases

| Database | ID | What Goes Here |
|----------|----|---------------|
| **Content** | `<CONTENT_DB_ID>` | All content pieces: posts, lead magnets, drafts |
| **Templates** | `<CONTACTS_DB_ID>` | Reusable content frameworks and templates |

### How to Save Content

Use the Notion MCP tools (`mcp__mr-notion__*`):

1. **Fetch the instructions page** to get current DB schema and required properties
2. **Create a page** in the Content DB with:
   - Title: the content piece title
   - Status: Draft
   - Content type: {LinkedIn Post | Lead Magnet}
   - Format (for lead magnets): {Workflow | Notion Database | Agent Skill | Checklist | Mini-Guide}
   - Content pillar: match to brand profile pillars
   - Body: the full polished content as page content

3. **If a reusable template was created**, also save to Templates DB with the template structure.

### Property Names
Property names come from the instructions page, NOT from this document. Always check the instructions page for current field names and allowed values. The names above are descriptive — the actual Notion properties may use different capitalization or naming.

## 3. n8n Skill Chain (Workflow Lead Magnets Only)

### When to Invoke
Only when the selected output format is a workflow automation lead magnet.

### How to Invoke
Use the `Skill` tool with `skill: "n8n"`.

### What to Pass
- The workflow concept and node list
- Request validation of node types and type versions
- Request Sticky Note annotations for each workflow section

### Optional: Deploy to n8n
If the user wants the workflow deployed (not just exported as JSON):
- Use n8n MCP tools (`mcp__mr-n8n__*`) to create the workflow
- Validate with `n8n_validate_workflow` before creation
- Strip credentials (user configures in n8n UI)

## Error Handling

| Error | Response |
|-------|----------|
| Writing skill unavailable | STOP. Tell user. Do not deliver unpolished content. |
| Notion instructions page unreachable | STOP. Tell user. Do not save to Notion without reading instructions first. |
| Notion MCP tools fail | Check config per CLAUDE.md MCP troubleshooting. Report to user. |
| n8n skill unavailable | Can still create workflow JSON manually, but flag that it's unvalidated. |
| User rejects polished draft | Return to Phase 3 with their feedback. Re-transform and re-polish. |

## Phase 4 Gate
- Writing skill was invoked (not skipped)
- User approved the polished draft
- Notion instructions page was fetched before any save
- Content saved to correct DB with proper properties
- For lead magnets: artifact was created AND companion post was written
