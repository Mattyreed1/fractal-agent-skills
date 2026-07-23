# Discovery / Sales — Meeting Prep Branch 2

**They evaluate the user — the user is the seller.** A first/early call with a prospect or inbound lead who represents a potential *client* business and stands to *buy* Fractal AI services. No signed engagement yet. Directionality: **the prospect is deciding whether to hire Fractal AI.**

Not an existing relationship (Branch 1 / Standard, `standard-meeting.md`) and not evaluating a candidate for a role the user is filling (Branch 3 / Hiring, `hiring-interview.md`).

Reference example: a discovery prep page for an inbound prospect evaluating Fractal AI.

---

## When this branch applies

- First or early call with a prospect / inbound lead.
- "Sales call", "discovery call", "automation audit".
- They represent a potential *client* business; no signed engagement.
- The counterparty stands to *buy* Fractal AI services.

**A bare inbound booking with no stated reason is NOT automatically a sales lead** — a Cal.com/booking link attached to a *job posting* is a Hiring interview (Branch 3). Thin identity + no intake reason = below 90% confidence → ask (see `SKILL.md` Step 0 confidence gate).

---

## Context-gathering cascade — Discovery

Run in order (or fan out per the Subagent stage in `SKILL.md`). Do not skip. Do not write until complete.

**1. Notion** — Invoke the `notion` skill. Search person, company, topic; read every result fully. Also check CRM (Contacts DB) and Companies DB for existing records.

**2. Knowledge graph** — query your knowledge graph / CRM for the person and the company. Surface role, relationship, history. *(READ half — you also WRITE back per **KG write-back** in `SKILL.md`.)*

**3. LinkedIn scrape (mandatory for discovery — deep, not a skim)**
Invoke the `scrape` skill on the person's LinkedIn URL. If you don't have the URL, find it first via web search (`site:linkedin.com/in "[Person Name]" "[Company]"`). Extract: current title, location, full career history, education, any posts or activity. Also scrape the **company's LinkedIn page and website** (step 4 adds the research layer on top; this step pulls the actual pages).

**4. Web research (mandatory for discovery — company + broader context)**
Invoke the `research` skill to research:
- The **company**: website, founding year, size, services, locations, recent news, tech stack if visible
- The **person**: any public writing, talks, press, or community involvement not on LinkedIn
Search for: `"[Person Name]" "[Company]"`, `"[Company Name]" [industry] automation`, `"[Company Name]" site:[companywebsite]`.

**5. Their intake form / what they told the user** — Pull from email or calendar invite. What did they say they want to automate? What triggered the call?

**6. Email** — Pull the full thread with this person. Note exact language they used.

**7. Local project files + memory / notes** — Check for any prior notes.

