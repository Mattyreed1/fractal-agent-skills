# Closed-Loop Quality Checklist

Evaluate each rendered PNG against these 10 criteria. For each item, state **PASS** or **FAIL: {specific problem and fix}**.

Be concrete, not vague. Say "headline text clipped at right edge around 950px mark — reduce font-size from 72px to 64px or add word-break" NOT "looks a bit off."

---

## 1. TEXT LEGIBILITY
- All text large enough to read on mobile (body ≥ 24px, headlines ≥ 48px)
- Sufficient contrast between text and background (no light gray on white, no dark text on dark backgrounds)
- Text is crisp, not blurry (font loaded correctly, not fallback sans-serif)

## 2. TEXT CONTAINMENT
- No text cut off at any edge of the canvas
- All text sits within the safe zone boundary (60px from edges minimum)
- Long words or URLs don't overflow their containers

## 3. NO OVERLAPPING ELEMENTS
- No text overlaps other text
- No text overlaps decorative elements (shapes, lines, icons)
- No elements bleed into each other unintentionally

## 4. MARGINS AND SPACING
- Minimum 60px padding from all canvas edges (safe zone)
- At least 30px vertical spacing between distinct content blocks
- Consistent spacing rhythm throughout (no random gaps or cramped sections)

## 5. BRAND COLOR COMPLIANCE
- Background color matches brand config
- Text color matches brand config
- Accent/highlight colors match brand config
- No unexpected or off-brand colors appear

## 6. VISUAL HIERARCHY
- Clear primary element (largest, boldest — usually the headline)
- Secondary elements visually subordinate (subheads, supporting text)
- Eye flows in intended reading order (top→bottom for most formats)
- One focal point per slide, not competing elements

## 7. TYPOGRAPHY QUALITY
- No orphaned words (single word alone on last line of a text block)
- No awkward mid-phrase line breaks (e.g., "AI" on one line, "Agents" on the next when they're a compound term)
- Consistent font usage (heading font for headings, body font for body — no accidental mixing)
- Line height provides comfortable reading (1.3-1.6x font size)

## 8. CAROUSEL CONSISTENCY (multi-slide only)
- All slides use identical font sizes for equivalent elements
- Color scheme is the same across all slides
- Spacing patterns are consistent
- Slide numbers or progress indicators (if present) are in the same position
- Header/footer elements maintain position across slides

## 9. DECORATIVE BALANCE
- Decorative elements (lines, shapes, gradients) serve the design — they guide the eye or create structure
- Nothing feels random or tacked on
- Negative space is intentional, not accidental
- Decorative elements don't compete with content for attention

## 10. OVERALL POLISH
- The slide looks professional enough to post immediately
- Nothing screams "auto-generated" or "template"
- Design feels intentional and crafted, not default
- If you showed this to a designer, they wouldn't cringe

## 11. EDITABILITY GATE (Claude Code gallery — a script gate, not a visual judgment)
- Run `python3 scripts/check-editable.py /tmp/social-canvas`; it MUST return exit 0 ("all text editable").
- EVERY visible text node (headline, eyebrow, band labels, chips, diagram labels, footer note, captions) must carry `contenteditable="plaintext-only"` or sit inside an element that does. Spot-checking the headline is NOT enough — a non-editable `.band-label` ("Replaceable · swap anytime") and `.bottom-note` shipped 2026-06-17.
- Never declare the preview ready until this passes.

---

## Iteration Rules

- **Round 1**: Fix all FAIL items. Focus on structural issues (overflow, overlap, missing elements).
- **Round 2**: Fix remaining FAIL items. Focus on refinement (spacing, hierarchy, typography).
- **Round 3**: Final polish. Only fix items that meaningfully improve the output.
- **After Round 3**: Accept the result. Note any remaining issues to the user but don't loop further.
