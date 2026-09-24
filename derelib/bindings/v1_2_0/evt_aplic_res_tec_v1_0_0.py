from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from derelib.bindings.v1_2_0.xmldsig_core_schema import Signature
from derelib.mixin import DereMixin

__NAMESPACE__ = "http://www.dere.gov.br/schemas/evtAplicResTec/v1_0_0"


class IdeEventoAplicEmi(Enum):
    """
    :cvar VALUE_1: Emissão com aplicativo da empresa
    :cvar VALUE_2: Aplicativo governamental
    """

    VALUE_1 = "1"
    VALUE_2 = "2"


class IdeEventoMotExcl(Enum):
    """
    :cvar VALUE_1: Determinação judicial ou administrativa
    :cvar VALUE_2: Envio indevido (fato inexistente)
    :cvar VALUE_3: Erro na identificação (CNPJ/período incorretos)
    :cvar VALUE_9: Outro
    """

    VALUE_1 = "1"
    VALUE_2 = "2"
    VALUE_3 = "3"
    VALUE_9 = "9"


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
    :cvar VALUE_2: Alteração
    :cvar VALUE_3: Exclusão
    """

    VALUE_1 = "1"
    VALUE_2 = "2"
    VALUE_3 = "3"


class InfoAplicResTecSemAplic(Enum):
    """
    :cvar VALUE_1: Não existem informações de aplicações financeiras a declarar
        para este período
    """

    VALUE_1 = "1"


@dataclass(kw_only=True)
class DeRe(DereMixin):
    """
    Envelope raiz dos eventos da DeRE.

    :ivar evtAplicResTec: Evento de identificação e detalhamento de aplicações
        financeiras sobre reserva técnica.
    :ivar signature:
    """

    class Meta:
        name = "DeRE"
        namespace = "http://www.dere.gov.br/schemas/evtAplicResTec/v1_0_0"

    evtAplicResTec: DeRe.EvtAplicResTec = field(
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
    class EvtAplicResTec:
        """
        :ivar ideEvento: Informações de identificação do evento.
        :ivar ideContrib: Informações de identificação do contribuinte.
        :ivar idePeriodo: Período de referência das informações do evento.
        :ivar infoAplicResTec: Informações de aplicações financeiras sobre
            reserva técnica.
        :ivar id: Identificador que representa unicamente o evento.
        """

        ideEvento: DeRe.EvtAplicResTec.IdeEvento = field(
            metadata={
                "type": "Element",
            }
        )
        ideContrib: DeRe.EvtAplicResTec.IdeContrib = field(
            metadata={
                "type": "Element",
            }
        )
        idePeriodo: DeRe.EvtAplicResTec.IdePeriodo = field(
            metadata={
                "type": "Element",
            }
        )
        infoAplicResTec: None | DeRe.EvtAplicResTec.InfoAplicResTec = field(
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
        class IdeEvento:
            """
            :ivar tpOper: Tipo de operação do evento. Nota: A alteração substitui
                integralmente as informações do evento enviado anteriormente.
            :ivar motExcl: Motivo da Exclusão. Código do motivo que justifica a
                exclusão do evento. Validação: Obrigatório se {tpOper} = [3].
            :ivar nrProc: Informar o número do processo administrativo/judicial.
                Validação: Obrigatório se {motExcl} = [1]. Deve ser um número de
                processo válido e existente no evento D-1021.
            :ivar nrRecibo: Caso seja um evento de alteração/retificação ou
                exclusão, preencher com o número do recibo do arquivo a ser
                alterado/retificado ou excluído.
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
            motExcl: None | IdeEventoMotExcl = field(
                default=None,
                metadata={
                    "type": "Element",
                    "white_space": "preserve",
                },
            )
            nrProc: None | str = field(
                default=None,
                metadata={
                    "type": "Element",
                    "max_length": 21,
                    "white_space": "preserve",
                    "pattern": r"[A-Za-z0-9]+",
                },
            )
            nrRecibo: None | str = field(
                default=None,
                metadata={
                    "type": "Element",
                    "length": 31,
                    "white_space": "preserve",
                    "pattern": r"[0-9]{4}-20[0-9]{2}(0[1-9]|1[0-2])-[0-9A-Z]{19}",
                },
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
                competência da declaração. Máscara: AAAA-MM Validação: Se
                {tpOper} = [1], só pode existir um único {perApur} para cada
                {nrInsc}. Quando informado {nrRecibo}, o {perApur} deve ser
                exatamento ao mesmo existente no {nrRecibo} (caracteres 6 a 11 do
                recibo).
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
        class InfoAplicResTec:
            """
            :ivar semAplic: Indicação da inexistência de aplicações financeiras
                sobre reserva técnica. Preenchimento: Deve ser preenchido
                exclusivamente quando o contribuinte não possuir ativos
                financeiros vinculados à reserva técnica a detalhar no período de
                apuração {perApur}.
            :ivar infoAplic: Detalhamento das informações da aplicação financeira
                sobre reserva técnica.
            """

            semAplic: None | InfoAplicResTecSemAplic = field(
                default=None,
                metadata={
                    "type": "Element",
                    "white_space": "preserve",
                },
            )
            infoAplic: list[DeRe.EvtAplicResTec.InfoAplicResTec.InfoAplic] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "max_occurs": 100,
                },
            )

            @dataclass(kw_only=True)
            class InfoAplic:
                """
                :ivar cCta: Código da Conta Analítica (como informada no evento
                    D-1011.{cCta}). Nota: Devem estar no PGCC vigente no último
                    dia do {perApur} todas as contas que tiveram movimentação no
                    período, ainda que tenham sido criadas ou encerradas no
                    período. Validação: Não informar contas sintéticas. O {cCta}
                    deve existir e estar vigente na tabela PGCC do contribuinte
                    no último dia do {perApur} correspondente.
                :ivar detAtivo: Detalhamento do título/ativo.
                """

                cCta: str = field(
                    metadata={
                        "type": "Element",
                        "max_length": 53,
                        "white_space": "preserve",
                        "pattern": r"[0-9A-Za-z]+",
                    }
                )
                detAtivo: list[
                    DeRe.EvtAplicResTec.InfoAplicResTec.InfoAplic.DetAtivo
                ] = field(
                    default_factory=list,
                    metadata={
                        "type": "Element",
                        "min_occurs": 1,
                        "max_occurs": 500,
                    },
                )

                @dataclass(kw_only=True)
                class DetAtivo:
                    """
                    :ivar descAtivo: Descrição da denominação do ativo financeiro
                        vinculado a reserva técnica.
                    :ivar vSaldoInic: Valor do título em 01/01/2026 ou na data da
                        aquisição, se esta for posterior a esta data.
                        Preenchimento: Deve ser igual ao {vSaldoFinal} do período
                        anterior para o mesmo {idAtivo} (exceto na primeira
                        competência do declarante).
                    :ivar vRendPerReceb: Valor de rendimentos periódicos
                        recebidos no período de apuração (cupons, dividentos,
                        etc).
                    :ivar vVarMensal: Valores de variação mensal a serem
                        incorporados ao saldo do ativo. Nota: Valores podem ser
                        positivos ou negativos.
                    :ivar vPrincLiqResg: Valor do principal liquidado ou
                        resgatado do ativo financeiro.
                    :ivar vRendLiqResg: Valor dos rendimentos recebidos na
                        liquidação ou resgate do ativo financeiro.
                    :ivar vSaldoFinal: Valor do título no último dia do período
                        de apuração {perApur}. Cálculo: {vSaldoInic} +
                        {vVarMensal} - {vPrincLiqResg}
                    :ivar vApur: Valor base sobre o qual serão aplicadas as
                        regras definidas pelo código de tributação ({codTrib}).
                        Cálculo: {vRendPerReceb} + {vRendLiqResg}
                    :ivar idAtivo: Número de identificação do título/ativo.
                    """

                    descAtivo: str = field(
                        metadata={
                            "type": "Element",
                            "max_length": 255,
                            "white_space": "preserve",
                            "pattern": r"([!-ÿ][ -ÿ]*[!-ÿ]|[!-ÿ])",
                        }
                    )
                    vSaldoInic: str = field(
                        metadata={
                            "type": "Element",
                            "min_length": 4,
                            "max_length": 18,
                            "white_space": "preserve",
                            "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                        }
                    )
                    vRendPerReceb: None | str = field(
                        default=None,
                        metadata={
                            "type": "Element",
                            "min_length": 4,
                            "max_length": 18,
                            "white_space": "preserve",
                            "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                        },
                    )
                    vVarMensal: None | str = field(
                        default=None,
                        metadata={
                            "type": "Element",
                            "min_length": 4,
                            "max_length": 19,
                            "white_space": "preserve",
                            "pattern": r"-?(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                        },
                    )
                    vPrincLiqResg: str = field(
                        metadata={
                            "type": "Element",
                            "min_length": 4,
                            "max_length": 18,
                            "white_space": "preserve",
                            "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                        }
                    )
                    vRendLiqResg: None | str = field(
                        default=None,
                        metadata={
                            "type": "Element",
                            "min_length": 4,
                            "max_length": 18,
                            "white_space": "preserve",
                            "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                        },
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
                    vApur: str = field(
                        metadata={
                            "type": "Element",
                            "min_length": 4,
                            "max_length": 18,
                            "white_space": "preserve",
                            "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                        }
                    )
                    idAtivo: str = field(
                        metadata={
                            "type": "Attribute",
                            "max_length": 30,
                            "white_space": "preserve",
                            "pattern": r"[0-9A-Za-z]{1,30}",
                        }
                    )
