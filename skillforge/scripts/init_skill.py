#!/usr/bin/env python3
"""
Skill Initializer - Creates a new skill from template.

Adapted from Anthropic's skill-creator init_skill.py.

Usage:
    init_skill.py <skill-name> --path <path>

Examples:
    init_skill.py my-new-skill --path ~/.claude/skills
    init_skill.py api-helper --path /custom/location
"""

import sys
from pathlib import Path


SKILL_TEMPLATE = """---
name: {skill_name}
description: >
  [TODO: Complete and informative explanation of what the skill does and when
  to use it. Include specific scenarios, file types, or tasks that trigger it.
  This is the primary trigger mechanism — Claude reads this to decide when to
  load the skill. Put ALL "when to use" info here, not in the body.]
license: MIT
---

# {skill_title}

[TODO: 1-2 sentences explaining what this skill enables]

## Triggers

- `[TODO: trigger phrase 1]` - [description]
- `[TODO: trigger phrase 2]` - [description]
- `[TODO: trigger phrase 3]` - [description]

## Quick Reference

| Input | Output | Duration |
|-------|--------|----------|
| [TODO] | [TODO] | [TODO] |

## Process

[TODO: Choose structure that fits this skill's purpose:

**Workflow-Based** — clear step-by-step procedures
**Task-Based** — different operations/capabilities
**Reference/Guidelines** — standards or specifications
**Capabilities-Based** — interrelated features

Delete this guidance section when done.]

## Anti-Patterns

| Avoid | Why | Instead |
|-------|-----|---------|
| [TODO] | [TODO] | [TODO] |

## Verification

- [ ] [TODO: measurable success criterion]
- [ ] [TODO: measurable success criterion]

## Extension Points

1. **[TODO]:** [description]
2. **[TODO]:** [description]
"""

EXAMPLE_SCRIPT = '''#!/usr/bin/env python3
"""
Example helper script for {skill_name}.

Replace with actual implementation or delete if not needed.
"""

def main():
    print("Example script for {skill_name}")
    # TODO: Add actual script logic

if __name__ == "__main__":
    main()
'''

EXAMPLE_REFERENCE = """# Reference Documentation for {skill_title}

Replace with actual reference content or delete if not needed.

Reference docs are ideal for:
- Comprehensive API documentation
- Detailed workflow guides
- Information too lengthy for SKILL.md
- Content only needed for specific use cases
"""


def title_case_skill_name(skill_name):
    """Convert hyphenated skill name to Title Case."""
    return ' '.join(word.capitalize() for word in skill_name.split('-'))


def init_skill(skill_name, path):
    """Initialize a new skill directory with template SKILL.md."""
    skill_dir = Path(path).resolve() / skill_name

    if skill_dir.exists():
        print(f"Error: Skill directory already exists: {skill_dir}")
        return None

    try:
        skill_dir.mkdir(parents=True, exist_ok=False)
        print(f"Created skill directory: {skill_dir}")
    except Exception as e:
        print(f"Error creating directory: {e}")
        return None

    skill_title = title_case_skill_name(skill_name)

    # Create SKILL.md
    skill_md = skill_dir / 'SKILL.md'
    skill_md.write_text(SKILL_TEMPLATE.format(
        skill_name=skill_name,
        skill_title=skill_title
    ))
    print("Created SKILL.md")

    # Create resource directories with examples
    try:
        scripts_dir = skill_dir / 'scripts'
        scripts_dir.mkdir(exist_ok=True)
        example_script = scripts_dir / 'example.py'
        example_script.write_text(EXAMPLE_SCRIPT.format(skill_name=skill_name))
        example_script.chmod(0o755)
        print("Created scripts/example.py")

        references_dir = skill_dir / 'references'
        references_dir.mkdir(exist_ok=True)
        example_ref = references_dir / 'reference.md'
        example_ref.write_text(EXAMPLE_REFERENCE.format(skill_title=skill_title))
        print("Created references/reference.md")

        assets_dir = skill_dir / 'assets'
        assets_dir.mkdir(exist_ok=True)
        print("Created assets/")
    except Exception as e:
        print(f"Error creating resource directories: {e}")
        return None

    print(f"\nSkill '{skill_name}' initialized at {skill_dir}")
    print("\nNext steps:")
    print("1. Edit SKILL.md — complete TODO items, write description with when-to-use")
    print("2. Customize or delete example files in scripts/, references/, assets/")
    print("3. Run quick_validate.py when ready")
    return skill_dir


def main():
    if len(sys.argv) < 4 or sys.argv[2] != '--path':
        print("Usage: init_skill.py <skill-name> --path <path>")
        print("\nSkill name: hyphen-case, lowercase, max 64 chars")
        print("\nExamples:")
        print("  init_skill.py my-skill --path ~/.claude/skills")
        print("  init_skill.py api-helper --path /custom/location")
        sys.exit(1)

    skill_name = sys.argv[1]
    path = sys.argv[3]

    result = init_skill(skill_name, path)
    sys.exit(0 if result else 1)


if __name__ == "__main__":
    main()
