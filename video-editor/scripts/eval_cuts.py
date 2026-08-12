#!/usr/bin/env python3
"""eval_cuts.py — verify EVERY cut on the timeline lands in silence (no mid-word clips).

For each clip on the clean-audio track, the source in-point (trimStartFrame) and
out-point (trimStartFrame+durationFrames) are where the audio was cut. This decodes the
clean audio, builds a dBFS envelope, and checks the level at every cut is at/below the
noise-floor-relative silence threshold. Any cut above it = a word clipped mid-waveform = FAIL.

This is the check eval_sync.py was missing. Run after every radio_edit.

Usage: eval_cuts.py --audio <clean.mp3> [--margin 12] [--win 0.02]
Exit: 0 all cuts clean, 1 a cut is mid-waveform, 2 cannot run. Stdlib + numpy + ffmpeg.
"""
import json, sys, argparse, urllib.request, urllib.error
import audio_env as ae

URL = "http://127.0.0.1:19789/mcp"


def die_run(m):
    print(f"RESULT: ERROR - {m}"); sys.exit(2)


class MCP:
    def __init__(self, url):
        self.url, self.sid, self._id = url, None, 0

    def _post(self, payload, notify=False):
        h = {"Content-Type": "application/json", "Accept": "application/json, text/event-stream",
             "MCP-Protocol-Version": "2025-06-18"}
        if self.sid:
            h["mcp-session-id"] = self.sid
        req = urllib.request.Request(self.url, data=json.dumps(payload).encode(), headers=h, method="POST")
        try:
            resp = urllib.request.urlopen(req, timeout=60)
        except urllib.error.URLError as e:
            die_run(f"cannot reach Palmier MCP ({e})")
        sid = resp.headers.get("mcp-session-id")
        if sid:
            self.sid = sid
        body = resp.read().decode()
        if notify:
            return None
        msgs = []
        if body.lstrip()[:1] == "{":
            try: msgs.append(json.loads(body))
            except Exception: pass
        else:
            for ln in body.splitlines():
                ln = ln.strip()
                if ln.startswith("data:") and ln[5:].strip()[:1] == "{":
                    try: msgs.append(json.loads(ln[5:].strip()))
                    except Exception: pass
        for m in msgs:
            if m.get("id") == payload.get("id"):
                return m
        return msgs[-1] if msgs else None

    def initialize(self):
        self._id += 1
        self._post({"jsonrpc": "2.0", "id": self._id, "method": "initialize",
                    "params": {"protocolVersion": "2025-06-18", "capabilities": {},
                               "clientInfo": {"name": "eval_cuts", "version": "1.0"}}})
        self._post({"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}}, notify=True)

    def call(self, name, args):
        self._id += 1
        m = self._post({"jsonrpc": "2.0", "id": self._id, "method": "tools/call",
                        "params": {"name": name, "arguments": args}})
        if not m or "result" not in m:
            die_run(f"{name} no result: {m}")
        for b in m["result"].get("content", []):
            if b.get("type") == "text":
                try:
                    p = json.loads(b["text"])
                    if isinstance(p, (dict, list)):
                        return p
                except Exception:
                    continue
        return m["result"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--audio", required=True)
    ap.add_argument("--margin", type=float, default=12.0)
    ap.add_argument("--win", type=float, default=0.02, help="+/- window around a cut to test (s)")
    a = ap.parse_args()

    mcp = MCP(URL); mcp.initialize()
    tl = mcp.call("get_timeline", {})
    fps = tl.get("fps", 30)
    # clean audio track = audio track whose clips have no linkGroupId
    track = next((t for t in tl["tracks"]
                  if t["type"] == "audio" and t.get("clips") and not any(c.get("linkGroupId") for c in t["clips"])), None)
    if not track:
        print("RESULT: FAIL - no independent clean-audio track found"); return 1
    clips = sorted(track["clips"], key=lambda c: c["startFrame"])

    an = ae.analyze(a.audio, margin_db=a.margin)
    db, hop, floor, thresh, dur = an["db"], an["hop_s"], an["floor"], an["thresh"], an["dur_s"]

    # collect cut points (source seconds): each clip's in and out, skipping file edges (~0 / ~dur)
    cuts = []
    for c in clips:
        src_in = c["trimStartFrame"] / fps
        src_out = (c["trimStartFrame"] + c["durationFrames"]) / fps
        for label, t in (("in", src_in), ("out", src_out)):
            if t <= 0.05 or t >= dur - 0.05:
                continue
            cuts.append((c["id"][:8], label, t))

    print(f"eval_cuts: floor {floor:.1f}dB, silence threshold {thresh:.1f}dB, "
          f"{len(clips)} clips, {len(cuts)} interior cuts (discard-side window {a.win*1000:.0f}ms)")
    bad = 0
    for cid, label, t in cuts:
        d = ae.db_side(db, hop, t, a.win, label)  # 'in' looks before the cut, 'out' after
        if d > thresh:
            bad += 1
            print(f"  CLIPPED clip {cid} {label} @ {t:7.3f}s : discard-side {d:6.1f}dB  (> {thresh:.1f})")
    if bad == 0:
        print(f"  all {len(cuts)} cuts <= {thresh:.1f}dB (in silence)")
    print(f"RESULT: {'PASS' if bad == 0 else 'FAIL'} ({bad} mid-waveform cut(s))")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
