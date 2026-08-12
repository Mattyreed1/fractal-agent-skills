# Pipeline 1 — Ingest & media management

**Step 1 of 8** — before any editing. **Backend:** palmier-pro.

**Goal:** get footage/audio in, organized and synced.

- `import_media` (url / path / directory / bytes) · `organize_media` · `get_media` · `inspect_media`
- `sync_clips` — dual-system / multicam alignment → [audio-video-sync.md](../audio-video-sync.md)

**Do first:** copy source off CloudStorage to a stable local path, then probe duration / WxH /
**rotation metadata** / fps / audio rate — vertical footage often arrives as landscape-plus-rotation,
which changes every downstream frame number. Then set the canvas (`set_project_settings`) BEFORE
captioning.

**Call-shape traps** (`import_media` is async and single-asset on v0.6.5):
[palmier-pro.md](../palmier-pro.md).
