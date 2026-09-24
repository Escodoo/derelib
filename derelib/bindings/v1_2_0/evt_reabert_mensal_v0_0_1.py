from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from derelib.bindings.v1_2_0.xmldsig_core_schema import Signature
from derelib.mixin import DereMixin

__NAMESPACE__ = "http://www.dere.gov.br/schemas/evtReabertMensal/v0_0_1"


class IdeEventoAplicEmi(Enum):
    """
    :cvar VALUE_1: Emissão com aplicativo da empresa
    :cvar VALUE_2: Aplicativo governamental
    """

    VALUE_1 = "1"
    VALUE_2 = "2"


class IdeEventoTpAmb(Enum):
    """
    :cvar VALUE_1: Produção
    :cvar VALUE_2: Produção restrita
    """

    VALUE_1 = "1"
    VALUE_2 = "2"


class IdeEventoTpOper(Enum):
    """
    :cvar VALUE_1: Inclusão
    """

    VALUE_1 = "1"


@dataclass(kw_only=True)
class DeRe(DereMixin):
    """
    Envelope raiz dos eventos da DeRE.

    :ivar evtReabertMensal: Evento de Reabertura Mensal.
    :ivar signature:
    """

    class Meta:
        name = "DeRE"
        namespace = "http://www.dere.gov.br/schemas/evtReabertMensal/v0_0_1"

    evtReabertMensal: DeRe.EvtReabertMensal = field(
        metadata={
            "type": "Element",
        }
    )
    signature: None | Signature = field(
        default=None,
        metadata={
            "name": "Signature",
            "type": "Element",
            "namespace": "http://www.w3.org/2000/09/xmldsig#",
        },
    )

    @dataclass(kw_only=True)
    class EvtReabertMensal:
        """
        :ivar ideEvento: Informações de identificação do evento.
        :ivar ideContrib: Informações de identificação do contribuinte.
        :ivar idePeriodo: Período de referência das informações do evento.
        :ivar infoReabertura: Informações do evento de reabertura mensal.
        :ivar id: Identificador que representa unicamente o evento.
        """

        ideEvento: DeRe.EvtReabertMensal.IdeEvento = field(
            metadata={
                "type": "Element",
            }
        )
        ideContrib: DeRe.EvtReabertMensal.IdeContrib = field(
            metadata={
                "type": "Element",
            }
        )
        idePeriodo: DeRe.EvtReabertMensal.IdePeriodo = field(
            metadata={
                "type": "Element",
            }
        )
        infoReabertura: DeRe.EvtReabertMensal.InfoReabertura = field(
            metadata={
                "type": "Element",
            }
        )
        id: str = field(
            metadata={
                "type": "Attribute",
                "length": 42,
                "white_space": "preserve",
                "pattern": r"DeRE[0-9]{4}[1-2][0-9A-Z]{14}[0-9]{19}",
            }
        )

        @dataclass(kw_only=True)
        class IdeEvento:
            """
            :ivar tpOper: Tipo de operação do evento. Nota: O evento de
                Reabertura de Período de Apuração (D-1198) aceita exclusivamente
                a operação de Inclusão.
            :ivar tpAmb: Identificação do ambiente para o qual os dados estão
                sendo transmitidos.
            :ivar aplicEmi: Identificação do aplicativo emissor do evento.
            :ivar verAplic: Versão do aplicativo emissor do evento.
            """

            tpOper: IdeEventoTpOper = field(
                metadata={
                    "type": "Element",
                    "white_space": "preserve",
                }
            )
            tpAmb: IdeEventoTpAmb = field(
                metadata={
                    "type": "Element",
                    "white_space": "preserve",
                }
            )
            aplicEmi: IdeEventoAplicEmi = field(
                metadata={
                    "type": "Element",
                    "white_space": "preserve",
                }
            )
            verAplic: str = field(
                metadata={
                    "type": "Element",
                    "max_length": 20,
                    "white_space": "preserve",
                    "pattern": r"([!-ÿ][ -ÿ]*[!-ÿ]|[!-ÿ])",
                }
            )

        @dataclass(kw_only=True)
        class IdeContrib:
            """
            :ivar nrInsc: Número de inscrição do contribuinte (CNPJ raiz).
                Validação: Deve ser um CNPJ raiz válido de 8 posições.
            """

            nrInsc: str = field(
                metadata={
                    "type": "Element",
                    "length": 8,
                    "white_space": "preserve",
                    "pattern": r"[0-9A-Z]{8}",
                }
            )

        @dataclass(kw_only=True)
        class IdePeriodo:
            """
            :ivar perApur: Informar o período de apuração a que se deseja
                realizar a reabertura, sendo o ano e mês da competência da
                declaração. Máscara: AAAA-MM Validação: Deve existir um evento
                D-1199 ativo para o {perApur} correspondente.
            """

            perApur: str = field(
                metadata={
                    "type": "Element",
                    "length": 7,
                    "white_space": "preserve",
                    "pattern": r"20[0-9]{2}-(0[1-9]|1[0-2])",
                }
            )

        @dataclass(kw_only=True)
        class InfoReabertura:
            """
            :ivar nrReciboReab: Número do recibo do evento de Fechamento Mensal
                (D-1199) relativo ao período de apuração a que se deseja realizar
                a reabertura. Validação: Validar a consistência do recibo de
                fechamento referenciado no evento de reabertura D-1198: 1. O
                sistema deve verificar se o prefixo (caracteres 1 a 4) do campo
                {nrReciboReab} informado corresponde a 1199 (Evento de Fechamento
                Mensal). Caso seja diferente de 1199, o evento deve ser
                rejeitado; 2. O recibo informado no campo {nrReciboReab} deve
                existir e ser o último vigente na base de dados da DeRE associado
                ao CNPJ declarante ({nrInsc}) com o status "Ativo" para aquele
                {perApur}; 3. O período de apuração {perApur} informado no grupo
                {idePeriodo} deve ser idêntico ao período apontado nos caracteres
                6 a 11 do recibo informado ({nrReciboReab}).
            """

            nrReciboReab: str = field(
                metadata={
                    "type": "Element",
                    "length": 31,
                    "white_space": "preserve",
                    "pattern": r"[0-9]{4}-20[0-9]{2}(0[1-9]|1[0-2])-[0-9A-Z]{19}",
                }
            )
