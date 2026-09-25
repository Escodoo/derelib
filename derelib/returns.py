"""Parse official DeRE return XML into a stable dictionary."""

from __future__ import annotations

from lxml import etree

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


def _localname(element):
    return etree.QName(element).localname


def _child(element, name):
    if element is None:
        return None
    for child in element.iterchildren(tag=etree.Element):
        if _localname(child) == name:
            return child
    return None


def _path(element, *names):
    for name in names:
        element = _child(element, name)
        if element is None:
            return None
    return element


def _path_text(element, *names):
    element = _path(element, *names)
    if element is None or not element.text:
        return False
    return element.text.strip()


def _children(element, name):
    if element is None:
        return []
    return [
        child
        for child in element.iterchildren(tag=etree.Element)
        if _localname(child) == name
    ]


def _return_totals(node):
    info = _child(node, "infoEvento")
    balan = _child(info, "infoTotBalan")
    if balan is not None:
        return [
            {name: _path_text(group, name) for name in RETURN_TOTAL_FIELDS}
            for group in _children(balan, "gTotalCodTrib")
        ]
    total = _path_text(info, "infoTotAplicFin", "vApurTot")
    return [{"vApurTot": total}] if total else []


def _return_taxes(node):
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


def _return_receipts(node):
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


def _return_extract(node):
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


def _return_node(root):
    if _localname(root).startswith("evtRetorno"):
        return root
    if _localname(root) == "DeRE":
        for child in root.iterchildren(tag=etree.Element):
            if _localname(child).startswith("evtRetorno"):
                return child
    return None


def _occurrence_vals(element):
    occurrence = {}
    for child in element:
        occurrence[_localname(child)] = (child.text or "").strip()
    return occurrence


def _read_return_header(node, data):
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
        "seqEvento": False,
        "dhRecepcao": False,
        "dhProcess": False,
        "returnTag": False,
        "xml": False,
        "perApur": False,
        "nrReciboPGCC": False,
        "totals": [],
        "taxes": {"lines": [], "total": {}},
        "receipts": {},
        "extract": {},
        "ocorrencias": [],
    }
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


def parse_return(xml_content):
    """Normalize a lot or event return into a stable dictionary.

    Keys include the lot status (``cdResposta``, ``descResposta``,
    ``events``) and, for each D-9xxx payload, ``seqEvento``, ``perApur``,
    ``extract`` (D-9001), ``totals`` (D-9101 / D-9106), ``taxes`` (D-9199)
    and ``ocorrencias``.
    """
    if isinstance(xml_content, bytes):
        payload = xml_content
    else:
        payload = (xml_content or "").encode("utf-8")
    root = etree.fromstring(payload)
    event = _parse_event_return(root)
    data = dict(event, cdResposta=False, descResposta=False, events=[])
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
        data["events"] = [event]
    return data
