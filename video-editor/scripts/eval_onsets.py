#!/usr/bin/env python3
"""eval_onsets.py — catch pre-speech CLICKS and dead-air at the head of each clip.

eval_cuts proves a cut lands in silence; it does NOT prove the clip starts right before the
WORD. A clip can pass eval_cuts yet open with a mouth-click/breath sitting in a long silent
lead-in (sound above the noise floor but not speech). That faint pre-speech transient shows as a
waveform before the speaker actually talks — exactly what a viewer notices. This gate flags it.

Method: for each clean-audio clip, find the SUSTAINED speech onset (energy that holds ≥150ms),
not the first sound above the floor. Flag the clip if the lead-in to that onset is long
(> --max-lead-ms) OR there is an above-threshold transient before the speech (a click/breath).

Fix when flagged: re-anchor the clip start to speech_onset - ~50ms, snapped to deep silence
(the click then lands on the discard side). snap_keeps.py does this for new cuts.

Usage: eval_onsets.py --audio clean.mp3 [--max-lead-ms 150] [--trim 25]
Exit: 0 all clean, 1 flags, 2 cannot run. Stdlib + numpy + ffmpeg + the MCP client.
"""
import sys, argparse
sys.path.insert(0, '~/the project/skills/video-editor/scripts')
from radio_edit import MCP, URL
import audio_env as ae


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--audio", required=True)
    ap.add_argument("--margin", type=float, default=12.0)
    ap.add_argument("--max-lead-ms", type=float, default=150.0)
    ap.add_argument("--click-margin", type=float, default=6.0,
                    help="a pre-speech transient counts as an audible click only if its peak is "
                         "this many dB above the silence threshold (~floor+18). Lower-level blips "
                         "(natural lips-parting noise within a tight lead) are not flagged.")
    ap.add_argument("--trim", type=float, default=25.0)
    a = ap.parse_args()

    an = ae.analyze(a.audio, margin_db=a.margin, min_sil_s=0.05)
    db, hop, floor, thresh = an["db"], an["hop_s"], an["floor"], an["thresh"]
    SPEECH = thresh + 12          # clearly speech, not a click (~ -50dB here)
    SUS = int(0.15 / hop)         # speech must hold for 150ms to count as the onset

    def onset(s0, s1):
        for i in range(int(s0 / hop), min(int(s1 / hop), len(db) - SUS)):
            if db[i] >= SPEECH and sum(1 for x in db[i:i + SUS] if x > thresh) >= 0.7 * SUS:
                return i * hop
        return None

    mcp = MCP(URL); mcp.initialize()
    tl = mcp.call("get_timeline", {})
    fps = tl.get("fps", 30)
    track = next((t for t in tl["tracks"] if t["type"] == "audio" and t.get("clips")
                  and not any(c.get("linkGroupId") for c in t["clips"])), None)
    if not track:
        print("RESULT: ERROR - no clean-audio track"); return 2
    clips = sorted(track["clips"], key=lambda c: c["startFrame"])

    flags, leads = [], []
    for k, c in enumerate(clips):
        s0 = c["trimStartFrame"] / fps
        s1 = (c["trimStartFrame"] + c["durationFrames"]) / fps
        on = onset(s0, s1)
        if on is None:
            continue
        lead_ms = (on - s0) * 1000
        leads.append(lead_ms)
        j0, j1 = int((s0 + 0.02) / hop), int((on - 0.04) / hop)
        click = any(db[i] > thresh + a.click_margin for i in range(j0, max(j0, j1)))
        if lead_ms > a.max_lead_ms or click:
            flags.append((k + 1, round(lead_ms), click))

    med = sorted(leads)[len(leads) // 2] if leads else 0
    print(f"eval_onsets: {len(clips)} clips, median lead-in to speech {med:.0f}ms, "
          f"max {max(leads):.0f}ms" if leads else "eval_onsets: no onsets")
    for k, lead, click in flags:
        print(f"  clip{k}: lead-in {lead}ms{'  +pre-speech CLICK' if click else '  (dead air at head)'}")
    print(f"RESULT: {'PASS (clean onsets)' if not flags else f'FAIL ({len(flags)} clip(s) with click/dead-air at head)'}")
    return 1 if flags else 0


if __name__ == "__main__":
    sys.exit(main())
