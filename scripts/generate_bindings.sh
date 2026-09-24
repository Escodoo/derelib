#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
export PATH="${ROOT}/.venv/bin:${PATH}"
if ! command -v xsdata >/dev/null 2>&1; then
  echo "xsdata is not installed. Run: pip install 'xsdata[cli]'" >&2
  exit 1
fi
rm -rf derelib/bindings/v1_2_0
xsdata generate derelib/schemas/v1_2_0 --config .xsdata.xml
python - <<'PY'
from pathlib import Path

init = Path("derelib/bindings/__init__.py")
init.parent.mkdir(parents=True, exist_ok=True)
if not init.exists():
    init.write_text("")
version_init = Path("derelib/bindings/v1_2_0/__init__.py")
if not version_init.exists():
    version_init.write_text("")

old = """    signature: Signature = field(
        metadata={
            "name": "Signature",
            "type": "Element",
            "namespace": "http://www.w3.org/2000/09/xmldsig#",
        }
    )"""
new = """    signature: None | Signature = field(
        default=None,
        metadata={
            "name": "Signature",
            "type": "Element",
            "namespace": "http://www.w3.org/2000/09/xmldsig#",
        },
    )"""
for path in Path("derelib/bindings/v1_2_0").glob("*.py"):
    text = path.read_text()
    if old in text:
        path.write_text(text.replace(old, new))
PY
echo "Generated bindings under derelib/bindings/v1_2_0"
