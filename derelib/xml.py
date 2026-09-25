"""Hardened lxml helpers for untrusted DeRE XML."""

from __future__ import annotations

from lxml import etree
from lxml.etree import _Element


def xml_parser() -> etree.XMLParser:
    return etree.XMLParser(resolve_entities=False, no_network=True)


def fromstring(xml_content: bytes | str) -> _Element:
    """Parse XML without resolving entities or following network URLs."""
    if isinstance(xml_content, bytes):
        payload = xml_content
    else:
        payload = (xml_content or "").encode("utf-8")
    return etree.fromstring(payload, parser=xml_parser())
