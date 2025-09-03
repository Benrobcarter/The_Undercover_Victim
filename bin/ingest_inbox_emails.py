#!/usr/bin/env python3
import os, json, re, datetime
from pathlib import Path
try:
    import fitz  # PyMuPDF
except ImportError:
    print("⚠️ PyMuPDF not installed. Run: pip install PyMuPDF")
    exit(1)

PROJECT = Path.home() / "Documents" / "the_undercover_victim"
INBOX = PROJECT / "inbox"
ATLAS = PROJECT / "07_meta" / "atlas.json"

KEYWORDS = {
    "safeguarding": {
        "tags": ["SAFEGUARDING_DEFLECTION", "RECKLESS_ENDANGERMENT"],
        "contradiction": "DUNCAN_ATTEMPTED_MURDER",
        "timeline_tag": "SAFEGUARDING_ESCALATION",
        "clause": "SAFEGUARDING_DUTY"
    },
    "ticket": {
        "tags": ["UNINSURABLE_EVENT", "IMPOSSIBLE_COMPLIANCE_CONDITION"],
        "contradiction": "BF-CONTRA-BOXOFFICE-BREACH",
        "timeline_tag": "TICKETING_CONFUSION",
        "clause": "BOX_OFFICE_DUTIES"
    },
    "suicide": {
        "tags": ["SUICIDE_DISCLOSURE_IGNORED", "DEATH_BY_SILENCE"],
        "contradiction": "DEATH_BY_SILENCE_THREAD",
        "timeline_tag": "SUICIDE_ESCALATION",
        "clause": "SAFEGUARDING_DUTY"
    },
    "subject access": {
        "tags": ["DPA_GDPR", "SAR_STRUCTURAL_ABSENCE"],
        "contradiction": "BF-CONTRA-SAR-GDPR-BREACH-2025",
        "timeline_tag": "SAR_ESCALATION",
        "clause": "DATA_TRANSPARENCY_DUTY"
    },
    "veritas": {
        "tags": ["SAFEGUARDING_THIRD_PARTY_VALIDATION", "ADVOCACY_CONFIRMATION"],
        "contradiction": "DUNCAN_ASSISTED_ERASURE",
        "timeline_tag": "THIRD_PARTY_VALIDATION",
        "clause": "SAFEGUARDING_DUTY"
    },
    "trustee": {
        "tags": ["GOVERNANCE_ERASURE", "GOVERNANCE_FAILURE"],
        "contradiction": "BF-CONTRA-GOV-FAILURE-2025",
        "timeline_tag": "GOVERNANCE_ESCALATION",
        "clause": "TRUSTEE_DECISION_DUTY"
    },
    "libel": {
        "tags": ["LIBEL_ACTION_DISGUISED_AS_NEUTRAL_UPDATE", "REPUTATIONAL_HARM"],
        "contradiction": "BF-CONTRA-LIBEL-2025",
        "timeline_tag": "REPUTATIONAL_ESCALATION",
        "clause": "DEFAMATION_RISK_MANAGEMENT"
    },
    "observer role": {
        "tags": ["VENUE_OBSERVER_ROLE_MANIPULATION"],
        "contradiction": "BF-CONTRA-OBSERVER-ERASURE",
        "timeline_tag": "OBSERVER_ERASURE_ESCALATION",
        "clause": "STAKEHOLDER_RECOGNITION_CLAUSE"
    }
}

def load_atlas():
    with open(ATLAS, "r", encoding="utf-8") as f:
        return json.load(f)

def find_shard_path(atlas, name):
    for shard in atlas["shards"]:
        if name in shard["name"]:
            return PROJECT / Path(shard["path"])
    return None

def extract_text_from_pdf(path):
    try:
        doc = fitz.open(path)
        return "\n".join([page.get_text() for page in doc])
    except Exception as e:
        print(f"❌ OCR failed for {path.name}: {e}")
        return ""

