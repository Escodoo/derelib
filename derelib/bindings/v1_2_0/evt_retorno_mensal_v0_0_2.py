from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from derelib.bindings.v1_2_0.xmldsig_core_schema import Signature
from derelib.mixin import DereMixin

__NAMESPACE__ = "http://www.dere.gov.br/schemas/evtRetornoMensal/v0_0_2"


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

    :ivar evtRetornoMensal: Retorno Totalizador – Fechamento Mensal.
    :ivar signature:
    """

    class Meta:
        name = "DeRE"
        namespace = "http://www.dere.gov.br/schemas/evtRetornoMensal/v0_0_2"

    evtRetornoMensal: DeRe.EvtRetornoMensal = field(
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
    class EvtRetornoMensal:
        """
        :ivar ideContrib: Informações de identificação do contribuinte.
        :ivar ideStatus: Situação do processamento do evento.
        :ivar infoRecEv: Informações de processamento dos eventos.
        :ivar infoEvento: Informações do evento processado.
        :ivar id: Identificação única do evento (campo id do evento transmitido
            pelo contribuinte, a que se refere este retorno).
        """

        ideContrib: DeRe.EvtRetornoMensal.IdeContrib = field(
            metadata={
                "type": "Element",
            }
        )
        ideStatus: DeRe.EvtRetornoMensal.IdeStatus = field(
            metadata={
                "type": "Element",
            }
        )
        infoRecEv: DeRe.EvtRetornoMensal.InfoRecEv = field(
            metadata={
                "type": "Element",
            }
        )
        infoEvento: None | DeRe.EvtRetornoMensal.InfoEvento = field(
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
            ocorrencias: list[DeRe.EvtRetornoMensal.IdeStatus.Ocorrencias] = field(
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
                Como o evento D-1199 admite apenas a operação de Inclusão
                ({tpOper} = [1]), as versões subsequentes ({seqEvento} maior que
                [00]) decorrem obrigatoriamente de novas transmissões de
                Fechamento efetuadas após o período ter sido reaberto por um
                evento de Reabertura de Período de Apuração (D-1198). Exemplo: 1º
                Envio (Inclusão): seqEvento = [00]; 2º Envio (Nova Inclusão):
                seqEvento = [01]; 3º Envio (Nova Inclusão): seqEvento = [02].
            :ivar protocoloLote: Número do protocolo de entrega do lote.
            :ivar dhRecepcao: Data e hora da recepção do evento (UTC). Máscara:
                AAAA-MM-DDThh:mm:ss.sssssssTZD
            :ivar dhProcess: Data e hora do início do processamento do evento
                (UTC). Máscara: AAAA-MM-DDThh:mm:ss.sssssssTZD
            :ivar tpEv: Sigla de identificação do tipo de evento. Exemplo:
                D-1199.
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
            :ivar infoAdic: Grupo destinado ao retorno de informações
                complementares relativas ao evento processado.
            :ivar infoTotFinanceiro: Informações relativas a totalizadores dos
                Serviços Financeiros.
            :ivar infoTotSaude: Informações relativas a totalizadores dos Planos
                de Assistência à Saúde.
            :ivar infoTotProg: Informações relativas a totalizadores dos
                Concursos de Prognósticos.
            :ivar totalTributosGeral: Totalização dos tributos do declarante.
            """

            idePeriodo: DeRe.EvtRetornoMensal.InfoEvento.IdePeriodo = field(
                metadata={
                    "type": "Element",
                }
            )
            infoAdic: DeRe.EvtRetornoMensal.InfoEvento.InfoAdic = field(
                metadata={
                    "type": "Element",
                }
            )
            infoTotFinanceiro: (
                None | DeRe.EvtRetornoMensal.InfoEvento.InfoTotFinanceiro
            ) = field(
                default=None,
                metadata={
                    "type": "Element",
                },
            )
            infoTotSaude: None | DeRe.EvtRetornoMensal.InfoEvento.InfoTotSaude = field(
                default=None,
                metadata={
                    "type": "Element",
                },
            )
            infoTotProg: None | DeRe.EvtRetornoMensal.InfoEvento.InfoTotProg = field(
                default=None,
                metadata={
                    "type": "Element",
                },
            )
            totalTributosGeral: DeRe.EvtRetornoMensal.InfoEvento.TotalTributosGeral = (
                field(
                    metadata={
                        "type": "Element",
                    }
                )
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
                :ivar nrReciboBalancete: Número do recibo do evento D-1101
                    (Balancete Mensal) utilizado para a totalização deste
                    processamento.
                :ivar nrReciboAplicFin: Número do recibo do evento D-1106
                    (Detalhamento de Aplicações Financeiras) utilizado para a
                    totalização deste processamento.
                :ivar nrReciboRelDedu: Número do recibo do evento D-1121 (Relação
                    de Deduções Utilizadas na Apuração) utilizado para a
                    totalização deste processamento.
                :ivar nrReciboOperTitPub: Número do recibo do evento D-2101
                    (Operações com Título de Oferta Pública) utilizado para a
                    totalização deste processamento.
                """

                nrReciboBalancete: str = field(
                    metadata={
                        "type": "Element",
                        "length": 31,
                        "white_space": "preserve",
                        "pattern": r"[0-9]{4}-20[0-9]{2}(0[1-9]|1[0-2])-[0-9A-Z]{19}",
                    }
                )
                nrReciboAplicFin: None | str = field(
                    default=None,
                    metadata={
                        "type": "Element",
                        "length": 31,
                        "white_space": "preserve",
                        "pattern": r"[0-9]{4}-20[0-9]{2}(0[1-9]|1[0-2])-[0-9A-Z]{19}",
                    },
                )
                nrReciboRelDedu: list[str] = field(
                    default_factory=list,
                    metadata={
                        "type": "Element",
                        "max_occurs": 99,
                        "length": 31,
                        "white_space": "preserve",
                        "pattern": r"[0-9]{4}-20[0-9]{2}(0[1-9]|1[0-2])-[0-9A-Z]{19}",
                    },
                )
                nrReciboOperTitPub: None | str = field(
                    default=None,
                    metadata={
                        "type": "Element",
                        "length": 31,
                        "white_space": "preserve",
                        "pattern": r"[0-9]{4}-20[0-9]{2}(0[1-9]|1[0-2])-[0-9A-Z]{19}",
                    },
                )

            @dataclass(kw_only=True)
            class InfoTotFinanceiro:
                """
                :ivar detBC: Detalhamento da base de cálculo.
                :ivar totalTributos: Totalização dos tributos do Regime
                    Específico de Serviços Financeiros.
                """

                detBC: list[
                    DeRe.EvtRetornoMensal.InfoEvento.InfoTotFinanceiro.DetBc
                ] = field(
                    default_factory=list,
                    metadata={
                        "type": "Element",
                        "min_occurs": 1,
                        "max_occurs": 100,
                    },
                )
                totalTributos: DeRe.EvtRetornoMensal.InfoEvento.InfoTotFinanceiro.TotalTributos = field(
                    metadata={
                        "type": "Element",
                    }
                )

                @dataclass(kw_only=True)
                class DetBc:
                    """
                    :ivar codBC: Código identificador da base de cálculo,
                        conforme [[Tabela 12 – Códigos de Bases de Cálculo]].
                    :ivar xDetBC: Descrição da base de cálculo.
                    :ivar gCoeficientes: Grupo de detalhamento dos coeficientes
                        de rateio e de reversão calculados pelo sistema para a
                        formação desta base de cálculo.
                    :ivar memoriaCalculo: Descrição textual dos valores
                        intermediários usados no cálculo. Todos os valores
                        apresentados serão arredondados para oito casas decimais.
                    :ivar gBCIBS: Detalhamento da base de cálculo do IBS.
                    :ivar gBCCBS: Detalhamento da base de cálculo da CBS.
                    :ivar infoBCN: Grupo de informações de bases de cálculo
                        negativas.
                    """

                    codBC: str = field(
                        metadata={
                            "type": "Element",
                            "length": 4,
                            "white_space": "preserve",
                            "pattern": r"[1-9][0-9A-Z]{3}",
                        }
                    )
                    xDetBC: str = field(
                        metadata={
                            "type": "Element",
                            "max_length": 1024,
                            "white_space": "preserve",
                            "pattern": r"([!-ÿ][ -ÿ]*[!-ÿ]|[!-ÿ])",
                        }
                    )
                    gCoeficientes: (
                        None
                        | DeRe.EvtRetornoMensal.InfoEvento.InfoTotFinanceiro.DetBc.GCoeficientes
                    ) = field(
                        default=None,
                        metadata={
                            "type": "Element",
                        },
                    )
                    memoriaCalculo: str = field(
                        metadata={
                            "type": "Element",
                            "max_length": 4096,
                            "white_space": "preserve",
                            "pattern": r"([!-ÿ][ -ÿ]*[!-ÿ]|[!-ÿ])",
                        }
                    )
                    gBCIBS: DeRe.EvtRetornoMensal.InfoEvento.InfoTotFinanceiro.DetBc.GBcibs = field(
                        metadata={
                            "type": "Element",
                        }
                    )
                    gBCCBS: DeRe.EvtRetornoMensal.InfoEvento.InfoTotFinanceiro.DetBc.GBccbs = field(
                        metadata={
                            "type": "Element",
                        }
                    )
                    infoBCN: (
                        None
                        | DeRe.EvtRetornoMensal.InfoEvento.InfoTotFinanceiro.DetBc.InfoBcn
                    ) = field(
                        default=None,
                        metadata={
                            "type": "Element",
                        },
                    )

                    @dataclass(kw_only=True)
                    class GCoeficientes:
                        """
                        :ivar pRateioDespCapt: Coeficiente utilizado para ratear
                            as despesas de captação de recursos entre as
                            atividades financeiras que permitem essa dedução.
                        :ivar pRevDedAtoCoop: Coeficiente utilizado para reverter
                            as deduções de despesas vinculadas a receitas
                            decorrentes de atos cooperados (sujeitas à alíquota
                            zero).
                        :ivar pExportIaV: Coeficiente aplicado para reverter
                            deduções de despesas vinculadas a receitas de
                            exportação das atividades previstas nos incisos I a V
                            do caput do art. 182 da LC 214/2025.
                        :ivar pExportVI: Coeficiente aplicado para reverter
                            deduções de despesas vinculadas a receitas de
                            exportação das atividades previstas no inciso VI do
                            caput do art. 182 da LC 214/2025.
                        :ivar pExportIX: Coeficiente aplicado para reverter
                            deduções de despesas vinculadas a receitas de
                            exportação das atividades previstas no inciso IX do
                            caput do art. 182 da LC 214/2025.
                        :ivar pExportXI: Coeficiente aplicado para reverter
                            deduções de despesas vinculadas a receitas de
                            exportação das atividades previstas no inciso XI do
                            caput do art. 182 da LC 214/2025.
                        :ivar pExportXIII: Coeficiente aplicado para reverter
                            deduções de despesas vinculadas a receitas de
                            exportação das atividades previstas no inciso XIII do
                            caput do art. 182 da LC 214/2025.
                        :ivar pExportXIV: Coeficiente aplicado para reverter
                            deduções de despesas vinculadas a receitas de
                            exportação das atividades previstas no inciso XIV do
                            caput do art. 182 da LC 214/2025.
                        """

                        pRateioDespCapt: None | str = field(
                            default=None,
                            metadata={
                                "type": "Element",
                                "min_length": 10,
                                "max_length": 12,
                                "white_space": "preserve",
                                "pattern": r"(0|[1-9][0-9]{0,2})\.[0-9]{8}",
                            },
                        )
                        pRevDedAtoCoop: None | str = field(
                            default=None,
                            metadata={
                                "type": "Element",
                                "min_length": 10,
                                "max_length": 12,
                                "white_space": "preserve",
                                "pattern": r"(0|[1-9][0-9]{0,2})\.[0-9]{8}",
                            },
                        )
                        pExportIaV: None | str = field(
                            default=None,
                            metadata={
                                "type": "Element",
                                "min_length": 10,
                                "max_length": 12,
                                "white_space": "preserve",
                                "pattern": r"(0|[1-9][0-9]{0,2})\.[0-9]{8}",
                            },
                        )
                        pExportVI: None | str = field(
                            default=None,
                            metadata={
                                "type": "Element",
                                "min_length": 10,
                                "max_length": 12,
                                "white_space": "preserve",
                                "pattern": r"(0|[1-9][0-9]{0,2})\.[0-9]{8}",
                            },
                        )
                        pExportIX: None | str = field(
                            default=None,
                            metadata={
                                "type": "Element",
                                "min_length": 10,
                                "max_length": 12,
                                "white_space": "preserve",
                                "pattern": r"(0|[1-9][0-9]{0,2})\.[0-9]{8}",
                            },
                        )
                        pExportXI: None | str = field(
                            default=None,
                            metadata={
                                "type": "Element",
                                "min_length": 10,
                                "max_length": 12,
                                "white_space": "preserve",
                                "pattern": r"(0|[1-9][0-9]{0,2})\.[0-9]{8}",
                            },
                        )
                        pExportXIII: None | str = field(
                            default=None,
                            metadata={
                                "type": "Element",
                                "min_length": 10,
                                "max_length": 12,
                                "white_space": "preserve",
                                "pattern": r"(0|[1-9][0-9]{0,2})\.[0-9]{8}",
                            },
                        )
                        pExportXIV: None | str = field(
                            default=None,
                            metadata={
                                "type": "Element",
                                "min_length": 10,
                                "max_length": 12,
                                "white_space": "preserve",
                                "pattern": r"(0|[1-9][0-9]{0,2})\.[0-9]{8}",
                            },
                        )

                    @dataclass(kw_only=True)
                    class GBcibs:
                        """
                        :ivar vBCIBS: Valor da base de cálculo do IBS. Cálculo:
                            SE {tabCodBC.vBCIBS} &gt;= [0.00], ENTÃO {vBCIBS} =
                            {tabCodBC.vBCIBS}, SENÃO {vBCIBS} = [0.00]
                        :ivar vBCNIBS: Valor absoluto do prejuízo (base de
                            cálculo negativa do IBS) gerado na apuração do
                            período corrente. Preenchimento: Este campo é
                            informado exclusivamente caso o resultado do cálculo
                            resulte em uma base de cálculo negativa
                            ({tabCodBC.vBCIBS} &lt; [0.00]). O valor é
                            apresentado em módulo. Cálculo: {vBCNIBS} =
                            {tabCodBC.vBCIBS} * (-1)
                        :ivar vDedBCN: Valor da base de cálculo negativa relativa
                            a período de apuração anterior a deduzir nesta
                            competência. Preenchimento: 1. SE o grupo
                            {D-1199.gUtilizBCN} não for informado, OU SE o campo
                            {D-1199.usarBCNAcum} correspondente for igual a [0]
                            (Opção por NÃO efetuar o aproveitamento de bases
                            negativas neste período), ENTÃO o campo {vDedBCN} não
                            será retornado; 2. SE o campo {D-1199.usarBCNAcum}
                            for igual a [1], o preenchimento observará o método
                            indicado pelo declarante: a. Método PEPS Automático
                            ({D-1199.metodoAproveit} = [0]): O valor de {vDedBCN}
                            será calculado automaticamente pelo sistema DeRE,
                            consumindo os saldos de bases negativas mais antigos
                            da {codBCNRaiz} correspondente até o limite da base
                            de cálculo positiva do mês corrente; b. Método Manual
                            ({D-1199.metodoAproveit} = [1]): O valor de {vDedBCN}
                            corresponderá ao somatório dos valores informados no
                            campo {D-1199.vUsarBCN} dentro do grupo
                            {D-1199.detBCNeg} para os códigos {D-1199.codBCN}
                            correspondentes. Validação: O valor de {vDedBCN} deve
                            ser menor ou igual a {vBCIBS}. Caso ultrapasse, o
                            valor de {vDedBCN} fica limitado ao valor da
                            {vBCIBS}, ajustando o valor utilizado na tabela de
                            bases de cálculo negativas.
                        :ivar vBCApurIBS: Base de cálculo efetiva do IBS após
                            compensação de saldos de base de cálculo negativas de
                            períodos anteriores. Cálculo: SE {vBCIBS} = [0.00],
                            ENTÃO {vBCApurIBS} = [0.00], SENÃO {vBCApurIBS} =
                            {vBCIBS} - {vDedBCN}
                        :ivar pIBSMun: Alíquota do IBS municipal. Sem símbolo
                            (%).
                        :ivar vIBSMun: Valor do IBS municipal. Cálculo:
                            {vBCApurIBS} * ({pIBSMun} / 100)
                        :ivar pIBSUF: Alíquota do IBS estadual. Sem símbolo (%).
                        :ivar vIBSUF: Valor do IBS estadual. Cálculo:
                            {vBCApurIBS} * ({pIBSUF} / 100)
                        :ivar pIBS: Soma das alíquotas {pIBSMun} e {pIBSUF}. Sem
                            símbolo (%).
                        :ivar vIBSTot: Valor total do IBS. Cálculo: {vIBSMun} +
                            {vIBSUF}
                        """

                        vBCIBS: str = field(
                            metadata={
                                "type": "Element",
                                "min_length": 4,
                                "max_length": 18,
                                "white_space": "preserve",
                                "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                            }
                        )
                        vBCNIBS: None | str = field(
                            default=None,
                            metadata={
                                "type": "Element",
                                "min_length": 4,
                                "max_length": 18,
                                "white_space": "preserve",
                                "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                            },
                        )
                        vDedBCN: None | str = field(
                            default=None,
                            metadata={
                                "type": "Element",
                                "min_length": 4,
                                "max_length": 18,
                                "white_space": "preserve",
                                "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                            },
                        )
                        vBCApurIBS: str = field(
                            metadata={
                                "type": "Element",
                                "min_length": 4,
                                "max_length": 18,
                                "white_space": "preserve",
                                "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                            }
                        )
                        pIBSMun: str = field(
                            metadata={
                                "type": "Element",
                                "min_length": 8,
                                "max_length": 10,
                                "white_space": "preserve",
                                "pattern": r"(0|[1-9][0-9]{0,2})\.[0-9]{6}",
                            }
                        )
                        vIBSMun: str = field(
                            metadata={
                                "type": "Element",
                                "min_length": 4,
                                "max_length": 18,
                                "white_space": "preserve",
                                "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                            }
                        )
                        pIBSUF: str = field(
                            metadata={
                                "type": "Element",
                                "min_length": 8,
                                "max_length": 10,
                                "white_space": "preserve",
                                "pattern": r"(0|[1-9][0-9]{0,2})\.[0-9]{6}",
                            }
                        )
                        vIBSUF: str = field(
                            metadata={
                                "type": "Element",
                                "min_length": 4,
                                "max_length": 18,
                                "white_space": "preserve",
                                "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                            }
                        )
                        pIBS: str = field(
                            metadata={
                                "type": "Element",
                                "min_length": 8,
                                "max_length": 10,
                                "white_space": "preserve",
                                "pattern": r"(0|[1-9][0-9]{0,2})\.[0-9]{6}",
                            }
                        )
                        vIBSTot: str = field(
                            metadata={
                                "type": "Element",
                                "min_length": 4,
                                "max_length": 18,
                                "white_space": "preserve",
                                "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                            }
                        )

                    @dataclass(kw_only=True)
                    class GBccbs:
                        """
                        :ivar vBCCBS: Valor da base de cálculo da CBS. Cálculo:
                            SE {tabCodBC.vBCCBS} &gt;= [0.00], ENTÃO {vBCCBS} =
                            {tabCodBC.vBCCBS}, SENÃO {vBCCBS} = [0.00]
                        :ivar vBCNCBS: Valor absoluto da base de cálculo negativa
                            da CBS gerado na apuração do período corrente.
                            Preenchimento: Este campo é informado exclusivamente
                            caso o resultado do cálculo resulte em uma base de
                            cálculo negativa ({tabCodBC.vBCCBS} &lt; [0.00]). O
                            valor é apresentado em módulo. Cálculo: {vBCNCBS} =
                            {tabCodBC.vBCCBS} * (-1)
                        :ivar vDedBCN: Valor da base de cálculo negativa relativa
                            a período de apuração anterior a deduzir nesta
                            competência. Preenchimento: 1. SE o grupo
                            {D-1199.gUtilizBCN} não for informado, OU SE o campo
                            {D-1199.usarBCNAcum} correspondente for igual a [0]
                            (Opção por NÃO efetuar o aproveitamento de bases
                            negativas neste período), ENTÃO o campo {vDedBCN} não
                            será retornado; 2. SE o campo {D-1199.usarBCNAcum}
                            for igual a [1], o preenchimento observará o método
                            indicado pelo declarante: a. Método PEPS Automático
                            ({D-1199.metodoAproveit} = [0]): O valor de {vDedBCN}
                            será calculado automaticamente pelo sistema DeRE,
                            consumindo os saldos de bases negativas mais antigos
                            da {codBCNRaiz} correspondente até o limite da base
                            de cálculo positiva do mês corrente; b. Método Manual
                            ({D-1199.metodoAproveit} = [1]): O valor de {vDedBCN}
                            corresponderá ao somatório dos valores informados no
                            campo {D-1199.vUsarBCN} dentro do grupo
                            {D-1199.detBCNeg} para os códigos {D-1199.codBCN}
                            correspondentes. Validação: O valor de {vDedBCN} deve
                            ser menor ou igual a {vBCCBS}. Caso ultrapasse, o
                            valor de {vDedBCN} fica limitado ao valor da
                            {vBCCBS}, ajustando o valor utilizado na tabela de
                            bases de cálculo negativas.
                        :ivar vBCApurCBS: Base de cálculo efetiva da CBS após
                            compensação de saldos de base de cálculo negativas de
                            períodos anteriores. Cálculo: SE {vBCCBS} = [0.00],
                            ENTÃO {vBCApurCBS} = [0.00], SENÃO {vBCApurCBS} =
                            {vBCCBS} - {vDedBCN}
                        :ivar pCBS: Alíquota da CBS. Sem símbolo (%).
                        :ivar vCBS: Valor da CBS. Cálculo: {vBCApurCBS} * ({pCBS}
                            / 100)
                        """

                        vBCCBS: str = field(
                            metadata={
                                "type": "Element",
                                "min_length": 4,
                                "max_length": 18,
                                "white_space": "preserve",
                                "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                            }
                        )
                        vBCNCBS: None | str = field(
                            default=None,
                            metadata={
                                "type": "Element",
                                "min_length": 4,
                                "max_length": 18,
                                "white_space": "preserve",
                                "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                            },
                        )
                        vDedBCN: None | str = field(
                            default=None,
                            metadata={
                                "type": "Element",
                                "min_length": 4,
                                "max_length": 18,
                                "white_space": "preserve",
                                "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                            },
                        )
                        vBCApurCBS: str = field(
                            metadata={
                                "type": "Element",
                                "min_length": 4,
                                "max_length": 18,
                                "white_space": "preserve",
                                "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                            }
                        )
                        pCBS: str = field(
                            metadata={
                                "type": "Element",
                                "min_length": 8,
                                "max_length": 10,
                                "white_space": "preserve",
                                "pattern": r"(0|[1-9][0-9]{0,2})\.[0-9]{6}",
                            }
                        )
                        vCBS: str = field(
                            metadata={
                                "type": "Element",
                                "min_length": 4,
                                "max_length": 18,
                                "white_space": "preserve",
                                "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                            }
                        )

                    @dataclass(kw_only=True)
                    class InfoBcn:
                        """
                        :ivar gBCNIBS: Grupo de detalhamento de bases de cálculo
                            negativas de IBS.
                        :ivar gBCNCBS: Grupo de detalhamento de bases de cálculo
                            negativas de CBS.
                        """

                        gBCNIBS: DeRe.EvtRetornoMensal.InfoEvento.InfoTotFinanceiro.DetBc.InfoBcn.GBcnibs = field(
                            metadata={
                                "type": "Element",
                            }
                        )
                        gBCNCBS: DeRe.EvtRetornoMensal.InfoEvento.InfoTotFinanceiro.DetBc.InfoBcn.GBcncbs = field(
                            metadata={
                                "type": "Element",
                            }
                        )

                        @dataclass(kw_only=True)
                        class GBcnibs:
                            """
                            :ivar codBCNRaiz: Código identificador raiz da base
                                de cálculo negativa, conforme [[Tabela 12 –
                                Códigos de Bases de Cálculo]].
                            :ivar vSaldoAnt: Valor do saldo anterior. Montante
                                acumulado da base de cálculo negativa disponível
                                no início do período de apuração atual, antes das
                                compensações do mês.
                            :ivar vUtilPer: Valor da base de cálculo negativa
                                utilizado como dedução da base de cálculo do
                                período de apuração atual. Cálculo: Igual a
                                {vDedBCN}
                            :ivar vSaldoFinal: Valor do saldo remanescente de
                                base de cálculo negativa a ser transportado para
                                o próximo período de apuração. Cálculo:
                                {vSaldoAnt} - {vUtilPer} + {vBCNIBS} (se houver)
                            :ivar qtdOrigens: Quantidade de períodos de origem.
                                Indica quantos períodos distintos compõem o saldo
                                atual. Exemplo: Se o saldo é composto por bases
                                negativas de jan/25 e mar/26, {qtdOrigens} = [2].
                            :ivar detBCN: Detalhamento da composição do saldo por
                                período de origem.
                            """

                            codBCNRaiz: str = field(
                                metadata={
                                    "type": "Element",
                                    "length": 5,
                                    "white_space": "preserve",
                                    "pattern": r"[1-9][0-9]{3}[IC]",
                                }
                            )
                            vSaldoAnt: str = field(
                                metadata={
                                    "type": "Element",
                                    "min_length": 4,
                                    "max_length": 18,
                                    "white_space": "preserve",
                                    "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                                }
                            )
                            vUtilPer: str = field(
                                metadata={
                                    "type": "Element",
                                    "min_length": 4,
                                    "max_length": 18,
                                    "white_space": "preserve",
                                    "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                                }
                            )
                            vSaldoFinal: str = field(
                                metadata={
                                    "type": "Element",
                                    "min_length": 4,
                                    "max_length": 18,
                                    "white_space": "preserve",
                                    "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                                }
                            )
                            qtdOrigens: str = field(
                                metadata={
                                    "type": "Element",
                                    "max_length": 2,
                                    "white_space": "preserve",
                                    "pattern": r"[1-9][0-9]?",
                                }
                            )
                            detBCN: list[
                                DeRe.EvtRetornoMensal.InfoEvento.InfoTotFinanceiro.DetBc.InfoBcn.GBcnibs.DetBcn
                            ] = field(
                                default_factory=list,
                                metadata={
                                    "type": "Element",
                                    "max_occurs": 100,
                                },
                            )

                            @dataclass(kw_only=True)
                            class DetBcn:
                                """
                                :ivar codBCN: Código identificador da base de
                                    cálculo negativa, conforme [[Tabela 12 –
                                    Códigos de Bases de Cálculo]].
                                :ivar perOrigem: Período de origem da base de
                                    cálculo negativa. Máscara: AAAA-MM
                                :ivar vOrigemIni: Valor inicial da base de
                                    cálculo negativa no respectivo período de
                                    origem.
                                :ivar vSaldoAnt: Valor da base de cálculo
                                    negativa disponível para uso neste período de
                                    apuração. Cálculo: SE {perOrigem} =
                                    {perApur}, ENTÃO {vSaldoAnt} = [0.00], SENÃO
                                    {vSaldoAnt} = {vSaldoFinal} do {perApur}
                                    imediatamente anterior.
                                :ivar vUtilPer: Valor da base de cálculo negativa
                                    utilizada neste período de apuração.
                                :ivar vSaldoFinal: Saldo remanescente desta base
                                    de cálculo negativa para os próximos períodos
                                    de apuração.
                                """

                                codBCN: str = field(
                                    metadata={
                                        "type": "Element",
                                        "length": 13,
                                        "white_space": "preserve",
                                        "pattern": r"[1-9][0-9]{3}[IC][0-9]{8}",
                                    }
                                )
                                perOrigem: str = field(
                                    metadata={
                                        "type": "Element",
                                        "length": 7,
                                        "white_space": "preserve",
                                        "pattern": r"20[0-9]{2}-(0[1-9]|1[0-2])",
                                    }
                                )
                                vOrigemIni: str = field(
                                    metadata={
                                        "type": "Element",
                                        "min_length": 4,
                                        "max_length": 18,
                                        "white_space": "preserve",
                                        "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                                    }
                                )
                                vSaldoAnt: str = field(
                                    metadata={
                                        "type": "Element",
                                        "min_length": 4,
                                        "max_length": 18,
                                        "white_space": "preserve",
                                        "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                                    }
                                )
                                vUtilPer: str = field(
                                    metadata={
                                        "type": "Element",
                                        "min_length": 4,
                                        "max_length": 18,
                                        "white_space": "preserve",
                                        "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                                    }
                                )
                                vSaldoFinal: str = field(
                                    metadata={
                                        "type": "Element",
                                        "min_length": 4,
                                        "max_length": 18,
                                        "white_space": "preserve",
                                        "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                                    }
                                )

                        @dataclass(kw_only=True)
                        class GBcncbs:
                            """
                            :ivar codBCNRaiz: Código identificador raiz da base
                                de cálculo negativa, conforme [[Tabela 12 –
                                Códigos de Bases de Cálculo]].
                            :ivar vSaldoAnt: Valor do saldo anterior. Montante
                                acumulado da base de cálculo negativa disponível
                                no início do período de apuração atual, antes das
                                compensações do mês.
                            :ivar vUtilPer: Valor da base de cálculo negativa
                                utilizado como dedução da base de cálculo do
                                período de apuração atual. Cálculo: Igual a
                                {vDedBCN}
                            :ivar vSaldoFinal: Valor do saldo remanescente de
                                base de cálculo negativa a ser transportado para
                                o próximo período de apuração. Cálculo:
                                {vSaldoAnt} - {vUtilPer} + {vBCNCBS} (se houver)
                            :ivar qtdOrigens: Quantidade de períodos de origem.
                                Indica quantos períodos distintos compõem o saldo
                                atual. Exemplo: Se o saldo é composto por bases
                                negativas de jan/25 e mar/26, {qtdOrigens} = [2].
                            :ivar detBCN: Detalhamento da composição do saldo por
                                período de origem.
                            """

                            codBCNRaiz: str = field(
                                metadata={
                                    "type": "Element",
                                    "length": 5,
                                    "white_space": "preserve",
                                    "pattern": r"[1-9][0-9]{3}[IC]",
                                }
                            )
                            vSaldoAnt: str = field(
                                metadata={
                                    "type": "Element",
                                    "min_length": 4,
                                    "max_length": 18,
                                    "white_space": "preserve",
                                    "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                                }
                            )
                            vUtilPer: str = field(
                                metadata={
                                    "type": "Element",
                                    "min_length": 4,
                                    "max_length": 18,
                                    "white_space": "preserve",
                                    "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                                }
                            )
                            vSaldoFinal: str = field(
                                metadata={
                                    "type": "Element",
                                    "min_length": 4,
                                    "max_length": 18,
                                    "white_space": "preserve",
                                    "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                                }
                            )
                            qtdOrigens: str = field(
                                metadata={
                                    "type": "Element",
                                    "max_length": 2,
                                    "white_space": "preserve",
                                    "pattern": r"[1-9][0-9]?",
                                }
                            )
                            detBCN: list[
                                DeRe.EvtRetornoMensal.InfoEvento.InfoTotFinanceiro.DetBc.InfoBcn.GBcncbs.DetBcn
                            ] = field(
                                default_factory=list,
                                metadata={
                                    "type": "Element",
                                    "max_occurs": 100,
                                },
                            )

                            @dataclass(kw_only=True)
                            class DetBcn:
                                """
                                :ivar codBCN: Código identificador da base de
                                    cálculo negativa, conforme [[Tabela 12 –
                                    Códigos de Bases de Cálculo]].
                                :ivar perOrigem: Período de origem da base de
                                    cálculo negativa. Máscara: AAAA-MM
                                :ivar vOrigemIni: Valor inicial da base de
                                    cálculo negativa no respectivo período de
                                    origem.
                                :ivar vSaldoAnt: Valor da base de cálculo
                                    negativa disponível para uso neste período de
                                    apuração. Cálculo: SE {perOrigem} =
                                    {perApur}, ENTÃO {vSaldoAnt} = [0.00], SENÃO
                                    {vSaldoAnt} = {vSaldoFinal} do {perApur}
                                    imediatamente anterior.
                                :ivar vUtilPer: Valor da base de cálculo negativa
                                    utilizada neste período de apuração.
                                :ivar vSaldoFinal: Saldo remanescente desta base
                                    de cálculo negativa para os próximos períodos
                                    de apuração.
                                """

                                codBCN: str = field(
                                    metadata={
                                        "type": "Element",
                                        "length": 13,
                                        "white_space": "preserve",
                                        "pattern": r"[1-9][0-9]{3}[IC][0-9]{8}",
                                    }
                                )
                                perOrigem: str = field(
                                    metadata={
                                        "type": "Element",
                                        "length": 7,
                                        "white_space": "preserve",
                                        "pattern": r"20[0-9]{2}-(0[1-9]|1[0-2])",
                                    }
                                )
                                vOrigemIni: str = field(
                                    metadata={
                                        "type": "Element",
                                        "min_length": 4,
                                        "max_length": 18,
                                        "white_space": "preserve",
                                        "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                                    }
                                )
                                vSaldoAnt: str = field(
                                    metadata={
                                        "type": "Element",
                                        "min_length": 4,
                                        "max_length": 18,
                                        "white_space": "preserve",
                                        "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                                    }
                                )
                                vUtilPer: str = field(
                                    metadata={
                                        "type": "Element",
                                        "min_length": 4,
                                        "max_length": 18,
                                        "white_space": "preserve",
                                        "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                                    }
                                )
                                vSaldoFinal: str = field(
                                    metadata={
                                        "type": "Element",
                                        "min_length": 4,
                                        "max_length": 18,
                                        "white_space": "preserve",
                                        "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                                    }
                                )

                @dataclass(kw_only=True)
                class TotalTributos:
                    """
                    :ivar vIBSMun: Valor do IBS municipal. Cálculo:
                        SOMA({infoTotFinanceiro.detBC.vIBSMun})
                    :ivar vIBSUF: Valor do IBS estadual. Cálculo:
                        SOMA({infoTotFinanceiro.detBC.vIBSUF})
                    :ivar vIBSTot: Valor total do IBS. Cálculo:
                        {totalTributos.vIBSMun} + {totalTributos.vIBSUF}
                    :ivar vCBS: Valor da CBS. Cálculo:
                        SOMA({infoTotFinanceiro.detBC.vCBS})
                    """

                    vIBSMun: str = field(
                        metadata={
                            "type": "Element",
                            "min_length": 4,
                            "max_length": 18,
                            "white_space": "preserve",
                            "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                        }
                    )
                    vIBSUF: str = field(
                        metadata={
                            "type": "Element",
                            "min_length": 4,
                            "max_length": 18,
                            "white_space": "preserve",
                            "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                        }
                    )
                    vIBSTot: str = field(
                        metadata={
                            "type": "Element",
                            "min_length": 4,
                            "max_length": 18,
                            "white_space": "preserve",
                            "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                        }
                    )
                    vCBS: str = field(
                        metadata={
                            "type": "Element",
                            "min_length": 4,
                            "max_length": 18,
                            "white_space": "preserve",
                            "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                        }
                    )

            @dataclass(kw_only=True)
            class InfoTotSaude:
                """
                :ivar detBC: Detalhamento da base de cálculo.
                :ivar totalTributos: Totalização dos tributos do Regime
                    Específico de Planos de Assistência à Saúde.
                """

                detBC: list[DeRe.EvtRetornoMensal.InfoEvento.InfoTotSaude.DetBc] = (
                    field(
                        default_factory=list,
                        metadata={
                            "type": "Element",
                            "min_occurs": 1,
                            "max_occurs": 100,
                        },
                    )
                )
                totalTributos: DeRe.EvtRetornoMensal.InfoEvento.InfoTotSaude.TotalTributos = field(
                    metadata={
                        "type": "Element",
                    }
                )

                @dataclass(kw_only=True)
                class DetBc:
                    """
                    :ivar codBC: Código identificador da base de cálculo,
                        conforme [[Tabela 12 – Códigos de Bases de Cálculo]].
                    :ivar xDetBC: Descrição da base de cálculo.
                    :ivar memoriaCalculo: Descrição textual dos valores
                        intermediários usados no cálculo. Todos os valores
                        apresentados serão arredondados para oito casas decimais.
                    :ivar gBCIBS: Detalhamento da base de cálculo do IBS.
                    :ivar gBCCBS: Detalhamento da base de cálculo da CBS.
                    :ivar infoBCN: Grupo de informações de bases de cálculo
                        negativas.
                    """

                    codBC: str = field(
                        metadata={
                            "type": "Element",
                            "length": 4,
                            "white_space": "preserve",
                            "pattern": r"[1-9][0-9A-Z]{3}",
                        }
                    )
                    xDetBC: str = field(
                        metadata={
                            "type": "Element",
                            "max_length": 1024,
                            "white_space": "preserve",
                            "pattern": r"([!-ÿ][ -ÿ]*[!-ÿ]|[!-ÿ])",
                        }
                    )
                    memoriaCalculo: str = field(
                        metadata={
                            "type": "Element",
                            "max_length": 4096,
                            "white_space": "preserve",
                            "pattern": r"([!-ÿ][ -ÿ]*[!-ÿ]|[!-ÿ])",
                        }
                    )
                    gBCIBS: DeRe.EvtRetornoMensal.InfoEvento.InfoTotSaude.DetBc.GBcibs = field(
                        metadata={
                            "type": "Element",
                        }
                    )
                    gBCCBS: DeRe.EvtRetornoMensal.InfoEvento.InfoTotSaude.DetBc.GBccbs = field(
                        metadata={
                            "type": "Element",
                        }
                    )
                    infoBCN: (
                        None
                        | DeRe.EvtRetornoMensal.InfoEvento.InfoTotSaude.DetBc.InfoBcn
                    ) = field(
                        default=None,
                        metadata={
                            "type": "Element",
                        },
                    )

                    @dataclass(kw_only=True)
                    class GBcibs:
                        """
                        :ivar vBCIBS: Valor da base de cálculo do IBS. Cálculo:
                            SE {tabCodBC.vBCIBS} &gt;= [0.00], ENTÃO {vBCIBS} =
                            {tabCodBC.vBCIBS}, SENÃO {vBCIBS} = [0.00]
                        :ivar vBCNIBS: Valor absoluto do prejuízo (base de
                            cálculo negativa do IBS) gerado na apuração do
                            período corrente. Preenchimento: Este campo é
                            informado exclusivamente caso o resultado do cálculo
                            resulte em uma base de cálculo negativa
                            ({tabCodBC.vBCIBS} &lt; [0.00]). O valor é
                            apresentado em módulo. Cálculo: {vBCNIBS} =
                            {tabCodBC.vBCIBS} * (-1)
                        :ivar vDedBCN: Valor da base de cálculo negativa relativa
                            a período de apuração anterior a deduzir nesta
                            competência. Preenchimento: 1. SE o grupo
                            {D-1199.gUtilizBCN} não for informado, OU SE o campo
                            {D-1199.usarBCNAcum} correspondente for igual a [0]
                            (Opção por NÃO efetuar o aproveitamento de bases
                            negativas neste período), ENTÃO o campo {vDedBCN} não
                            será retornado; 2. SE o campo {D-1199.usarBCNAcum}
                            for igual a [1], o preenchimento observará o método
                            indicado pelo declarante: a. Método PEPS Automático
                            ({D-1199.metodoAproveit} = [0]): O valor de {vDedBCN}
                            será calculado automaticamente pelo sistema DeRE,
                            consumindo os saldos de bases negativas mais antigos
                            da {codBCNRaiz} correspondente até o limite da base
                            de cálculo positiva do mês corrente; b. Método Manual
                            ({D-1199.metodoAproveit} = [1]): O valor de {vDedBCN}
                            corresponderá ao somatório dos valores informados no
                            campo {D-1199.vUsarBCN} dentro do grupo
                            {D-1199.detBCNeg} para os códigos {D-1199.codBCN}
                            correspondentes. Validação: O valor de {vDedBCN} deve
                            ser menor ou igual a {vBCIBS}. Caso ultrapasse, o
                            valor de {vDedBCN} fica limitado ao valor da
                            {vBCIBS}, ajustando o valor utilizado na tabela de
                            bases de cálculo negativas.
                        :ivar vBCApurIBS: Base de cálculo efetiva do IBS após
                            compensação de saldos de base de cálculo negativas de
                            períodos anteriores. Cálculo: SE {vBCIBS} = [0.00],
                            ENTÃO {vBCApurIBS} = [0.00], SENÃO {vBCApurIBS} =
                            {vBCIBS} - {vDedBCN}
                        :ivar pIBSMun: Alíquota do IBS municipal. Sem símbolo
                            (%).
                        :ivar vIBSMun: Valor do IBS municipal. Cálculo:
                            {vBCApurIBS} * ({pIBSMun} / 100)
                        :ivar pIBSUF: Alíquota do IBS estadual. Sem símbolo (%).
                        :ivar vIBSUF: Valor do IBS estadual. Cálculo:
                            {vBCApurIBS} * ({pIBSUF} / 100)
                        :ivar pIBS: Soma das alíquotas {pIBSMun} e {pIBSUF}. Sem
                            símbolo (%).
                        :ivar vIBSTot: Valor total do IBS. Cálculo: {vIBSMun} +
                            {vIBSUF}
                        """

                        vBCIBS: str = field(
                            metadata={
                                "type": "Element",
                                "min_length": 4,
                                "max_length": 18,
                                "white_space": "preserve",
                                "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                            }
                        )
                        vBCNIBS: None | str = field(
                            default=None,
                            metadata={
                                "type": "Element",
                                "min_length": 4,
                                "max_length": 18,
                                "white_space": "preserve",
                                "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                            },
                        )
                        vDedBCN: None | str = field(
                            default=None,
                            metadata={
                                "type": "Element",
                                "min_length": 4,
                                "max_length": 18,
                                "white_space": "preserve",
                                "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                            },
                        )
                        vBCApurIBS: str = field(
                            metadata={
                                "type": "Element",
                                "min_length": 4,
                                "max_length": 18,
                                "white_space": "preserve",
                                "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                            }
                        )
                        pIBSMun: str = field(
                            metadata={
                                "type": "Element",
                                "min_length": 8,
                                "max_length": 10,
                                "white_space": "preserve",
                                "pattern": r"(0|[1-9][0-9]{0,2})\.[0-9]{6}",
                            }
                        )
                        vIBSMun: str = field(
                            metadata={
                                "type": "Element",
                                "min_length": 4,
                                "max_length": 18,
                                "white_space": "preserve",
                                "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                            }
                        )
                        pIBSUF: str = field(
                            metadata={
                                "type": "Element",
                                "min_length": 8,
                                "max_length": 10,
                                "white_space": "preserve",
                                "pattern": r"(0|[1-9][0-9]{0,2})\.[0-9]{6}",
                            }
                        )
                        vIBSUF: str = field(
                            metadata={
                                "type": "Element",
                                "min_length": 4,
                                "max_length": 18,
                                "white_space": "preserve",
                                "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                            }
                        )
                        pIBS: str = field(
                            metadata={
                                "type": "Element",
                                "min_length": 8,
                                "max_length": 10,
                                "white_space": "preserve",
                                "pattern": r"(0|[1-9][0-9]{0,2})\.[0-9]{6}",
                            }
                        )
                        vIBSTot: str = field(
                            metadata={
                                "type": "Element",
                                "min_length": 4,
                                "max_length": 18,
                                "white_space": "preserve",
                                "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                            }
                        )

                    @dataclass(kw_only=True)
                    class GBccbs:
                        """
                        :ivar vBCCBS: Valor da base de cálculo da CBS. Cálculo:
                            SE {tabCodBC.vBCCBS} &gt;= [0.00], ENTÃO {vBCCBS} =
                            {tabCodBC.vBCCBS}, SENÃO {vBCCBS} = [0.00]
                        :ivar vBCNCBS: Valor absoluto da base de cálculo negativa
                            da CBS gerado na apuração do período corrente.
                            Preenchimento: Este campo é informado exclusivamente
                            caso o resultado do cálculo resulte em uma base de
                            cálculo negativa ({tabCodBC.vBCCBS} &lt; [0.00]). O
                            valor é apresentado em módulo. Cálculo: {vBCNCBS} =
                            {tabCodBC.vBCCBS} * (-1)
                        :ivar vDedBCN: Valor da base de cálculo negativa relativa
                            a período de apuração anterior a deduzir nesta
                            competência. Preenchimento: 1. SE o grupo
                            {D-1199.gUtilizBCN} não for informado, OU SE o campo
                            {D-1199.usarBCNAcum} correspondente for igual a [0]
                            (Opção por NÃO efetuar o aproveitamento de bases
                            negativas neste período), ENTÃO o campo {vDedBCN} não
                            será retornado; 2. SE o campo {D-1199.usarBCNAcum}
                            for igual a [1], o preenchimento observará o método
                            indicado pelo declarante: a. Método PEPS Automático
                            ({D-1199.metodoAproveit} = [0]): O valor de {vDedBCN}
                            será calculado automaticamente pelo sistema DeRE,
                            consumindo os saldos de bases negativas mais antigos
                            da {codBCNRaiz} correspondente até o limite da base
                            de cálculo positiva do mês corrente; b. Método Manual
                            ({D-1199.metodoAproveit} = [1]): O valor de {vDedBCN}
                            corresponderá ao somatório dos valores informados no
                            campo {D-1199.vUsarBCN} dentro do grupo
                            {D-1199.detBCNeg} para os códigos {D-1199.codBCN}
                            correspondentes. Validação: O valor de {vDedBCN} deve
                            ser menor ou igual a {vBCCBS}. Caso ultrapasse, o
                            valor de {vDedBCN} fica limitado ao valor da
                            {vBCCBS}, ajustando o valor utilizado na tabela de
                            bases de cálculo negativas.
                        :ivar vBCApurCBS: Base de cálculo efetiva da CBS após
                            compensação de saldos de base de cálculo negativas de
                            períodos anteriores. Cálculo: SE {vBCCBS} = [0.00],
                            ENTÃO {vBCApurCBS} = [0.00], SENÃO {vBCApurCBS} =
                            {vBCCBS} - {vDedBCN}
                        :ivar pCBS: Alíquota da CBS. Sem símbolo (%).
                        :ivar vCBS: Valor da CBS. Cálculo: {vBCApurCBS} * ({pCBS}
                            / 100)
                        """

                        vBCCBS: str = field(
                            metadata={
                                "type": "Element",
                                "min_length": 4,
                                "max_length": 18,
                                "white_space": "preserve",
                                "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                            }
                        )
                        vBCNCBS: None | str = field(
                            default=None,
                            metadata={
                                "type": "Element",
                                "min_length": 4,
                                "max_length": 18,
                                "white_space": "preserve",
                                "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                            },
                        )
                        vDedBCN: None | str = field(
                            default=None,
                            metadata={
                                "type": "Element",
                                "min_length": 4,
                                "max_length": 18,
                                "white_space": "preserve",
                                "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                            },
                        )
                        vBCApurCBS: str = field(
                            metadata={
                                "type": "Element",
                                "min_length": 4,
                                "max_length": 18,
                                "white_space": "preserve",
                                "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                            }
                        )
                        pCBS: str = field(
                            metadata={
                                "type": "Element",
                                "min_length": 8,
                                "max_length": 10,
                                "white_space": "preserve",
                                "pattern": r"(0|[1-9][0-9]{0,2})\.[0-9]{6}",
                            }
                        )
                        vCBS: str = field(
                            metadata={
                                "type": "Element",
                                "min_length": 4,
                                "max_length": 18,
                                "white_space": "preserve",
                                "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                            }
                        )

                    @dataclass(kw_only=True)
                    class InfoBcn:
                        """
                        :ivar gBCNIBS: Grupo de detalhamento de bases de cálculo
                            negativas de IBS.
                        :ivar gBCNCBS: Grupo de detalhamento de bases de cálculo
                            negativas de CBS.
                        """

                        gBCNIBS: DeRe.EvtRetornoMensal.InfoEvento.InfoTotSaude.DetBc.InfoBcn.GBcnibs = field(
                            metadata={
                                "type": "Element",
                            }
                        )
                        gBCNCBS: DeRe.EvtRetornoMensal.InfoEvento.InfoTotSaude.DetBc.InfoBcn.GBcncbs = field(
                            metadata={
                                "type": "Element",
                            }
                        )

                        @dataclass(kw_only=True)
                        class GBcnibs:
                            """
                            :ivar codBCNRaiz: Código identificador raiz da base
                                de cálculo negativa, conforme [[Tabela 12 –
                                Códigos de Bases de Cálculo]].
                            :ivar vSaldoAnt: Valor do saldo anterior. Montante
                                acumulado da base de cálculo negativa disponível
                                no início do período de apuração atual, antes das
                                compensações do mês.
                            :ivar vUtilPer: Valor da base de cálculo negativa
                                utilizado como dedução da base de cálculo do
                                período de apuração atual. Cálculo: Igual a
                                {vDedBCN}
                            :ivar vSaldoFinal: Valor do saldo remanescente de
                                base de cálculo negativa a ser transportado para
                                o próximo período de apuração. Cálculo:
                                {vSaldoAnt} - {vUtilPer} + {vBCNIBS} (se houver)
                            :ivar qtdOrigens: Quantidade de períodos de origem.
                                Indica quantos períodos distintos compõem o saldo
                                atual. Exemplo: Se o saldo é composto por bases
                                negativas de jan/25 e mar/26, {qtdOrigens} = [2].
                            :ivar detBCN: Detalhamento da composição do saldo por
                                período de origem.
                            """

                            codBCNRaiz: str = field(
                                metadata={
                                    "type": "Element",
                                    "length": 5,
                                    "white_space": "preserve",
                                    "pattern": r"[1-9][0-9]{3}[IC]",
                                }
                            )
                            vSaldoAnt: str = field(
                                metadata={
                                    "type": "Element",
                                    "min_length": 4,
                                    "max_length": 18,
                                    "white_space": "preserve",
                                    "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                                }
                            )
                            vUtilPer: str = field(
                                metadata={
                                    "type": "Element",
                                    "min_length": 4,
                                    "max_length": 18,
                                    "white_space": "preserve",
                                    "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                                }
                            )
                            vSaldoFinal: str = field(
                                metadata={
                                    "type": "Element",
                                    "min_length": 4,
                                    "max_length": 18,
                                    "white_space": "preserve",
                                    "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                                }
                            )
                            qtdOrigens: str = field(
                                metadata={
                                    "type": "Element",
                                    "max_length": 2,
                                    "white_space": "preserve",
                                    "pattern": r"[1-9][0-9]?",
                                }
                            )
                            detBCN: list[
                                DeRe.EvtRetornoMensal.InfoEvento.InfoTotSaude.DetBc.InfoBcn.GBcnibs.DetBcn
                            ] = field(
                                default_factory=list,
                                metadata={
                                    "type": "Element",
                                    "max_occurs": 100,
                                },
                            )

                            @dataclass(kw_only=True)
                            class DetBcn:
                                """
                                :ivar codBCN: Código identificador da base de
                                    cálculo negativa, conforme [[Tabela 12 –
                                    Códigos de Bases de Cálculo]].
                                :ivar perOrigem: Período de origem da base de
                                    cálculo negativa. Máscara: AAAA-MM
                                :ivar vOrigemIni: Valor inicial da base de
                                    cálculo negativa no respectivo período de
                                    origem.
                                :ivar vSaldoAnt: Valor da base de cálculo
                                    negativa disponível para uso neste período de
                                    apuração. Cálculo: SE {perOrigem} =
                                    {perApur}, ENTÃO {vSaldoAnt} = [0.00], SENÃO
                                    {vSaldoAnt} = {vSaldoFinal} do {perApur}
                                    imediatamente anterior.
                                :ivar vUtilPer: Valor da base de cálculo negativa
                                    utilizada neste período de apuração.
                                :ivar vSaldoFinal: Saldo remanescente desta base
                                    de cálculo negativa para os próximos períodos
                                    de apuração.
                                """

                                codBCN: str = field(
                                    metadata={
                                        "type": "Element",
                                        "length": 13,
                                        "white_space": "preserve",
                                        "pattern": r"[1-9][0-9]{3}[IC][0-9]{8}",
                                    }
                                )
                                perOrigem: str = field(
                                    metadata={
                                        "type": "Element",
                                        "length": 7,
                                        "white_space": "preserve",
                                        "pattern": r"20[0-9]{2}-(0[1-9]|1[0-2])",
                                    }
                                )
                                vOrigemIni: str = field(
                                    metadata={
                                        "type": "Element",
                                        "min_length": 4,
                                        "max_length": 18,
                                        "white_space": "preserve",
                                        "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                                    }
                                )
                                vSaldoAnt: str = field(
                                    metadata={
                                        "type": "Element",
                                        "min_length": 4,
                                        "max_length": 18,
                                        "white_space": "preserve",
                                        "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                                    }
                                )
                                vUtilPer: str = field(
                                    metadata={
                                        "type": "Element",
                                        "min_length": 4,
                                        "max_length": 18,
                                        "white_space": "preserve",
                                        "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                                    }
                                )
                                vSaldoFinal: str = field(
                                    metadata={
                                        "type": "Element",
                                        "min_length": 4,
                                        "max_length": 18,
                                        "white_space": "preserve",
                                        "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                                    }
                                )

                        @dataclass(kw_only=True)
                        class GBcncbs:
                            """
                            :ivar codBCNRaiz: Código identificador raiz da base
                                de cálculo negativa, conforme [[Tabela 12 –
                                Códigos de Bases de Cálculo]].
                            :ivar vSaldoAnt: Valor do saldo anterior. Montante
                                acumulado da base de cálculo negativa disponível
                                no início do período de apuração atual, antes das
                                compensações do mês.
                            :ivar vUtilPer: Valor da base de cálculo negativa
                                utilizado como dedução da base de cálculo do
                                período de apuração atual. Cálculo: Igual a
                                {vDedBCN}
                            :ivar vSaldoFinal: Valor do saldo remanescente de
                                base de cálculo negativa a ser transportado para
                                o próximo período de apuração. Cálculo:
                                {vSaldoAnt} - {vUtilPer} + {vBCNCBS} (se houver)
                            :ivar qtdOrigens: Quantidade de períodos de origem.
                                Indica quantos períodos distintos compõem o saldo
                                atual. Exemplo: Se o saldo é composto por bases
                                negativas de jan/25 e mar/26, {qtdOrigens} = [2].
                            :ivar detBCN: Detalhamento da composição do saldo por
                                período de origem.
                            """

                            codBCNRaiz: str = field(
                                metadata={
                                    "type": "Element",
                                    "length": 5,
                                    "white_space": "preserve",
                                    "pattern": r"[1-9][0-9]{3}[IC]",
                                }
                            )
                            vSaldoAnt: str = field(
                                metadata={
                                    "type": "Element",
                                    "min_length": 4,
                                    "max_length": 18,
                                    "white_space": "preserve",
                                    "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                                }
                            )
                            vUtilPer: str = field(
                                metadata={
                                    "type": "Element",
                                    "min_length": 4,
                                    "max_length": 18,
                                    "white_space": "preserve",
                                    "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                                }
                            )
                            vSaldoFinal: str = field(
                                metadata={
                                    "type": "Element",
                                    "min_length": 4,
                                    "max_length": 18,
                                    "white_space": "preserve",
                                    "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                                }
                            )
                            qtdOrigens: str = field(
                                metadata={
                                    "type": "Element",
                                    "max_length": 2,
                                    "white_space": "preserve",
                                    "pattern": r"[1-9][0-9]?",
                                }
                            )
                            detBCN: list[
                                DeRe.EvtRetornoMensal.InfoEvento.InfoTotSaude.DetBc.InfoBcn.GBcncbs.DetBcn
                            ] = field(
                                default_factory=list,
                                metadata={
                                    "type": "Element",
                                    "max_occurs": 100,
                                },
                            )

                            @dataclass(kw_only=True)
                            class DetBcn:
                                """
                                :ivar codBCN: Código identificador da base de
                                    cálculo negativa, conforme [[Tabela 12 –
                                    Códigos de Bases de Cálculo]].
                                :ivar perOrigem: Período de origem da base de
                                    cálculo negativa. Máscara: AAAA-MM
                                :ivar vOrigemIni: Valor inicial da base de
                                    cálculo negativa no respectivo período de
                                    origem.
                                :ivar vSaldoAnt: Valor da base de cálculo
                                    negativa disponível para uso neste período de
                                    apuração. Cálculo: SE {perOrigem} =
                                    {perApur}, ENTÃO {vSaldoAnt} = [0.00], SENÃO
                                    {vSaldoAnt} = {vSaldoFinal} do {perApur}
                                    imediatamente anterior.
                                :ivar vUtilPer: Valor da base de cálculo negativa
                                    utilizada neste período de apuração.
                                :ivar vSaldoFinal: Saldo remanescente desta base
                                    de cálculo negativa para os próximos períodos
                                    de apuração.
                                """

                                codBCN: str = field(
                                    metadata={
                                        "type": "Element",
                                        "length": 13,
                                        "white_space": "preserve",
                                        "pattern": r"[1-9][0-9]{3}[IC][0-9]{8}",
                                    }
                                )
                                perOrigem: str = field(
                                    metadata={
                                        "type": "Element",
                                        "length": 7,
                                        "white_space": "preserve",
                                        "pattern": r"20[0-9]{2}-(0[1-9]|1[0-2])",
                                    }
                                )
                                vOrigemIni: str = field(
                                    metadata={
                                        "type": "Element",
                                        "min_length": 4,
                                        "max_length": 18,
                                        "white_space": "preserve",
                                        "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                                    }
                                )
                                vSaldoAnt: str = field(
                                    metadata={
                                        "type": "Element",
                                        "min_length": 4,
                                        "max_length": 18,
                                        "white_space": "preserve",
                                        "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                                    }
                                )
                                vUtilPer: str = field(
                                    metadata={
                                        "type": "Element",
                                        "min_length": 4,
                                        "max_length": 18,
                                        "white_space": "preserve",
                                        "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                                    }
                                )
                                vSaldoFinal: str = field(
                                    metadata={
                                        "type": "Element",
                                        "min_length": 4,
                                        "max_length": 18,
                                        "white_space": "preserve",
                                        "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                                    }
                                )

                @dataclass(kw_only=True)
                class TotalTributos:
                    """
                    :ivar vIBSMun: Valor do IBS municipal Cálculo:
                        SOMA({infoTotSaude.detBC.vIBSMun})
                    :ivar vIBSUF: Valor do IBS estadual. Cálculo:
                        SOMA({infoTotSaude.detBC.vIBSUF})
                    :ivar vIBSTot: Valor total do IBS. Cálculo:
                        {totalTributos.vIBSMun} + {totalTributos.vIBSUF}
                    :ivar vCBS: Valor da CBS. Cálculo:
                        SOMA({infoTotSaude.detBC.vCBS})
                    """

                    vIBSMun: str = field(
                        metadata={
                            "type": "Element",
                            "min_length": 4,
                            "max_length": 18,
                            "white_space": "preserve",
                            "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                        }
                    )
                    vIBSUF: str = field(
                        metadata={
                            "type": "Element",
                            "min_length": 4,
                            "max_length": 18,
                            "white_space": "preserve",
                            "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                        }
                    )
                    vIBSTot: str = field(
                        metadata={
                            "type": "Element",
                            "min_length": 4,
                            "max_length": 18,
                            "white_space": "preserve",
                            "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                        }
                    )
                    vCBS: str = field(
                        metadata={
                            "type": "Element",
                            "min_length": 4,
                            "max_length": 18,
                            "white_space": "preserve",
                            "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                        }
                    )

            @dataclass(kw_only=True)
            class InfoTotProg:
                """
                :ivar detBC: Detalhamento da base de cálculo.
                :ivar totalTributos: Totalização dos tributos do Regime
                    Específico de Concursos de Prognósticos.
                """

                detBC: list[DeRe.EvtRetornoMensal.InfoEvento.InfoTotProg.DetBc] = field(
                    default_factory=list,
                    metadata={
                        "type": "Element",
                        "min_occurs": 1,
                        "max_occurs": 100,
                    },
                )
                totalTributos: DeRe.EvtRetornoMensal.InfoEvento.InfoTotProg.TotalTributos = field(
                    metadata={
                        "type": "Element",
                    }
                )

                @dataclass(kw_only=True)
                class DetBc:
                    """
                    :ivar codBC: Código identificador da base de cálculo,
                        conforme [[Tabela 12 – Códigos de Bases de Cálculo]].
                    :ivar xDetBC: Descrição da base de cálculo.
                    :ivar gCoeficientes: Grupo de detalhamento dos coeficientes
                        de rateio e de reversão calculados pelo sistema para a
                        formação desta base de cálculo.
                    :ivar memoriaCalculo: Descrição textual dos valores
                        intermediários usados no cálculo. Todos os valores
                        apresentados serão arredondados para oito casas decimais.
                    :ivar gBCIBS: Detalhamento da base de cálculo do IBS.
                    :ivar gBCCBS: Detalhamento da base de cálculo da CBS.
                    :ivar gBCIS: Detalhamento da base de cálculo do IS.
                    :ivar infoBCN: Grupo de informações de bases de cálculo
                        negativas.
                    """

                    codBC: str = field(
                        metadata={
                            "type": "Element",
                            "length": 4,
                            "white_space": "preserve",
                            "pattern": r"[1-9][0-9A-Z]{3}",
                        }
                    )
                    xDetBC: str = field(
                        metadata={
                            "type": "Element",
                            "max_length": 1024,
                            "white_space": "preserve",
                            "pattern": r"([!-ÿ][ -ÿ]*[!-ÿ]|[!-ÿ])",
                        }
                    )
                    gCoeficientes: (
                        None
                        | DeRe.EvtRetornoMensal.InfoEvento.InfoTotProg.DetBc.GCoeficientes
                    ) = field(
                        default=None,
                        metadata={
                            "type": "Element",
                        },
                    )
                    memoriaCalculo: str = field(
                        metadata={
                            "type": "Element",
                            "max_length": 4096,
                            "white_space": "preserve",
                            "pattern": r"([!-ÿ][ -ÿ]*[!-ÿ]|[!-ÿ])",
                        }
                    )
                    gBCIBS: DeRe.EvtRetornoMensal.InfoEvento.InfoTotProg.DetBc.GBcibs = field(
                        metadata={
                            "type": "Element",
                        }
                    )
                    gBCCBS: DeRe.EvtRetornoMensal.InfoEvento.InfoTotProg.DetBc.GBccbs = field(
                        metadata={
                            "type": "Element",
                        }
                    )
                    gBCIS: DeRe.EvtRetornoMensal.InfoEvento.InfoTotProg.DetBc.GBcis = (
                        field(
                            metadata={
                                "type": "Element",
                            }
                        )
                    )
                    infoBCN: (
                        None
                        | DeRe.EvtRetornoMensal.InfoEvento.InfoTotProg.DetBc.InfoBcn
                    ) = field(
                        default=None,
                        metadata={
                            "type": "Element",
                        },
                    )

                    @dataclass(kw_only=True)
                    class GCoeficientes:
                        """
                        :ivar pExportProg: Coeficiente aplicado para reverter
                            deduções de despesas vinculadas a receitas de
                            exportação das atividades previstas no art. 244 da LC
                            214/2025.
                        """

                        pExportProg: None | str = field(
                            default=None,
                            metadata={
                                "type": "Element",
                                "min_length": 10,
                                "max_length": 12,
                                "white_space": "preserve",
                                "pattern": r"(0|[1-9][0-9]{0,2})\.[0-9]{8}",
                            },
                        )

                    @dataclass(kw_only=True)
                    class GBcibs:
                        """
                        :ivar vBCIBS: Valor da base de cálculo do IBS. Cálculo:
                            SE {tabCodBC.vBCIBS} &gt;= [0.00], ENTÃO {vBCIBS} =
                            {tabCodBC.vBCIBS}, SENÃO {vBCIBS} = [0.00]
                        :ivar vBCNIBS: Valor absoluto do prejuízo (base de
                            cálculo negativa do IBS) gerado na apuração do
                            período corrente. Preenchimento: Este campo é
                            informado exclusivamente caso o resultado do cálculo
                            resulte em uma base de cálculo negativa
                            ({tabCodBC.vBCIBS} &lt; [0.00]). O valor é
                            apresentado em módulo. Cálculo: {vBCNIBS} =
                            {tabCodBC.vBCIBS} * (-1)
                        :ivar vDedBCN: Valor da base de cálculo negativa relativa
                            a período de apuração anterior a deduzir nesta
                            competência. Preenchimento: 1. SE o grupo
                            {D-1199.gUtilizBCN} não for informado, OU SE o campo
                            {D-1199.usarBCNAcum} correspondente for igual a [0]
                            (Opção por NÃO efetuar o aproveitamento de bases
                            negativas neste período), ENTÃO o campo {vDedBCN} não
                            será retornado; 2. SE o campo {D-1199.usarBCNAcum}
                            for igual a [1], o preenchimento observará o método
                            indicado pelo declarante: a. Método PEPS Automático
                            ({D-1199.metodoAproveit} = [0]): O valor de {vDedBCN}
                            será calculado automaticamente pelo sistema DeRE,
                            consumindo os saldos de bases negativas mais antigos
                            da {codBCNRaiz} correspondente até o limite da base
                            de cálculo positiva do mês corrente; b. Método Manual
                            ({D-1199.metodoAproveit} = [1]): O valor de {vDedBCN}
                            corresponderá ao somatório dos valores informados no
                            campo {D-1199.vUsarBCN} dentro do grupo
                            {D-1199.detBCNeg} para os códigos {D-1199.codBCN}
                            correspondentes. Validação: O valor de {vDedBCN} deve
                            ser menor ou igual a {vBCIBS}. Caso ultrapasse, o
                            valor de {vDedBCN} fica limitado ao valor da
                            {vBCIBS}, ajustando o valor utilizado na tabela de
                            bases de cálculo negativas.
                        :ivar vBCApurIBS: Base de cálculo efetiva do IBS após
                            compensação de saldos de base de cálculo negativas de
                            períodos anteriores. Cálculo: SE {vBCIBS} = [0.00],
                            ENTÃO {vBCApurIBS} = [0.00], SENÃO {vBCApurIBS} =
                            {vBCIBS} - {vDedBCN}
                        :ivar pIBSMun: Alíquota do IBS municipal. Sem símbolo
                            (%).
                        :ivar vIBSMun: Valor do IBS municipal. Cálculo:
                            {vBCApurIBS} * ({pIBSMun} / 100)
                        :ivar pIBSUF: Alíquota do IBS estadual. Sem símbolo (%).
                        :ivar vIBSUF: Valor do IBS estadual. Cálculo:
                            {vBCApurIBS} * ({pIBSUF} / 100)
                        :ivar pIBS: Soma das alíquotas {pIBSMun} e {pIBSUF}. Sem
                            símbolo (%).
                        :ivar vIBSTot: Valor total do IBS. Cálculo: {vIBSMun} +
                            {vIBSUF}
                        """

                        vBCIBS: str = field(
                            metadata={
                                "type": "Element",
                                "min_length": 4,
                                "max_length": 18,
                                "white_space": "preserve",
                                "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                            }
                        )
                        vBCNIBS: None | str = field(
                            default=None,
                            metadata={
                                "type": "Element",
                                "min_length": 4,
                                "max_length": 18,
                                "white_space": "preserve",
                                "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                            },
                        )
                        vDedBCN: None | str = field(
                            default=None,
                            metadata={
                                "type": "Element",
                                "min_length": 4,
                                "max_length": 18,
                                "white_space": "preserve",
                                "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                            },
                        )
                        vBCApurIBS: str = field(
                            metadata={
                                "type": "Element",
                                "min_length": 4,
                                "max_length": 18,
                                "white_space": "preserve",
                                "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                            }
                        )
                        pIBSMun: str = field(
                            metadata={
                                "type": "Element",
                                "min_length": 8,
                                "max_length": 10,
                                "white_space": "preserve",
                                "pattern": r"(0|[1-9][0-9]{0,2})\.[0-9]{6}",
                            }
                        )
                        vIBSMun: str = field(
                            metadata={
                                "type": "Element",
                                "min_length": 4,
                                "max_length": 18,
                                "white_space": "preserve",
                                "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                            }
                        )
                        pIBSUF: str = field(
                            metadata={
                                "type": "Element",
                                "min_length": 8,
                                "max_length": 10,
                                "white_space": "preserve",
                                "pattern": r"(0|[1-9][0-9]{0,2})\.[0-9]{6}",
                            }
                        )
                        vIBSUF: str = field(
                            metadata={
                                "type": "Element",
                                "min_length": 4,
                                "max_length": 18,
                                "white_space": "preserve",
                                "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                            }
                        )
                        pIBS: str = field(
                            metadata={
                                "type": "Element",
                                "min_length": 8,
                                "max_length": 10,
                                "white_space": "preserve",
                                "pattern": r"(0|[1-9][0-9]{0,2})\.[0-9]{6}",
                            }
                        )
                        vIBSTot: str = field(
                            metadata={
                                "type": "Element",
                                "min_length": 4,
                                "max_length": 18,
                                "white_space": "preserve",
                                "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                            }
                        )

                    @dataclass(kw_only=True)
                    class GBccbs:
                        """
                        :ivar vBCCBS: Valor da base de cálculo da CBS. Cálculo:
                            SE {tabCodBC.vBCCBS} &gt;= [0.00], ENTÃO {vBCCBS} =
                            {tabCodBC.vBCCBS}, SENÃO {vBCCBS} = [0.00]
                        :ivar vBCNCBS: Valor absoluto da base de cálculo negativa
                            da CBS gerado na apuração do período corrente.
                            Preenchimento: Este campo é informado exclusivamente
                            caso o resultado do cálculo resulte em uma base de
                            cálculo negativa ({tabCodBC.vBCCBS} &lt; [0.00]). O
                            valor é apresentado em módulo. Cálculo: {vBCNCBS} =
                            {tabCodBC.vBCCBS} * (-1)
                        :ivar vDedBCN: Valor da base de cálculo negativa relativa
                            a período de apuração anterior a deduzir nesta
                            competência. Preenchimento: 1. SE o grupo
                            {D-1199.gUtilizBCN} não for informado, OU SE o campo
                            {D-1199.usarBCNAcum} correspondente for igual a [0]
                            (Opção por NÃO efetuar o aproveitamento de bases
                            negativas neste período), ENTÃO o campo {vDedBCN} não
                            será retornado; 2. SE o campo {D-1199.usarBCNAcum}
                            for igual a [1], o preenchimento observará o método
                            indicado pelo declarante: a. Método PEPS Automático
                            ({D-1199.metodoAproveit} = [0]): O valor de {vDedBCN}
                            será calculado automaticamente pelo sistema DeRE,
                            consumindo os saldos de bases negativas mais antigos
                            da {codBCNRaiz} correspondente até o limite da base
                            de cálculo positiva do mês corrente; b. Método Manual
                            ({D-1199.metodoAproveit} = [1]): O valor de {vDedBCN}
                            corresponderá ao somatório dos valores informados no
                            campo {D-1199.vUsarBCN} dentro do grupo
                            {D-1199.detBCNeg} para os códigos {D-1199.codBCN}
                            correspondentes. Validação: O valor de {vDedBCN} deve
                            ser menor ou igual a {vBCCBS}. Caso ultrapasse, o
                            valor de {vDedBCN} fica limitado ao valor da
                            {vBCCBS}, ajustando o valor utilizado na tabela de
                            bases de cálculo negativas.
                        :ivar vBCApurCBS: Base de cálculo efetiva da CBS após
                            compensação de saldos de base de cálculo negativas de
                            períodos anteriores. Cálculo: SE {vBCCBS} = [0.00],
                            ENTÃO {vBCApurCBS} = [0.00], SENÃO {vBCApurCBS} =
                            {vBCCBS} - {vDedBCN}
                        :ivar pCBS: Alíquota da CBS. Sem símbolo (%).
                        :ivar vCBS: Valor da CBS. Cálculo: {vBCApurCBS} * ({pCBS}
                            / 100)
                        """

                        vBCCBS: str = field(
                            metadata={
                                "type": "Element",
                                "min_length": 4,
                                "max_length": 18,
                                "white_space": "preserve",
                                "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                            }
                        )
                        vBCNCBS: None | str = field(
                            default=None,
                            metadata={
                                "type": "Element",
                                "min_length": 4,
                                "max_length": 18,
                                "white_space": "preserve",
                                "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                            },
                        )
                        vDedBCN: None | str = field(
                            default=None,
                            metadata={
                                "type": "Element",
                                "min_length": 4,
                                "max_length": 18,
                                "white_space": "preserve",
                                "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                            },
                        )
                        vBCApurCBS: str = field(
                            metadata={
                                "type": "Element",
                                "min_length": 4,
                                "max_length": 18,
                                "white_space": "preserve",
                                "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                            }
                        )
                        pCBS: str = field(
                            metadata={
                                "type": "Element",
                                "min_length": 8,
                                "max_length": 10,
                                "white_space": "preserve",
                                "pattern": r"(0|[1-9][0-9]{0,2})\.[0-9]{6}",
                            }
                        )
                        vCBS: str = field(
                            metadata={
                                "type": "Element",
                                "min_length": 4,
                                "max_length": 18,
                                "white_space": "preserve",
                                "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                            }
                        )

                    @dataclass(kw_only=True)
                    class GBcis:
                        """
                        :ivar vBCIS: Valor da base de cálculo do Imposto Seletivo
                            (IS). Cálculo: SE {tabCodBC.vBCIS} &gt;= [0.00],
                            ENTÃO {vBCIS} = {tabCodBC.vBCIS}, SENÃO {vBCIS} =
                            [0.00]
                        :ivar vBCApurIS: Valor da base de cálculo efetiva do
                            Imposto Seletivo. Cálculo: {vBCApurIS} = {vBCIS}
                        :ivar pIS: Alíquota do Imposto Seletivo do Regime
                            Específico de Concursos de Prognósticos. Sem símbolo
                            (%).
                        :ivar vIS: Valor do Imposto Seletivo. Cálculo:
                            {vBCApurIS} * ({pIS} / 100)
                        """

                        vBCIS: str = field(
                            metadata={
                                "type": "Element",
                                "min_length": 4,
                                "max_length": 18,
                                "white_space": "preserve",
                                "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                            }
                        )
                        vBCApurIS: str = field(
                            metadata={
                                "type": "Element",
                                "min_length": 4,
                                "max_length": 18,
                                "white_space": "preserve",
                                "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                            }
                        )
                        pIS: str = field(
                            metadata={
                                "type": "Element",
                                "min_length": 8,
                                "max_length": 10,
                                "white_space": "preserve",
                                "pattern": r"(0|[1-9][0-9]{0,2})\.[0-9]{6}",
                            }
                        )
                        vIS: str = field(
                            metadata={
                                "type": "Element",
                                "min_length": 4,
                                "max_length": 18,
                                "white_space": "preserve",
                                "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                            }
                        )

                    @dataclass(kw_only=True)
                    class InfoBcn:
                        """
                        :ivar gBCNIBS: Grupo de detalhamento de bases de cálculo
                            negativas de IBS.
                        :ivar gBCNCBS: Grupo de detalhamento de bases de cálculo
                            negativas de CBS.
                        """

                        gBCNIBS: DeRe.EvtRetornoMensal.InfoEvento.InfoTotProg.DetBc.InfoBcn.GBcnibs = field(
                            metadata={
                                "type": "Element",
                            }
                        )
                        gBCNCBS: DeRe.EvtRetornoMensal.InfoEvento.InfoTotProg.DetBc.InfoBcn.GBcncbs = field(
                            metadata={
                                "type": "Element",
                            }
                        )

                        @dataclass(kw_only=True)
                        class GBcnibs:
                            """
                            :ivar codBCNRaiz: Código identificador raiz da base
                                de cálculo negativa, conforme [[Tabela 12 –
                                Códigos de Bases de Cálculo]].
                            :ivar vSaldoAnt: Valor do saldo anterior. Montante
                                acumulado da base de cálculo negativa disponível
                                no início do período de apuração atual, antes das
                                compensações do mês.
                            :ivar vUtilPer: Valor da base de cálculo negativa
                                utilizado como dedução da base de cálculo do
                                período de apuração atual. Cálculo: Igual a
                                {vDedBCN}
                            :ivar vSaldoFinal: Valor do saldo remanescente de
                                base de cálculo negativa a ser transportado para
                                o próximo período de apuração. Cálculo:
                                {vSaldoAnt} - {vUtilPer} + {vBCNIBS} (se houver)
                            :ivar qtdOrigens: Quantidade de períodos de origem.
                                Indica quantos períodos distintos compõem o saldo
                                atual. Exemplo: Se o saldo é composto por bases
                                negativas de jan/25 e mar/26, {qtdOrigens} = [2].
                            :ivar detBCN: Detalhamento da composição do saldo por
                                período de origem.
                            """

                            codBCNRaiz: str = field(
                                metadata={
                                    "type": "Element",
                                    "length": 5,
                                    "white_space": "preserve",
                                    "pattern": r"[1-9][0-9]{3}[IC]",
                                }
                            )
                            vSaldoAnt: str = field(
                                metadata={
                                    "type": "Element",
                                    "min_length": 4,
                                    "max_length": 18,
                                    "white_space": "preserve",
                                    "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                                }
                            )
                            vUtilPer: str = field(
                                metadata={
                                    "type": "Element",
                                    "min_length": 4,
                                    "max_length": 18,
                                    "white_space": "preserve",
                                    "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                                }
                            )
                            vSaldoFinal: str = field(
                                metadata={
                                    "type": "Element",
                                    "min_length": 4,
                                    "max_length": 18,
                                    "white_space": "preserve",
                                    "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                                }
                            )
                            qtdOrigens: str = field(
                                metadata={
                                    "type": "Element",
                                    "max_length": 2,
                                    "white_space": "preserve",
                                    "pattern": r"[1-9][0-9]?",
                                }
                            )
                            detBCN: list[
                                DeRe.EvtRetornoMensal.InfoEvento.InfoTotProg.DetBc.InfoBcn.GBcnibs.DetBcn
                            ] = field(
                                default_factory=list,
                                metadata={
                                    "type": "Element",
                                    "max_occurs": 100,
                                },
                            )

                            @dataclass(kw_only=True)
                            class DetBcn:
                                """
                                :ivar codBCN: Código identificador da base de
                                    cálculo negativa, conforme [[Tabela 12 –
                                    Códigos de Bases de Cálculo]].
                                :ivar perOrigem: Período de origem da base de
                                    cálculo negativa. Máscara: AAAA-MM
                                :ivar vOrigemIni: Valor inicial da base de
                                    cálculo negativa no respectivo período de
                                    origem.
                                :ivar vSaldoAnt: Valor da base de cálculo
                                    negativa disponível para uso neste período de
                                    apuração. Cálculo: SE {perOrigem} =
                                    {perApur}, ENTÃO {vSaldoAnt} = [0.00], SENÃO
                                    {vSaldoAnt} = {vSaldoFinal} do {perApur}
                                    imediatamente anterior.
                                :ivar vUtilPer: Valor da base de cálculo negativa
                                    utilizada neste período de apuração.
                                :ivar vSaldoFinal: Saldo remanescente desta base
                                    de cálculo negativa para os próximos períodos
                                    de apuração.
                                """

                                codBCN: str = field(
                                    metadata={
                                        "type": "Element",
                                        "length": 13,
                                        "white_space": "preserve",
                                        "pattern": r"[1-9][0-9]{3}[IC][0-9]{8}",
                                    }
                                )
                                perOrigem: str = field(
                                    metadata={
                                        "type": "Element",
                                        "length": 7,
                                        "white_space": "preserve",
                                        "pattern": r"20[0-9]{2}-(0[1-9]|1[0-2])",
                                    }
                                )
                                vOrigemIni: str = field(
                                    metadata={
                                        "type": "Element",
                                        "min_length": 4,
                                        "max_length": 18,
                                        "white_space": "preserve",
                                        "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                                    }
                                )
                                vSaldoAnt: str = field(
                                    metadata={
                                        "type": "Element",
                                        "min_length": 4,
                                        "max_length": 18,
                                        "white_space": "preserve",
                                        "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                                    }
                                )
                                vUtilPer: str = field(
                                    metadata={
                                        "type": "Element",
                                        "min_length": 4,
                                        "max_length": 18,
                                        "white_space": "preserve",
                                        "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                                    }
                                )
                                vSaldoFinal: str = field(
                                    metadata={
                                        "type": "Element",
                                        "min_length": 4,
                                        "max_length": 18,
                                        "white_space": "preserve",
                                        "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                                    }
                                )

                        @dataclass(kw_only=True)
                        class GBcncbs:
                            """
                            :ivar codBCNRaiz: Código identificador raiz da base
                                de cálculo negativa, conforme [[Tabela 12 –
                                Códigos de Bases de Cálculo]].
                            :ivar vSaldoAnt: Valor do saldo anterior. Montante
                                acumulado da base de cálculo negativa disponível
                                no início do período de apuração atual, antes das
                                compensações do mês.
                            :ivar vUtilPer: Valor da base de cálculo negativa
                                utilizado como dedução da base de cálculo do
                                período de apuração atual. Cálculo: Igual a
                                {vDedBCN}
                            :ivar vSaldoFinal: Valor do saldo remanescente de
                                base de cálculo negativa a ser transportado para
                                o próximo período de apuração. Cálculo:
                                {vSaldoAnt} - {vUtilPer} + {vBCNCBS} (se houver)
                            :ivar qtdOrigens: Quantidade de períodos de origem.
                                Indica quantos períodos distintos compõem o saldo
                                atual. Exemplo: Se o saldo é composto por bases
                                negativas de jan/25 e mar/26, {qtdOrigens} = [2].
                            :ivar detBCN: Detalhamento da composição do saldo por
                                período de origem.
                            """

                            codBCNRaiz: str = field(
                                metadata={
                                    "type": "Element",
                                    "length": 5,
                                    "white_space": "preserve",
                                    "pattern": r"[1-9][0-9]{3}[IC]",
                                }
                            )
                            vSaldoAnt: str = field(
                                metadata={
                                    "type": "Element",
                                    "min_length": 4,
                                    "max_length": 18,
                                    "white_space": "preserve",
                                    "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                                }
                            )
                            vUtilPer: str = field(
                                metadata={
                                    "type": "Element",
                                    "min_length": 4,
                                    "max_length": 18,
                                    "white_space": "preserve",
                                    "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                                }
                            )
                            vSaldoFinal: str = field(
                                metadata={
                                    "type": "Element",
                                    "min_length": 4,
                                    "max_length": 18,
                                    "white_space": "preserve",
                                    "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                                }
                            )
                            qtdOrigens: str = field(
                                metadata={
                                    "type": "Element",
                                    "max_length": 2,
                                    "white_space": "preserve",
                                    "pattern": r"[1-9][0-9]?",
                                }
                            )
                            detBCN: list[
                                DeRe.EvtRetornoMensal.InfoEvento.InfoTotProg.DetBc.InfoBcn.GBcncbs.DetBcn
                            ] = field(
                                default_factory=list,
                                metadata={
                                    "type": "Element",
                                    "max_occurs": 100,
                                },
                            )

                            @dataclass(kw_only=True)
                            class DetBcn:
                                """
                                :ivar codBCN: Código identificador da base de
                                    cálculo negativa, conforme [[Tabela 12 –
                                    Códigos de Bases de Cálculo]].
                                :ivar perOrigem: Período de origem da base de
                                    cálculo negativa. Máscara: AAAA-MM
                                :ivar vOrigemIni: Valor inicial da base de
                                    cálculo negativa no respectivo período de
                                    origem.
                                :ivar vSaldoAnt: Valor da base de cálculo
                                    negativa disponível para uso neste período de
                                    apuração. Cálculo: SE {perOrigem} =
                                    {perApur}, ENTÃO {vSaldoAnt} = [0.00], SENÃO
                                    {vSaldoAnt} = {vSaldoFinal} do {perApur}
                                    imediatamente anterior.
                                :ivar vUtilPer: Valor da base de cálculo negativa
                                    utilizada neste período de apuração.
                                :ivar vSaldoFinal: Saldo remanescente desta base
                                    de cálculo negativa para os próximos períodos
                                    de apuração.
                                """

                                codBCN: str = field(
                                    metadata={
                                        "type": "Element",
                                        "length": 13,
                                        "white_space": "preserve",
                                        "pattern": r"[1-9][0-9]{3}[IC][0-9]{8}",
                                    }
                                )
                                perOrigem: str = field(
                                    metadata={
                                        "type": "Element",
                                        "length": 7,
                                        "white_space": "preserve",
                                        "pattern": r"20[0-9]{2}-(0[1-9]|1[0-2])",
                                    }
                                )
                                vOrigemIni: str = field(
                                    metadata={
                                        "type": "Element",
                                        "min_length": 4,
                                        "max_length": 18,
                                        "white_space": "preserve",
                                        "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                                    }
                                )
                                vSaldoAnt: str = field(
                                    metadata={
                                        "type": "Element",
                                        "min_length": 4,
                                        "max_length": 18,
                                        "white_space": "preserve",
                                        "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                                    }
                                )
                                vUtilPer: str = field(
                                    metadata={
                                        "type": "Element",
                                        "min_length": 4,
                                        "max_length": 18,
                                        "white_space": "preserve",
                                        "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                                    }
                                )
                                vSaldoFinal: str = field(
                                    metadata={
                                        "type": "Element",
                                        "min_length": 4,
                                        "max_length": 18,
                                        "white_space": "preserve",
                                        "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                                    }
                                )

                @dataclass(kw_only=True)
                class TotalTributos:
                    """
                    :ivar vIS: Valor do Imposto Seletivo (IS). Cálculo:
                        SOMA({infoTotProg.detBC.vIS})
                    :ivar vIBSMun: Valor do IBS municipal. Cálculo:
                        SOMA({infoTotProg.detBC.vIBSMun})
                    :ivar vIBSUF: Valor do IBS estadual. Cálculo:
                        SOMA({infoTotProg.detBC.vIBSUF})
                    :ivar vIBSTot: Valor total do IBS. Cálculo:
                        {totalTributos.vIBSMun} + {totalTributos.vIBSUF}
                    :ivar vCBS: Valor da CBS. Cálculo:
                        SOMA({infoTotProg.detBC.vCBS})
                    """

                    vIS: str = field(
                        metadata={
                            "type": "Element",
                            "min_length": 4,
                            "max_length": 18,
                            "white_space": "preserve",
                            "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                        }
                    )
                    vIBSMun: str = field(
                        metadata={
                            "type": "Element",
                            "min_length": 4,
                            "max_length": 18,
                            "white_space": "preserve",
                            "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                        }
                    )
                    vIBSUF: str = field(
                        metadata={
                            "type": "Element",
                            "min_length": 4,
                            "max_length": 18,
                            "white_space": "preserve",
                            "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                        }
                    )
                    vIBSTot: str = field(
                        metadata={
                            "type": "Element",
                            "min_length": 4,
                            "max_length": 18,
                            "white_space": "preserve",
                            "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                        }
                    )
                    vCBS: str = field(
                        metadata={
                            "type": "Element",
                            "min_length": 4,
                            "max_length": 18,
                            "white_space": "preserve",
                            "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                        }
                    )

            @dataclass(kw_only=True)
            class TotalTributosGeral:
                """
                :ivar vIS: Valor total do Imposto Seletivo (IS). Preenchimento:
                    Corresponde ao campo {vIS} do grupo {totalTributos} do grupo
                    {infoTotProg}. Cálculo: SOMA({totalTributos.vIS})
                :ivar vIBSMun: Valor total do IBS municipal. Preenchimento: Soma
                    do campo {vIBSMun} de todas as ocorrências do grupo
                    {totalTributos} dos grupos {infoTotFinanc}, {infoTotSaude} e
                    {infoTotProg}. Cálculo: SOMA({totalTributos.vIBSMun})
                :ivar vIBSUF: Valor total do IBS estadual. Preenchimento: Soma do
                    campo {vIBSUF} de todas as ocorrências do grupo
                    {totalTributos} dos grupos {infoTotFinanc}, {infoTotSaude} e
                    {infoTotProg}. Cálculo: SOMA({totalTributos.vIBSUF})
                :ivar vIBSTot: Valor total do IBS. Cálculo:
                    SOMA({totalTributosGeral.vIBSMun}) +
                    SOMA({totalTributosGeral.vIBSUF})
                :ivar vCBS: Valor total da CBS. Preenchimento: Soma do campo
                    {vCBS} de todas as ocorrências do grupo {totalTributos} dos
                    grupos {infoTotFinanc}, {infoTotSaude} e {infoTotProg}.
                    Cálculo: SOMA({totalTributos.vCBS})
                """

                vIS: None | str = field(
                    default=None,
                    metadata={
                        "type": "Element",
                        "min_length": 4,
                        "max_length": 18,
                        "white_space": "preserve",
                        "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                    },
                )
                vIBSMun: str = field(
                    metadata={
                        "type": "Element",
                        "min_length": 4,
                        "max_length": 18,
                        "white_space": "preserve",
                        "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                    }
                )
                vIBSUF: str = field(
                    metadata={
                        "type": "Element",
                        "min_length": 4,
                        "max_length": 18,
                        "white_space": "preserve",
                        "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                    }
                )
                vIBSTot: str = field(
                    metadata={
                        "type": "Element",
                        "min_length": 4,
                        "max_length": 18,
                        "white_space": "preserve",
                        "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                    }
                )
                vCBS: str = field(
                    metadata={
                        "type": "Element",
                        "min_length": 4,
                        "max_length": 18,
                        "white_space": "preserve",
                        "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                    }
                )
