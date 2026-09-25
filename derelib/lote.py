"""Assemble a DeRE lot without reserializing already signed events."""

from __future__ import annotations

from lxml import etree

from derelib.events import LOTE_NAMESPACE
from derelib.xml import fromstring


def build_lote(nr_insc, events):
    """Build a lot envelope.

    Each item in ``events`` is ``{"id": event_id, "xml": signed_or_raw_xml}``.
    Inner event XML is inserted as-is so an existing XML-DSig digest stays
    valid.
    """
    root = etree.Element("DeRE", nsmap={None: LOTE_NAMESPACE})
    lote = etree.SubElement(root, "loteEventos")
    ide = etree.SubElement(lote, "ideContrib")
    insc = etree.SubElement(ide, "nrInsc")
    insc.text = str(nr_insc)
    eventos = etree.SubElement(lote, "eventos")
    for event in events:
        node = etree.SubElement(eventos, "evento", id=event["id"])
        xml = event["xml"]
        node.append(fromstring(xml))
    return etree.tostring(root, encoding="unicode")
