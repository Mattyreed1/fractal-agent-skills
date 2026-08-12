#!/bin/zsh
# check_version.sh — compare the INSTALLED Palmier Pro against the latest release and print the
# changelog delta. Palmier ships fast (multiple releases/week) and its MCP tool surface changes
# between versions, so a stale build silently makes this skill's workarounds wrong (e.g. v0.3.2
# needed a two-pass add+trim; v0.3.5 lets add_clips set trim on placement). RUN THIS at the start
# of any non-trivial Palmier session, and any time a workaround here feels heavier than it should.
#
# Sources: installed version from the app bundle Info.plist; latest + human changelog from the
# GitHub Releases API (the Sparkle appcast at SUFeedURL only lists versions, not release notes).
# Exit 0 = up to date, 1 = update available, 2 = cannot determine.
set -uo pipefail
PLIST=/Applications/PalmierPro.app/Contents/Info.plist
REPO=palmier-io/palmier-pro

inst=$(/usr/bin/defaults read "$PLIST" CFBundleShortVersionString 2>/dev/null || echo "")
[ -z "$inst" ] && { echo "Palmier Pro not found at /Applications/PalmierPro.app"; exit 2; }
echo "installed: v$inst (build $(/usr/bin/defaults read "$PLIST" CFBundleVersion 2>/dev/null))"

latest=$(curl -fsSL --max-time 20 -H "Accept: application/vnd.github+json" \
  "https://api.github.com/repos/$REPO/releases/latest" 2>/dev/null \
  | python3 -c "import sys,json;print(json.load(sys.stdin).get('tag_name','') or '')" 2>/dev/null)
[ -z "$latest" ] && { echo "could not reach GitHub Releases (offline / rate-limited)"; exit 2; }
echo "latest:    $latest"

if [ "v$inst" = "$latest" ]; then echo "UP TO DATE"; exit 0; fi

echo
echo "OUT OF DATE — release notes from your version up to latest:"
curl -fsSL --max-time 20 -H "Accept: application/vnd.github+json" \
  "https://api.github.com/repos/$REPO/releases?per_page=30" 2>/dev/null \
  | INST="$inst" python3 -c "
import sys, json, os
def key(t):
    try: return [int(x) for x in t.lstrip('v').split('.')]
    except Exception: return None
ik = key(os.environ['INST'])
rels = json.load(sys.stdin)
for r in reversed(rels):                       # oldest -> newest
    k = key(r.get('tag_name',''))
    if k and ik and k > ik:
        print('\n### ' + r.get('tag_name',''))
        print((r.get('body') or '').strip())
"
echo
echo "Update: Palmier menu > Check for Updates (Sparkle), or download the .dmg from"
echo "  https://github.com/$REPO/releases/latest"
echo "After updating, RELAUNCH the app — the MCP tool surface (new tools / new params)"
echo "only changes on a fresh launch. Re-derive capabilities from the LIVE tool schemas, not memory."
exit 1
