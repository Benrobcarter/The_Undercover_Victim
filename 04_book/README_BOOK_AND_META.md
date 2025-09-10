# UNDERCOVER VICTIM PROJECT – BOOK & META FILES

This README documents the key structural files supporting the *Undercover Victim* book, its VEX-tagging system, and timeline/contradiction infrastructure.

---

## 📚 Folder: `04_book/`

Contains all narrative, quote, and structural overlays for the published and in-progress book build.

### Key Files:
- `BOOK_RELEVANT_FILES_INDEX_v5.json`: Master list of all files that directly support the Undercover Victim book structure.
- `QUOTE_TO_CONTRADICTION_CROSSWALK.json`: Maps each quote card ID to its related contradiction(s) for frontend sliders and inline narrative overlays.
- `BOOK_MASTER_MERGED_POC_*.json`: Core book manuscripts, including v5.2 and patched editions.
- `BOOK_UNDERCOVER_VICTIM_v2_structured.json`: Structured chapter version with quote syncing and auto-chaptering logic.

---

## 🧠 Folder: `07_meta/`

Contains merged data, contradiction overlays, and supporting dashboards.

### Key Files:
- `consolidated_master.json`: Merged monolith containing contradictions, contradiction VEX, timeline entries, and evidence VEX.
- `TIMELINE_TO_CONTRADICTION_CROSSWALK.json`: Maps timeline events to contradiction IDs for navigation and dashboard integration.

---

## 📊 Folder: `08_audit/`

Contains reports and cross-validation tools.

### Key Files:
- `STATUS_REPORT_2025-09-01_v3.json`: Summary of item counts from the consolidated master, used to verify structural coverage.
- `BOOK_JSON_BUNDLE_2025-09-01.zip`: Snapshot archive containing all core book-related JSONs at merge point.

---

For terminal instructions or rebuild support, see `PROJECT_STRUCTURE_OVERVIEW.md`.
