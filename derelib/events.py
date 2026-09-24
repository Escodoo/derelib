"""Official DeRE event identifiers and schema mapping."""

from __future__ import annotations

from importlib import import_module

EVENT_D1001 = "D-1001"
EVENT_D1011 = "D-1011"
EVENT_D1101 = "D-1101"
EVENT_D1106 = "D-1106"
EVENT_D1121 = "D-1121"
EVENT_D1198 = "D-1198"
EVENT_D1199 = "D-1199"

EVENT_SCHEMA = {
    EVENT_D1001: "evtInfoContrib-v1_0_1.xsd",
    EVENT_D1011: "evtPGCC-v1_0_3.xsd",
    EVENT_D1101: "evtBalancete-v1_0_1.xsd",
    EVENT_D1106: "evtAplicResTec-v1_0_0.xsd",
    EVENT_D1121: "evtRelDeducoes-v0_0_1.xsd",
    EVENT_D1198: "evtReabertMensal-v0_0_1.xsd",
    EVENT_D1199: "evtFechMensal-v0_0_2.xsd",
}

EVENT_NAMESPACE = {
    EVENT_D1001: "http://www.dere.gov.br/schemas/evtInfoContrib/v1_0_1",
    EVENT_D1011: "http://www.dere.gov.br/schemas/evtPGCC/v1_0_3",
    EVENT_D1101: "http://www.dere.gov.br/schemas/evtBalancete/v1_0_1",
    EVENT_D1106: "http://www.dere.gov.br/schemas/evtAplicResTec/v1_0_0",
    EVENT_D1121: "http://www.dere.gov.br/schemas/evtRelDeducoes/v0_0_1",
    EVENT_D1198: "http://www.dere.gov.br/schemas/evtReabertMensal/v0_0_1",
    EVENT_D1199: "http://www.dere.gov.br/schemas/evtFechMensal/v0_0_2",
}

LOTE_SCHEMA = "envioLoteDere-v1_0_1.xsd"
LOTE_NAMESPACE = "http://www.dere.gov.br/schemas/envioLoteDere/v1_0_1"
DS_NS = "http://www.w3.org/2000/09/xmldsig#"

_BINDING_MODULE = {
    EVENT_D1001: "derelib.bindings.v1_2_0.evt_info_contrib_v1_0_1",
    EVENT_D1011: "derelib.bindings.v1_2_0.evt_pgcc_v1_0_3",
    EVENT_D1101: "derelib.bindings.v1_2_0.evt_balancete_v1_0_1",
    EVENT_D1106: "derelib.bindings.v1_2_0.evt_aplic_res_tec_v1_0_0",
    EVENT_D1121: "derelib.bindings.v1_2_0.evt_rel_deducoes_v0_0_1",
    EVENT_D1198: "derelib.bindings.v1_2_0.evt_reabert_mensal_v0_0_1",
    EVENT_D1199: "derelib.bindings.v1_2_0.evt_fech_mensal_v0_0_2",
}


def event_binding(event_type: str):
    """Return the generated root class for a production DeRE event type."""
    module_name = _BINDING_MODULE.get(event_type)
    if not module_name:
        raise ValueError(f"Unknown DeRE event type {event_type}")
    return import_module(module_name).DeRe
