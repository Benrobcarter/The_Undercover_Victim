
import os, hashlib, json, subprocess, datetime
from pathlib import Path

ROOT = Path.home() / "Documents" / "the_undercover_victim"
PDF_IN = ROOT / "01_evidence/pdf_unprocessed"
PDF_OCRD = ROOT / "01_evidence/pdf_ocrd"
TEXT_OUT = ROOT / "01_evidence/text"
VEX_OUT = ROOT / "01_evidence/vex"
AUDIT = ROOT / "08_audit"

for p in [PDF_IN, PDF_OCRD, TEXT_OUT, VEX_OUT, AUDIT]:
    p.mkdir(parents=True, exist_ok=True)

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def ocr_pdf(src, dst):
    print(f"🔄 OCR: {src.name}")
    subprocess.run([
        "ocrmypdf", "--force-ocr", "--output-type", "pdfa", "--optimize", "3",
        str(src), str(dst)
    ], check=True)

def extract_text(pdf, txt):
    print(f"📝 Extract text: {pdf.name}")
    subprocess.run(["pdftotext", "-layout", str(pdf), str(txt)], check=True)

def create_vex(pdf, txt, hash):
    print(f"💾 Create VEX: {pdf.name}")
    vex = {
        "id": f"VEX_{pdf.stem}_{hash[:8]}",
        "source_file": pdf.name,
        "sha256": hash,
        "tags": ["ocr", "auto-ingest", "undated_flag_if_needed"],
        "timeline": [],
        "contradictions": [],
        "notes": "Auto-generated VEX stub from OCR pipeline."
    }
    out_path = VEX_OUT / f"{pdf.stem}.json"
    out_path.write_text(json.dumps(vex, indent=2), encoding="utf-8")
    return out_path

def main():
    report = {"processed_pdfs": [], "errors": []}
    for pdf_path in PDF_IN.glob("*.pdf"):
        try:
            print(f"\n📥 Processing: {pdf_path.name}")
            ocr_path = PDF_OCRD / pdf_path.name
            txt_path = TEXT_OUT / (pdf_path.stem + ".txt")

            ocr_pdf(pdf_path, ocr_path)
            extract_text(ocr_path, txt_path)
            file_hash = sha256(ocr_path)
            vex_path = create_vex(ocr_path, txt_path, file_hash)

            report["processed_pdfs"].append({
                "source": str(pdf_path),
                "ocr_pdf": str(ocr_path),
                "text": str(txt_path),
                "vex": str(vex_path),
                "sha256": file_hash
            })
        except Exception as e:
            report["errors"].append({"file": str(pdf_path), "error": str(e)})

    stamp = datetime.datetime.now().strftime("%Y-%m-%d")
    audit_file = AUDIT / f"STATUS_REPORT_{stamp}.json"
    audit_file.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"\n✅ Done. Audit saved to: {audit_file}")

if __name__ == "__main__":
    main()
