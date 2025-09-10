
set -e
export PATH="/opt/homebrew/bin:$PATH"
ROOT="$HOME/Documents/the_undercover_victim"
VENV="$ROOT/06_scripts/.venv/bin/activate"
echo "== PolicePlease Doctor =="
echo "- ROOT: $ROOT"
echo "- PATH head: $(echo $PATH | awk -F: '{print $1,$2,$3}')"
echo
for t in ocrmypdf tesseract gs qpdf pdftotext exiftool ffmpeg; do
  if command -v "$t" >/dev/null; then
    echo "✔ $t: $(command -v $t)"
  else
    echo "✖ $t: NOT FOUND"
  fi
done
echo
if [ -f "$VENV" ]; then
  echo "✔ venv found at $VENV"
  source "$VENV"
  echo "✔ python: $(python -V)"
  echo "✔ pip:    $(pip -V)"
  python - <<PY
try:
  import pdfminer, PyPDF2, pikepdf, mutagen
  print("✔ python deps: pdfminer, PyPDF2, pikepdf, mutagen OK")
except Exception as e:
  print("✖ python deps error:", e)
PY
else
  echo "✖ venv missing ($VENV)"
fi
echo
for d in 01_evidence/pdf_unprocessed 01_evidence/pdf_ocrd 01_evidence/text 01_evidence/vex 01_evidence/audio 08_audit; do
  [ -d "$ROOT/$d" ] && echo "✔ dir: $d" || echo "✖ dir missing: $d"
done
