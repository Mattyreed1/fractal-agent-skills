#!/usr/bin/env python3
"""eval_sync.py — verify a Palmier Pro double-system audio/video sync was done right.

Connects to the running Palmier Pro app's MCP server over HTTP, auto-detects the
synced clips, and asserts:
  1. A source video clip is on the timeline.
  2. The camera scratch audio (linked to the video, shared linkGroupId) is muted (volume 0).
  3. A separate, audible clean-audio clip exists and was advanced (trimStartFrame > 0).
  4. Lip-sync: matched transcript words in the video clip vs the clean-audio clip
     (clip-scoped inspect_media -> project frames) land within TOL_FRAMES of each other.

Exit codes: 0 = PASS, 1 = FAIL (sync wrong/incomplete), 2 = could not run
(app not open, MCP unreachable, or no clips). Stdlib only.
"""
import json, sys, urllib.request, urllib.error
from collections import Counter

URL = "http://127.0.0.1:19789/mcp"
TOL_FRAMES = 5
WINDOW = (0, 90)  # source-seconds window to transcribe for the sync check


def die_run(msg):
    print(f"RESULT: ERROR - {msg}")
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
        try:
            resp = urllib.request.urlopen(req, timeout=30)
        except urllib.error.URLError as e:
            die_run(f"cannot reach Palmier MCP at {self.url} - is the app open? ({e})")
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
            try:
                msgs.append(json.loads(body))
            except Exception:
                pass
        else:  # SSE: lines of "data: {json}"
            for line in body.splitlines():
                line = line.strip()
                if line.startswith("data:"):
                    chunk = line[5:].strip()
                    if chunk[:1] == "{":
                        try:
                            msgs.append(json.loads(chunk))
                        except Exception:
                            pass
        for m in msgs:
            if m.get("id") == want_id:
                return m
        return msgs[-1] if msgs else None

    def initialize(self):
        self._id += 1
        self._post({"jsonrpc": "2.0", "id": self._id, "method": "initialize",
                    "params": {"protocolVersion": "2025-06-18", "capabilities": {},
                               "clientInfo": {"name": "eval_sync", "version": "1.0"}}})
        self._post({"jsonrpc": "2.0", "method": "notifications/initialized",
                    "params": {}}, notify=True)

    def call(self, name, arguments):
        self._id += 1
        m = self._post({"jsonrpc": "2.0", "id": self._id, "method": "tools/call",
                        "params": {"name": name, "arguments": arguments}})
        if not m or "result" not in m:
            die_run(f"tool {name} returned no result: {m}")
        res = m["result"]
        for block in res.get("content", []):
            if block.get("type") == "text":
                try:
                    parsed = json.loads(block["text"])
                    if isinstance(parsed, (dict, list)):
                        return parsed
                except Exception:
                    continue
        if isinstance(res.get("structuredContent"), dict):
            return res["structuredContent"]
        return res


def _norm(w):
    return "".join(c for c in w.lower() if c.isalnum())


def _words(payload):
    src = payload.get("transcription", payload)  # video wraps under "transcription"; audio does not
    out = []
    for t in src.get("words", []):
        if len(t) >= 2 and _norm(t[0]):
            out.append((_norm(t[0]), float(t[1])))
    return out


def main():
    mcp = MCP(URL)
    mcp.initialize()
    tl = mcp.call("get_timeline", {})

    clips = []
    for tr in tl.get("tracks", []):
        for c in tr.get("clips", []):
            d = dict(c)
            d["_tt"] = tr.get("type")
            clips.append(d)

    video = next((c for c in clips
                  if c.get("_tt") == "video" and c.get("mediaType", "video") != "audio"), None)
    if not video:
        print("RESULT: FAIL - no video clip on the timeline")
        return 1
    link = video.get("linkGroupId")
    auds = [c for c in clips if c.get("mediaType") == "audio" or c.get("_tt") == "audio"]
    scratch = next((c for c in auds if link and c.get("linkGroupId") == link), None)
    clean = next((c for c in auds if not (link and c.get("linkGroupId") == link)), None)

    fails, oks = [], []

    if scratch is None:
        fails.append("camera scratch audio (linked to video) not found")
    elif scratch.get("volume", 1.0) not in (0, 0.0):
        fails.append(f"scratch audio not muted (volume={scratch.get('volume')}, want 0)")
    else:
        oks.append("scratch audio muted (volume 0)")

    if clean is None:
        fails.append("clean audio clip (separate, independent) not found")
    else:
        if clean.get("volume", 1.0) in (0, 0.0):
            fails.append("clean audio is muted - should be audible")
        else:
            oks.append("clean audio audible")
        if clean.get("trimStartFrame", 0) > 0:
            oks.append(f"clean audio advanced (trimStartFrame={clean['trimStartFrame']})")
        else:
            fails.append("clean audio not advanced (trimStartFrame missing/0) - offset not applied")

    if video and clean:
        vw = _words(mcp.call("inspect_media", {"mediaRef": video["mediaRef"], "clipId": video["id"],
                                               "startSeconds": WINDOW[0], "endSeconds": WINDOW[1],
                                               "wordTimestamps": True}))
        cw = _words(mcp.call("inspect_media", {"mediaRef": clean["mediaRef"], "clipId": clean["id"],
                                               "startSeconds": WINDOW[0], "endSeconds": WINDOW[1],
                                               "wordTimestamps": True}))
        vc, cc = Counter(w for w, _ in vw), Counter(w for w, _ in cw)
        vmap = {w: f for w, f in vw if vc[w] == 1}
        cmap = {w: f for w, f in cw if cc[w] == 1}
        deltas = sorted(abs(vmap[w] - cmap[w]) for w in vmap if w in cmap)
        if len(deltas) < 3:
            fails.append(f"sync check inconclusive: only {len(deltas)} shared unique words")
        else:
            med = deltas[len(deltas) // 2]
            (oks if med <= TOL_FRAMES else fails).append(
                f"lip-sync median |delta|={med:.0f}f over {len(deltas)} words "
                f"({'<=' if med <= TOL_FRAMES else '>'}{TOL_FRAMES}f)")

    print("PALMIER AUDIO/VIDEO SYNC EVAL")
    for o in oks:
        print(f"  PASS  {o}")
    for f in fails:
        print(f"  FAIL  {f}")
    if fails:
        print("RESULT: FAIL")
        return 1
    print("RESULT: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
