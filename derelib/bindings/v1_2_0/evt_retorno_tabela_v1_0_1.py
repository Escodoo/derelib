from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from xsdata.models.datatype import XmlDate, XmlDateTime

from derelib.bindings.v1_2_0.xmldsig_core_schema import Signature
from derelib.mixin import DereMixin

__NAMESPACE__ = "http://www.dere.gov.br/schemas/evtRetornoTabela/v1_0_1"


class DetEventoIndAjusteAuto(Enum):
    """
    Indicador se este período sofreu corte temporal com a atribuição do campo
    {fimValidEfetiva} pelo sistema em razão da existência de outro evento com
    vigência posterior. 0 – Não; 1 – Sim (houve corte pelo sistema);.
    """

    VALUE_0 = 0
    VALUE_1 = 1


class IdeStatusCdRetorno(Enum):
    """
    Código indicativo do status do retorno.

    Valores: 0 - ERRO; 1 - SUCESSO;.
    """

    VALUE_0 = 0
    VALUE_1 = 1


class IdeStatusDescRetorno(Enum):
    """
    Descrição literal do status do retorno.
    """

    ERRO = "Erro"
    SUCESSO = "Sucesso"


@dataclass(kw_only=True)
class DeRe(DereMixin):
    """
    Envelope raiz dos eventos da DeRE.

    :ivar evtRetornoTabela: Retorno de eventos de tabela.
    :ivar signature:
    """

    class Meta:
        name = "DeRE"
        namespace = "http://www.dere.gov.br/schemas/evtRetornoTabela/v1_0_1"

    evtRetornoTabela: DeRe.EvtRetornoTabela = field(
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
    class EvtRetornoTabela:
        """
        :ivar ideContrib: Informações de identificação do contribuinte
        :ivar ideStatus: Situação do processamento do do evento
        :ivar infoRecEv: Informações de processamento dos eventos
        :ivar infoEvento: Informações do evento processado
        :ivar extratoEventos: Grupo contendo o extrato completo das vigências
            ativas para os eventos processados da respectiva tabela. Retorna a
            'Foto' atualizada após o processamento.
        :ivar id:
        """

        ideContrib: DeRe.EvtRetornoTabela.IdeContrib = field(
            metadata={
                "type": "Element",
            }
        )
        ideStatus: DeRe.EvtRetornoTabela.IdeStatus = field(
            metadata={
                "type": "Element",
            }
        )
        infoRecEv: DeRe.EvtRetornoTabela.InfoRecEv = field(
            metadata={
                "type": "Element",
            }
        )
        infoEvento: None | DeRe.EvtRetornoTabela.InfoEvento = field(
            default=None,
            metadata={
                "type": "Element",
            },
        )
        extratoEventos: None | DeRe.EvtRetornoTabela.ExtratoEventos = field(
            default=None,
            metadata={
                "type": "Element",
            },
        )
        id: str = field(
            metadata={
                "type": "Attribute",
                "max_length": 42,
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
        class IdeStatus:
            """
            :ivar cdRetorno:
            :ivar descRetorno:
            :ivar ocorrencias: Informações de ocorrências registradas
            """

            cdRetorno: IdeStatusCdRetorno = field(
                metadata={
                    "type": "Element",
                }
            )
            descRetorno: IdeStatusDescRetorno = field(
                metadata={
                    "type": "Element",
                }
            )
            ocorrencias: list[DeRe.EvtRetornoTabela.IdeStatus.Ocorrencias] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "max_occurs": 10,
                },
            )

            @dataclass(kw_only=True)
            class Ocorrencias:
                """
                :ivar codigo: Código numérico da ocorrência
                :ivar descricao: Descrição detalhada da ocorrência (mensagem de
                    erro ou aviso)
                :ivar tipo: Classificação do tipo da ocorrência. Valores: 1 -
                    Erro; 2 - Aviso;
                :ivar localizacao: Identificação do campo ou grupo onde a
                    ocorrência foi detectada
                """

                codigo: str = field(
                    metadata={
                        "type": "Element",
                        "min_length": 1,
                        "max_length": 6,
                    }
                )
                descricao: str = field(
                    metadata={
                        "type": "Element",
                        "min_length": 1,
                        "max_length": 2048,
                    }
                )
                tipo: int = field(
                    metadata={
                        "type": "Element",
                    }
                )
                localizacao: None | str = field(
                    default=None,
                    metadata={
                        "type": "Element",
                        "min_length": 1,
                        "max_length": 2048,
                    },
                )

        @dataclass(kw_only=True)
        class InfoRecEv:
            """
            :ivar nrRecibo:
            :ivar protocoloLote:
            :ivar dhRecepcao: Data e hora da recepção do evento (UTC)
            :ivar dhProcess: Data e hora do início do processamento do evento
                (UTC)
            :ivar tpEv:
            :ivar hash:
            """

            nrRecibo: None | str = field(
                default=None,
                metadata={
                    "type": "Element",
                    "max_length": 31,
                },
            )
            protocoloLote: None | str = field(
                default=None,
                metadata={
                    "type": "Element",
                    "max_length": 28,
                },
            )
            dhRecepcao: XmlDateTime = field(
                metadata={
                    "type": "Element",
                }
            )
            dhProcess: XmlDateTime = field(
                metadata={
                    "type": "Element",
                }
            )
            tpEv: str = field(
                metadata={
                    "type": "Element",
                    "max_length": 6,
                }
            )
            hash: str = field(
                metadata={
                    "type": "Element",
                    "max_length": 44,
                }
            )

        @dataclass(kw_only=True)
        class InfoEvento:
            """
            :ivar idePeriodo: Grupo de identificação do período de validade do
                evento
            """

            idePeriodo: DeRe.EvtRetornoTabela.InfoEvento.IdePeriodo = field(
                metadata={
                    "type": "Element",
                }
            )

            @dataclass(kw_only=True)
            class IdePeriodo:
                """
                :ivar iniValid:
                :ivar fimValid:
                :ivar novaValidade: Novo período de validade. Preenchido
                    exclusivamente em casos de alteração de vigência de evento já
                    existente.
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
                novaValidade: (
                    None | DeRe.EvtRetornoTabela.InfoEvento.IdePeriodo.NovaValidade
                ) = field(
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
        class ExtratoEventos:
            """
            :ivar detEvento: Detalhamento do evento constante na tabela do
                contribuinte
            :ivar detLacuna: Detalhamento de período descoberto (sem cobertura de
                evento) na linha do tempo
            """

            detEvento: list[DeRe.EvtRetornoTabela.ExtratoEventos.DetEvento] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "max_occurs": 100,
                },
            )
            detLacuna: list[DeRe.EvtRetornoTabela.ExtratoEventos.DetLacuna] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "max_occurs": 100,
                },
            )

            @dataclass(kw_only=True)
            class DetEvento:
                nrRecibo: str = field(
                    metadata={
                        "type": "Element",
                        "max_length": 31,
                    }
                )
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
                fimValidEfetiva: None | XmlDate = field(
                    default=None,
                    metadata={
                        "type": "Element",
                    },
                )
                indAjusteAuto: None | DetEventoIndAjusteAuto = field(
                    default=None,
                    metadata={
                        "type": "Element",
                    },
                )

            @dataclass(kw_only=True)
            class DetLacuna:
                iniLacuna: XmlDate = field(
                    metadata={
                        "type": "Element",
                    }
                )
                fimLacuna: None | XmlDate = field(
                    default=None,
                    metadata={
                        "type": "Element",
                    },
                )
