---
name: meeting-prep
description: >
  Creates a structured meeting prep brief for any call, meeting, or intro the user is about to have.
  Invoke this whenever the user asks to "prep for a meeting", "create a meeting prep page", "get me ready
  for a call with [person]", "write a pre-meeting brief", "what do I need to know before meeting [X]",
  or any variant. Also invoke proactively when context suggests a meeting is imminent and preparation
  would be useful. Always runs the full context-gathering cascade before writing anything — do not skip
  context steps even if you think you know enough about the person.
---

# Meeting Prep

Creates a structured meeting prep brief by pulling all available context before writing anything.

This SKILL.md is the **router + shared doctrine**. The per-type cascade, Notion page structure, and script live in the matching **branch file** — load the one Step 0 selects and follow it.

| Branch | Meeting type | Playbook |
|--------|--------------|----------|
| 1 | **Standard** (existing client / partner / internal) | [`references/standard-meeting.md`](references/standard-meeting.md) |
| 2 | **Discovery / Sales** (prospect evaluating the user) | [`references/discovery-sales.md`](references/discovery-sales.md) |
| 3 | **Hiring interview** (the user evaluating a candidate) | [`references/hiring-interview.md`](references/hiring-interview.md) |

## Step 0: Route the meeting type — classify, then gate on confidence

Before running the cascade, classify the meeting into **exactly one** of three types. The single most reliable discriminator is the **direction of the transaction — who is evaluating whom.**

| Type | Direction | Signals | Branch |
|------|-----------|---------|--------|
| **Discovery / Sales** (Fractal AI lead) | **They evaluate the user** — the user is the *seller* | First/early call with a prospect or inbound lead; "sales call", "discovery call", "automation audit"; they represent a potential *client* business; no signed engagement; the counterparty stands to *buy* Fractal AI services | → Branch 2 (`references/discovery-sales.md`) |
| **Hiring interview** | **the user evaluates them** — the user is the *buyer of their labor* | Candidate for a role the user is filling; applied or booked off a **job posting** (ytjobs, Upwork, LinkedIn job, referral for a role); role words — editor, VA, designer, developer, contractor, freelancer, assistant, applicant; a **portfolio / reel / résumé** is in play; they'd *work for* the user | → Branch 3 (`references/hiring-interview.md`) |
| **Standard** | **Established relationship** — no one is auditioning | Existing client, internal, partner sync, kickoff, follow-up, work sync — any call inside a signed engagement or ongoing relationship | → Branch 1 (`references/standard-meeting.md`) |

### Confidence gate (mandatory — do not skip)

After classifying, estimate your confidence. **If you are below ~90% confident, STOP and confirm with the `AskUserQuestion` tool before running any cascade.** Never guess the type — the wrong branch produces a brief that walks the user into the call with the wrong plan.

Ask one question:
- **"What kind of meeting is this?"** — options: `Fractal AI discovery / sales call (they're a potential client)` · `Hiring interview (they'd work for you — editor, contractor, employee)` · `Standard (existing client, partner, internal, follow-up)`. (AskUserQuestion auto-adds an "Other" escape.)

**A bare inbound booking with no stated reason is NOT automatically a sales lead.** Check the channel they came through: a Cal.com/booking link attached to a *job posting* is a **hiring interview**, not Discovery. Thin identity + no intake reason = you are below 90% → ask.

> ⚠️ **Failure note (real example):** an inbound Cal.com booking from a video editor who applied to a Founder Freedom job posting was confidently mis-routed to Branch 2 (automation Discovery). The brief invented an "anonymous automation lead," scripted a scoping-session pitch, and guessed a wrong LinkedIn identity — all backwards, because the user was the *buyer*, not the seller. "Inbound + self-booked + on the Fractal AI calendar" got pattern-matched to *sales* without checking the direction of the transaction. This gate exists to catch exactly that: when signals conflict or context is thin, ask.

Once the type is locked, **open that branch's playbook** (table above) and run its context-gathering cascade + Notion page structure. Everything below Step 0 is **shared across all three branches.**

---

## Subagent stage: parallel context fan-out

The per-branch cascade is a **fan-out read** — bounded retrieval where only the findings survive into the brief. Run it as up to **3 isolated Haiku readers in parallel** (default cap; no fork), not sequentially in the main loop:

- **Reader A — internal:** Notion (invoke `notion`) — the **Meetings DB notes from the past 90 days are the PRIMARY meeting-history source** — plus your knowledge graph / CRM, local project files, and your memory / notes.
- **Reader B — comms:** email threads ONLY. ⛔ **Never raw meeting transcripts by default** — your meeting-notes process already turns every transcript into Meetings DB notes + CRM updates, and Reader A reads those. Read a full transcript ONLY when the user specifically asks, or after flagging a missing/thin note and getting their OK.
- **Reader C — external (discovery + hiring):** a **deep scrape, not a skim** (invoke `scrape`): the person's full LinkedIn (career history, education, posts, activity) AND the company's LinkedIn page + website(s), plus targeted web research (invoke `research`). *Discovery:* company + person fit, pain points. *Hiring:* verify the candidate's claimed work and reputation against the role's bar — portfolio/reel, real ownership of credited work, reviews/vouches/references (see `references/hiring-interview.md`).

