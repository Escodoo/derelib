"""Parse official DeRE return XML into a stable dictionary."""

from __future__ import annotations

from typing import Any

from lxml import etree
from lxml.etree import _Element

from derelib.xml import fromstring

RETURN_HEADER = {
    "ideStatus": ("cdRetorno", "descRetorno"),
    "infoRecEv": (
        "nrRecibo",
        "seqEvento",
        "protocoloLote",
        "protocolo",
        "dhRecepcao",
        "dhProcess",
        "tpEv",
        "hash",
    ),
}
RETURN_TOTAL_FIELDS = (
    "codTrib",
    "indTribISS",
    "vApurTot",
    "vTotSaldoInic",
    "vTotSaldoFinal",
)
# D-9199 groups mapped to the official secondary-regime codes.
RETURN_TAX_GROUPS = {
    "infoTotFinanceiro": "1",
    "infoTotSaude": "2",
    "infoTotProg": "3",
}
RETURN_DETBC_PATHS = {
    "codBC": ("codBC",),
    "xDetBC": ("xDetBC",),
    "memoriaCalculo": ("memoriaCalculo",),
    "vBCIBS": ("gBCIBS", "vBCIBS"),
    "vBCNIBS": ("gBCIBS", "vBCNIBS"),
    "vDedBCNIBS": ("gBCIBS", "vDedBCN"),
    "vBCApurIBS": ("gBCIBS", "vBCApurIBS"),
    "pIBSMun": ("gBCIBS", "pIBSMun"),
    "vIBSMun": ("gBCIBS", "vIBSMun"),
    "pIBSUF": ("gBCIBS", "pIBSUF"),
    "vIBSUF": ("gBCIBS", "vIBSUF"),
    "pIBS": ("gBCIBS", "pIBS"),
    "vIBSTot": ("gBCIBS", "vIBSTot"),
    "vBCCBS": ("gBCCBS", "vBCCBS"),
    "vBCNCBS": ("gBCCBS", "vBCNCBS"),
    "vDedBCNCBS": ("gBCCBS", "vDedBCN"),
    "vBCApurCBS": ("gBCCBS", "vBCApurCBS"),
    "pCBS": ("gBCCBS", "pCBS"),
    "vCBS": ("gBCCBS", "vCBS"),
    "vBCIS": ("gBCIS", "vBCIS"),
    "vBCApurIS": ("gBCIS", "vBCApurIS"),
    "pIS": ("gBCIS", "pIS"),
    "vIS": ("gBCIS", "vIS"),
    "vSaldoFinalBCNIBS": ("infoBCN", "gBCNIBS", "vSaldoFinal"),
    "vSaldoFinalBCNCBS": ("infoBCN", "gBCNCBS", "vSaldoFinal"),
}
RETURN_TAX_TOTALS = ("vIS", "vIBSMun", "vIBSUF", "vIBSTot", "vCBS")
RETURN_VALIDITY_FIELDS = (
    "nrRecibo",
    "iniValid",
    "fimValid",
    "fimValidEfetiva",
    "indAjusteAuto",
)
RETURN_GAP_FIELDS = ("iniLacuna", "fimLacuna")


def _localname(element: Any) -> str:
    tag = getattr(element, "tag", None)
    if not isinstance(tag, str):
        return ""
    return etree.QName(element).localname


def _child(element: _Element | None, name: str) -> _Element | None:
    if element is None:
        return None
    for child in element.iterchildren(tag=etree.Element):
        if _localname(child) == name:
            return child
    return None


def _path(element: _Element | None, *names: str) -> _Element | None:
    for name in names:
        element = _child(element, name)
        if element is None:
            return None
    return element


def _path_text(element: _Element | None, *names: str) -> str | None:
    element = _path(element, *names)
    if element is None or not element.text:
        return None
    return element.text.strip()


def _children(element: _Element | None, name: str) -> list[_Element]:
    if element is None:
        return []
    return [
        child
        for child in element.iterchildren(tag=etree.Element)
        if _localname(child) == name
    ]


def _return_totals(node: _Element | None) -> list[dict[str, str | None]]:
    info = _child(node, "infoEvento")
    balan = _child(info, "infoTotBalan")
    if balan is not None:
        return [
            {name: _path_text(group, name) for name in RETURN_TOTAL_FIELDS}
            for group in _children(balan, "gTotalCodTrib")
        ]
    total = _path_text(info, "infoTotAplicFin", "vApurTot")
    return [{"vApurTot": total}] if total else []


def _return_taxes(node: _Element | None) -> dict[str, Any]:
    info = _child(node, "infoEvento")
    lines = []
    for group, regime in RETURN_TAX_GROUPS.items():
        for det in _children(_child(info, group), "detBC"):
            vals = {
                key: _path_text(det, *path) for key, path in RETURN_DETBC_PATHS.items()
            }
            vals["regime"] = regime
            lines.append(vals)
    general = _child(info, "totalTributosGeral")
    total = {}
    if general is not None:
        total = {name: _path_text(general, name) for name in RETURN_TAX_TOTALS}
    return {"lines": lines, "total": total}


def _return_receipts(node: _Element | None) -> dict[str, Any]:
    info_adic = _path(node, "infoEvento", "infoAdic")
    return {
        "nrReciboBalancete": _path_text(info_adic, "nrReciboBalancete"),
        "nrReciboAplicFin": _path_text(info_adic, "nrReciboAplicFin"),
        "nrReciboRelDedu": [
            element.text.strip()
            for element in _children(info_adic, "nrReciboRelDedu")
            if element.text
        ],
    }


