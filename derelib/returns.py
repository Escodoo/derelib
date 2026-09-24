"""Parse official DeRE return XML into the dict used by host applications."""

from __future__ import annotations

from lxml import etree


def _localname(element):
    return etree.QName(element).localname


def _occurrence_vals(element):
    occurrence = {}
    for child in element:
        occurrence[_localname(child)] = (child.text or "").strip()
    return occurrence


def _parse_event_return(root):
    data = {
        "id": False,
        "cdRetorno": False,
        "descRetorno": False,
        "nrRecibo": False,
        "protocoloLote": False,
        "protocolo": False,
        "tpEv": False,
        "hash": False,
        "ocorrencias": [],
    }
    if root.get("id"):
        data["id"] = root.get("id")
    for element in root.iter():
        name = _localname(element)
        if name in (
            "cdRetorno",
            "descRetorno",
            "nrRecibo",
            "protocoloLote",
            "protocolo",
            "tpEv",
            "hash",
        ):
            if element.text:
                data[name] = element.text.strip()
        elif name == "ocorrencias":
            occurrence = _occurrence_vals(element)
            if occurrence and "codigo" in occurrence:
                data["ocorrencias"].append(occurrence)
        elif name == "ocorrencia":
            occurrence = _occurrence_vals(element)
            if occurrence:
                data["ocorrencias"].append(occurrence)
    return data


def parse_return(xml_content):
    """Normalize a lot or event return into a stable dictionary.

    Keys are stable for host applications: ``cdResposta``,
    ``descResposta``, ``events``, ``ocorrencias``.
    """
    if isinstance(xml_content, bytes):
        payload = xml_content
    else:
        payload = (xml_content or "").encode("utf-8")
    root = etree.fromstring(payload)
    data = _parse_event_return(root)
    data.update(
        {
            "cdResposta": False,
            "descResposta": False,
            "events": [],
        }
    )
    for element in root.iter():
        name = _localname(element)
        if name in ("cdResposta", "descResposta") and element.text:
            data[name] = element.text.strip()
        elif name == "evento" and element.getparent() is not None:
            parent = _localname(element.getparent())
            if parent == "retornoEventos":
                inner = next(iter(element), None)
                parsed = _parse_event_return(inner if inner is not None else element)
                parsed["id"] = element.get("id") or parsed.get("id")
                data["events"].append(parsed)
    if not data["events"] and data.get("cdRetorno"):
        data["events"] = [
            {
                key: data.get(key)
                for key in (
                    "id",
                    "cdRetorno",
                    "descRetorno",
                    "nrRecibo",
                    "protocoloLote",
                    "protocolo",
                    "tpEv",
                    "hash",
                    "ocorrencias",
                )
            }
        ]
    return data
