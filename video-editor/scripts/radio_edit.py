#!/usr/bin/env python3
"""radio_edit.py — apply a keep-list (EDL) to the live Palmier timeline.

Edits the VIDEO track and the INDEPENDENT clean-audio track; any linked scratch
audio follows the video automatically (split/remove/move all propagate to a linked
partner). Linked-audio tracks are therefore SKIPPED here, not edited directly.

Per edited track: split at every keep boundary -> remove_clips(discards) ->
move_clips(survivors -> cumulative positions). Every edited track is cut at the
SAME project frames and re-stacked with the SAME offsets, so synced tracks stay
in lockstep.

Hard-won rules baked in (see projects/.../edit-trace.md post-mortem):
  * Identify tracks by stable ID and re-find after every mutation — track arrays
    reorder and emptied tracks auto-remove, so positional indexing corrupts state.
  * Keep the video<->scratch link intact. Splitting a linked clip makes per-segment
    pairs (distinct groups), so remove_clips takes only that pair, never a cascade.
    Do NOT remove the scratch track first — that orphans the link and one remove
    wipes the whole group.

Keep-list = ordered, non-overlapping [startFrame, endFrame] ranges in PROJECT
FRAMES. The last range's end may be "end" (resolves to each track's content end).

Usage:
  radio_edit.py --keeps '[[812,934],[1064,1140],[1766,1865],[2074,"end"]]'   # DRY-RUN
  radio_edit.py --keeps-file keeps.json --execute                            # apply
Exit: 0 ok, 2 cannot-run. Stdlib only.
"""
import json, sys, argparse, re, urllib.request, urllib.error

URL = "http://127.0.0.1:19789/mcp"


def _right_id(res):
    """Parse the new right-clip ID from a split_clip text result (first UUID after 'right clip(s):')."""
    if not isinstance(res, str):
        return None
    m = re.search(r"right clip\(s\):\s*([0-9A-Fa-f-]{36})", res)
    return m.group(1) if m else None


def die_run(msg):
    print(f"ERROR (cannot run): {msg}")
    sys.exit(2)


