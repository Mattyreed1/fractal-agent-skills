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

The stages lean on supporting skills: `content-hooks` calls `hook-machine`, `content-visuals` calls `diagram-design` / `social-canvas`, briefs pull from `notion`, and `lead-magnet` / `youtube-script` extend the cascade. All are included. The skills are written as a **template** — they will not run until you fill in your own workspace details. See **[Setting up the Content Engine](#setting-up-the-content-engine)** below.

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
git clone https://github.com/Mattyreed1/fractal-agent-skills.git
cp -R fractal-agent-skills/deep-deliberation fractal-agent-skills/devils-advocate \
      fractal-agent-skills/judge fractal-agent-skills/action-plan fractal-agent-skills/coo \
      fractal-agent-skills/agent-collab ~/.claude/skills/
```

Then, in any Claude Code session:

```
> stress-test this decision: should we raise prices 20% or hold?
```

## Setting up the Content Engine

The Content Engine skills (`content-*`, plus `notion` / `hook-machine` / `diagram-design` / `social-canvas` / `lead-magnet` / `youtube-script`) ship as **templates**. They carry `<PLACEHOLDER>` tokens where one workspace's specifics used to be, so they will not work until you fill them in for *your* setup.

> **If you're an agent setting these up: do not guess these values. Have a short discussion with the user to gather them first (Step 1), then find-and-replace (Step 2).** Filling a Notion ID or channel with a guess silently points the pipeline at the wrong place.

### Step 1 — interview the user

Ask, and record the answers:

1. **Brands & folders** — Which brand(s) do you publish under? The skills assume two (`fractal-ai-content`, `founder-freedom-content`); rename those folders to yours or collapse to one.
2. **Notion (or another CMS)** — Do you run your content calendar in Notion? If yes, collect the DB IDs in the table below. If no, tell me your tool and I'll adapt the read/write steps.
3. **Review channel** — Where do drafts get reviewed (a Discord/Slack channel)? I need its channel ID for the hook / script / visual threads.
4. **Solo or fleet** — One agent running every stage, or a split (an orchestrator role + a content-creator role)? `content-orchestrator` / `content-creator` are just labels — rename or collapse them.
5. **Lead capture** — How do lead magnets capture emails (an n8n webhook + form, Gumroad, none)? Used by `content-packaging`.
6. **Strategy inputs** — Your content pillars, platforms, and cadence (for `content-strategy`).

### Step 2 — fill the placeholders

Replace these once, repo-wide (find them with `grep -rl '<CONTENT_DB_ID>' .`):

| Placeholder | What it is | Where to find it |
|---|---|---|
| `<INSTRUCTIONS_PAGE_ID>` | Your Notion "content rules" page (voice, schema, allowed values); `notion` reads it first | Notion page → Copy link → the 32-char id |
| `<CONTENT_DB_ID>` + `<CONTENT_DB_DATA_SOURCE_ID>` | Your content-calendar database | Notion DB → Copy link / retrieve data source |
| `<QUOTES_DB_ID>`, `<QUOTABLE_PEOPLE_DB_ID>` | Quote-bank DBs `content-brief` mines | Notion |
| `<CASE_STUDIES_DB_ID>` | Case-study source-of-record DB | Notion |
| `<CONTACTS_DB_ID>` `<TASKS_DB_ID>` `<MEETINGS_DB_ID>` `<PROJECTS_DB_ID>` `<COMPANIES_DB_ID>` `<LEADS_DB_ID>` | Other DBs the briefs / handoffs reference (only the ones you use) | Notion |
| `<LANDING_PAGE_ID>` | Lead-magnet landing page | Notion |
| `your-content-channel-id` | Chat channel for review threads | Discord/Slack channel ID |
| `<your-n8n-instance>`, `<YOUR_N8N_NOTION_CREDENTIAL_ID>` | Lead-capture automation | your n8n |
| `your-workspace.notion.site` | Your published Notion site domain | Notion → Publish |
| `<YOUR_NOTION_INTERNAL_INTEGRATION_TOKEN>` | Notion MCP auth | Notion → Integrations (keep out of git) |
| `fractal-ai-content` / `founder-freedom-content` | Per-brand project folders | rename to your brands |
| `content-orchestrator` / `content-creator` | Agent role names | rename or collapse to one |

Don't have a given DB? Drop the step that uses it, or point it at your equivalent.

### Step 3 — runtime tokens (leave these alone)

Tokens like `<slug>`, `<brand>`, `<YYYY-MM-DD-slug>`, `<topic>`, `<seed>`, `<client>` are filled **automatically as the pipeline runs** — they are not setup values. Leave them. The `notion` skill's own template note and each skill body explain the rest.

## Contributing / privacy

This repo is mirrored from a private collection, with owner-specific content removed. A CI check (`.github/workflows/private-scan.yml`) scans every push and **fails if any private data is detected**, so nothing personal leaks on an update.

## License

[MIT](LICENSE) — built by [Matty Reed](https://fractalai.agency). Use it, fork it, ship it.
