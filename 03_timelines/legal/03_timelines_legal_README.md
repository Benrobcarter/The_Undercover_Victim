
# 📁 03_timelines/legal/

This folder contains **legal-relevant timeline entries**, organized to support:
- Chronologies for ICO, IOPC, Charity Commission, CPS, or civil proceedings
- Law-breach tracking (Care Act, Equality Act, GDPR, etc.)
- Public accountability and systemic failure documentation

---

## 📜 Typical Contents

Each file should represent a legal or regulatory moment:

```json
{
  "quote": "The police were informed on 8 April 2024 — and still failed to act.",
  "date": "2024-04-08T15:47:00Z",
  "source": "Email to Sussex Police",
  "linked_laws": ["Care Act 2014", "GDPR Article 15"],
  "linked_contradictions": ["LOST_EVIDENCE_SUSSEX_POLICE"],
  "tags": ["duty_of_care_breach", "sar_suppression", "safeguarding_failure"]
}
```

---

## 🧠 How It Connects

- Feeds **legal timelines** in the public interface
- Supports bundling for each regulator (IOPC, ICO, CPS, etc.)
- Cross-referenced with contradiction clusters and master complaint index

---

## ✅ File Naming

Use formats like:
- `ICO_Suppression_Timeline.json`
- `CPS_Escalation_2025-04-08.json`
- `Charity_Commission_Referral_2025.json`

---

## 🔗 Connected Structures

- `MASTER_COMPLAINT_INDEX_v1.json`
- `shard_timelines_core.json`
- `atlas.json` → links to contradictions/legal impact
