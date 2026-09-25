"""Shared helpers mixed into generated DeRE root dataclasses."""

from __future__ import annotations

import warnings
from pathlib import Path
from typing import Any

from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.parsers.config import ParserConfig
from xsdata.formats.dataclass.serializers import XmlSerializer
from xsdata.formats.dataclass.serializers.config import SerializerConfig


class DereMixin:
    """Parse, serialize and validate a generated DeRE root class."""

    schema_path: str | None = None

    @classmethod
    def from_xml(cls, xml: str, config: ParserConfig | None = None) -> Any:
        """Parse XML and return an instance of the class."""
        parser = XmlParser() if config is None else XmlParser(config=config)
        return parser.from_string(xml, cls)

    @classmethod
    def from_path(cls, path: str | Path) -> Any:
        """Parse XML at the given path and return an instance of the class."""
        return cls.from_xml(Path(path).read_text(encoding="utf-8"))

    @classmethod
    def schema_validation(cls, xml: str, schema_path: str | None = None) -> list[str]:
        """Validate XML against the XSD and return error messages."""
        from derelib.validation import validate_against_schema

        return validate_against_schema(xml, schema_path or cls._resolve_schema_path())

    @classmethod
    def _resolve_schema_path(cls) -> str:
        if cls.schema_path:
            return cls.schema_path
        module = cls.__module__.rsplit(".", maxsplit=1)[-1]
        filename = _SCHEMA_BY_MODULE.get(module)
        if not filename:
            raise ValueError(f"No XSD mapped for binding module {module}")
        return str(Path(__file__).resolve().parent / "schemas" / "v1_2_0" / filename)

    def to_xml(self, indent: str | None = "  ") -> str:
        """Serialize the binding as XML.

        Re-serializing a payload that already carries ``ds:Signature``
        changes the canonical form and invalidates the digest. Signed XML
        must be treated as opaque; ``build_lote`` inserts it as-is.
        """
        if getattr(self, "signature", None) is not None:
            warnings.warn(
                "Serializing a signed DeRE binding invalidates the XML-DSig "
                "digest. Treat signed XML as opaque and pass it to "
                "build_lote as-is.",
                UserWarning,
                stacklevel=2,
            )
        ns_map = {None: self.Meta.namespace} if hasattr(self, "Meta") else None
        serializer = XmlSerializer(config=SerializerConfig(indent=indent))
        return serializer.render(obj=self, ns_map=ns_map)

    def validate_xml(self, schema_path: str | None = None) -> list[str]:
        """Serialize the binding and validate it against the XSD."""
        return self.schema_validation(self.to_xml(), schema_path)

    def sign_xml(self, key: bytes | str, cert_pem: bytes | str, reference: str) -> str:
        """Serialize and sign the binding (requires derelib[sign])."""
        from derelib.signing import sign_event

        return sign_event(self.to_xml(indent=None), key, cert_pem, reference)


_SCHEMA_BY_MODULE = {
    "evt_info_contrib_v1_0_1": "evtInfoContrib-v1_0_1.xsd",
    "evt_pgcc_v1_0_3": "evtPGCC-v1_0_3.xsd",
    "evt_balancete_v1_0_1": "evtBalancete-v1_0_1.xsd",
    "evt_aplic_res_tec_v1_0_0": "evtAplicResTec-v1_0_0.xsd",
    "evt_rel_deducoes_v0_0_1": "evtRelDeducoes-v0_0_1.xsd",
    "evt_reabert_mensal_v0_0_1": "evtReabertMensal-v0_0_1.xsd",
    "evt_fech_mensal_v0_0_2": "evtFechMensal-v0_0_2.xsd",
    "envio_lote_dere_v1_0_1": "envioLoteDere-v1_0_1.xsd",
    "retorno_lote_dere_v1_0_1": "retornoLoteDere-v1_0_1.xsd",
    "evt_retorno_tabela_v1_0_1": "evtRetornoTabela-v1_0_1.xsd",
    "evt_retorno_mensal_v0_0_2": "evtRetornoMensal-v0_0_2.xsd",
    "evt_retorno_reabert_v0_0_1": "evtRetornoReabert-v0_0_1.xsd",
    "evt_retorno_aplic_fin_v1_0_0": "evtRetornoAplicFin-v1_0_0.xsd",
    "evt_retorno_rded_v0_0_1": "evtRetornoRDed-v0_0_1.xsd",
    "evt_retorno_balan_v1_0_0": "evtRetornoBalan-v1_0_0.xsd",
    "evt_retorno_tit_pub_v0_0_2": "evtRetornoTitPub-v0_0_2.xsd",
    "evt_retorno_transac_v0_0_1": "evtRetornoTransac-v0_0_1.xsd",
}
