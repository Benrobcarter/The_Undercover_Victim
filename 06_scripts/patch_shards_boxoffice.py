from pathlib import Path
import json

# --- paths ---
ROOT = Path.home() / "Documents" / "The_Undercover_Victim"
EVID = ROOT / "01_evidence/vex/shard_evidence_vex_merged_v3.json"
CONT = ROOT / "02_contradictions/shard_contradictions_core_merged_v3.json"
TIME = ROOT / "03_timelines/shard_timelines_core_merged_UPDATED_2025-09-01_v3.json"
CLIX = ROOT / "07_meta/contradiction_cluster_index_2025-09-01.json"

# --- helpers ---
def load_json(p: Path):
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        # fallback: keep file safe if broken
        bak = p.with_suffix(p.suffix + ".bak")
        bak.write_bytes(p.read_bytes())
        return {}

def save_json(p: Path, obj):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2, ensure_ascii=False), encoding="utf-8")

def ensure_list(d: dict, key: str):
    if key not in d or not isinstance(d[key], list):
        d[key] = []
    return d[key]

def has_evidence(items, evidence_id):
    for it in items:
        meta = it.get("meta") or {}
        if meta.get("evidence_id") == evidence_id:
            return True
    return False

def has_by_id(items, _id):
    return any((isinstance(x, dict) and x.get("id") == _id) for x in items)

# --- payloads ---

# Evidence items -> stored as {"meta": {...}}
E_ITEMS = [
  {
    "meta": {
      "evidence_id": "EMAIL_2025-04-22_BoxOffice_Requesting_Private_Booker_Details",
      "source_type": "email",
      "date_local": "2025-04-22",
      "title": "Email: Box Office Requests Private Booker Details",
      "timeline_link": "t2_brighton_fringe_consequences#2025-04-22",
      "related_contradictions": ["BF_CONTRA_VENUE_BOXOFFICE_DATA_BREACH"],
      "tags": [
        "BOX_OFFICE_REALLOCATION_FAILURE",
        "VENUE_CUSTOMER_DATA_REQUESTED",
        "GDPR_RISK_UNAUTHORISED_CONTACT",
        "OPERATIONAL_BOUNDARY_CROSSING",
        "VENUE_AUTONOMY_IGNORED"
      ]
    }
  },
  {
    "meta": {
      "evidence_id": "EMAIL_2025-05-04_Crime_Reference_And_Safeguarding_Ignored",
      "source_type": "email",
      "date_local": "2025-05-04",
      "title": "Email: Crime Reference Ignored and Safeguarding Disclosure Dismissed",
      "timeline_link": "t2_brighton_fringe_consequences#2025-05-04",
      "related_contradictions": [
        "BF_CONTRA_VENUE_CRIME_REF_SILENCE_BREACH",
        "BF_CONTRA_VENUE_VOICEMAIL_DEFLECTION_BREACH",
        "BF_CONTRA_VENUE_BOXOFFICE_MISREPRESENTATION_BREACH"
      ],
      "tags": [
        "SAFEGUARDING_ESCALATION",
        "CONFIDENTIALITY_BREACH",
        "NARRATIVE_REPLACEMENT",
        "INSTITUTIONAL_GASLIGHTING",
        "OPERATIONAL_BREAKDOWN",
        "BOX_OFFICE_REALLOCATION_FAILURE",
        "REPUTATIONAL_HARM"
      ]
    }
  }
]