def extract_text_from_txt(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read().strip()

def split_thread(text):
    return re.split(r"(?=^From:)", text, flags=re.MULTILINE)

def get_tags_and_links(text):
    lower = text.lower()
    result = {
        "tags": [], "contradictions": [], "timeline_tag": None, "clause": None
    }
    for key, val in KEYWORDS.items():
        if key in lower:
            result["tags"].extend(val["tags"])
            result["contradictions"].append(val["contradiction"])
            result["timeline_tag"] = val["timeline_tag"]
            result["clause"] = val["clause"]
            break
    return result

def write_json(p, data):
    with open(p, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def append_to_shard(shard_path, entry):
    if not shard_path.exists(): return
    with open(shard_path, "r+", encoding="utf-8") as f:
        data = json.load(f)
        key = "items" if "items" in data else "entries" if "entries" in data else None
        if not key: return
        data[key].append(entry)
        f.seek(0)
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.truncate()

def process_message(text, base_name, seq, atlas, thread_id):
    info = get_tags_and_links(text)
    today = datetime.date.today().isoformat()
    evid_id = f"EVID_{today}_{base_name}_MSG{seq:02d}"

    vex = {
        "meta": {
            "evidence_id": evid_id,
            "title": f"{base_name} part {seq}",
            "type": "email",
            "date_local": today,
            "source_file": base_name,
            "thread_id": thread_id,
            "thread_seq": seq,
            "vex_tags": info["tags"],
            "clusters": ["BRIGHTON_FRINGE"],
            "links": {
                "contradictions": info["contradictions"],
                "contract_clause_refs": [info["clause"]] if info["clause"] else []
            }
        },
        "excerpt": text[:1000] + ("…" if len(text) > 1000 else "")
    }

    path = PROJECT / "01_evidence/vex" / f"{evid_id}.json"
    write_json(path, vex)
    append_to_shard(find_shard_path(atlas, "shard_evidence_vex"), vex)
    print(f"📧 VEX saved: {path.name}")

    if info["contradictions"]:
        contra = {
            "id": info["contradictions"][0],
            "links": {"evidence_refs": [evid_id]},
            "tags": info["tags"],
            "contract_clause_refs": [{"clause_key": info["clause"]}] if info["clause"] else []
        }
        append_to_shard(find_shard_path(atlas, "shard_contradictions_core"), contra)

    if info["timeline_tag"]:
        timeline_event = {
            "id": f"{evid_id}_EVENT",
            "when": f"{today}T12:00:00",
            "title": f"Ingested: {base_name} (msg {seq})",
            "summary": f"Auto-ingested message with tags: {', '.join(info['tags'])}",
            "evidence": [evid_id],
            "contradictions": info["contradictions"],
            "tags": info["tags"]
        }
        append_to_shard(find_shard_path(atlas, "shard_timelines_core"), timeline_event)

def process_file(fpath, atlas):
    name = fpath.stem
    ext = fpath.suffix.lower()
    print(f"🧾 Ingesting: {fpath.name}")

    if ext == ".pdf":
        text = extract_text_from_pdf(fpath)
        name = name[:50]
        thread_id = f"THREAD_{datetime.date.today()}_{name}"
        process_message(text, name, 1, atlas, thread_id)
        fpath.rename(PROJECT / "01_evidence/pdf" / fpath.name)
    elif ext in [".eml", ".txt"]:
        full_text = extract_text_from_txt(fpath)
        thread_parts = split_thread(full_text)
        thread_id = f"THREAD_{datetime.date.today()}_{name[:40]}"
        for i, part in enumerate(thread_parts, 1):
            if part.strip():
                process_message(part.strip(), name, i, atlas, thread_id)
        fpath.unlink()

def main():
    files = sorted(INBOX.glob("*"))
    if not files:
        print("📭 Inbox empty")
        return
    atlas = load_atlas()
    for f in files:
        process_file(f, atlas)

if __name__ == "__main__":
    main()
