#!/bin/bash

# Paths
BASE_DIR="$HOME/Documents/the_undercover_victim"
PATCH="$BASE_DIR/02_contradictions/sussex_police/CONTRA_PATCH_SUSSEX_POLICE_TIMELINE_MANIPULATION_2025-09-09_v1.json"
TARGET="$BASE_DIR/02_contradictions/sussex_police/CLUSTER_SUSSEX_POLICE_TIMELINE_MANIPULATION.json"
TMP="$TARGET.tmp"

echo "🛠️ Merging Veritas contradiction patch into Sussex Police timeline cluster…"

# Backup original
cp "$TARGET" "$TARGET.bak.$(date +%Y-%m-%d_%H%M%S)"

# Use jq to deep merge "add" block from patch into the cluster
jq --argfile patch "$PATCH" '
  .anchors += $patch.add.anchors //
  [] |
  .evidence_links += $patch.add.evidence_links //
  [] |
  .contradictions += $patch.add.contradictions //
  [] |
  .timeline_events += $patch.add.timeline_events //
  [] |
  .legal += $patch.add.legal // []
' "$TARGET" > "$TMP" && mv "$TMP" "$TARGET"

echo "✅ Patch merged successfully into: $TARGET"
