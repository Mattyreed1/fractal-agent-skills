---
name: content-publish
description: Stage 7 (final) of the Content Engine. Publish content to LinkedIn and collect 7-day performance metrics. CC publishes; CO schedules and runs metrics collection. Tracks impressions, reactions, comments, reposts, link clicks, engagement rate, lead captures, new followers — writes everything back to the Notion Content DB.
license: MIT
metadata:
  version: 3.0.0
  created: 2026-03-27
  updated: 2026-04-28
  author: content-orchestrator
  domains: ['content', 'analytics', 'linkedin']
---

# Content Publish & Metrics

## Trigger

the user gives final go in the Discord thread, OR CC receives a `Publish — {name}` task from `content-packaging`.

## Who

CC publishes. CO collects metrics at 7 days.

## Inputs

- Final post text (from Discord thread / Notion page)
- Images/visuals
- Landing page URL (must be `your-workspace.notion.site/...` format)

## Steps

### 1. CC: publish to LinkedIn

- Post the content
- Include images/visuals
- Post the LinkedIn URL in the Discord thread:

```
## Published — {content piece name}

**LinkedIn URL:** {url}
**Published:** {date}

Content is live. CO will collect metrics in 7 days.
```

### 2. CC: update Notion content page

- Set **Stage**: `Packaging/Posting` → `Published`
- Set **Published Date**: today
- Set **LinkedIn URL**: the post URL

### 3. CO: schedule metrics collection

Create board task:
- title: `Collect Metrics — {name}`
- assignedTo: `content-orchestrator`
- dueDate: published date + 7 days
- description: Notion page URL + LinkedIn URL

### 4. CO: collect 7-day metrics (on due date)

Pull from LinkedIn analytics + internal data:

| Metric | Source | How to get |
|--------|--------|-----------|
| Impressions | LinkedIn Analytics | Post analytics page |
| Reactions | LinkedIn Analytics | Post analytics page |
| Comments | LinkedIn Analytics | Post analytics page |
| Reposts | LinkedIn Analytics | Post analytics page |
| Link Clicks | LinkedIn Analytics | Post analytics page |
| Engagement Rate | Calculated | (Reactions + Comments + Reposts + Clicks) / Impressions × 100 |
| Lead Captures | Notion Contacts DB | Filter by Signup = lead magnet name, created in last 7 days |
| New Followers | LinkedIn Analytics | Profile analytics, 7-day delta |

### 5. CO: update Notion content page

Set all metric properties:
- Metrics Date, Impressions, Reactions, Comments, Reposts, Link Clicks, Engagement Rate, Lead Captures, New Followers

### 6. CO: post metrics summary

In the Discord thread:

```
## 7-Day Metrics — {content piece name}

| Metric | Value |
|--------|-------|
| Impressions | {n} |
| Reactions | {n} |
| Comments | {n} |
| Reposts | {n} |
| Link Clicks | {n} |
| Engagement Rate | {n}% |
| Lead Captures | {n} |
| New Followers | {n} |

**Top takeaway:** {one sentence on what worked or didn't}
```

Mark metrics task as `done`. Thread complete.

### 7. CO: feed signal back into the engine

Append a one-liner to your `memory.md` with the takeaway. The weekly memory consolidation will surface this when future briefs run their retrieval cascade through `content-brief`'s "Related Prior Work" step — closing the loop.

## Edge cases

- **LinkedIn post fails to publish**: retry. If platform issue, save post text and try next day. Note in thread.
- **Metrics not available at 7 days**: LinkedIn sometimes delays analytics. Wait 24h and retry. If still unavailable, note partial data.
- **Zero lead captures**: still record it. Analyze why in the metrics summary (no CTA? wrong audience? weak offer?).
- **Notion metric properties don't exist yet**: flag to the user. Required: Published Date, Metrics Date, Impressions, Reactions, Comments, Reposts, Link Clicks, Engagement Rate, Lead Captures, New Followers, LinkedIn URL.
- **Content piece has no lead magnet**: skip Lead Captures metric. Note N/A.