def _return_extract(node: _Element | None) -> dict[str, Any]:
    """Return the D-9001 validity photo, or {} when the group is absent."""
    extract = _child(node, "extratoEventos")
    if extract is None:
        return {}
    return {
        "validity": [
            {name: _path_text(det, name) for name in RETURN_VALIDITY_FIELDS}
            for det in _children(extract, "detEvento")
        ],
        "gaps": [
            {name: _path_text(det, name) for name in RETURN_GAP_FIELDS}
            for det in _children(extract, "detLacuna")
        ],
    }


def _return_node(root: _Element) -> _Element | None:
    if _localname(root).startswith("evtRetorno"):
        return root
    if _localname(root) == "DeRE":
        for child in root.iterchildren(tag=etree.Element):
            if _localname(child).startswith("evtRetorno"):
                return child
    return None


def _lot_node(root: _Element) -> _Element | None:
    if _localname(root) == "retornoLoteEventos":
        return root
    if _localname(root) == "DeRE":
        return _child(root, "retornoLoteEventos")
    return None


def _empty_event() -> dict[str, Any]:
    return {
        "id": None,
        "cdRetorno": None,
        "descRetorno": None,
        "nrRecibo": None,
        "protocoloLote": None,
        "protocolo": None,
        "tpEv": None,
        "hash": None,
        "seqEvento": None,
        "dhRecepcao": None,
        "dhProcess": None,
        "returnTag": None,
        "xml": None,
        "perApur": None,
        "nrReciboPGCC": None,
        "totals": [],
        "taxes": {"lines": [], "total": {}},
        "receipts": {},
        "extract": {},
        "ocorrencias": [],
    }


def _occurrence_vals(element: _Element) -> dict[str, str]:
    occurrence = {}
    for child in element:
        occurrence[_localname(child)] = (child.text or "").strip()
    return occurrence


def _read_return_header(node: _Element, data: dict[str, Any]) -> dict[str, Any]:
    # D-9001 repeats nrRecibo inside extratoEventos, so the header must be
    # read from its own groups only.
    for group, names in RETURN_HEADER.items():
        parent = _child(node, group)
        source = parent if parent is not None else node
        for name in names:
            element = _child(source, name)
            if element is not None and element.text:
                data[name] = element.text.strip()
    return data


def _parse_event_return(root: _Element) -> dict[str, Any]:
    data = _empty_event()
    envelope = root
    node = _return_node(root)
    if node is not None:
        data.update(
            {
                "returnTag": _localname(node),
                "xml": etree.tostring(envelope, encoding="unicode"),
                "perApur": _path_text(node, "infoEvento", "idePeriodo", "perApur"),
                "nrReciboPGCC": _path_text(
                    node, "infoEvento", "infoAdic", "nrReciboPGCC"
                ),
                "totals": _return_totals(node),
                "taxes": _return_taxes(node),
                "receipts": _return_receipts(node),
                "extract": _return_extract(node),
            }
        )
        _read_return_header(node, data)
        root = node
    if root.get("id"):
        data["id"] = root.get("id")
    elif envelope.get("id"):
        data["id"] = envelope.get("id")
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
            if node is None and element.text:
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


def _lot_ocorrencias(status: _Element | None) -> list[dict[str, str]]:
    wrapper = _child(status, "ocorrencias")
    if wrapper is None:
        return []
    occurrences = []
    for element in _children(wrapper, "ocorrencia"):
        occurrence = _occurrence_vals(element)
        if occurrence:
            occurrences.append(occurrence)
    if occurrences:
        return occurrences
    occurrence = _occurrence_vals(wrapper)
    return [occurrence] if occurrence and "codigo" in occurrence else []


def _parse_lot_return(lote: _Element) -> dict[str, Any]:
    """Keep only lot-envelope fields at the top level."""
    status = _child(lote, "status")
    recepcao = _child(lote, "dadosRecepcaoLote")
    processamento = _child(lote, "dadosProcessamentoLote")
    events = []
    for evento in _children(_child(lote, "retornoEventos"), "evento"):
        inner = next((child for child in evento.iterchildren(tag=etree.Element)), None)
        parsed = _parse_event_return(inner if inner is not None else evento)
        parsed["id"] = evento.get("id") or parsed.get("id")
        events.append(parsed)
    data = _empty_event()
    data.update(
        {
            "id": lote.get("id") or None,
            "cdResposta": _path_text(status, "cdResposta"),
            "descResposta": _path_text(status, "descResposta"),
            "protocolo": _path_text(recepcao, "protocolo"),
            "dhRecepcao": _path_text(recepcao, "dhRecepcao"),
            "dhProcessamento": _path_text(processamento, "dhProcessamento"),
            "ocorrencias": _lot_ocorrencias(status),
            "events": events,
        }
    )
    return data


def parse_return(xml_content: bytes | str | None) -> dict[str, Any]:
    """Normalize a lot or event return into a stable dictionary.

    A lot envelope exposes only lot fields at the top level
    (``cdResposta``, ``descResposta``, ``protocolo``, ``dhRecepcao``,
    ``dhProcessamento``, lot ``ocorrencias`` and ``events``). Event
    fields stay inside ``events``. A single D-9xxx payload also fills
    ``seqEvento``, ``perApur``, ``extract`` (D-9001), ``totals``
    (D-9101 / D-9106), ``taxes`` (D-9199) and ``ocorrencias``.
    """
    root = fromstring(xml_content or "")
    lote = _lot_node(root)
    if lote is not None:
        return _parse_lot_return(lote)
    event = _parse_event_return(root)
    data = dict(
        event,
        cdResposta=None,
        descResposta=None,
        dhProcessamento=None,
        events=[],
    )
    if event.get("cdRetorno"):
        data["events"] = [event]
    return data
