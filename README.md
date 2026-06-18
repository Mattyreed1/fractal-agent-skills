# mr-agent-skills

A collection of [Claude Code](https://docs.claude.com/en/docs/claude-code) skills for AI agent workflows — built around one idea:

> **Panels of AI models consistently beat a single "genius" model.**

The two headline skills put that into practice: a **decision engine** that runs any call through a panel of perspectives and a judge, and a **collaboration protocol** that lets multiple agents confer before they answer.

## The headliners

### 🧠 `deep-deliberation` — the decision engine

An orchestrator that pushes any decision through a panel and a judge. It's worth understanding *why* it's not one skill but a chain — the chaining **is** the panel:

```
deep-deliberation                  ← orchestrator (runs the pipeline)
├─ devils-advocate   challenge the premise, surface hidden constraints
├─ last30days        scan what practitioners are actually saying      (needs API keys)
├─ research          verify the specific claims against sources        (needs API keys)
├─ coo               map the real operational constraints
├─ (adversarial debate — agents argue it out)
├─ judge             score both sides, pick a winner
└─ action-plan       turn the verdict into a phased plan
```

Runs in **lite mode** (the reasoning skills) with zero setup. Add your own Perplexity / OpenAI / xAI keys to unlock the live-research stages (`research`, `last30days`).

### 🤝 `agent-collab` — multi-agent collaboration

A protocol for agents to post turns to a shared board, challenge each other, and record a decision. Ships a **zero-infra local backend** (works immediately) and a **Convex backend** for real-time multi-machine setups, plus a note on mapping to Google's A2A standard.

### ✍️ `content-pipeline` — the content engine

Same idea as the decision engine, applied to publishing: one piece moves through a **chain of single-purpose stages**, each its own skill, instead of one prompt trying to do everything.

```
content-strategy                   ← optional Stage 0: pillars, editorial calendar, channel mix
content-pipeline                   ← orchestrator (routes a piece by its Stage field)
├─ content-ideation    diverge on angles, converge on one concept
├─ content-brief       assemble the context + proof brief (hook-agnostic)
├─ content-hooks       generate + grade title and hook options
├─ content-scripting   write the full post from the chosen hook
├─ content-visuals     on-brand diagrams / infographics for the post
├─ content-packaging   lead magnet + capture form + landing page
└─ content-publish     publish, then collect 7-day metrics
                       (content-case-study is a specialized ideation→brief entry for client work)
```

The stages lean on supporting skills: `content-hooks` calls `hook-machine`, `content-visuals` calls `diagram-design` / `social-canvas`, briefs pull from `notion`, and `lead-magnet` / `youtube-script` extend the cascade. All are included. The skills are written as a **template** — plug your own Notion DB IDs and channel into the `<...>` placeholders.

## All skills

| Skill | What it does |
|-------|--------------|
| `deep-deliberation` | Run a decision through a full panel + judge + action plan |
| `agent-collab` | Multi-agent collaboration board (local or Convex) |
| `devils-advocate` | Challenge a premise, surface hidden constraints |
| `judge` | Impartially score a multi-agent debate and pick a winner |
| `action-plan` | Turn a verdict into a phased, metric-anchored plan |
| `coo` | Operational analysis — systems, bottlenecks, risk, deletion |
| `research` | Deep web research via Perplexity |
| `last30days` | Reddit + X + web research from the last 30 days |
| `writing` | Headlines, hooks, structure, anti-AI-slop rules |
| `scrape` | Web scraping + lead enrichment method ladder |
| `browser` | Route between real-browser control and headless automation |
| `design-principles` | A product/UX design constitution — action-first, progressive disclosure, simplicity |
| `frontend-design` | Distinctive, production-grade frontend interfaces |
| `google-maps` | Places, directions, geocoding via the Maps API |
| `gumroad` | Create and publish Gumroad products via the API |
| `mcp-builder` | Build an MCP server |
| `mcp-setup` | Install, configure, and debug MCP servers |
| `skill-creator` | Create, edit, and eval-test Claude Code skills |
| `skillforge` | Route to or create the right skill; dedupe before building |
| **Content Engine** | |
| `content-pipeline` | Orchestrate a piece through the 7 content stages |
| `content-strategy` | Plan pillars, editorial calendar, channel mix (the layer above) |
| `content-ideation` | Diverge then converge on the angle for a content seed |
| `content-brief` | Assemble the context + proof brief for a locked concept |
| `content-hooks` | Generate and grade title + hook options against a rubric |
| `content-scripting` | Write the full post from an approved hook |
| `content-visuals` | Create on-brand diagrams / infographics for a post |
| `content-packaging` | Lead magnet + capture form + landing page assembly |
| `content-publish` | Publish and collect 7-day performance metrics |
| `content-case-study` | Turn a real client engagement into a case-study brief |
| `hook-machine` | Build a data-driven hook rubric from your top/bottom posts |
| `diagram-design` | Brand-styled D2 diagrams (SVG / PNG) |
| `social-canvas` | Render social graphics / carousels via a headless browser |
| `lead-magnet` | Turn expertise into a downloadable lead magnet |
| `youtube-script` | Long-form founder-story / personal-journey video scripts |
| `notion` | Notion MCP setup, schema-caching discipline, and API gotchas |

## Install

Claude Code loads skills from `~/.claude/skills/`. Drop in the ones you want:

```bash
git clone https://github.com/Mattyreed1/mr-agent-skills.git
cp -R mr-agent-skills/deep-deliberation mr-agent-skills/devils-advocate \
      mr-agent-skills/judge mr-agent-skills/action-plan mr-agent-skills/coo \
      mr-agent-skills/agent-collab ~/.claude/skills/
```

Then, in any Claude Code session:

```
> stress-test this decision: should we raise prices 20% or hold?
```

## Contributing / privacy

This repo is mirrored from a private collection, with owner-specific content removed. A CI check (`.github/workflows/private-scan.yml`) scans every push and **fails if any private data is detected**, so nothing personal leaks on an update.

## License

[MIT](LICENSE) — built by [Matty Reed](https://fractalai.agency). Use it, fork it, ship it.
