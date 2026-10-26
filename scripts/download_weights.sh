#!/usr/bin/env bash
set -euo pipefail
DEST="${1:-weights}"
mkdir -p "$DEST"
echo "[1/3] DINO weight package: place manifest.json and *.pt here: $DEST"
echo "[2/3] RadImageNet encoder SHA256: 08629f7e7bd3e29b8ee9522ca3f65ce4d010a7ddf74f0ea3c7e3f3d0bbab0734"
echo "[3/3] v52 heads SHA256: 54f657826b3458a7ba3d462e198ba380732f2b136246182312704929874a9a2c"
echo "Done."
