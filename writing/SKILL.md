---
name: writing
description: Expert writing assistant trained in proven frameworks for headlines, hooks, intros, blog structure, formatting, and rhythm. Use for any content creation task.
---

# Writing Skills

This is your comprehensive writing assistant, trained in proven frameworks and techniques for creating compelling content across all formats.

## When to Use This Skill

Use this skill when you need help with:
- Writing compelling headlines that drive clicks
- Creating attention-grabbing hooks and openers
- Structuring blog posts and long-form content
- Formatting content for maximum readability
- Developing effective introductions with credibility
- Crafting social media content (especially X/Twitter and LinkedIn)
- Writing LinkedIn posts, carousels, and thought leadership content
- Building writing rhythm and flow
- Picking and applying a proven storytelling format

## Skill Layout

```
writing/
├── SKILL.md          ← this file (router)
├── references/       ← doctrine — load when applying a framework
│   ├── headlines.md
│   ├── hooks.md
│   ├── intros.md
│   ├── outlines.md
│   ├── blogs.md
│   ├── x-twitter.md
│   ├── linkedin.md
│   └── storytelling.md
└── examples/         ← complete worked example posts (for storytelling formats)
    ├── 01-heros-journey.md
    ├── 02-personal-learning.md
    ├── 03-about-me.md
    ├── 04-before-after.md
    ├── 05-goal-dream-journey.md
    ├── 06-challenge.md
    ├── 07-win.md
    ├── 08-day-in-the-life.md
    ├── 09-personal-update.md
    └── 10-lesson-from-others.md
```

## Reference Docs (`references/`)

Each file is the doctrine for one writing dimension. Load the matching file when working on that dimension.

### 1. [Headlines](./references/headlines.md)
Write compelling headlines using proven formulas and archetypes that capture attention and make readers want to click.

### 2. [Hooks](./references/hooks.md)
Create effective single-sentence openers using 6 proven techniques to immediately grab reader attention.

### 3. [Intros](./references/intros.md)
Build credible introductions that establish trust and use rhythm patterns (1/3/1) to engage readers.

### 4. [Outlines](./references/outlines.md)
Structure blog posts and long-form content with clear organization, mirroring techniques, and the 5 pieces of effective formatting.

### 5. [Blogs](./references/blogs.md)
Master blog formatting with subheads, writing rhythms (1/3/1, 1/5/1, rhythm pyramids), and visual structure.

### 6. [X-Twitter](./references/x-twitter.md)
Create viral X/Twitter content with proven hook templates, thread structures, and compelling CTAs.

### 7. [LinkedIn](./references/linkedin.md)
Write high-engagement LinkedIn posts, carousels, and thought leadership content. Covers hook formulas, algorithm mechanics, formatting rules, post types, content pillars, and engagement strategy. **Use this file for all LinkedIn writing tasks.**

