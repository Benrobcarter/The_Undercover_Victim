
set -euo pipefail
export PATH="/opt/homebrew/bin:$PATH"
ROOT="$HOME/Documents/the_undercover_victim"
source "$ROOT/06_scripts/.venv/bin/activate"
python "$ROOT/06_scripts/policeplease_merge.py" "$@"
