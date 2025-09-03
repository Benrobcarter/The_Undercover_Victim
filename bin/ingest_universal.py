#!/usr/bin/env python3
import os, json, shutil, re, datetime
from pathlib import Path
try:
    import fitz  # PyMuPDF
except ImportError:
    print("❌ PyMuPDF not installed. Run: pip install PyMuPDF")
    exit(1)

# Paths
PROJECT = Path.home() / "Documents" / "the_undercover_victim"
INBOX = PROJECT / "inbox"
ARCHIVE = INBOX / "archive"
ERROR = INBOX / "error"
VEX_ROOT = PROJECT / "01_evidence/vex"
PDF_DIR = PROJECT / "01_evidence/pdf"
ATLAS = PROJECT / "07_meta/atlas.json"

# Known sources and routing
SOURCE_KEYWORDS = {
    "brighton_fringe": ["fringe", "duncan", "alexander", "box office"],
    "sussex_police": ["police", "crime reference", "101 call", "nfa", "dixon"],
    "veritas": ["veritas", "advocacy", "sian berry"],
    "sar_requests": ["subject access", "SAR", "ICO", "data request"],
    "book_material": ["draft", "chapter", "maggots law", "diary", "foreword"]
}

def load_atlas():
    with open(ATLAS, "r", encoding="utf-8") as f:
        return json.load(f)

def find_shard_path(atlas, name):
    for s in atlas["shards"]:
        if name in s["name"]:
            return PROJECT / s["path"]
    return None

def extract_text_from_pdf(path):
    try:
        doc = fitz.open(path)
        return "\n".join([page.get_text() for page in doc])
    except Exception as e:
        print(f"❌ Failed to OCR {path.name}: {e}")
        return ""

def detect_source(text, fname):
    all_text = f"{fname.lower()} {text.lower()}"
    for source, keywords in SOURCE_KEYWORDS.items():
        for kw in keywords:
            if kw.lower() in all_text:
                return source
    return "other"

def write_json(path, obj):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)

def append_to_shard(shard_path, entry, key="items"):
    if not shard_path.exists(): return
    with open(shard_path, "r+", encoding="utf-8") as f:
        data = json.load(f)
        if key in data:
            data[key].append(entry)
            f.seek(0)
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.truncate()

def process_pdf(fpath, atlas):
    print(f"📄 Processing PDF: {fpath.name}")
    text = extract_text_from_pdf(fpath)
    if not text.strip():
        print(f"⚠️ No content extracted from {fpath.name}")
        shutil.move(str(fpath), ERROR / fpath.name)
        return

    source = detect_source(text, fpath.name)
    today = datetime.date.today().isoformat()
    safe_id = re.sub(r'[^a-zA-Z0-9]+', '_', fpath.stem)[:50]
    evid_id = f"EVID_{today}_{safe_id}"

    # VEX
    vex = {
        "meta": {
            "evidence_id": evid_id,
            "title": fpath.name,
            "type": "pdf",
            "date_local": today,
            "source_file": fpath.name,
            "source_entity": source,
            "vex_tags": [],
            "clusters": [],
            "links": {
                "contradictions": [],
                "contract_clause_refs": []
            }
        },
        "excerpt": text[:1000] + ("…" if len(text) > 1000 else "")
    }

    vex_out = VEX_ROOT / source / f"{evid_id}.json"
    write_json(vex_out, vex)
    print(f"✅ VEX saved: {vex_out.name} in {source}/")

    # Append to shard
    append_to_shard(find_shard_path(atlas, "shard_evidence_vex"), vex)

    # Archive
    shutil.copy(str(fpath), PDF_DIR / fpath.name)
    shutil.move(str(fpath), ARCHIVE / fpath.name)

def main():
    os.makedirs(ARCHIVE, exist_ok=True)
    os.makedirs(ERROR, exist_ok=True)

    files = list(INBOX.glob("*"))
    if not files:
        print("📭 Inbox is empty")
        return

    atlas = load_atlas()
    total = 0

    for f in files:
        if f.is_file() and f.suffix.lower() == ".pdf":
            process_pdf(f, atlas)
            total += 1
        # add .txt, .eml, .docx, .mp3, .jpg later
        elif f.name not in ["archive", "error", "unpack"]:
            print(f"⚠️ Unsupported file: {f.name}")
            shutil.move(str(f), ERROR / f.name)

    print(f"📦 Finished processing {total} PDF file(s). Others skipped for now.")

if __name__ == "__main__":
    main()
