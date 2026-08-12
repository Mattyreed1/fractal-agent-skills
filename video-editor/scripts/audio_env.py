#!/usr/bin/env python3
"""audio_env.py — shared amplitude-envelope analysis for clean radio-edit cuts.

Why this exists: ffmpeg silencedetect with a fixed dB threshold cuts mid-word — a
word's soft attack and fricative tail (e.g. the "...sss" of "crossroads") sit well
below -30dB but far above the true noise floor, so they ARE audible waveform. We must
detect silence RELATIVE TO THE REAL NOISE FLOOR and only ever cut where the envelope
is at that floor.

Decodes the audio to mono PCM via ffmpeg, builds a dBFS envelope, estimates the noise
floor from the quietest frames, and derives silence/speech regions. Needs numpy + ffmpeg.
"""
import subprocess, math, array


def decode_pcm(audio_path, sr=16000):
    raw = subprocess.run(
        ["ffmpeg", "-hide_banner", "-loglevel", "error", "-i", audio_path,
         "-ac", "1", "-ar", str(sr), "-f", "s16le", "-"],
        capture_output=True).stdout
    a = array.array("h")
    a.frombytes(raw)
    import numpy as np
    return np.asarray(a, dtype=np.float64), sr


def envelope_db(samples, sr, hop_s=0.01):
    import numpy as np
    hop = max(1, int(sr * hop_s))
    n = len(samples) // hop
    if n == 0:
        return np.array([]), hop_s
    trimmed = samples[:n * hop].reshape(n, hop)
    rms = np.sqrt(np.mean(trimmed ** 2, axis=1))
    db = 20 * np.log10(np.maximum(rms, 1e-9) / 32768.0)
    return db, hop_s


def noise_floor_db(db, pct=5.0):
    import numpy as np
    if len(db) == 0:
        return -90.0
    return float(np.percentile(db, pct))


def silence_regions(db, hop_s, thresh_db, min_sil_s):
    """Contiguous runs below thresh_db lasting >= min_sil_s, as (start_s, end_s)."""
    regions, i, n = [], 0, len(db)
    while i < n:
        if db[i] < thresh_db:
            j = i
            while j < n and db[j] < thresh_db:
                j += 1
            if (j - i) * hop_s >= min_sil_s:
                regions.append((i * hop_s, j * hop_s))
            i = j
        else:
            i += 1
    return regions


def speech_regions(db, hop_s, thresh_db, min_sil_s, dur_s):
    """Spans between silence regions = phrases (internal sub-min_sil dips stay attached)."""
    sil = silence_regions(db, hop_s, thresh_db, min_sil_s)
    sp, prev = [], 0.0
    for s, e in sil:
        if s > prev:
            sp.append((prev, s))
        prev = e
    if prev < dur_s:
        sp.append((prev, dur_s))
    return sp


def analyze(audio_path, noise_pct=5.0, margin_db=12.0, min_sil_s=0.12, hop_s=0.01):
    """One-call: returns dict with db envelope, hop, floor, threshold, dur, speech/silence regions."""
    samples, sr = decode_pcm(audio_path)
    db, hop_s = envelope_db(samples, sr, hop_s)
    dur_s = len(samples) / sr
    floor = noise_floor_db(db, noise_pct)
    thresh = floor + margin_db
    return {
        "db": db, "hop_s": hop_s, "dur_s": dur_s, "floor": floor, "thresh": thresh,
        "silence": silence_regions(db, hop_s, thresh, min_sil_s),
        "speech": speech_regions(db, hop_s, thresh, min_sil_s, dur_s),
    }


def db_at(db, hop_s, t_s, win_s=0.02):
    """Max dBFS in a +/- win_s window around t_s (for checking a cut sits in silence)."""
    import numpy as np
    if len(db) == 0:
        return -90.0
    lo = max(0, int((t_s - win_s) / hop_s))
    hi = min(len(db), int((t_s + win_s) / hop_s) + 1)
    if hi <= lo:
        return float(db[min(max(0, int(t_s / hop_s)), len(db) - 1)])
    return float(np.max(db[lo:hi]))


def db_side(db, hop_s, t_s, win_s, side):
    """Max dBFS on the DISCARD side of a cut: 'in' (clip start) looks BEFORE the cut,
    'out' (clip end) looks AFTER it. A clean cut is silent on its discard side; a small
    lead-in/tail of kept audio on the other side is fine and not flagged."""
    import numpy as np
    if len(db) == 0:
        return -90.0
    lo, hi = (t_s - win_s, t_s) if side == "in" else (t_s, t_s + win_s)
    i0 = max(0, int(lo / hop_s))
    i1 = min(len(db), int(hi / hop_s) + 1)
    if i1 <= i0:
        i1 = min(len(db), i0 + 1)
    return float(np.max(db[i0:i1])) if i1 > i0 else -90.0
