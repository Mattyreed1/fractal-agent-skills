# Setting up `video-editor`

This skill ships as a **template**. It encodes a real production pipeline, so a few
values point at the original author's workspace and must be replaced before use.

> **For the agent reading this: interview the user for these values. Do not guess them,
> and do not invent plausible-looking IDs or paths.**

| Placeholder | What it is | Where to find it |
|---|---|---|
| `<REPO_ROOT>` | Repo where content projects live | The repo you keep video projects in |
| `<YOUR_GOOGLE_ACCOUNT>` | Google account whose Drive is mounted | Finder → `~/Library/CloudStorage/GoogleDrive-…` |
| `<CONTENT_DB_DATA_SOURCE_ID>` | Notion Content DB data source | `notion-fetch` the database → read its `collection://…` URL |
| Delivery folder paths | Where finished video + thumbnail are published | `references/pipeline/08-delivery.md` |

## Prerequisites

- **Palmier Pro** desktop app running (the MCP bridges to a localhost server — a timeout means the app is closed).
- **ffmpeg / ffprobe** on `PATH`. Scripts expect a Python with `numpy` + `PIL`.
- **DaVinci Resolve Studio** only if you need the Magic Mask fallback for background removal.
- Optional: a **fal.ai** API key for hosted background removal (`bria/video/background-removal`).

## What is worth reading even if you never run it

`references/delivery-gate.md` is the core of this skill: a set of hard gates that turn
"ready for review" into a claim only the gate can produce. Each gate exists because a
specific defect shipped once. Read the failure notes — they are the actual content.
