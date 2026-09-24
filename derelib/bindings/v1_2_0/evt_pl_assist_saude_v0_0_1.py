from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from derelib.bindings.v1_2_0.xmldsig_core_schema import Signature
from derelib.mixin import DereMixin

__NAMESPACE__ = "http://www.dere.gov.br/schemas/evtPlAssistSaude/v0_0_1"


class AdqExteriorCNaoNif(Enum):
    """
    :cvar VALUE_1: Dispensado de NIF
    :cvar VALUE_2: Não exigência de NIF
    """

    VALUE_1 = "1"
    VALUE_2 = "2"


class IdeEventoAplicEmi(Enum):
    """
    :cvar VALUE_1: Emissão com aplicativo da empresa
    :cvar VALUE_2: Aplicativo governamental
    """

    VALUE_1 = "1"
    VALUE_2 = "2"


class IdeEventoFinEvt(Enum):
    """
    :cvar VALUE_11: Registro original
    :cvar VALUE_31: Devolução
    :cvar VALUE_41: Cancelamento
    """

    VALUE_11 = "11"
    VALUE_31 = "31"
    VALUE_41 = "41"


class IdeEventoTpAmb(Enum):
    """
    :cvar VALUE_1: Produção
    :cvar VALUE_2: Produção restrita
    """

    VALUE_1 = "1"
    VALUE_2 = "2"


class QualifOperTpContrato(Enum):
    """
    :cvar VALUE_1: Plano ou seguro individual/familiar
    :cvar VALUE_2: Plano ou seguro coletivo sem administradora de benefícios
    :cvar VALUE_3: Plano ou seguro coletivo com administradora de benefícios
    :cvar VALUE_4: Plano ou seguro sem valor definido por usuário
    """

    VALUE_1 = "1"
    VALUE_2 = "2"
    VALUE_3 = "3"
    VALUE_4 = "4"


