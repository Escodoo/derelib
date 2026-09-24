from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from derelib.bindings.v1_2_0.xmldsig_core_schema import Signature
from derelib.mixin import DereMixin

__NAMESPACE__ = "http://www.dere.gov.br/schemas/evtRetornoBalan/v1_0_0"


class GTotalCodTribIndTribIss(Enum):
    """
    :cvar VALUE_0: Não sujeita ao ISS
    :cvar VALUE_1: Sujeita ao ISS
    """

    VALUE_0 = "0"
    VALUE_1 = "1"


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

    :ivar evtRetornoBalan: Retorno do evento Balancete Mensal.
    :ivar signature:
    """

    class Meta:
        name = "DeRE"
        namespace = "http://www.dere.gov.br/schemas/evtRetornoBalan/v1_0_0"

    evtRetornoBalan: DeRe.EvtRetornoBalan = field(
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
    class EvtRetornoBalan:
        """
        :ivar ideContrib: Informações de identificação do contribuinte.
        :ivar ideStatus: Situação do processamento do evento.
        :ivar infoRecEv: Informações de processamento dos eventos.
        :ivar infoEvento: Informações do evento processado.
        :ivar id: Identificação única do evento (campo id do evento transmitido
            pelo contribuinte, a que se refere este retorno).
        """

        ideContrib: DeRe.EvtRetornoBalan.IdeContrib = field(
            metadata={
                "type": "Element",
            }
        )
        ideStatus: DeRe.EvtRetornoBalan.IdeStatus = field(
            metadata={
                "type": "Element",
            }
        )
        infoRecEv: DeRe.EvtRetornoBalan.InfoRecEv = field(
            metadata={
                "type": "Element",
            }
        )
        infoEvento: None | DeRe.EvtRetornoBalan.InfoEvento = field(
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
                "pattern": r"DeRE[0-9]{4}[1-2][A-Z0-9]{14}[0-9]{19}",
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
            ocorrencias: list[DeRe.EvtRetornoBalan.IdeStatus.Ocorrencias] = field(
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
                    erro ou aviso).
                :ivar tipo: Classificação do tipo da ocorrência.
                :ivar localizacao: Identificação do campo ou grupo onde a
                    ocorrência foi detectada.
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
                Validação: Preenchido somente quando {cdRetorno} = [1] (Sucesso).
            :ivar seqEvento: Número sequencial de identificação que indica a
                versão do evento processado na base de dados. Nota: O controle
                sequencial é ininterrupto para a mesma chave de identificação. A
                exclusão de um evento não zera a contagem para futuras
                reinclusões. Exemplo: 1º Envio (Inclusão): seqEvento = [00]; 2º
                Envio (Alteração): seqEvento = [01]; 3º Envio (Exclusão):
                seqEvento = [02]; 4º Envio (Nova Inclusão): seqEvento = [03].
            :ivar protocoloLote: Número do protocolo de entrega do lote.
            :ivar dhRecepcao: Data e hora da recepção do evento (UTC). Máscara:
                AAAA-MM-DDThh:mm:ss.sssssssTZD
            :ivar dhProcess: Data e hora do início do processamento do evento
                (UTC). Máscara: AAAA-MM-DDThh:mm:ss.sssssssTZD
            :ivar tpEv: Sigla de identificação do tipo de evento. Exemplo:
                D-1101.
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
                    "pattern": r"[A-Za-z0-9+/]{43}=",
                }
            )

        @dataclass(kw_only=True)
        class InfoEvento:
            """
            :ivar idePeriodo: Grupo de identificação do período de referência das
                informações do evento.
            :ivar infoAdic: Grupo destinado à prestação de informações
                complementares relativas ao evento processado.
            :ivar infoTotBalan: Informações de totalizadores do evento D-1101 -
                Balancete Mensal {evtBalancete}.
            """

            idePeriodo: DeRe.EvtRetornoBalan.InfoEvento.IdePeriodo = field(
                metadata={
                    "type": "Element",
                }
            )
            infoAdic: None | DeRe.EvtRetornoBalan.InfoEvento.InfoAdic = field(
                default=None,
                metadata={
                    "type": "Element",
                },
            )
            infoTotBalan: None | DeRe.EvtRetornoBalan.InfoEvento.InfoTotBalan = field(
                default=None,
                metadata={
                    "type": "Element",
                },
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

            @dataclass(kw_only=True)
            class InfoAdic:
                """
                :ivar nrReciboPGCC: Número do recibo do evento D-1011 (Plano
                    Geral de Contas Comentado) utilizado para o mapeamento das
                    contas e totalização deste processamento.
                """

                nrReciboPGCC: str = field(
                    metadata={
                        "type": "Element",
                        "length": 31,
                        "white_space": "preserve",
                        "pattern": r"[0-9]{4}-20[0-9]{2}(0[1-9]|1[0-2])-[0-9A-Z]{19}",
                    }
                )

            @dataclass(kw_only=True)
            class InfoTotBalan:
                """
                :ivar gTotalCodTrib: Totalização de informações por Código de
                    Tributação.
                """

                gTotalCodTrib: list[
                    DeRe.EvtRetornoBalan.InfoEvento.InfoTotBalan.GTotalCodTrib
                ] = field(
                    default_factory=list,
                    metadata={
                        "type": "Element",
                        "max_occurs": 999,
                    },
                )

                @dataclass(kw_only=True)
                class GTotalCodTrib:
                    """
                    :ivar codTrib: Código de tributação para fins de IBS, CBS e
                        IS. Preenchimento: Listagem de valores únicos de
                        {codTrib} informados no evento D-1101 ({evtBalancete}).
                    :ivar indTribISS: Indicador de sujeição ou vinculação ao
                        ISSQN. Preenchimento: Se não informado, atribuir [0].
                    :ivar vApurTot: Somatório de todas as ocorrências de {vApur}
                        do evento D-1101 ({evtBalancete}) para o {codTrib} e
                        {indTribISS} informados. Cálculo: SOMA({vApur.codTrib} =
                        {codTrib})
                    :ivar vTotSaldoInic: Somatório de todas as ocorrências de
                        {vSaldoInic} do evento D-1101 ({evtBalancete}) para o
                        {codTrib} informado. Preenchimento: Campo retornado
                        apenas se {codTrib} = [220110001; 220210001; 220310001].
                        Cálculo: SOMA({vSaldoInic.codTrib} = [220110001;
                        220210001; 220310001])
                    :ivar vTotSaldoFinal: Somatório de todas as ocorrências de
                        {vSaldoFinal} do evento D-1101 ({evtBalancete}) para o
                        {codTrib} informado. Preenchimento: Campo retornado
                        apenas se {codTrib} = [220110001; 220210001; 220310001].
                        Cálculo: SOMA({vSaldoFinal.codTrib} = [220110001;
                        220210001; 220310001])
                    """

                    codTrib: str = field(
                        metadata={
                            "type": "Element",
                            "length": 9,
                            "white_space": "preserve",
                            "pattern": r"[1-9][0-9]{8}",
                        }
                    )
                    indTribISS: GTotalCodTribIndTribIss = field(
                        metadata={
                            "type": "Element",
                            "white_space": "preserve",
                        }
                    )
                    vApurTot: str = field(
                        metadata={
                            "type": "Element",
                            "min_length": 4,
                            "max_length": 18,
                            "white_space": "preserve",
                            "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                        }
                    )
                    vTotSaldoInic: None | str = field(
                        default=None,
                        metadata={
                            "type": "Element",
                            "min_length": 4,
                            "max_length": 18,
                            "white_space": "preserve",
                            "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                        },
                    )
                    vTotSaldoFinal: None | str = field(
                        default=None,
                        metadata={
                            "type": "Element",
                            "min_length": 4,
                            "max_length": 18,
                            "white_space": "preserve",
                            "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                        },
                    )
