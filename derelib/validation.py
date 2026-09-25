"""Validate DeRE XML against the official 1.2.0 XSD."""

from __future__ import annotations

from functools import cache
from pathlib import Path

from lxml import etree

from derelib.events import (
    DS_NS,
    EVENT_SCHEMA,
    LOTE_SCHEMA,
    RETURN_SCHEMA,
    RETURN_SCHEMA_BY_NAMESPACE,
)
from derelib.xml import fromstring, xml_parser

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


@cache
def _schema(filename):
    path = SCHEMA_DIR / filename
    return etree.XMLSchema(etree.parse(str(path), xml_parser()))


def _error_messages(error_log):
    return [f"{error.path}: {error.message}" for error in error_log]


def _with_placeholder_signature(root):
    if root.find(f"{{{DS_NS}}}Signature") is not None:
        return root
    clone = fromstring(etree.tostring(root))
    clone.append(fromstring(PLACEHOLDER_SIGNATURE))
    return clone


def _validate_tree(root, filename, signed=False):
    if not signed:
        root = _with_placeholder_signature(root)
    schema = _schema(filename)
    if schema.validate(root):
        return []
    return _error_messages(schema.error_log)


def validate_against_schema(xml_content, schema_path, signed=False):
    """Validate XML against an XSD path. Used by generated root classes."""
    return _validate_tree(fromstring(xml_content), Path(schema_path).name, signed)


def validate(xml_content, event_type, signed=False):
    """Validate an event or D-9xxx return XML.

    Returns an empty list when the payload is valid.
    """
    filename = EVENT_SCHEMA.get(event_type) or RETURN_SCHEMA.get(event_type)
    if not filename:
        raise ValueError(f"Unknown DeRE event type {event_type}")
    return _validate_tree(fromstring(xml_content), filename, signed)


def validate_lote(xml_content):
    """Validate a lot envelope against envioLoteDere."""
    return _validate_tree(fromstring(xml_content), LOTE_SCHEMA, signed=True)


def validate_return(xml_content):
    """Validate a D-9xxx or lot return against its official XSD.

    Returns ``None`` when the payload is not a ``DeRE`` root in a known
    return namespace, otherwise the list of schema errors.
    """
    root = fromstring(xml_content)
    qname = etree.QName(root)
    filename = RETURN_SCHEMA_BY_NAMESPACE.get(qname.namespace)
    if qname.localname != "DeRE" or not filename:
        return None
    return _validate_tree(root, filename)
