---
name: frontend-design
description: Create distinctive, production-grade frontend interfaces with high design quality. Use this skill when the user asks to build web components, pages, or applications. Generates creative, polished code that avoids generic AI aesthetics. Bundles 19 review/refinement sub-commands (audit, critique, polish, distill, harden, optimize, animate, colorize, typeset, arrange, extract, adapt, delight, bolder, quieter, clarify, onboard, normalize, overdrive) invoked as arguments, e.g. "/frontend-design audit header".
argument-hint: "[command] [target] — e.g. 'audit header', 'polish checkout-form', or empty to build"
license: MIT + Apache 2.0 (Impeccable commands by pbakaus)
---

This skill guides creation of distinctive, production-grade frontend interfaces that avoid generic "AI slop" aesthetics. Implement real working code with exceptional attention to aesthetic details and creative choices.

## Context Gathering Protocol

Design skills produce generic output without project context. You MUST have confirmed design context before doing any design work.

**Required context** — every design skill needs at minimum:
- **Target audience**: Who uses this product and in what context?
- **Use cases**: What jobs are they trying to get done?
- **Brand personality/tone**: How should the interface feel?

**Gathering order:**
1. **Check current instructions (instant)**: If your loaded instructions already contain a **Design Context** section, proceed immediately.
2. **Check .impeccable.md (fast)**: If not in instructions, read `.impeccable.md` from the project root. If it exists and contains the required context, proceed.
3. **Ask the user**: If neither source has context, ask the user directly. Do NOT attempt to infer context from the codebase — code tells you what was built, not who it's for.

---

## Design Direction

Commit to a **refined, premium aesthetic** — Apple-inspired, minimal, sleek, and intuitive.

- **Purpose**: What problem does this interface solve? Who uses it?
- **Tone**: Premium, clean, elegant. Restraint over excess. Clarity over decoration.
- **Constraints**: Technical requirements (framework, performance, accessibility).
- **Differentiation**: What makes this UNFORGETTABLE? Focus on fluid motion, physics-based interactions, and meticulous attention to detail.

**CRITICAL**: Execute the minimalist direction with precision. A premium feel requires restraint, perfect alignment, and careful attention to spacing. Stay on brand — do not randomize aesthetics between generations.

Then implement working code (HTML/CSS/JS, React, Vue, etc.) that is:
- Production-grade and functional
- Visually striking through elegance and simplicity
- Cohesive with a clear premium point-of-view
- Meticulously refined in every detail

## Frontend Aesthetics Guidelines

### Typography
> *Consult [typography reference](reference/typography.md) for scales, pairing, and loading strategies.*

Utilize system fonts (`-apple-system`, `SF Pro Display`, `Inter`) to maintain a native, premium feel. Ensure strong hierarchy through weight and size rather than font variety.

**DO**: Use a modular type scale with clear size steps
**DO**: Vary font weights and sizes to create visual hierarchy
**DON'T**: Use overused generic fonts (Roboto, Arial, Open Sans) when personality matters
**DON'T**: Use monospace typography as lazy shorthand for "technical/developer" vibes
**DON'T**: Put large icons with rounded corners above every heading — they make sites look templated

### Color & Theme
> *Consult [color reference](reference/color-and-contrast.md) for OKLCH, palettes, and dark mode.*

Commit to a cohesive, sophisticated palette. Use ample white/negative space. Rely on subtle grays, stark contrasts, and occasionally vibrant but controlled accent colors.

**DO**: Use modern CSS color functions (oklch, color-mix, light-dark) for maintainable palettes
**DO**: Tint neutrals toward your brand hue for subconscious cohesion
**DON'T**: Use gray text on colored backgrounds — use a shade of the background color instead
**DON'T**: Use the AI color palette: cyan-on-dark, purple-to-blue gradients, neon accents on dark backgrounds
**DON'T**: Use gradient text for "impact" — especially on metrics or headings
**DON'T**: Default to dark mode with glowing accents — it looks "cool" without requiring actual design decisions

### Layout & Space
> *Consult [spatial reference](reference/spatial-design.md) for grids, rhythm, and container queries.*

Grid-based layouts. Generous negative space. Center-aligned elements or strong, clear structural alignments.

**DO**: Create visual rhythm through varied spacing — tight groupings, generous separations
**DO**: Use fluid spacing with clamp() that breathes on larger screens
**DON'T**: Wrap everything in cards — not everything needs a container
**DON'T**: Nest cards inside cards — visual noise, flatten the hierarchy
**DON'T**: Use identical card grids — same-sized cards with icon + heading + text, repeated endlessly
**DON'T**: Use the hero metric layout template — big number, small label, supporting stats, gradient accent
**DON'T**: Use the same spacing everywhere — without rhythm, layouts feel monotonous

### Visual Details
**DO**: Use subtle visual cues — "liquid glass" effects (refraction, blur), soft layered shadows, subtle noise/grain for texture
**DO**: Elevate standard components with premium finishes (squircles, backdrop blurs, refined shadows)
**DON'T**: Use glassmorphism everywhere — blur effects, glass cards, glow borders used decoratively rather than purposefully
**DON'T**: Use rounded elements with thick colored border on one side — lazy accent that never looks intentional
**DON'T**: Use sparklines as decoration — tiny charts that look sophisticated but convey nothing
**DON'T**: Use rounded rectangles with generic drop shadows — safe, forgettable, could be any AI output
**DON'T**: Use modals unless there's truly no better alternative

### Motion
> *Consult [motion reference](reference/motion-design.md) for timing, easing, and reduced motion.*

Prioritize physics-based motion (springs) over linear transitions. Focus on high-impact scrolling experiences, staggered reveals, and smooth interactions.

