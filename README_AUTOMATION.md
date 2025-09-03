# AUTO_EMAIL_INGEST_V2 — Email + PDF OCR Ingest

📥 Drop `.eml`, `.txt`, or `.pdf` files into `inbox/`.

⚙️ Run the ingest:

```bash
python3 bin/ingest_inbox_emails.py
```

This will:
- Parse emails
- OCR text from PDFs (via PyMuPDF)
- Auto-tag and generate VEX JSONs
- Append to main shards
- Update manifest/meta
- Move original PDFs to `01_evidence/pdf/`
- Log audit trail
- Print filename + actions

💡 Compatible with:
- `shard_evidence_vex_merged_v3.json`
- `shard_contradictions_core_merged_v3.json`
- `shard_timelines_core_merged_UPDATED_2025-09-01_v3.json`
- `atlas.json`, `vex_tag_reference_merged.json`
