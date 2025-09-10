
# 📁 02_contradictions/

This folder stores all contradiction data — split into machine-readable `auto/` shards and human-readable `manual/` exports.

## 📂 Subfolders

### `auto/`
Use this for contradictions automatically generated, merged, or fed into the dashboard. Examples:
- `shard_contradictions_core.json`
- `MASTER_CONTRADICTIONS_INJECTED_*.json`
- `*_v4.json`, `*_v2.json`, etc.

These files are parsed directly into:
- The contradiction explorer
- Timeline crosslinks
- The `consolidated_master.json` build

### `manual/`
Use this for hand-crafted contradictions, patch files, or bundles designed for:
- Legal use
- Narrative development
- Git commits and version history

Examples:
- `DUNCAN_ATTEMPTED_MURDER_CONTRADICTION_PATCH.json`
- `EX_VERITAS_CHAT_CONTRADICTION_2025.json`
- `CONTRADICTION_PACK_HOLIDAY_ALIBI_FULL_BUNDLE.json`

---

## 🛠 Contribution Rules

- **Do not edit `auto/` files manually.** Use the shard builders.
- **Manual files** should follow the naming pattern:
  ```
  CONTRA_<YYYY-MM-DD>_<summary>.json
  ```

## 🔄 Dashboard Pipeline Integration

Contradictions from `auto/` will show up live once:
1. `consolidate_shards.py` is run
2. The dashboard is pointed to the new `consolidated_master.json`