**8. CRM check + add** — Search Contacts and Companies DB in Notion. If not found, create entries now (don't wait until after the meeting). Use the `notion` skill.

---

## Notion page structure

```
## About [Company Name]
Website | Location | Industry | Founded | Size
[3–5 bullet points: what they do, services, specializations, any geographic or market context]

## About [Person Name]
LinkedIn | Email | Phone (if known)
Title | Location (be precise — city, not just country)
Certifications/credentials if relevant

### Career Timeline
| Period | Company | Role | Location |
[Full career table — every role from LinkedIn, oldest to newest]

### Key Insight: [One-liner about their background]
[2–3 sentences synthesizing what their background means for the call. What mental model do they bring? What language will resonate? What will they be skeptical of?]

## What They Told You
[Exact quote or close paraphrase of what they said they want to automate / why they booked the call. Pull from intake form or email.]

## Why This Is a Strong Lead
- [Bullet: domain fit, inbound vs outbound, specific signal]
- [Bullet: relevant comparison to existing client work]
- [Bullet: any urgency signal — hiring, growth, stated frustration]

## Likely Pain Points ([Industry] Firms)
1. [Specific workflow pain — be industry-specific, not generic]
2. [Specific workflow pain]
3. [Specific workflow pain]
4. [Specific workflow pain]
5. [Specific workflow pain]
[5–7 items. Pull from what the user has seen with similar clients.]

## Discovery Call Strategy
[Numbered overview of how to run this specific call — tailored to this person, not the generic script.]
1. Frame (X min) — [What to say specific to their background]
2. Understand [Company] (X min) — [Key questions for their specific context]
3. Unpack their stated interest (X min) — [How to probe their specific ask]
4. Find the bottleneck (X min) — [What to listen for given their industry]
5. Share relevant experience (X min) — [Which client comparisons to use]
6. Bridge to next step (X min) — [What the ask is]

## Discovery Call Script — [Person Name]
*Goal: identify one high-pain workflow, confirm it's automatable, sell a paid scoping session.*

### 1. Frame the Call (2 min)
[Verbatim opening — what to actually say]

### 2. Understand [Company] (5 min)
- [Exact question to ask]
- [Exact question to ask]

### 3. Unpack "[Their stated interest]" (10 min)
- [Exact question to ask]
- [Exact question to ask]
*Listen for: [specific signals relevant to their industry]*

### 4. Quantify the Pain (10 min)
- How often does that happen? Daily? Weekly?
- How many people touch that workflow?
- Roughly how many hours per week?
  - *If they can't estimate:* If that task disappeared tomorrow, what would your team do with the freed-up time?
- What happens when it goes wrong? What's the downstream cost?
- What have you already tried, and why didn't it work?

### 5. Validate Feasibility (internal — don't say out loud)
- Does this involve moving data between systems? → Automatable
- Does this involve repetitive decisions with clear rules? → Automatable
- Does this require complex judgment or physical presence? → Probably not a fit
- Do I know the tools involved? → Green light

### 6. Share Relevant Experience (5 min)
- Bridge: "Here's what I'm hearing — your team spends significant time on {workflow}, and it's causing {consequence}."
- [Specific client comparison 1 with brief description]
- [Specific client comparison 2 with brief description]
- "I won't pretend I have the exact solution mapped out right now. That takes looking under the hood. But based on what you've described, I'm confident this is solvable."

### 7. Bridge to Next Step (5 min)
- "Here's what I'd propose: a focused scoping session where I map the workflow end-to-end and deliver a specific plan. You're not buying a black box."
- "The scoping session runs {price} and takes about a week. You walk away with a documented workflow map and automation plan — even if you don't proceed with the build, you keep the deliverable."
- "Most clients move into the build phase because the ROI becomes obvious once the numbers are on paper."

### 8. Close
- "I have availability to start scoping {timeframe}. Want to lock that in?"
- *If they want to skip scoping:* "I appreciate the confidence. Let me at least do a quick 2-hour deep dive so I can scope it accurately — I'll roll that cost into the project fee. Fair?"
- "Any reason we wouldn't move forward today?"

### 9. Objection Handling
- **"I don't know if this is even automatable"** → That's exactly what the scoping session answers. If it's not a fit, I'll tell you straight and refund the fee.
- **"Can't you just tell me what you'd build right now?"** → I could guess, but that's how projects go sideways. Scoping takes a week and saves months of back-and-forth.
- **"I need to think about it"** → Totally fair. What specifically? Let's solve it now.
- **"I need to talk to my partner/team"** → What do you think they'll say? What would you need to show them?
- **"It's too expensive"** → Compared to what? What's the cost of doing this manually for another 6 months?
- **"We've been burned by vendors before"** → What went wrong? Here's specifically how my process prevents that — you see the full plan before any build starts, and you own everything I create.
- **Split payment:** How much can you comfortably pay now? The other half can come after delivery.

## Connection Points
- [Shared background, geography, industry, mutual contacts]
- [Relevant client work that maps to their situation]
- [Any personal overlap — events, community, credentials]
```

Meetings DB properties: Type = ["Discovery", "Meeting Prep"], **Date (required — see Output rules in `SKILL.md`)**, Venture = "Fractal AI Agency".
CRM: create Contact + Company entries in Notion if not already present.

**Go deep** — Branch 2 is intentionally the heaviest branch. This is a sales tool, not just a briefing.
