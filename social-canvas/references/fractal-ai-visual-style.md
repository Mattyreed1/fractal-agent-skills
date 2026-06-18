# Fractal AI — Visual Style Guide for Social Canvas

Source: Fractal AI Brand Doc (Notion)

---

## Contents

- Color System
- Typography
- Layout & Spacing
- Visual Elements
- Content Design Patterns
- Brand Alignment Checklist
- Hard Rules (Learned from Production)
- Quick Reference: CSS Variables

## Color System

**Philosophy**: Black and white. Dark mode. High contrast, monochromatic. No color for decoration — only for meaning.

### Primary Palette
| Role | Hex | Usage |
|------|-----|-------|
| Background | `#09090b` | Canvas background. Near-black, not pure black (avoids harshness on screens). |
| Surface | `#111113` | Cards, code blocks, elevated containers. Barely lighter than bg. |
| Border | `#1c1c22` | Subtle dividers, container outlines. Visible but quiet. |
| Text | `#fafafa` | Primary text. Near-white, not pure white (reduces eye strain). |
| Text Muted | `#71717a` | Secondary text, captions, descriptions. Zinc-500. |
| Text Dim | `#3f3f46` | Tertiary text, comments, metadata. Zinc-700. |

### Emphasis (No Color Needed)
The primary visual system is contrast and weight — not color.

| Role | Hex | When to use |
|------|-----|-------------|
| Primary emphasis | `#fafafa` | Bold white text on dark. This IS the accent. |
| Secondary emphasis | `#e4e4e7` | Slightly dimmer. For supporting highlights. |
| Code/Mono | `#a1a1aa` | Monospace text in code blocks. Zinc-400. |

### Brand Accent — The Teal → Blue Gradient (PRIMARY)

The Fractal AI brand's signature visual is a **135° gradient from teal to electric blue**. This is the canonical brand treatment, sourced directly from `fractalai.agency`'s `--color-accent-start` and `--color-accent-end` CSS variables.

| Token | Hex | Role |
|-------|-----|------|
| `--accent-teal` (start) | `#00c6a2` | Solid color for strokes, arrows, icons, halos, small accents. Brand primary. |
| `--accent-end` (end) | `#0077ff` | Gradient endpoint only — never used as a solid by itself. |
| `--accent-gradient` | `linear-gradient(135deg, #00c6a2, #0077ff)` | Hero fills: large filled disks/badges, hero highlight backgrounds on key words, top-border accent strips on cards. |

**Use the simple two-stop form verbatim — same as the website.** No mid-stops, no custom weighting, no aspect-ratio adjustments. The site uses `linear-gradient(135deg, #00c6a2, #0077ff)` on every gradient surface regardless of shape; mirror that exactly. the user caught a 60%-hold variant 2026-05-10 — it shifted too much weight to teal and made shapes look muddied on the blue side. Don't reintroduce stop tweaks.

**SVG gradient def (paste into every SVG `<defs>` that needs the gradient):**
```svg
<linearGradient id="accent-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
  <stop offset="0%" stop-color="#00c6a2"/>
  <stop offset="100%" stop-color="#0077ff"/>
</linearGradient>
```
Use as `fill="url(#accent-gradient)"` on filled shapes (rect, circle, path with `fill-rule: evenodd`).

**Where the gradient goes (hero shapes):**
- Large filled circles/disks that anchor a diagram (e.g., the EXECUTING/EVALUATING nodes in the Execution-Evaluation Loop slide)
- Hero-highlight word backgrounds (the emerald block behind a single key word in the headline — now a gradient block)
- Top-border accent strips on cards (1–4px tall, `background: var(--accent-gradient)`)
- CTA button backgrounds

**Where the gradient does NOT go (use solid `#00c6a2` instead):**
- Arrow strokes, lines, dividers, thin borders (`<1px` widths read as muddy under a gradient)
- SVG marker arrowheads (small triangles — solid teal is crisper)
- Halo / glow elements (filter-blurred shapes — the gradient blurs out)
- Icons under ~24px
- Body text or labels

**Single-system rule.** A piece uses EITHER the brand gradient + solid `#00c6a2` (default), OR a single alternate accent (emerald/amber/pink/red — see palette below) for non-brand pieces. Never mix the brand gradient with an alternate accent.

### Alternate Accent Palette (for non-brand work)

Use only when the piece is intentionally off-brand or needs a different semantic color (e.g., amber for warning, red for danger in a comparative chart). Default to the brand gradient otherwise.

