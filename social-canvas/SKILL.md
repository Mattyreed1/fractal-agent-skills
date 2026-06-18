---
name: social-canvas
description: >
  Closed-loop social media infographic and carousel generator for Claude Code on the user's Mac.
  Renders HTML/CSS to PNG via Python Playwright (scripts/render.py), reads the PNG back,
  evaluates quality, and iterates until polished and publish-ready.
  Supports LinkedIn carousels, Instagram posts/stories, Twitter/X graphics, and infographics.
  (the agent fleet agents run their own fork of this skill on the VPS — keep the two in sync
  via skill-translate, but THIS copy is Claude Code-native.)
license: MIT
metadata:
  version: 3.0.0
  platform: claude-code
  parity_note: the agent runtime fork lives on the VPS (synced via skill-translate); render.js is kept for that runtime
---

# Social Canvas — Closed-Loop Visual Generator (Claude Code)

Generate pixel-perfect social media infographics and carousels with a visual feedback loop. Generate HTML/CSS → render to PNG via `scripts/render.py` (Python Playwright) → Read the PNG back → evaluate against quality criteria → fix and re-render until the output is polished.

**Skill base directory:** `~/.claude/skills/social-canvas` (also reachable as `~/.claude/skills/social-canvas`)
**Renderers:** `scripts/render.py` is the Claude Code/Mac renderer (Python Playwright, verified working). `scripts/render.js` is the agent runtime-container renderer (playwright-core) — kept only for syncing to the VPS fork; do not use it locally.

---

## PHASE 0 — CLARIFY

**Before doing anything, gather what you need.** Ask the user clarifying questions to fill gaps. Skip questions they already answered in their prompt.

**Hard gate**:
- Do not assume the format, scope, slide count, platform, or aesthetic direction when the user has not explicitly provided them.
- Do not inspect prior artifacts for direction-setting, propose a concept, read design references, or start building files until Phase 0 is complete.
- Your first substantive response after loading this skill must be a clarification message if any required inputs are missing.
- If required inputs are still missing after the first clarification pass, stop and wait for the user's answer instead of proceeding with assumptions.
- If the user explicitly says "you decide", record that delegated choice in one sentence, then proceed.

