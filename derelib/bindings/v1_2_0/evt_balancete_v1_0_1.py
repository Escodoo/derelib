from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from derelib.bindings.v1_2_0.xmldsig_core_schema import Signature
from derelib.mixin import DereMixin

__NAMESPACE__ = "http://www.dere.gov.br/schemas/evtBalancete/v1_0_1"


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


class InfoContaNatSaldoFinal(Enum):
    """
    :cvar D: Devedor
    :cvar C: Credor
    """

    D = "D"
    C = "C"


class InfoContaNatSaldoInic(Enum):
    """
    :cvar D: Devedor
    :cvar C: Credor
    """

    D = "D"
    C = "C"


class InfoContaNatVapur(Enum):
    """
    :cvar D: Movimento devedor
    :cvar C: Movimento credor
    """

    D = "D"
    C = "C"


@dataclass(kw_only=True)
class DeRe(DereMixin):
    """
    Envelope raiz dos eventos da DeRE.

    :ivar evtBalancete: Evento Balancete Mensal.
    :ivar signature:
    """

    class Meta:
        name = "DeRE"
        namespace = "http://www.dere.gov.br/schemas/evtBalancete/v1_0_1"

    evtBalancete: DeRe.EvtBalancete = field(
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
    class EvtBalancete:
        """
        :ivar ideEvento: Informações de identificação do evento.
        :ivar ideContrib: Informações de identificação do contribuinte.
        :ivar idePeriodo: Período de referência das informações do evento.
        :ivar infoBalancete: Informações do Balancete Mensal.
        :ivar id: Identificador que representa unicamente o evento.
        """

        ideEvento: DeRe.EvtBalancete.IdeEvento = field(
            metadata={
                "type": "Element",
            }
        )
        ideContrib: DeRe.EvtBalancete.IdeContrib = field(
            metadata={
                "type": "Element",
            }
        )
        idePeriodo: DeRe.EvtBalancete.IdePeriodo = field(
            metadata={
                "type": "Element",
            }
        )
        infoBalancete: None | DeRe.EvtBalancete.InfoBalancete = field(
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
        class InfoBalancete:
            """
            :ivar infoContas: Lista de contas do balancete.
            """

            infoContas: DeRe.EvtBalancete.InfoBalancete.InfoContas = field(
                metadata={
                    "type": "Element",
                }
            )

            @dataclass(kw_only=True)
            class InfoContas:
                """
                :ivar infoConta: Detalhamento de informações da conta contábil no
                    balancete.
                """

                infoConta: list[
                    DeRe.EvtBalancete.InfoBalancete.InfoContas.InfoConta
                ] = field(
                    default_factory=list,
                    metadata={
                        "type": "Element",
                        "min_occurs": 1,
                        "max_occurs": 90000,
                    },
                )

                @dataclass(kw_only=True)
                class InfoConta:
                    """
                    :ivar cCta: Código da Conta Analítica (como informada no
                        evento D-1011.{cCta}). Nota: Devem estar no PGCC vigente
                        no último dia do {perApur} todas as contas que tiveram
                        movimentação no período, ainda que tenham sido criadas ou
                        encerradas no período. Validação: Não informar contas
                        sintéticas. O {cCta} deve existir e estar vigente na
                        tabela PGCC do contribuinte no último dia do {perApur}
                        correspondente.
                    :ivar natSaldoInic: Natureza do saldo inicial da conta na
                        abertura do período de apuração.
                    :ivar vSaldoInic: Valor do saldo inicial da conta no período
                        de competência. Preenchimento: Valor absoluto (sem
                        sinal). Se D-1011.{codNat} = [1, 2 ou 3] (contas
                        patrimoniais); então {vSaldoInic} deve corresponder ao
                        {vSaldoFinal} da conta no período anterior. Se {codNat} =
                        [4 ou 5] e D-1011.{freqEncerr} = [A] e {perApur} =
                        [AAAA-01]; então {vSaldoInic} = [0.00]. Se {codNat} = [4
                        ou 5] e D-1011.{freqEncerr} = [S], e {perApur} = [AAAA-01
                        ou AAAA-07]; então {vSaldoInic} = [0.00]. Se {codNat} =
                        [4 ou 5] e D-1011.{freqEncerr} = [Q], e {perApur} =
                        [AAAA-01; AAAA-05 ou AAAA-09]; então {vSaldoInic} =
                        [0.00]. Se {codNat} = [4 ou 5] e D-1011.{freqEncerr} =
                        [T], e {perApur} = [AAAA-01;AAAA-04; AAAA-07 ou AAAA-10];
                        então {vSaldoInic} = [0.00]. Se {codNat} = [4 ou 5] e
                        D-1011.{freqEncerr} = [B], e {perApur} = [AAAA-01;
                        AAAA-03; AAAA-05; AAAA-07; AAAA-09; AAAA-11]; então
                        {vSaldoInic} = [0.00]. Se {codNat} = [4 ou 5] e
                        D-1011.{freqEncerr} = [M], então {vSaldoInic} = [0.00].
                    :ivar vMovDebt: Valor total dos lançamentos a débito
                        realizados na conta no mês de competência, em valor
                        absoluto e sem sinal. Preenchimento: Informar [0.00] se
                        não houver movimentação.
                    :ivar vAjusteDebt: Valor dos ajustes a serem excluídos no
                        {vMovDebt} para fins de cálculo do {vApur} (ex: estornos,
                        cancelamentos etc.). Validação: Deve ser menor ou igual a
                        {vMovDebt}.
                    :ivar vMovCred: Valor total dos lançamentos a crédito
                        realizados na conta no mês de competência, em valor
                        absoluto e sem sinal. Preenchimento: Informar [0.00] se
                        não houver movimentação.
                    :ivar vAjusteCred: Valor dos ajustes a serem excluídos no
                        {vMovCred}, ex: estornos, cancelamentos etc., ou a serem
                        somados no {vMovDev} para fins de cálculo do {vApur} .
                        Validação: Deve ser menor ou igual a {vMovCred}.
                    :ivar natSaldoFinal: Natureza do saldo final da conta no
                        encerramento do mês de competência.
                    :ivar vSaldoFinal: Valor do saldo final da conta no período
                        de competência. Deve ser informado antes do encerramento
                        das contas de resultado. Preenchimento: Valor absoluto
                        (sem sinal).
                    :ivar natVApur: Informar a natureza do movimento informado no
                        {vApur}. Validação: Obrigatório se {vApur} &gt; [0.00].
                    :ivar vApur: Valor base sobre o qual serão aplicadas as
                        regras definidas pelo código de tributação ({codTrib}).
                        Preenchimento: Informar [0.00] se não houver
                        movimentação.
                    """

                    cCta: str = field(
                        metadata={
                            "type": "Element",
                            "max_length": 53,
                            "white_space": "preserve",
                            "pattern": r"[0-9A-Za-z]+",
                        }
                    )
                    natSaldoInic: InfoContaNatSaldoInic = field(
                        metadata={
                            "type": "Element",
                            "white_space": "preserve",
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
                    vMovDebt: str = field(
                        metadata={
                            "type": "Element",
                            "min_length": 4,
                            "max_length": 18,
                            "white_space": "preserve",
                            "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                        }
                    )
                    vAjusteDebt: None | str = field(
                        default=None,
                        metadata={
                            "type": "Element",
                            "min_length": 4,
                            "max_length": 18,
                            "white_space": "preserve",
                            "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                        },
                    )
                    vMovCred: str = field(
                        metadata={
                            "type": "Element",
                            "min_length": 4,
                            "max_length": 18,
                            "white_space": "preserve",
                            "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                        }
                    )
                    vAjusteCred: None | str = field(
                        default=None,
                        metadata={
                            "type": "Element",
                            "min_length": 4,
                            "max_length": 18,
                            "white_space": "preserve",
                            "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                        },
                    )
                    natSaldoFinal: InfoContaNatSaldoFinal = field(
                        metadata={
                            "type": "Element",
                            "white_space": "preserve",
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
                    natVApur: None | InfoContaNatVapur = field(
                        default=None,
                        metadata={
                            "type": "Element",
                            "white_space": "preserve",
                        },
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
