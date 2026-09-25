#!/bin/bash
# Repo checks (see CLAUDE.md "Testing"). Run from anywhere: scripts/check.sh [--smoke]
#   1. src/build.py must reproduce the committed index.html byte for byte
#   2. the page script must parse (node --check)
#   3. --smoke: headless load + transition with scripts/smoke.py (needs Playwright)
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT

echo "[1/3] build reproduces index.html"
python3 src/build.py --out "$TMP/index.html" >/dev/null
if ! cmp -s "$TMP/index.html" index.html; then
  echo "  FAIL: index.html is stale. Run: python3 src/build.py  (and commit the result)"; exit 1
fi
echo "  ok"

echo "[2/3] node --check on the page script"
python3 - "$TMP" <<'PY'
import pathlib, re, sys
html = pathlib.Path("index.html").read_text(encoding="utf-8")
blocks = re.findall(r"<script[^>]*>(.*?)</script>", html, re.S)
assert blocks, "no <script> block found"
for i, s in enumerate(blocks):
    pathlib.Path(sys.argv[1], f"script{i}.js").write_text(s, encoding="utf-8")
print(f"  {len(blocks)} script block(s)")
PY
for f in "$TMP"/script*.js; do node --check "$f"; done
echo "  ok"

if [[ "${1:-}" == "--smoke" ]]; then
  echo "[3/3] headless smoke test"
  python3 scripts/smoke.py
else
  echo "[3/3] smoke test skipped (pass --smoke)"
fi
