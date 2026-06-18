---
name: lead-magnet
description: >
  Turns conversations, frameworks, and expertise into downloadable lead magnets
  (workflows, checklists, skills, guides, Notion DBs) plus companion LinkedIn posts.
  Extracts insights, selects the right format, builds the artifact, and chains to
  writing and notion skills for polish and storage.
license: MIT
model: claude-opus-4-5-20251101
metadata:
  version: 1.0.0
  author: the user
  category: lead-generation
  tags: [lead-magnet, linkedin, writing, notion, content]
---

# Lead Magnet Builder

Turns any conversation, framework, or expertise into a functional lead magnet and a companion LinkedIn post. A 4-phase pipeline: extract insights, classify the best format, build the artifact, then deliver through writing polish and Notion storage.

Base directory: this skill's directory.

## Triggers

- `Create a lead magnet from this` — full pipeline or lead-magnet-only, depending on intake
- `Build a lead magnet for this post` — Path A: post already written, just build the artifact
- `I have a post, now I need the lead magnet` — Path A
- `Turn this into a lead magnet` — Path B: raw inputs, build post + artifact
- `Extract insights from this` — Path B, Phase 1 only
- `What lead magnets can I get from this?` — Path B, Phases 1-2 only

## Quick Reference

| Path | Starting Point | Output |
|------|---------------|--------|
| A — Lead Magnet Only | Post already written | Lead magnet artifact + updated post CTA |
| B — Full Pipeline | Raw inputs (notes, conversation, framework) | LinkedIn post + lead magnet artifact |

| Route | Phases |
|-------|--------|
| Path A: Lead Magnet Only | Intake → Transform (artifact) → Deliver |
| Path B: Full Pipeline | Intake → Extract → Classify → Transform (post + artifact) → Deliver |
| Path B: Insight audit only | Intake → Extract → Classify (stop, present options) |

## Process

### Intake: Decision Tree + Clarifying Questions

**Step 1 — Route the request.**

Ask the user one question before doing anything else:

> "Do you have a LinkedIn post already written, or are we starting from raw material?"

```
Do you have a LinkedIn post already written?
│
├── YES → PATH A: Lead Magnet Only
│         Skip to Phase 3 (Transform)
│         Build the artifact only
│         Polish post CTA if needed
│
└── NO  → PATH B: Full Pipeline
          Run Phase 1 (Extract) → Phase 2 (Classify)
          → Phase 3 (Transform: post + artifact)
          → Phase 4 (Deliver)
```

If it's unclear which path applies, ask. Do not assume.

---

**Step 2 — Gather context before proceeding.**

Once the path is confirmed, ask any of the following that aren't already clear from what the user provided. Ask them all at once in a single message — do not ask one at a time.

**Path A — clarifying questions:**
1. Can you paste the LinkedIn post? (if not already provided)
2. Do you have a lead magnet format in mind, or should I recommend one based on the post?
3. Who is the target audience for this lead magnet?
4. Is there anything you want to make sure is included or excluded?

**Path B — clarifying questions:**
1. What's the raw material? (paste it, or describe what you've built/learned)
2. What's the goal of the lead magnet — capture emails, drive DMs, establish authority, or something else?
3. Who is the target audience?
4. Do you have a format in mind (workflow, checklist, guide, skill, Notion DB), or should I recommend one?
5. Any constraints — things to avoid, length preferences, or platforms beyond LinkedIn?

**Skip any question that's already answered.** If the user has provided clear material and context, proceed without interrogating them. The goal is to fill genuine gaps, not to ask questions for the sake of it.

Do not proceed to Phase 1 (or Phase 3 for Path A) until you have enough to work with.

---

### Phase 1: EXTRACT
*(Path B only — skip if Path A)*

Mine the source material for publishable insights using the [Insight Taxonomy](references/insight-taxonomy.md).

1. **Accept input** - Conversation transcript, session notes, links, or pasted context. Ask the user what to process if unclear.
2. **Scan for 7 insight types** - Framework, Contrarian Take, Aha Moment, War Story, Data Point, Tool/Tactic, Principle. Use detection heuristics from the taxonomy.
3. **Score content gravity** - Rate each insight 1-5 on standalone content value.
4. **Flag lead magnet candidates** - If the source contains a workflow pattern, structured collection, repeatable process, sequential steps, or deep framework — flag it.
5. **Output the Insight Map** - Present all extracted insights in the taxonomy format.

