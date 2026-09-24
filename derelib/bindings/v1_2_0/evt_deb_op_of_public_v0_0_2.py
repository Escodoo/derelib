from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from derelib.bindings.v1_2_0.xmldsig_core_schema import Signature
from derelib.mixin import DereMixin

__NAMESPACE__ = "http://www.dere.gov.br/schemas/evtDebOpOfPublic/v0_0_2"


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


class InfoDebOpOfPublicSemTitulos(Enum):
    """
    :cvar VALUE_1: Sem movimento com títulos de dívida com oferta pública neste
        período
    """

    VALUE_1 = "1"


@dataclass(kw_only=True)
class DeRe(DereMixin):
    """
    Envelope raiz dos eventos da DeRE.

    :ivar evtDebOpOfPublic: Evento débito mensal de operações com títulos de
        dívida com oferta pública.
    :ivar signature:
    """

    class Meta:
        name = "DeRE"
        namespace = "http://www.dere.gov.br/schemas/evtDebOpOfPublic/v0_0_2"

    evtDebOpOfPublic: DeRe.EvtDebOpOfPublic = field(
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
    class EvtDebOpOfPublic:
        """
        :ivar ideEvento: Informações de identificação do evento.
        :ivar ideContrib: Informações de identificação do contribuinte.
        :ivar idePeriodo: Período de referência das informações do evento.
        :ivar infoDebOpOfPublic: Informações de títulos de dívida com oferta
            pública.
        :ivar id: Identificador que representa unicamente o evento.
        """

        ideEvento: DeRe.EvtDebOpOfPublic.IdeEvento = field(
            metadata={
                "type": "Element",
            }
        )
        ideContrib: DeRe.EvtDebOpOfPublic.IdeContrib = field(
            metadata={
                "type": "Element",
            }
        )
        idePeriodo: DeRe.EvtDebOpOfPublic.IdePeriodo = field(
            metadata={
                "type": "Element",
            }
        )
        infoDebOpOfPublic: None | DeRe.EvtDebOpOfPublic.InfoDebOpOfPublic = field(
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
            :ivar tpOper: Tipo de operação do evento. Nota: A alteração substitui
                integralmente as informações do evento enviado anteriormente.
            :ivar motExcl: Motivo da exclusão. Código do motivo que justifica a
                exclusão do evento. Preenchimento: Exclusivo e obrigatório se
                {tpOper} = [3].
            :ivar nrProc: Informar o número do processo administrativo/judicial.
                Preenchimento: Obrigatório se {motExcl} = [1]. Validação: Deve
                ser um número de processo válido e existente no evento D-1021.
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
                    "pattern": r"[0-9A-Za-z]+",
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
                exatamente o mesmo existente no {nrRecibo} (caracteres 6 a 11 do
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
        class InfoDebOpOfPublic:
            """
            :ivar semTitulos: Indicação da inexistência de títulos de dívida com
                oferta pública movimentados no período. Preenchimento: Deve ser
                preenchido exclusivamente quando o contribuinte não possuir
                movimento com títulos de dívida com oferta pública a detalhar no
                período de apuração ({perApur}).
            :ivar infoTitulos: Informações do título de dívida com oferta
                pública.
            """

            semTitulos: None | InfoDebOpOfPublicSemTitulos = field(
                default=None,
                metadata={
                    "type": "Element",
                    "white_space": "preserve",
                },
            )
            infoTitulos: None | DeRe.EvtDebOpOfPublic.InfoDebOpOfPublic.InfoTitulos = (
                field(
                    default=None,
                    metadata={
                        "type": "Element",
                    },
                )
            )

            @dataclass(kw_only=True)
            class InfoTitulos:
                """
                :ivar detTitulo: Detalhamento do título.
                """

                detTitulo: list[
                    DeRe.EvtDebOpOfPublic.InfoDebOpOfPublic.InfoTitulos.DetTitulo
                ] = field(
                    default_factory=list,
                    metadata={
                        "type": "Element",
                        "min_occurs": 1,
                        "max_occurs": 10000,
                    },
                )

                @dataclass(kw_only=True)
                class DetTitulo:
                    """
                    :ivar descFundo: Descrição do nome do fundo. Validação:
                        Obrigatório se aquisição se der por meio de fundos de
                        investimento com composição mínima de 95% de títulos de
                        dívida.
                    :ivar CNPJDevedor: Número de inscrição no CNPJ do devedor
                        emitente do título de dívida. Validação: Deve ser um CNPJ
                        válido com 14 posições.
                    :ivar vSaldoContIni: Representa o valor do título sobre o
                        qual haverá a incidência dos juros no período.
                        Preenchimento: Deve ser igual ao {vSaldoContFin} do
                        período anterior para o mesmo {idTitulo} (exceto na
                        primeira competência do declarante).
                    :ivar vEntradas: Valor total das entradas (compras de novos
                        títulos) da mesma emissão e série de ativos no período de
                        apuração.
                    :ivar vSaidas: Valor total das saídas (vendas de títulos e
                        amortizações) da mesma emissão e série de ativos, no
                        período de apuração.
                    :ivar vJurosRec: Valor dos juros recebidos relativos à mesma
                        emissão e série de ativos, no período de apuração.
                    :ivar vJurosApropr: Valor total da receita de juros e demais
                        rendimentos financeiros auferidos sobre o título no
                        período.
                    :ivar vSaldoContFin: Valor final do agrumento de títulos.
                        Cálculo: {vSaldoContFin} = {vSaldoContIni} + {vEntradas}
                        - {vSaidas} - {vJurosRec} + {vJurosApropr}
                    :ivar vSelic: Valor equivalente à variação da taxa Selic no
                        período. Representa o teto tributável para a operação.
                    :ivar vPisCofins: Valor da dedução relativa ao PIS/COFINS
                        incidente sobre a receita tributada. Nota: Informar
                        apenas a parcela passível de dedução da base de cálculo
                        do IBS/CBS.
                    :ivar vApur: Valor base sobre o qual serão aplicadas as
                        regras definidas pelo código de tributação ({codTrib}).
                        Cálculo: {vApur} = (MENORENTRE({vSelic} e {vJurosAprop}))
                        - {vPisCofins}
                    :ivar idTitulo: Código de identificação global do título no
                        padrão ISO 6166 (ISIN). Preenchimento: Deve ser informado
                        sem espaços ou caracteres especiais, contendo exatamente
                        12 caracteres alfanuméricos.
                    :ivar cCta: Código da conta analítica (como informada no
                        evento D-1011.{cCta}). Preenchimento: Não informar contas
                        sintéticas. Nota: Devem estar no PGCC vigente no último
                        dia do {perApur} todas as contas que tiveram movimentação
                        no período, ainda que tenham sido criadas ou encerradas
                        no período. Validação: O {cCta} deve existir e estar
                        vigente na tabela PGCC do contribuinte no último dia do
                        {perApur} correspondente.
                    """

                    descFundo: None | str = field(
                        default=None,
                        metadata={
                            "type": "Element",
                            "max_length": 255,
                            "white_space": "preserve",
                            "pattern": r"([!-ÿ][ -ÿ]*[!-ÿ]|[!-ÿ])",
                        },
                    )
                    CNPJDevedor: str = field(
                        metadata={
                            "type": "Element",
                            "length": 14,
                            "white_space": "preserve",
                            "pattern": r"[0-9A-Z]{12}[0-9]{2}",
                        }
                    )
                    vSaldoContIni: str = field(
                        metadata={
                            "type": "Element",
                            "min_length": 6,
                            "max_length": 20,
                            "white_space": "preserve",
                            "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{4}",
                        }
                    )
                    vEntradas: str = field(
                        metadata={
                            "type": "Element",
                            "min_length": 6,
                            "max_length": 20,
                            "white_space": "preserve",
                            "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{4}",
                        }
                    )
                    vSaidas: str = field(
                        metadata={
                            "type": "Element",
                            "min_length": 6,
                            "max_length": 20,
                            "white_space": "preserve",
                            "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{4}",
                        }
                    )
                    vJurosRec: str = field(
                        metadata={
                            "type": "Element",
                            "min_length": 6,
                            "max_length": 20,
                            "white_space": "preserve",
                            "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{4}",
                        }
                    )
                    vJurosApropr: str = field(
                        metadata={
                            "type": "Element",
                            "min_length": 6,
                            "max_length": 20,
                            "white_space": "preserve",
                            "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{4}",
                        }
                    )
                    vSaldoContFin: str = field(
                        metadata={
                            "type": "Element",
                            "min_length": 6,
                            "max_length": 20,
                            "white_space": "preserve",
                            "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{4}",
                        }
                    )
                    vSelic: str = field(
                        metadata={
                            "type": "Element",
                            "min_length": 6,
                            "max_length": 20,
                            "white_space": "preserve",
                            "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{4}",
                        }
                    )
                    vPisCofins: None | str = field(
                        default=None,
                        metadata={
                            "type": "Element",
                            "min_length": 6,
                            "max_length": 20,
                            "white_space": "preserve",
                            "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{4}",
                        },
                    )
                    vApur: str = field(
                        metadata={
                            "type": "Element",
                            "min_length": 6,
                            "max_length": 20,
                            "white_space": "preserve",
                            "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{4}",
                        }
                    )
                    idTitulo: str = field(
                        metadata={
                            "type": "Attribute",
                            "length": 12,
                            "white_space": "preserve",
                            "pattern": r"[A-Z]{2}[0-9A-Z]{9}[0-9]",
                        }
                    )
                    cCta: str = field(
                        metadata={
                            "type": "Attribute",
                            "max_length": 53,
                            "white_space": "preserve",
                            "pattern": r"[0-9A-Za-z]+",
                        }
                    )
