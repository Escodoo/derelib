from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from xsdata.models.datatype import XmlDate

from derelib.bindings.v1_2_0.xmldsig_core_schema import Signature
from derelib.mixin import DereMixin

__NAMESPACE__ = "http://www.dere.gov.br/schemas/evtPGCC/v1_0_3"


class IdeEventoAplicEmi(Enum):
    """
    :cvar VALUE_1: Emissão com aplicativo da empresa
    :cvar VALUE_2: Aplicativo Governamental
    """

    VALUE_1 = 1
    VALUE_2 = 2


class IdeEventoMotExcl(Enum):
    """
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
    :cvar VALUE_1: Inclusão
    :cvar VALUE_2: Alteração
    :cvar VALUE_3: Exclusão
    """

    VALUE_1 = 1
    VALUE_2 = 2
    VALUE_3 = 3


class InfoContaCodNat(Enum):
    """
    :cvar VALUE_1: Contas do Ativo
    :cvar VALUE_2: Contas do Passivo
    :cvar VALUE_3: Contas do Patrimônio Líquido
    :cvar VALUE_4: Contas de receita
    :cvar VALUE_5: Contas de despesa
    """

    VALUE_1 = 1
    VALUE_2 = 2
    VALUE_3 = 3
    VALUE_4 = 4
    VALUE_5 = 5


class InfoContaIndCta(Enum):
    """
    :cvar S: Sintética
    :cvar A: Analítica
    """

    S = "S"
    A = "A"


class InfoContaIndTribIss(Enum):
    """
    :cvar VALUE_0: Não sujeita ao ISS
    :cvar VALUE_1: Sujeita ao ISS
    """

    VALUE_0 = 0
    VALUE_1 = 1


class InfoContaNatCta(Enum):
    """
    :cvar C: Credora
    :cvar D: Devedora
    :cvar V: Variável
    """

    C = "C"
    D = "D"
    V = "V"


class InfoPgccFreqEncerr(Enum):
    """
    :cvar A: Anual
    :cvar S: Semestral
    :cvar Q: Quadrimestral
    :cvar T: Trimestral
    :cvar B: Bimestral
    :cvar M: Mensal
    """

    A = "A"
    S = "S"
    Q = "Q"
    T = "T"
    B = "B"
    M = "M"


class InfoPgccPlanoCtaRef(Enum):
    """
    :cvar VALUE_1: COSIF
    :cvar VALUE_2: ANS
    :cvar VALUE_3: SUSEP
    :cvar VALUE_4: SPED
    :cvar VALUE_5: PREVIC
    """

    VALUE_1 = 1
    VALUE_2 = 2
    VALUE_3 = 3
    VALUE_4 = 4
    VALUE_5 = 5


