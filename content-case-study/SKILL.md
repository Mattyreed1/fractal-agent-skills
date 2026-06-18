---
name: content-case-study
description: Stage 1-2 specialization of the Content Engine. Turns a REAL client engagement (a project folder + KG + meeting notes + metrics) into a structured case-study Content Context Brief — problem → before-state → system built → after-state → ONE quantified proprietary result → transferable lesson. This is the proof-of-work artifact at the center of the 2026 LinkedIn authority strategy (see projects/fractal-ai-content/2026-growth-strategy/). Use to turn a construction GC / a crypto OTC desk / a hospitality brand (or any client) into a publishable case study. Hook-agnostic — emits a brief that flows into content-hooks. Triggers — 'case study for', 'turn [client] into a case study', 'build the case study on', 'client teardown', 'content-case-study'.
license: MIT
metadata:
  version: 1.1.0
  created: 2026-06-15
  updated: 2026-06-17
  author: the Content Engine
  domains: ['content', 'case-study', 'client-work', 'authority']
  pipeline_stage: '1-2 (specialized entry; emits a brief consumable by content-hooks)'
---

# Content Case Study

Turns one real client engagement into a structured, publishable case-study brief. This is the **highest-authority content Fractal AI can produce** — reach-adjusted analysis of the user's own posts shows proof-of-work + a proprietary number is the moat, and generic AI-tooling content is the commodity to avoid. A case study is that proof-of-work in its purest form.

It sits inside the Content Engine as a specialized Stage 1-2: instead of diverging on angles (`content-ideation`) then gathering generic context (`content-brief`), it runs a fixed client→narrative transformation and emits a brief that `content-hooks` (Stage 3) consumes.

## Precondition: a REAL engagement with a REAL result

