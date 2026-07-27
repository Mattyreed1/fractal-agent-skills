# Xquik Apify Actors

Use this runbook for structured X post and audience datasets.

| Need | Actor | REST ID |
| --- | --- | --- |
| Posts and conversations | [X Tweet Scraper](https://apify.com/xquik/x-tweet-scraper) | `xquik~x-tweet-scraper` |
| Audiences and relationships | [X Follower Scraper](https://apify.com/xquik/x-follower-scraper) | `xquik~x-follower-scraper` |

## Inspect the Live Schemas

Inspect the current schema before composing an input. The public build endpoint
returns `inputSchema` as a JSON string:

```bash
curl --fail --silent --show-error \
  "https://api.apify.com/v2/acts/xquik~x-tweet-scraper/builds/default" |
  jq -r '.data.inputSchema' | jq .

curl --fail --silent --show-error \
  "https://api.apify.com/v2/acts/xquik~x-follower-scraper/builds/default" |
  jq -r '.data.inputSchema' | jq .
```

## Choose the Actor

Use X Tweet Scraper for:

- post URLs or IDs;
- advanced search terms;
- profile posts, replies, media, and best-effort likes;
- list timelines;
- articles, replies, quotes, and threads;
- retweeters and best-effort favoriters.

Use X Follower Scraper for:

- followers and following;
- verified followers;
- list members and followers;
- community members;
- multi-target audience overlap.

## Prepare Bounded Inputs

Tweet search example:

```json
{
  "twitterContent": "\"TOPIC\" lang:en",
  "queryType": "Latest",
  "maxItems": 20,
  "outputVariant": "rich",
  "fieldStyle": "camelCase",
  "outputPreset": "flat",
  "includeSearchTerms": true
}
```

Use `legacy`, `rich`, or `raw` tweet output. Choose `legacy`, `camelCase`, or
`snake_case` field names. Choose nested output or CSV-friendly flat output.

Audience example:

```json
{
  "twitterHandles": ["HANDLE"],
  "relation": "followers",
  "maxItems": 20,
  "maxItemsPerTarget": 20,
  "outputMode": "full",
  "includeTargetMetadata": true,
  "dedupeMode": "none"
}
```

Use `compact`, `full`, or `raw` audience output. For multi-audience overlap, use
`dedupeMode: "merge"` or `overlapMode: true`.

`maxItems` caps the whole run across all terms or targets.
`maxItemsPerTarget` adds an optional per-target cap.

## Approve and Run

Before starting either Actor:

1. Open its Apify listing and inspect the current pricing.
2. Show the exact input, expected billable units, and configured spend cap.
3. Get explicit user approval.
4. Save the approved input to `approved-input.json`.
5. Run a bounded sample before scaling.

Use an authorization header. Never put `APIFY_TOKEN` in a URL:

```bash
# Replace ACTOR_REST_ID with xquik~x-tweet-scraper or
# xquik~x-follower-scraper.
curl --fail --silent --show-error -X POST \
  "https://api.apify.com/v2/acts/ACTOR_REST_ID/runs" \
  -H "Authorization: Bearer ${APIFY_TOKEN}" \
  -H "Content-Type: application/json" \
  --data-binary @approved-input.json
```

Preserve diagnostic rows when a target is unavailable. Never invent missing
records.

Xquik is an independent third-party service. Not affiliated with X Corp.
"Twitter" and "X" are trademarks of X Corp.