# Contradiction entries -> stored as objects with "id"
C_ITEMS = [
  {
    "id": "BF_CONTRA_VENUE_BOXOFFICE_DATA_BREACH",
    "title": "Breach — Box Office Data & Venue Autonomy",
    "claim": "Brighton Fringe must not contact venue customers or override venue systems without consent.",
    "reality": "Box Office requested direct customer contact details from Half a Camel and proposed contacting audience members.",
    "linked_evidence": ["EMAIL_2025-04-22_BoxOffice_Requesting_Private_Booker_Details"],
    "linked_timeline_ids": ["t2_brighton_fringe_consequences#2025-04-22"],
    "vex_tags": [
      "VENUE_CUSTOMER_DATA_REQUESTED",
      "GDPR_RISK_UNAUTHORISED_CONTACT",
      "OPERATIONAL_BOUNDARY_CROSSING",
      "VENUE_AUTONOMY_IGNORED"
    ],
    "cluster": "BF-CONTRA-VENUE-MANAGER-CONTRACT-BREACHES-2025",
    "status": "active"
  },
  {
    "id": "BF_CONTRA_VENUE_CRIME_REF_SILENCE_BREACH",
    "title": "Breach — Crime Ref Ignored & Safeguarding Dismissed",
    "claim": "Prompt, appropriate handling of safeguarding disclosures is required.",
    "reality": "New crime ref and safeguarding were denied/deflected by the Chair; voicemail denied.",
    "linked_evidence": ["EMAIL_2025-05-04_Crime_Reference_And_Safeguarding_Ignored"],
    "linked_timeline_ids": ["t2_brighton_fringe_consequences#2025-05-04"],
    "vex_tags": [
      "COMMUNICATION_TIMELINESS_BREACH",
      "SAFEGUARDING_ESCALATION",
      "CONFIDENTIALITY_BREACH",
      "NARRATIVE_REPLACEMENT",
      "INSTITUTIONAL_GASLIGHTING"
    ],
    "cluster": "BF-CONTRA-VENUE-MANAGER-CONTRACT-BREACHES-2025",
    "status": "active"
  },
  {
    "id": "BF_CONTRA_VENUE_VOICEMAIL_DEFLECTION_BREACH",
    "title": "Breach — Voicemail Dismissal & Responsibility Denial",
    "claim": "Venue managers' issues must be supported with clear logging and dialogue.",
    "reality": "Safeguarding voicemail was denied and support deflected to a hub despite risk.",
    "linked_evidence": ["EMAIL_2025-05-04_Crime_Reference_And_Safeguarding_Ignored"],
    "linked_timeline_ids": ["t2_brighton_fringe_consequences#2025-05-04"],
    "vex_tags": [
      "SAFEGUARDING_DEFLECTION",
      "INSTITUTIONAL_GASLIGHTING",
      "CONSTRUCTIVE_EXPULSION",
      "REPUTATIONAL_HARM"
    ],
    "cluster": "BF-CONTRA-VENUE-MANAGER-CONTRACT-BREACHES-2025",
    "status": "active"
  },
  {
    "id": "BF_CONTRA_VENUE_BOXOFFICE_MISREPRESENTATION_BREACH",
    "title": "Breach — Box Office Misrepresentation & Venue Collapse",
    "claim": "Venues opting out must be coordinated correctly without public misdirection.",
    "reality": "All six venues opted out; public comms still promoted box office, causing confusion/damage.",
    "linked_evidence": ["EMAIL_2025-05-04_Crime_Reference_And_Safeguarding_Ignored"],
    "linked_timeline_ids": ["t2_brighton_fringe_consequences#2025-05-04"],
    "vex_tags": [
      "BOX_OFFICE_REALLOCATION_FAILURE",
      "OPERATIONAL_BREAKDOWN",
      "UNINSURABLE_EVENT",
      "REPUTATIONAL_HARM",
      "CONTRACTUAL_CONFIRMATION_BREACH"
    ],
    "cluster": "BF-CONTRA-VENUE-MANAGER-CONTRACT-BREACHES-2025",
    "status": "active"
  },
  {
    "id": "BF_CONTRA_VENUE_COMMUNICATION_NARRATIVE_DISCLOSURE_BREACH",
    "title": "Breach — Communication Timeliness & Narrative Disclosure",
    "claim": "Timely responses and proper safeguarding handling are required.",
    "reality": "Internal narratives about mental health/business capacity shared; consent/accuracy issues; no timely response.",
    "linked_evidence": ["EMAIL_2025-05-11_SAFEGUARDING_BREACH_NARRATIVE_DISCLOSURE"],
    "linked_timeline_ids": ["t2_brighton_fringe_consequences#2025-05-11"],
    "vex_tags": [
      "COMMUNICATION_TIMELINESS_BREACH",
      "NARRATIVE_REPLACEMENT",
      "INSTITUTIONAL_GASLIGHTING",
      "CONFIDENTIALITY_BREACH",
      "SAFEGUARDING_ESCALATION"
    ],
    "cluster": "BF-CONTRA-VENUE-MANAGER-CONTRACT-BREACHES-2025",
    "status": "active"
  }
]

