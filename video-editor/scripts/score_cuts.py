#!/usr/bin/env python3
"""score_cuts.py — strict 0-100 scoring of every cut on the timeline.

Goes beyond eval_cuts' pass/fail. For each interior cut on the clean-audio track it grades:
  * CLIP SAFETY (hard gate): the discard side must be at the noise floor. Any audible
    waveform on the discard side = a word sliced = the cut scores 0 and the run is NOT perfect.
  * EDGE TIGHTNESS: the silence kept on the KEPT side (lead-in before a clip's first word /
    tail after its last word). Ideal 30-110ms — long enough not to clip, short enough not to
    sound like a pause. Too long = dead air / "started too early"; too short = clip risk.
  * SILENCE DEPTH: how far below threshold the cut sits (deeper = safer).
Plus, per edited clip (< --max-clip-s), the longest internal silence (an uncut pause/breath).

PERFECT = zero clip violations, every cut edge-score >= --pass (default 90), no internal
dead air over --dead-ms. Prints a per-cut table so you can see exactly what to fix.

Usage: score_cuts.py --audio <clean.mp3> [--margin 12] [--pass 90] [--dead-ms 200] [--max-clip-s 12]
Exit: 0 perfect, 1 not perfect, 2 cannot run. Stdlib + numpy + ffmpeg.
"""
import json, sys, argparse, urllib.request, urllib.error
import numpy as np
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
                               "clientInfo": {"name": "score_cuts", "version": "1.0"}}})
        self._post({"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}}, notify=True)

    def call(self, name, args):
        self._id += 1
        m = self._post({"jsonrpc": "2.0", "id": self._id, "method": "tools/call",
                        "params": {"name": name, "arguments": args}})
        if not m or "result" not in m:
            die_run(f"{name} no result")
        for b in m["result"].get("content", []):
            if b.get("type") == "text":
                try:
                    p = json.loads(b["text"])
                    if isinstance(p, (dict, list)):
                        return p
                except Exception:
                    continue
        return m["result"]


def kept_gap_ms(db, hop, t, side, thresh, maxscan=0.6):
    """Silence on the KEPT side: in-cut -> ms until first speech after t; out-cut -> ms since last speech before t."""
    n = len(db)
    if side == "in":
        i = max(0, int(t / hop)); end = min(n, int((t + maxscan) / hop))
        while i < end and db[i] <= thresh:
            i += 1
        return (i * hop - t) * 1000.0
    else:
        i = min(n, int(t / hop)); lo = max(0, int((t - maxscan) / hop))
        while i > lo and db[i - 1] <= thresh:
            i -= 1
        return (t - i * hop) * 1000.0


def edge_score(gap_ms):
    """100 in the ideal band; ramps down for too-tight (clip risk) or too-long (dead air)."""
    LO, HI = 30.0, 110.0
    if gap_ms < 0:
        gap_ms = 0
    if gap_ms < LO:
        return max(55.0, 55.0 + 45.0 * (gap_ms / LO))      # 55 at 0ms -> 100 at LO
    if gap_ms <= HI:
        return 100.0
    return max(0.0, 100.0 - (gap_ms - HI) * 0.5)            # -0.5/ms over HI -> 0 at 310ms


def longest_internal_silence_ms(db, hop, t0, t1, thresh):
    i0, i1 = max(0, int(t0 / hop)), min(len(db), int(t1 / hop))
    run = best = 0
    for i in range(i0, i1):
        if db[i] <= thresh:
            run += 1; best = max(best, run)
        else:
            run = 0
    return best * hop * 1000.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--audio", required=True)
    ap.add_argument("--margin", type=float, default=12.0)
    ap.add_argument("--win", type=float, default=0.03, help="discard-side window (s)")
    ap.add_argument("--pass", dest="passv", type=float, default=90.0, help="min per-cut edge score to be perfect")
    ap.add_argument("--dead-ms", type=float, default=300.0, help="max allowed internal silence in an edited clip")
    ap.add_argument("--max-clip-s", type=float, default=12.0, help="clips shorter than this are 'edited' (dead-air checked)")
    a = ap.parse_args()

    mcp = MCP(URL); mcp.initialize()
    tl = mcp.call("get_timeline", {})
    fps = tl.get("fps", 30)
    track = next((t for t in tl["tracks"]
                  if t["type"] == "audio" and t.get("clips") and not any(c.get("linkGroupId") for c in t["clips"])), None)
    if not track:
        print("RESULT: FAIL - no clean-audio track"); return 1
    clips = sorted(track["clips"], key=lambda c: c["startFrame"])

    an = ae.analyze(a.audio, margin_db=a.margin)
    db, hop, floor, thresh, dur = an["db"], an["hop_s"], an["floor"], an["thresh"], an["dur_s"]

    cuts = []
    for c in clips:
        si = c["trimStartFrame"] / fps
        so = (c["trimStartFrame"] + c["durationFrames"]) / fps
        if si > 0.05 and si < dur - 0.05:
            cuts.append((c["id"][:8], "in", si))
        if so > 0.05 and so < dur - 0.05:
            cuts.append((c["id"][:8], "out", so))

    print(f"score_cuts: floor {floor:.1f}dB, thresh {thresh:.1f}dB, {len(clips)} clips, {len(cuts)} cuts")
    print(f"{'clip':10s}{'side':5s}{'t(s)':>9s}{'discard':>9s}{'gap_ms':>8s}{'score':>7s}  notes")
    clips_perfect, scores = True, []
    for cid, side, t in cuts:
        dd = ae.db_side(db, hop, t, a.win, side)
        clipped = dd > thresh
        gap = kept_gap_ms(db, hop, t, side, thresh)
        s = 0.0 if clipped else edge_score(gap)
        scores.append(s)
        notes = ""
        if clipped:
            notes = "CLIP — discard side not silent"; clips_perfect = False
        elif s < a.passv:
            notes = ("dead air / too early" if gap > 110 else "too tight"); clips_perfect = False
        print(f"{cid:10s}{side:5s}{t:9.3f}{dd:8.1f}dB{gap:8.0f}{s:7.0f}  {notes}")

    # internal dead air on edited (short) clips
    dead_flags = []
    for c in clips:
        dframes = c["durationFrames"]
        if dframes / fps > a.max_clip_s:
            continue
        si = c["trimStartFrame"] / fps
        so = (c["trimStartFrame"] + c["durationFrames"]) / fps
        dead = longest_internal_silence_ms(db, hop, si + 0.12, so - 0.12, thresh)
        if dead > a.dead_ms:
            dead_flags.append((c["id"][:8], dead))
    for cid, dead in dead_flags:
        print(f"  internal dead air in clip {cid}: {dead:.0f}ms (> {a.dead_ms:.0f})")

    overall = min(scores) if scores else 0
    avg = sum(scores) / len(scores) if scores else 0
    perfect = clips_perfect and not dead_flags and (overall >= a.passv)
    print(f"OVERALL: min {overall:.0f}, avg {avg:.0f}; "
          f"{sum(1 for s in scores if s == 0)} clipped, {len(dead_flags)} dead-air")
    print(f"RESULT: {'PERFECT' if perfect else 'NOT PERFECT'}")
    return 0 if perfect else 1


if __name__ == "__main__":
    sys.exit(main())