### 8. [Storytelling](./references/storytelling.md)
10 medium-agnostic storytelling formats (Hero's Journey, Personal Learning/Epiphany, About Me, Before and After, Goal/Dream Journey, Challenge, Win, Day In The Life, Personal Update, Lesson From Others) — each with description, strategy, secret sauce, and plug-and-play mad-lib templates. The verbatim source is from Short Form Academy (Kallaway), but the file opens with a cross-medium translation table so the formats apply to **LinkedIn posts, X threads, blog intros, case studies, email sequences, sales pages, About pages, podcast openings, keynote talks, and video scripts** — not just short-form video. Each format points to a complete worked example in `examples/`. Use this file whenever a piece of content needs a proven narrative arc; pick the format from the "Pick the right format for the job" table near the top.

## Worked Examples (`examples/`)

`examples/` holds **complete, fully-written posts** — one per storytelling format — that show what the mad-lib templates look like populated with realistic content. Always read the matching example file when drafting in one of the 10 formats; the templates alone are abstract, the worked example shows the rhythm.

**Note on scope.** `examples/` is reserved for full-length deliverables (a complete LinkedIn post, a complete short-form script, etc.). Inline mini-examples — single illustrative headlines, hook one-liners, paragraph snippets — stay inline in the `references/` files where they're contextually needed.

## Core Writing Principles

### Clarity Over Cleverness
Always be clear, not clever. Clever headlines and openers confuse readers more than they hook them.

### Make a Promise
Your headline and intro must make a clear promise to the reader about what they'll gain.

### Be Specific
Specificity builds trust. Vague writing confuses and loses readers.

### Take a Stance
Polarizing content resonates. Write for someone, not everyone.

### Create Curiosity Gaps
Tease the ending without revealing the answer. Make readers click to fill in the middle.

### Use Patterns and Rhythm
Readers love patterns. Use writing rhythms like 1/3/1, mirroring, and visual symmetry.

## How to Use These Skills

1. **For a complete piece**: Start with `references/headlines.md` to craft your title, then `references/hooks.md` for your opener, `references/intros.md` to establish credibility, `references/outlines.md` to structure your piece, and `references/blogs.md` to format beautifully.

2. **For quick content**: Use `references/x-twitter.md` for X/Twitter posts, `references/linkedin.md` for LinkedIn posts, or `references/hooks.md` for any short-form opener.

3. **For editing**: Use `references/blogs.md` to improve rhythm and formatting, or `references/outlines.md` to fix structure.

4. **For LinkedIn**: Always use `references/linkedin.md` — it has platform-specific rules for hooks, formatting, algorithm mechanics, and engagement strategy that differ significantly from other platforms.

5. **For narrative-driven content**: Pick a format from `references/storytelling.md`, then read the matching `examples/NN-*.md` to see the rhythm before drafting.

## Quick Reference

- **Need a headline?** → [references/headlines.md](./references/headlines.md) — 25 proven formulas
- **Need an opener?** → [references/hooks.md](./references/hooks.md) — 6 proven openers
- **Need credibility?** → [references/intros.md](./references/intros.md) — personal vs borrowed credibility
- **Need structure?** → [references/outlines.md](./references/outlines.md) — 5-piece formatting system
- **Need rhythm?** → [references/blogs.md](./references/blogs.md) — 1/3/1, 1/5/1, pyramids
- **Need viral content?** → [references/x-twitter.md](./references/x-twitter.md) — proven hook templates
- **Need LinkedIn content?** → [references/linkedin.md](./references/linkedin.md) — hooks, algorithm, formatting, post types
- **Need a story structure?** → [references/storytelling.md](./references/storytelling.md) — 10 narrative arcs + cross-medium translation, with worked examples in [`examples/`](./examples/)
- **Hooks graded against performance data / audience rubric** → `hook-machine` skill
- **Need a long-form YouTube video script?** → use the dedicated [`youtube-script`](../youtube-script/SKILL.md) skill (Founder Freedom: Personal Journey + Founder Story formats, voice, 2026 retention/packaging). This `writing` skill has no video reference by design.

## Anti-AI-Slop Rules (CRITICAL)

**NEVER use these generic AI patterns that scream "bot-written":**

### BANNED: "It's not just X, it's Y" pattern
- "It's not just about technology. It's about observation."
- "This isn't just a strategy. It's a mindset."
- "It's not about the tools. It's about the process."

### BANNED: "Here's why" followed by a colon
- "Here's why:" (as its own line)
- Use direct statements instead

### BANNED: "The truth is..." opener
- Overused AI filler phrase
- State the truth directly instead

### BANNED: Excessive use of em dashes (—)
- Maximum 1-2 per essay, if at all
- Use periods and commas instead

### BANNED: "Let me explain" / "Let's dive in"
- Just explain it. Don't announce you're explaining.

### BANNED: Starting paragraphs with "And..."
- "And that's when everything changed."
- Use natural transitions instead

### BANNED: Generic conclusions
- "The bottom line?"
- "The lesson here?"
- Be more specific and genuine

### BANNED: Reflexive analogies (the AI "go-to" comparisons)
The first analogy that comes to mind is the one every AI reaches for. Ban these on sight:
- "It's like hiring a brilliant new employee/intern who just showed up on day one..."
- "Imagine a world where..."
- "Think of it like a Swiss Army knife / a recipe / an orchestra conductor..."
- "the secret sauce," "the special ingredient"
If you use an analogy it must be specific to THIS topic and literally true. A comparison that could bolt onto any subject is slop. Prefer real, named examples over an invented comparison. (Learned 2026-06-14: opened an explainer with "a brilliant new hire, useless to you" — a cliché AND false.)

### BANNED: Fabricated anecdotes or claims about the author
NEVER invent a first-person story, anecdote, or factual claim about the author (what they run, built, felt, said, or how they work). Putting invented words in the author's mouth is the worst failure mode: it reads as authentic and it is a lie. If a story would strengthen the piece, use ONLY what the author actually told you or what you can verify. If you don't have it, ask, or make the point without a story. "Use your storytelling skills" never means "make up a story." (Learned 2026-06-14: fabricated a first-person narrative about how the author runs his AI.)

### BANNED: Overclaiming for effect
Do not exaggerate to make a line hit harder. "useless," "nobody," "everyone," "impossible," "always," "never," "broken" must be literally true or cut. A raw model is not "useless"; "almost nobody" is more honest than "nobody." An overclaim the reader can falsify destroys the whole post's credibility. Accuracy beats punch.

### DO THIS INSTEAD
- **Understand the subject before writing a word.** State the core idea in one sentence and check it against the source. If you can't, you don't understand it well enough to explain it. (On an explainer, a wrong concept is unsalvageable by polish.)
- Use direct, confident statements
- Write like a professional having a conversation
- Vary sentence structure naturally
- Be specific, not generic
- Anchor abstractions with real, named, true examples, not invented analogies
- Show, don't tell

## Usage Notes

When you invoke this skill or any of the sub-skills, you should:
1. Ask for the necessary context (topic, audience, goal, word count)
2. Apply the relevant frameworks from the appropriate `references/` file
3. For storytelling formats, read the matching `examples/NN-*.md` file before drafting
4. Generate multiple options when possible
5. Always prioritize clarity and specificity over cleverness
6. **STRICTLY AVOID all patterns listed in Anti-AI-Slop Rules**
