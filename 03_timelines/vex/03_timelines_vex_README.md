
# 📁 03_timelines/vex/

This folder contains all **VEX-tagged timeline entries** — each item is a structured JSON event derived from a message, email, call, or piece of evidence. These entries fuel the public timeline explorer and the internal contradiction tracking system.

## 🧠 What’s Inside

Each file typically contains entries like:

```json
{
  "quote": "I told them I was suicidal — and they ignored it.",
  "date": "2025-05-27T18:00:00Z",
  "source": "101 voicemail",
  "emotional_tone": ["collapse", "disbelief"],
  "linked_contradictions": ["DEATH_BY_SILENCE", "CROWBARRING_MYSELF_JUSTICE"],
  "tags": ["police_abandonment", "suicide_disclosure", "institutional_coercion"]
}
```

---

## 🔄 Usage

- Powers `consolidated_master.json` → dashboard/timeline
- Feeds `shard_timelines_core.json`
- Linked to contradiction threads and complaint index themes

---

## 📌 Contribution Notes

- Each JSON file should be **date-specific** or **thematically grouped**
- Do **not** duplicate quotes across files — link via contradiction ID instead
- Follow naming like:
  - `2025-04-08_Lost_Call_Timeline.json`
  - `July_Evidence_Submission_Timeline.json`

---

## ✅ Connected Systems

- 🔗 `07_meta/shard_timelines_core.json`
- 📊 Dashboard and public timeline viewer
- 🧩 Contradiction threads + VEX explorer