**DO**: Use exponential easing (ease-out-quart/quint/expo) for natural deceleration
**DO**: For height animations, use grid-template-rows transitions instead of animating height directly
**DO**: Use spring physics (Framer Motion, GSAP) for interactive motion
**DON'T**: Animate layout properties (width, height, padding, margin) — use transform and opacity only
**DON'T**: Use bounce or elastic easing — they feel dated and tacky; real objects decelerate smoothly

### Interaction
> *Consult [interaction reference](reference/interaction-design.md) for forms, focus, and loading patterns.*

Make interactions feel fast. Use optimistic UI — update immediately, sync later.

**DO**: Use progressive disclosure — start simple, reveal sophistication through interaction
**DO**: Design empty states that teach the interface, not just say "nothing here"
**DON'T**: Repeat the same information — redundant headers, intros that restate the heading
**DON'T**: Make every button primary — use ghost buttons, text links, secondary styles; hierarchy matters

### Responsive
> *Consult [responsive reference](reference/responsive-design.md) for mobile-first, fluid design, and container queries.*

**DO**: Use container queries (@container) for component-level responsiveness
**DO**: Adapt the interface for different contexts — don't just shrink it
**DON'T**: Hide critical functionality on mobile — adapt the interface, don't amputate it

### UX Writing
> *Consult [ux-writing reference](reference/ux-writing.md) for labels, errors, and empty states.*

**DO**: Make every word earn its place
**DON'T**: Repeat information users can already see

---

## The AI Slop Test

**Critical quality check**: If you showed this interface to someone and said "AI made this," would they believe you immediately? If yes, that's the problem.

Review the DON'T guidelines above — they are the fingerprints of generic AI-generated work.

---

## Apple Style Frontend Implementation

When the user specifically requests an "Apple Style" aesthetic or premium tech feel, strictly follow these implementation patterns:

**1. Aesthetics & Interface Elements**
- **Clarity, Deference, Depth**: Prioritize high-impact typography, generous white space, and high-quality imagery.
- **Typography**: Use Apple's system font stack (`SF Pro Display`, `SF Pro Text`, or `-apple-system, BlinkMacSystemFont`, `Inter`).
- **Shapes**: Emulate "squircles" (superellipses) using SVG masks or intricate `clip-path` properties rather than standard `border-radius`.
- **Lighting & Shadows**: Use layered, highly diffused shadows to simulate realistic depth rather than harsh offsets.

**2. "Liquid Glass" Effect & Shaders**
- **CSS Approximation**: Use `backdrop-filter: blur(20px) saturate(150%)` mixed with a minimal semi-transparent background and a thin inner border.
- **Advanced (WebGL/Shaders)**: For true realism, implement WebGL shaders (via raw WebGL, React Three Fiber, or liquidGL). Utilize Framebuffers to render the background, pass it to a custom fragment shader, and compute mathematical SDF distortion, real-time light refraction, and chromatic dispersion (splitting R, G, B channels at the edges).

**3. Organic Smooth Transitions & Spring Physics**
- **CSS Transitions**: Rely on snappy custom cubic-bezier curves (e.g., `cubic-bezier(0.16, 1, 0.3, 1)`).
- **JS Spring Physics**: Use engines like Framer Motion (`type: "spring"`) or GSAP to handle interactive motion dynamically every frame.

**4. Scroll Interactions & Storytelling**
- **Scroll Scrubbing**: Use GSAP ScrollTrigger's `scrub` property to bind animation timelines directly to the scrollbar position.
- **Pinned Sections**: Pin layout containers to the viewport while internal contents change dynamically.
- **Canvas Image Sequences**: Recreate the "AirPods Effect" by extracting 3D animations into high-res flat frames, rendering them to a `<canvas>`, and updating the frame index via scroll position.

---

## Sub-Commands (argument routing)

This skill bundles 19 review/refinement commands as files in [`commands/`](commands/). They are invoked **as arguments to this skill** — `/frontend-design audit header`, `/frontend-design polish checkout-form` — or by name in conversation ("run the frontend audit on the header").

**Routing rule:** when the skill is invoked with arguments and the first word matches a command below, READ `commands/<word>.md` and execute it against the rest of the arguments as the target. The command files assume this skill's design foundation is already in context.

| Command | Purpose |
|---------|---------|
| `audit` | Technical quality checks (a11y, performance, responsive, anti-patterns) |
| `critique` | UX design review: hierarchy, clarity, emotional resonance |
| `polish` | Final pass before shipping: alignment, spacing, consistency |
| `distill` | Strip to essence — remove unnecessary complexity |
| `harden` | Error handling, i18n, text overflow, edge cases |
| `optimize` | Performance: loading, rendering, animations, bundle size |
| `animate` | Add purposeful motion and micro-interactions |
| `colorize` | Introduce strategic color to monochromatic designs |
| `typeset` | Fix font choices, hierarchy, sizing, weight consistency |
| `arrange` | Fix layout, spacing, visual rhythm |
| `extract` | Pull reusable components into design system |
| `adapt` | Adapt for different devices/contexts |
| `delight` | Add moments of joy and personality |
| `bolder` | Amplify boring/timid designs |
| `quieter` | Tone down overly bold designs |
| `clarify` | Improve unclear UX copy |
| `onboard` | Design onboarding flows |
| `normalize` | Align with design system standards |
| `overdrive` | Add technically extraordinary effects |

All commands use THIS skill as their design foundation — your premium aesthetic, not random bold directions.

---

Remember: You are capable of extraordinary creative work. Don't hold back — show what can truly be created when thinking outside the box and committing fully to a distinctive vision.
