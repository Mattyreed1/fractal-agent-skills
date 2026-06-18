---
name: content-visuals
description: Stage 5 of the Content Engine. Create visuals and diagrams for an approved LinkedIn post script. Use when the user approves the script or you receive a 'Create Visuals' task. Creates architecture diagrams, infographics, KG visualizations per brief specs.
license: MIT
metadata:
  version: 3.0.0
  created: 2026-03-27
  updated: 2026-04-28
  author: content-orchestrator
  domains: ['content', 'design', 'diagrams']
---

# Content Visuals

## Trigger

the user approves the script in the Discord thread, OR you receive a `Create Visuals — {name}` task from `content-scripting`.

## Who

CC (`content-creator`)

## Inputs

- Approved script (Notion page, `## Final Script` section)
- Visual Suggestions section from the content brief (written by `content-brief` v1.0.0+)

## Steps

### 1. Read the brief's Visual Suggestions

Use `notion` (read mode) to fetch the page. The brief's `## Visual Suggestions` describes the *substance* to render, hook-agnostic. You decide creative direction (style, framing, branding) based on the script's tone.

**Then lock the core idea (BLOCKING, before choosing any concept).** Write ONE sentence: "the single idea this visual must land is ___." Derive it from the brief's **Core Claim** and the source's own **central metaphor**, NEVER the hook (the hook is the entry line; the visual must illustrate the *payoff*). Test every candidate concept against it and reject any that only illustrate the hook, a sub-claim, or a tangent. **Form must fit the idea:** a loop or compounding idea needs a cycle that visibly grows; a comparison needs contrast; a hierarchy needs layers; a quantity needs a stat. A static arrangement for a process/loop idea is automatically wrong, so catch it before rendering. If the piece reacts to a source, pull the source's key phrase (e.g. "hill-climbing machine") and ask "what does THAT look like?" This gate exists because a visual shipped illustrating only the hook ("the model is replaceable") and missed the post's actual thesis (the compounding learning loop), then got polished through ~8 execution iterations downstream of the wrong concept (2026-06-17).

### 2. Create visuals

Common types:

- **Architecture diagrams**: data flow with labeled arrows, component boxes. Technical, not decorative.
- **KG visualizations**: circular nodes, labeled relationship edges. Obsidian-style. Use real data (`cd <your-board-dir> && npx convex run kg:getConnected '{"entityId":"<id>","hops":1}'`).
- **Infographics**: one-pager summarizing key points. Dark theme, brand colors.

Visual rules (the user's standing constraints):
- ❌ NO pyramids
- ❌ NO concentric circles
- ✅ Data flow diagrams with arrows
- ✅ Circular nodes with labeled edges for KG
- ✅ Clean, technical, informative

Use the agent runtime's native browser (Chromium, headless+noSandbox) for rendering when needed.

**For node-edge diagrams (architecture data-flow, KG graphs), prefer the `diagram-design` skill (D2)** over hand-built HTML/CSS — it auto-lays-out nodes and edges and styles them on-brand. Render `diagram-design/scripts/render.sh graph.d2 out.svg --brand fractal` (or `--brand founder-freedom`, matching the piece's brand), then frame the SVG. Keep infographics and simple step-rows as HTML/CSS. The brand rules above (no pyramids/concentric circles; data-flow arrows; circular KG nodes) still apply.

**Runtime:** D2 must exist where this runs. On Claude Code/Mac it's installed (`~/.claude/skills/diagram-design`). On the agent runtime, check `which d2`; if absent, install D2 on the VPS (follow-up via your deployment tooling) and sync this engine via `skill-translate`. Until then, fall back to the browser render above.

Output PNGs to:
- **On the agent fleet (fleet agents):** `~/.agent/<your-workspace>/projects/content-engine/visuals/<slug>/`
- **On Mac (local):** `projects/<brand-content>/<YYYY-MM-DD-slug>/visuals/` where `<brand-content>` is `fractal-ai-content` or `founder-freedom-content`. Brand must already be set by `content-pipeline`. The `visuals/` directory sits next to the piece's `brief.md`.

### 3. Post in Discord thread

Use **this format:**

```
## Visuals — {content piece name}

**Visual 1: {name}**
{description of what it shows}
[attached image]

**Visual 2: {name}**
{description of what it shows}
[attached image]

---
@user — approve visuals or request changes. Max 2 revision rounds.
```

### 4. Move Notion Stage

Stage: `Scripting` → `Visual Editing`

## Output Format (handoff to content-packaging)

Once the user approves:

1. **Upload visuals to Notion page** (use Notion API for image blocks, or `notion` if adding captions/descriptions as markdown)
2. **board task**: title=`Package Content — {name}`, assignedTo=`content-orchestrator`, evaluator=`content-orchestrator`, priority=P2
3. **board message to CO**: `Visuals approved for {name}. Ready for packaging. Notion page: {url}`

## Edge cases

- **Brief has no Visual Suggestions**: propose 1-2 visuals based on the script content. Post proposals in thread before creating.
- **Tools can't produce the requested style**: note limitations, produce closest alternative, explain in thread.
- **the user rejects style direction**: ask for a reference image or specific direction. Don't guess twice.
- **Visuals need real system data (KG, architecture)**: query the system. Use actual data, not made-up examples.
- **Lead magnet artifact (e.g. GitHub repo screenshots) needed**: those come during packaging — don't try to fabricate them here.
