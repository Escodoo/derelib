"""Hardened lxml helpers for untrusted DeRE XML."""

from __future__ import annotations

from lxml import etree


def xml_parser():
    return etree.XMLParser(resolve_entities=False, no_network=True)


def fromstring(xml_content):
    """Parse XML without resolving entities or following network URLs."""
    if isinstance(xml_content, bytes):
        payload = xml_content
    else:
        payload = (xml_content or "").encode("utf-8")
    return etree.fromstring(payload, parser=xml_parser())
