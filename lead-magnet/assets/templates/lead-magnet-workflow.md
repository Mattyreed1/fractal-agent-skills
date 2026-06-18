# Template: Workflow Automation Lead Magnet

## What This Is
An importable n8n workflow that the audience can deploy into their own n8n instance. Packaged with a description, setup instructions, and a companion LinkedIn post to promote it.

## When to Use
The conversation contains a workflow pattern, automation logic, or multi-step process that can be built as an n8n workflow. Look for:
- Step-by-step processes with clear inputs/outputs
- Integration patterns (API → transform → destination)
- Recurring operational tasks that follow predictable logic
- Agent workflows with tool chains

## Deliverables

### 1. Workflow JSON
- Valid n8n workflow JSON, importable via n8n UI
- Use the `n8n` skill to validate node configurations and type versions
- Include Sticky Notes inside the workflow explaining each section
- Strip credentials (user configures their own)
- Name the workflow clearly: "{What It Does} — Fractal AI"

### 2. README / Description
Structure:
```
## {Workflow Name}

### What it does
{1-2 sentences — the outcome, not the mechanics}

### Who it's for
{Target audience + use case}

### How it works
1. {Step 1 — trigger}
2. {Step 2 — process}
3. {Step 3 — output}

### Setup
1. Import the workflow JSON into your n8n instance
2. Configure credentials for: {list services}
3. {Any environment-specific setup}
4. Test with: {specific test scenario}

### Customization
- {What users can change to fit their use case}
- {Key nodes to modify}
```

### 3. Companion LinkedIn Post
Use the `linkedin-post.md` template. The post should:
- Lead with the OUTCOME the workflow produces (not the tool)
- Include a specific example or war story of using it
- CTA: "Comment '{keyword}' and I'll send you the workflow"

## Quality Checks

| Check | Pass | Fail |
|-------|------|------|
| Workflow imports clean | User can import JSON and see all nodes | Broken references or missing nodes |
| Credentials stripped | No API keys or tokens in JSON | Leaked credentials |
| Sticky Notes explain logic | Each section has context | Raw nodes with no explanation |
| README has setup steps | User can get running in <15 min | "Figure it out" |
| Companion post written | LinkedIn post using linkedin-post.md template | Workflow shipped without promotion content |

## Notion Storage
Save to **Content DB** (`<CONTENT_DB_ID>`) with:
- Content type: Lead Magnet
- Format: Workflow
- Status: Draft
- Attach workflow JSON as a code block in the page