# Timeline event -> stored as objects with "id"
T_ITEMS = [
  {
    "id": "t2_brighton_fringe_consequences#2025-04-22",
    "date": "2025-04-22",
    "title": "Box Office Requests Private Booker Data from Half a Camel",
    "summary": "Brighton Fringe Box Office asked for direct audience contact details from venue system, creating GDPR risk and contradicting manager agreement.",
    "linked_contradictions": ["BF_CONTRA_VENUE_BOXOFFICE_DATA_BREACH"],
    "vex_tags": [
      "BOX_OFFICE_REALLOCATION_FAILURE",
      "VENUE_CUSTOMER_DATA_REQUESTED",
      "GDPR_RISK_UNAUTHORISED_CONTACT"
    ]
  }
]

# Cluster index record
CL_ITEM = {
  "id": "BF-CONTRA-VENUE-MANAGER-CONTRACT-BREACHES-2025",
  "sub_contradictions": [
    "BF_CONTRA_VENUE_BOXOFFICE_DATA_BREACH",
    "BF_CONTRA_VENUE_CRIME_REF_SILENCE_BREACH",
    "BF_CONTRA_VENUE_VOICEMAIL_DEFLECTION_BREACH",
    "BF_CONTRA_VENUE_BOXOFFICE_MISREPRESENTATION_BREACH",
    "BF_CONTRA_VENUE_COMMUNICATION_NARRATIVE_DISCLOSURE_BREACH"
  ],
  "meta_overlays": [
    "07_meta/VENUE_MANAGER_CONTRACT_BREACH_CROSSWALK.json",
    "07_meta/VENUE_MANAGER_CONTRACT_CLAUSE_ANCHORS_2025.json"
  ]
}

# --- patch: evidence ---
e = load_json(EVID)
e_items = ensure_list(e, "items")
for it in E_ITEMS:
    ev_id = it["meta"]["evidence_id"]
    if not has_evidence(e_items, ev_id):
        e_items.append({"meta": it["meta"]})
save_json(EVID, e)

# --- patch: contradictions ---
c = load_json(CONT)
c_items = ensure_list(c, "contradictions")
for it in C_ITEMS:
    if not has_by_id(c_items, it["id"]):
        c_items.append(it)
save_json(CONT, c)

# --- patch: timeline ---
t = load_json(TIME)
t_items = ensure_list(t, "events")
for it in T_ITEMS:
    if not has_by_id(t_items, it["id"]):
        t_items.append(it)
save_json(TIME, t)

# --- patch: cluster index ---
cl = load_json(CLIX)
# allow either {"clusters":[...]} or {"clusters":{...}} or empty
if isinstance(cl.get("clusters"), dict):
    cl["clusters"][CL_ITEM["id"]] = CL_ITEM
else:
    cl_items = ensure_list(cl, "clusters")
    for i, existing in enumerate(cl_items):
        if isinstance(existing, dict) and existing.get("id") == CL_ITEM["id"]:
            cl_items[i] = CL_ITEM
            break
    else:
        cl_items.append(CL_ITEM)
save_json(CLIX, cl)

print("✅ Shards patched into:")
print("  •", EVID)
print("  •", CONT)
print("  •", TIME)
print("  •", CLIX)
