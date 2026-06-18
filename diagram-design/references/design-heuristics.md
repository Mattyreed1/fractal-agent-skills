# Diagram design heuristics

How to make a diagram look *designed* and on-brand, not like generic library output or AI slop. These rules drive the `diagram-design` skill. Distilled from the frontend-design skill, applied to node-edge diagrams.

## The core problem

A diagramming library (D2, Mermaid) gives you **auto-layout + a few generic themes**. It does not give you beauty, brand, or judgment. Those are authored. Default library output reads as "a tool made this." The job here is to add the design layer.

## The anti-slop test

If someone saw the diagram and said "AI/tool made this," that's the failure. The 2024–2025 fingerprints to avoid:

- **Glowing neon accents on a dark background** ("cyan-on-dark"). Our brand *is* dark + teal, so we earn it back with **restraint**: teal appears once (the focal point) and as the focal edge, never as a glow on every node.
- **Rainbow color-coding** — five accent colors competing. Color must be rare and meaningful.
- **Every node identical** — same box, same weight, no hierarchy.
- **Decoration without meaning** — gratuitous icons, shadows on everything, textures everywhere.

## The rules

1. **One focal point.** Exactly one node carries the `focal` class (solid accent). It's where the eye lands — usually the key outcome or the core system. Everything else is quiet. If two things are focal, nothing is.
2. **Restraint / hierarchy.** Most nodes use `node` (quiet, tinted-dark, thin border, soft shadow) and recede. Hierarchy comes from *contrast with the quiet majority*, not from making everything loud.
3. **Color = meaning.** Each color encodes one thing: accent = the goal/primary path; amber `gate` = a human decision; neutral = everything else. Same color = same meaning across the whole diagram.
4. **Depth via shadow on the focal ONLY.** Only the `focal` class carries `shadow: true`; quiet nodes stay flat so they recede. Shadows-on-everything reads as slop (and D2's hard offset shadow looks like a doubled box on a dark canvas). Depth is one more signal that points at the focal. Never simulate importance with a neon halo.
5. **Tinted neutrals.** Surfaces are nudged toward the brand hue (dark teal-gray), not pure black — subconscious cohesion. Don't put gray text on a colored fill; use a dark shade of that fill's hue.
6. **Breathing room.** Use `pad: 50` and let the layout space out. A cramped diagram looks cheap. One idea per node.
7. **Short labels.** Node labels 1–4 words. Edge labels 1–2 words (`yes`, `revise`, `context`). Put detail in surrounding prose, not in the diagram.
8. **Axial flow.** Pick one direction (`down` or `right`) and let the spine run straight; branches come off it. Don't make the reader's eye zigzag.
9. **Sharp corners.** Fractal brand = `border-radius: 0` (the default). Do not round. (Founder Freedom uses sketch mode instead.)
10. **Legible labels on dark.** Edge labels render in muted italic; keep them off busy crossings.

## Shape language (consistent meaning)

| Role | Shape | Class |
|------|-------|-------|
| Process / step | rectangle (default) | `node` |
| The one focal point | rectangle | `focal` |
| Service / engine / transform | hexagon | `node` (or `focal` if it's the focus) |
| Data store / memory | cylinder | `data` |
| Decision / human gate | diamond | `gate` |
| Document / artifact | page | `node` |
| External system / actor | cloud / person, dashed | `external` |
| Grouping / boundary | container | `group` |

## Edge craft — apply an edge class, don't hand-color

Edges carry classes too, defined in the brand theme. Prefer these over inline `style.stroke`
so the SAME diagram renders correctly on every brand (on `founder-freedom`, `accent` becomes
amber automatically instead of teal):

| Meaning | Edge class | Fractal renders as |
|---------|-----------|--------------------|
| Normal flow | `flow` | solid, muted `#3a4441`, width 1 |
| Path into the focal node | `accent` | solid, teal `#00c6a2`, width 2 |
| Feedback / retry / kickback loop | `feedback` | dashed, muted amber `#6b5a2f` |
| Data / context / async / cycle | `dataflow` | dashed, muted `#313d3a` |

```d2
a -> b: yes { class: accent }      # the one bright edge — into the focal
b -> a: revise { class: feedback } # dashed amber loop
```

**Highlight the happy path.** `accent` is not only the single edge touching the focal node —
extend it along the *entire* success route so the eye traces "the path that works" end-to-end,
while reject/detour branches stay `flow` (muted). One continuous bright thread, everything else quiet.

`stroke-width` must be an **integer** (D2 constraint), 1–15. Inline `style.*` still works and
overrides the class when you need a true one-off (e.g. a state-machine start dot).

## Before you ship a diagram

- Is there exactly ONE focal point, and does the eye land there first?
- Is every color doing a job? Could you remove one and lose nothing?
- Do quiet nodes actually look quiet (not competing with the focal)?
- Short labels? Straight spine? Room to breathe?
- Would someone say "a tool made this"? If yes, simplify and re-render.
