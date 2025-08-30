# The Undercover Victim – Consolidated Shard Merge (v1.0)

This repository holds the most recent consolidated evidence, contradiction, and timeline files from the `consolidate_shards.py` merge utility.

## 🔧 Merge Summary

- Script: `consolidate_shards.py`
- Run from: `~/Documents/The_Undercover_Victim`
- Output directory: `08_audit/`
- Run date: 2025-08-30

## ✅ Included Shards

| Shard Name                     | Output Key            | Notes                                       |
|-------------------------------|------------------------|---------------------------------------------|
| `shard_contradictions_core`   | `contradictions.json`  | Core contradiction entries                  |
| `shard_contradictions_vex`    | `contradictions_vex.json` | VEX-tagged contradiction fragments      |
| `shard_timelines_core`        | `timelines.json`       | Timeline structure and events               |
| `shard_evidence_vex`          | `evidence_vex.json`    | VEX-tagged evidence references              |
| `shard_manifest_meta`         | `manifest_meta.json`   | File metadata and structure mappings        |
| `contradictions_holiday_alibi`| `contradictions.json`  | ✅ Merged into main contradiction stream     |

## 📦 Output Files (in `08_audit/`)

- `consolidated_master.json` → Full merged bundle
- `contradictions.json` → Merged contradictions
- `contradictions_vex.json` → VEX-only contradiction fragments
- `evidence_vex.json` → Tagged evidence
- `timelines.json` → Timeline stream
- `manifest_meta.json` → Meta overview

## 🧩 Working State

The following `working_state.json` was used:

```json
{
  "version": "1.0",
  "filters": {},
  "notes": "Minimal working state for consolidate_shards.py"
}