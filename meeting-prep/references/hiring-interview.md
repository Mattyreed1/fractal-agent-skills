# Hiring Interview — Meeting Prep Branch 3

The user is the **buyer / employer.** They are evaluating a candidate (video editor, VA, designer, developer, engineer, contractor, freelancer, assistant) for a role they're filling. This is **not** selling Fractal AI services (Branch 2 / Discovery) and **not** an existing relationship (Branch 1 / Standard). Directionality: **the candidate is auditioning for the user.**

Worked example: *a candidate for Founder Freedom's first video-editor hire.*

---

## When this branch applies

- They **applied to or booked off a job posting** — ytjobs, Upwork, Wellfound, a LinkedIn job, or a referral for a specific role.
- **Role / skill words** are present: editor, VA, designer, developer, engineer, contractor, freelancer, assistant, applicant, candidate.
- A **portfolio / reel / résumé / GitHub** is in play.
- The counterparty stands to be **paid by the user**, not to pay the user.

If which role or which brand/project the hire is for is unclear, **ask (AskUserQuestion) before writing** — never guess the role. You cannot judge fit without knowing the bar.

---

## Context-gathering cascade — Hiring

Run in order (or fan out per the Subagent stage in `SKILL.md`). Do not skip. Do not write until complete.

**1. Identify the role + the actual work.** What is the user hiring for, under which brand/project? Pull the job-posting text if you can find it. Then read the target project's **brand + strategy docs** (find them via your knowledge-graph node for the project and any `brand_doc_url` / `strategy_doc_url` properties) so you know the concrete bar the candidate must clear.

**2. Notion CRM (Contacts DB).** Is there a record? Create or repair it as a **candidate** — not a sales Lead. Do not fabricate a Company for an employer they never named.

**3. Knowledge graph.** Search the person, and search the **project they'd work on** (its requirements, visual system, required tools, current status). The project node usually already states what the hire is for.

**4. Portfolio / work-sample scrape (mandatory).** Invoke `scrape` on their portfolio / profile / reel / GitHub. Extract: real experience, tools & skills, sample work, clients, stats (views/likes/stars), reviews/vouches/ratings, location, languages, and rate if listed.

**5. Verify claims — credited work ≠ owned work.** A name on a big-channel video or repo does not mean they did it, or did it alone. Note the reviews/vouches count; **if it's zero, flag it.** Hunt specifically for evidence of the **one skill the role actually needs**, not just general competence.

**6. Email / booking.** How did they come in, what did they say, and what's their **timezone** (flag if the slot is awkward for them — a 1 a.m. call is a real async-collaboration signal, not a throwaway detail).

**7. Memory / notes + local project files.** Any prior notes on the person or the hiring project.

---

## Establish the bar before the call

Write down, straight from the project's own docs, the concrete requirements the candidate must meet — the **specific tools, style, turnaround, and volume.** A hiring interview is judged against **this bar**, not against "are they generally good at this craft."

> Example bar: DaVinci Resolve required (shared-project collaboration); hand-drawn sketchpad animation + Tim Urban–style diagrams; teal-blue / orange-yellow color system; retention editing for long-form talking-head. A strong motion-graphics editor who can't do the hand-drawn doodle style **fails this specific bar** even though they're a good editor — which is the entire point of naming the bar first.

---

## Notion page structure — Hiring interview