**Gate:** Minimum 3 insights extracted, 2+ types represented, at least 1 with gravity >= 4. If not met, tell the user the source lacks enough publishable material.

### Phase 2: CLASSIFY
*(Path B only — skip if Path A)*

Score insights against output formats using the [Format Selection Guide](references/format-selection-guide.md).

1. **Run the decision tree** - Check for workflow patterns, structured collections, agent processes, sequential processes, deep frameworks, or standalone social content.
2. **Score each candidate format** - Rate 1-5 on insight fit, audience value, buildability, and promotability. Only recommend formats scoring >= 3 on ALL criteria.
3. **Present ranked recommendations** - Show 1-3 output options with reasoning tied to specific insight numbers.
4. **Apply companion post rule** - Every lead magnet recommendation MUST include a companion LinkedIn post.

**Gate:** User confirms which format(s) to produce before proceeding to Phase 3.

### Phase 3: TRANSFORM

Build structured drafts using brand profile and templates.

1. **Load brand profile** - Fetch the Notion brand doc at page `<LEADS_DB_ID>` (canonical). If a local cache exists at `assets/profiles/default.md` (or user-specified), use it instead.
2. **Load the template** - Select from `assets/templates/` based on the confirmed format:
   - LinkedIn post → [linkedin-post.md](assets/templates/linkedin-post.md)
   - n8n workflow lead magnet → [lead-magnet-workflow.md](assets/templates/lead-magnet-workflow.md)
   - Notion resource DB → [lead-magnet-notion-db.md](assets/templates/lead-magnet-notion-db.md)
   - Claude Code skill → [lead-magnet-skill.md](assets/templates/lead-magnet-skill.md)
   - Checklist/cheat sheet → [lead-magnet-checklist.md](assets/templates/lead-magnet-checklist.md)
   - Mini-guide → [lead-magnet-mini-guide.md](assets/templates/lead-magnet-mini-guide.md)
3. **Build the lead magnet artifact** - Follow the template skeleton, inject insights (Path B) or extract topic/structure from the existing post (Path A), apply brand voice.
4. **Path B only: also draft the companion LinkedIn post** - Use the LinkedIn post template with CTA driving to the lead magnet.
   **Path A only: review the existing post's CTA** - Check if it references the lead magnet clearly. If the CTA is missing or weak, suggest an updated version. Do not rewrite the whole post unless asked.
5. **Self-check** - Scan for anti-slop violations (no "unlock/supercharge/game-changer", no generic AI phrasing). Verify specific numbers, names, and outcomes are preserved from source.

**Gate:** Structured draft(s) ready for polish. Each draft has metadata (content type, format, pillar, source insights).

### Phase 4: DELIVER

Polish, review, and save. Follow the [Integration Handoffs](references/integration-handoffs.md) chain.

1. **Chain to writing skill** - ALWAYS invoke using `Skill` tool with `skill: "writing"`.
   - **Path B:** Pass the full post draft for hook optimization, headline options, rhythm check, and anti-slop verification.
   - **Path A:** Pass the existing post to check whether it effectively promotes the lead magnet. If edits are needed, the writing skill makes them. If the post is already strong, it confirms it's clean before saving.
2. **Present to user** - Show the polished draft for approval or edits. If rejected, return to Phase 3 with feedback.
3. **Save to Notion** - On approval:
   - FIRST: Fetch Notion instructions page `<INSTRUCTIONS_PAGE_ID>` (mandatory, non-negotiable)
   - Save to Content DB (`<CONTENT_DB_ID>`) with Draft status
   - Use `mcp__mr-notion__*` tools for all Notion operations
4. **Create artifact** (lead magnets only):
   - Workflow → Chain to `n8n` skill for validation, create workflow JSON
   - Notion DB → Define schema and create duplicatable template
   - Agent skill → Build skill directory structure (SKILL.md + references)
   - Checklist/Mini-guide → Format final markdown
5. **Return summary** - Notion page URL + artifact location + what was created

**Gate:** Writing skill was invoked (not skipped), user approved, Notion instructions fetched before save, content saved with proper properties, lead magnets have both artifact AND companion post.

## Anti-Patterns

