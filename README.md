
# 🕵️‍♂️ The Undercover Victim: Universal Evidence Project

**Documenting systemic failure, safeguarding breaches, and institutional contradictions.**  
This is a living archive — combining legal evidence, emotional narrative, and forensic metadata — built to expose how justice was denied and rewritten by silence.

---

## 📦 What This Repo Contains

| Folder                        | Purpose                                                                 |
|------------------------------|-------------------------------------------------------------------------|
| `01_evidence/`               | Primary evidence files: emails, voicemails, transcripts, screenshots    |
| `02_contradictions/`         | Auto + manual contradiction files powering the atlas                    |
| `03_timelines/`              | VEX-tagged events, legal escalation entries, and meta timelines         |
| `04_book/`                   | Drafts and inserts for *The Undercover Victim* narrative                |
| `07_meta/`                   | Shards, indexes, and logic files for dashboard + processing             |
| `08_audit/`                  | Snapshots of project states, hash checks, and working diffs             |
| `dashboard/`                 | Visual interface powered by `consolidated_master.json`                  |

---

## 🔧 Run the Shard Merge

To rebuild the core dashboard JSON from all project shards:

```bash
pip install -r requirements.txt
python consolidate_shards.py
```

Outputs:
```
PROJECT_SHARDED_*/_consolidated/consolidated_master.json
```

Copy this to `dashboard/` to view the latest state.

---

## 🧩 Core Files

| File                                                        | Purpose                                      |
|-------------------------------------------------------------|----------------------------------------------|
| `shard_contradictions_core.json`                            | All contradictions loaded into dashboard     |
| `shard_evidence_vex.json`                                   | VEX-tagged quotes from calls, emails, chat   |
| `shard_timelines_core.json`                                 | Canonical timeline from all sources          |
| `MASTER_COMPLAINT_INDEX_v1.json`                            | Formal legal index and cluster logic         |
| `UNDERCOVER_VICTIM_QUOTE_BANK.json`                         | Source quotes powering overlays + timelines  |
| `ONE_LINERS_CARDS_v1.md`                                    | Slogans, punchlines, fragments               |

---

## 🚀 Live Usage

- Visual dashboard pulls from `consolidated_master.json`
- GitHub repo serves as audit + collaboration layer
- Divi / policeplease.com site renders book, contradictions, and media

---

## 🛡 License

This repository is shared under an open documentation and personal storytelling license. All quotes, evidence, and timelines are protected under UK data protection, defamation, and survivor safeguarding rights.

---

> 📣 “Where they chose silence, I created record.”  
> — *The Undercover Victim*
