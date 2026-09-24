from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from derelib.bindings.v1_2_0.xmldsig_core_schema import Signature
from derelib.mixin import DereMixin

__NAMESPACE__ = "http://www.dere.gov.br/schemas/evtFechMensal/v0_0_2"


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


class InfoBcnMetodoAproveit(Enum):
    """
    :cvar VALUE_0: Método PEPS calculado automaticamente pelo sistema
    :cvar VALUE_1: Informação manual pelo contribuinte de valores de bases de
        cálculo negativas que deseja realizar o aproveitamento, com a informação
        dos respectivos períodos de origem
    """

    VALUE_0 = "0"
    VALUE_1 = "1"


class InfoBcnUsarBcnacum(Enum):
    """
    :cvar VALUE_0: Opção por NÃO efetuar o aproveitamento de bases negativas
        neste período
    :cvar VALUE_1: Opção por efetuar o aproveitamento de bases negativas neste
        período
    """

    VALUE_0 = "0"
    VALUE_1 = "1"


class InfoParamFechIndInexistDedu(Enum):
    """
    :cvar VALUE_1: Declaro que, embora sujeito à obrigatoriedade de entrega do
        evento D-1121, não possuo deduções a detalhar neste período
    """

    VALUE_1 = "1"


@dataclass(kw_only=True)
class DeRe(DereMixin):
    """
    Envelope raiz dos eventos da DeRE.

    :ivar evtFechMensal: Evento de Fechamento Mensal.
    :ivar signature:
    """

    class Meta:
        name = "DeRE"
        namespace = "http://www.dere.gov.br/schemas/evtFechMensal/v0_0_2"

    evtFechMensal: DeRe.EvtFechMensal = field(
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
    class EvtFechMensal:
        """
        :ivar ideEvento: Informações de identificação do evento.
        :ivar ideContrib: Informações de identificação do contribuinte.
        :ivar idePeriodo: Período de referência das informações do evento.
        :ivar infoFechamento: Informações sobre o fechamento da apuração mensal e
            aproveitamento de bases de cálculo negativas (BCN).
        :ivar id: Identificador que representa unicamente o evento.
        """

        ideEvento: DeRe.EvtFechMensal.IdeEvento = field(
            metadata={
                "type": "Element",
            }
        )
        ideContrib: DeRe.EvtFechMensal.IdeContrib = field(
            metadata={
                "type": "Element",
            }
        )
        idePeriodo: DeRe.EvtFechMensal.IdePeriodo = field(
            metadata={
                "type": "Element",
            }
        )
        infoFechamento: None | DeRe.EvtFechMensal.InfoFechamento = field(
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
        class IdeEvento:
            """
            :ivar tpOper: Tipo de operação do evento. Nota: O envio deste evento
                consolida a totalização da apuração mensal. Para retificações,
                exige-se a transmissão prévia do evento de reabertura
                correspondente.
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
            :ivar perApur: Informar o período de apuração, sendo o ano e mês da
                competência da declaração. Máscara: AAAA-MM Validação: Só pode
                existir um único {perApur} para cada {nrInsc}. Não é permitida a
                inclusão de um novo fechamento para um período que já possua um
                evento D-1199 ativo, exceto se precedido pelo respectivo evento
                de reabertura.
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
        class InfoFechamento:
            """
            :ivar infoParamFech: Grupo de informações de indicadores de não
                ocorrência ou outras parametrizações específicas que qualificam o
                encerramento do período. Preenchimento: Deve ser informado
                exclusivamente quando houver necessidade de declarar dispensa de
                eventos auxiliares ou outras opções do contribuinte para o
                período de apuração {perApur}.
            :ivar gUtilizBCN: Grupo de informação de aproveitamento de bases de
                cálculo negativa de períodos anteriores.
            """

            infoParamFech: None | DeRe.EvtFechMensal.InfoFechamento.InfoParamFech = (
                field(
                    default=None,
                    metadata={
                        "type": "Element",
                    },
                )
            )
            gUtilizBCN: None | DeRe.EvtFechMensal.InfoFechamento.GUtilizBcn = field(
                default=None,
                metadata={
                    "type": "Element",
                },
            )

            @dataclass(kw_only=True)
            class InfoParamFech:
                """
                :ivar indInexistDedu: Declaração de inexistência de deduções a
                    detalhar no período, dispensando a transmissão do evento
                    auxiliar D-1121 (Relação de Deduções Utilizadas na Apuração)
                    para os contribuintes sujeitos à sua obrigatoriedade.
                    Preenchimento: Este campo não deve ser informado (deve ser
                    omitido do XML) nas seguintes situações: 1. Caso o
                    contribuinte possua deduções no mês (hipótese em que deverá
                    transmitir o respectivo evento D-1121 com os dados); ou 2.
                    Caso o contribuinte, por sua natureza jurídica ou regime, não
                    esteja sujeito a nenhuma regra de obrigatoriedade de entrega
                    do evento D-1121.
                """

                indInexistDedu: None | InfoParamFechIndInexistDedu = field(
                    default=None,
                    metadata={
                        "type": "Element",
                        "white_space": "preserve",
                    },
                )

            @dataclass(kw_only=True)
            class GUtilizBcn:
                """
                :ivar infoBCN: Detalhamento de informações da base de cálculo
                    negativa por tipo de serviço.
                :ivar detBCNeg: Informação individualizada de cada base de
                    cálculo negativa a ser aproveitada pelo contribuinte.
                """

                infoBCN: list[DeRe.EvtFechMensal.InfoFechamento.GUtilizBcn.InfoBcn] = (
                    field(
                        default_factory=list,
                        metadata={
                            "type": "Element",
                            "min_occurs": 1,
                            "max_occurs": 99,
                        },
                    )
                )
                detBCNeg: list[
                    DeRe.EvtFechMensal.InfoFechamento.GUtilizBcn.DetBcneg
                ] = field(
                    default_factory=list,
                    metadata={
                        "type": "Element",
                        "max_occurs": 99,
                    },
                )

                @dataclass(kw_only=True)
                class InfoBcn:
                    """
                    :ivar codBCNRaiz: Informar o código identificador da base de
                        cálculo negativa específica do qual se deseja utilizar a
                        base de cálculo negativa, conforme [[Tabela 12 – Códigos
                        de Bases de Cálculo]].
                    :ivar usarBCNAcum: Informar a opção por utilizar (se existir)
                        o valor de base de cálculo negativa acumulada em períodos
                        anteriores.
                    :ivar metodoAproveit: Informar qual método o contribuinte
                        deseja para o aproveitamento da base de cálculo negativa.
                        Preenchimento: Obrigatório se {usarBCNAcum} = [1]. Vedado
                        se {usarBCNAcum} = [0].
                    """

                    codBCNRaiz: str = field(
                        metadata={
                            "type": "Element",
                            "length": 5,
                            "white_space": "preserve",
                            "pattern": r"[1-9][0-9]{3}[IC]",
                        }
                    )
                    usarBCNAcum: InfoBcnUsarBcnacum = field(
                        metadata={
                            "type": "Element",
                            "white_space": "preserve",
                        }
                    )
                    metodoAproveit: None | InfoBcnMetodoAproveit = field(
                        default=None,
                        metadata={
                            "type": "Element",
                            "white_space": "preserve",
                        },
                    )

                @dataclass(kw_only=True)
                class DetBcneg:
                    """
                    :ivar codBCN: Informar o código da base de cálculo negativa
                        que será utilizado para dedução nesta competência.
                    :ivar vUsarBCN: Valor máximo da base de cálculo negativa que
                        o contribuinte deseja realizar o aproveitamento na
                        competência atual. Preenchimento: Não informar caso o
                        contribuinte deseje aproveitar toda a base de cálculo
                        negativa disponível no {codBCN}. Validação: Se o valor
                        informado pelo contribuinte for superior ao existente em
                        sua conta corrente para aquele {codBCN}, será atribuído o
                        valor máximo disponível na conta corrente e retornado
                        alerta informando não existir o saldo total disponível
                        naquela base de cálculo negativa.
                    """

                    codBCN: str = field(
                        metadata={
                            "type": "Element",
                            "length": 13,
                            "white_space": "preserve",
                            "pattern": r"[1-9][0-9]{3}[IC][0-9]{8}",
                        }
                    )
                    vUsarBCN: None | str = field(
                        default=None,
                        metadata={
                            "type": "Element",
                            "min_length": 4,
                            "max_length": 18,
                            "white_space": "preserve",
                            "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                        },
                    )
