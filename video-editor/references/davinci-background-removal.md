# DaVinci Resolve — Background Removal (AI Magic Mask 2 → transparent cutout)

**Empirically verified end-to-end via computer-use on DaVinci Resolve Studio 21.0.0.48 (2026-06-23).** Removed real room backgrounds behind a talking head on two clips of `timeline_1`, tracked across each clip, output as alpha. Everything below is Color-page UI / computer-use — see the capability verdict.

## ⚠️ CHECK THE HOSTED-API ROUTE FIRST — Resolve is the fallback, not the default (added 2026-08-11)

**This file used to describe the Resolve UI route as if it were the only way to cut out a real
background, and that omission produced a flatly wrong answer to the user** (*"there's no API path"*).
There is one, and their key is already on the machine.

| | Hosted API (fal.ai) | Resolve Magic Mask 2 |
|---|---|---|
| Cost | **$0.0042/sec** — a 178.8s source = **$0.75** | free |
| Human effort | one script | **~4–6 clicks/shot + tracking at ~1 fps** (a 5,400-frame source ≈ 90 min of computer-use) |
| Verified? | ⚠️ **documented, NOT yet runtime-verified — do not report it as working until it has been run** | ✅ end-to-end 2026-06-23 |

- **Model: `bria/video/background-removal`** (VRMBG 3.0) — built for talking heads with no green screen.
  Params (verified on the model page 2026-08-11): `video_url` (required), `background_color`
  (default `Black` → set **`Transparent`**), `preserve_audio` (default true),
  `output_container_and_codec` (default `webm_vp9`, which carries alpha).
  **Limits: input < 4000x4000 and duration < 30s** — longer sources must be chunked.
- Alternatives on the same key: `veed/video-background-removal` (+ `/fast`), `fal-ai/birefnet/v2/video`.
- **Credential:** `FAL_KEY` in `~/.config/mr-ea/.env`, also Keychain `mr-secret/fal_key`. Never inline it.
- **Pipeline:** normalise/downscale to the delivery res FIRST (a 4K master is a pointless upload when
  the output is 1080x1920) -> split into <30s chunks -> call per chunk -> transcode the webm/VP9 alpha
  to **ProRes 4444** -> concat -> `import_media` onto a track above the graphics. Palmier reads alpha.
- **Watch for:** matte consistency across chunk seams, and the fact that a hosted model bills per call —
  ask the user before spending, and re-check pricing rather than quoting this table months later.
- **When Resolve still wins:** no network/credential, a source the API's limits reject, or a shot that
  needs hand-refined subtract-clicks the model gets wrong. Keep the runbook below for those.

### ⚠️ VP9 alpha is invisible to ffmpeg's default decoder — this WILL look like the model failed

`bria/video/background-removal` returns `webm_vp9`, which stores alpha as a **separate coded layer**.
`ffprobe` reports `pix_fmt=yuv420p` and a plain `ffmpeg -i` composite shows **the original background
fully intact** — so the first check says "the model ignored `Transparent`" and it is WRONG.

```bash
ffprobe -v error -show_streams out.webm | grep -i alpha      # look for TAG:alpha_mode=1
ffmpeg -c:v libvpx-vp9 -i out.webm ...                        # EXPLICIT decoder, or alpha is dropped
```
Verified 2026-08-11: `TAG:alpha_mode=1`, and decoding with `-c:v libvpx-vp9` gives alpha extrema 0..255
on a matte that was perfect (hair edges and separated fingers both clean). Convert for Palmier with
`-c:v libvpx-vp9 -i in.webm -c:v prores_ks -profile:v 4444 -pix_fmt yuva444p10le` — note the input
decoder flag goes BEFORE `-i`. **Never judge a matte through the default decoder.**

**The general lesson (this is why the error happened, and it is not about video):** the answer was
reasoned from the one route this file documents, instead of **enumerating what is actually installed
and credentialled on the machine**. Same family as the Apify/Reddit miss — *count independent paths
before declaring a capability absent, and treat a doc's silence as silence, never as evidence.*

## Capability verdict (tested, not reasoned)
- **Real-world background (normal room) → DaVinci Magic Mask 2, 100% Color-page UI.** The MCP's *only* role is `resolve_control(open_page="color")` + `timeline.get_items` to pick a clip. Magic Mask, tracking, and alpha routing are **NOT in the Blackmagic scripting API** (api_truth: "cannot add, delete, or connect nodes … qualifiers/power windows"; Magic Mask isn't in the object model at all).
- **Green screen** → alternative path = Fusion **Delta Keyer** (scriptable to *build* via `fusion_comp`; tune in the viewer). Not needed for real backgrounds.
- **palmier-pro → no AI background-removal / subject segmentation.** (v0.6.1 adds `apply_effect` `key.chroma` ⚠️ — real chroma keying for green-screen sources, and `create_matte` for solid mattes — but nothing Magic-Mask-like for un-keyed backgrounds.)

