# Changelog

## 0.1.0 (2026-09-25)

- First public release: xsdata bindings for DeRE layout 1.2.0.
- Helpers for XSD validation, XML-DSig signing, lot assembly and return
  parsing. Production coverage is D-1001, D-1011, D-1101, D-1106, D-1121,
  D-1198, D-1199 plus lots and official returns.
- Treat D-9xxx returns as first-class layout helpers: named types,
  `return_binding`, `validate_return` and structured `parse_return`
  (`extract`, `totals`, `taxes`).
- `parse_return` keeps lot-envelope fields isolated from nested events
  and uses `None` for missing values.
- Official XSD fixtures for lot and event returns, including D-9112 and
  D-9198.
- Hardened XML parser (`resolve_entities=False`, `no_network=True`).
- `make_event_id`, `parse_datetime` and `retornoLoteDere` validation.
- `to_xml()` warns when reserializing a signed binding.
- Release workflow tests the tag against `__version__` before publishing.
