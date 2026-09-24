from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from xsdata.models.datatype import XmlDate

from derelib.bindings.v1_2_0.xmldsig_core_schema import Signature
from derelib.mixin import DereMixin

__NAMESPACE__ = "http://www.dere.gov.br/schemas/evtInfoContrib/v1_0_1"


class IdeEventoAplicEmi(Enum):
    """
    Identificação do aplicativo emissor do evento.

    :cvar VALUE_1: Emissão com aplicativo da empresa
    :cvar VALUE_2: Aplicativo Governamental
    """

    VALUE_1 = 1
    VALUE_2 = 2


class IdeEventoMotExcl(Enum):
    """
    Motivo da Exclusão.

    Código do motivo que justifica a exclusão do evento.

    :cvar VALUE_1: Determinação judicial ou administrativa
    :cvar VALUE_2: Envio indevido (fato inexistente)
    :cvar VALUE_3: Erro na identificação (CNPJ/período incorretos)
    :cvar VALUE_9: Outro
    """

    VALUE_1 = 1
    VALUE_2 = 2
    VALUE_3 = 3
    VALUE_9 = 9


class IdeEventoTpAmb(Enum):
    """
    Identificação do ambiente para o qual os dados estão sendo transmitidos.

    :cvar VALUE_1: Produção
    :cvar VALUE_2: Produção Restrita
    """

    VALUE_1 = 1
    VALUE_2 = 2


class IdeEventoTpOper(Enum):
    """
    Tipo de operação do evento.

    :cvar VALUE_1: Inclusão
    :cvar VALUE_2: Alteração
    :cvar VALUE_3: Exclusão
    """

    VALUE_1 = 1
    VALUE_2 = 2
    VALUE_3 = 3


class InfoContribIndNatTrib(Enum):
    """
    Indicador da natureza tributária do declarante (para casos de imunidades ou não
    incidências subjetivas).

    :cvar VALUE_0: Tributação regular
    :cvar VALUE_1: Imunidade ou não incidência
    """

    VALUE_0 = 0
    VALUE_1 = 1


class InfoContribRegTribPrinc(Enum):
    """
    Regime de tributação ao qual o contribuinte está sujeito em sua atividade
    preponderante.

    :cvar VALUE_1: Regime Específico de Serviços Financeiros
    :cvar VALUE_2: Regime Específico de Plano de Assistência à Saúde
    :cvar VALUE_3: Regime Específico de Concursos de Prognósticos
    :cvar VALUE_9: Outros Regimes de Tributação
    """

    VALUE_1 = 1
    VALUE_2 = 2
    VALUE_3 = 3
    VALUE_9 = 9


class InfoContribRegTribSecund(Enum):
    """
    Regime de tributação ao qual o contribuinte está sujeito em sua atividade
    secundária.

    :cvar VALUE_1: Regime Específico de Serviços Financeiros
    :cvar VALUE_2: Regime Específico de Plano de Assistência à Saúde
    :cvar VALUE_3: Regime Específico de Concursos de Prognósticos
    """

    VALUE_1 = 1
    VALUE_2 = 2
    VALUE_3 = 3


