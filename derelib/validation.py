"""Validate DeRE XML against the official 1.2.0 XSD."""

from __future__ import annotations

from functools import cache
from pathlib import Path

from lxml import etree

from derelib.events import DS_NS, EVENT_SCHEMA, LOTE_SCHEMA

SCHEMA_DIR = Path(__file__).resolve().parent / "schemas" / "v1_2_0"

# Official event XSDs require ds:Signature. Stored DeRE XML stays unsigned, so
# unsigned validation appends this placeholder before checking the schema.
PLACEHOLDER_SIGNATURE = (
    f'<ds:Signature xmlns:ds="{DS_NS}">'
    "<ds:SignedInfo>"
    '<ds:CanonicalizationMethod Algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315"/>'
    '<ds:SignatureMethod Algorithm="http://www.w3.org/2001/04/xmldsig-more#rsa-sha256"/>'
    '<ds:Reference URI="#placeholder">'
    '<ds:DigestMethod Algorithm="http://www.w3.org/2001/04/xmlenc#sha256"/>'
    "<ds:DigestValue>AA==</ds:DigestValue>"
    "</ds:Reference>"
    "</ds:SignedInfo>"
    "<ds:SignatureValue>AA==</ds:SignatureValue>"
    "</ds:Signature>"
)


def _to_bytes(xml_content):
    if isinstance(xml_content, bytes):
        return xml_content
    return (xml_content or "").encode("utf-8")


@cache
def _schema(filename):
    path = SCHEMA_DIR / filename
    parser = etree.XMLParser(resolve_entities=False, no_network=True)
    return etree.XMLSchema(etree.parse(str(path), parser))


def _error_messages(error_log):
    return [f"{error.path}: {error.message}" for error in error_log]


def _with_placeholder_signature(root):
    if root.find(f"{{{DS_NS}}}Signature") is not None:
        return root
    clone = etree.fromstring(etree.tostring(root))
    clone.append(etree.fromstring(PLACEHOLDER_SIGNATURE))
    return clone


def validate_against_schema(xml_content, schema_path, signed=False):
    """Validate XML against an XSD path. Used by generated root classes."""
    root = etree.fromstring(_to_bytes(xml_content))
    if not signed:
        root = _with_placeholder_signature(root)
    schema = _schema(Path(schema_path).name)
    if schema.validate(root):
        return []
    return _error_messages(schema.error_log)


def validate(xml_content, event_type, signed=False):
    """Validate an event XML. Returns an empty list when the payload is valid."""
    filename = EVENT_SCHEMA.get(event_type)
    if not filename:
        raise ValueError(f"Unknown DeRE event type {event_type}")
    root = etree.fromstring(_to_bytes(xml_content))
    if not signed:
        root = _with_placeholder_signature(root)
    schema = _schema(filename)
    if schema.validate(root):
        return []
    return _error_messages(schema.error_log)


def validate_lote(xml_content):
    """Validate a lot envelope against envioLoteDere."""
    root = etree.fromstring(_to_bytes(xml_content))
    schema = _schema(LOTE_SCHEMA)
    if schema.validate(root):
        return []
    return _error_messages(schema.error_log)
