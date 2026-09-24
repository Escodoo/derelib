from __future__ import annotations

from dataclasses import dataclass, field

from derelib.mixin import DereMixin

__NAMESPACE__ = "http://www.dere.gov.br/schemas/envioLoteDere/v1_0_1"


@dataclass(kw_only=True)
class TeventoDere:
    """
    Define os dados de um evento da DERE.

    :ivar any_element: Contem o xml do evento
    :ivar id: Contem a chave de acesso do evento
    """

    class Meta:
        name = "TEventoDere"

    any_element: None | object = field(
        default=None,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "process_contents": "skip",
        },
    )
    id: str = field(
        metadata={
            "type": "Attribute",
        }
    )


@dataclass(kw_only=True)
class DeRe(DereMixin):
    """
    :ivar loteEventos: Lote de eventos da DERE
    """

    class Meta:
        name = "DeRE"
        namespace = "http://www.dere.gov.br/schemas/envioLoteDere/v1_0_1"

    loteEventos: DeRe.LoteEventos = field(
        metadata={
            "type": "Element",
        }
    )

    @dataclass(kw_only=True)
    class LoteEventos:
        """
        :ivar ideContrib: Identificacao do Contribuinte
        :ivar eventos: Relacao de eventos que compoe o lote
        """

        ideContrib: DeRe.LoteEventos.IdeContrib = field(
            metadata={
                "type": "Element",
            }
        )
        eventos: DeRe.LoteEventos.Eventos = field(
            metadata={
                "type": "Element",
            }
        )

        @dataclass(kw_only=True)
        class IdeContrib:
            nrInsc: str = field(
                metadata={
                    "type": "Element",
                    "max_length": 8,
                    "pattern": r"[0-9A-Z]{8}",
                }
            )

        @dataclass(kw_only=True)
        class Eventos:
            evento: list[TeventoDere] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "min_occurs": 1,
                    "max_occurs": 50,
                },
            )
