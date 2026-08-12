#!/usr/bin/env python3
"""Audit every V1 clip boundary for mid-word / mid-speech cuts.

For each boundary between consecutive clips A|B:
- A's OUT point in source: does speech continue right up to (and past) the cut?
- B's IN point in source: does the clip start inside speech?
- The 2-frame slivers: what do they contain?

Uses RMS energy vs noise floor on the pinned source wav (16k mono).
"""
import struct, wave, math, json

WAV = "build/source.wav"  # point at your extracted full-rate audio
FPS = 30.0

# V1 clips: (id, startFrame, durationFrames, trimStartFrame)
CLIPS = [
    ("F34ABC1C", 0,    175, 334),
    ("493989E2", 175,  207, 1101),
    ("CCE8C637", 382,  131, 1454),
    ("BB242F93", 513,  60,  1603),
    ("3BDC154F", 573,  279, 1730),
    ("10A5DE21", 852,  2,   2370),
    ("76FD3775", 854,  188, 2440),
    ("F52E9173", 1042, 2,   3089),
    ("DADBECE7", 1044, 182, 3323),
    ("E8D4D746", 1226, 460, 3697),
    ("49A6D373", 1686, 161, 4497),
    ("8A44DAE5", 1847, 154, 4885),
    ("75BC3976", 2001, 44,  5191),
    ("75D1023D", 2045, 75,  5404),
    ("6A2B6110", 2120, 97,  5555),
    ("3222356A", 2217, 2,   5787),
    ("9BD60A9F", 2219, 277, 6340),
    ("61A8592D", 2496, 283, 6703),
    ("F745DAB9", 2779, 72,  7235),
]

w = wave.open(WAV, 'rb')
sr = w.getframerate()
n = w.getnframes()
raw = w.readframes(n)
w.close()
samples = struct.unpack(f"<{n}h", raw)

HOP = int(sr * 0.02)   # 20ms hop
def rms_db(t0, t1):
    a, b = max(0, int(t0*sr)), min(n, int(t1*sr))
    if b <= a: return -90.0
    s = samples[a:b]
    m = sum(x*x for x in s) / len(s)
    return 10*math.log10(m/ (32768.0**2) + 1e-12)

# noise floor: 5th percentile of 50ms windows
import random
wins = []
t = 0.0
dur = n/sr
while t < dur - 0.05:
    wins.append(rms_db(t, t+0.05))
    t += 0.25
wins.sort()
floor = wins[max(0, len(wins)//20)]
SPEECH = floor + 14.0
print(f"duration={dur:.1f}s floor={floor:.1f}dB speech_thresh={SPEECH:.1f}dB\n")

def is_speech(t):
    return rms_db(t-0.03, t+0.03) > SPEECH

def next_silence(t, max_ahead=2.5):
    """first time >= t where a 100ms window is all below thresh"""
    x = t
    while x < min(dur, t+max_ahead):
        if rms_db(x, x+0.10) < SPEECH - 4:
            return x
        x += 0.02
    return None

def prev_silence(t, max_back=2.5):
    x = t
    while x > max(0, t-max_back):
        if rms_db(x-0.10, x) < SPEECH - 4:
            return x
        x -= 0.02
    return None

print(f"{'clip':10} {'tl_range':>14} {'IN: speech?':>12} {'OUT: speech?':>13}  notes")
issues = []
for i,(cid, sf, du, tr) in enumerate(CLIPS):
    src_in = tr / FPS
    src_out = (tr + du) / FPS
    in_bad = is_speech(src_in)
    out_bad = is_speech(src_out)
    notes = []
    if du <= 4:
        e = rms_db(src_in, src_out)
        notes.append(f"SLIVER content={e:.0f}dB{' SPEECH!' if e > SPEECH else ' (quiet)'}")
    if out_bad:
        ns = next_silence(src_out)
        notes.append(f"out mid-speech; next silence +{(ns-src_out):.2f}s ({int((ns-src_out)*30)}f)" if ns else "out mid-speech; no silence within 2.5s")
    if in_bad:
        ps = prev_silence(src_in)
        notes.append(f"in mid-speech; prev silence -{(src_in-ps):.2f}s ({int((src_in-ps)*30)}f)" if ps else "in mid-speech; no silence within 2.5s back")
    flag = "⚠️" if (in_bad or out_bad or (du<=4)) else "  "
    print(f"{flag}{cid:9} [{sf:>5}..{sf+du:>5}) {str(in_bad):>12} {str(out_bad):>13}  {'; '.join(notes)}")
    if in_bad or out_bad or du <= 4:
        issues.append(cid)
print(f"\n{len(issues)} flagged: {issues}")
