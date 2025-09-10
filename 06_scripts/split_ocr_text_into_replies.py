#!/usr/bin/env python3

import os
import re
import json
from pathlib import Path
from datetime import datetime

# Root setup
ROOT = Path(__file__).resolve().parent.parent
TEXT_IN = ROOT / "01_evidence/text"
VEX_OUT = ROOT / "01_evidence/vex"
SHARD_PATH = ROOT / "01_evidence/vex/shard_evidence_vex_merged_v3.json"

VEX_OUT.mkdir(parents=True, exist_ok=True)

def detect_reply_blocks(text):
    # Break up text based on common patterns in email/chat logs
    pattern = r"(?:From:|\d{1,2}/\d{1,2}/\d{2,4}, \d{1,2}:\d{2} - .+?:)"
    blocks = re.split(pattern, text)
    headers = re.findall(pattern, text)
    results = []

    for i, block in enumerate(blocks[1:]):
        header = headers[i].strip()
        content = block.strip()
        if len(content) > 10:
            results.append((header, content))
    return results

def generate_vex(reply_index, header, content, thread_id, source_file, base_name):
    reply_id = f"{thread_id}_reply_{str(reply_index).zfill(3)}"
    summary = content[:160].replace("\n", " ").strip()
    timestamp_guess = "DATE_NOT_FOUND"

    # Try to extract date from header or content
    date_match = re.search(r"(\d{4}-\d{2}-\d{2})", header)
    if not date_match:
        date_match = re.search(r"(\d{1,2}/\d{1,2}/\d{2,4})", header)
    if date_match:
        timestamp_guess = date_match.group(1)

    vex = {
        "id": reply_id,
        "type": "evidence",
        "source": "Thread Reply Split (Smart OCR)",
        "date": timestamp_guess,
        "summary": f"[{header}] {summary}",
        "meta": {
            "thread_id": thread_id,
            "original_filename": source_file.name,
            "reply_index": reply_index,
            "split_on": "regex: header blocks",
            "ingested_on": datetime.now().isoformat()
        },
        "links": {
            "source_text_file": str(source_file)
        },
        "tags": ["reply_split", "auto_ocr_thread"]
    }
    return vex

def main():
    for txt_file in TEXT_IN.glob("*.txt"):
        print(f"🔍 Splitting replies in: {txt_file.name}")
        base_name = txt_file.stem
        thread_id = f"thread_{base_name}"
        with open(txt_file, "r", encoding="utf-8") as f:
            raw = f.read()

        replies = detect_reply_blocks(raw)
        all_vex = []

        for i, (header, content) in enumerate(replies, start=1):
            vex = generate_vex(i, header, content, thread_id, txt_file, base_name)
            vex_file = VEX_OUT / f"{vex['id']}.json"
            with open(vex_file, "w", encoding="utf-8") as f:
                json.dump(vex, f, indent=2)
            print(f"🧾 VEX saved: {vex_file.name}")
            all_vex.append(vex)

        # Inject all into shard
        if SHARD_PATH.exists():
            with open(SHARD_PATH, "r", encoding="utf-8") as f:
                shard = json.load(f)
        else:
            shard = {"items": []}

        shard["items"].extend(all_vex)
        with open(SHARD_PATH, "w", encoding="utf-8") as f:
            json.dump(shard, f, indent=2)

        print(f"📎 {len(all_vex)} replies injected into shard.")

if __name__ == "__main__":
    main()
