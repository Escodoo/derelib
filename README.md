# derelib

Python binding for the official Brazilian **DeRE** (Declaração Eletrônica de
Regimes Específicos) layout 1.2.0.

`derelib` plays the same role [nfelib](https://github.com/akretion/nfelib)
plays for NF-e / CT-e / MDF-e: serialize and parse events and lots from
dataclasses generated with [xsdata](https://xsdata.readthedocs.io/), validate
them against the official XSD, and sign them with XML-DSig.

Business rules (`tpOper`, MS1135 / MS1147, PGCC checks) belong in the
host application, not in this library.

## Install

```bash
pip install derelib
pip install derelib[sign]   # XML-DSig helpers (signxml)
```

## Scope

| Included                               | Not included                      |
| -------------------------------------- | --------------------------------- |
| Build / parse events, lots and returns | Choice of `tpOper`                |
| XSD validation (unsigned and signed)   | MS1135 / MS1147 / PGCC checks     |
| XML-DSig RSA-SHA256 signing            | Transmission to Receita Integra   |
| NBR 5891 amount formatting             | Host-application data models      |

Supported production helpers today: **D-1001, D-1011, D-1101, D-1106,
D-1121, D-1198, D-1199**, lots and official returns. Transactional events
(D-22xx / D-32xx) are generated from the XSD but are **not** validated in
production yet.

## Quick start

```python
from derelib.bindings.v1_2_0.evt_fech_mensal_v0_0_2 import DeRe
from derelib.validation import validate
from derelib.lote import build_lote
from derelib.signing import sign_event
from derelib.returns import parse_return
from derelib.utils import format_amount

xml = event.to_xml()
errors = validate(xml, "D-1199")
signed = sign_event(xml, key=private_key, cert_pem=cert_pem, reference=event_id)
lote = build_lote("12345678", [{"id": event_id, "xml": signed}])
payload = parse_return(response_xml)
print(format_amount(10.125))  # "10.12" (NBR 5891 half-even)
```

## Regenerating bindings

Bindings under `derelib/bindings/` are generated. Do not edit them by hand.

```bash
pip install xsdata
./scripts/generate_bindings.sh
```

When CGIBS publishes a new layout, update `derelib/schemas/` and regenerate.

## Publishing

Releases use PyPI Trusted Publishing from `.github/workflows/release.yml`
on tags `v*`. One-time setup:

1. Create a pending publisher on TestPyPI and PyPI for project `derelib`:
   owner `Escodoo`, repository `derelib`, workflow `release.yml`,
   environment `pypi`.
2. Push a tag: `git tag v0.1.0 && git push origin v0.1.0`.

## License

MIT. Copyright 2026 Escodoo.
