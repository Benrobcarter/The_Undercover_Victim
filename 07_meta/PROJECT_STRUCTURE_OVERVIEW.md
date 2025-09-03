# 🗂 UNDERCOVER VICTIM — PROJECT STRUCTURE OVERVIEW

_Last updated: 2025-09-01_

This document outlines the canonical folder and file structure for the `the_undercover_victim` project — including contradictions, VEX-tagged evidence, timeline entries, meta overlays, and book/quote integration.

---

## 🔧 01_evidence/
> All VEX-tagged files: emails, transcripts, audio logs, receipts, PDFs.

- `vex/` → Merged VEX: `shard_evidence_vex_merged_v3.json`
- Audio, screenshots, transcripts sorted by subfolder or incident
- VEX entries linked to source path + timeline + contradiction IDs

---

## 🧱 02_contradictions/
> Merged contradiction data, structured for timeline, quote, and legal use.

- `shard_contradictions_core_merged_v3.json` ✅
- Each contradiction includes: ID, claim vs reality, law breached, tags, linked timeline, linked VEX
- Source bundles (e.g. `CONTRA_2025-03-29_Fringe_Was_Silent`) stored as ZIPs or JSON

---

## 📅 03_timelines/
> Chronological event tracker (sourced from VEX, transcripts, email threads)

- `shard_timelines_core_merged_UPDATED_2025-09-01_v3.json` ✅
- All events VEX-linked, contradiction-linked, tag-labelled
- Entries include metadata like source file, ID, description

---

## 📖 04_book/
> Drafted and crosswalked narrative versions of the user’s story

- `BOOK_MASTER_MERGED_POC_2025-08-27_v5.2.json`
- Links to quote bank, contradictions, timeline hooks
- Used in conjunction with `CROSSWALK_BOOK_SHARD_TIMELINE_2025-08-31.json`

---

## 🌐 05_public/
> Public-facing elements (quote overlays, audio snippets, WordPress-ready fragments)

- `quote_cards.json` → Used for Divi & frontend quote modules
- Assets tied to safe-for-public timeline exposure
- Used for TikTok + WordPress rollout

---

## 🔧 06_scripts/
> Python tools for injection, merging, dashboard generation

- `consolidate_shards.py` ✅ Merges VEX, timeline, contradictions into dashboard-ready format
- Uses `atlas.json` to route shards to the correct folder

---

## 🧠 07_meta/
> Master overlays, tag maps, quote hooks, crosswalks

| File | Purpose |
|------|---------|
| `atlas.json` | Controls logic paths for all shard injections |
| `vex_tag_reference_merged.json` | All tag descriptions and origins |
| `CONTRA_QUOTE_LINKS_PATCH.json` | Maps contradiction IDs to quote IDs |
| `CROSSWALK_BOOK_SHARD_TIMELINE_2025-08-31.json` | Maps book sections to VEX/timeline/contradiction |
| `STATUS_REPORT_06A_to_06H.json` | Audit log of all recent injections |
| `working_state.json` | Active merge/injection state tracking |
| `evidence_suppression_audit_log_Q3_2025.json` | ICO-ready summary of SAR suppression & GDPR breaches |

---

## 🔍 08_audit/
> Final rollup summaries + visual dashboards

- `PROJECT_STATUS_SNAPSHOT.json` (optional)
- Outputs from `consolidate_shards.py`
- Includes SHA, last-modified, folder health status

---

## 📦 ARCHIVE / HISTORICAL PATCHES

Move anything outdated here:
- Previous `v2` versions of shards
- Old unmerged VEX/contradiction drafts
- Temporary folders like `bf_batch_01`, `with_probe_synced`, `safeguarding_draft/`

---

# ✅ CORE SHARDS TO USE GOING FORWARD

- `shard_evidence_vex_merged_v3.json`
- `shard_contradictions_core_merged_v3.json`
- `shard_timelines_core_merged_UPDATED_2025-09-01_v3.json`
- `vex_tag_reference_merged.json`