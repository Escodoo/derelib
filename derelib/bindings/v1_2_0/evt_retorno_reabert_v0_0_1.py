from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from derelib.bindings.v1_2_0.xmldsig_core_schema import Signature
from derelib.mixin import DereMixin

__NAMESPACE__ = "http://www.dere.gov.br/schemas/evtRetornoReabert/v0_0_1"


class IdeStatusCdRetorno(Enum):
    """
    :cvar VALUE_0: Erro
    :cvar VALUE_1: Sucesso
    """

    VALUE_0 = "0"
    VALUE_1 = "1"


class IdeStatusDescRetorno(Enum):
    ERRO = "Erro"
    SUCESSO = "Sucesso"


class OcorrenciasTipo(Enum):
    """
    :cvar VALUE_1: Erro
    :cvar VALUE_2: Aviso
    """

    VALUE_1 = "1"
    VALUE_2 = "2"


@dataclass(kw_only=True)
class DeRe(DereMixin):
    """
    Envelope raiz dos eventos da DeRE.

    :ivar evtRetornoReabert: Retorno – Reabertura de Período de Apuração.
    :ivar signature:
    """

    class Meta:
        name = "DeRE"
        namespace = "http://www.dere.gov.br/schemas/evtRetornoReabert/v0_0_1"

    evtRetornoReabert: DeRe.EvtRetornoReabert = field(
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
    class EvtRetornoReabert:
        """
        :ivar ideContrib: Informações de identificação do contribuinte.
        :ivar ideStatus: Situação do processamento do evento.
        :ivar infoRecEv: Informações de processamento dos eventos.
        :ivar infoEvento: Informações do evento processado.
        :ivar id: Identificação única do evento (campo id do evento transmitido
            pelo contribuinte, a que se refere este retorno).
        """

        ideContrib: DeRe.EvtRetornoReabert.IdeContrib = field(
            metadata={
                "type": "Element",
            }
        )
        ideStatus: DeRe.EvtRetornoReabert.IdeStatus = field(
            metadata={
                "type": "Element",
            }
        )
        infoRecEv: DeRe.EvtRetornoReabert.InfoRecEv = field(
            metadata={
                "type": "Element",
            }
        )
        infoEvento: None | DeRe.EvtRetornoReabert.InfoEvento = field(
            default=None,
            metadata={
                "type": "Element",
            },
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
        class IdeStatus:
            """
            :ivar cdRetorno: Código indicativo do status do retorno.
            :ivar descRetorno: Descrição literal do status do retorno.
            :ivar ocorrencias: Informações de ocorrências registradas.
            """

            cdRetorno: IdeStatusCdRetorno = field(
                metadata={
                    "type": "Element",
                    "white_space": "preserve",
                }
            )
            descRetorno: IdeStatusDescRetorno = field(
                metadata={
                    "type": "Element",
                    "white_space": "preserve",
                }
            )
            ocorrencias: list[DeRe.EvtRetornoReabert.IdeStatus.Ocorrencias] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "max_occurs": 10,
                },
            )

            @dataclass(kw_only=True)
            class Ocorrencias:
                """
                :ivar codigo: Código numérico da ocorrência.
                :ivar descricao: Descrição detalhada da ocorrência (mensagem de
                    erro ou aviso).
                :ivar tipo: Classificação do tipo da ocorrência.
                :ivar localizacao: Identificação do campo ou grupo onde a
                    ocorrência foi detectada.
                """

                codigo: str = field(
                    metadata={
                        "type": "Element",
                        "max_length": 6,
                        "white_space": "preserve",
                    }
                )
                descricao: str = field(
                    metadata={
                        "type": "Element",
                        "max_length": 2048,
                        "white_space": "preserve",
                        "pattern": r"([!-ÿ][ -ÿ]*[!-ÿ]|[!-ÿ])",
                    }
                )
                tipo: OcorrenciasTipo = field(
                    metadata={
                        "type": "Element",
                        "white_space": "preserve",
                    }
                )
                localizacao: None | str = field(
                    default=None,
                    metadata={
                        "type": "Element",
                        "max_length": 2048,
                        "white_space": "preserve",
                        "pattern": r"([!-ÿ][ -ÿ]*[!-ÿ]|[!-ÿ])",
                    },
                )

        @dataclass(kw_only=True)
        class InfoRecEv:
            """
            :ivar nrRecibo: Número do recibo do evento processado com sucesso.
                Preenchimento: Preenchido somente quando {cdRetorno} = [1]
                (Sucesso).
            :ivar seqEvento: Número sequencial de identificação que indica a
                versão do evento processado na base de dados. Nota: O controle
                sequencial é ininterrupto para a mesma chave de identificação.
                Como o evento D-1198 admite apenas a operação de Inclusão
                ({tpOper} = [1]), as versões subsequentes ({seqEvento} maior que
                [00]) decorrem obrigatoriamente de novas transmissões de
                Reabertura efetuadas após o período ter sido novamente encerrado
                por um evento de Fechamento Mensal (D-1199). Exemplo: 1º Envio
                (Inclusão): seqEvento = [00]; 2º Envio (Nova Inclusão): seqEvento
                = [01]; 3º Envio (Nova Inclusão): seqEvento = [02].
            :ivar protocoloLote: Número do protocolo de entrega do lote.
            :ivar dhRecepcao: Data e hora da recepção do evento (UTC). Máscara:
                AAAA-MM-DDThh:mm:ss.sssssssTZD
            :ivar dhProcess: Data e hora do início do processamento do evento
                (UTC). Máscara: AAAA-MM-DDThh:mm:ss.sssssssTZD
            :ivar tpEv: Sigla de identificação do tipo de evento. Exemplo:
                D-1198.
            :ivar hash: Hashcode do arquivo processado.
            """

            nrRecibo: None | str = field(
                default=None,
                metadata={
                    "type": "Element",
                    "length": 31,
                    "white_space": "preserve",
                    "pattern": r"[0-9]{4}-20[0-9]{2}(0[1-9]|1[0-2])-[0-9A-Z]{19}",
                },
            )
            seqEvento: None | str = field(
                default=None,
                metadata={
                    "type": "Element",
                    "length": 2,
                    "white_space": "preserve",
                    "pattern": r"[0-9]{2}",
                },
            )
            protocoloLote: None | str = field(
                default=None,
                metadata={
                    "type": "Element",
                    "length": 28,
                    "white_space": "preserve",
                    "pattern": r"[12]\.20[0-9]{2}(0[1-9]|1[0-2])\.[0-9]{19}",
                },
            )
            dhRecepcao: str = field(
                metadata={
                    "type": "Element",
                    "min_length": 25,
                    "max_length": 33,
                    "white_space": "preserve",
                    "pattern": r"(((20(([02468][048])|([13579][26]))-02-29))|(20[0-9][0-9])-((((0[1-9])|(1[0-2]))-((0[1-9])|(1\d)|(2[0-8])))|((((0[13578])|(1[02]))-31)|(((0[1,3-9])|(1[0-2]))-(29|30)))))T(20|21|22|23|[0-1]\d):[0-5]\d:[0-5]\d\.[0-9]{7}([\-\+](0[0-9]|10|11):00|([\+](12):00))",
                }
            )
            dhProcess: str = field(
                metadata={
                    "type": "Element",
                    "min_length": 25,
                    "max_length": 33,
                    "white_space": "preserve",
                    "pattern": r"(((20(([02468][048])|([13579][26]))-02-29))|(20[0-9][0-9])-((((0[1-9])|(1[0-2]))-((0[1-9])|(1\d)|(2[0-8])))|((((0[13578])|(1[02]))-31)|(((0[1,3-9])|(1[0-2]))-(29|30)))))T(20|21|22|23|[0-1]\d):[0-5]\d:[0-5]\d\.[0-9]{7}([\-\+](0[0-9]|10|11):00|([\+](12):00))",
                }
            )
            tpEv: str = field(
                metadata={
                    "type": "Element",
                    "length": 6,
                    "white_space": "preserve",
                    "pattern": r"D-[0-9]{4}",
                }
            )
            hash: str = field(
                metadata={
                    "type": "Element",
                    "length": 44,
                    "white_space": "preserve",
                    "pattern": r"[0-9A-Za-z+/]{43}=",
                }
            )

        @dataclass(kw_only=True)
        class InfoEvento:
            """
            :ivar idePeriodo: Grupo de identificação do período de referência das
                informações do evento.
            """

            idePeriodo: DeRe.EvtRetornoReabert.InfoEvento.IdePeriodo = field(
                metadata={
                    "type": "Element",
                }
            )

            @dataclass(kw_only=True)
            class IdePeriodo:
                """
                :ivar perApur: Período de apuração, sendo o ano e mês da
                    competência da declaração. Máscara: AAAA-MM Cálculo: Valor do
                    campo {perApur} informado no evento de origem.
                """

                perApur: str = field(
                    metadata={
                        "type": "Element",
                        "length": 7,
                        "white_space": "preserve",
                        "pattern": r"20[0-9]{2}-(0[1-9]|1[0-2])",
                    }
                )
