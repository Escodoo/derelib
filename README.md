# derelib

[![CI](https://github.com/Escodoo/derelib/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/Escodoo/derelib/actions/workflows/ci.yml?query=branch%3Amain)
[![codecov](https://codecov.io/gh/Escodoo/derelib/branch/main/graph/badge.svg)](https://codecov.io/gh/Escodoo/derelib)
[![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue)](https://github.com/Escodoo/derelib)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Python binding for the official Brazilian **DeRE** (Declaração Eletrônica de
Regimes Específicos) layout **1.2.0**.

`derelib` plays the same role [nfelib](https://github.com/akretion/nfelib)
plays for NF-e / CT-e / MDF-e: serialize and parse events, lots and official
returns from dataclasses generated with [xsdata](https://xsdata.readthedocs.io/),
validate them against the official XSD, and sign them with XML-DSig.

The library has **no host-application dependency**. Business rules (`tpOper`,
MS1135 / MS1147, PGCC checks, journal entries, transmission to Receita Integra)
belong in the application that uses `derelib`.

## Why derelib

- **Bindings stay in sync with the XSD.** Root dataclasses are generated from
  the official 1.2.0 schemas. CI fails if committed bindings drift.
- **Unsigned XML still validates.** Official event XSDs require `ds:Signature`.
  Stored drafts are unsigned, so validation injects a placeholder signature
  unless you pass `signed=True`.
- **Lots do not break the digest.** `build_lote` inserts already-signed event
  XML as-is (`xs:any`), so the XML-DSig digest stays valid.
- **Returns are first-class.** D-9xxx payloads get typed bindings plus a stable
  `parse_return` dictionary (`extract`, `totals`, `taxes`, `ocorrencias`).

## Install

```bash
pip install derelib
pip install "derelib[sign]"   # XML-DSig helpers (signxml)
```

Quote the extra in zsh (and other shells that glob `[]`). Requires Python
3.10+. Runtime dependencies are `lxml>=4.8` and `xsdata>=24.0`. Signing
needs the optional `sign` extra (`signxml`, `cryptography`).

## Scope

| Included                               | Not included                    |
| -------------------------------------- | ------------------------------- |
| Build / parse events, lots and returns | Choice of `tpOper`              |
| XSD validation (unsigned and signed)   | MS1135 / MS1147 / PGCC checks   |
| XML-DSig RSA-SHA256 signing            | Transmission to Receita Integra |
| NBR 5891 amount formatting             | Host-application data models    |

## Event catalog (layout 1.2.0)

Production helpers today:

| Type        | Schema               | Binding helper                      |
| ----------- | -------------------- | ----------------------------------- |
| D-1001      | `evtInfoContrib`     | `event_binding("D-1001")`           |
| D-1011      | `evtPGCC`            | `event_binding("D-1011")`           |
| D-1101      | `evtBalancete`       | `event_binding("D-1101")`           |
| D-1106      | `evtAplicResTec`     | `event_binding("D-1106")`           |
| D-1121      | `evtRelDeducoes`     | `event_binding("D-1121")`           |
| D-1198      | `evtReabertMensal`   | `event_binding("D-1198")`           |
| D-1199      | `evtFechMensal`      | `event_binding("D-1199")`           |
| lote        | `envioLoteDere`      | `build_lote` / `validate_lote`      |
| lote return | `retornoLoteDere`    | `return_binding("retornoLoteDere")` |
| D-9001      | `evtRetornoTabela`   | `return_binding("D-9001")`          |
| D-9101      | `evtRetornoBalan`    | `return_binding("D-9101")`          |
| D-9106      | `evtRetornoAplicFin` | `return_binding("D-9106")`          |
| D-9112      | `evtRetornoRDed`     | `return_binding("D-9112")`          |
| D-9198      | `evtRetornoReabert`  | `return_binding("D-9198")`          |
| D-9199      | `evtRetornoMensal`   | `return_binding("D-9199")`          |

D-9121 (`evtRetornoTitPub`) and D-9209 (`evtRetornoTransac`) have generated
bindings and named constants, but they are **not** validated as production
helpers yet. Transactional events (D-22xx / D-32xx) are generated from the XSD
the same way.

Constants such as `EVENT_D1199` and `RETURN_D9101` are exported from
`derelib`.

## Quick start

### Parse and serialize

```python
from derelib import event_binding

DeRe = event_binding("D-1199")
event = DeRe.from_path("tests/samples/v1_2_0/d1199.xml")
# event = DeRe.from_xml(xml_string)

event.evtFechMensal.ideContrib.nrInsc  # "00000000"
event.evtFechMensal.idePeriodo.perApur  # "2026-10"

xml = event.to_xml()
```

Every generated root class is a `DeRe` dataclass mixed with `DereMixin`
(`from_xml`, `from_path`, `to_xml`, `validate_xml`, `sign_xml`).

### Build an event

```python
from datetime import datetime, timezone

from derelib import event_binding, make_event_id
from derelib.bindings.v1_2_0.evt_fech_mensal_v0_0_2 import (
    IdeEventoAplicEmi,
    IdeEventoTpAmb,
    IdeEventoTpOper,
)

DeRe = event_binding("D-1199")
event_id = make_event_id(
    "D-1199", "00000000", datetime(2026, 9, 24, 16, 25, 7, tzinfo=timezone.utc), 1
)
event = DeRe(
    evtFechMensal=DeRe.EvtFechMensal(
        id=event_id,
        ideEvento=DeRe.EvtFechMensal.IdeEvento(
            tpOper=IdeEventoTpOper.VALUE_1,
            tpAmb=IdeEventoTpAmb.VALUE_2,
            aplicEmi=IdeEventoAplicEmi.VALUE_1,
            verAplic="derelib-0.1.0",
        ),
        ideContrib=DeRe.EvtFechMensal.IdeContrib(nrInsc="00000000"),
        idePeriodo=DeRe.EvtFechMensal.IdePeriodo(perApur="2026-10"),
    )
)
xml = event.to_xml()
errors = event.validate_xml()  # [] when the payload matches the XSD
```

### Validate

```python
from derelib import validate, validate_lote, validate_return

validate(xml, "D-1199")  # unsigned: placeholder Signature is injected
validate(signed_xml, "D-1199", signed=True)
validate(return_xml, "D-9101")  # outgoing and D-9xxx share this helper
validate_lote(lote_xml)
validate_return(return_xml)  # [] for D-9xxx or retornoLoteDere
```

`validate` / `validate_lote` / `validate_xml` return a list of XSD error
strings (empty means valid). `validate_return` returns `None` when the payload
is not a `DeRE` root in a known return namespace (including
`retornoLoteDere`).

### Sign and assemble a lot

```python
from derelib import build_lote
from derelib.signing import sign_event

signed = sign_event(xml, key=private_key, cert_pem=cert_pem, reference=event_id)
# or: signed = event.sign_xml(private_key, cert_pem, event_id)

lote = build_lote("00000000", [{"id": event_id, "xml": signed}])
```

`key` and `cert_pem` are PEM bytes or strings. `reference` is the event `id`
attribute **without** the leading `#`. Signing requires `derelib[sign]`.
`sign_event_with_certificate` accepts an `erpbrasil.assinatura` certificate
object.

Signed XML is opaque. Calling `to_xml()` on a binding parsed from a signed
payload invalidates the digest (the method emits a `UserWarning`). Pass the
original signed string to `build_lote`; do not reserialize it.

### Parse official returns

```python
from derelib import parse_return, return_binding, validate_return

payload = parse_return(response_xml)
payload["cdResposta"]  # lot status only; None on a single D-9xxx
payload["protocolo"]
payload["dhProcessamento"]
payload["events"][0]["nrRecibo"]
payload["events"][0]["ocorrencias"]

# D-9001 validity photo
payload["extract"]["validity"][0]["iniValid"]
payload["extract"]["gaps"][0]["iniLacuna"]

# D-9101 / D-9106 totals
payload["perApur"]
payload["totals"][0]["vApurTot"]

# D-9199 tax groups (regime 1=financial, 2=health, 3=programs)
payload["taxes"]["lines"][0]["codBC"]
payload["taxes"]["total"]["vCBS"]

cls = return_binding("D-9101")
parsed = cls.from_xml(response_xml)
validate_return(response_xml)  # [] when valid
```

Header fields such as `nrRecibo` are read from `ideStatus` / `infoRecEv` only.
D-9001 repeats `nrRecibo` inside `extratoEventos`; that copy is **not** used
as the event receipt.

Values stay strings (`None` when absent). Comparing RFB totals to a local
trial balance is a host job. A lot envelope never copies `cdRetorno` or
`nrRecibo` to the top level; those keys stay inside `events`.

## `parse_return` dictionary

Top-level keys (lot envelope, or a single D-9xxx wrapped as one event):

| Key               | Meaning                              |
| ----------------- | ------------------------------------ |
| `cdResposta`      | Lot status code (`None` when absent) |
| `descResposta`    | Lot status text                      |
| `protocolo`       | Lot reception protocol               |
| `dhRecepcao`      | Lot reception timestamp              |
| `dhProcessamento` | Lot processing timestamp             |
| `ocorrencias`     | Lot-level occurrences only           |
| `events`          | List of per-event dictionaries       |

Each event (and the top level when a single return is parsed) includes:

| Key                           | Meaning                                       |
| ----------------------------- | --------------------------------------------- |
| `id`                          | Event or envelope `id`                        |
| `cdRetorno`                   | Event status code                             |
| `descRetorno`                 | Event status text                             |
| `nrRecibo`                    | Receipt from `infoRecEv`                      |
| `seqEvento`                   | Sequence inside the period                    |
| `tpEv`                        | Original event type (`D-1101`, …)             |
| `perApur`                     | Apuration period (`AAAA-MM`)                  |
| `hash`                        | Event hash                                    |
| `protocolo` / `protocoloLote` | Processing protocol                           |
| `dhRecepcao` / `dhProcess`    | Official timestamps (strings)                 |
| `returnTag`                   | Local name (`evtRetornoBalan`, …)             |
| `nrReciboPGCC`                | Linked D-1011 receipt                         |
| `receipts`                    | Linked D-1101 / D-1106 / D-1121 receipts      |
| `extract`                     | D-9001 `{validity, gaps}`                     |
| `totals`                      | D-9101 `gTotalCodTrib` or D-9106 `{vApurTot}` |
| `taxes`                       | D-9199 `{lines, total}`                       |
| `ocorrencias`                 | List of `{codigo, descricao, …}`              |

## Amounts

`format_amount` uses NBR 5891 half-even rounding with two decimals:

```python
from derelib import format_amount

format_amount(10.125)  # "10.12"
format_amount(10.135)  # "10.14"
format_amount(-1.5)  # "1.50"
format_amount(-1.5, signed=True)  # "-1.50"
```

Official returns use seven fractional digits. `parse_datetime` keeps the
timezone (naive values become UTC):

```python
from derelib import parse_datetime

parse_datetime("2026-12-05T12:00:00.1234567-03:00")
```

`make_event_id(event_type, nr_insc, moment, seq)` builds the 42-character
structured id. The host owns the sequential counter.

## Public API

Imported from `derelib`:

| Helper                          | Role                                        |
| ------------------------------- | ------------------------------------------- |
| `event_binding(type)`           | Generated root class for a production event |
| `return_binding(type)`          | Generated root class for a D-9xxx return    |
| `validate(xml, type, signed=)`  | XSD check for events and returns            |
| `validate_lote(xml)`            | XSD check for `envioLoteDere`               |
| `validate_return(xml)`          | XSD check by return namespace               |
| `build_lote(nr_insc, events)`   | Lot envelope; inner XML inserted as-is      |
| `parse_return(xml)`             | Stable dict for lot and D-9xxx returns      |
| `format_amount(value, signed=)` | NBR 5891 half-even, 2 decimals              |
| `parse_datetime(value)`         | Aware datetime from official `xs:dateTime`  |
| `make_event_id(...)`            | 42-character structured event id            |
| `EVENT_*` / `RETURN_*`          | Official type strings                       |

Signing helpers live in `derelib.signing` (`sign_event`,
`sign_event_with_certificate`).

## Regenerating bindings

Bindings under `derelib/bindings/` are generated. Do not edit them by hand.

```bash
pip install "xsdata[cli]"
./scripts/generate_bindings.sh
```

When CGIBS publishes a new layout, update `derelib/schemas/` and regenerate.
The generate script also makes `ds:Signature` optional on the dataclass so
unsigned drafts can be built before signing.

## Development

```bash
python -m venv .venv
.venv/bin/pip install -e ".[dev]"
.venv/bin/pre-commit install
.venv/bin/pytest
.venv/bin/pre-commit run --all-files
```

The `dev` extra installs `pre-commit`, `mypy` and the test dependencies.
Use `".[test]"` when you only need pytest. See [CONTRIBUTING.md](CONTRIBUTING.md).

Anonymized golden fixtures live in `tests/samples/v1_2_0/`. Coverage of
generated bindings is omitted; the project threshold is 90% on the hand-written
package.

## Publishing

Releases use PyPI Trusted Publishing from `.github/workflows/release.yml`
on tags `v*`. One-time setup:

1. Create a pending publisher on TestPyPI and PyPI for project `derelib`:
   owner `Escodoo`, repository `derelib`, workflow `release.yml`,
   environment `pypi`.
2. Push a tag: `git tag v0.1.0 && git push origin v0.1.0`.

## License

MIT. Copyright 2026 Escodoo.

See also [nfelib](https://github.com/akretion/nfelib) for the same binding
pattern on NF-e / NFS-e / CT-e / MDF-e / BP-e.
