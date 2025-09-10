
import os, sys, json, hashlib, subprocess, datetime, shlex
from pathlib import Path

ROOT = Path.home()/ "Documents" / "the_undercover_victim"
PDF_IN   = ROOT / "01_evidence" / "pdf_unprocessed"
PDF_OCRD = ROOT / "01_evidence" / "pdf_ocrd"
TEXT_OUT = ROOT / "01_evidence" / "text"
VEX_OUT  = ROOT / "01_evidence" / "vex"
AUD_DIR  = ROOT / "01_evidence" / "audio"
AUDIT    = ROOT / "08_audit"

for p in (PDF_IN, PDF_OCRD, TEXT_OUT, VEX_OUT, AUD_DIR, AUDIT):
    p.mkdir(parents=True, exist_ok=True)

def sha256(path: Path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1<<20), b""): h.update(chunk)
    return h.hexdigest()

def run(cmd):
    subprocess.run(cmd, check=True)

def ocr_pdf(src: Path, dst: Path):
    run(["ocrmypdf", "--force-ocr", "--optimize", "3", "--jobs", "2", str(src), str(dst)])

def pdftotext(src: Path, txt: Path):
    run(["pdftotext", "-layout", str(src), str(txt)])

def vex_stub(pdf_path: Path, text_path: Path, sha: str):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    base = pdf_path.stem
    out = {
        "id": f"VEX_{base}_{sha[:8]}",
        "source_file": str(pdf_path.name),
        "sha256": sha,
        "ingested_at": now,
        "tags": ["ocr","auto-ingest","undated_flag_if_needed"],
        "timeline": [],
        "contradictions": [],
        "notes": f"Auto-generated stub for {pdf_path.name}. Confirm date before finalizing filename."
    }
    out_path = VEX_OUT / f"{base}.json"
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    return out_path

def process_pdf(path: Path):
    ocr_dst = PDF_OCRD / path.name
    txt_dst = TEXT_OUT / (path.stem + ".txt")

    # 1) OCR
    ocr_pdf(path, ocr_dst)
    # 2) Text extract
    pdftotext(ocr_dst, txt_dst)
    # 3) Hashes
    sha = sha256(ocr_dst)
    # 4) VEX stub
    vex_path = vex_stub(ocr_dst, txt_dst, sha)
    return {
        "pdf_in": str(path),
        "pdf_ocrd": str(ocr_dst),
        "text": str(txt_dst),
        "vex": str(vex_path),
        "sha256": sha
    }

def hash_audio(path: Path):
    return {"audio": str(path), "sha256": sha256(path)}

def main(args):
    report = {"processed_pdfs": [], "hashed_audio": [], "errors": []}
    # If files are dropped onto the app, process only those; else batch everything in pdf_unprocessed.
    targets = [Path(a) for a in args] if args else sorted(PDF_IN.glob("*.pdf"))

    for p in targets:
        try:
            if p.suffix.lower()==".pdf":
                report["processed_pdfs"].append(process_pdf(p))
            elif p.suffix.lower() in (".mp3",".wav",".m4a",".flac"):
                report["hashed_audio"].append(hash_audio(p))
        except Exception as e:
            report["errors"].append({"file": str(p), "error": str(e)})

    # Write status report
    stamp = datetime.datetime.now().strftime("%Y-%m-%d")
    (AUDIT / f"STATUS_REPORT_{stamp}.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    main(sys.argv[1:])
