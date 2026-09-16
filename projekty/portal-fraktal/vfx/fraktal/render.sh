#!/usr/bin/env bash
# Render sceny fraktalnej "portal" w Mandelbulberze 2.
# Uzycie:
#   ./render.sh podglad          - szybki podglad 960x540
#   ./render.sh final            - render 1920x1080 do EXR
#   ./render.sh sweep <KLUCZ> <v1> <v2> ...  - seria wariantow jednego parametru
#   ./render.sh anim <od> <do>   - sekwencja klatek z animacji keyframe
set -euo pipefail
cd "$(dirname "$0")"
SCENA="portal_v01.fract"
WYJ="render"
MB="${MB:-mandelbulber2}"
# na maszynie bez X-serwera:
export QT_QPA_PLATFORM="${QT_QPA_PLATFORM:-offscreen}"
# dodaj -g zeby liczyc na GPU (OpenCL), -G dla wszystkich GPU
GPU="${GPU:-}"

mkdir -p "$WYJ"

case "${1:-podglad}" in
  podglad)
    $MB -n -C $GPU -r 960x540 -f png -o "$WYJ/podglad.png" "$SCENA"
    ;;
  final)
    $MB -n -C $GPU -r 1920x1080 -f exr -o "$WYJ/final.exr" "$SCENA"
    ;;
  sweep)
    KLUCZ="$2"; shift 2
    i=0
    for v in "$@"; do
      i=$((i+1))
      echo ">>> $KLUCZ=$v"
      $MB -n -C $GPU -r 640x360 -f png -o "$WYJ/sweep_${KLUCZ}_${i}.png" \
          -O "${KLUCZ}=${v}" "$SCENA"
    done
    echo "Warianty w $WYJ/sweep_${KLUCZ}_*.png"
    ;;
  anim)
    OD="${2:-0}"; DO="${3:-96}"
    $MB -n -C $GPU -K -s "$OD" -e "$DO" -r 1920x1080 -f exr -o "$WYJ/seq/" "$SCENA"
    ;;
  *)
    echo "Nieznany tryb: $1"; exit 1
    ;;
esac