@dataclass(kw_only=True)
class DeRe(DereMixin):
    """
    Envelope raiz dos eventos da DeRE.

    :ivar evtPGCC: Evento Plano Geral de Contas Comentado.
    :ivar signature:
    """

    class Meta:
        name = "DeRE"
        namespace = "http://www.dere.gov.br/schemas/evtPGCC/v1_0_3"

    evtPGCC: DeRe.EvtPgcc = field(
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
    class EvtPgcc:
        """
        :ivar ideEvento: Informações de identificação do evento.
        :ivar ideContrib: Informações de identificação do contribuinte.
        :ivar idePeriodo: Período de validade
        :ivar infoPGCC: Informações do plano geral de contas comentado.
        :ivar id: Identificador que representa unicamente o evento.
        """

        ideEvento: DeRe.EvtPgcc.IdeEvento = field(
            metadata={
                "type": "Element",
            }
        )
        ideContrib: DeRe.EvtPgcc.IdeContrib = field(
            metadata={
                "type": "Element",
            }
        )
        idePeriodo: DeRe.EvtPgcc.IdePeriodo = field(
            metadata={
                "type": "Element",
            }
        )
        infoPGCC: None | DeRe.EvtPgcc.InfoPgcc = field(
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
            """
            :ivar tpOper: Tipo de operação do evento.
            :ivar motExcl: Motivo da Exclusão. Código do motivo que justifica a
                exclusão do evento.
            :ivar nrProc: Informar o número do processo administrativo/judicial.
            :ivar tpAmb:
            :ivar aplicEmi: Identificação do aplicativo emissor do evento.
            :ivar verAplic: Versão do aplicativo emissor do evento.
            """

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
            """
            :ivar nrInsc: Número de inscrição do contribuinte (CNPJ raiz).
            """

            nrInsc: str = field(
                metadata={
                    "type": "Element",
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
            novaValidade: None | DeRe.EvtPgcc.IdePeriodo.NovaValidade = field(
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
        class InfoPgcc:
            """
            :ivar planoCtaRef: Identificação do Plano de Contas Referencial
                vinculado à atividade preponderante do contribuinte.
            :ivar freqEncerr: Indicador de frequência de encerramento contábil.
                Informa a periodicidade com que a entidade realiza o encerramento
                das contas de resultado (receitas e despesas) para apuração do
                resultado do exercício.
            :ivar infoContas: Lista de detalhamentos de informações de contas
                contábeis.
            """

            planoCtaRef: InfoPgccPlanoCtaRef = field(
                metadata={
                    "type": "Element",
                    "pattern": r"\d{1}",
                }
            )
            freqEncerr: InfoPgccFreqEncerr = field(
                metadata={
                    "type": "Element",
                    "length": 1,
                }
            )
            infoContas: DeRe.EvtPgcc.InfoPgcc.InfoContas = field(
                metadata={
                    "type": "Element",
                }
            )

            @dataclass(kw_only=True)
            class InfoContas:
                """
                :ivar infoConta: Detalhamento de informações da conta contábil.
                """

                infoConta: list[DeRe.EvtPgcc.InfoPgcc.InfoContas.InfoConta] = field(
                    default_factory=list,
                    metadata={
                        "type": "Element",
                        "min_occurs": 1,
                        "max_occurs": 150000,
                    },
                )

                @dataclass(kw_only=True)
                class InfoConta:
                    """
                    :ivar cCta: Código completo da conta. Resultante da
                        concatenação de {cCtaInterna} e {cDbrMista}.
                        Preenchimento: Informar apenas caracteres alfanuméricos,
                        sem pontos ou traços.
                    :ivar cCtaInterna: Código da conta contábil de acordo com o
                        Plano de Contas interno (Grupo, Subgrupo, Título e
                        Subtítulo). Preenchimento: Informar apenas caracteres
                        alfanuméricos, sem pontos ou traços. Nota: Devem ser
                        informadas todas as contas patrimoniais e de resultado.
                    :ivar cDbrMista: Desdobramento de conta mista. Preenchimento:
                        Se não houver desdobramento, informar [000]. Caso
                        contrário, sequencial de [001] a [999]. Nota: Havendo
                        conta mista, esta assume nível sintético [000] e seus
                        desdobramentos assumem nível analítico.
                    :ivar nomeCta: Nome da conta.
                    :ivar indCta: Indicador do tipo de conta (sintética ou
                        analítica).
                    :ivar descCta: Descrição detalhada da natureza das operações
                        contabilizadas na conta.
                    :ivar cCtaSup: Código da Conta hierárquica imediatamente
                        superior. Preenchimento: Informar apenas caracteres
                        alfanuméricos, sem pontos ou traços. A conta desdobrada
                        deve referenciar a mesma superior da conta mista.
                    :ivar cCtaRef: Código da conta do plano de contas
                        referencial, conforme opção selecionada no evento
                        Informações do Contribuinte. Preenchimento: Informar
                        apenas caracteres alfanuméricos, sem pontos ou traços.
                        Validação: O código deve existir na tabela correspondente
                        ao plano informado em {planoCtaRef}: Se [1] (COSIF):
                        Tabela 22 – Plano de Contas Referencial – COSIF Se [2]
                        (ANS): Tabela 32 – Plano de Contas Referencial – ANS Se
                        [3] (SUSEP): Tabela 23 – Plano de Contas Referencial –
                        SUSEP Se [4] (SPED): Tabela 14 – Plano de Contas
                        Referencial – SPED Se [5] (PREVIC): Tabela 24 – Plano de
                        Contas Referencial – PREVIC Caso o {cDbrMista} seja maior
                        que zero, o {cCtaRef} desta {cCta} deve ser igual ao
                        {cCtaRef} da {cCtaSup}
                    :ivar nivelCta: Nível hierárquico da conta.
                    :ivar natCta: Natureza da conta
                    :ivar codNat: Código da Natureza da Conta.
                    :ivar codTrib: Código de tributação para fins de IBS, CBS e
                        IS. Preenchimento: Informar apenas caracteres numéricos,
                        sem pontos ou traços.
                    :ivar indTribISS: Indicador de sujeição ou vinculação ao
                        ISSQN. Informa se os valores recebidos ou receitas
                        auferidas sofrem a incidência de ISSQN. Validação: Não
                        preencher se {indCta} = [S]
                    :ivar idLeiDisp: Código que identifica o fundamento legal
                        utilizado para embasar a destinação obrigatória de
                        recursos a órgãos/fundos públicos/demais beneficiários ou
                        a classificação tributária que exija comprovação legal
                        específica na escrituração. Máscara: CC-CC Nota: Regra de
                        preenchimento do campo a ser informada em futura versão
                        da DeRE.
                    :ivar iniVig:
                    :ivar fimVig:
                    """

                    cCta: str = field(
                        metadata={
                            "type": "Element",
                            "pattern": r"[0-9A-Za-z]{1,53}",
                        }
                    )
                    cCtaInterna: str = field(
                        metadata={
                            "type": "Element",
                            "pattern": r"[0-9A-Za-z]{1,50}",
                        }
                    )
                    cDbrMista: str = field(
                        metadata={
                            "type": "Element",
                            "length": 3,
                            "pattern": r"\d{3}",
                        }
                    )
                    nomeCta: str = field(
                        metadata={
                            "type": "Element",
                            "min_length": 1,
                            "max_length": 100,
                        }
                    )
                    indCta: InfoContaIndCta = field(
                        metadata={
                            "type": "Element",
                            "length": 1,
                        }
                    )
                    descCta: None | str = field(
                        default=None,
                        metadata={
                            "type": "Element",
                            "min_length": 1,
                            "max_length": 600,
                        },
                    )
                    cCtaSup: None | str = field(
                        default=None,
                        metadata={
                            "type": "Element",
                            "pattern": r"[0-9A-Za-z]{1,53}",
                        },
                    )
                    cCtaRef: str = field(
                        metadata={
                            "type": "Element",
                            "pattern": r"[0-9A-Za-z]{1,13}",
                        }
                    )
                    nivelCta: str = field(
                        metadata={
                            "type": "Element",
                            "pattern": r"[1-9][0-9]?",
                        }
                    )
                    natCta: InfoContaNatCta = field(
                        metadata={
                            "type": "Element",
                            "length": 1,
                        }
                    )
                    codNat: InfoContaCodNat = field(
                        metadata={
                            "type": "Element",
                            "pattern": r"\d{1}",
                        }
                    )
                    codTrib: None | int = field(
                        default=None,
                        metadata={
                            "type": "Element",
                            "min_inclusive": 1,
                            "max_inclusive": 999999999,
                        },
                    )
                    indTribISS: None | InfoContaIndTribIss = field(
                        default=None,
                        metadata={
                            "type": "Element",
                            "pattern": r"\d{1}",
                        },
                    )
                    idLeiDisp: None | str = field(
                        default=None,
                        metadata={
                            "type": "Element",
                            "length": 5,
                            "pattern": r"\d{2}\-\d{2}",
                        },
                    )
                    iniVig: XmlDate = field(
                        metadata={
                            "type": "Element",
                        }
                    )
                    fimVig: None | XmlDate = field(
                        default=None,
                        metadata={
                            "type": "Element",
                        },
                    )
