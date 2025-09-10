# UNDERCOVER VICTIM PROJECT – CONTRADICTIONS MODULE

This folder (`02_contradictions/`) contains the full contradiction architecture for the *Undercover Victim* project. These files document institutional breaches, narrative reversals, and suppression patterns as JSON-structured contradictions.

---

## 🔁 Folder Purpose

To store:
- Direct contradiction entries (named or by ID)
- Contradiction overlays for book integration
- Cluster bundles connecting related contradictions
- Inject-ready JSON for dashboard and Divi display

---

## 📂 Key File Types

### `shard_contradictions_core.json`
- Base contradiction entries with `id`, `title`, `description`, `linked_evidence`, `timeline_refs`, and `legal_violations`.

### `shard_contradictions_vex.json`
- Contradiction overlays for emotional metadata and Victim Experience (VEX) tagging.

### `*_BUNDLE.json`
- Clustered contradictions organized by legal thread (e.g. safeguarding, suicide attempt, SAR suppression).
- Examples:
  - `CONTRADICTION_PACK_HOLIDAY_ALIBI_FULL_BUNDLE.json`
  - `UPDATED_CONTRA_CLUSTER_2025-08-30_PALMER_SUPERVISORY_FAILURE_BUNDLE_v3.json`

### `CONTRA_*.json`
- Individually declared contradictions for scene-specific breaches.
- Example:
  - `CONTRA_2025-06-22_101_Humiliation_Protocol.json` → From Section 3.17

---

## 📌 Integration Pathways

- Every contradiction can be linked to:
  - One or more timeline entries
  - Book chapters (via `CROSSWALK_BOOK_SHARD_TIMELINE.json`)
  - Quote cards (via `CONTRA_QUOTE_LINKS_PATCH.json`)

Contradictions are injected during consolidation (see `consolidate_shards.py`) and used for:
- Dashboard summaries
- Legal mapping
- Chapter overlays
- IOPC and ICO evidence export

---

For syncing new contradictions, add them to the appropriate shard and rerun the consolidation process.