There must be an actual client engagement with an actual, quantifiable outcome. If there's no number, there's no case study — pick a different engagement or go get the number from the client. **Never fabricate a client, a number, or a result.** (HARD RULE territory — same as content-brief's "never fabricate case studies.")

## What this skill does NOT do

- Does NOT propose hooks, headlines, or post copy. The brief is hook-agnostic; `content-hooks` and `content-scripting` mine it later. A provocative framing of the result is an *angle*, not a hook — never populate the Notion `Hook` property.
- Does NOT invent metrics. Every number traces to the client's data, the user's records, the project folder, or a meeting transcript. Cite the source inline.
- Does NOT publish. Real client names + real numbers require **explicit client consent** before anything goes public (see Confidentiality gate). Default to anonymized framing until consent is confirmed.

## Inputs

- **Client + engagement** (required): e.g. "a construction GC / proposal-automation" or "a crypto OTC desk / desk automation". Maps to a `projects/<client>/` folder.
- **The ONE proprietary number** (required, or to be discovered in retrieval): the single headline result the case study is built around (e.g. "~2 hrs → minutes per proposal," "60% win rate," "22 nodes → 5"). One per piece — resist stacking three weak numbers.
- **Brand**: defaults to `fractal-ai` (case studies are agency proof). Confirm if ambiguous.
- **Confidentiality level**: `named` (client OK'd) or `anonymized` (default until OK'd) — "a multi-state GC," "a crypto OTC desk," etc.

If the engagement or number is missing, ask ONE question or fetch from the client folder. Don't proceed without a quantified result.

## Steps

### 1. Confirm the engagement + the headline number

Repeat back in one line:

> Case study I'm building: **{client/engagement}** — headline result: **"{the one proprietary number}"** — confidentiality: **{named | anonymized}**. Right?

If there's no quantified result yet, stop and get it (from the project folder, a meeting transcript, or the user/the client) before continuing.

### 2. Retrieval cascade (client-scoped)

Go wide on THIS client's footprint. Run in parallel where possible:

1. **Client project folder** — `ls projects/<client>/` and read the engagement subfolder (overview, briefs, audits, deliverables, screenshots, before/after artifacts, rate card). This is the primary source.
2. **Knowledge Graph** — `bash "$CLAUDE_PROJECT_DIR/scripts/kg-search.sh" "<client>"` → the client Org entity + connected people/projects + their `## Contact Log` (per KG CRM-v3, meetings live as Contact Log notes on the person/company, not as nodes).
3. **Notion — Meetings DB** — meetings with this client (transcripts, decisions, the moment the result landed). Run `notion` setup (fetch instructions page `<INSTRUCTIONS_PAGE_ID>`) first.
4. **Memory files** — grep `memory/` for decisions, wins, numbers tied to the client.
5. **Metrics / records** — any revenue, time-saved, win-rate, throughput numbers (Stripe records, the client's own reporting, the user's notes). Source each.
6. **Prior content** — grep `projects/fractal-ai-content/` for any earlier post about this client (avoid repetition; note the differentiation).
7. **Notion Case Studies DB** (`<CASE_STUDIES_DB_ID>`) — most builds already have an entry here (Company/Client + Summary + the documented outcome). Find this engagement's entry and **link it in the brief as the source of record**. Also capture the **Content DB page + live Post URL** of any earlier post on this client (for differentiation / reposts).

Pull every concrete artifact: the before-state numbers, the system architecture (named tools), screenshots, the after-state numbers, quotes from the client if any.

### 3. Write the case-study brief

Save to `projects/fractal-ai-content/YYYY-MM-DD-<client>-case-study/brief.md` (create the per-piece folder; all downstream artifacts live alongside it). Use this exact structure — it IS the case-study narrative:

```markdown
# Case Study Brief — {Client/engagement, named or anonymized}

**Date:** YYYY-MM-DD
**Type:** Case Study
**Brand:** Fractal AI
**Confidentiality:** {named — client OK'd | anonymized}
**Headline number (the one proprietary result):** {e.g. "~2 hrs → ~10 min per proposal"}
**AEC?:** {yes → frame via the AI-for-AEC lane | no → frame for the relevant industry}

## 1. Client & context
[Who they are (named or "a multi-state GC"), their industry, their scale. If AEC, say so — it activates the Lane B / AI-for-AEC framing and speaks to the 47%-AEC audience.]

## 2. The problem (before-state, QUANTIFIED)
[The operational pain, with a number. "Every proposal took ~2 hours of manual work" / "52% of rework traced to bad communication." The reader must feel the cost.]

## 3. What we built (the system)
[The actual solution — named tools, the architecture, the agents/automations. Specific enough to be credible and un-fakeable, not so deep it becomes a tutorial. This is the proof-of-work.]

## 4. The after-state + THE RESULT
[The outcome, anchored on the ONE proprietary number. Before vs after. "~2 hrs → ~10 min, ~60% win rate held." Source every number inline.]

## 5. The transferable lesson (what the reader STEALS)
[The single insight a non-client reader takes away — this is what makes it content, not a brag. E.g. "construction is an automation problem, not a software problem." Without this, it's a testimonial; with it, it's authority.]

## 6. Proof artifacts
- [screenshot / metric with source / the actual build / a client quote with attribution]

## 7. Confidentiality / consent status
- [ ] Client OK to use real name? {yes/no/pending}
- [ ] Client OK to use real numbers? {yes/no/pending}
- Anonymization plan if not: {how it reads without the name}

## 8. Visual suggestion (hook-agnostic)
[The before/after diagram, the system architecture, or the result-number card. Describe the substance; social-canvas / diagram-design render it. Note: per format analysis, "you presenting" video and hand-drawn/sketch styles over-index — a sketched before/after is a strong option.]

## 9. Lead magnet tie-in (optional)
[If this case study can hang a specific, novel give-away — a template, the actual skill, a checklist — name it. Specific assets out-perform vague ones.]

## Source links (REQUIRED — never omit)
- **Case Studies DB entry:** [Notion URL — the source of record]
- **Client project folder:** [repo path] · **Company KG entity:** [link]
- **Prior post on this client (if any):** [Content DB page URL] + live Post URL
- **Lead-magnet asset:** [GitHub / Notion landing / Gumroad URL, if any]

## Raw context
[Verbatim excerpts: meeting transcript snippets, KG entries, the project-folder source material, the records the numbers came from.]
```

### 4. Confidentiality gate (blocking before publish)

If any real client name or real number is `pending` consent, the piece can be **written and reviewed** but NOT published until consent is confirmed. Surface this explicitly. Default to an anonymized version the user can ship without waiting.

### 5. Push to Notion

Create a Content DB page (run `notion` setup first):
- **Type:** Case Study
- **Brand:** Fractal AI
- **Topic Pillar:** Client Work
- **Stage:** Idea (until the brief is approved → On Deck)
- Append the brief sections to the page body.

### 6. Submit + handoff

Post in chat: Notion URL, the headline number, confidentiality status, any `[NEEDS INPUT]` gaps, lead-magnet status. On approval → Stage `Idea → On Deck` → "Case study brief approved. Next: `content-hooks`."

## Strategy alignment (why this skill exists)

From `projects/fractal-ai-content/2026-growth-strategy/` (the data-backed 2026 plan):
- The decline was reach decay + drift to commodity AI-tooling content, not a writing problem. The fix is posting the **moat**: proof-of-work + one proprietary number.
- Case studies are the strongest buyer-facing + authority content, and the engine had no path to produce them — this skill is that path.
- **AEC clients → frame via the AI-for-AEC lane** (Lane B): "a real construction problem + the AI system that solved it, and I know it's real because I lived the problem." That intersection is the moat and serves the 47%-AEC audience without nostalgia.
- One proprietary number per piece. The transferable lesson is non-negotiable — it's what separates authority content from a testimonial.

## Edge cases

- **No quantified result** → stop; get the number or pick a different engagement. A case study without a number is a testimonial, not proof.
- **Client won't allow name/numbers** → anonymize (industry + scale + the number, no name). Still works.
- **Engagement is thin / early** → not yet a case study; revisit when there's a real outcome. Don't pad.
- **Client isn't AEC** (e.g. a crypto OTC desk/crypto, a hospitality brand/hospitality) → still works; frame for that industry. The AEC lane is a bonus when it applies, not a requirement.
- **Notion update fails** → keep the markdown; tell the user; don't retry silently.

## Handoff

Case-study brief approved → Stage=On Deck → invoke `content-hooks` (Stage 3). Can also be consumed standalone by `writing` (draft), `social-canvas` / `diagram-design` (before/after visual), `lead-magnet` (the tie-in asset).

## Multi-agent note

The content agent produces case studies in practice. This canonical skill lives in `~/.claude/skills/content-case-study/`. To run it on a remote agent fleet, stage a copy into that fleet's `skills/content-case-study/` directory and sync it with your own deployment tooling.
