# Changelog

## Unreleased

- Treat D-9xxx returns as first-class layout helpers: named types,
  `return_binding`, `validate_return` and structured `parse_return`
  (`extract`, `totals`, `taxes`).

## 0.1.0 (2026-09-24)

- First public release: xsdata bindings for DeRE layout 1.2.0.
- Helpers for XSD validation, XML-DSig signing, lot assembly and return
  parsing. Production coverage is D-1001, D-1011, D-1101, D-1106, D-1121,
  D-1198, D-1199 plus lots and official returns.