## 🔑 The #1 rule (cost a whole session to learn)
**AI Magic Mask 2 segments the OBJECT under each click — NOT the whole person automatically.** One click on the shirt masks *just the shirt*; on the hair, *just the hair*; above the hairline, *the background*. To cut out a whole person you must place **one positive click on EACH major body part**: **hair → face → torso → each visible hand/arm** (≈4–6 clicks for a talking head). Then refine. Do not expect a single click to grab the person.

## FAST PATH — the runbook (do exactly this, in order)
**Pre-flight (MCP, no UI):** `resolve_control(open_page="color")`; `timeline.get_items("video",1)` to pick the talking-head clip. For a *specific* clip ("the first one"), **select it on the EDIT page first, then switch to Color** — the Color-page clip strip mixes tracks, so don't trust strip order. Then `request_access(["DaVinci Resolve"])` + `open_application` (full tier).
**Coverage check:** if b-roll on an upper track (V2) covers the target A-roll clip, the cutout won't be visible in playback — confirm with the user before spending a tracking pass.

1. **Select the clip** (per pre-flight). Confirm the viewer shows the person, not b-roll.
2. **Open Magic Mask** — palette toolbar (bottom-center): the **person-bust-in-a-frame** icon, in the right group **between Tracker** (crosshair) **and Blur** (two droplets). Header reads "AI Magic Mask 2". *(this workspace ≈ (531, 521))*
3. **Wire Alpha Output FIRST (live preview).** Node editor → right-click empty space → **Add Alpha Output** (blue square, far right) → drag the node's **key output** (blue square, node's bottom-right corner ≈ (636,159)) → the Alpha node ≈ (1023,235). With an empty mask the frame goes black; now every click you add lights up that part — a far more reliable check than the overlay.
4. **Build the mask part-by-part.** Arm **"Add Click"** (leftmost brush ≈ (332,567)). Place one click on **hair, face, torso, each hand** — watch each part appear on black. Refine: any part still transparent → one more Add Click on it; any background leak → **Subtract Click** on it. A good build order: hair → face → chest → hand.
5. **Track the whole clip** — **Track Forward and Reverse** (the **⇄** bidirectional transport icon ≈ (240,567)) covers both directions from the reference frame. Wait for the "Tracking…" dialog (~1 fps); done = green check on the **Overall Track** row.
6. **Verify** — scrub 2–3 frames; the subject stays isolated through motion. Hair against bright areas is the only soft spot.

## Input-mechanics gotchas (these ate the round-trips)
- **A `left_click_drag` registers as a single positive point at its START coordinate** — not a stroke across. Put the start point squarely on the part you want; the end barely matters. (Plain `left_click` on the viewer is unreliable — use a tiny drag.)
- **The first interaction after opening/arming often doesn't register** — if the panel still says "No Mask", just repeat it; the second one takes.
- **The palette reset arrow (↻, panel header ≈ (467,545)) does NOT clear clicks.** To start over, delete each entry via the **trash icon** in the Click list (≈ x=101; delete **bottom-up** so positions stay stable) until it reads "No Mask".
- **Don't rely on the mask overlay to confirm.** The two squares by the brushes are **Invert Mask** (filled ≈456) and **Toggle Mask Overlay** (outline ≈480); their on/off parity carries between clips and is confusing. Wire Alpha (step 3) and read the viewer instead. (An inverted/empty mask tints the *whole frame* — that's the tell.)
- **Strokes that cross the subject's edge grab background** (e.g. a face stroke that nicks the hairline pulls in the ceiling). Keep clicks well inside the subject; clean leaks with Subtract Click.

## Output & timeline gotchas
- **Transparent renders as BLACK, not a checkerboard,** when the clip is on V1 (nothing below). The alpha *is* set. To see/use it: put a background on a lower track, or **export an alpha codec (ProRes 4444 / DNxHR w/ alpha)**.
- **Magic Mask is a non-destructive color-node effect** — it never edits the timeline, and it **carries to both halves if the clip is later split**.
- The blue dots in the viewer are click-markers, not rendered output.
- A clip at the very timeline start has its reference frame at frame 0, so only forward tracking happens (Track Forward and Reverse still works).

## Where it fits
Background removal is a **compositing/VFX** step (pipeline step 4) even though Magic Mask lives on the Color page. **This is the ONE reason to open Resolve for a Palmier build** — everything else in the pipeline stays in Palmier. See [davinci-resolve.md](davinci-resolve.md) for prerequisites + the Fusion Delta Keyer route for green screen. palmier side: chroma key only (`apply_effect` `key.chroma` — confirmed on the live manifest as the sole keying effect, needs a keyable backdrop) — see [palmier-pro.md](palmier-pro.md).

**Getting the cutout back into a Palmier timeline:** render the masked clip out of Resolve as an alpha codec (**ProRes 4444** / DNxHR with alpha), then `import_media` it onto a top track in Palmier. Palmier reads the alpha; a transparent clip on V1 with nothing below renders black, which is expected.