@dataclass(kw_only=True)
class DeRe(DereMixin):
    """
    Envelope raiz dos eventos da DeRE.

    :ivar evtPlAssistSaude: Evento de identificação e detalhamento dos
        adquirentes e beneficiários dos planos de assistência à saúde. Validação:
        Evento exclusivo e obrigatório para o registro de operações cujos códigos
        de base de cálculo ({codBC}) correspondam a um dos seguintes valores:
        [5010; 5020; 5030; 5050].
    :ivar signature:
    """

    class Meta:
        name = "DeRE"
        namespace = "http://www.dere.gov.br/schemas/evtPlAssistSaude/v0_0_1"

    evtPlAssistSaude: DeRe.EvtPlAssistSaude = field(
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
    class EvtPlAssistSaude:
        """
        :ivar ideEvento: Informações de identificação do evento.
        :ivar ideContrib: Informações de identificação do contribuinte.
        :ivar idePeriodo: Período de referência das informações do evento.
        :ivar infoOper: Informações das operações.
        :ivar id: Identificador que representa unicamente o evento.
        """

        ideEvento: DeRe.EvtPlAssistSaude.IdeEvento = field(
            metadata={
                "type": "Element",
            }
        )
        ideContrib: DeRe.EvtPlAssistSaude.IdeContrib = field(
            metadata={
                "type": "Element",
            }
        )
        idePeriodo: DeRe.EvtPlAssistSaude.IdePeriodo = field(
            metadata={
                "type": "Element",
            }
        )
        infoOper: DeRe.EvtPlAssistSaude.InfoOper = field(
            metadata={
                "type": "Element",
            }
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
            :ivar finEvt: Finalidade do evento.
            :ivar tpAmb: Identificação do ambiente para o qual os dados estão
                sendo transmitidos.
            :ivar aplicEmi: Identificação do aplicativo emissor do evento.
            :ivar verAplic: Versão do aplicativo emissor do evento.
            """

            finEvt: IdeEventoFinEvt = field(
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
            :ivar perApur: Período de apuração, sendo o ano e mês da competência
                da declaração. Máscara: AAAA-MM
            :ivar dhEmi: Data e hora de emissão do documento fiscal. Máscara:
                AAAA-MM-DDThh:mm:ss.sssTZD
            """

            perApur: str = field(
                metadata={
                    "type": "Element",
                    "length": 7,
                    "white_space": "preserve",
                    "pattern": r"20[0-9]{2}-(0[1-9]|1[0-2])",
                }
            )
            dhEmi: str = field(
                metadata={
                    "type": "Element",
                    "length": 29,
                    "white_space": "preserve",
                    "pattern": r"(((20(([02468][048])|([13579][26]))-02-29))|(20[0-9][0-9])-((((0[1-9])|(1[0-2]))-((0[1-9])|(1\d)|(2[0-8])))|((((0[13578])|(1[02]))-31)|(((0[1,3-9])|(1[0-2]))-(29|30)))))T(20|21|22|23|[0-1]\d):[0-5]\d:[0-5]\d\.[0-9]{3}([\-\+](0[0-9]|10|11):00|([\+](12):00))",
                }
            )

        @dataclass(kw_only=True)
        class InfoOper:
            """
            :ivar gOper: Grupo de operações por adquirente.
            """

            gOper: list[DeRe.EvtPlAssistSaude.InfoOper.GOper] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "min_occurs": 1,
                    "max_occurs": 1000,
                },
            )

            @dataclass(kw_only=True)
            class GOper:
                """
                :ivar chDeRE: Chave de acesso de agrupamento de operações da
                    DeRE.
                :ivar codBC: Código identificador da base de cálculo, conforme
                    [[Tabela 12 – Códigos de Bases de Cálculo]]. Validação: Deve
                    ser um código da listagem abaixo: [5010; 5020; 5030; 5050].
                :ivar chOperRef: Chave da operação objeto de cancelamento ou
                    devolução. Preenchimento: Exclusivo e obrigatório se {finEvt}
                    = [31; 41]. Validação: Deve ser uma chave válida e existente
                    no banco de dados.
                :ivar idePartes: Grupo de identificação e qualificação das partes
                    envolvidas.
                :ivar dadosOper: Grupo de informação das operações por
                    adquirente.
                """

                chDeRE: str = field(
                    metadata={
                        "type": "Element",
                        "length": 53,
                        "white_space": "preserve",
                        "pattern": r"[0-9A-Z]{10}[1-59][0-9A-Z]{24}20[0-9]{2}(0[1-9]|1[0-2])(0[1-9]|[12][0-9]|3[01])(0[1-9]|[12][0-9]|3[01])[0-9]{8}",
                    }
                )
                codBC: str = field(
                    metadata={
                        "type": "Element",
                        "length": 4,
                        "white_space": "preserve",
                        "pattern": r"[1-9][0-9A-Z]{3}",
                    }
                )
                chOperRef: None | str = field(
                    default=None,
                    metadata={
                        "type": "Element",
                        "length": 53,
                        "white_space": "preserve",
                        "pattern": r"[0-9A-Z]{10}[1-59][0-9A-Z]{24}20[0-9]{2}(0[1-9]|1[0-2])(0[1-9]|[12][0-9]|3[01])(0[1-9]|[12][0-9]|3[01])[0-9]{8}",
                    },
                )
                idePartes: DeRe.EvtPlAssistSaude.InfoOper.GOper.IdePartes = field(
                    metadata={
                        "type": "Element",
                    }
                )
                dadosOper: DeRe.EvtPlAssistSaude.InfoOper.GOper.DadosOper = field(
                    metadata={
                        "type": "Element",
                    }
                )

                @dataclass(kw_only=True)
                class IdePartes:
                    """
                    :ivar infoAdq: Informações de identificação do adquirente.
                    """

                    infoAdq: DeRe.EvtPlAssistSaude.InfoOper.GOper.IdePartes.InfoAdq = (
                        field(
                            metadata={
                                "type": "Element",
                            }
                        )
                    )

                    @dataclass(kw_only=True)
                    class InfoAdq:
                        """
                        :ivar CPF: Número de inscrição no CPF do adquirente, se
                            pessoa física. Preenchimento: Vedado se o campo
                            {CNPJ} ou grupo {adqExterior} forem informados.
                            Validação: Deve ser um CPF válido.
                        :ivar CNPJ: Número de inscrição no CNPJ do adquirente, se
                            pessoa jurídica. Preenchimento: Vedado se o campo
                            {CPF} ou o grupo {adqExterior} forem informados.
                            Validação: Deve ser um CNPJ válido.
                        :ivar cMun: Código IBGE do município do endereço do
                            adquirente, conforme informações existentes na base
                            cadastral do declarante. Preenchimento: Obrigatório
                            se {CPF} ou {CNPJ forem informados. Vedado nos demais
                            casos. Validação: Deve ser um código existente na
                            tabela de municípios do IBGE.
                        :ivar adqExterior: Identificação do adquirente residente
                            ou domiciliado no exterior. Preenchimento: Exclusivo
                            e obrigatório quando o adquirente da operação for
                            residente ou domiciliado no exterior e não possuir
                            inscrição ativa no CPF ou CNPJ no território
                            nacional.
                        """

                        CPF: None | str = field(
                            default=None,
                            metadata={
                                "type": "Element",
                                "length": 11,
                                "white_space": "preserve",
                                "pattern": r"[0-9]{11}",
                            },
                        )
                        CNPJ: None | str = field(
                            default=None,
                            metadata={
                                "type": "Element",
                                "length": 14,
                                "white_space": "preserve",
                                "pattern": r"[0-9A-Z]{12}[0-9]{2}",
                            },
                        )
                        cMun: None | str = field(
                            default=None,
                            metadata={
                                "type": "Element",
                                "length": 7,
                                "white_space": "preserve",
                                "pattern": r"[0-9]{7}",
                            },
                        )
                        adqExterior: (
                            None
                            | DeRe.EvtPlAssistSaude.InfoOper.GOper.IdePartes.InfoAdq.AdqExterior
                        ) = field(
                            default=None,
                            metadata={
                                "type": "Element",
                            },
                        )

                        @dataclass(kw_only=True)
                        class AdqExterior:
                            """
                            :ivar NIF: Número de Identificação Fiscal (NIF) do
                                adquirente estrangeiro, fornecido por órgão de
                                administração tributária no exterior.
                                Preenchimento: 1. Exclusivo e obrigatório se o
                                {cNaoNIF} não for informado; 2. Formato
                                alfanumérico, sem máscaras ou caracteres
                                especiais.
                            :ivar cNaoNIF: Código do motivo para a não informação
                                do NIF do adquirente estrangeiro. Preenchimento:
                                Exclusivo e obrigatório se o {NIF} não for
                                informado.
                            :ivar nrDocIdent: Número do documento de
                                identificação oficial no exterior (passaporte,
                                carteira de identidade estrangeira ou documento
                                oficial equivalente). Preenchimento: 1. Exclusivo
                                e obrigatório se {cNaoNIF} for informado; 2.
                                Formato alfanumérico, sem máscaras ou caracteres
                                especiais.
                            :ivar cPais: Código de identificação do país de
                                domicílio fiscal (emissor do NIF) ou de
                                residência física do adquirente residente no
                                exterior, conforme coluna “A2” da [[Tabela 15 –
                                Tabela de Países]]. Exemplo: [US; PT; AR].
                            """

                            NIF: None | str = field(
                                default=None,
                                metadata={
                                    "type": "Element",
                                    "max_length": 20,
                                    "white_space": "preserve",
                                    "pattern": r"[0-9A-Z]+",
                                },
                            )
                            cNaoNIF: None | AdqExteriorCNaoNif = field(
                                default=None,
                                metadata={
                                    "type": "Element",
                                    "white_space": "preserve",
                                },
                            )
                            nrDocIdent: None | str = field(
                                default=None,
                                metadata={
                                    "type": "Element",
                                    "max_length": 20,
                                    "white_space": "preserve",
                                    "pattern": r"[0-9A-Z]+",
                                },
                            )
                            cPais: str = field(
                                metadata={
                                    "type": "Element",
                                    "length": 2,
                                    "white_space": "preserve",
                                    "pattern": r"[A-Z]{2}",
                                }
                            )

                @dataclass(kw_only=True)
                class DadosOper:
                    """
                    :ivar detOper: Detalhamento das informações da operação
                        individualizada.
                    """

                    detOper: list[
                        DeRe.EvtPlAssistSaude.InfoOper.GOper.DadosOper.DetOper
                    ] = field(
                        default_factory=list,
                        metadata={
                            "type": "Element",
                            "min_occurs": 1,
                            "max_occurs": 999,
                        },
                    )

                    @dataclass(kw_only=True)
                    class DetOper:
                        """
                        :ivar seqRef: Número sequencial ({seq}) da chave-filha da
                            operação de origem registrada anteriormente na DeRE,
                            à qual se vincula a presente operação (ex: devolução,
                            cancelamento etc.). Preenchimento: Exclusivo e
                            obrigatório se o campo {chOperRef} for preenchido.
                            Validação: O sequencial informado deve constar como
                            ativo e associado à chave-mãe referenciada
                            ({chOperRef}) na base de dados da DeRE.
                        :ivar dhOper: Data e hora da operação (UTC). Máscara:
                            AAAA-MM-DDThh:mm:ss.sssTZD Validação: Deve estar
                            compreendida no período de apuração ({perApur}) deste
                            evento.
                        :ivar qualifOper: Grupo destinado aos atributos e
                            qualificadores específicos da transação.
                        :ivar gBC: Grupo de aferição da base de cálculo do IBS e
                            da CBS.
                        :ivar gTributos: Grupo de totalização de tributos
                            incidentes sobre a operação. Preenchimento: Exclusivo
                            e obrigatório se {codBC} = [5050].
                        :ivar seq: Número sequencial de identificação da operação
                            individualizada dentro deste agrupamento.
                            Preenchimento: Deve ser preenchido de forma
                            incremental e cronológica (de [001] a [999]). Nota:
                            Este sequencial é utilizado pela base de dados,
                            substituindo o sufixo [000] da chave-mãe do
                            agrupamento (chDeRE) para compor a chave única da
                            transação (chave-filha).
                        """

                        seqRef: None | str = field(
                            default=None,
                            metadata={
                                "type": "Element",
                                "length": 3,
                                "white_space": "preserve",
                                "pattern": r"00[1-9]|0[1-9][0-9]|[1-9][0-9]{2}",
                            },
                        )
                        dhOper: str = field(
                            metadata={
                                "type": "Element",
                                "length": 29,
                                "white_space": "preserve",
                                "pattern": r"(((20(([02468][048])|([13579][26]))-02-29))|(20[0-9][0-9])-((((0[1-9])|(1[0-2]))-((0[1-9])|(1\d)|(2[0-8])))|((((0[13578])|(1[02]))-31)|(((0[1,3-9])|(1[0-2]))-(29|30)))))T(20|21|22|23|[0-1]\d):[0-5]\d:[0-5]\d\.[0-9]{3}([\-\+](0[0-9]|10|11):00|([\+](12):00))",
                            }
                        )
                        qualifOper: DeRe.EvtPlAssistSaude.InfoOper.GOper.DadosOper.DetOper.QualifOper = field(
                            metadata={
                                "type": "Element",
                            }
                        )
                        gBC: DeRe.EvtPlAssistSaude.InfoOper.GOper.DadosOper.DetOper.GBc = field(
                            metadata={
                                "type": "Element",
                            }
                        )
                        gTributos: (
                            None
                            | DeRe.EvtPlAssistSaude.InfoOper.GOper.DadosOper.DetOper.GTributos
                        ) = field(
                            default=None,
                            metadata={
                                "type": "Element",
                            },
                        )
                        seq: str = field(
                            metadata={
                                "type": "Attribute",
                                "length": 3,
                                "white_space": "preserve",
                                "pattern": r"00[1-9]|0[1-9][0-9]|[1-9][0-9]{2}",
                            }
                        )

                        @dataclass(kw_only=True)
                        class QualifOper:
                            """
                            :ivar idContrato: Número de identificação do contrato
                                relativo à operação. Código alfanumérico que
                                identifica unicamente o contrato ou apólice de
                                saúde na base da operadora ou administradora.
                            :ivar tpContrato: Tipo de contrato.
                            :ivar CNPJEntidRelac: Número de inscrição no CNPJ da
                                outra entidade jurídica participante da relação
                                do contrato coletivo administrado. Preenchimento:
                                Exclusivo e obrigatório se {tpContrato} = [3].
                                Validação: SE {codBC} = [5050], informar o CNPJ
                                da entidade (plano ou seguro saúde); SENÃO,
                                informar o CNPJ da administradora de benefícios
                                vinculada.
                            """

                            idContrato: str = field(
                                metadata={
                                    "type": "Element",
                                    "max_length": 30,
                                    "white_space": "preserve",
                                }
                            )
                            tpContrato: QualifOperTpContrato = field(
                                metadata={
                                    "type": "Element",
                                    "white_space": "preserve",
                                }
                            )
                            CNPJEntidRelac: None | str = field(
                                default=None,
                                metadata={
                                    "type": "Element",
                                    "length": 14,
                                    "white_space": "preserve",
                                    "pattern": r"[0-9A-Z]{12}[0-9]{2}",
                                },
                            )

                        @dataclass(kw_only=True)
                        class GBc:
                            """
                            :ivar gVOper: Detalhamento do valor da operação.
                            :ivar detBC: Grupo de detalhamento da base de cálculo
                                do IBS/CBS. Preenchimento: Exclusivo e
                                obrigatório se {codBC} = [5050].
                            :ivar gIdBenef: Grupo de identificação dos
                                beneficiários de planos de assistência à saúde.
                                Preenchimento: Exclusivo e obrigatório nos
                                seguintes casos: 1. Contrato coletivo sem
                                administradora de benefícios ({tpContrato} =
                                [2]); 2. Contrato sem valor definido por usuário
                                ({tpContrato} = [4]); 3. Contrato coletivo com
                                administradora de benefícios quando o evento for
                                enviado por essa entidade ({tpContrato} = [3] E
                                {codBC} = [5050]); Vedado nos demais casos.
                            """

                            gVOper: DeRe.EvtPlAssistSaude.InfoOper.GOper.DadosOper.DetOper.GBc.GVoper = field(
                                metadata={
                                    "type": "Element",
                                }
                            )
                            detBC: (
                                None
                                | DeRe.EvtPlAssistSaude.InfoOper.GOper.DadosOper.DetOper.GBc.DetBc
                            ) = field(
                                default=None,
                                metadata={
                                    "type": "Element",
                                },
                            )
                            gIdBenef: (
                                None
                                | DeRe.EvtPlAssistSaude.InfoOper.GOper.DadosOper.DetOper.GBc.GIdBenef
                            ) = field(
                                default=None,
                                metadata={
                                    "type": "Element",
                                },
                            )

                            @dataclass(kw_only=True)
                            class GVoper:
                                """
                                :ivar vOper: Valor total recebido pela
                                    contraprestação ou prêmio de seguro saúde
                                    referente ao contrato ou, em se tratando de
                                    administradoras de benefícios, o valor da
                                    comissão recebida.
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

                            @dataclass(kw_only=True)
                            class DetBc:
                                """
                                :ivar vBCApur: Valor da base de cálculo líquida
                                    correspondente ao valor da operação ({vOper})
                                    com a exclusão dos tributos que não integram
                                    a base de cálculo (ISS e PIS/COFINS).
                                """

                                vBCApur: str = field(
                                    metadata={
                                        "type": "Element",
                                        "min_length": 4,
                                        "max_length": 18,
                                        "white_space": "preserve",
                                        "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                                    }
                                )

                            @dataclass(kw_only=True)
                            class GIdBenef:
                                """
                                :ivar detBenef: Detalhamento de beneficiários do
                                    contrato.
                                """

                                detBenef: list[
                                    DeRe.EvtPlAssistSaude.InfoOper.GOper.DadosOper.DetOper.GBc.GIdBenef.DetBenef
                                ] = field(
                                    default_factory=list,
                                    metadata={
                                        "type": "Element",
                                        "min_occurs": 1,
                                        "max_occurs": 20000,
                                    },
                                )

                                @dataclass(kw_only=True)
                                class DetBenef:
                                    """
                                    :ivar CPFTitular: Número de inscrição no CPF
                                        do beneficiário titular do plano de
                                        saúde. Preenchimento: Obrigatório se
                                        {tpContrato} = [2; 3; 4]; Vedado nos
                                        demais casos.
                                    :ivar dtNascTitular: Data de nascimento do
                                        beneficiário titular do plano de saúde.
                                        Máscara: AAAA-MM-DD Preenchimento:
                                        Obrigatório se {tpContrato} = [4]. Vedado
                                        nos demais casos.
                                    :ivar vTitularDep: Valor total relativo ao
                                        titular do plano ou seguro, incluindo
                                        seus dependentes. Preenchimento:
                                        Obrigatório se {tpContrato} = [2; 3].
                                        Vedado nos demais casos.
                                    :ivar detDependentes: Detalhamento de
                                        beneficiários dependentes vinculados.
                                        Preenchimento: Exclusivo se {tpContrato}
                                        = [4] (Plano ou seguro sem valor definido
                                        por usuário) e existirem dependentes
                                        vinculados ao titular.
                                    """

                                    CPFTitular: None | str = field(
                                        default=None,
                                        metadata={
                                            "type": "Element",
                                            "length": 11,
                                            "white_space": "preserve",
                                            "pattern": r"[0-9]{11}",
                                        },
                                    )
                                    dtNascTitular: None | str = field(
                                        default=None,
                                        metadata={
                                            "type": "Element",
                                            "length": 10,
                                            "white_space": "preserve",
                                            "pattern": r"(((20(([02468][048])|([13579][26]))-02-29))|(20[0-9][0-9])-((((0[1-9])|(1[0-2]))-((0[1-9])|(1\d)|(2[0-8])))|((((0[13578])|(1[02]))-31)|(((0[1,3-9])|(1[0-2]))-(29|30)))))",
                                        },
                                    )
                                    vTitularDep: None | str = field(
                                        default=None,
                                        metadata={
                                            "type": "Element",
                                            "min_length": 4,
                                            "max_length": 18,
                                            "white_space": "preserve",
                                            "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                                        },
                                    )
                                    detDependentes: (
                                        None
                                        | DeRe.EvtPlAssistSaude.InfoOper.GOper.DadosOper.DetOper.GBc.GIdBenef.DetBenef.DetDependentes
                                    ) = field(
                                        default=None,
                                        metadata={
                                            "type": "Element",
                                        },
                                    )

                                    @dataclass(kw_only=True)
                                    class DetDependentes:
                                        """
                                        :ivar dtNascDep: Data de nascimento do
                                            beneficiário dependente vinculado ao
                                            titular do plano de saúde. Máscara:
                                            AAAA-MM-DD
                                        """

                                        dtNascDep: list[str] = field(
                                            default_factory=list,
                                            metadata={
                                                "type": "Element",
                                                "min_occurs": 1,
                                                "max_occurs": 50,
                                                "length": 10,
                                                "white_space": "preserve",
                                                "pattern": r"(((20(([02468][048])|([13579][26]))-02-29))|(20[0-9][0-9])-((((0[1-9])|(1[0-2]))-((0[1-9])|(1\d)|(2[0-8])))|((((0[13578])|(1[02]))-31)|(((0[1,3-9])|(1[0-2]))-(29|30)))))",
                                            },
                                        )

                        @dataclass(kw_only=True)
                        class GTributos:
                            """
                            :ivar vBCTrib: Valor da base de cálculo oferecida à
                                tributação. Cálculo: {vBCTrib} = {vBCApur}
                            :ivar pIBSMunTrib: Alíquota do IBS municipal
                                incidente sobre a operação.
                            :ivar vIBSMunTrib: Valor do IBS Municipal. Cálculo:
                                {vIBSMunTrib} = {vBCTrib} * ({pIBSMunTrib} / 100)
                            :ivar pIBSUFTrib: Alíquota do IBS estadual incidente
                                sobre a operação.
                            :ivar vIBSUFTrib: Valor do IBS Estadual. Cálculo:
                                {vIBSUFTrib} = {vBCTrib} * ({pIBSUFTrib} / 100)
                            :ivar pCBSTrib: Alíquota da CBS incidente sobre a
                                operação.
                            :ivar vCBSTrib: Valor da CBS. Cálculo: {vCBSTrib} =
                                {vBCTrib} * ({pCBSTrib} / 100)
                            """

                            vBCTrib: str = field(
                                metadata={
                                    "type": "Element",
                                    "min_length": 4,
                                    "max_length": 18,
                                    "white_space": "preserve",
                                    "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                                }
                            )
                            pIBSMunTrib: str = field(
                                metadata={
                                    "type": "Element",
                                    "min_length": 8,
                                    "max_length": 10,
                                    "white_space": "preserve",
                                    "pattern": r"(0|[1-9][0-9]{0,2})\.[0-9]{6}",
                                }
                            )
                            vIBSMunTrib: str = field(
                                metadata={
                                    "type": "Element",
                                    "min_length": 4,
                                    "max_length": 18,
                                    "white_space": "preserve",
                                    "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                                }
                            )
                            pIBSUFTrib: str = field(
                                metadata={
                                    "type": "Element",
                                    "min_length": 8,
                                    "max_length": 10,
                                    "white_space": "preserve",
                                    "pattern": r"(0|[1-9][0-9]{0,2})\.[0-9]{6}",
                                }
                            )
                            vIBSUFTrib: str = field(
                                metadata={
                                    "type": "Element",
                                    "min_length": 4,
                                    "max_length": 18,
                                    "white_space": "preserve",
                                    "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                                }
                            )
                            pCBSTrib: str = field(
                                metadata={
                                    "type": "Element",
                                    "min_length": 8,
                                    "max_length": 10,
                                    "white_space": "preserve",
                                    "pattern": r"(0|[1-9][0-9]{0,2})\.[0-9]{6}",
                                }
                            )
                            vCBSTrib: str = field(
                                metadata={
                                    "type": "Element",
                                    "min_length": 4,
                                    "max_length": 18,
                                    "white_space": "preserve",
                                    "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                                }
                            )
