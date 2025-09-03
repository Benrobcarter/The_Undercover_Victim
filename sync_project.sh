#!/bin/bash

set -e

echo "🔍 Navigating to 07_meta..."
cd "$(dirname "$0")/07_meta"

# Get the newest zip file
ZIP=$(ls -t *.zip | head -n 1)

if [ -z "$ZIP" ]; then
  echo "❌ No ZIP file found in 07_meta/"
  exit 1
fi

echo "📦 Unzipping: $ZIP"
unzip -o "$ZIP"

# Rename shard files
echo "✏️ Renaming shard files..."
mv -f shard_contradictions_core_UPDATED_*.json shard_contradictions_core.json
mv -f shard_evidence_vex_UPDATED_*.json shard_evidence_vex.json

# Return to root
cd ..

echo "🧠 Running consolidate_shards.py..."
python3 consolidate_shards.py

# Copy to dashboard
echo "📁 Copying output to dashboard..."
cp consolidated_master.json dashboard/data/consolidated_master.json

echo "✅ Sync complete. You can now run your dashboard:"
echo "   cd dashboard && python3 -m http.server"

