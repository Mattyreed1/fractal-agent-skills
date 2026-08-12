#!/bin/bash
# Publish a finished video + thumbnail to the Fractal AI Drive delivery folders.
#
# WRITES TO THE MOUNTED DRIVE FOLDER, NOT THE API. The API updates the CLOUD copy;
# the folder mounted on the user's Mac is a SECOND copy and does not reliably pick that
# change up. On 2026-08-12 they opened marketing/video in Finder and got a three-cuts-old
# file while the API reported the new one present and byte-verified. Both were true.
# Write the copy the human opens; upward sync is reliable, downward is not.
#
# Usage: publish_delivery.sh <slug> <master.mp4> <thumbnail.png>
#   e.g. publish_delivery.sh ai-notetaker-7-5-hours \
#          assets/renders/ai-notetaker-hook-v8-cutout-m14.mp4 \
#          assets/renders/ai-notetaker-7-5-hours-thumbnail.png
set -euo pipefail

SLUG="${1:?slug required}"; MASTER="${2:?master mp4 required}"; THUMB="${3:?thumbnail png required}"
# NOTE: "Business   Career" contains THREE spaces. Quote every expansion.
DRIVE="$HOME/Library/CloudStorage/GoogleDrive-<YOUR_GOOGLE_ACCOUNT>/My Drive/Business   Career/Entrepreneurship/Fractal AI Agency/marketing"
VID_DIR="$DRIVE/video"; THUMB_DIR="$DRIVE/images/thumbnails"

for d in "$VID_DIR" "$THUMB_DIR"; do
  [ -d "$d" ] || { echo "FAIL: delivery folder missing — is Google Drive mounted?"; echo "  $d"; exit 1; }
done
for f in "$MASTER" "$THUMB"; do [ -f "$f" ] || { echo "FAIL: no such file: $f"; exit 1; }; done

# G16 guard — refuse to publish a master that was never loudness-mastered.
LUFS=$(ffmpeg -hide_banner -nostats -i "$MASTER" -af ebur128 -f null - 2>&1 \
       | awk '/^ *I: /{v=$2} END{print v}')
if [ -n "$LUFS" ] && awk -v l="$LUFS" 'BEGIN{exit !(l < -15.5 || l > -12.5)}'; then
  echo "FAIL (G16): master is ${LUFS} LUFS, outside -14 +/-1.5. Master it before publishing."; exit 1
fi

cp "$MASTER" "$VID_DIR/${SLUG}-final.mp4"
cp "$THUMB"  "$THUMB_DIR/${SLUG}-thumbnail.png"

# G19 — verify on the MOUNTED path, never on an upload response.
ok=1
for pair in "$MASTER|$VID_DIR/${SLUG}-final.mp4" "$THUMB|$THUMB_DIR/${SLUG}-thumbnail.png"; do
  src="${pair%%|*}"; dst="${pair##*|}"
  a=$(stat -f%z "$src"); b=$(stat -f%z "$dst")
  if [ "$a" = "$b" ]; then echo "OK   $(basename "$dst")  $b bytes"
  else echo "FAIL $(basename "$dst")  local=$a mounted=$b"; ok=0; fi
done
[ "$ok" = 1 ] || { echo "PUBLISH FAILED — sizes differ on the mounted path."; exit 1; }

echo
echo "Published to the mounted Drive folders (Drive Desktop will sync upward):"
echo "  $VID_DIR/${SLUG}-final.mp4"
echo "  $THUMB_DIR/${SLUG}-thumbnail.png"
echo
echo "Remaining delivery-tail step: flip the Notion Content page Stage -> Packaging/Posting (G9)."
echo "Reveal in Finder:  open -R \"$VID_DIR/${SLUG}-final.mp4\""
