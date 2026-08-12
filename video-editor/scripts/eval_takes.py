#!/usr/bin/env python3
"""eval_takes.py — catch DUPLICATE / repeated takes left on the timeline after a radio edit.

eval_cuts/score_cuts check cut *quality* (no mid-word cuts, tight edges); they are blind to
*content* — a clip that plays the same line twice, or two adjacent clips that are two takes of
the same line. That is the failure this gate catches. Run it after every radio edit, alongside
the cut-quality gates.

Method (avoids the reconstruction double-count artifact):
  * Read the clean-audio track's clips (sorted). Each clip plays source [trim, trim+dur] seconds.
  * Assign each transcript segment to the ONE clip whose source window contains the segment's
    midpoint (a segment spanning two clips is counted once, where most of it sits).
  * INTERNAL repeat: a clip with >=2 assigned segments where consecutive segments share a long
    common word-prefix (a restart) or are near-identical (the line said twice in one clip).
  * ADJACENT repeat: consecutive clips whose assigned text shares a long common prefix and
    similar length (the same line kept as two separate takes).

Needs a transcript of the clean audio (source seconds): rows [text, start, end, ...]. Fetch with
get_transcript.py (windowed inspect_media) and pass via --transcript.

Usage: eval_takes.py --transcript /tmp/transcript.json [--trim 25] [--prefix 3] [--adj-prefix 4]
Exit: 0 no duplicates, 1 duplicates found, 2 cannot run. Stdlib + the MCP client.
"""
import sys, json, re, argparse
sys.path.insert(0, '~/the project/skills/video-editor/scripts')
from radio_edit import MCP, URL


def norm(s):
    return re.sub(r'[^a-z0-9 ]', '', s.lower()).split()


def common_prefix(a, b):
    n = 0
    for x, y in zip(a, b):
        if x == y:
            n += 1
        else:
            break
    return n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--transcript", required=True)
    ap.add_argument("--trim", type=float, default=25)
    ap.add_argument("--prefix", type=int, default=3, help="min shared word-prefix for an INTERNAL restart")
    ap.add_argument("--adj-prefix", type=int, default=4, help="min shared word-prefix for an ADJACENT dup")
    a = ap.parse_args()

    segs = sorted(json.load(open(a.transcript)), key=lambda r: r[1])  # [text,start,end,...]
    mcp = MCP(URL); mcp.initialize()
    tl = mcp.call("get_timeline", {})
    fps = tl.get("fps", 30)
    track = next((t for t in tl["tracks"] if t["type"] == "audio" and t.get("clips")
                  and not any(c.get("linkGroupId") for c in t["clips"])), None)
    if not track:
        print("RESULT: ERROR - no clean-audio track"); return 2
    clips = sorted(track["clips"], key=lambda c: c["startFrame"])

    # source window per clip; assign segments by midpoint
    wins = []
    for c in clips:
        s0 = (c["trimStartFrame"]) / fps + a.trim / fps if False else c["trimStartFrame"] / fps
        s1 = (c["trimStartFrame"] + c["durationFrames"]) / fps
        wins.append((s0, s1))
    assigned = [[] for _ in clips]
    for r in segs:
        t, sa, sb = r[0], r[1], r[2]
        mid = (sa + sb) / 2
        for i, (s0, s1) in enumerate(wins):
            if s0 <= mid <= s1:
                assigned[i].append(t); break

    # INTERNAL stutter: a phrase that repeats WITHIN one clip's text. This is the case the old
    # version missed — a restart like "but what happens when you're, but what happens when..." is
    # a single transcript segment, so a cross-segment check never sees it. Tokenize the clip's
    # whole text and look for any repeated >=3-word phrase.
    def repeated_phrase(toks):
        for L in range(6, 2, -1):
            for s in range(len(toks) - L):
                ph = toks[s:s + L]
                for t in range(s + 1, len(toks) - L + 1):
                    if toks[t:t + L] == ph:
                        return " ".join(ph)
        return None

    internal, adjacent = [], []
    for i, segs_i in enumerate(assigned):
        toks = norm(" ".join(segs_i))
        ph = repeated_phrase(toks)
        if ph:
            internal.append((i + 1, ph, " ".join(segs_i)))
    for i in range(len(clips) - 1):
        x = norm(" ".join(assigned[i])); y = norm(" ".join(assigned[i + 1]))
        if x and y and common_prefix(x, y) >= a.adj_prefix and abs(len(x) - len(y)) <= 6:
            adjacent.append((i + 1, i + 2, " ".join(assigned[i])[:60], " ".join(assigned[i + 1])[:60]))

    print(f"eval_takes: {len(clips)} clips, {len(segs)} transcript segments")
    if internal:
        print(f"\nINTERNAL repeats (clip plays a line ~twice / restart) — {len(internal)}:")
        for k, s1, s2 in internal:
            print(f"  clip{k}: \"{s1[:45]}\" | \"{s2[:45]}\"")
    if adjacent:
        print(f"\nADJACENT duplicate takes (same line in consecutive clips) — {len(adjacent)}:")
        for i, j, ti, tj in adjacent:
            print(f"  clip{i}+{j}: \"{ti}\" ~ \"{tj}\"")
    n = len(internal) + len(adjacent)
    print(f"\nRESULT: {'PASS (no duplicate takes)' if n == 0 else f'FAIL ({n} duplicate-take site(s))'}")
    return 0 if n == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
