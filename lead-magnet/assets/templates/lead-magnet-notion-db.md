# Template: Resource Database Lead Magnet

## What This Is
A Notion database template that the audience can duplicate into their own workspace. Packaged with a description, property guide, and a companion LinkedIn post to promote it.

## When to Use
The conversation contains a structured collection of information, a tracking system, or an organizational framework that maps naturally to a database. Look for:
- Lists of tools, resources, or vendors with attributes
- Tracking systems (projects, clients, content, habits)
- Decision frameworks with scoring criteria
- Reference libraries or knowledge bases
- Pipeline/funnel structures

## Deliverables

### 1. Notion Database Schema
Define using the Notion MCP `create-database` tool:
- Table name and description
- Properties with types, options, and colors
- At least one useful view (filtered/sorted)
- 3-5 example rows showing intended usage
- A template entry if the DB supports recurring entries

Schema documentation format:
```
## {Database Name}

### Properties
| Property | Type | Options/Notes |
|----------|------|---------------|
| Name | Title | Primary identifier |
| Status | Select | To Review, Active, Archived |
| Category | Multi-select | {relevant categories} |
| ... | ... | ... |

### Views
1. **{View Name}** — {filter/sort description}

### Example Rows
{3-5 rows showing intended usage}
```

### 2. README / Description
Structure:
```
## {Database Name}

### What it tracks
{1-2 sentences — the outcome}

### Who it's for
{Target audience + use case}

### How to use it
1. Duplicate this template to your Notion workspace
2. {Customize step}
3. {First entry workflow}

### Properties explained
- **{Property}**: {Why this field exists and how to fill it}
```

### 3. Companion LinkedIn Post
Use the `linkedin-post.md` template. The post should:
- Lead with the PROBLEM the database solves
- Show how disorganization or lack of tracking costs real time/money
- CTA: "Comment '{keyword}' and I'll send you the template"

## Quality Checks

| Check | Pass | Fail |
|-------|------|------|
| Schema is complete | All properties defined with types | Missing types or unnamed columns |
| Example rows exist | 3-5 rows showing real usage | Empty database |
| Properties are explained | User knows what goes where | Ambiguous column names |
| At least 1 useful view | Filtered/sorted for a real workflow | Default "all items" only |
| Companion post written | LinkedIn post using template | DB shipped without promotion content |

## Notion Storage
Save to **Content DB** (`<CONTENT_DB_ID>`) with:
- Content type: Lead Magnet
- Format: Notion Database
- Status: Draft
- Include schema definition in the page body
