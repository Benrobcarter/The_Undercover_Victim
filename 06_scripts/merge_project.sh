#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python3 consolidate_shards.py \
  07_meta/atlas_FINAL_2025-09-01.json \
  07_meta/working_state.json \
  08_audit/
echo "[OK] Merge complete → 08_audit/"
