#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
umask 077
if [[ ! -x .venv/bin/python ]]; then
    python3.12 -m venv .venv
fi
# Wariant demonstracyjny używa sterownika SQLite dołączonego do Pythona.
if .venv/bin/python -m pip --version >/dev/null 2>&1; then
    instalator=(.venv/bin/python -m pip)
else
    instalator=(pip --python .venv/bin/python)
fi
grep -v '^mysqlclient==' requirements.txt | "${instalator[@]}" install --disable-pip-version-check -r /dev/stdin
mkdir -p .demo
.venv/bin/python - <<'PY'
from pathlib import Path
from secrets import token_urlsafe

try:
    with Path(".demo/klucz").open("x") as plik:
        print(token_urlsafe(48), file=plik)
except FileExistsError:
    pass
PY
