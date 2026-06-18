# Founder Story — Phase 0.5: Source Gathering (REQUIRED before scripting)

_Founder Stories are carried by REAL artifacts (the visual rule in storytelling.md / founder-stories.md). So before you script, you gather the real sources: footage of the founder on camera, verbatim quotes, revenue screenshots, blog passages. This step produces a `sources.md` dossier the scripting step drafts from, and it enforces data-honesty — every stat the script uses must trace to a real source gathered here. First run: the Pieter Levels video. Worked example: `projects/founder-freedom-content/2026-06-08-pieter-levels-one-person-empire/sources.md`._

## When
After packaging is locked (thesis / title / thumbnail), BEFORE outlining or scripting the body. Personal Journeys do NOT need this (carried by the user's own metaphor world + lived experience). **Founder Stories REQUIRE it.**

## Output
`projects/founder-freedom-content/<slug>/sources.md` — three research sections + a corrections list + (usually) a key-creative-insight callout. Template at the bottom.

## Run the 3 passes in PARALLEL (independent → fan out as background agents)
Spawn three background subagents (Agent tool, `model: sonnet`, `run_in_background: true`), one per pass. Each MUST: use real tools, NEVER fabricate a URL / quote / number, flag anything unverified, and return ONE clean markdown dossier section. Then YOU assemble + reconcile.

### Pass 1 — Videos & Podcasts ← THE PRIORITY (footage of the founder on camera)
Real-artifacts Founder Stories live on footage of the founder, so this pass matters most. Tools: WebSearch + `yt-video-report` (Apify transcripts) + Perplexity. Find + rank on-camera sources (long interviews, podcasts, conference talks, the founder's own channel); pull transcripts of the top 2-3 for exact quotes + timestamps.

### Pass 2 — Facts & Timeline (verify every number)
Tools: `research` skill / Perplexity (`search` + `reason`; AVOID `deep_research` — it stalls) + WebSearch. Verify or correct every specific claim the packaging/draft makes; return a verdict table + corrections list. Never invent a number.

### Pass 3 — Tweets & Blogs (primary-source artifacts)
Tools: `scrape` skill (X via xAI API; firecrawl/web for blogs). Pull verbatim posts + key blog passages + any book/landing page. Flag paraphrased vs verbatim; drop the unverifiable.

## VERIFICATION GATE — confirm every on-screen quote/stat against the RAW primary source (HARD)
Secondary pages, search snippets, and Perplexity/agent renderings PARAPHRASE. So after the 3 passes, before anything goes on screen, pull the RAW source and confirm it verbatim. **Nothing at "medium confidence" ships, and this is the skill's job — never the user's.**

Per source type:
- **YouTube video → raw transcript.** Prefer the official transcript (e.g. `lexfridman.com/<guest>-transcript`); else the video captions via `yt-video-report` / Apify. Proven method:
  ```bash
  curl -sL "<transcript-url>" | sed -e 's/<[^>]*>/ /g' > /tmp/t.txt
  # LC_ALL=C makes '.' match bytes, avoiding the UTF-8 regex-complexity error that ugrep throws on .{0,N}
  LC_ALL=C grep -io ".\{0,50\}<distinctive phrase>.\{0,90\}" /tmp/t.txt
  ```
  Confirm exact wording; grab the timestamp.
- **X / tweet → fetch the exact tweet** by URL via the `scrape` skill (xAI API). Confirm verbatim text + date.
- **Substack / blog / essay → `firecrawl_scrape`** (or `scrape` skill) on the post URL; confirm the passage verbatim.
- **Audio-only podcast →** official transcript if published; else mark lower-fidelity and prefer to paraphrase as narration.

Rules:
- Every on-screen quote is VERBATIM from the raw source, with URL + timestamp in `sources.md`, marked **"verified (raw)"**.
- Raw source beats every secondary claim — if they conflict, fix to the raw source and note it.
- A quote you can't confirm verbatim does NOT go on screen: paraphrase it as narration, or cut it.

## Assemble + RECONCILE (your job, not the agents')
1. Paste the three sections into `sources.md` (template below).
2. **Cross-check the passes against each other — they WILL sometimes conflict.** (First run: the facts pass claimed a 2013 date that a direct blog scrape contradicted as 2014; the scrape won.) Rule: **a direct scrape of the PRIMARY source beats a secondary citation.** Resolve every conflict and note the resolution. Never trust a single pass.
3. Write "### Script corrections to apply" — every place the packaging/draft is wrong or overstated, with the fix.
4. Add a "🎯 KEY CREATIVE INSIGHT" callout if a pass surfaced a non-obvious angle. This is often the richest output (Pass 1 found Levels' "constraints make you happy / I'm free, therefore I'm lost" reframe — the thing that made the video non-generic). Hunt for it.
5. **Run the VERIFICATION GATE (above) on every quote/stat destined for screen.** Nothing ships unverified — pull the raw transcript/tweet/essay and confirm verbatim yourself. Don't hand a "verify this" residual to the user.

## Feed it into the script
- Every `[VERIFY]` in the draft must resolve to a real source here, or get cut.
- Map specific real artifacts to each beat in the visual plan: which video + timestamp, which tweet screenshot, which blog passage. "Real artifacts carry it" becomes concrete here.
- Keep a FACT-CHECK table in the script for residual items to confirm against raw primary sources before recording (e.g. a quote pulled from a transcript page, not the raw transcript).

## Dossier template
```markdown
# {Founder} — Sources Dossier
_For the "{video}" Founder Story. 3-pass sourcing, {date}._
**Status:** facts ⏳ · videos ⏳ · tweets/blogs ⏳

## Verified Facts & Timeline        (Pass 2)
| # | Claim | Verdict | Real figure | Source + date | Confidence |
### Script corrections to apply

## Videos & Podcasts                 (Pass 1)
🎯 KEY CREATIVE INSIGHT — …
### Ranked sources (on-camera prioritized)
### Key quotes (verbatim + source + timestamp)
### Couldn't verify

## Tweets & Blog Artifacts           (Pass 3)
### A) Tweets   ### B) Blogs   ### C) Book/landing
### Paraphrased / unverified
```

## Agent-prompt templates (replace {FOUNDER} and {@HANDLE}, then fan out the three in one message)

**Pass 1 — Videos & Podcasts:**
> You are sourcing REAL video and podcast material of {FOUNDER} ({@HANDLE}) for a Founder Freedom "Founder Story" video built from REAL footage of the founder, so finding the actual videos that show {FOUNDER} on camera is the HIGHEST priority. Use WebSearch heavily; use the yt-video-report skill (Apify) for transcripts; you may use Perplexity. CRITICAL: never fabricate URLs, dates, episode numbers, or quotes — every link must be real; mark anything uncertain. Find + rank the best video/podcast sources where {FOUNDER} appears or speaks, prioritizing real on-camera footage (long interviews, podcasts, conference talks, their own channel). For EACH: title · show/host · date · URL · length · on-camera? · topics · 3-6 verbatim quotes with approximate timestamps on the founder's core themes. Then pull transcripts of the top 2-3 (richest long interview first) and extract exact quotes + timestamps. Final message = a clean markdown section "## Videos & Podcasts" (ranked table, then "### Key quotes (verbatim, source + timestamp)", then "### Couldn't verify"). Return ONLY that section, self-contained and accurate.

**Pass 2 — Facts & Timeline:**
> You are fact-checking a Founder Freedom "Founder Story" about {FOUNDER} ({@HANDLE}). Use the research skill / Perplexity (search + reason; AVOID deep_research — it times out) + WebSearch. Every fact needs a real source URL + a confidence level; never fabricate — mark UNVERIFIED + best estimate if unsure. Verify or correct each specific claim the packaging and draft make about {FOUNDER}: dates, timeline, revenue/figures, team & funding status, tech/approach, key milestones, plus 2-3 verbatim philosophy quotes with sources. Final message = a clean markdown section "## Verified Facts & Timeline" (table: Claim | Verdict confirmed/corrected/unverified | Real figure | Source URL+date | Confidence) + "### Notes / corrections for the script". Accuracy over completeness; never invent a number. Return ONLY that section.

**Pass 3 — Tweets & Blogs:**
> You are pulling REAL primary-source artifacts from {FOUNDER} ({@HANDLE}) for a Founder Freedom video that puts real screenshots/tweets on screen. Use the scrape skill (X via xAI API for tweets; firecrawl/web for blogs); fall back to WebSearch + firecrawl if needed. CRITICAL: every artifact needs a real URL + VERBATIM text; never fabricate — label paraphrases clearly; drop anything you can't verify. Pull: A) 8-12 notable {@HANDLE} tweets/posts (verbatim + URL + date) on the founder's signature themes; B) key blog posts (URL + 3-5 verbatim passages each); C) any book/landing page (URL + core premise in their words). Final message = a clean markdown section "## Tweets & Blog Artifacts" (A Tweets / B Blogs / C Book) + "### Paraphrased / unverified". Return ONLY that section.

---
**One-line positioning:** Founder Stories are carried by real artifacts, so you gather the artifacts before you write. Three parallel passes (video+podcast / facts / tweets+blogs) → one reconciled `sources.md` → a script where every claim traces to a real source and every beat has real footage behind it.
