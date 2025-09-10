
# 📁 04_book/inserts/

This subfolder contains modular inserts — supporting content that plugs directly into the main book manuscript, Divi modules, or multimedia timelines.

---

## 🧩 Purpose

These inserts are:
- Smaller than full chapters
- Rich in media, contradiction overlays, or scene detail
- Designed for precision placement within a larger narrative

---

## 🗂 Common Insert Types

| Insert Type        | Example Filename                         | Purpose                                                  |
|--------------------|-------------------------------------------|----------------------------------------------------------|
| 📜 Scene fragments | `insert_3.21_courtroom_emotional.md`      | Drop-in prose for a specific section                     |
| 🧠 Contradiction overlays | `insert_contra_reflections_4a.json`      | JSON modules to inject into both book + dashboard        |
| 🎧 Audio-linked content | `insert_voicemail_overlay_april11.json`    | Embedded quote + audio wave players                      |
| 🖼 Divi-ready sections | `insert_divi_glitch_blocks_05.md`          | Divi-compatible HTML/markdown fragments                  |
| 📆 Timeline triggers | `insert_timeline_crowbarring.json`         | Narrative overlays linked to VEX events or JSON timelines |

---

## ✅ Naming Convention

Use this structure:
```
insert_<chapter/section/tag>_<brief-summary>.<md/json>
```

Examples:
- `insert_3.25_police_final_call.json`
- `insert_glitch_closing_quote_block.md`

---

## 🔗 Connected Systems

- Injected into `SECTION_3_WORKING_DRAFT_v1.1.md` and other drafts
- Parsed by the dashboard/timeline visualizer
- Cross-linked to `VEX`, `contradictions`, and `Divi` exports

