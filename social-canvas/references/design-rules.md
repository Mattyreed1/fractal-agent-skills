# Design Rules — Hard Constraints

These are non-negotiable rules learned from real production iterations. Every rule here exists because it was violated and caught. Claude MUST check every rule before generating HTML.

---

## Contents

- Brand Enforcement
- Sizing — Locked Values
- Layout
- Layout Rules of Thumb — Filling Space & Spacing Between Containers
- Color Usage
- Carousel Consistency
- Workflow Rules
- Anti-AI-Slop
- the user's Visual Preferences (Learned from Production)
- 2026-06-03 Corrections (the user review — these SUPERSEDE earlier rules where noted)

## Brand Enforcement

1. **Background is `#09090b` + dotted grid texture.** Not `#0a0a1a`, not `#12122a`, not `#1e1e3a`. The body ALWAYS overlays a 2×2 px white square at 9% opacity on a 24 px grid (see `templates/base-vars.css` body rule). Do not render slides with a solid flat `--bg` — the grid texture is part of the brand. **The canvas ALSO carries a 1px hairline edge border (`border: 1px solid rgba(255,255,255,0.14)` on `body`, inside via `box-sizing: border-box`) so the near-black image reads as a distinct rectangle. Without it the image edges vanish into any dark background — LinkedIn dark mode, a black slide deck, the preview gallery — and the viewer cannot tell where the image starts and stops (the user 2026-06-17). Every slide gets this edge.**
2. **Text is `#fafafa`.** Not `#e0e0e0`, not `#ccc`. Near-white.
3. **Surfaces are glass, not opaque.** Cards, panels, columns, badges, image frames, code blocks — ALL container surfaces use the glass treatment: `background: rgba(17,17,19,0.55)` + `backdrop-filter: blur(18px)` + `border: 1px solid rgba(255,255,255,0.12)`. Use `var(--glass-bg)` / `var(--glass-blur)` / `var(--glass-border)` or the `.glass` / `.card` / `.panel` classes. Opaque `--surface` (#111113) is reserved for full-bleed backgrounds only. Confirmed 2026-04-22.
4. **Fonts are Geist Sans (headlines + body) / Geist Mono (labels, code, terminal) / Silkscreen (eyebrows only).** No exceptions. No Inter, Roboto, Arial, system fonts. (Outfit / Instrument Sans / JetBrains Mono retired 2026-04-23 — see rule 81.)
5. **Fractal AI logo in bottom-left of every slide.** Use `logo.png` (relative path in HTML served by preview). For Playwright rendering, copy the logo to `/tmp/social-canvas/logo.png`.
6. **NEVER use a text handle** like `@mattyfreed` or `@username`. The brand is represented by the logo only.

---

## Sizing — Locked Values

7. **Eyebrows and all small-cap labels default to `--text-muted` (#71717a)** — UPDATED AGAIN 2026-04-23 after the user caught color redundancy: an emerald eyebrow stacked on an emerald hero highlight weakens both elements. The stronger accent element wins; smaller adjacent labels yield to muted grey. Only elevate eyebrow to `--accent-emerald` on slides with zero other accent elements within 200px (rare). NEVER use `--text-dim` (#3f3f46) on any label meant to be read — it fails contrast on `#09090b` and disappears. `--text-dim` is reserved for decorative strikethroughs, separators, and inactive states.
8. **Block labels are 36px MonoBold.** Centered in the block. Letter-spacing 5px. Uppercase.
9. **Headlines are 56-64px Geist Sans (bold weights).** Never smaller than 56px for content slides, 64px for hook slides.
10. **Body/description text is 26-30px Geist Sans.** Never smaller than 26px.
11. **Code/terminal text is 24px Geist Mono.** Never smaller than 20px.
12. **Logo is 44px height, 1.0 opacity.** Bottom-left, every slide. Pulled from `logo_render` in `brand-config.json` (this skill's directory).
13. **Bottom-right corner is the website (`fractalai.agency`), never a slide number.** Use `.bottom-note` class, 14-22px Geist Mono, `--text-muted`. `.slide-num` / `{{SLIDE_NUM}}` is retired.

---

## Layout

14. **Safe zone padding: 64px top/sides, 28px bottom.** Reduced bottom padding lets the logo + website note sit in the lower margin (confirmed 2026-04-23). `.canvas { padding: 64px 64px 28px; }`. Never approach the top/side edges; the reduced bottom is intentional.
15. **Flex column layout.** Never absolute positioning for text content.
16. **Left-aligned text by default.** Center-aligned ONLY for CTA/closing slides.
17. **One idea per slide.** If content doesn't fit, the content is too much — cut it.
18. **`justify-content: space-between`** on the canvas flex container distributes content top-to-bottom with the footer at the bottom.

---

## Layout Rules of Thumb — Filling Space & Spacing Between Containers

**READ THIS SECTION EVERY TIME YOU BUILD A SLIDE.** Dead space and cramped layouts are the two most common regressions. These numbers are calibrated for 1080×1080 slides with 64/28px canvas padding (952×988 content area).

### Header Group Rule — eyebrow + headline + subtitle are ONE tight block

**Subtitles sit immediately under titles. Never let Pattern B distribute slack between them.** the user caught this 2026-04-23: the debate slide had Pattern B spreading the headline-to-sub gap across ~400px, orphaning the subtitle. A subtitle that floats alone is information rot — it's supposed to extend the title, not restate it from across the room.

Structure:
```html
<div class="eyebrow">...</div>
<div class="header">        <!-- tight group, internal gap 16-20px -->
  <h1>Headline</h1>
  <p class="sub">One-line subtitle.</p>
</div>
<div class="data-viz">...</div>   <!-- charts, I/O cards, timeline, diagram -->
<div class="takeaway">...</div>   <!-- optional callout -->
```

`.header { display: flex; flex-direction: column; gap: 18px; }` — tight internal spacing.

Then `.main { justify-content: space-between; }` distributes the LEFTOVER slack between `.header`, `.data-viz`, and `.takeaway` — NOT inside the header group.

**Fill the rest of the space with useful content.** Below the header group belongs: charts, graphs, data viz, diagrams, code blocks, terminals, card grids, flow/process maps, numbered lists, quote cards, I/O pairs, callouts. Never leave vertical rows of pure negative space — the canvas area below the header should carry a visual element that extends the headline's argument.

### The Three-Zone Canvas Pattern (MANDATORY for every slide)

```html
<div class="canvas">          <!-- flex column, justify-content: space-between -->
  <div class="eyebrow">...</div>   <!-- zone 1: natural height, top-anchored -->
  <div class="main">...</div>      <!-- zone 2: flex: 1, fills remaining space -->
  <div class="bottom">...</div>    <!-- zone 3: natural height, bottom-anchored -->
</div>
```

- The canvas is `display: flex; flex-direction: column; justify-content: space-between;`.
- **Zone 1 (eyebrow/header)** — natural height. Sits flush with the top safe-zone.
- **Zone 2 (`.main`)** — ALWAYS `flex: 1` so it claims every remaining pixel. This is the single most important rule for avoiding dead space.
- **Zone 3 (bottom bar)** — natural height. Sits flush with the lower margin.

If `.main` isn't set to `flex: 1`, content bunches at the top and you get a gap above the bottom bar. Catch this every time.

### Filling Zone 2 — Three Patterns

Pick ONE based on content type:

**Pattern A: Top-loaded content with takeaway-to-bottom.** Use when the main content is short (headline + sub + small visual) and a callout should anchor the bottom of zone 2:
```css
.main { display: flex; flex-direction: column; gap: 20px; flex: 1; }
.takeaway { margin-top: auto; }   /* pushes callout to the bottom of .main */
```

**Pattern B: Evenly-distributed rows.** Use when you have 3–7 stacked items (timeline steps, pills, feature cards) that should divide the vertical space equally:
```css
.main { flex: 1; display: flex; flex-direction: column; }
.inner { width: 100%; height: 100%; display: flex; flex-direction: column; justify-content: space-between; }
```
`justify-content: space-between` on a column flex container with `height: 100%` spreads children evenly top-to-bottom. This is how slide-1's timeline fills the canvas.

**Pattern C: Centered block.** Use for CTA/closing slides where content should vertically center in zone 2:
```css
.main { flex: 1; display: flex; flex-direction: column; justify-content: center; align-items: center; }
```

**Rule of thumb:** If your slide has visible dead space at the bottom (above the logo), you forgot `flex: 1` on `.main`, `margin-top: auto` on the last element, OR `justify-content: space-between` on the inner container. One of these three always fixes it.

### Spacing Rules of Thumb (px values)

All spacing uses the 4/8px grid. Never use odd numbers like 5, 7, 13, 17.

| Relationship | Gap | Notes |
|--------------|-----|-------|
| Eyebrow → headline | **16–24px** (use `margin-top: 16px` on `.main`) | Tight group — eyebrow belongs to the headline |
| Headline → subtitle | **12–20px** | Part of the same thought |
| Headline → subtitle (when weighted by size) | Use `gap` on parent, typically 16px | Flex-column with gap is cleaner than margins |
| Subtitle → body content (I/O card, chart, list) | **24–32px** | Clear handoff from header block to evidence |
| Body content → takeaway callout | **auto** (push to bottom) OR **24–32px** | Depends on pattern A vs B |
| Between stacked cards/rows in a timeline | **14–22px** | Close enough to read as a group, far enough to breathe |
| Between major sections (header, data viz, callout) | **28–40px** | Larger than intra-section gaps |
| Inside a card/container (padding) | **22–32px** (small), **32–40px** (large/hero) | Never less than 16px padding; cramped cards are an instant regression |
| Between grid/flex columns | **20–32px** | Match vertical gaps for visual balance |

### Container Rules of Thumb

- **Stacked cards need `min-height`** when they hold varied content lengths. Typical: 180–220px. Without it, rows collapse to content height and the stack feels lopsided.
- **Equal-weight row grids should use `flex: 1` per child** inside a flex-column parent with `height: 100%` — all rows stretch to fill the space proportionally.
- **`.glass` surface is the default container background** (see rule 3). Border is 1px `--glass-border`. Radius is 0 (rule 82).
- **Inside a glass card, inner gap is 10–14px** between stacked elements. Tighter than between-card gaps because the card itself provides breathing room.
- **Two-column card grids**: columns should be equal width (`grid-template-columns: 1fr 1fr`) with a gap of 20–28px. Match this to the outer content width so the cards feel anchored.
- **Input/Output or before/after pairs**: stack VERTICALLY (the user confirmed 2026-04-23) — one card full-width, then the next. Two-up side-by-side compresses labels and text, feels cramped at 1080×1080. 16px gap between stacked cards.

### Avoiding Cramped Layouts

- **Vertical rhythm check**: squint at the slide. You should see 3–4 clear horizontal bands (header, mid-content, takeaway, footer). If bands blur together, add 8–12px to the gap between them.
- **When adding a new element, check total vertical content height.** Canvas content area is 988px tall (1080 − 64 − 28). If header+body+takeaway+footer > 988, something has to shrink (font-size, padding, or cut content). Don't silently crop.
- **`min-height: 0` on flex children** that might overflow — lets them shrink rather than push siblings off-canvas.

### Avoiding Dead Space

- **The footer should touch the bottom safe-zone (28px).** If you see a gap between your last content element and the footer, `flex: 1` is missing somewhere.
- **`justify-content: space-between` on any flex container** with 3+ children will evenly distribute them. Use this when you want even vertical rhythm without hand-tuning margins.
- **`margin-top: auto` on the last element** of a flex-column container pushes that element to the bottom regardless of sibling count — great for takeaway callouts that should anchor the bottom.

### Quick Audit Checklist (run before calling a slide done)

1. Is `.main` set to `flex: 1`? (If no → add it.)
2. Does the bottom bar touch the bottom margin? (If there's a gap → use pattern A/B/C above.)
3. Are gaps between stacked cards in the 14–22px range? (If tighter → cramped; if wider → feels disconnected.)
4. Is padding inside glass cards 22–32px? (If 16px or less → cramped.)
5. Does the squint-test show clear horizontal bands? (If blurred → increase section gaps.)
6. Does content fit without overflow? (Check for `overflow: hidden` cropping.)

---

## Color Usage

19. **ONE accent color per piece, max.** Pick one color from the accent palette (emerald, blue, amber, pink) and use it for ONE semantic meaning throughout the entire piece. Same color = same meaning everywhere. If you can't state the color's meaning in one sentence, use no color.
20. **Color appears in small doses only.** Acceptable: a keyword, a thin border (1-4px), a number, a small indicator bar, a tight highlight behind a single hero word (see rule 80). NOT acceptable: large background fills, full-width colored blocks, colored section headers. The piece must still read as monochromatic overall.

82. **Every box, card, container, panel, pill, terminal, and button has SHARP corners — `border-radius: 0`.** This applies universally to slide-content surfaces AND gallery chrome (already confirmed for gallery cards 2026-04-23, extended to slide content 2026-04-23). The only exceptions: (a) circular dots and status indicators (`border-radius: 50%`), (b) the bottom-bar logo image if the logo asset itself has organic edges. `--block-radius` and `--card-radius` are both locked to `0` in base-vars.css. Do NOT use 4/8/12/14/16/999px — any rounded corner is a regression.

83. **No redundant labels OR redundant color — one piece of information, one representation.** If a fact is communicated once on a slide (stage number, skill name, section kind, a stat, a category), do NOT repeat it in a second element. the user caught "STAGE 02 · VERIFY" eyebrow + giant "02 of 07 stages" subheader both saying "02" on the same slide 2026-04-23 — the eyebrow already carries the stage number AND the kind, so the large "02" decorator was pure redundancy. Pick the strongest single representation and delete the others.

   Common label redundancies to avoid: (a) same word appearing in headline AND subhead, (b) same stat shown in chart label AND callout, (c) skill name in both eyebrow AND card header, (d) date shown in timestamp AND body copy, (e) metric name shown next to its value AND in a legend.

   **Color redundancy (extension, locked 2026-04-23):** the same rule applies to accent color, not just text. If the accent already appears in a strong hero element on the slide (highlight block, accent-bordered card, colored keyword), do NOT ALSO use the accent on an adjacent small element (eyebrow, label, sidebar pill). the user caught emerald eyebrow "STAGE 05 · MULTI-AGENT DEBATE" stacked directly above an emerald-background "debate" highlight 2026-04-23 — two green elements inches apart weaken each other. **The stronger element wins; the smaller one goes muted.** Default eyebrow color is therefore `--text-muted` (#71717a), not accent. Elevate the eyebrow to accent ONLY on slides with NO other accent-colored element within 200px of it (rare). When in doubt: if a viewer sees two adjacent green things at the same moment, one has to go grey.

   Rule of thumb for both labels and color: cover the page with your hand except for one element. If removing every OTHER element still leaves the viewer informed of that fact (or sees the accent), the fact is covered — anywhere else it appears is redundant decoration.

80. **Hero highlight pattern — background color beats colored text.** When one key phrase on a hook slide needs to pop (e.g. a product name), apply the accent as a BACKGROUND behind the word (`background: var(--accent-emerald); color: var(--bg);` with `padding: 6px 18px 10px; display: inline-block; box-decoration-break: clone;`) — NOT as text color. the user confirmed 2026-04-23: a solid highlight behind white/dark text reads stronger and more intentional than colored text on dark bg. Use this for the single hero moment only; everything else stays monochromatic.

81. **Headline type is Geist Sans throughout — NEVER mix mono into a sans headline.** the user rejected the mono-for-product-name pattern 2026-04-23. The hero highlight (rule 80) uses Geist Sans at the same size and weight as the surrounding headline; only the `background` and `color` change. Mono reads as a typographic foreign object next to sans at hero sizes — it looks thinner, wider, and off-beat. Reserve Geist Mono for labels, code, terminal lines, and website notes — never headline text. Silkscreen is the only non-sans family allowed inside headline-level content, and only as an 14px eyebrow above the headline, never inside it.
21. **Never use the same color for two different meanings.** If amber = "warning" in one section, it cannot also mean "section label" in another. This is the #1 color mistake — it makes the piece feel disorienting rather than structured.
22. **No gradients. No shadows. No patterns.** Flat, monochromatic, engineering-precision aesthetic.
23. **Emojis go on dark backgrounds only.** Never place an emoji on a colored background.

---

## Carousel Consistency

24. **Same `:root` CSS variables on every slide.** Copy-paste the identical `:root` block.
25. **Same `@font-face` declarations on every slide.** Copy-paste all 5 font-face blocks.
26. **Same bottom bar layout on every slide.** Logo left, slide number right.
27. **Same typography scale across all slides.** Don't use 56px headlines on one slide and 44px on another for the same element type.

---

## Workflow Rules

28. **NEVER re-render PNGs without explicit user permission.** If the user is editing in the preview, their changes are sacred. Only re-render when they say "render the finals" or similar.
29. **Copy logo to `/tmp/social-canvas/` at start of every session.** The preview server serves from `/tmp/social-canvas/`, so logos need to be there with relative paths.
30. **Preview gallery uses iframes, not PNGs.** This enables direct text editing. PNGs are only for final export.
31. **Max 3 evaluation rounds per slide.** Diminishing returns after that.
32. **NEVER edit the HTML file while the user may have unsaved preview edits.** If you need to make a CSS/structural change, ask the user to "Save Edits" in the preview first, THEN read the current file (which includes their edits) and make only the targeted change. Overwriting user text edits is the #1 trust-breaker.

---

## Anti-AI-Slop

33. **No cookie-cutter layouts.** Every carousel should have varied slide layouts (hook, content, terminal, flow, CTA).
34. **No decorative circles, blobs, or abstract shapes** unless they directly represent a concept.
35. **No purple gradients.** Ever.
36. **No "pretty" — aim for "precise."** A technical founder should think "this person knows their stuff."
37. **No filler text.** Every word on the slide must earn its place.

---

## the user's Visual Preferences (Learned from Production)

These are the user's personal design preferences, learned from real feedback sessions.

### Process
38. **Discuss concept and layout before building.** Don't jump straight to code. Talk through the design direction, get alignment, then build.
39. **If a visual element needs explanation, it's not working.** Every element should communicate its meaning instantly. If you have to describe what it represents, redesign it (e.g., a "4.9/8KB buffer gauge" is unclear — a "sleep cycle" bar chart is immediate).

### Iconography & Imagery
40. **Literal over abstract.** Use recognizable imagery, not abstract representations. A brain icon should look like a brain — not concentric rings that symbolize a brain.
41. **Labels beside icons, not above.** Horizontal text to the left/right of an icon lets the icon be larger. Use stacked two-line labels (e.g., "HUMAN\nBRAIN") right-aligned left of the icon, or left-aligned right of the icon.

### Layout & Structure
42. **Separate stacks over unified containers.** Three distinct bordered cards read better than one merged block, even when they're conceptually connected. Use connecting elements (vertical lines, flow labels) between them.
43. **Breathing room between sections.** Cramped flow connectors between stacked sections hurt readability. More padding makes it feel like a cohesive diagram, not a cramped list. Use pill-shaped flow labels on a vertical connector line.
44. **Fill dead space purposefully.** Empty space next to content needs a visual that earns its place — not filler. The visual should reinforce the section's core concept (e.g., a sleep cycle chart next to the weekly memory buffer).
45. **Thin divider lines under section headers.** A 1px border-bottom on layer headers clarifies the hierarchy between the section label and its content.

### Color
46. **Accent color on data visualizations: one focal node only.** A touch of emerald on the central/primary node in a KG visualization works. Don't color secondary nodes — it dilutes the focal point.

### Paths & Flow Lines (Learned 2026-04-06)
47. **Paths are the visual hero, not decoration.** When a design uses a flowing path/timeline, it should be prominent — multi-layer glow (ambient 48px + medium 20px + core 3px + bright 2px), not a thin 2px line that blends into the background.
48. **Paths must connect meaningfully to content.** Enter each card from the SIDE, exit from the BOTTOM. The path should feel like it's threading through the content, not floating behind it. Each card should sit at a curve point.
49. **Path origin matters.** Start the path from a meaningful anchor — e.g., directly under a key word in the headline, not from an arbitrary center point. Mark the origin with a small emerald circle (r=6, opacity 0.7).
50. **Graceful curves, not flat diagonals.** When the path transitions between cards, the bezier control points must create visible J-curves or hooks. Flat transitions between cards look like diagonal lines, not flowing paths. Bow control points outward to create visible arcs.
51. **Path starts vertical, then curves.** When dropping from a headline to content, the path should begin with a short vertical segment before curving — this looks intentional, not just a diagonal line from point A to B.

### Cards & Containers (Learned 2026-04-06)
52. **Glassmorphism over solid surface.** Semi-transparent cards (`rgba(17,17,19,0.6)` + `backdrop-filter: blur(16px)`) with subtle borders (`rgba(255,255,255,0.12)`) look better than solid `#111113` containers. The path glow shows through them, adding depth.
53. **Filled phase numbers over outlined.** Solid emerald circles with dark text (`background: var(--accent); color: var(--bg)`) are more readable and impactful than hollow outlined circles.
54. **Phase time labels in accent color.** Small mono text showing the timeline (DAY 1, WEEKS 2-3) works well in emerald — it's a consistent secondary marker that reinforces the phase progression.

### Positioning Precision (Learned 2026-04-06)
55. **Never claim positioning is correct without rendering and visually verifying.** SVG coordinates are imprecise at thumbnail scale. Render, read the PNG, confirm the position. Getting caught lying about placement destroys trust.
56. **"Under X" means directly below those specific words**, not below the center of the line. Calculate the actual horizontal position of the referenced text.
57. **Small adjustments are incremental.** When the user says "shift by 1cm", that's ~38px at 1x resolution. Apply the exact offset to all Y (or X) coordinates in the path.

### Logo Placement
58. **Logo goes where it balances the composition**, not always bottom-left. If content is weighted to the left (e.g., final card on the left), put the logo bottom-right to balance.

### Brand Compliance — Read The Style Guide FIRST (Learned 2026-04-11)
63. **Read `fractal-ai-visual-style.md` BEFORE generating any HTML.** The style guide has specific sizing minimums (logo 48px+, slide numbers 20px+, opacity 0.85+) that differ from the template defaults. Skipping this step produces output that looks "off brand" and requires a full rewrite. This was the #1 time-waster in the 2026-04-11 session.
64. **Never use template default sizes for logo/footer.** The templates use 28px/0.7 opacity as placeholders. The actual brand minimums are 48px height, 0.85 opacity (recommended: 56px, 0.9). Always override.

### Color System — Two Accents Allowed With Clear Semantics (Learned 2026-04-11)
65. **Red (`#ef4444`) is an available accent for danger/cost/negative.** Add `--accent-red: #ef4444;` to `:root` when needed. Best for: cost increases, warnings, negative outcomes. Pairs well with emerald (positive vs negative).
66. **Two accent colors are acceptable when they represent a clear binary.** Emerald (good/affordable) + Red (bad/expensive) is a valid pairing because the meaning is instantly obvious. This overrides the "one accent per piece" default when the semantic system is a clear binary contrast.
67. **Glowing red for emphasis.** Use `box-shadow: 0 0 24px rgba(239,68,68,0.12), inset 0 0 24px rgba(239,68,68,0.06)` on bars and `text-shadow: 0 0 40px rgba(239,68,68,0.3), 0 0 80px rgba(239,68,68,0.1)` on text. Flat fill only (`rgba(239,68,68,0.1)`), no gradients.

### Layout — Group Header Elements (Learned 2026-04-11)
68. **Eyebrow + headline + subtitle should be wrapped in a `.header` container with 16px internal gap.** The main content gap (40-48px) is too large between the eyebrow label and headline. Group them tightly, then let the larger gap separate the header block from the body content (chart, cards, etc.).
69. **The hero stat/callout goes BELOW the chart, not between chart rows.** When the infographic has a "punchline" number (e.g., 10x), it reads better as a conclusion under the data than as a divider within it. The chart presents the evidence; the callout delivers the verdict.

### Eyebrow Labels (Learned 2026-04-11)
70. **Eyebrow text must be specific to the story, not generic category labels.** "Agent Infrastructure Cost" is a category. "Anthropic's Token Shutdown" is a story. The eyebrow should frame the specific event or context — it's the "why should I care" primer before the headline lands. Generic labels like "AI Agent Ops" or "The Real Cost of AI Agents" feel like template filler.

### Canvas Space Management (CRITICAL — Learned 2026-04-15)
71. **NEVER leave awkward empty space on a slide.** If content only fills 60% of the canvas, increase element sizes, add `flex: 1` to containers, or use `justify-content: space-between` on the main flex container. Dead space = lazy design. Every slide should feel balanced and full.
72. **Use `flex: 1` on repeating elements to fill vertical space.** Layer blocks, list items, and card grids should grow to fill available height. Set `flex: 1` on both the parent grid and child items, with `padding: 0 28px` so the block stretches but content stays centered.
73. **`justify-content: space-between` is the default for `.main` containers.** This distributes headline, content, and footer/callout evenly. Never rely on fixed gaps alone — let flex handle distribution.
74. **`margin-top: auto` pushes a final element to the bottom.** Use for callout boxes and footer notes to fill remaining space naturally.

### Accent Color — Structural Only (Learned 2026-04-15)
75. **NEVER use accent color on inline text within body copy.** Don't highlight words like "ship 6 deliverables" or "2.3M" in emerald. Body text stays monochrome (white/muted). Accent color is reserved for structural elements: numbers in lists, border indicators, icon badges, and pill outlines.
76. **Equal treatment for equivalent items.** If showing 4 layers/skills/steps on a hook slide, highlight ALL of them the same way (all emerald numbers, all white text). Don't dim some to create artificial hierarchy when the point is that all are equally important.

### Callout Pattern (Learned 2026-04-15)
77. **Use lightbulb callout containers for takeaway notes.** Instead of a left-border accent bar, use a surface container with a 💡 emoji (36-40px) + body text (26-28px, text-muted). Class pattern: `.callout` (flex, gap 20px, surface bg, border, rounded) + `.callout-icon` + `.callout-text` (contenteditable). This is now the standard pattern for insight/verdict/takeaway text.

### Editability (CRITICAL — Learned 2026-04-15, extended 2026-05-10, hardened 2026-05-10)
78. **ALL text elements must be clickable-and-editable in the gallery preview — including every label inside an SVG diagram.** If the user can see it, they must be able to click and edit it. Missing editability on any text element is a bug.

   **HARD RULE: never use plain SVG `<text>` for any text in a diagram.** Even with `contenteditable="true"` on the element, click-to-position-cursor on SVG `<text>` is unreliable in Chromium — the attribute reports `isContentEditable: true` but the user cannot reliably click and type. the user hit this 2026-05-10 on the "Separate agent · clean ctx" label.

   **Use `<foreignObject>` containing a contenteditable HTML `<div>` for EVERY text label in an SVG diagram.** This is the canonical SVG+HTML interop pattern and works reliably across Chromium, WebKit, and Gecko. Template:
   ```svg
   <foreignObject x="${cx - half_width}" y="${cy - 0.8 * font_size}" width="${full_width}" height="${font_size * 1.4}">
     <div xmlns="http://www.w3.org/1999/xhtml" contenteditable="true"
          style="font-family:'Geist',sans-serif;font-size:20px;font-weight:600;color:#fafafa;text-align:center;line-height:1;outline:none;">TEXT</div>
   </foreignObject>
   ```
   The `xmlns="http://www.w3.org/1999/xhtml"` is required so the inner element is parsed as HTML, not SVG. `outline:none` removes the focus ring once editing starts. The `0.8 * font_size` y-offset converts SVG baseline-anchored y to HTML top-anchored y.

   For HTML descendants of a `contenteditable="true"` parent (eyebrow div, headline h1, subtitle p, punchline divs, etc.), inheritance works fine — no per-child attribute needed.

   **MANDATORY PRE-RENDER CHECK** — run this before every `render.py` invocation:
   ```bash
   grep -n '<text ' /tmp/social-canvas/slide-*.html
   ```
   The expected output is **empty**. ANY match means a plain SVG `<text>` exists — convert it to `<foreignObject>` before rendering. This is a hard gate; do not export a static visual until it passes. (Note: the earlier weaker check `grep -v 'contenteditable'` is no longer sufficient — `contenteditable` on SVG text passes the grep but still fails for the user.)

   **ALSO MANDATORY: the editable-text gate (HTML text, not just SVG).** `grep` cannot tell which HTML text nodes are editable, so run `python3 scripts/check-editable.py /tmp/social-canvas` before every render AND before declaring the preview ready. It parses each slide and FAILs if any visible text node lacks a `contenteditable` ancestor. Spot-checking one element is NOT enough: a non-editable `.band-label` ("Replaceable · swap anytime") and `.bottom-note` shipped 2026-06-17 because only the headline's editability was verified. EVERY text-bearing element (band labels, footer note, diagram labels, captions, eyebrows) must carry `contenteditable="plaintext-only"` or sit inside an element that does. The gate must return exit 0; if it FAILs, add the attribute to each listed node and re-run.

   **CLICK-FOCUS HELPER (REQUIRED in every slide HTML).** Even with foreignObject + contenteditable correct, Chromium can fail to route focus on real `mousedown` when the slide is hosted in a `transform: scale`'d iframe (the gallery preview). Symptom: `isContentEditable: true` and `elementFromPoint` returns the div, but real user clicks don't focus it. the user hit this 2026-05-10 on the "Separate agent · clean ctx" label after foreignObject conversion.

   Every slide HTML must include this script (place at end of body):
   ```html
   <script>
   (function () {
     function focusEditableAncestor(target) {
       var n = target;
       while (n && n !== document.body) {
         if (n.isContentEditable) { n.focus(); return; }
         n = n.parentElement;
       }
     }
     document.addEventListener('mousedown', function (e) { focusEditableAncestor(e.target); }, true);
     document.addEventListener('pointerdown', function (e) { focusEditableAncestor(e.target); }, true);
   })();
   </script>
   ```
   Pre-render check (second gate):
   ```bash
   for f in /tmp/social-canvas/slide-*.html; do
     grep -q 'focusEditableAncestor' "$f" || echo "MISSING focus helper: $f"
   done
   ```
   Expected output: empty.

### Minimum Readable Font Sizes (Learned 2026-04-24, accessibility-hardened 2026-05-10)
80. **Minimum font sizes for 1080×1080 carousel slides.** Carousels are viewed thumb-sized in the LinkedIn feed. Anything below these floors becomes unreadable. NEVER shrink below these to fit content — restructure (fewer cards, bigger grid cells, less text) instead.
    - **Body / data values** (the actual content of a card — metric, description, sample text): **≥ 16px**, prefer 17–20px
    - **Eyebrow labels** (WEEK / OPTIONS UNDER DEBATE / R1 · OPENING / 01 · CONSTRAINTS): **≥ 13px** Silkscreen or Geist Mono
    - **Footnotes / secondary captions** (flip conditions, source notes, helper text): **≥ 18px** when on `--text-muted` (#71717a) — below 18px on muted grey fails WCAG AA contrast (4.5:1 required for normal text; #71717a on #09090b is ~4:1, just under). At 18px+ regular OR 14px+ bold, the text qualifies as WCAG "large text" (3:1 minimum) which `--text-muted` meets comfortably.
    - **Process-label section header**: 14px Silkscreen with 0.22em letter-spacing
    - **Anything ≤ 12px is forbidden** in carousel slides except the dotted-grid background pattern.

   **WCAG AA contrast — color × size matrix on the `#09090b` background:**
   | Color | Hex | Contrast | Min font for AA |
   |-------|-----|---------:|----------------:|
   | `--text` | #fafafa | 18.6:1 | any |
   | `--text-muted` | #71717a | 4.0:1 | 18px (large-text) OR ≥ 22px any weight |
   | `--text-dim` | #3f3f46 | 1.7:1 | **never use for readable text** |
   | zinc-400 | #a1a1aa | 6.4:1 | any (AA pass for normal text) |

   When a card has 3 stacked text rows (eyebrow + headline + footnote), use 14 / 18 / 14 minimum. If padding can't fit those sizes, the card is too small — drop one of the text rows or merge cards. Captions that must stay quiet but readable: use `#a1a1aa` (zinc-400, 6.4:1) at 18–20px instead of trying to squeeze contrast out of `--text-muted` at 14px.

### Font Loading (Learned 2026-04-15)
79. **When a font is already installed on the user's machine, use `local()` in @font-face.** Example: `@font-face { font-family: 'Display'; src: local('Chango'), local('Chango-Regular'); }`. This avoids downloading fonts and works reliably in both browser preview and Playwright render.

### Preview Save System — Claude Code only (NOT applicable on the agent runtime)
Rules 59-61 below describe the interactive preview-gallery save flow that runs on the Claude Code runtime (`preview_*` MCP tools, in-browser editable iframes). the agent runtime has none of those tools — the closed-loop evaluation in Phase 4 of SKILL.md is the only quality gate. These rules are kept here for parity with the Claude Code skill, not for execution on the agent runtime.

59. **(Claude Code only)** Test the save function BEFORE telling the user the preview is ready. After writing index.html, click Save Edits yourself via preview_eval or preview_click and verify the server logs show a successful POST.
60. **(Claude Code only)** NEVER reload the iframe or page when the user may have unsaved edits. Fix index.html on disk, inject the fix into the live DOM via preview_eval, ask the user to re-save. Reloading destroys their in-browser edits.
61. **(Claude Code only)** Verify saves by reading the file on disk after each save test. "Save succeeded" from the server means nothing if the file content is wrong.
62. **Playwright renders fonts slightly differently than a regular browser.** On both runtimes: after every render, read the PNG and compare text wrapping against the live preview (or against the prior render on the agent runtime). If any text wraps differently, widen the container by 20px and re-render.

---

## 2026-06-03 Corrections (the user review — these SUPERSEDE earlier rules where noted)

Every rule below exists because the 2026-06-03 "Org Singularity" pass shipped it wrong and the user caught it. They are HARD GATES — verify each before declaring any slide done.

84. **EYEBROW DEFAULTS TO THE BRAND ACCENT (teal `#00c6a2`), NOT muted.** SUPERSEDES rules 7 & 83's "muted by default." The eyebrow is a branded micro-label and should carry the accent. Drop it to `--text-muted` ONLY when an accent-colored element sits within ~200px and would clash (true color-redundancy — e.g. the CTA slide where a gradient hero-highlight is right below the eyebrow). On a normal content slide the accent element is in the diagram far below the eyebrow, so **the eyebrow is teal.** Bonus: teal at 14px clears contrast; muted grey at 14px FAILS it (rule 86). When in doubt, eyebrow = teal.

85. **HERO-HIGHLIGHT IS MANDATORY ON THE HOOK/TITLE SLIDE.** The hook headline MUST apply the gradient hero-highlight (rule 80: `background: var(--accent-gradient); color: var(--bg)`) to its single key phrase. A title slide with a flat all-white headline is unfinished. The CTA slide also gets one. Content-slide headlines stay monochrome — their one teal "hero moment" lives in the diagram. (One hero moment per slide; the hook's is its title, a content slide's is its diagram.)

86. **CONTRAST IS A HARD GATE — RUN IT BEFORE EVERY RENDER.** NEVER use `--text-dim` (`#3f3f46`, 1.7:1) for ANY text that is meant to be read — labels, captions, sub-labels, diagram text, or dots/marks that carry meaning. `--text-muted` (`#71717a`, 4.0:1) is allowed ONLY at ≥18px; below 18px on muted FAILS AA. For quiet-but-readable text at any size use `#a1a1aa` (zinc-400, 6.4:1). Invented faint greys (`#52525f`, `#56565f`, etc.) on label text are FORBIDDEN — they fail contrast and read as broken placeholders. Pre-render check: `grep -nE '#3f3f46|text-dim|#5[0-9a-f]{5}' /tmp/social-canvas/slide-*.html` — any hit on a text element is a failure to fix before rendering.

87. **EVERY SLIDE CARRIES THE ACCENT AT LEAST ONCE.** No all-monochrome slide in a branded carousel. Even the "problem"/failure slide must show the accent on the semantically-correct element. On a slide about a thing failing, the accent goes on the *subject* (e.g. the AI-native initiative being attacked is teal; the forces attacking it are grey) — never leave the slide colorless. A zero-accent slide reads as unfinished and breaks carousel rhythm.

88. **DIAGRAM ARROWS MUST ALIGN WITH THE ELEMENTS THEY CONNECT.** An arrow that floats between two elements without sharing an axis with its source AND target is a confusing-diagram bug (the user: "arrows are not center aligned with the boxes, making the diagram very confusing"). Use a CSS grid so each arrow sits in the same column/row as the box it points from and to. After rendering, trace each arrow by eye: it must visibly run box → box. Never eyeball-space arrows with a fixed gap and hope they line up.

89. **NO BOTTOM-SQUEEZE.** Do not cram a caption / takeaway / quote into the strip between the diagram and the footer to "fill space" or tack on a stray thought. Two valid options only: (a) integrate the line into the header/sub or as a deliberate, properly-spaced element *inside* the diagram, or (b) cut it and give the diagram the room. A line wedged above the footer reads as an afterthought and starves the diagram of space. If a thought matters, it earns a real place in the composition; if it doesn't, delete it.

90. **CLAUDE CODE RUNTIME → EDITABLE GALLERY, NOT JUST PNGs.** On Claude Code / Claude Code Desktop the preview MUST be an editable gallery: every text element is `contenteditable` (plus the rule-78 click-focus helper), served by a preview server that has a save endpoint, so the user can click any text in the preview and edit it. PNG export exists only to assemble the final PDF. Shipping a static PNG-only preview on Claude Code (the agent runtime flow) is wrong — the agent runtime variant is PNG-only solely because it has no gallery. If the installed skill copy is the agent runtime variant on a Claude Code machine, stand up the editable gallery anyway and flag the variant mismatch. **The gallery server is the DURABLE `scripts/preview-gallery-server.py` (it serves the slide dir, renders scaled iframes, and exposes the Save button + `/save` endpoint with a pre-write backup), NEVER a `/tmp`-resident script. Phase 2's `rm -rf /tmp/social-canvas` wipes /tmp every run, so a server kept there is destroyed and the preview ships save-less (this exact bug shipped 2026-06-17). Only slide DATA (HTML, logo, PNGs, `.backups/`) lives in /tmp. `launch.json`'s `social-canvas-preview` MUST run the durable script with the slide dir + port as args: `["…/skills/social-canvas/scripts/preview-gallery-server.py", "/tmp/social-canvas", "8547"]`. After `preview_start`, VERIFY a save round-trips (POST `/save` returns 200 and a `.backups/` file appears) before telling the user the preview is ready (rule 59).**

91. **EDITABLE-GALLERY SAVE MUST STAY CLEAN — AND USER EDITS ARE SACRED.** When wiring rule-90 editability: (a) use `contenteditable="plaintext-only"` on text elements so the browser does NOT inject inline `style` spans / `background-color` / `&nbsp;` during editing (raw `contenteditable="true"` mangles the hero-highlight span markup — confirmed 2026-06-03). (b) On save, sanitize before writing: strip every runtime-added `contenteditable` attribute and any browser-injected `style` attribute (slide text carries no original inline styles — styling lives in the `<style>` block; the only legit inline style is the logo `<img>`). Saving raw `outerHTML` bakes cruft that compounds on the next edit. (c) Re-render PNGs from the SANITIZED HTML. (d) NEVER re-render PNGs or overwrite a slide the user has edited/may be editing without explicit permission (rules 28 & 32) — preserve the user's TEXT intent even when cleaning injected markup.

92. **NEVER DESTROY USER EDITS — THE EDIT-IN-PLACE PROTOCOL.** THE #1 TRUST-BREAKER. Violated catastrophically 2026-06-04: repeated re-renders that `cp`'d working copies over the served files, plus iframe reloads, erased the user's title/subtitle edits across multiple slides — and there was NO backup, so it was unrecoverable. "Don't overwrite edits" (rules 28/32/91) was not enough; the specific mechanisms must be banned. Once an editable gallery is live and the user can edit, their text lives in the SERVED files and sometimes only in the unsaved iframe DOM — it is irreplaceable. Treat every served slide file as sacred. These are absolute:

   a. **SERVED FILES ARE THE ONLY SOURCE OF TRUTH.** The instant the gallery is up, ABANDON every `/tmp`/working copy. NEVER `cp`, overwrite, or regenerate a served slide file from a working copy or template. To read a slide's current content, READ THE SERVED FILE. The fatal pattern was `cp /tmp/.../slide-N.html <served-dir>/` on every "sync"/"re-render" — it silently clobbers user edits. Never run it.

   b. **NEVER RELOAD THE USER'S IFRAMES OR PREVIEW.** No `location.reload()`, no `iframe.contentWindow.location.reload()`, no reloading the panel, no restart that refetches. A reload discards EVERY unsaved edit on EVERY slide at once. If you changed a served file, ASK THE USER to refresh when they're ready — never refresh for them.

   c. **CHANGE THINGS BY EDITING THE SERVED FILE IN PLACE, SURGICALLY, AFTER READING IT.** Targeted Edit only. A CSS/size change touches only the CSS rule; a copy fix touches only that one text node — every other byte stays identical. NEVER rewrite a whole slide file the user has seen; full regeneration from a template is how their text dies.

   d. **BACK UP BEFORE EVERY WRITE.** Before editing or rendering any slide the user may have touched, copy it to a timestamped backup (`.backups/slide-N.html.bak-<ts>`). 2026-06-04 was unrecoverable solely because no backup existed. With backups, user edits are always restorable.

   e. **RE-RENDER ONLY ON EXPLICIT INSTRUCTION** ("re-render" / "render the finals" / "lock it"), and render FROM the served, user-edited files — never from a stale working copy.

   f. **ONE DIRECTORY.** Generate, serve, render, and export from a SINGLE location so a working copy can never diverge from (and overwrite) the served copy. If the launch config path must live elsewhere (e.g. `/tmp`), have that launcher SERVE the durable project dir — do not keep a second editable copy.

   Self-check before ANY file write or `preview_eval` once a gallery is live: "Am I about to `cp` over a served file, reload an iframe, or rewrite a whole slide the user has seen?" If yes → STOP. Read the served file and make a surgical, backed-up, in-place edit instead.

93. **DESIGN / VOICE HEURISTICS (the user review 2026-06-04).**
   a. **No em dashes in on-slide copy.** the user's no-em-dash voice rule (from email) extends to ALL slide text — titles, subs, captions, labels. Use a period, comma, parentheses, or colon. No exceptions.
   b. **Converging arrows distribute around the target's perimeter — never stack on one edge.** When several arrows point at one box, give each a DISTINCT landing point (top-left, top-right, bottom-left, bottom-right, mid-left, mid-right). Corner source-boxes elbow (one right angle) to the nearest top/bottom edge point; boxes level with the target go straight into the side. Three arrowheads piled onto one edge reads as a confusing diagram (the user flagged exactly this on the "surrounded" slide).
   c. **Size text to FILL its container.** A label left at the size-minimum inside a large box reads as dead space. Scale it up to fill (e.g. the legacy workflow labels went 19px → 32px in tall row-boxes). "Fill the space" (rule 71) applies to text inside containers, not just overall layout — when a box looks empty, the text in it is usually too small.