class MCP:
    def __init__(self, url):
        self.url, self.sid, self._id = url, None, 0

    def _post(self, payload, notify=False):
        headers = {"Content-Type": "application/json",
                   "Accept": "application/json, text/event-stream",
                   "MCP-Protocol-Version": "2025-06-18"}
        if self.sid:
            headers["mcp-session-id"] = self.sid
        req = urllib.request.Request(self.url, data=json.dumps(payload).encode(),
                                     headers=headers, method="POST")
        resp = urllib.request.urlopen(req, timeout=180)  # raises on error; callers retry/handle
        sid = resp.headers.get("mcp-session-id")
        if sid:
            self.sid = sid
        body = resp.read().decode()
        if notify:
            return None
        return self._extract(body, payload.get("id"))

    @staticmethod
    def _extract(body, want_id):
        msgs = []
        if body.lstrip()[:1] == "{":
            try: msgs.append(json.loads(body))
            except Exception: pass
        else:
            for line in body.splitlines():
                line = line.strip()
                if line.startswith("data:"):
                    chunk = line[5:].strip()
                    if chunk[:1] == "{":
                        try: msgs.append(json.loads(chunk))
                        except Exception: pass
        for m in msgs:
            if m.get("id") == want_id:
                return m
        return msgs[-1] if msgs else None

    def _reinit(self):
        self.sid = None
        self._id += 1
        self._post({"jsonrpc": "2.0", "id": self._id, "method": "initialize",
                    "params": {"protocolVersion": "2025-06-18", "capabilities": {},
                               "clientInfo": {"name": "radio_edit", "version": "2.0"}}})
        self._post({"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}}, notify=True)

    def initialize(self):
        try:
            self._reinit()
        except urllib.error.URLError as e:
            die_run(f"cannot reach Palmier MCP at {self.url} - is the app open? ({e})")

    def call(self, name, arguments):
        self._id += 1
        payload = {"jsonrpc": "2.0", "id": self._id, "method": "tools/call",
                   "params": {"name": name, "arguments": arguments}}
        m = None
        for attempt in range(3):  # OSError covers URLError + socket.timeout
            try:
                m = self._post(payload)
                break
            except OSError:
                try:
                    self._reinit()
                except OSError:
                    pass
        if m is None:
            die_run(f"tool {name} failed after retries")
        if not m or "result" not in m:
            die_run(f"tool {name} returned no result: {m}")
        res = m["result"]
        texts = [b.get("text", "") for b in res.get("content", []) if b.get("type") == "text"]
        for t in texts:
            try:
                parsed = json.loads(t)
                if isinstance(parsed, (dict, list)):
                    return parsed
            except Exception:
                continue
        if isinstance(res.get("structuredContent"), dict):
            return res["structuredContent"]
        return texts[0] if texts else res


def span(c):
    return c["startFrame"], c["startFrame"] + c["durationFrames"]


def find_track(tl, tid):
    return next((t for t in tl["tracks"] if t["id"] == tid), None)


def resolve_keeps(raw, cstart, cend):
    out = []
    for s, e in raw:
        e = cend if e == "end" else e
        s = max(s, cstart); e = min(e, cend)
        if e > s:
            out.append((s, e))
    return sorted(out)


def is_keep(seg, keeps):
    a0, b0 = span(seg)
    return any(ks <= a0 and b0 <= ke for ks, ke in keeps)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--keeps")
    ap.add_argument("--keeps-file")
    ap.add_argument("--execute", action="store_true")
    a = ap.parse_args()
    if not (a.keeps or a.keeps_file):
        die_run("provide --keeps or --keeps-file")
    raw = json.load(open(a.keeps_file)) if a.keeps_file else json.loads(a.keeps)

    mcp = MCP(URL)
    mcp.initialize()
    tl = mcp.call("get_timeline", {})
    tracks = tl.get("tracks", [])
    if not any(t.get("clips") for t in tracks):
        die_run("timeline has no clips")

    # Choose edit targets: video tracks + audio tracks with NO linkGroupId (independent).
    # Linked-audio (scratch) tracks follow the video and are skipped.
    edit_ids, skipped = [], []
    for tr in tracks:
        clips = tr.get("clips", [])
        if not clips:
            continue
        if tr["type"] == "video":
            edit_ids.append(tr["id"])
        elif tr["type"] == "audio" and not any(c.get("linkGroupId") for c in clips):
            edit_ids.append(tr["id"])
        else:
            skipped.append(tr.get("label", tr["id"]))

    mode = "EXECUTE" if a.execute else "DRY-RUN"
    print(f"radio_edit v2 [{mode}] — {len(raw)} keep ranges; "
          f"edit {len(edit_ids)} track(s); skip linked {skipped or '[]'}")

    for tid in edit_ids:
        tr = find_track(mcp.call("get_timeline", {}), tid)
        clips = tr["clips"]
        cstart = min(c["startFrame"] for c in clips)
        cend = max(span(c)[1] for c in clips)
        keeps = resolve_keeps(raw, cstart, cend)
        if not keeps:
            print(f"  [{tr['label']}] no keeps in range — skipped")
            continue
        bset = sorted({b for s, e in keeps for b in (s, e) if cstart < b < cend})
        kept = sum(e - s for s, e in keeps)
        print(f"  [{tr['label']}] {tr['type']}: span {cstart}-{cend}, {len(bset)} cut pts, "
              f"keep {kept}f / discard {cend - cstart - kept}f")
        if not a.execute:
            continue

        # 1) split at each ascending boundary. Fast path: chain on split's returned right-clip id
        # (no get_timeline per split). Fall back to a re-read whenever a return doesn't parse.
        clips0 = sorted(find_track(mcp.call("get_timeline", {}), tid)["clips"], key=lambda c: c["startFrame"])
        cur = clips0[0]["id"] if len(clips0) == 1 else None
        for b in bset:
            if cur is None:
                t = find_track(mcp.call("get_timeline", {}), tid)
                tgt = next((c for c in t["clips"] if c["startFrame"] < b < span(c)[1]), None)
                cur = tgt["id"] if tgt else None
                if cur is None:
                    continue
            res = mcp.call("split_clip", {"clipId": cur, "atFrame": b})
            cur = _right_id(res)  # right segment carries the next (larger) boundary; None -> re-read

        # 2) remove discards (linked scratch partners go with them) — chunked to keep calls small
        segs = sorted(find_track(mcp.call("get_timeline", {}), tid)["clips"], key=lambda c: c["startFrame"])
        discards = [s["id"] for s in segs if not is_keep(s, keeps)]
        for i in range(0, len(discards), 40):
            mcp.call("remove_clips", {"clipIds": discards[i:i + 40]})

        # 3) ripple-close survivors to cumulative positions (chunked; scratch follows)
        survivors = sorted(find_track(mcp.call("get_timeline", {}), tid)["clips"], key=lambda c: c["startFrame"])
        moves, pos = [], cstart
        for s in survivors:
            if s["startFrame"] != pos:
                moves.append({"clipId": s["id"], "toFrame": pos})
            pos += s["durationFrames"]
        for i in range(0, len(moves), 40):
            mcp.call("move_clips", {"moves": moves[i:i + 40]})
        print(f"    -> split {len(bset)}, removed {len(discards)}, moved {len(moves)}; final {pos - cstart}f")

    print("done." if a.execute else "dry-run only — pass --execute to apply.")


if __name__ == "__main__":
    main()
