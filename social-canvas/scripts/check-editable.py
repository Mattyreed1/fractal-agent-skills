#!/usr/bin/env python3
"""Editable-text gate for social-canvas slides (enforces design-rule 78).

Fails (exit 1) if ANY visible text node in a slide is not inside a
`contenteditable` element. This is the deterministic check that must pass
before a Claude Code preview/gallery is declared ready: spot-checking one
headline is not enough (a non-editable .band-label/.bottom-note shipped
2026-06-17 because only the headline was verified).

Usage:  python3 check-editable.py [SLIDE_DIR_or_FILE]
Default SLIDE_DIR=/tmp/social-canvas
Exit 0 = all text editable; exit 1 = violations printed.
"""
import sys
import os
import glob
from html.parser import HTMLParser

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input",
        "link", "meta", "param", "source", "track", "wbr"}


class EditableCheck(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []      # list of {"tag":..., "editable":bool}
        self.skip = 0        # >0 while inside <script>/<style>
        self.violations = []

    def handle_starttag(self, tag, attrs):
        if tag in VOID:
            return
        d = dict(attrs)
        ce = d.get("contenteditable")
        parent_editable = self.stack[-1]["editable"] if self.stack else False
        editable = parent_editable or (ce is not None and ce.lower() != "false")
        self.stack.append({"tag": tag, "editable": editable})
        if tag in ("script", "style"):
            self.skip += 1

    def handle_startendtag(self, tag, attrs):
        pass  # self-closing element, holds no text

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if tag in ("script", "style") and self.skip > 0:
            self.skip -= 1
        if self.stack:
            self.stack.pop()

    def handle_data(self, data):
        if self.skip > 0 or not data.strip():
            return
        editable = self.stack[-1]["editable"] if self.stack else False
        if not editable:
            parent = self.stack[-1]["tag"] if self.stack else "(root)"
            self.violations.append((parent, data.strip()[:60]))


def check_file(path):
    with open(path, encoding="utf-8") as fh:
        parser = EditableCheck()
        parser.feed(fh.read())
        return parser.violations


def main():
    arg = sys.argv[1] if len(sys.argv) > 1 else "/tmp/social-canvas"
    files = [arg] if os.path.isfile(arg) else sorted(glob.glob(os.path.join(arg, "slide-*.html")))
    if not files:
        print("no slide-*.html found at %s" % arg)
        sys.exit(1)
    total = 0
    for fp in files:
        v = check_file(fp)
        if v:
            total += len(v)
            print("FAIL %s: %d non-editable text node(s)" % (os.path.basename(fp), len(v)))
            for parent, txt in v:
                print("   <%s> %r" % (parent, txt))
        else:
            print("OK   %s: all text editable" % os.path.basename(fp))
    if total:
        print("\n%d violation(s). Every visible text node must sit inside a contenteditable element (design-rule 78)." % total)
        sys.exit(1)
    print("\nAll text editable.")
    sys.exit(0)


if __name__ == "__main__":
    main()
