#!/usr/bin/env bash
# diagram-design: render beautiful, brand-styled diagrams from D2 source.
#
# Usage:
#   render.sh <input.d2|-> <output.(svg|png)> [--brand fractal|founder-freedom|plain] [extra d2 flags]
#
# Examples:
#   render.sh flow.d2 flow.svg                       # Fractal brand (default), SVG — best for embedding
#   render.sh flow.d2 flow.png --brand founder-freedom   # hand-drawn sketch, PNG
#   render.sh flow.d2 flow.svg --brand plain         # no brand styling, D2 default theme
#   cat flow.d2 | render.sh - out.png --brand fractal
#
# HOW IT WORKS:
#   Prepends the chosen brand header (themes/<brand>.d2 — a D2 `vars: { d2-config: {...} }`
#   block that sets theme-id, sketch, pad, and brand color overrides) to the diagram, then
#   runs `d2`. SVG is preferred (pure Go, scales, embeds into social-canvas/content-visuals);
#   PNG is for standalone use (D2 rasterises via its own bundled browser).
#
#   Optional brand font: if assets/fonts/Geist-Regular.ttf exists, the fractal brand uses it
#   (matches social-canvas). Drop Geist TTFs there to enable; otherwise D2's default font is used.
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
THEMES="$SKILL_DIR/themes"
FONTS="$SKILL_DIR/assets/fonts"

usage() {
  echo "usage: render.sh <input.d2|-> <output.(svg|png)> [--brand fractal|founder-freedom|plain] [extra d2 flags]" >&2
  exit 2
}

[ "$#" -ge 2 ] || usage
IN="$1"; OUT="$2"; shift 2

BRAND="fractal"        # default brand
PASS=()                # extra flags passed through to d2
while [ "$#" -gt 0 ]; do
  case "$1" in
    --brand)   BRAND="${2:-}"; shift 2;;
    --brand=*) BRAND="${1#*=}"; shift;;
    *)         PASS+=("$1"); shift;;
  esac
done

command -v d2 >/dev/null 2>&1 || { echo "render.sh: d2 not installed. Run: brew install d2" >&2; exit 1; }

# Build combined source in a temp dir: brand header (if any) + the diagram.
WORK="$(mktemp -d -t diagram-design)"
trap 'rm -rf "$WORK"' EXIT
SRC="$WORK/diagram.d2"
: > "$SRC"
HEADER="$THEMES/$BRAND.d2"
if [ "$BRAND" != "plain" ] && [ -f "$HEADER" ]; then cat "$HEADER" >> "$SRC"; printf '\n' >> "$SRC"; fi
if [ "$IN" = "-" ]; then cat >> "$SRC"; else cat "$IN" >> "$SRC"; fi

# Assemble the d2 command (bash 3.2-safe: guard empty arrays before expanding).
cmd=(d2)
# Brand font: Fractal renders in Geist (matches social-canvas). Each flag is guarded by
# file presence so the skill still works if a face is missing. Geist v1.7+ ships a true
# italic, so edge labels (rendered italic by D2) stay in-brand. Mono = Geist Mono.
if [ "$BRAND" = "fractal" ] && [ -f "$FONTS/Geist-Regular.ttf" ]; then
  cmd+=(--font-regular "$FONTS/Geist-Regular.ttf")
  [ -f "$FONTS/Geist-Bold.ttf" ]        && cmd+=(--font-bold        "$FONTS/Geist-Bold.ttf")
  [ -f "$FONTS/Geist-Italic.ttf" ]      && cmd+=(--font-italic      "$FONTS/Geist-Italic.ttf")
  [ -f "$FONTS/Geist-SemiBold.ttf" ]    && cmd+=(--font-semibold    "$FONTS/Geist-SemiBold.ttf")
  [ -f "$FONTS/GeistMono-Regular.ttf" ] && cmd+=(--font-mono        "$FONTS/GeistMono-Regular.ttf")
  [ -f "$FONTS/GeistMono-Bold.ttf" ]    && cmd+=(--font-mono-bold   "$FONTS/GeistMono-Bold.ttf")
fi
[ "${#PASS[@]}" -gt 0 ] && cmd+=("${PASS[@]}")
cmd+=("$SRC" "$OUT")

exec "${cmd[@]}"
