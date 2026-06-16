#!/usr/bin/env python3
"""Private-info scanner for this public skills repo.

Runs in CI on every push/PR. Exits non-zero if any owner-specific / private data
is detected in tracked files, so it can never reach the public repo. Scrubbing is
a human step on a failed run — auto-rewriting prose is too risky to automate, so
this gate blocks the merge and tells you exactly what to fix.

Usage:
  private-scan.py [--root .]
To whitelist a confirmed-safe match, put a comment containing 'private-scan: allow'
on that line.
"""
import argparse
import os
import re
import sys

# (label, regex) — tuned for high-confidence owner/private signals.
# Generic product names (Convex, OpenClaw, Notion-as-a-word) are intentionally NOT flagged.
PATTERNS = [
    ("email",      re.compile(r"[A-Za-z0-9._%+-]+@(?:gmail\.com|fractalai\.agency|founderfreedom[A-Za-z.]*)", re.I)),
    ("notion-id",  re.compile(r"\b[0-9a-f]{32}\b|\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b")),
    ("vps/agent",  re.compile(r"ssh\s+molty|moltyreed_[a-z]+|focused-crocodile|/home/deploy|/home/node|hetzner", re.I)),
    ("client",     re.compile(r"\bstyleghost\b|\btulum\b|\bblackboard\b|\bmippo\b|\borbifitech\b", re.I)),
    ("local-path", re.compile(r"/Users/[A-Za-z0-9._-]+")),
    ("api-key",    re.compile(r"\bsk-[A-Za-z0-9]{20,}|\bpplx-[A-Za-z0-9]{20,}|\bxai-[A-Za-z0-9]{20,}|\bghp_[A-Za-z0-9]{20,}|\bAKIA[A-Z0-9]{16}|\bxoxb-[A-Za-z0-9-]{10,}")),
]

ALLOW = "private-scan: allow"
SKIP_DIRS = {".git", "node_modules", ".agent-board", "__pycache__", ".github/scripts"}
TEXT_EXT = {".md", ".py", ".ts", ".js", ".json", ".txt", ".yml", ".yaml", ".sh", ".html", ".css", ".toml", ".cfg", ".ini", ""}


def scan(root):
    findings = []
    for dp, dns, fns in os.walk(root):
        dns[:] = [d for d in dns if d not in SKIP_DIRS and os.path.join(os.path.relpath(dp, root), d) not in SKIP_DIRS]
        for fn in fns:
            ext = os.path.splitext(fn)[1].lower()
            if ext not in TEXT_EXT:
                continue
            p = os.path.join(dp, fn)
            try:
                with open(p, encoding="utf-8", errors="ignore") as f:
                    for i, line in enumerate(f, 1):
                        if ALLOW in line:
                            continue
                        for label, rx in PATTERNS:
                            m = rx.search(line)
                            if m:
                                findings.append((os.path.relpath(p, root), i, label, m.group(0)[:60]))
            except (OSError, UnicodeDecodeError):
                continue
    return findings


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    args = ap.parse_args()
    findings = scan(args.root)
    if not findings:
        print("private-scan: clean (no owner-specific data found)")
        return 0
    print(f"private-scan: FAILED — {len(findings)} potential private-data leak(s):\n")
    for rel, i, label, snip in findings:
        print(f"  {rel}:{i}  [{label}]  {snip}")
    print(f"\nScrub these before merging. To whitelist a confirmed-safe match, add a")
    print(f"comment containing '{ALLOW}' on that line.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
