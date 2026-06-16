---
name: scrape
description: Multi-tool web scraping and lead enrichment workflow. Use when asked to scrape pages, enrich leads, research a person or company from LinkedIn, crawl sites, extract lists/tables/content, handle JavaScript-heavy targets, fetch X/Twitter posts, search/scrape Reddit threads, or set up and run scraping tools via MCP. For LinkedIn enrichment, uses Firecrawl Agent + Perplexity + web search in parallel, with Apify escalation.
---

# Scrape

Execute web data extraction with a method ladder: always try Firecrawl MCP first for LLM-friendly Markdown/JSON and general scraping. If data is not easily accessible, heavily protected by anti-bot measures, or requires massive scale, fall back to Apify Actors. (For static public JSON endpoints, `curl`/`jq` can be used as a simple alternative).

## Core Workflow

1. Define the extraction contract first.
   - Capture source URLs, required fields, output format (`json`/`csv`/`markdown`), pagination depth, and freshness requirements.
2. Pick the most direct tool for LLM ingestion.
   - Primary default (Standard web pages / LLM context): use Firecrawl MCP.
   - Fallback (Deep JS rendering, heavy anti-bot friction, massive broad crawls): use Apify via MCP.
   - Edge case (Public JSON endpoints only): use local CLI tools (`curl`/`jq`).
3. Run small validation samples before full extraction.
   - Pull 5-20 records first, verify schema completeness, then scale.
4. Normalize and validate output.
   - Remove duplicates, enforce field types, keep raw + normalized outputs.
5. Record reproducibility.
   - Save exact commands, actor input, and timestamp.

## Tool Selection Matrix

