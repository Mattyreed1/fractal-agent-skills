# Tier 2 — embed a D2 diagram in a social-canvas frame

D2 renders the **diagram** beautifully (auto-layout, brand classes, depth). It cannot paint the full Fractal *canvas* — the dotted-grid background + glass surfaces are an HTML/CSS capability. For hero / marquee external pieces, embed the D2 **SVG** inside a `social-canvas` slide so the diagram sits on the real brand canvas.

## When to use which tier

| Tier | Output | Use for |
|------|--------|---------|
| **1 — D2 standalone** | PNG/SVG straight from `render.sh` (tinted-dark canvas, grain on containers) | Most diagrams: drafts, internal, quick social, decks |
| **2 — embed in social-canvas** | D2 SVG placed in an HTML slide (true dotted grid + glass + logo/eyebrow) | Hero pieces, carousels, anything that must match social-canvas pixel-for-pixel |

## Tier 2 steps

1. **Render the diagram as SVG with a transparent background** so the slide's grid shows through:
   ```bash
   ~/.claude/skills/diagram-design/scripts/render.sh flow.d2 /tmp/flow.svg --brand fractal --pad 0
   ```
   Then strip/blank the SVG's outer background rect if present (D2 may emit a solid bg rect — delete it or set `fill="none"`), so only the nodes/edges remain over the canvas.
2. **Drop the SVG into the slide's data-viz zone** in social-canvas (Phase 2). Treat it like any embedded asset: place it in the content block, size it to the safe zone, let the slide supply the dotted grid, eyebrow, title, logo, and footer.
3. **Match palettes.** The fractal D2 classes already use the social-canvas tokens (`#09090b`, teal `#00c6a2`), so the diagram and the frame read as one piece. Keep the diagram's focal accent = the slide's accent.
4. **Run social-canvas Phase 4** (read the PNG, evaluate, fix) on the combined slide — the diagram is now just one element competing for the slide's single focal point, so quiet the diagram's internal accent if the slide has its own hero.

## Gotchas

- Don't double up focal points: if the slide has a hero headline, the embedded diagram should be all-quiet (no `focal` node) or the focal should BE the diagram.
- Keep the SVG vector (don't rasterise to PNG before embedding) so it stays crisp at the slide's resolution.
- On the agent runtime, D2 must be installed on the VPS first (see SKILL.md runtime note) before content-visuals/social-canvas can do Tier 2 there.
