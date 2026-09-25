"""Official DeRE event identifiers and schema mapping."""

from __future__ import annotations

from importlib import import_module
from typing import Any

EVENT_D1001 = "D-1001"
EVENT_D1011 = "D-1011"
EVENT_D1101 = "D-1101"
EVENT_D1106 = "D-1106"
EVENT_D1121 = "D-1121"
EVENT_D1198 = "D-1198"
EVENT_D1199 = "D-1199"
RETURN_D9001 = "D-9001"
RETURN_D9101 = "D-9101"
RETURN_D9106 = "D-9106"
RETURN_D9112 = "D-9112"
RETURN_D9121 = "D-9121"
RETURN_D9198 = "D-9198"
RETURN_D9199 = "D-9199"
RETURN_D9209 = "D-9209"
RETURN_LOTE = "retornoLoteDere"

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
LOTE_RETURN_SCHEMA = "retornoLoteDere-v1_0_1.xsd"
LOTE_RETURN_NAMESPACE = "http://www.dere.gov.br/schemas/retornoLoteDere/v1_0_1"
DS_NS = "http://www.w3.org/2000/09/xmldsig#"

RETURN_SCHEMA = {
    RETURN_LOTE: LOTE_RETURN_SCHEMA,
    RETURN_D9001: "evtRetornoTabela-v1_0_1.xsd",
    RETURN_D9101: "evtRetornoBalan-v1_0_0.xsd",
    RETURN_D9106: "evtRetornoAplicFin-v1_0_0.xsd",
    RETURN_D9112: "evtRetornoRDed-v0_0_1.xsd",
    RETURN_D9121: "evtRetornoTitPub-v0_0_2.xsd",
    RETURN_D9198: "evtRetornoReabert-v0_0_1.xsd",
    RETURN_D9199: "evtRetornoMensal-v0_0_2.xsd",
    RETURN_D9209: "evtRetornoTransac-v0_0_1.xsd",
}

RETURN_NAMESPACE = {
    RETURN_LOTE: LOTE_RETURN_NAMESPACE,
    RETURN_D9001: "http://www.dere.gov.br/schemas/evtRetornoTabela/v1_0_1",
    RETURN_D9101: "http://www.dere.gov.br/schemas/evtRetornoBalan/v1_0_0",
    RETURN_D9106: "http://www.dere.gov.br/schemas/evtRetornoAplicFin/v1_0_0",
    RETURN_D9112: "http://www.dere.gov.br/schemas/evtRetornoRDed/v0_0_1",
    RETURN_D9121: "http://www.dere.gov.br/schemas/evtRetornoTitPub/v0_0_2",
    RETURN_D9198: "http://www.dere.gov.br/schemas/evtRetornoReabert/v0_0_1",
    RETURN_D9199: "http://www.dere.gov.br/schemas/evtRetornoMensal/v0_0_2",
    RETURN_D9209: "http://www.dere.gov.br/schemas/evtRetornoTransac/v0_0_1",
}

RETURN_SCHEMA_BY_NAMESPACE = {
    namespace: RETURN_SCHEMA[event_type]
    for event_type, namespace in RETURN_NAMESPACE.items()
}

_BINDING_MODULE = {
    EVENT_D1001: "derelib.bindings.v1_2_0.evt_info_contrib_v1_0_1",
    EVENT_D1011: "derelib.bindings.v1_2_0.evt_pgcc_v1_0_3",
    EVENT_D1101: "derelib.bindings.v1_2_0.evt_balancete_v1_0_1",
    EVENT_D1106: "derelib.bindings.v1_2_0.evt_aplic_res_tec_v1_0_0",
    EVENT_D1121: "derelib.bindings.v1_2_0.evt_rel_deducoes_v0_0_1",
    EVENT_D1198: "derelib.bindings.v1_2_0.evt_reabert_mensal_v0_0_1",
    EVENT_D1199: "derelib.bindings.v1_2_0.evt_fech_mensal_v0_0_2",
}


_RETURN_BINDING_MODULE = {
    RETURN_LOTE: "derelib.bindings.v1_2_0.retorno_lote_dere_v1_0_1",
    RETURN_D9001: "derelib.bindings.v1_2_0.evt_retorno_tabela_v1_0_1",
    RETURN_D9101: "derelib.bindings.v1_2_0.evt_retorno_balan_v1_0_0",
    RETURN_D9106: "derelib.bindings.v1_2_0.evt_retorno_aplic_fin_v1_0_0",
    RETURN_D9112: "derelib.bindings.v1_2_0.evt_retorno_rded_v0_0_1",
    RETURN_D9121: "derelib.bindings.v1_2_0.evt_retorno_tit_pub_v0_0_2",
    RETURN_D9198: "derelib.bindings.v1_2_0.evt_retorno_reabert_v0_0_1",
    RETURN_D9199: "derelib.bindings.v1_2_0.evt_retorno_mensal_v0_0_2",
    RETURN_D9209: "derelib.bindings.v1_2_0.evt_retorno_transac_v0_0_1",
}


def _binding(event_type: str, modules: dict[str, str], kind: str) -> type[Any]:
    module_name = modules.get(event_type)
    if not module_name:
        raise ValueError(f"Unknown DeRE {kind} type {event_type}")
    return import_module(module_name).DeRe


def event_binding(event_type: str) -> type[Any]:
    """Return the generated root class for a production DeRE event type."""
    return _binding(event_type, _BINDING_MODULE, "event")


def return_binding(event_type: str) -> type[Any]:
    """Return the generated root class for a D-9xxx return type."""
    return _binding(event_type, _RETURN_BINDING_MODULE, "return")
