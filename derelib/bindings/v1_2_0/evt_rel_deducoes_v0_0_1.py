from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from derelib.bindings.v1_2_0.xmldsig_core_schema import Signature
from derelib.mixin import DereMixin

__NAMESPACE__ = "http://www.dere.gov.br/schemas/evtRelDeducoes/v0_0_1"


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
    :cvar VALUE_4: Retificação após fechamento mensal
    """

    VALUE_1 = "1"
    VALUE_2 = "2"
    VALUE_3 = "3"
    VALUE_4 = "4"


class InfoDfeTpAtiv(Enum):
    """
    :cvar VALUE_01: Operações de Crédito, Câmbio, TVM, Securitização e
        Faturização
    :cvar VALUE_02: Arrendamentos
    :cvar VALUE_03: Seguros, com exceção de Seguro Saúde
    :cvar VALUE_04: Previdência
    :cvar VALUE_05: Capitalização
    :cvar VALUE_06: Planos de Assistência à Saúde
    :cvar VALUE_07: Concursos de Prognósticos
    """

    VALUE_01 = "01"
    VALUE_02 = "02"
    VALUE_03 = "03"
    VALUE_04 = "04"
    VALUE_05 = "05"
    VALUE_06 = "06"
    VALUE_07 = "07"


class InfoDfeTpDfe(Enum):
    """
    :cvar VALUE_01: DeRE
    :cvar VALUE_02: NFS-e
    :cvar VALUE_03: NF-e
    :cvar VALUE_04: NFC-e
    :cvar VALUE_05: NF-e ABI
    """

    VALUE_01 = "01"
    VALUE_02 = "02"
    VALUE_03 = "03"
    VALUE_04 = "04"
    VALUE_05 = "05"


class InfoDeducoesFinEvt(Enum):
    """
    :cvar VALUE_1: Inclusão de registro
    :cvar VALUE_2: Alteração de registro
    :cvar VALUE_3: Exclusão de registro
    """

    VALUE_1 = "1"
    VALUE_2 = "2"
    VALUE_3 = "3"


@dataclass(kw_only=True)
class DeRe(DereMixin):
    """
    Envelope raiz dos eventos da DeRE.

    :ivar evtRelDeducoes: Evento Relação de Deduções Utilizadas na Apuração.
    :ivar signature:
    """

    class Meta:
        name = "DeRE"
        namespace = "http://www.dere.gov.br/schemas/evtRelDeducoes/v0_0_1"

    evtRelDeducoes: DeRe.EvtRelDeducoes = field(
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
    class EvtRelDeducoes:
        """
        :ivar ideEvento: Informações de identificação do evento.
        :ivar ideContrib: Informações de identificação do contribuinte.
        :ivar idePeriodo: Período de referência das informações do evento.
        :ivar infoDeducoes: Informações das deduções utilizadas na apuração.
            Preenchimento: Vedado se {tpOper} = [3] (exclusão); Obrigatório nos
            demais casos.
        :ivar id: Identificador que representa unicamente o evento.
        """

        ideEvento: DeRe.EvtRelDeducoes.IdeEvento = field(
            metadata={
                "type": "Element",
            }
        )
        ideContrib: DeRe.EvtRelDeducoes.IdeContrib = field(
            metadata={
                "type": "Element",
            }
        )
        idePeriodo: DeRe.EvtRelDeducoes.IdePeriodo = field(
            metadata={
                "type": "Element",
            }
        )
        infoDeducoes: None | DeRe.EvtRelDeducoes.InfoDeducoes = field(
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
                integralmente as informações do evento enviado anteriormente. A
                inclusão, alteração ou exclusão do evento completo só é permitida
                antes do fechamento mensal. Após o processamento com sucesso do
                Fechamento Mensal (D-1199) para o período ({perApur}), caso sejam
                necessários ajustes, estes devem ser feitos individualmente por
                documento fiscal utilizando a operação [4] (Retificação após
                fechamento mensal), sendo necessário o envio de um evento
                Reabertura de Período de Apuração (D-1198) previamente e um novo
                Fechamento Mensal (D-1199). Validação: 1. As operações [1], [2] e
                [3] são permitidas exclusivamente antes da primeira transmissão
                com sucesso do Fechamento Mensal (D-1199) para a competência
                ({perApur}); 2. A operação [4] é vedada se não houver Fechamento
                Mensal (D-1199) prévio para o período ({perApur}); 3. A operação
                [4] é permitida se, e somente se, o período ({perApur}) estiver
                com status "Reaberto" decorrente do processamento com sucesso de
                evento de Reabertura de Período de Apuração (D-1198).
            :ivar motExcl: Motivo da exclusão. Código do motivo que justifica a
                exclusão do evento. Preenchimento: Exclusivo e obrigatório se
                {tpOper} = [3].
            :ivar nrProc: Número do processo administrativo/judicial.
                Preenchimento: Obrigatório se {motExcl} = [1]. Validação: Deve
                ser um número de processo válido e existente no evento D-1021.
            :ivar nrRecibo: Caso seja um evento de alteração/retificação ou
                exclusão, preencher com o número do recibo do arquivo a ser
                alterado/retificado ou excluído. Preenchimento: Obrigatório se
                {tpOper} = [2; 3]; Vedado se {tpOper} = [1; 4].
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
            :ivar perApur: Período de apuração, sendo o ano e mês da competência
                da declaração. Máscara: AAAA-MM Validação: Se {tpOper} = [1], só
                pode existir um único {perApur} para cada {nrInsc}. Quando
                informado {nrRecibo}, o {perApur} deve ser exatamente o mesmo
                existente no {nrRecibo} (caracteres 6 a 11 do recibo).
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
        class InfoDeducoes:
            """
            :ivar finEvt: Finalidade do evento. Preenchimento: Exclusivo e
                obrigatório se {tpOper} for igual a [4] (Retificação após
                fechamento mensal).
            :ivar infoDeducao: Informações da dedução.
            """

            finEvt: None | InfoDeducoesFinEvt = field(
                default=None,
                metadata={
                    "type": "Element",
                    "white_space": "preserve",
                },
            )
            infoDeducao: list[DeRe.EvtRelDeducoes.InfoDeducoes.InfoDeducao] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "min_occurs": 1,
                    "max_occurs": 50000,
                },
            )

            @dataclass(kw_only=True)
            class InfoDeducao:
                """
                :ivar infoDFe: Informação do documento fiscal. Preenchimento:
                    Vedado se {infoImovel} for informado.
                :ivar infoImovel: Informações de imóvel objeto de arrendamento
                    mercantil. Nota: Preenchimento exclusivo em caso de aquisição
                    de imóvel de pessoa física não contribuinte (sem emissão de
                    DF-e). Preenchimento: Vedado se {infoDFe} for informado no
                    mesmo grupo {infoDeducao}. Caso o declarante tenha adquirido
                    mais de um imóvel do mesmo alienante, deve ser gerada uma
                    ocorrência distinta do grupo {infoDeducao} para cada imóvel.
                :ivar detDeducao: Grupo de informação das deduções.
                :ivar itemDFe: Relação de itens específicos do documento fiscal
                    eletrônico (DFe) utilizados para dedução. Preenchimento: 1.
                    Registro inicial: ({perApur} igual ao mês/ano de {dtEmi}):
                    Obrigatório se {tpDFe} = [01; 03; 04] E o valor total
                    dedutível for menor que o valor total do documento fiscal
                    ({vDedTotal} &lt; {vOper}); 2. Períodos subsequentes
                    ({perApur} posterior ao mês/ano de {dtEmi}): Obrigatório para
                    os itens com dedução na competência ({vItemDed} &gt; [0.00]),
                    desde que a conta-corrente do documento fiscal ({chDFe})
                    tenha sido inaugurada no mês de sua emissão com o
                    detalhamento do grupo {itemDFe}. Cálculo: 1. No registro
                    inicial o somatório de todos os valores totais dedutíveis por
                    item ({vItemDedTotal}) associados ao documento fiscal deve
                    ser igual ao campo geral de teto do documento declarado
                    (SOMA({vItemDedTotal}) = {vDedTotal}); 2. O somatório de
                    todos os valores de dedução do período por item ({vItemDed})
                    informados na competência atual deve ser igual ao campo geral
                    de dedução do mês (SOMA({vItemDed}) = {vDed}) para este
                    documento fiscal ({chDFe}).
                """

                infoDFe: None | DeRe.EvtRelDeducoes.InfoDeducoes.InfoDeducao.InfoDfe = (
                    field(
                        default=None,
                        metadata={
                            "type": "Element",
                        },
                    )
                )
                infoImovel: (
                    None | DeRe.EvtRelDeducoes.InfoDeducoes.InfoDeducao.InfoImovel
                ) = field(
                    default=None,
                    metadata={
                        "type": "Element",
                    },
                )
                detDeducao: DeRe.EvtRelDeducoes.InfoDeducoes.InfoDeducao.DetDeducao = (
                    field(
                        metadata={
                            "type": "Element",
                        }
                    )
                )
                itemDFe: list[DeRe.EvtRelDeducoes.InfoDeducoes.InfoDeducao.ItemDfe] = (
                    field(
                        default_factory=list,
                        metadata={
                            "type": "Element",
                            "max_occurs": 998,
                        },
                    )
                )

                @dataclass(kw_only=True)
                class InfoDfe:
                    """
                    :ivar tpDFe: Tipo de documento fiscal. Preenchimento: Vedado
                        {chDFeRetif} for informado. Obrigatório nos demais casos.
                    :ivar chDFe: Chave de acesso do documento fiscal que
                        acobertou a operação que deu origem à dedução.
                        Preenchimento: Vedado {chDFeRetif} for informado.
                        Obrigatório nos demais casos. Uma chave de um documento
                        fiscal ({chDFe}) só pode ocorrer uma única vez por
                        arquivo em cada período de apuração ({perApur}), vedando
                        repetições da mesma nota no mesmo mês. Nota: 1. O
                        registro inicial da chave na base da DeRE inaugura uma
                        conta-corrente para o controle de saldos do documento; 2.
                        Em competências futuras, o reenvio da mesma chave é
                        tratado como apropriação contínua de deduções pendentes
                        (ex: regime de caixa), acumulando os valores de {vDed}
                        até o limite de {vDedTotal}; 3. A conta-corrente do
                        documento fiscal só é inaugurada se informada no seu mês
                        de emissão, sendo vedada a abertura em {perApur} distinto
                        do {dtEmi}.
                    :ivar dtEmi: Data de emissão do documento fiscal. Máscara:
                        AAAA-MM-DD
                    :ivar chDFeRetif: Chave de acesso do documento fiscal cujo
                        registro será objeto de alteração ou exclusão.
                        Preenchimento: Exclusivo e obrigatório se {tpOper} for
                        igual a [4] E {finEvt} for diferente de [1].
                    :ivar tpAtiv: Tipo de atividade que está vinculada a dedução.
                    """

                    tpDFe: None | InfoDfeTpDfe = field(
                        default=None,
                        metadata={
                            "type": "Element",
                            "white_space": "preserve",
                        },
                    )
                    chDFe: None | str = field(
                        default=None,
                        metadata={
                            "type": "Element",
                            "min_length": 44,
                            "max_length": 53,
                            "white_space": "preserve",
                            "pattern": r"[0-9A-Z]+",
                        },
                    )
                    dtEmi: str = field(
                        metadata={
                            "type": "Element",
                            "length": 10,
                            "white_space": "preserve",
                            "pattern": r"(((20(([02468][048])|([13579][26]))-02-29))|(20[0-9][0-9])-((((0[1-9])|(1[0-2]))-((0[1-9])|(1\d)|(2[0-8])))|((((0[13578])|(1[02]))-31)|(((0[1,3-9])|(1[0-2]))-(29|30)))))",
                        }
                    )
                    chDFeRetif: None | str = field(
                        default=None,
                        metadata={
                            "type": "Element",
                            "min_length": 44,
                            "max_length": 53,
                            "white_space": "preserve",
                            "pattern": r"[0-9A-Z]+",
                        },
                    )
                    tpAtiv: InfoDfeTpAtiv = field(
                        metadata={
                            "type": "Element",
                            "white_space": "preserve",
                        }
                    )

                @dataclass(kw_only=True)
                class InfoImovel:
                    """
                    :ivar CPFAlien: Número de inscrição no CPF do alienante do
                        imóvel, quando este não for contribuinte do IBS/CBS,
                        adquirido para fins de arrendamento mercantil. Validação:
                        Deve ser um CPF válido.
                    """

                    CPFAlien: str = field(
                        metadata={
                            "type": "Element",
                            "length": 11,
                            "white_space": "preserve",
                            "pattern": r"[0-9]{11}",
                        }
                    )

                @dataclass(kw_only=True)
                class DetDeducao:
                    """
                    :ivar vOper: Valor total da operação, conforme documento
                        fiscal ou transação. Preenchimento: 1. Quando o grupo
                        {infoDFe} for informado, este campo deve corresponder ao
                        valor total do respectivo documento {chDFe}; 2. Quando o
                        grupo {infoImovel} for informado, preencher com o valor
                        do imóvel.
                    :ivar vDedTotal: Valor total do documento fiscal eletrônico
                        (DFe) que será destinado à dedução da base de cálculo,
                        ainda que o aproveitamento ocorra de forma parcelada em
                        competências futuras. Exemplo: Se o documento fiscal
                        apresentar o valor total ({vOper}) de R$ 1.000,00, mas
                        apenas R$ 800,00 forem passíveis de dedução na atividade,
                        informar R$ 800,00. Nota: No caso de aquisição de bens
                        para arrendamento, informar o valor total depreciável do
                        bem. Preenchimento: Exclusivo e obrigatório no período de
                        apuração correspondente ao mês/ano de emissão do
                        documento fiscal (quando o mês/ano de {dtEmi}
                        corresponder ao {perApur}), e desde que o grupo {infoDFe}
                        esteja preenchido. O valor total previsto para a dedução
                        ({vDedTotal}) deve ser declarado uma única vez (no mês de
                        emissão do DF-e), sendo vedado o seu preenchimento em
                        competências subsequentes (quando o {perApur} for
                        posterior ao mês/ano do documento fiscal ({dtEmi})).
                        Validação: Não pode ser superior a {vOper}.
                    :ivar vDed: Valor efetivamente utilizado como dedução da base
                        de cálculo do IBS e da CBS no período de apuração
                        corrente. No caso de despesas ou aquisições liquidadas de
                        forma fracionada (regime de caixa), informar apenas a
                        parcela cuja dedução seja apropriada na competência
                        atual. Preenchimento: 1. No período de apuração de
                        emissão do documento fiscal (registro inicial neste
                        evento) se não houver fração de valor a deduzir na
                        competência corrente, informar [0.00]; 2. Nos períodos de
                        apuração subsequentes (continuação de dedução parcelada
                        ou depreciação mensal): preenchimento obrigatório para
                        reportar a fração mensal utilizada na competência, sendo
                        vedada a informação do campo {vDedTotal} neste evento.
                        Para a utilização da dedução neste formato, é obrigatória
                        a existência prévia da informação do campo {vDedTotal}
                        deste documento fiscal ({chDFe}) em período de apuração
                        ({perApur}) anterior. Nota: No caso de aquisição de bens
                        destinados a arrendamento mercantil operacional amparados
                        por documento fiscal, informar o valor da quota de
                        depreciação mensal apropriada na competência. Validação:
                        1. Quando {vDedTotal} for informado, {vDed} deve ser
                        igual ou inferior a {vDedTotal}. 2. A soma histórica
                        acumulada das ocorrências de {vDed} para a mesma chave de
                        documento fiscal ({chDFe}) não poderá ultrapassar o
                        limite estabelecido no campo {vDedTotal} original.
                    """

                    vOper: str = field(
                        metadata={
                            "type": "Element",
                            "min_length": 4,
                            "max_length": 18,
                            "white_space": "preserve",
                            "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                        }
                    )
                    vDedTotal: None | str = field(
                        default=None,
                        metadata={
                            "type": "Element",
                            "min_length": 4,
                            "max_length": 18,
                            "white_space": "preserve",
                            "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                        },
                    )
                    vDed: str = field(
                        metadata={
                            "type": "Element",
                            "min_length": 4,
                            "max_length": 18,
                            "white_space": "preserve",
                            "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                        }
                    )

                @dataclass(kw_only=True)
                class ItemDfe:
                    """
                    :ivar nItem: Número do item ou sequencial do documento fiscal
                        que identifica o item utilizado para a dedução.
                        Validação: O número informado deve corresponder a um item
                        válido e existente no documento fiscal eletrônico
                        referenciado.
                    :ivar vItem: Valor total do item, conforme documento fiscal
                        ou transação.
                    :ivar vItemDedTotal: Valor total dedutível correspondente ao
                        item do documento fiscal, ainda que o aproveitamento
                        ocorra de forma parcelada ou diferida em competências
                        futuras. Preenchimento: Exclusivo e obrigatório se o
                        {vDedTotal} for preenchido para este documento fiscal
                        ({chDFe}). Validação: O valor de {vItemDedTotal} não pode
                        ser superior ao valor correspondente ao respectivo item
                        no documento fiscal eletrônico ({vItem}) referenciado.
                    :ivar vItemDed: Valor efetivamente utilizado como dedução
                        correspondente a este item específico na competência
                        (período de apuração) corrente. Preenchimento: 1. No
                        período de apuração de emissão do documento fiscal
                        (registro inicial neste evento) se não houver fração de
                        valor a deduzir na competência corrente, informar [0.00];
                        2. Nos períodos de apuração subsequentes: preenchimento
                        obrigatório para reportar a fração mensal utilizada na
                        competência, sendo vedada, neste caso, a informação do
                        campo {vItemDedTotal} neste evento. Para a utilização da
                        dedução neste formato, é obrigatória a existência prévia
                        da informação do campo {vItemDedTotal} para este mesmo
                        item ({nItem}) deste documento fiscal ({chDFe}) em
                        período de apuração ({perApur}) anterior. Validação: 1.
                        Quando {vItemDedTotal} for informado no mesmo evento
                        (registro inicial), o valor de {vItemDed} deve ser igual
                        ou inferior a {vItemDedTotal}; 2. A soma histórica
                        acumulada das ocorrências de {vItemDed} para o mesmo item
                        ({nItem}) da chave de documento fiscal ({chDFe}) não
                        poderá ultrapassar o limite de saldo estabelecido no
                        campo {vItemDedTotal} original.
                    """

                    nItem: str = field(
                        metadata={
                            "type": "Element",
                            "max_length": 3,
                            "white_space": "preserve",
                            "pattern": r"[1-9][0-9]{0,2}",
                        }
                    )
                    vItem: str = field(
                        metadata={
                            "type": "Element",
                            "min_length": 4,
                            "max_length": 18,
                            "white_space": "preserve",
                            "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                        }
                    )
                    vItemDedTotal: None | str = field(
                        default=None,
                        metadata={
                            "type": "Element",
                            "min_length": 4,
                            "max_length": 18,
                            "white_space": "preserve",
                            "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                        },
                    )
                    vItemDed: str = field(
                        metadata={
                            "type": "Element",
                            "min_length": 4,
                            "max_length": 18,
                            "white_space": "preserve",
                            "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                        }
                    )
