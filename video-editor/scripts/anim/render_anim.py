#!/usr/bin/env python3
"""Deterministic frame-stepped HTML animation -> video renderer.

The HTML must define:
  window.TOTAL_FRAMES  (int)
  window.MOTION_RANGES ([[a,b],...] frame ranges with motion; frames outside are
                        holds and get file-copied from the previous frame)
  window.seek(f)       (sets ALL animated styles for frame f, deterministically)

Usage:
  python3 render_anim.py graphic.html out.mov --w 1080 --h 1920 --alpha
  python3 render_anim.py graphic.html out.mp4 --w 1080 --h 960
"""
import argparse, os, pathlib, shutil, subprocess, sys, tempfile
from playwright.sync_api import sync_playwright

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("html"); ap.add_argument("out")
    ap.add_argument("--w", type=int, default=1080)
    ap.add_argument("--h", type=int, default=1920)
    ap.add_argument("--alpha", action="store_true")
    ap.add_argument("--fps", type=int, default=30)
    a = ap.parse_args()

    html = pathlib.Path(a.html).resolve()
    out = pathlib.Path(a.out).resolve()
    seqdir = pathlib.Path(tempfile.mkdtemp(prefix="anim_"))

    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": a.w, "height": a.h}, device_scale_factor=1)
        pg.goto(f"file://{html}", wait_until="networkidle")
        pg.evaluate("document.fonts.ready")
        pg.wait_for_timeout(300)
        total = pg.evaluate("window.TOTAL_FRAMES")
        ranges = pg.evaluate("window.MOTION_RANGES || null") or [[0, total]]
        prev = None
        for f in range(total):
            path = seqdir / f"f{f:05d}.png"
            moving = f == 0 or any(lo <= f < hi for lo, hi in ranges)
            if moving:
                pg.evaluate(f"window.seek({f})")
                pg.screenshot(path=str(path), omit_background=a.alpha)
                prev = path
            else:
                shutil.copyfile(prev, path)
            if f % 30 == 0:
                print(f"  frame {f}/{total}", flush=True)
        b.close()

    if a.alpha:
        vc = ["-c:v", "prores_ks", "-profile:v", "4444", "-pix_fmt", "yuva444p10le", "-vendor", "apl0"]
    else:
        vc = ["-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p"]
    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
           "-framerate", str(a.fps), "-i", str(seqdir / "f%05d.png"), *vc, str(out)]
    subprocess.run(cmd, check=True)
    shutil.rmtree(seqdir)
    print(f"OK {out} ({total}f @ {a.fps}fps, alpha={a.alpha})")

if __name__ == "__main__":
    main()