@dataclass(kw_only=True)
class DeRe(DereMixin):
    """
    Envelope raiz dos eventos da DeRE.

    :ivar evtInfoContrib: Evento Informações do Contribuinte
    :ivar signature:
    """

    class Meta:
        name = "DeRE"
        namespace = "http://www.dere.gov.br/schemas/evtInfoContrib/v1_0_1"

    evtInfoContrib: DeRe.EvtInfoContrib = field(
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
    class EvtInfoContrib:
        """
        :ivar ideEvento: Informações de Identificação do Evento
        :ivar ideContrib: Informações de identificação do contribuinte
        :ivar idePeriodo: Período de validade
        :ivar infoContrib: Informações do contribuinte
        :ivar id:
        """

        ideEvento: DeRe.EvtInfoContrib.IdeEvento = field(
            metadata={
                "type": "Element",
            }
        )
        ideContrib: DeRe.EvtInfoContrib.IdeContrib = field(
            metadata={
                "type": "Element",
            }
        )
        idePeriodo: DeRe.EvtInfoContrib.IdePeriodo = field(
            metadata={
                "type": "Element",
            }
        )
        infoContrib: None | DeRe.EvtInfoContrib.InfoContrib = field(
            default=None,
            metadata={
                "type": "Element",
            },
        )
        id: str = field(
            metadata={
                "type": "Attribute",
                "pattern": r"[0-9A-Za-z]{42}",
            }
        )

        @dataclass(kw_only=True)
        class IdeEvento:
            tpOper: IdeEventoTpOper = field(
                metadata={
                    "type": "Element",
                    "pattern": r"\d{1}",
                }
            )
            motExcl: None | IdeEventoMotExcl = field(
                default=None,
                metadata={
                    "type": "Element",
                    "min_inclusive": "1",
                    "max_inclusive": "9",
                    "pattern": r"\d{1}",
                },
            )
            nrProc: None | str = field(
                default=None,
                metadata={
                    "type": "Element",
                    "min_length": 1,
                    "max_length": 21,
                },
            )
            tpAmb: IdeEventoTpAmb = field(
                metadata={
                    "type": "Element",
                    "pattern": r"\d{1}",
                }
            )
            aplicEmi: IdeEventoAplicEmi = field(
                metadata={
                    "type": "Element",
                    "pattern": r"\d{1}",
                }
            )
            verAplic: str = field(
                metadata={
                    "type": "Element",
                    "min_length": 1,
                    "max_length": 20,
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
        class IdePeriodo:
            """
            :ivar iniValid:
            :ivar fimValid:
            :ivar novaValidade: Novo período de validade. Usado exclusivamente
                quando a vigência do evento precisa ser alterada para um valor
                diferente.
            """

            iniValid: XmlDate = field(
                metadata={
                    "type": "Element",
                }
            )
            fimValid: None | XmlDate = field(
                default=None,
                metadata={
                    "type": "Element",
                },
            )
            novaValidade: None | DeRe.EvtInfoContrib.IdePeriodo.NovaValidade = field(
                default=None,
                metadata={
                    "type": "Element",
                },
            )

            @dataclass(kw_only=True)
            class NovaValidade:
                iniValid: XmlDate = field(
                    metadata={
                        "type": "Element",
                    }
                )
                fimValid: None | XmlDate = field(
                    default=None,
                    metadata={
                        "type": "Element",
                    },
                )

        @dataclass(kw_only=True)
        class InfoContrib:
            regTribPrinc: InfoContribRegTribPrinc = field(
                metadata={
                    "type": "Element",
                    "pattern": r"\d{1}",
                }
            )
            regTribSecund: list[InfoContribRegTribSecund] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "max_occurs": 3,
                    "pattern": r"\d{1}",
                },
            )
            indNatTrib: InfoContribIndNatTrib = field(
                metadata={
                    "type": "Element",
                    "pattern": r"\d{1}",
                }
            )
            servFinanc: None | DeRe.EvtInfoContrib.InfoContrib.ServFinanc = field(
                default=None,
                metadata={
                    "type": "Element",
                },
            )
            plAssistSaude: None | DeRe.EvtInfoContrib.InfoContrib.PlAssistSaude = field(
                default=None,
                metadata={
                    "type": "Element",
                },
            )
            prognosticos: None | DeRe.EvtInfoContrib.InfoContrib.Prognosticos = field(
                default=None,
                metadata={
                    "type": "Element",
                },
            )

            @dataclass(kw_only=True)
            class ServFinanc:
                """
                Informações de serviços financeiros.

                Exclusivo para contribuintes deste setor.
                """

                tpAtividades: DeRe.EvtInfoContrib.InfoContrib.ServFinanc.TpAtividades = field(
                    metadata={
                        "type": "Element",
                    }
                )

                @dataclass(kw_only=True)
                class TpAtividades:
                    """
                    Lista de atividades realizadas pelo contribuinte.
                    """

                    tpAtividade: list[str] = field(
                        default_factory=list,
                        metadata={
                            "type": "Element",
                            "min_occurs": 1,
                            "max_occurs": 99,
                            "pattern": r"[0-9]{2}[A-Z]",
                        },
                    )

            @dataclass(kw_only=True)
            class PlAssistSaude:
                """
                Informações de planos de assistência à saúde.

                Exclusivo para contribuintes deste setor.
                """

                tpAtividades: DeRe.EvtInfoContrib.InfoContrib.PlAssistSaude.TpAtividades = field(
                    metadata={
                        "type": "Element",
                    }
                )

                @dataclass(kw_only=True)
                class TpAtividades:
                    """
                    Lista de atividades realizadas pelo contribuinte.
                    """

                    tpAtividade: list[str] = field(
                        default_factory=list,
                        metadata={
                            "type": "Element",
                            "min_occurs": 1,
                            "max_occurs": 99,
                            "pattern": r"[0-9]{2}[A-Z]",
                        },
                    )

            @dataclass(kw_only=True)
            class Prognosticos:
                """
                Informações de concursos de prognósticos.

                Exclusivo para contribuintes deste setor.
                """

                tpAtividades: DeRe.EvtInfoContrib.InfoContrib.Prognosticos.TpAtividades = field(
                    metadata={
                        "type": "Element",
                    }
                )
                UFsCredenc: (
                    None | DeRe.EvtInfoContrib.InfoContrib.Prognosticos.UfsCredenc
                ) = field(
                    default=None,
                    metadata={
                        "type": "Element",
                    },
                )

                @dataclass(kw_only=True)
                class TpAtividades:
                    """
                    Lista de atividades realizadas pelo contribuinte.
                    """

                    tpAtividade: list[str] = field(
                        default_factory=list,
                        metadata={
                            "type": "Element",
                            "min_occurs": 1,
                            "max_occurs": 99,
                            "pattern": r"[0-9]{2}[A-Z]",
                        },
                    )

                @dataclass(kw_only=True)
                class UfsCredenc:
                    """
                    Listagem das Unidades da Federação (UF) nas quais o contribuinte
                    possui credenciamento para operar.
                    """

                    UFCredenc: list[str] = field(
                        default_factory=list,
                        metadata={
                            "type": "Element",
                            "min_occurs": 1,
                            "max_occurs": 30,
                            "min_inclusive": "1",
                            "max_inclusive": "99",
                            "pattern": r"\d{2}",
                        },
                    )