| Name | Hex | Best for |
|------|-----|----------|
| Emerald (legacy) | `#10b981` | Retained for backward compatibility on existing emerald-colored decks. NOT the brand primary — that's teal. |
| Blue | `#3b82f6` | Technical, system, process (distinct from the gradient endpoint `#0077ff`) |
| Amber | `#f59e0b` | Warning, caution, cost, risk |
| Pink | `#ec4899` | Human, emotion, creative |
| Red | `#ef4444` | Danger, error, cost-up |

**Rules:**
1. **Default is no accent at all.** Most content works best as pure monochrome — white, gray, black on the dark bg.
2. **One accent system per piece.** Either the brand gradient (with `#00c6a2` solids), OR one alternate accent — never mixed.
3. **Same color = same meaning.** A color is a semantic label. Using it for two different meanings is worse than using no color at all.
4. **Color in small doses only.** Acceptable: a keyword, a thin border, a number, a 4px indicator bar, a hero fill on 1–2 shapes per piece. NOT acceptable: large background fills on multiple containers, full-width colored blocks.
5. **When in doubt, skip color.** White text hierarchy (bold/regular/muted/dim) handles 90% of visual communication.

---

## Typography

**Philosophy**: Clean sans-serif. Sharp, geometric. Bold for headlines. Readable at all sizes.

### Font Stack (from canvas-fonts directory)

| Role | Font | File | Why |
|------|------|------|-----|
| Headlines | **Outfit Bold** | `Outfit-Bold.ttf` | Geometric sans-serif. Sharp, modern, high impact. |
| Body | **Instrument Sans** | `InstrumentSans-Regular.ttf` | Clean, neutral, excellent readability. |
| Code/Files | **JetBrains Mono** | `JetBrainsMono-Regular.ttf` | Technical monospace. File names, code, terminal output. |
| Code Bold | **JetBrains Mono Bold** | `JetBrainsMono-Bold.ttf` | Emphasis within code blocks. |

**No other fonts.** Consistency across all Fractal AI visual content. No serif, no display, no handwriting fonts.

### Type Scale (1080px canvas)

| Element | Size | Weight | Line Height | Font |
|---------|------|--------|-------------|------|
| Hero headline | 56–72px | Bold | 1.05–1.1 | Outfit Bold |
| Slide headline | 44–56px | Bold | 1.1 | Outfit Bold |
| Subhead | 28–36px | Regular | 1.3 | Instrument Sans |
| Body text | 24–28px | Regular | 1.5 | Instrument Sans |
| Caption | 18–20px | Regular | 1.4 | Instrument Sans |
| Code/filenames | 16–20px | Regular/Bold | 1.6 | JetBrains Mono |
| Handle/meta | 16px | Regular | 1.0 | JetBrains Mono |

### Typography Rules
- Headlines are always **Outfit Bold**. Never lightweight headlines.
- Body text is always **Instrument Sans Regular**. Never bold body.
- File names, code, and terminal output are always **JetBrains Mono**.
- All caps + letter-spacing (2-3px) for eyebrow labels only. Never for body or headlines.
- Maximum 2 font sizes per slide (headline + body). 3 if a code block is present.

---

## Layout & Spacing

**Philosophy**: Minimalism and clarity. Engineering precision. Every element placed with intention.

### Grid System
- **8px base grid**. All spacing values are multiples of 8.
- **64px canvas padding** (safe zone on all sides).
- **32px** default gap between content blocks.
- **16px** gap within grouped elements (e.g., lines in a code block).

### Layout Rules
- **Flex column** for vertical content flow. Never absolute positioning for text.
- **Left-aligned text** as default. Center-aligned only for CTA slides.
- **One idea per slide.** If it doesn't fit, split it.
- **Generous negative space.** When in doubt, remove an element. Don't fill the canvas.
- **Top-weighted content.** Headlines and primary content sit in the upper 60% of the canvas. Bottom 40% breathes.

### Consistent Elements (every slide)
- Fractal AI logo — bottom-left, 48-56px height, 0.85-0.9 opacity. NEVER a text handle.
- Slide indicator (e.g., `01 / 06`) — bottom-right, 14px JetBrains Mono, text-muted color.
- Both positioned within the 64px safe zone.

---

## Visual Elements

**Philosophy**: Technical, precise. Thin linework. Diagrams over decoration.

### Containers & Cards
- Background: `#111113` (surface color)
- Border: `1px solid #1c1c22`
- Border radius: `10–12px` (subtle rounding, not bubbly)
- Padding: `24–32px` internal

### Indicator Bars
- Width: `4–6px`
- Height: matches content height or `40–48px` fixed
- Border radius: `3px`
- Used for: layer identification, section markers

### Dividers
- `1px solid #1c1c22`
- Full width or partial (60% for subtle section breaks)
- Never thick. Never colored.