| Situation | Preferred tools |
| --- | --- |
| Default: LLM-ready Context / Markdown | Firecrawl MCP (`firecrawl_scrape`) |
| Default: Structured Schema Extraction | Firecrawl MCP (`firecrawl_extract`) |
| Default: Broad URL Discovery / Sitemap | Firecrawl MCP (`firecrawl_map`) |
| Default: Multi-page Crawl | Firecrawl MCP (`firecrawl_crawl` + `firecrawl_check_crawl_status`) |
| Default: Web Search | Firecrawl MCP (`firecrawl_search`) |
| Default: Agentic Extraction | Firecrawl MCP (`firecrawl_agent` + `firecrawl_agent_status`) |
| Default: Browser Automation | Firecrawl MCP (`firecrawl_browser_*`) |
| Fallback: JS-heavy / Anti-bot / Proxy needs | Check **Proven Apify Actors** table first → if none, run Actor Discovery |
| Fallback: Massive Scale / Deep traversal | Check **Proven Apify Actors** table first → if none, run Actor Discovery |
| Fallback: Repeatable production pipeline | Apify API direct (`curl`) or `mcpc ... --json` |
| Edge case: Public JSON endpoints | `curl`, `jq` |
| **LinkedIn profiles** (linkedin.com/in/*) | **Firecrawl Agent** (`firecrawl_agent`) → Apify (`linkedin-profile-scraper`) |
| **Lead enrichment** (person + company research) | **Firecrawl Agent + Perplexity + Web Search** in parallel, Apify escalation |
| **X/Twitter posts** (x.com or twitter.com URLs) | **xAI API** (`x_search` tool via curl) |
| **Reddit posts/threads** (reddit.com URLs) | **Reddit JSON API** (append `.json` to URL) |
| **Reddit search** (find posts about a topic) | **Reddit JSON API** (`/search.json`) |

## LinkedIn & Lead Enrichment (CRITICAL — READ FIRST)

**When the user asks to "enrich a lead", "scrape LinkedIn", or "research a person/company for meeting prep", follow this exact method ladder. Run Steps 1-3 in parallel. Do NOT try `firecrawl_scrape`, `firecrawl_extract`, or `firecrawl_browser` on linkedin.com — they are ALL blocked.**

### Model Routing for Enrichment

All enrichment sub-agent research steps (Steps 1-4) MUST use `model: "sonnet"` when spawned via the Agent tool. Only the final compile & write step (Step 5) runs on the main agent's model. This saves Opus tokens for synthesis and decision-making.

### Step 1: Firecrawl Agent (PRIMARY — LinkedIn profile data)

`firecrawl_agent` is the ONLY Firecrawl tool that works for LinkedIn. It uses a professional enrichment API that bypasses the auth wall. Launch this FIRST — it's async and takes 1-3 minutes.

```
firecrawl_agent:
  prompt: "Find detailed professional background for [NAME], [TITLE] at [COMPANY]. LinkedIn: [URL]. Return: full name, headline, location, verified email, all work history (company, title, dates, description), education, certifications, skills."
  urls: ["https://linkedin.com/in/HANDLE"]
```

Then poll `firecrawl_agent_status` every 15-30 seconds until `status: "completed"`.

**Returns:** Verified email, full work history with dates, company details, location, seniority level. Does NOT reliably return education, certifications, skills, or recent posts.

### Step 2: Perplexity Research (PARALLEL — supplemental context)

Run `mcp__perplexity__search` simultaneously with the Firecrawl agent. Use a detailed query:

```
"[Full Name] [Company Name] [Title] [Location] background experience education career history"
```

Perplexity cannot access LinkedIn profiles directly but often finds mentions in news, conference speaker bios, industry directories, and company pages that fill gaps the agent misses.

### Step 3: Web Search + Company Website (PARALLEL — company intel)

Run these in parallel with Steps 1-2:
- `firecrawl_search` for `"[Name]" "[Company]" [industry keywords]` — finds profile URL if unknown, plus news/mentions
- `firecrawl_search` for `"[Company]" company` — finds company pages, job postings, press
- `firecrawl_scrape` on the company website (NOT linkedin.com) — services, team, projects, about page
- `firecrawl_search` for company job postings — reveals current operations, team size, active markets

### Step 4: Apify LinkedIn Scraper (ESCALATION — if Steps 1-3 leave gaps)

Use when Firecrawl agent returns incomplete data (missing education, certifications, skills, posts) OR when you need the full unabridged profile.

**Requires:** `APIFY_TOKEN` in `~/.config/mr-ea/.env`

```bash
APIFY_TOKEN=$(grep '^APIFY_TOKEN=' ~/.config/mr-ea/.env 2>/dev/null | cut -d= -f2)

# Via mcpc (if installed)
mcpc @apify tools-call call-actor \
  actorId:="apify/linkedin-profile-scraper" \
  input:='{"profileUrls":["https://linkedin.com/in/HANDLE"]}' \
  --json

# Via direct API (if mcpc not available)
curl -s -X POST "https://api.apify.com/v2/acts/apify~linkedin-profile-scraper/runs?token=$APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"profileUrls":["https://linkedin.com/in/HANDLE"]}'
```

**Returns:** Complete profile including education, certifications, skills, endorsements, recent posts, follower count.

### Step 5: Compile & Write to CRM

After all sources return, merge the data and:
1. Create/update **Companies DB** entry with company details, services, projects, intel
2. Create/update **Contacts DB** entry with full career timeline, certifications, notes
3. Add rich **page body content** to both entries — not just property fields
4. Cross-link Company ↔ Contact relations
5. Add enrichment to the meeting prep page if one exists

### What NEVER works on LinkedIn

| Tool | Result | Why |
|------|--------|-----|
| `firecrawl_scrape` | ❌ Always blocked | Firecrawl explicitly excludes LinkedIn |
| `firecrawl_extract` | ❌ Always blocked | Same restriction |
| `firecrawl_browser` | ❌ Auth wall | Browser session has no LinkedIn login |
| `perplexity` for profile data | ❌ Can't access profiles | Returns generic/hallucinated info |
| Direct `curl` on linkedin.com | ❌ Auth wall | Returns login page HTML |

### Enrichment Quality Checklist

Before declaring enrichment complete, verify you have:
- [ ] Full name, title, headline
- [ ] Verified email and/or phone
- [ ] Complete work history with dates
- [ ] Education (if available)
- [ ] Certifications (PMP, etc.)
- [ ] Company details (size, industry, services, website)
- [ ] Active projects or recent activity
- [ ] Key intel / talking points for meeting prep
- [ ] Both Notion entries created with page body content (not just property fields)

---

## Reddit (Public JSON API)

**URL detection**: If the target URL matches `reddit.com/r/*/comments/*`, or the user asks to search/scrape Reddit, use the Reddit JSON API directly. No API key needed — just a browser User-Agent.

**CRITICAL**: Always use a browser User-Agent. Reddit blocks default `urllib`/`python-requests` UAs.

### Fetch a Specific Reddit Post/Thread

Append `.json` to any Reddit URL to get structured data:

```bash
# Fetch post + comments
curl -s -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36" \
  "https://www.reddit.com/r/SUBREDDIT/comments/POST_ID/SLUG.json?raw_json=1"
```

**Response structure**:
- `[0].data.children[0].data` — the submission (title, selftext, score, num_comments, upvote_ratio, created_utc, author, permalink)
- `[1].data.children[]` — comments (kind `t1`). Each has `.data.body`, `.data.score`, `.data.author`, `.data.created_utc`

### Search Reddit for a Topic

```bash
# Search across all of Reddit
curl -s -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
  "https://www.reddit.com/search.json?q=QUERY&sort=new&limit=25&t=month"

# Search within a specific subreddit
curl -s -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
  "https://www.reddit.com/r/SUBREDDIT/search.json?q=QUERY&restrict_sr=on&sort=new&limit=25&t=month"
```

**Search parameters**:
- `q` — search query
- `sort` — `new`, `hot`, `top`, `relevance` (default)
- `t` — time filter: `hour`, `day`, `week`, `month`, `year`, `all`
- `limit` — max results (1-100, default 25)
- `restrict_sr` — `on` to limit to subreddit (when searching within `/r/SUBREDDIT/`)
- `after` / `before` — pagination cursors (from `data.after` in response)

### Browse a Subreddit

```bash
# Hot posts
curl -s -A "Mozilla/5.0 ..." "https://www.reddit.com/r/SUBREDDIT/hot.json?limit=25"

# New posts
curl -s -A "Mozilla/5.0 ..." "https://www.reddit.com/r/SUBREDDIT/new.json?limit=25"

# Top posts (with time filter)
curl -s -A "Mozilla/5.0 ..." "https://www.reddit.com/r/SUBREDDIT/top.json?limit=25&t=week"
```

### Parse Reddit Response (Python one-liner)

```bash
curl -s -A "Mozilla/5.0 ..." "https://www.reddit.com/search.json?q=QUERY&sort=new&limit=10&t=month" | \
  python3 -c "
import sys, json
d = json.load(sys.stdin)
for post in d['data']['children']:
    p = post['data']
    print(f\"r/{p['subreddit']} | {p['title'][:80]}\")
    print(f\"  Score: {p['score']} | Comments: {p['num_comments']} | Author: u/{p['author']}\")
    print(f\"  URL: https://reddit.com{p['permalink']}\")
    print()
"
```

### Key Rules

- **No API key needed** — Reddit's `.json` endpoints are public.
- **User-Agent is mandatory** — use the browser UA string, NOT a bot/script UA.
- **Rate limiting** — Reddit allows ~10 requests/minute for unauthenticated. Add `time.sleep(1)` between batch requests.
- **`raw_json=1`** — always include this param to prevent Reddit from HTML-encoding content.
- **Comments are nested** — top-level comments are in `[1].data.children[]`. Replies are in `.data.replies.data.children[]` (recursive).
- **Reference implementation** — see `~/.claude/skills/last30days/scripts/lib/reddit_enrich.py` for a battle-tested parser that extracts engagement metrics, top comments, and insights.

## X/Twitter Posts (xAI API)

**URL detection**: If the target URL matches `x.com/*/status/*` or `twitter.com/*/status/*`, skip Firecrawl entirely and use the xAI API.

**CRITICAL**: Use `curl`, NOT Python `urllib`. Cloudflare blocks non-browser User-Agents on `api.x.ai` (error 1010).

### API Key Resolution

Check these locations in order:
1. `~/.config/mr-ea/.env` → `XAI_API_KEY` (EA's dedicated key)
2. `~/.config/last30days/.env` → `XAI_API_KEY` (shared last30days key)

```bash
# Load the key
XAI_KEY=$(grep '^XAI_API_KEY=' ~/.config/mr-ea/.env 2>/dev/null | cut -d= -f2)
[ -z "$XAI_KEY" ] && XAI_KEY=$(grep '^XAI_API_KEY=' ~/.config/last30days/.env 2>/dev/null | cut -d= -f2)
```

### Fetch a Specific Post

```bash
curl -s -X POST "https://api.x.ai/v1/responses" \
  -H "Authorization: Bearer $XAI_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "grok-4-fast-non-reasoning",
    "tools": [{"type": "x_search"}],
    "input": [{"role": "user", "content": "Find and return the FULL text of this X post: POST_URL_HERE. Include author name, handle, date, full text, and engagement (likes, reposts, replies, bookmarks, views)."}]
  }'
```

### Search X for a Topic

```bash
curl -s -X POST "https://api.x.ai/v1/responses" \
  -H "Authorization: Bearer $XAI_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "grok-4-fast-non-reasoning",
    "tools": [{"type": "x_search"}],
    "input": [{"role": "user", "content": "Search X for recent posts about TOPIC. Return the top 10 most engaged posts with author, text, url, date, and engagement metrics as JSON."}]
  }'
```

### Key Rules

- **Model**: Must use `grok-4` family (grok-4-fast-non-reasoning for speed, grok-4 for quality). `grok-3-mini` does NOT support `x_search`.
- **Tool**: `{"type": "x_search"}` — this is a server-side tool, not a function call.
- **Response parsing**: Output is in `response.output[].content[].text` (type: `output_text`).
- **Timeout**: Allow 60-120s — xAI searches X in real-time.
- **No Python urllib**: Cloudflare error 1010. Always use `curl`.

## Firecrawl MCP Tools Reference (v3.9.0)

The MCP server name is `firecrawl`. Tools are called as `mcp__firecrawl__<tool_name>`.

| Tool | Purpose |
|------|---------|
| `firecrawl_scrape` | Scrape a single URL → Markdown/HTML/JSON. Primary tool for LLM-ready content. |
| `firecrawl_map` | Discover all URLs on a site (sitemap-like). Use for URL discovery before targeted scraping. |
| `firecrawl_search` | Search the web and return results with content. Combines search + scrape. |
| `firecrawl_crawl` | Crawl multiple pages from a starting URL. Returns a crawl job ID. |
| `firecrawl_check_crawl_status` | Check progress/results of an async crawl job. |
| `firecrawl_extract` | Schema-based structured extraction from URLs using LLM. |
| `firecrawl_agent` | Agentic extraction — give it a URL and a prompt, it navigates and extracts. |
| `firecrawl_agent_status` | Check status of an agent extraction job. |
| `firecrawl_browser_create` | Create a persistent browser session for multi-step automation. |
| `firecrawl_browser_execute` | Execute actions in a browser session. |
| `firecrawl_browser_delete` | Close a browser session. |
| `firecrawl_browser_list` | List active browser sessions. |

## Firecrawl MCP Setup

**Package**: `firecrawl-mcp` (npm, ESM module)

**Claude Desktop config** (`~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
"firecrawl": {
  "command": "/usr/local/opt/node@20/bin/node",
  "args": [
    "~/.local/node_modules/firecrawl-mcp/dist/index.js"
  ],
  "env": {
    "FIRECRAWL_API_KEY": "fc-YOUR_API_KEY"
  }
}
```

**Install/update**:
```bash
cd ~/.local && /usr/local/opt/node@20/bin/npm install firecrawl-mcp
```

Do NOT use `npx` or the old `@mendable/firecrawl-mcp-server` package (deprecated/removed from npm).

## YouTube Transcripts

**Skip Firecrawl/Apify for YouTube transcripts.** Use the `youtube-transcript-api` Python library directly — it's faster and more reliable.

```python
from youtube_transcript_api import YouTubeTranscriptApi
api = YouTubeTranscriptApi()
transcript = api.fetch('VIDEO_ID')  # 11-char ID only, not full URL
for snip in transcript:
    print(snip.text)
```

- Extract video ID from URL: everything after `v=` and before `&`
- `api.list('VIDEO_ID')` — check available languages first
- Returns snippets with `.text`, `.start`, `.duration`
- Works for auto-generated captions (most videos have these)
- **Do NOT use `yt-dlp`** — fails on most videos due to PO token requirements
- Library: `pip3 install youtube-transcript-api` (v1.x API — instantiate class, then call methods)

## Local-First Quick Patterns

### Pull JSON directly

```bash
curl -sSL "https://example.com/api/items" | jq '.items[] | {id, title, url}'
```

### Extract embedded JSON-LD from HTML

```bash
curl -sSL "https://example.com/post" \
  | rg -o '<script type="application/ld\+json">[\s\S]*?</script>'
```

### Basic pagination loop (shell)

```bash
for page in 1 2 3; do
  curl -sSL "https://example.com/api/items?page=${page}" >> raw-pages.jsonl
done
```

If primary tools like Firecrawl are blocked or incapable, escalate to the Apify MCP workflow.

## Apify MCP Setup (mcpc)

Read [references/apify-mcp-setup.md](references/apify-mcp-setup.md) for complete setup and troubleshooting.

Minimum commands:

```bash
npm install -g @apify/mcpc
mcpc mcp.apify.com login
mcpc mcp.apify.com connect @apify
mcpc @apify tools-list
```

Transport rule:
- Use `mcp.apify.com` as the endpoint.
- Do not use legacy `mcp.apify.com/sse`.

## Runtime Selection (CRITICAL)

Choose integration by execution environment:

1. Local workstation with interactive OAuth support:
   - Use `mcpc` flow (`login`, `connect`, `tools-list`).
2. Managed/embedded runtime (for example a containerized agent runtime) where native `mcpc` dependencies may fail:
   - Use MCP host config with `mcp-remote` + `Authorization: Bearer ${APIFY_TOKEN}` header.
   - Do not assume `mcpc` works in-container without a direct binary test.

Never claim Apify MCP is ready until you verify:
- skill availability at execution target,
- MCP server config exists,
- token/env is present,
- runtime restarts cleanly,
- no auth/startup errors in logs.

## Apify Actor Discovery (Last-Resort Escalation)

When Firecrawl fails (anti-bot, JS rendering, empty results after retries), search Apify's actor store to find a purpose-built scraper. **Only suggest actors that charge per usage/event — never flat monthly subscriptions.**

### Step 1: Search for Actors via API

```bash
APIFY_TOKEN=$(grep '^APIFY_TOKEN=' ~/.config/mr-ea/.env 2>/dev/null | cut -d= -f2)

# Search by target site or data type
curl -s "https://api.apify.com/v2/store?token=$APIFY_TOKEN&search=TARGET_SITE_OR_KEYWORD&limit=10&sortBy=popularity" | \
  python3 -c "
import sys, json
data = json.load(sys.stdin)
for actor in data.get('data', {}).get('items', []):
    pricing = actor.get('pricingModel', 'UNKNOWN')
    # Skip actors with flat monthly pricing
    if pricing in ('FLAT_PRICE_PER_MONTH',):
        continue
    name = actor.get('title', 'Unknown')
    actor_id = f\"{actor.get('username', '')}/{actor.get('name', '')}\"
    desc = (actor.get('description', '') or '')[:120]
    stats = actor.get('stats', {})
    runs = stats.get('totalRuns', 0)
    users = stats.get('totalUsers', 0)
    price_usd = actor.get('pricingPerEvent', {})
    event_price = price_usd.get('pricePerEvent', 'N/A') if price_usd else 'N/A'
    print(f\"Actor: {name}\")
    print(f\"  ID: {actor_id}\")
    print(f\"  Pricing: {pricing} | Per event: \${event_price}\")
    print(f\"  Runs: {runs:,} | Users: {users:,}\")
    print(f\"  {desc}\")
    print()
"
```

### Step 2: Get Actor Pricing Details

```bash
# Get full actor info including pricing tiers
curl -s "https://api.apify.com/v2/acts/ACTOR_ID?token=$APIFY_TOKEN" | \
  python3 -c "
import sys, json
d = json.load(sys.stdin).get('data', {})
print(f\"Name: {d.get('title')}\")
print(f\"Pricing model: {d.get('pricingModel')}\")
pe = d.get('pricingPerEvent', {})
if pe:
    print(f\"Price per event: \${pe.get('pricePerEvent', 'N/A')}\")
    print(f\"Event description: {pe.get('eventDescription', 'N/A')}\")
    print(f\"Min events: {pe.get('minimumNumberOfEvents', 'N/A')}\")
else:
    print('Pay per platform usage (Apify compute units)')
    print('Estimate: ~\$0.25-2.00 per 1,000 results depending on complexity')
print(f\"Description: {(d.get('description') or '')[:200]}\")
"
```

### Step 3: Present Options to User

**Before running any Apify actor, ALWAYS present the user with:**

1. **Actor name and ID** — what it does
2. **Pricing model** — per-event, per-result, or platform usage
3. **Estimated cost** — calculate based on the user's expected volume:
   - Per-event actors: `price_per_event × expected_results`
   - Platform-usage actors: estimate ~$0.25-2.00 per 1,000 results
4. **Popularity signal** — total runs and users (higher = more reliable)
5. **Ask for explicit confirmation** before running

Example presentation:
```
Firecrawl couldn't scrape [site] — it's blocked by anti-bot protection.
I found these Apify actors that could handle it:

1. **Google Maps Scraper** (apify/google-maps-scraper)
   - $0.50 per 1,000 results | 2.1M total runs | 45K users
   - For ~500 results: estimated cost ~$0.25

2. **Web Scraper** (apify/web-scraper)  
   - Platform usage (~$1.50/1K pages) | 890K runs | 22K users
   - For ~50 pages: estimated cost ~$0.08

Want me to try one of these?
```

### Pricing Filter Rules

| Pricing Model | Action |
|---------------|--------|
| `PAY_PER_EVENT` | Suggest — show per-event price × expected volume |
| `PRICE_PER_DATASET_ITEM` | Suggest — show per-item price × expected items |
| `FREE` | Suggest — note it uses Apify compute units (platform cost still applies) |
| `FLAT_PRICE_PER_MONTH` | Skip — never suggest monthly subscription actors |

### Step 4: Execute (After User Approval)

```bash
# Run the actor with a small sample first
curl -s -X POST "https://api.apify.com/v2/acts/ACTOR_ID/runs?token=$APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"startUrls":[{"url":"TARGET_URL"}],"maxItems":2}'

# Check run status
curl -s "https://api.apify.com/v2/actor-runs/RUN_ID?token=$APIFY_TOKEN" | \
  python3 -c "import sys,json; d=json.load(sys.stdin)['data']; print(f\"Status: {d['status']} | Items: {d.get('stats',{}).get('itemCount',0)} | Cost: \${d.get('usageTotalUsd',0):.4f}\")"

# Fetch results
curl -s "https://api.apify.com/v2/actor-runs/RUN_ID/dataset/items?token=$APIFY_TOKEN&limit=10"
```

Always run a small sample (1-2 items) first, verify the data quality, then scale up only after user confirms.

### Step 5: Incorporate Proven Actors (Learning Loop)

After a successful Apify actor run, **ask the user if this actor should be added to the skill for automatic use next time.** Do not silently add it — always confirm first.

**Prompt template:**
```
✅ [Actor Name] worked well for [use case]. 
Results: [X items, $Y cost, quality summary].

Should I add this as a default actor for [site/use case] in the scrape skill?
That way next time I'll use it automatically instead of going through discovery.
```

**If the user confirms**, add the actor to the **Proven Apify Actors** table below and update the **Tool Selection Matrix** with a new row mapping the use case to the actor. Include the actor ID, typical input config, and per-event cost at time of addition.

**If the user declines**, do nothing — the actor remains a one-off.

## Proven Apify Actors

Actors that have been tested and approved for automatic use. **Check this table BEFORE running Apify Actor Discovery** — if a proven actor exists for the use case, skip discovery and use it directly (still show the user the estimated cost before running).

| Use Case | Actor ID | Pricing | Typical Input | Added |
|----------|----------|---------|---------------|-------|
| LinkedIn profiles | `apify/linkedin-profile-scraper` | Per event | `{"profileUrls":["URL"]}` | pre-existing |
<!-- Add new proven actors here as they are approved -->

## Output Quality Gates

- Ensure every required field exists in at least 95% of records.
- Keep `raw` and `clean` datasets separately.
- Include source URL and scrape timestamp in each row.
- Deduplicate by stable key (`id`, canonical URL, or hash).

## Guardrails

- Respect robots, terms, and legal constraints for each target.
- Avoid high-rate burst scraping from local shell; prefer Apify managed retries/proxies at scale.
- Never store secrets in committed files; use environment variables.
