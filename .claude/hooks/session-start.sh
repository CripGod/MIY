#!/bin/bash
# SessionStart hook for Claude Code on the web.
# Installs what the repo's scripts need so a web session can run src/tools/*.py,
# scripts/check.sh --smoke and the README "Testing" recipe without setup.
set -euo pipefail

# Local sessions: do nothing (developers manage their own environment).
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

cd "${CLAUDE_PROJECT_DIR:-$(pwd)}"

# Asset tools need Pillow + numpy (src/tools/README.md).
# Headless capture needs the Python Playwright bindings. The web container ships
# Chromium for Playwright 1.56 (PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers, chromium-1194),
# so pin the same version and nothing gets downloaded.
python3 -m pip install --quiet --disable-pip-version-check pillow numpy 'playwright==1.56.0'

if [ ! -e "${PLAYWRIGHT_BROWSERS_PATH:-/opt/pw-browsers}/chromium-1194" ]; then
  echo "session-start: pre-installed Chromium revision differs from Playwright 1.56; scripts/smoke.py may need 'playwright install chromium'" >&2
fi

python3 -c "import PIL, numpy, playwright; print('session-start: pillow', PIL.__version__, 'numpy', numpy.__version__, 'playwright ready')"