**Minimum required inputs before Phase 1**:
- Output format
- Scope of the deliverable
- Aesthetic direction
- Whether the provided facts should be used as-is or verified first
- **The core idea the visual must land** (one sentence): derive it from the piece's thesis / Core Claim and the source's own central metaphor, NOT the hook. The visual illustrates the payoff, not the opening line. (A visual once shipped illustrating only the hook and missing the post's actual thesis, 2026-06-17.)

**Required question block**:
- Ask only for unanswered items.
- Prefer 3-5 concise questions.
- Plain-text questions with short option hints inline, e.g.: `Format: single infographic, LinkedIn carousel, Instagram post, or other?`

Questions to resolve:
1. **Platform/format**: LinkedIn carousel? Instagram post? Twitter/X? Story? (Determines dimensions — see `references/format-specs.md`)
2. **Core message**: What's the main point or topic?
3. **Slide count**: For carousels, how many slides? (Default: 5-7 for LinkedIn, 3-5 for Instagram)
4. **Content specifics**: Any stats, quotes, data points, or key facts to include?
5. **Images/logos**: Any files to embed? Collect absolute file paths.
6. **Aesthetic direction**: Minimal, bold, editorial, technical, or playful? (See `references/design-patterns.md` for details)
7. **Research needed?**: Should the topic be researched first to gather current stats/facts? If yes, use Perplexity (search or reason) to gather data before designing.

**Rule**: Only proceed once you have enough info to produce something useful.

**Phase 0 completion check**:
Before entering Phase 1, restate the resolved brief in 5 lines or fewer:
- Format
- Scope
- Style
- Fact-handling choice
- Core idea the image must land (one sentence, from the thesis not the hook)
If you cannot fill all five lines from the user's answers or an explicit "you decide", Phase 0 is not complete. Every candidate concept must be tested against the core idea; reject any that only illustrate the hook or a sub-point.

---

## PHASE 1 — INTAKE & PLANNING

### Load Brand Config
**MANDATORY.** Read brand config at `brand-config.json` (relative to this skill's directory). This contains exact colors, fonts, logo paths, and branding rules. Do NOT use hardcoded defaults — the JSON is the source of truth.

### Load Design Rules
**MANDATORY.** Read `references/design-rules.md` before generating any HTML. These are hard constraints learned from production — every rule exists because it was violated and caught. Internalize the design rules.

### Load Visual Style Guide
**MANDATORY.** Read `references/fractal-ai-visual-style.md` for the full Fractal AI visual identity.

### Determine Format
Look up exact dimensions in `references/format-specs.md`. Set the width, height, and safe zone values.

### Plan Content Structure
For carousels, plan the narrative arc:
- **Slide 1**: Hook/title — stop the scroll with a bold statement or question → use `templates/layouts/hook.html`
- **Slides 2-N**: Content — one idea per slide, varied layouts → use `content-block`, `stat`, `list`, `quote`, or `comparison` templates
- **Final slide**: CTA — tell them what to do next → use `templates/layouts/cta.html`

**CRITICAL**: Select a layout template for EACH slide from `templates/layouts/`. Vary the patterns — don't use the same layout on every content slide. Available layouts:

| Template | Use For |
|----------|---------|
| `hook.html` | First slide — bold headline + optional visual element |
| `content-block.html` | Detail slides with color header block + data viz (code, cards, terminal, flow) |
| `stat.html` | Single powerful number/metric |
| `list.html` | 3-5 numbered items or takeaways |
| `quote.html` | Pull quote with attribution |
| `comparison.html` | Before/after, old vs new, two-column contrast |
| `cta.html` | Final slide — call to action |

---

## PHASE 2 — HTML/CSS GENERATION

### Setup
```bash
rm -rf /tmp/social-canvas && mkdir -p /tmp/social-canvas
# Copy logo for renderer access (relative paths)
cp ~/.claude/skills/social-canvas/brand-assets/fractal-ai-logo-tree-text-transparent-bg.png /tmp/social-canvas/logo.png
```

### Generate HTML Files from Templates
Create one self-contained HTML file per slide at `/tmp/social-canvas/slide-{N}.html`.

**PROCESS: Start from a layout template, then customize.**
1. Read the chosen template from `templates/layouts/{name}.html`
2. Read `templates/base-vars.css` for the locked brand tokens
3. Copy the template's HTML structure
4. Replace `{{PLACEHOLDERS}}` with actual content
5. Customize the data visualization zone (code block, cards, terminal, flow steps) as needed
6. Set `body { width: {WIDTH}px; height: {HEIGHT}px; }` for the target format

**LOCKED BRAND TOKENS** — Copy these EXACTLY into every slide's `<style>`. Never modify:
```css
:root {
  --bg: #09090b; --surface: #111113; --border: #1c1c22;
  --text: #fafafa; --text-muted: #71717a; --text-dim: #3f3f46;
  --accent-teal: #00c6a2; --accent-emerald: #10b981; --accent-blue: #3b82f6; --accent-amber: #f59e0b; --accent-pink: #ec4899;
  --accent-gradient: linear-gradient(135deg, #00c6a2, #0077ff);
  --glass-bg: rgba(17, 17, 19, 0.55); --glass-border: rgba(255, 255, 255, 0.12); --glass-blur: 18px;
}
```

**BODY BACKGROUND** — Every slide body MUST include the dotted-grid texture. Do NOT render on flat `--bg`.
```css
body {
  width: {WIDTH}px; height: {HEIGHT}px; overflow: hidden;
  background-color: var(--bg);
  background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='24' height='24'><rect x='0' y='0' width='2' height='2' fill='%23ffffff' fill-opacity='0.14'/></svg>");
  background-size: 24px 24px;
  background-position: 12px 12px; /* 1/2 square shift — the user confirmed 2026-04-23 */
  color: var(--text); font-family: 'Geist', sans-serif;
  border: 1px solid rgba(255,255,255,0.14); /* edge border — defines the image on dark backgrounds; the user 2026-06-17 */
}
```
`background-position: 12px 12px` offsets the grid by half a tile so dots sit inset from the canvas edges instead of flush against them. This is mandatory — the grid should appear to float inside the frame, not be clipped by it. The `body` ALSO carries a 1px hairline edge border (`border: 1px solid rgba(255,255,255,0.14)`, kept inside the canvas via `box-sizing: border-box`) that defines the image rectangle so the near-black canvas does not vanish into a dark background (LinkedIn dark mode, a black deck, the preview gallery). Mandatory on every slide (the user 2026-06-17).

**SHARP CORNERS ONLY** — Every box, card, container, panel, pill, terminal, button — `border-radius: 0`. No 4/8/12/14/999px anywhere. Only exception: circular dots/indicators can use `border-radius: 50%`. Locked 2026-04-23 (extended from gallery chrome to slide content).

**SURFACES ARE GLASS** — Every card, panel, column, badge, image frame, code block uses the glass treatment (never opaque `--surface`):
```css
.card, .column, .panel, .badge {
  background: var(--glass-bg);
  backdrop-filter: blur(var(--glass-blur));
  -webkit-backdrop-filter: blur(var(--glass-blur));
  border: 1px solid var(--glass-border);
}
```
The dotted grid shows through the blur, giving depth. Using opaque `--surface` on cards is a regression — it hides the texture.

**LOCKED SIZES** — Never go below these minimums:

| Element | Min Size | Font | Weight |
|---------|----------|------|--------|
| Hook headline | 64px | Geist Sans | 700/800 |
| Content headline | 56px | Geist Sans | 700 |
| Description/subtitle | 28px | Geist Sans | 400/500 |
| Body text | 26px | Geist Sans | 400 |
| Code/terminal | 24px | Geist Mono | 400/500 |
| Mono labels/micro-type | 16-22px | Geist Mono | 500/700 |
| Eyebrow / micro-label | 14px | **Silkscreen** | 400/700 |
| Logo | 44px height | — | — |
| Website note | 14-22px | Geist Mono | 400 |

**FONT LOADING** — Single Google Fonts @import at the top of every slide's `<style>`:
```css
@import url('https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600;700;800&family=Geist+Mono:wght@400;500;700;800&family=Silkscreen:wght@400;700&display=swap');
```
The container has network access — `render.js` uses `waitUntil: 'networkidle'` and `document.fonts.ready`, so Google Fonts load deterministically before screenshot.

Then reference via `font-family` directly:
- `font-family: 'Geist', sans-serif;` — headlines (700/800), body (400/500), descriptions (400).
- `font-family: 'Geist Mono', monospace;` — labels, code, terminal, website note.
- `font-family: 'Silkscreen', monospace;` — eyebrows + micro-labels ONLY. Size **14px**. UPPERCASE. letter-spacing 0.22em (~3px at 14px).

**Font rules (updated 2026-04-23 — retired Outfit / Instrument Sans / JetBrains Mono):**
- Geist Sans is the only sans in the system — headlines AND body both use it, just different weights.
- Silkscreen is ONLY for eyebrows/micro-labels at **14px**. Never for body copy, headlines, or anything above 16px.
- Eyebrow pattern: `font-family: 'Silkscreen', monospace; font-size: 14px; font-weight: 400; letter-spacing: 0.22em; text-transform: uppercase; color: var(--accent-teal);` — **Eyebrow DEFAULTS to the brand accent (teal `#00c6a2`)** (the user 2026-06-03 — SUPERSEDES the old "muted by default", see design-rules #84). The eyebrow is a branded micro-label; it carries the accent. Drop it to `--text-muted` ONLY when an accent element sits within ~200px and would clash (true color-redundancy, e.g. the CTA slide's gradient highlight sitting right under the eyebrow). On a normal content slide the diagram's teal is far below the eyebrow, so the eyebrow stays teal. Bonus: teal clears contrast at 14px; muted grey at 14px FAILS it.
- Mono labels at ~18-22px use Geist Mono (not Silkscreen). Silkscreen's working range is 12-16px; 14px is the standard.

**BOTTOM BAR** — Identical on every slide. Logo in one corner, website in the other. NEVER a slide number, NEVER empty.
```html
<div class="bottom">
  <img src="logo.png" style="height:44px; width:auto; opacity:1;">
  <div class="bottom-note">fractalai.agency</div>
</div>
```
- Logo: bottom-left, 44px height, 100% opacity (see `logo_render` in `brand-config.json`)
- Website: bottom-right, pulled from `website` field in brand config (default `fractalai.agency`)
- The logo uses a RELATIVE path (`logo.png`). It's copied to `/tmp/social-canvas/` in setup.
- Do not reintroduce `.slide-num` / `{{SLIDE_NUM}}` — it was retired 2026-04-22.

**BOTTOM BAR POSITIONING — LOCKED 2026-04-23:**
- Canvas padding is **64px 64px 28px** (not uniform 64px). The reduced bottom padding pushes the logo down into the lower safe-zone margin, closer to the physical bottom edge.
- `.bottom` uses `align-items: center` (NOT `flex-end`) so the logo and the website note are vertically centered on the same axis.
- Add `margin-top: 18px` to `.bottom` for a consistent gap above it.
- Full rule: `.bottom { display: flex; justify-content: space-between; align-items: center; margin-top: 18px; }` and `.canvas { padding: 64px 64px 28px; }`.

**LAYOUT RULES**:
- `display: flex` or `display: grid` — NEVER absolute positioning for text
- Safe zone: `padding: 64px 64px 28px` on the canvas container (bottom reduced so logo sits in the margin)
- 4/8px grid for all spacing values (never 5/7/13/17)
- `justify-content: space-between` on canvas to push footer to bottom
- Left-aligned text (except CTA slides which are center-aligned)
- **READ `references/design-rules.md` "Layout Rules of Thumb — Filling Space & Spacing Between Containers"** before building any slide. It has the Three-Zone Canvas Pattern (eyebrow + flex:1 main + footer), the three fill patterns (A/B/C), exact spacing px tables, container rules, and the 6-item quick audit checklist. Dead-space bugs and cramped layouts are the top-2 regressions — that section prevents both.

**EMOJI RULE**: Emojis appear on the dark `--bg` background only. NEVER place an emoji on a colored background.

**COMPLEX DIAGRAMS → `diagram-design`**: For a real node-edge diagram (branching flow, architecture, KG graph), do NOT hand-position nodes in CSS. Render it with the **diagram-design** skill (D2 auto-layout; `--brand fractal` matches this palette — dark `#09090b` + teal `#00c6a2`), then embed the resulting SVG inside the slide's data-viz zone. Keep simple linear step sequences as the native `flow` pattern. Runtime: D2 is Mac-local for now; on the agent runtime the VPS needs D2 installed + this engine synced via `skill-translate` (until then, hand-build the diagram in HTML/CSS).

---

## PHASE 3 — RENDERING

### Pre-render gate — EDITABILITY CHECK (hard error)

Before rendering ANY slide, run this check:

```bash
grep -n '<text ' /tmp/social-canvas/slide-*.html
```

Expected output: **empty**. Any line returned is a plain SVG `<text>` element — a HARD ERROR on this runtime (the gallery iframe must support clickable editing, and SVG `<text>` rasterises differently than HTML text, introducing font-rendering inconsistencies). Convert to a `<foreignObject>` containing a `<div>`. See design-rules.md rule 78 for the canonical template.

**Then run the editable-text gate — EVERY visible text node must be editable, not just the headline:**

```bash
python3 ~/.claude/skills/social-canvas/scripts/check-editable.py /tmp/social-canvas
```

Expected: `all text editable` (exit 0). A FAIL lists any text node missing `contenteditable` (e.g. a `.band-label` or `.bottom-note`); add `contenteditable="plaintext-only"` to it (or its text wrapper) before rendering. Re-run this after `preview_start` too, and NEVER declare the preview ready until it returns exit 0. (A non-editable label shipped 2026-06-17 because only the headline was spot-checked — `grep` cannot see editability, so this script gate is mandatory.)

### Render

Render each slide HTML to PNG with the Python render script (verified working on this Mac):

```bash
python3 ~/.claude/skills/social-canvas/scripts/render.py \
  /tmp/social-canvas/slide-{N}.html \
  /tmp/social-canvas/slide-{N}.png \
  --width {WIDTH} --height {HEIGHT}
```

Verify the output message shows correct dimensions (e.g., `rendered .../slide-1.png (1080x1350)`).

If the render reports a dimension mismatch, check the HTML body width/height.

**Renderer behaviour:**
- Uses the Mac's Python Playwright + its managed Chromium (same engine as the `browser` skill). If launch fails with "Executable doesn't exist", run `python3 -m playwright install chromium` once.
- Sets `device_scale_factor=1` — prevents 2x output.
- `wait_until="networkidle"` for Google Fonts to download.
- `document.fonts.ready` wait — guarantees all @font-face rules have applied before screenshot.
- Viewport-clipped screenshot.

---

## PHASE 4 — CLOSED-LOOP EVALUATION

**This is the key innovation.** Read each rendered PNG and evaluate it visually.

### For each slide:

**Step 0: Message check (BEFORE any execution evaluation).** Ask: if a viewer saw ONLY this image, would they get the piece's core idea (the one sentence locked in Phase 0 / by `content-visuals`)? And does the FORM fit the idea (a loop/compounding idea shown as a cycle that grows, a comparison as contrast, a hierarchy as layers; a static arrangement for a process idea is wrong)? If no, the CONCEPT is wrong: stop, change the concept, and do NOT proceed to execution polish. Polishing a concept that fails this is wasted work, a stack-vs-loop concept miss got polished through ~8 execution rounds before it was caught (2026-06-17).

**Step 1: Read the PNG**
Read `/tmp/social-canvas/slide-{N}.png` to view it.

**Step 2: Evaluate against quality checklist**
Read `references/quality-checklist.md` for the full criteria. For each of the 10 items, state **PASS** or **FAIL: {specific problem and concrete fix}**.

**Also check against `references/design-rules.md`** — verify ALL hard rules are satisfied (the 2026-06-03 rules 84–90 are the most-missed). Mandatory per-slide gates before you call a slide done:
- **Eyebrow = teal** (rule 84) unless an accent element is within ~200px.
- **Hook/CTA title carries the gradient hero-highlight** (rule 85); content titles stay mono with teal in the diagram.
- **Contrast** (rule 86): grep for `#3f3f46`/`text-dim`/invented faint greys on any text — zero hits. Muted only at ≥18px.
- **Accent present on EVERY slide** (rule 87) — no colorless slide.
- **Arrows aligned to their boxes** (rule 88) — grid axes, verified by eye in the PNG.
- **No bottom-squeeze** (rule 89) — captions are integrated or cut, never wedged above the footer.
- **Editable gallery on Claude Code** (rule 90) — contenteditable + click-focus helper + save server, not PNG-only.
- **NEVER destroy user edits** (rule 92) — once the gallery is live, the SERVED files are the only source of truth: edit them in place after reading, back up before every write, NEVER `cp` a working copy over a served file, NEVER reload the user's iframes, re-render only on explicit instruction. This is the #1 trust-breaker.

Be CONCRETE, not vague:
- GOOD: "FAIL: Headline text 'Why AI Agents Need Feedback Loops' is clipped on the right side — reduce font-size from 72px to 60px"
- BAD: "FAIL: Looks a bit off"

**Step 3: Fix and re-render**
If ANY items fail:
1. Edit the specific HTML file to fix the identified issues
2. Re-run render.js to produce a new PNG
3. Read the new PNG and re-evaluate

**Step 4: Iteration cap**
- **Max 3 rounds per slide** (diminishing returns after that)
- Round 1: Fix structural issues (overflow, overlap, missing elements)
- Round 2: Fix refinement issues (spacing, hierarchy, line breaks)
- Round 3: Final polish (only fix things that meaningfully improve output)
- After round 3: Accept the result and note any remaining issues

### Carousel-specific checks
After all individual slides pass, do ONE cross-slide consistency check:
- Read all slide PNGs in sequence
- Verify: same font sizes for equivalent elements, same color scheme, same spacing patterns, headers/footers in consistent positions
- **Verify accent color is used consistently** — same color = same meaning on every slide
- Fix any inconsistencies found

---

## PHASE 5 — OUTPUT & DELIVERY

### Save final files
Once Phase 4 passes, deliverables live in `projects/` (never only `/tmp`):
```bash
SLUG="topic-name-here"  # lowercase, hyphenated
DATE=$(date +%Y-%m-%d)  # local time per CLAUDE.md timezone rule
# If this run belongs to a content piece, use that piece's folder instead:
#   ~/projects/<brand>-content/<piece-slug>/carousel/
OUTPUT_DIR="$HOME/projects/social-canvas-output/${DATE}-${SLUG}"
mkdir -p "$OUTPUT_DIR"
cp /tmp/social-canvas/slide-*.png "$OUTPUT_DIR/"
cp /tmp/social-canvas/slide-*.html "$OUTPUT_DIR/" 2>/dev/null || true
```

### Deliver to user
Report the output directory and per-slide file paths (clickable), with:
- Format and dimensions
- Number of slides
- Iteration count (how many rounds each slide needed)

**Editable gallery (Claude Code): the canonical preview, NOT a hand-rolled static viewer.** The gallery server is durable: `scripts/preview-gallery-server.py` (serves the slide dir, renders each slide in a scaled iframe, and exposes the **Save Edits** button + `/save` endpoint that writes a timestamped `.backups/` copy before every save). Stand it up and prove it:

1. `.claude/launch.json` `social-canvas-preview` `runtimeArgs` MUST point at the **durable** script with the slide dir + port: `["<repo>/skills/social-canvas/scripts/preview-gallery-server.py", "/tmp/social-canvas", "8547"]`. NEVER a `/tmp/social-canvas/*.py` path: Phase 2's `rm -rf /tmp/social-canvas` wipes /tmp every run, so a server kept there vanishes and you ship a save-less preview (this exact bug, 2026-06-17). Only slide DATA lives in /tmp; the server is durable in `scripts/`.
2. `preview_start "social-canvas-preview"`, then `preview_screenshot` to confirm the gallery + Save button render.
3. **TEST THE SAVE before telling the user it is ready (rule 59):** POST a save (`fetch('/save', …)` via `preview_eval`, or click the button) and confirm `200 {"ok":true}` AND a `/tmp/social-canvas/.backups/slide-*.bak-*` file appeared. A preview with no working Save button is a broken deliverable; this is a hard gate.

Then share the screenshot as proof.

### Iteration after delivery — SERVED FILES ARE THE ONLY SOURCE OF TRUTH (rule 92)
Once slides are saved to a project folder (and especially once an editable gallery is live, rule 90), **the `/tmp` edit-and-re-render flow is FORBIDDEN — it overwrites the user's saved edits.** Instead: (1) READ the served file (`<project>/.../carousel/slide-N.html`); it holds the user's edits and is the ONLY source of truth. (2) Back it up to `.backups/`. (3) Make a surgical in-place Edit (a CSS-only change touches ZERO text nodes). (4) NEVER `cp` a working copy over it; NEVER reload the user's iframes. (5) Ask the user to refresh. (6) Re-render PNGs/PDF only when the user explicitly says so, and only FROM the served files — `python3 scripts/render.py <served>.html <out>.png`. Editing `/tmp` and copying it over the served files, or reloading iframes, is what erased the user's work on 2026-06-04.

(The agent fleet fork of this skill delivers via Discord/Telegram and has no preview gallery — that's its concern, not this copy's.)

---

## DESIGN PHILOSOPHY

1. **Craftsmanship over speed**: The output must look like someone at the top of their field labored over every detail. Double-check spacing, alignment, and color choices.

2. **Anti-slop commitment**: No generic fonts, no template looks, no safe middle-ground aesthetics. Every design choice should feel intentional.

3. **Information density with breathing room**: Social media is information-dense but must not feel cramped. One idea per slide. Generous whitespace. Let content breathe.

4. **Refinement over addition**: When something doesn't look right, refine what exists rather than adding more elements. Simplify. Remove. Tighten.

5. **Visual hierarchy is non-negotiable**: On every slide, there must be ONE thing the eye goes to first. If everything is the same weight, nothing stands out.

6. **Precise, not pretty**: A technical founder should look at this and think "this person knows their stuff." Not "oh, nice Canva template."

---

## TEMPLATE SYSTEM

The template system ensures brand consistency without freehand CSS mistakes.

### Directory Structure
```
templates/
├── base-vars.css                 ← Locked brand tokens (colors, fonts, sizes, spacing)
├── base.html                     ← Reference shell
└── layouts/
    ├── hook.html                 ← First slide / title slide
    ├── content-block.html        ← Detail slide with color header + data viz
    ├── stat.html                 ← Single large number/metric
    ├── list.html                 ← Numbered items
    ├── quote.html                ← Pull quote with attribution
    ├── comparison.html           ← Before/after two-column
    └── cta.html                  ← Final CTA slide
```

### How Templates Work
- `base-vars.css` defines ALL brand tokens as CSS custom properties with locked values
- Each layout template is a complete HTML file with `{{PLACEHOLDERS}}` for content
- `content-block.html` includes 4 interchangeable data viz patterns (code, cards, terminal, flow) — pick one per slide
- Templates use relative `logo.png` path (copied to `/tmp/social-canvas/` during setup)
- The `:root` block is IDENTICAL across all templates

### Rules for Using Templates
1. **ALWAYS start from a template.** Never write slide HTML from scratch.
2. **NEVER modify the `:root` variables.** They are locked brand tokens.
3. **NEVER change font sizes below the locked minimums** in the size table above.
4. **ONE accent color per piece, max.** Same color = same meaning throughout. Default is monochrome.
5. **You MAY add new CSS classes** for custom data visualizations, but they must use the existing CSS variables.
6. **You MAY combine patterns** (e.g., a content-block slide with both cards and a code block), but test that content fits within the canvas.

---

## AVAILABLE FONTS

Loaded at runtime via Google Fonts `@import` (container has network access; `render.js` waits on `document.fonts.ready`).

**For Fractal AI brand, use ONLY these 3:**
- **Geist** → Headlines (weight 700/800) + body (400/500). `font-family: 'Geist', sans-serif;`
- **Geist Mono** → Labels, code, terminal, website note. `font-family: 'Geist Mono', monospace;`
- **Silkscreen** → Eyebrows + micro-labels ONLY at 14px uppercase. `font-family: 'Silkscreen', monospace;`

If you need a non-Fractal-AI palette (different brand for a different client), update the `@import` URL to load the alternative family alongside Geist. Do not change the locked Fractal AI brand tokens.

The previously bundled TTFs (Outfit-Bold, InstrumentSans, JetBrainsMono) are retired.

---

## OPENCLAW-SPECIFIC NOTES

- **Renderer**: `scripts/render.py` via the Mac's Python Playwright + managed Chromium (verified 2026-06-10; same engine as the `browser` skill). One-time fix if launch fails: `python3 -m playwright install chromium`. The old NODE_PATH/render.js dance from 2026-06-04 is obsolete on this runtime — `render.js` stays in scripts/ ONLY as the agent runtime-fork renderer for skill-translate syncs.
- **Preview tools EXIST here**: this runtime has the full `preview_*` toolset — use it for the editable gallery (rule 90) and for verification screenshots. The closed-loop Phase 4 evaluation remains the pixel-quality gate; preview is for interaction and proof.
- **Brand config**: Read from `brand-config.json` in this skill's directory (NOT a global `~/.claude/...` path).
- **Output delivery**: deliverables land under `~/projects/` (content piece's folder, or `projects/social-canvas-output/`); report clickable paths. No Discord/Telegram sends from this copy.
- **Tmp directory**: `/tmp/social-canvas/` for working files during generation ONLY — never the post-delivery source of truth (rule 92). `rm -rf` is blocked by destructive-guard — use `trash` / `mv ~/.Trash`.
- **Parity**: the agent fleet fork lives on the VPS and is kept aligned via `skill-translate` (Node renderer, Discord delivery, container paths over there). Every design rule, brand token, font choice, and quality-checklist item is identical across both. When updating either side, run `skill-translate` first.
