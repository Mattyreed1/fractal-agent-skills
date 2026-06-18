---
name: diagram-design
description: >
  Render beautiful, brand-styled, external-facing diagrams (flows, architecture,
  KG node-edge graphs) with D2, applying a baked design system: a shape language,
  role-based color-coding, one-focal-point hierarchy, and the Fractal AI / Founder
  Freedom brand canvas. Use for diagrams that go into content, LinkedIn posts,
  decks, or client-facing material where aesthetics matter. Triggers: "beautiful
  diagram", "pretty diagram", "external facing diagram", "diagram for content",
  "architecture diagram for the post", "D2 diagram", "branded diagram", "KG
  visualization", "make this diagram look good", "polished diagram". Outputs
  brand-styled SVG (for embedding into social-canvas / content-visuals frames) or
  standalone PNG. This is the polished/external engine; for fast internal or
  technical diagrams use mermaid-render instead. Not for social-graphic layout
  (social-canvas) or image prompts (visual-gen).
license: MIT
metadata:
  version: 2.0.0
---

# diagram-design

Beautiful node-edge diagrams via D2 + an authored design system. The library gives layout; **the beauty (shape language, color-coding, one focal point, brand canvas) is baked into the brand theme files here** — apply a class to each node and it looks designed.

## Usage

Write the diagram in D2, applying a class to each node, then render:

```bash
scripts/render.sh <input.d2|-> <output.(svg|png)> [--brand fractal|founder-freedom|plain] [extra d2 flags]
```

```bash
scripts/render.sh flow.d2 flow.svg                          # Fractal (default), SVG — best for embedding
scripts/render.sh flow.d2 flow.png --brand founder-freedom  # hand-drawn sketch, PNG
```

**Workflow:** write D2 with classes → render → **Read the PNG** → check against `references/design-heuristics.md` → fix → re-render. Treat it like social-canvas's closed loop.

## The design system — apply a class to every node

| Class | Role | Renders as |
|-------|------|-----------|
| `node` | process / step (the default for most nodes) | quiet tinted-dark box, flat |
| `focal` | **THE one focal point** — key outcome/system. Use **once**. | solid accent (teal), bold, larger, the only shadow |
| `data` | data store / memory | cylinder, quiet |
| `gate` | decision / human gate | diamond, amber accent |
| `external` | system outside the boundary | dashed, muted |
| `group` | a container/boundary (apply to a node with children) | grain texture, subtle border |

```d2
publish: "Publish" { class: focal }
review: "Approve?" { class: gate }
kg: "Knowledge graph" { class: data }
engine: "CONTENT ENGINE" { class: group;  step1: "..." { class: node } }
```

**The #1 rule: exactly ONE `focal` per diagram.** Everything else stays quiet so the eye lands on the focal point. This is what separates a designed diagram from generic library output. Full rules in `references/design-heuristics.md`.

### Edge conventions — apply a class to the edge

Edges carry classes too (defined in the brand theme), so the same diagram is brand-portable —
`accent` is teal on Fractal and amber on Founder Freedom, automatically.

| Class | Meaning |
|-------|---------|
| `flow` | normal flow (muted) |
| `accent` | the path into the focal node — extend it along the whole success path |
| `feedback` | retry / revise / kickback loop (dashed amber) |
| `dataflow` | data / context / async / cycle (dashed muted) |

```d2
review -> publish: yes { class: accent }
review -> script: revise { class: feedback }
```

Inline `style.*` still works and overrides the class for a true one-off. `stroke-width` must be an **integer** (1–15).

## Brands

| `--brand` | Look | For |
|-----------|------|-----|
| `fractal` (default) | Dark `#09090b`, teal `#00c6a2` focal, restrained, sharp | Fractal AI |
| `founder-freedom` | Warm, hand-drawn sketch, amber focal | Founder Freedom / friendly |
| `plain` | D2 default theme | Quick drafts |

Brand styling lives in `themes/<brand>.d2` (class definitions + canvas). Edit those to tune a brand; no script change.

## Output & the two background tiers

| Tier | Output | For |
|------|--------|-----|
| **1 — standalone** | `.svg` (embed) / `.png` (share) straight from `render.sh` | most diagrams |
| **2 — embed** | D2 SVG placed in a `social-canvas` frame (true dotted-grid + glass) | hero / marquee pieces |

D2 can't paint the full Fractal dotted-grid+glass canvas — that's HTML/CSS. For pixel-perfect brand, use Tier 2: see `references/social-canvas-embed.md`.

## Diagram types

Flowchart, architecture, sequence, KG/graph, decision tree, swimlane, timeline/state — when to use each and how to make it look great: `references/diagram-types.md`.

## References

- [design-heuristics.md](references/design-heuristics.md) — the rules (one focal point, restraint, color=meaning, anti-slop)
- [diagram-types.md](references/diagram-types.md) — per-type recipes
- [examples/](references/examples/) — **a worked `.d2` + rendered `.png` for all 7 types.** Copy the nearest one and adapt; it already has the classes, layout engine, and conventions baked in.
- [social-canvas-embed.md](references/social-canvas-embed.md) — Tier 2 embedding

## When NOT to use this

| Need | Skill |
|------|-------|
| Fast internal/technical diagram from Mermaid | **mermaid-render** |
| Social-graphic layout / carousel / infographic frame | **social-canvas** |
| Image / video generation prompts | **visual-gen** |

## Runtime note — local vs the agent fleet

- **Claude Code / Mac (EA):** D2 installed (`brew install d2`); works directly.
- **the agent runtime / the agent fleet:** D2 must be installed on the VPS first, and this skill synced via `skill-translate` + your deployment tooling. Verify with `which d2`. Until then, agents on the VPS fall back to HTML/CSS.

## Brand font

The fractal brand renders in **Geist** (matches social-canvas) — the TTFs are vendored in
`assets/fonts/` (Geist Regular/Bold/Italic/SemiBold + Geist Mono Regular/Bold, OFL-licensed,
v1.7.2). `render.sh` wires them automatically for `--brand fractal` and embeds them in the SVG,
so output is self-contained. If a face is missing, D2 falls back to its default for that face.
Founder Freedom and plain use D2's default font.
