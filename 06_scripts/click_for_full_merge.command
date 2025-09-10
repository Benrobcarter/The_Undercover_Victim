#!/bin/bash

# Always run from the correct project folder
cd ~/Documents/the_undercover_victim || exit 1

TS=$(date +"%Y-%m-%d_%H-%M-%S")
LOG_FILE="08_audit/merge_log_$TS.txt"
ZIP_NAME="08_audit/audit_backup_$TS.zip"
AUDIT_PATH="08_audit/STATUS_REPORT_2025-09-05.json"

echo "🚀 Starting Undercover Victim Full Merge – $TS" | tee -a "$LOG_FILE"

# Step 0: Smart PDF OCR
echo "📄 Step 0: Smart OCR ingest..." | tee -a "$LOG_FILE"
python3 06_scripts/ocr_ingest_smart.py 2>&1 | tee -a "$LOG_FILE"

# Step 0.5: Thread splitting
echo "✂️ Step 0.5: Splitting OCR'd threads into VEX replies..." | tee -a "$LOG_FILE"
python3 06_scripts/split_ocr_text_into_replies.py 2>&1 | tee -a "$LOG_FILE"

# Step 1: Patch shards
echo "📌 Step 1: Patching new VEX and contradictions..." | tee -a "$LOG_FILE"
python3 06_scripts/patch_shards_boxoffice.py 2>&1 | tee -a "$LOG_FILE"

# Step 2: Hash audio
echo "🔐 Step 2: Hashing audio (if any)..." | tee -a "$LOG_FILE"
for file in 01_evidence/vex/*.json; do
  python3 06_scripts/hash_audio.py "$file" 2>&1 | tee -a "$LOG_FILE"
done

# Step 3: Merge shards
echo "🧠 Step 3: Merging shards via atlas.json..." | tee -a "$LOG_FILE"
python3 06_scripts/MERGE_ATLAS.py 07_meta/atlas.json 07_meta/working_state.json 08_audit --dedupe 2>&1 | tee -a "$LOG_FILE"

# Step 4: Audit
echo "📊 Step 4: Running final audit..." | tee -a "$LOG_FILE"
python3 06_scripts/generate_status_report.py 2>&1 | tee -a "$LOG_FILE"

# Step 5: Zip the audit file
if [ -f "$AUDIT_PATH" ]; then
  echo "📦 Step 5: Zipping audit report..." | tee -a "$LOG_FILE"
  zip -j "$ZIP_NAME" "$AUDIT_PATH" 2>&1 | tee -a "$LOG_FILE"
else
  echo "❌ Audit file not found — zip skipped." | tee -a "$LOG_FILE"
fi

# Step 6: Open audit folder
echo "📂 Step 6: Opening audit folder..." | tee -a "$LOG_FILE"
open 08_audit/

# Step 7: Sound
afplay /System/Library/Sounds/Glass.aiff

echo "✅ Merge + Audit complete – $TS" | tee -a "$LOG_FILE"
