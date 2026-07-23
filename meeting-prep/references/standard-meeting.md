# Standard Meeting — Meeting Prep Branch 1

An **established relationship** — no one is auditioning. Existing client, internal, partner sync, kickoff, follow-up, work sync: any call inside a signed engagement or ongoing relationship. Directionality: **neither side is evaluating the other**; the job is to orient the user fast and drive the open threads to a next step.

Not selling Fractal AI services (that's Branch 2 / Discovery, `discovery-sales.md`) and not evaluating a candidate (Branch 3 / Hiring, `hiring-interview.md`).

---

## When this branch applies

- An existing client, partner, or internal call — there is already a signed engagement or ongoing relationship.
- Kickoffs, follow-ups, work syncs, check-ins, partner syncs.
- No one stands to be hired or sold to on this call.

If it's genuinely unclear whether this is Standard vs. Discovery vs. Hiring, **ask (AskUserQuestion) before writing** — see the confidence gate in `SKILL.md` Step 0.

---

## Context-gathering cascade — Standard

Run in order (or fan out per the Subagent stage in `SKILL.md`). Do not skip. Do not write until complete.

**1. Notion** — Invoke the `notion` skill. Search person name, company, project topic. Read every result fully and follow all linked sub-pages and databases.

**2. Knowledge graph** — query your knowledge graph / CRM for the person and the company. Surface role, relationship, history. *(This is the READ half — after context is gathered you also WRITE people/companies back to the CRM; see **KG write-back** in `SKILL.md`.)*

**3. Meeting notes (past 90 days)** — Query the Notion Meetings DB for every meeting with this person/company from the past 90 days and read the notes pages fully — prior commitments and pain points are the most valuable context. (your meeting-notes process turns every transcript into these notes + KG updates; the notes ARE the meeting history.)
   ⛔ **Raw meeting transcripts are NOT read by default.** Read one ONLY if the user specifically asks, or if the notes for a key meeting are missing/thin — in that case flag the gap and ask before downloading anything.

**4. Local project files** — Check your project files for a matching directory. Read all `.md` files.

**5. Memory / notes** — Scan your memory / notes file for recent entries on the person, company, or project.

**6. Email (if thin)** — Search your email to pull recent threads.

---

## Notion page structure

```
## Context
[One paragraph: who this person is, their role, why this meeting exists, where it sits in the engagement.]

## What we know going in
[Bullet points from Notion meeting notes, KG, and your memory / notes: project status, prior commitments, open blockers, stated priorities.]

## Open items from last meeting
[ ] [Checkbox for each thing promised or deferred, with owner]

## Objective
[One sentence: what a successful outcome looks like for this specific call.]

## Agenda

### 1. Intro (2–3 min)
[Verbatim opening — what to actually say to frame the call. Include who the user is, why this meeting exists, and what the goal is for today.]

### 2. [Topic] (X min)
- [Exact question to ask — written as the user would say it, not as a bullet descriptor]
- [Exact question]

### 3. [Topic] (X min)
- [Exact question]
- [Exact question]

### [Continue for each agenda section]

### [Last section]. Wrap (3–5 min)
- [Any open-floor question — "Anything I haven't asked about that I should know?"]
- [Confirm what's NOT changing without their sign-off, if relevant]
- [State the next step explicitly — what happens after this call]

## What to listen for
- [Specific signal that would change how the user approaches the engagement]

## What to avoid
- [Specific mistake or assumption not to make]

## Post-meeting actions
[ ] [Action with owner]

## Notes
[Blank — for capture during the meeting]

## Key resources
- [Links: proposal, prior meeting notes, relevant Notion pages, Drive files]
```

Meetings DB properties: Type = "Meeting Prep", **Date (required — see Output rules in `SKILL.md`)**, link Client and Project relations when they exist. **CRITICAL — relations are non-optional.** Before publishing the page, confirm Contact, Companies, and Project relation fields are populated (or explicitly verified as absent). Skipping relations on a Meeting Prep page makes it invisible in CRM rollups and is the most common meeting-prep miss.

**Keep it tight** — orient the user in 2 minutes. This is a briefing, not a sales tool.