### Terminal/Code Blocks
- Dark surface background with border
- Optional terminal header with 3 dots (red/yellow/green) for macOS feel
- Monospace font throughout
- Keys in accent/muted color, values in primary text color
- Comments in dim text color (`#3f3f46`)

### What to AVOID
- ❌ Gradients (violates monochromatic principle)
- ❌ Drop shadows (flat design only)
- ❌ Icons or emoji as visual elements (text and structure carry the message)
- ❌ Background patterns or textures
- ❌ Rounded pill shapes (too soft — keep it sharp)
- ❌ Color blocks or colored backgrounds on containers
- ❌ Decorative circles, blobs, or abstract shapes (unless directly representing a concept like a feedback loop)

---

## Content Design Patterns

### Hook/Title Slide
- Eyebrow label: all-caps monospace, muted color, letter-spaced
- Headline: 56–72px Outfit Bold, near-white
- Subtitle: 28–32px Instrument Sans, muted color
- Optional: structural element (stack diagram, terminal block) in lower half
- Bottom: handle + slide number

### Content Slide (Explanation)
- Section label: all-caps monospace, text-muted, letter-spaced (NOT colored — labels are structural, not semantic)
- Headline: 44–56px statement that summarizes the slide
- Body: 24–28px supporting explanation, max 3 lines
- Optional: code block, example cards, or flow steps
- Bottom: logo + slide number

### Stat Slide
- Large number: 80–120px Outfit Bold, primary white
- Label below: 28px Instrument Sans, muted
- Context sentence: 24px, muted
- Minimal — the number IS the slide

### CTA Slide
- Center-aligned layout
- Badges or labels at top (e.g., file name badges)
- Headline: 52–60px Outfit Bold
- Supporting text: 24–28px muted
- CTA keyword: large monospace, high contrast (white on dark, or inverted)
- Instruction: "Comment X below" in body text

---

## Brand Alignment Checklist

Before finalizing any visual, verify:

- [ ] Background is near-black (`#09090b`), not gray, not dark blue
- [ ] Text is near-white (`#fafafa`), not gray
- [ ] Color is used functionally (max 1 accent color per slide), never decoratively
- [ ] Fonts are Outfit Bold / Instrument Sans / JetBrains Mono only
- [ ] Layout feels engineered, not designed-by-template
- [ ] Negative space is generous — at least 30% of the canvas is empty
- [ ] Nothing feels "pretty" — it should feel **precise**
- [ ] Would a technical founder look at this and think "this person knows their stuff"?

---

## Hard Rules (Learned from Production)

These rules were learned from real carousel sessions. Violating any of them produces visibly bad output.

### Sizing Minimums
| Element | Minimum | Recommended | Never |
|---------|---------|-------------|-------|
| Logo (footer) | 48px height | 56px | Below 40px — becomes a white smudge |
| Slide numbers | 20px | 22px | Below 18px — unreadable at mobile size |
| Logo opacity | 0.85 | 0.9 | Below 0.7 — fades into background |
| Headlines (hook) | 56px | 64px | Below 48px |
| Headlines (content) | 48px | 56px | Below 40px |
| Body text | 26px | 30px | Below 24px |
| Block labels | 32px | 36px | Below 28px |
| Code/terminal text | 22px | 24px | Below 20px |

### Layout Rules
- **No dead space.** If content doesn't fill the canvas, use `flex: 1` on content containers so elements grow to fill. A large empty zone = lazy design.
- **Footer spacing.** Always add `padding-top: 32px` on the `.bottom` footer bar when content above could crowd it.
- **Accent consistency.** If an accent color appears on one slide, it carries the same meaning on every slide. Never use the same color for two different concepts.
- **64px safe zone.** All canvas padding is 64px. Content must never touch the edge.

### Emoji Rules
- Never place emojis on a colored background. Emojis go on the dark `--bg` background only.
- If a colored background needs an icon, use a beautiful SVG/unicode icon, not an emoji.
- Emoji size: 64px standalone.

### Brand Rules
- Always show the Fractal AI logo in the bottom-left footer. Never use a text handle like @username.
- Logo file must be copied to the working directory for iframe/preview access (relative path `logo.png`).
- Never overwrite user edits. If the user edits text in the preview, preserve those changes. Only re-render when the user says "render the finals."

---

## Quick Reference: CSS Variables

```css
:root {
  --bg: #09090b;
  --surface: #111113;
  --border: #1c1c22;
  --text: #fafafa;
  --text-muted: #71717a;
  --text-dim: #3f3f46;
  --font-heading: 'Heading', sans-serif;  /* Outfit-Bold.ttf */
  --font-body: 'Body', sans-serif;        /* InstrumentSans-Regular.ttf */
  --font-mono: 'Mono', monospace;         /* JetBrainsMono-Regular.ttf */
}
```
