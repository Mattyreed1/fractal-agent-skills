#!/usr/bin/env python3
"""snap_keeps.py — turn rough keep ranges into clean, silence-snapped cut frames.

The transcript tells you WHICH phrases to keep; this tells you WHERE to cut. It builds
a dBFS envelope of the clean audio, finds silence relative to the REAL noise floor
(not a fixed -30dB, which clips word tails), and snaps each requested keep so both cuts
land in true silence, starting just before the soundwave. NEVER cut mid-soundwave.

Input keeps are rough [start,end] in CLEAN-AUDIO SOURCE SECONDS (from the transcript).
Output is project-frame [start,end] for radio_edit.py: project_frame = round(sec*fps - trim).

Usage:
  snap_keeps.py --audio <mp3> --fps 30 --trim 25 \
      --keeps-sec '[[27.0,32.5],[36.5,39.0],[58.5,63.5],[69.0,76.5]]'
Tuning: --margin 12 (dB above noise floor), --min-sil 0.12 (s), --lead 0.04, --tail 0.05 (s).
Prints, for every cut, the dB at that point — must be near the floor (proof it's in silence).
"""
import json, sys, argparse
import audio_env as ae


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--audio", required=True)
    ap.add_argument("--fps", type=float, default=30)
    ap.add_argument("--trim", type=float, default=25, help="audio clip trimStartFrame (sync offset)")
    ap.add_argument("--keeps-sec", required=True)
    ap.add_argument("--margin", type=float, default=12.0, help="dB above noise floor = silence threshold")
    ap.add_argument("--min-sil", type=float, default=0.12)
    ap.add_argument("--lead", type=float, default=0.04, help="s of silence kept before each soundwave")
    ap.add_argument("--tail", type=float, default=0.05, help="s of silence kept after each soundwave")
    ap.add_argument("--min-peak", type=float, default=18.0,
                    help="a real-speech region must peak >= threshold + this (dB); excludes clicks/breaths")
    ap.add_argument("--merge-gap", type=float, default=0.30,
                    help="gaps shorter than this are natural (stay in one keep); longer = a pause to CUT")
    ap.add_argument("--min-keep", type=float, default=0.12, help="drop emitted keeps shorter than this (s)")
    ap.add_argument("--per-phrase", action="store_true",
                    help="emit one keep PER speech phrase in each range (auto-cuts internal pauses). "
                         "Default: one keep per range (union to silence) — use when ranges are already take-level.")
    a = ap.parse_args()

    rough = json.loads(a.keeps_sec)
    an = ae.analyze(a.audio, margin_db=a.margin, min_sil_s=a.min_sil)
    db, hop, floor, thresh, dur = an["db"], an["hop_s"], an["floor"], an["thresh"], an["dur_s"]

    def region_peak(r):
        i0 = max(0, int(r[0] / hop))
        i1 = min(len(db), int(r[1] / hop) + 1)
        return float(db[i0:i1].max()) if i1 > i0 else -99.0
    speech = [r for r in an["speech"] if region_peak(r) >= thresh + a.min_peak]
    # merge real-speech regions separated by < merge_gap into phrases; longer gaps stay as cuts
    phrases = []
    for r in sorted(speech):
        if phrases and r[0] - phrases[-1][1] < a.merge_gap:
            phrases[-1][1] = r[1]
        else:
            phrases.append([r[0], r[1]])
    print(f"snap_keeps: floor {floor:.1f}dB, thresh {thresh:.1f}dB, {len(speech)} real-speech regions "
          f"-> {len(phrases)} phrases (merge_gap {a.merge_gap*1000:.0f}ms), dur {dur:.1f}s")

    def to_frame(sec):
        return round(sec * a.fps - a.trim)

    out, ok, skipped, not_sil = [], True, 0, 0
    for a0, b0 in rough:
        if a.per_phrase:
            units = [(p[0], p[1]) for p in phrases
                     if a0 <= (p[0] + p[1]) / 2 <= b0 and p[1] - p[0] >= a.min_keep]
        else:  # one keep per range: union of real-speech in the range, snapped to silence
            hits = [p for p in speech if p[0] < b0 and p[1] > a0]
            units = [(min(p[0] for p in hits), max(p[1] for p in hits))] if hits else []
        if not units:
            print(f"  [{a0:.1f},{b0:.1f}] NO speech in range; skipped"); ok = False; skipped += 1; continue
        for onset, offset in units:
            ks, ke = onset - a.lead, offset + a.tail
            if ae.db_side(db, hop, ks, 0.03, "in") > thresh or ae.db_side(db, hop, ke, 0.03, "out") > thresh:
                not_sil += 1; ok = False
            out.append([to_frame(ks), to_frame(ke)])

    # post-process: sort, merge overlapping keeps (dedup), drop fragments
    out.sort()
    merged = []
    for k in out:
        if merged and k[0] < merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], k[1])
        else:
            merged.append([k[0], k[1]])
    mf = int(a.min_keep * a.fps)
    final = [k for k in merged if k[1] - k[0] >= mf]
    print(f"  {len(rough)} ranges -> {len(out)} raw keeps -> {len(final)} after merge/drop; "
          f"{skipped} skipped, {not_sil} cuts-not-in-silence")
    print(("OK. " if ok and not final_overlaps(final) else "CHECK. ") + "KEEPS_JSON " + json.dumps(final))
    sys.exit(0 if (ok and not final_overlaps(final)) else 1)


def final_overlaps(keeps):
    return any(keeps[i + 1][0] < keeps[i][1] for i in range(len(keeps) - 1))


if __name__ == "__main__":
    main()
