<<<<<<< HEAD
# Universal Evidence Project

A structured archive and analysis framework documenting safeguarding failures, evidence suppression, and institutional contradictions.  
This repository combines **forensic JSON shards**, **book manuscript sections**, and **supporting scripts** to consolidate and present evidence for oversight, complaint, and public transparency.

---

## 📂 Repository Structure

```text
├── 01_evidence/                # VEX-tagged evidence entries (emails, logs, transcripts)
├── 02_contradictions/          # JSON contradiction records + bundles
├── 03_timelines/               # Timeline JSONs (Sussex Police, Brighton Fringe, personal)
├── 04_book/                    # Merged manuscript + section skeletons
├── 07_meta/                    # Core shards and manifest files
│   ├── shard_contradictions_core.json
│   ├── shard_evidence_vex.json
│   ├── shard_timelines_core.json
│   ├── shard_manifest_meta.json
│   └── working_state.json
├── 08_audit/                   # Project snapshots + integrity hashes
├── consolidate_shards.py       # Python tool to merge shards into a master
├── requirements.txt            # Python dependencies
├── LICENSE
└── README.md
⚙️ Core Components
Shards
shard_contradictions_core.json — base contradiction records (e.g., lost evidence, holiday alibi, suicide log delays)

shard_evidence_vex.json — VEX-tagged evidence with contradictions + legal mapping

shard_timelines_core.json — canonical event chronology

shard_manifest_meta.json — metadata & source tracking

Book + Sections
SECTION_3_SKELETON_v1.1.json — outline of Part 3: From Victim to Investigator

BOOK_MASTER_MERGED_POC_2025-08-27_v5.2.json — merged manuscript with contradictions, allegations, and quotes

Bundles
VEX_CROWBARRING_MYSELF_JUSTICE_BUNDLE_v1.1.json — consolidated April 11th 101 calls

CONTRADICTION_PACK_HOLIDAY_ALIBI_FULL_BUNDLE.json — full contradiction pack for “Holiday Alibi”

🛠 Usage
Install dependencies
bash
Copy code
pip install -r requirements.txt
Consolidate shards
bash
Copy code
python consolidate_shards.py 07_meta/atlas.json 07_meta/working_state.json 08_audit/_consolidated
pgsql
Copy code

---
=======
# The Undercover Victim

A forensic evidence archive and narrative book on procedural failure, suicide risk, and institutional silence.
>>>>>>> 944f9dd (Initial commit – full scaffold)