Each reader's prompt states: objective (this person/company/meeting), boundaries (its sources only), the sources above, **output schema** (`{role, relationship, history, prior commitments, pain points, open threads, evidence links, uncertainty}`), evidence requirement (cite the source doc/URL), stop condition (sources exhausted), and a noise cap (compact findings, no raw transcript dumps). The **main loop owns synthesis** — it reads the three artifacts and writes the brief; it never promotes a reader's weak/uncorroborated claim to fact. For a standard meeting where internal context is already rich, a single Reader A may be enough — don't spawn readers you can't justify over a direct read.

---

## KG write-back — populate the CRM (mandatory, all branches)

Reading the knowledge graph (cascade step 2) is only **half** the job. Your knowledge graph **is the CRM** — treat it as agent-written — so once context is collected, **write the people and companies back into it** so the CRM reflects everyone on the user's radar, not only post-meeting attendees. Do this **after** the Notion prep page exists, so the note can link to it.

**Use your knowledge-graph / CRM tooling for the writes.** For each person and company surfaced:

1. **Search first, then upsert.** If the entity already exists, **update** it (add the dated note, refresh the ≤3-sentence summary) — never create a duplicate. Create only when genuinely new.
2. **Every new entity gets ≥1 typed relation — no orphans, ever:** create it together with its relation. If you can't connect it confidently, hold it in a pending queue rather than fake an edge.
   - **Hiring:** `person` → the hiring **project/brand** node (e.g. `candidate_for` → Founder Freedom). Add a company only if they genuinely represent one.
   - **Discovery:** `company` connected to **Fractal AI Agency** as a prospect/lead; `person` `works_at` that company.
   - **Standard:** person/company usually already exist — update them and append this meeting to their contact log.
3. **Stay in the KG's lane:** entity + typed relations + a **≤3-sentence summary** + a **dated contact-log note that links out to the Notion prep page**. **No long prose** — the brief lives in Notion; the KG indexes and links to it.
4. **Seed, don't duplicate.** Post-meeting, your meeting-notes process enriches these same nodes with what was learned — at prep time you're recording who they are, the meeting's purpose, the source, and the prep-page link.
5. **VERIFY, then you're done.** After writing, re-query your knowledge graph for each person and company and confirm the **typed** edge actually exists (`works_at`, `prospect_of`/`client_of`) — a `mentions`-only edge is NOT done (typed beats mentions). Do not consider this step complete until the query shows the typed edges.

> ⛔ **HARD GATE — meeting-prep is NOT complete without the knowledge-graph write-back.** Labeling this step "mandatory" is not enough on its own — it gets skipped under load (a real failure: Notion page + CRM done, graph write-back skipped, caught days later). Make it a blocking definition-of-done: your final output MUST include a "CRM entities created/updated + typed edges" line — if you can't write that line truthfully, you are not done. Back it with an audit that re-checks upcoming meetings' attendees for a connected node + the expected typed edge, so a skip is caught in hours, not weeks. Producing the Notion page without the verified write-back is an **incomplete deliverable**, not a done one.

---

## Definition of Done (blocking — all must be true before you report "done")

1. Notion prep page created/updated, **Date set**, Contact/Companies/Project relations populated (or verified absent).
2. Notion CRM Contact + Company exist (created if new).
3. **KG write-back executed AND verified** — person + company nodes exist, each carries its correct info (role, LinkedIn, email), and the **typed** edges are confirmed via a knowledge-graph query (Discovery: `person works_at company`, `company prospect_of Fractal AI Agency`).
4. Your reporting output includes the Notion link, the context sources, AND the KG entities/edges line (§Output rules 1-3).

If any of these is missing, the meeting-prep is not done — finish it before signing off.

---

## Output rules

**Notion:** Create a new page in the Meetings database with the appropriate type. Link Client and Project relations when they exist. Full brief goes in Notion.

**ALWAYS set the Date property — never publish a prep page with Date blank.** Source it from the calendar event for the meeting. **If no calendar event is booked yet, STOP and ask the user for the date** (per the never-guess rule) before publishing — do not leave it empty and do not guess. A meeting-prep page with no date is a common miss. Use the expanded date format on write (`date:Date:start`, optional `date:Date:is_datetime`).

**Reporting output (chat / Slack / Discord / in-conversation):** Post only:
1. The Notion page URL
2. A bullet list of every context source used (each Notion page / meeting note read, scrape + web research queries run, KG hits, local files, emails — and any raw transcript the user explicitly approved)
3. The KG entities created or updated (person / company + the typed relation)

Do NOT paste the full brief into your reporting channel or the conversation.

---

## General rules (all branches)

- Never write before completing the cascade. A brief without context is guesswork.
- If the person's name is ambiguous, ask before searching.
- If a topic is given ("we're talking about their RFI workflow"), lead the agenda/script with that.
- If no Notion contact/company record exists for a discovery call prospect, create it before writing the brief.
- Branch-specific depth: Standard is tight (orient in 2 minutes); Discovery is the deepest (it's a sales tool). See each branch file.

## Agenda rules (all branches)

- Every agenda section gets a time allocation in parentheses.
- Every question is written verbatim — the exact words the user would say, not a descriptor of what to ask.
- The first section is always an **Intro** (2–3 min): who the user is, why this meeting exists, what the goal is today.
- The last section is always a **Wrap** (3–5 min): open-floor question, any "nothing changes without your sign-off" confirmation if relevant, and an explicit next step stated out loud.
- Questions are placed in the section where they naturally belong — not batched at the end.
- Time allocations should add up to a realistic meeting length (usually 30–60 min total).