```
> 🎬 **This is a HIRING interview — the user is the buyer.** [Name] is a candidate for [role] on [project/brand]. Today's job: test whether they clear the SPECIFIC bar the role needs — [the 1–2 make-or-break requirements] — not whether they're generally competent. Best outcome: agree a small PAID test project on real work before committing.

## Meeting Context
**Type:** Hiring interview — [role] for [project/brand]
**When:** [date · time · the user's tz]
**Where:** [meet link]
**Attendees:** [Name] ([email]) · the user
**Source:** [which posting / referral they came through]
⚠️ **Timezone:** [their tz + what the slot means for them; flag async-collaboration reality]

## Who They Are — real profile ([source link])
[One line: role, years active, headline stats.]
- **Niche / craft match:** [how close their body of work is to what the user needs]
- **Tools:** [...] — flag whether the REQUIRED tool is primary vs. "have used it"
- **Samples / clients / stats:** [...]
- **Languages / location:** [...]

### 🟢 Green flags
- [Concrete strengths tied to the bar]

### 🔴 Verify / risks
- [Credited-vs-owned work; missing reviews/vouches; the specific-skill gap; logistics/tz]
- [Name the #1 thing to test live]

## The Work They'd Do
[The actual deliverable(s) / project(s), each named.]
Required bar: [tools + style + turnaround + volume, pulled from the brand/strategy docs.]

## Objective
[One sentence: decide fit against the bar, learn rate/turnaround/capacity, and — if promising — close a paid test project before committing to anything ongoing.]

## Agenda ([N] min)

### 1. Intro (2 min)
- [Verbatim: who the user is, what the role is, and that most of the call is about their work and style fit.]

### 2. Experience & what they actually own (X min)
- "Walk me through your background — how long, what kind of [work], what you specialize in."
- "On your portfolio — [specific pieces] — what did you own? Start-to-finish, or part of a team?"
- "You're new here with no reviews yet, which is fine. Who can vouch for you, and can you show me one raw-to-final that's 100% your work?"

### 3. The make-or-break skill fit (X min) ← the crux
- [Verbatim: describe the SPECIFIC required style/skill in concrete terms, then make them demonstrate it or show proof — do not accept "yes I can do that."]
- [A second probe that separates the required skill from an adjacent one they may be conflating it with.]
*Listen for: do they distinguish the exact skill from the near-neighbor? Do they light up, or hedge?*

### 4. Tools & workflow (X min)
- "Is [required tool] your primary, or do you work in [X] and export? I need someone who can work natively in [required tool / shared project]."
- "Walk me through your process from [raw input] to first deliverable."
- "How do you handle revision rounds and feedback?"

### 5. Capacity, turnaround, rate (X min)
- "Realistic turnaround for a first [deliverable] at this level?"
- "How many a month could you take without quality slipping?"
- "What's your rate — per [unit], hourly, or a monthly retainer?"
- "How do you usually run collaboration with a client in my timezone?"

### 6. The paid test project + next step (X min)
- "Here's how I like to start: one **paid** test [deliverable] on real work — [name the specific piece]. Small scope, real money, so we both find out if it's a fit before anything longer-term. Open to that?"
- "If yes — I'll send [the inputs] + a one-page style reference, and we lock a fee and a deadline."

### 7. Wrap (2 min)
- "Anything about the work or how I run [project] you want to ask me?"
- "I'm talking to a couple of candidates, so I'll follow up within a few days either way. Fair?"

## What to listen for
- **The required skill vs. its near-neighbor.** [e.g. hand-drawn doodle ≠ motion graphics.] If they can't show the exact thing, that's the gap that matters most.
- **Required-tool reality.** "I've used it" vs. "I work in it daily" are different answers. You need the second.
- **Ownership honesty.** A straight answer on what they did vs. claimed is a trust signal. Vagueness is a flag.
- **Feel for the mission.** Does the project's theme land, or is this just another gig?

## What to avoid
- Don't oversell the role or promise volume you don't have yet — you're evaluating them.
- Don't skip the skill-fit demonstration to be polite. It's the whole ballgame.
- Don't agree a rate or retainer before you've seen a paid test project.
- Don't treat portfolio view counts / stars as their solo work. Verify.

## Post-Meeting Actions
- [ ] Update CRM/KG as a **candidate** (not a sales Lead): role, rate, capacity, timezone, fit rating.
- [ ] If promising: send the paid-test-project brief (inputs + style ref); lock fee + deadline.
- [ ] If not a fit: thank them, keep the profile on file, note why.
- [ ] Record the skill-fit verdict against the actual deliverable(s).

## Notes
*(capture during the call — lead with the make-or-break skill fit, tool reality, rate, turnaround)*

## Key Resources
- [Profile / portfolio / clients links]
- [Meet link]
- [Brand doc · Strategy doc for the hiring project]
- [Local project folder(s)]
```

---

## Rules specific to hiring interviews

- **Name the bar first, judge against the bar.** The interview exists to test the *specific* requirement, not general talent. Put the make-or-break skill at the center of the agenda (its own section, before tools/rate).
- **Demonstration > claims.** Make them show the exact skill (a sample, a screen-share, a walk-through) — "yes I can do that" is not evidence.
- **Credited ≠ owned.** Always probe what they personally did on portfolio pieces. Zero reviews/vouches is a flag to surface, not to hide.
- **Always close on a PAID test project, never an unpaid "sample."** Real money on a small real deliverable buys real signal and respects their time. Don't commit to a retainer or a rate before that test lands.
- **CRM: candidate, not Lead.** Create/repair the Contact as a candidate for the role. Do **not** invent a Company record for an employer they never named — the relevant "company" is the user's own brand/project they'd work on.
- **Seed the KG at prep time.** Per SKILL.md → *KG write-back*, upsert the candidate as a `person` connected to the hiring project (e.g. `candidate_for` → the brand node), with a ≤3-sentence summary and a dated note linking the prep page. The KG is the CRM — don't wait for the post-meeting notes to record they exist.
- **Timezone is load-bearing.** For remote hires, treat the tz gap as a real collaboration constraint and note it in the brief.

## Meetings DB properties (Hiring)

- **Type = "Meeting Prep"** — NOT "Discovery."
- **Date (required)** — source from the calendar event; if none is booked, STOP and ask (per the never-guess rule). Never publish with Date blank.
- **Link the Contact** relation (the candidate).
- **Venture** = the hiring brand's parent venture (e.g. "Fractal AI Agency" for a Founder Freedom hire).
- No Company relation unless the candidate genuinely represents one that's relevant.
