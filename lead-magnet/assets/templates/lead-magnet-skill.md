# Template: Agent Skill Lead Magnet

## What This Is
A Claude Code / Claude Cowork skill that the audience can install into their `~/.claude/skills/` directory. Packaged with a description, install instructions, and a companion LinkedIn post to promote it.

## When to Use
The conversation contains a repeatable process, framework, or workflow that can be encoded as an agent skill. Look for:
- Multi-step processes with clear phases
- Specialized knowledge that improves agent output
- Workflows that chain multiple tools or skills
- Decision trees or classification logic
- Domain expertise that Claude doesn't have by default

## Deliverables

### 1. Skill Directory
Follow the skillforge template structure:
```
{skill-name}/
├── SKILL.md          # Frontmatter + triggers + phases + anti-patterns
└── references/       # Deep docs if needed
    └── {topic}.md
```

SKILL.md requirements (per skillforge):
- YAML frontmatter: `name` (kebab-case, ≤64 chars), `description` (≤1024 chars), `license`
- 3-5 trigger phrases
- Quick Reference table
- Process phases with verification gates
- Anti-patterns table
- Verification checklist

### 2. README / Install Guide
Structure:
```
## {Skill Name}

### What it does
{1-2 sentences — what capability this adds to your agent}

### Install
1. Download the `{skill-name}/` directory
2. Place it in `~/.claude/skills/{skill-name}/`
3. Restart Claude Code / Claude Desktop

### Usage
Trigger with: "{trigger phrase}"

### Example
{Show a real invocation and expected output}
```

### 3. Companion LinkedIn Post
Use the `linkedin-post.md` template. The post should:
- Lead with the PROBLEM this skill solves (repetitive work, inconsistent output, missing expertise)
- Explain the concept of "agent skills" briefly (not everyone knows)
- Show a before/after: manual process vs. skill-powered process
- CTA: "Comment '{keyword}' and I'll send you the skill"

## Quality Checks

| Check | Pass | Fail |
|-------|------|------|
| SKILL.md has valid frontmatter | name, description, license present | Missing or malformed YAML |
| 3-5 triggers defined | Varied, natural language | Single trigger or none |
| Phases are clear | User can follow the process | Vague or missing steps |
| Install instructions work | Drop in directory, restart, trigger | Requires debugging to get working |
| Companion post written | LinkedIn post using template | Skill shipped without promotion |

## Notion Storage
Save to **Content DB** (`<CONTENT_DB_ID>`) with:
- Content type: Lead Magnet
- Format: Agent Skill
- Status: Draft
- Include the full SKILL.md content in the page body
