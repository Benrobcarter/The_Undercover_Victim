#!/bin/bash

cd "$(dirname "$0")/dashboard/data" || exit 1

echo "🧼 Cleaning dashboard/data/..."

# Define what should be kept
keep_files=(
  "consolidated_master.json"
  "contradictions.json"
  "contradictions_vex.json"
  "evidence_vex.json"
  "manifest_meta.json"
  "timelines.json"
)

# Convert to a lookup pattern
for file in *.json; do
  skip=false
  for keep in "${keep_files[@]}"; do
    if [[ "$file" == "$keep" ]]; then
      skip=true
      break
    fi
  done

  if ! $skip; then
    echo "🗑️ Removing $file"
    rm -f "$file"
  fi
done

echo "✅ Cleanup complete."