# Contributing to derelib

Thank you for helping keep the DeRE layout binding accurate.

## Scope

`derelib` serializes, parses, validates and signs official DeRE XML.
Business rules (`tpOper`, MS1135 / MS1147, PGCC checks, transmission)
belong in the host application.

## Setup

```bash
python -m venv .venv
.venv/bin/pip install -e ".[dev]"
.venv/bin/pre-commit install
```

## Checks

```bash
.venv/bin/pytest
.venv/bin/pre-commit run --all-files
```

Do not edit files under `derelib/bindings/` by hand. After changing an
XSD, run `./scripts/generate_bindings.sh`.

## Commits

Use short English commit messages that explain **why**. Keep one theme
per commit (API change, fixtures, packaging, docs).

## Pull requests

Open a PR against `main`. CI must stay green: pre-commit, pytest on
Python 3.10–3.13, the bindings drift check and the minimum-deps job.