| Avoid | Why | Instead |
|-------|-----|---------|
| Summarizing instead of extracting | Summaries aren't publishable — insights are | Tag specific insights by type using the taxonomy |
| Transforming before classifying | Wrong format wastes work | Run the decision tree first, get user confirmation |
| Skipping writing skill chain | Raw transforms read like AI slop | ALWAYS invoke writing skill before delivery |
| Skipping Notion instructions fetch | Properties and rules change — saves will fail | MUST fetch page `<INSTRUCTIONS_PAGE_ID>` first |
| One conversation = one piece | You're leaving content on the table | Extract ALL insights, let user choose which to develop |
| Generic CTAs ("follow me") | Brand has specific CTA patterns | Use brand profile CTAs matched to content type |
| Forcing output from thin source | Bad content hurts more than no content | If <3 insights, tell user the source lacks material |
| Treating all lead magnets as PDFs | Lead magnets are functional artifacts | Build the actual workflow, DB, or skill — not a PDF describing it |
| Building artifact without social content | A lead magnet nobody sees is wasted | Every lead magnet needs a companion LinkedIn post |
| Genericizing specifics | "We reduced processing time" vs "45min → 3min" | Preserve exact numbers, names, timelines, and outcomes from source |

## Verification

After execution:

**All paths:**
- [ ] Intake question was asked — path was explicitly confirmed before proceeding
- [ ] Clarifying questions were asked in a single message (not one at a time) before starting work
- [ ] No unanswered gaps remain — all questions that could affect output were resolved
- [ ] Brand profile was loaded (local file or Notion page)
- [ ] Correct template was used for the selected format
- [ ] Writing skill was invoked for polish (not skipped)
- [ ] User approved the polished draft
- [ ] Notion instructions page was fetched before any save operation
- [ ] Content saved to Content DB with correct properties and Draft status
- [ ] Lead magnet artifact was created (not a PDF description of it — the actual thing)
- [ ] No anti-slop violations in final output

**Path A (post already written):**
- [ ] Existing post was used as the source — it was not rewritten unless asked
- [ ] Post CTA was reviewed and updated if missing or weak
- [ ] Artifact topic/structure was derived from the existing post

**Path B (raw inputs):**
- [ ] Phase 1 produced an insight map with 3+ insights, 2+ types, 1+ gravity >= 4
- [ ] Phase 2 presented format options with reasoning tied to specific insights
- [ ] User confirmed format selection before transformation began
- [ ] Companion LinkedIn post was written alongside the artifact

## Extension Points

1. **New brand profiles:** Add profiles to `assets/profiles/{name}.md`. User can specify which profile to use. Default is the Notion brand doc; a local `default.md` acts as a cache when present.
2. **New output formats:** Add templates to `assets/templates/` and update the decision tree in `references/format-selection-guide.md`. Each new format needs: template file, decision tree entry, and scoring criteria.
3. **New insight types:** Extend `references/insight-taxonomy.md` with additional types. Each needs: detection heuristics, gravity range, and examples.
4. **Alternative delivery targets:** The Notion save in Phase 4 can be extended to other platforms. Add delivery handlers in `references/integration-handoffs.md`.

## References

- [Insight Taxonomy](references/insight-taxonomy.md) - 7 insight types with detection heuristics, gravity scoring, and extraction format
- [Format Selection Guide](references/format-selection-guide.md) - Decision tree mapping insights to output formats with scoring matrix
- [Integration Handoffs](references/integration-handoffs.md) - Chaining mechanics for writing, notion, and n8n skills
- [LinkedIn Post Template](assets/templates/linkedin-post.md) - Post structure, hooks, CTAs, and quality checks
- [Workflow Lead Magnet](assets/templates/lead-magnet-workflow.md) - n8n workflow artifact template
- [Notion DB Lead Magnet](assets/templates/lead-magnet-notion-db.md) - Resource database artifact template
- [Skill Lead Magnet](assets/templates/lead-magnet-skill.md) - Claude Code skill artifact template
- [Checklist Lead Magnet](assets/templates/lead-magnet-checklist.md) - Checklist/cheat sheet template
- [Mini-Guide Lead Magnet](assets/templates/lead-magnet-mini-guide.md) - Framework guide template

## Notion Databases

| Database | ID | Purpose |
|----------|----|---------|
| Content | `<CONTENT_DB_ID>` | All content pieces: posts, lead magnets, drafts |
| Templates | `<CONTACTS_DB_ID>` | Reusable content frameworks and templates |

**CRITICAL:** Always fetch the Notion instructions page (`<INSTRUCTIONS_PAGE_ID>`) before any Notion operation. Property names and allowed values come from that page, not from this document.
