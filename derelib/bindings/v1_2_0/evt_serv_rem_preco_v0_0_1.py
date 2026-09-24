from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from derelib.bindings.v1_2_0.xmldsig_core_schema import Signature
from derelib.mixin import DereMixin

__NAMESPACE__ = "http://www.dere.gov.br/schemas/evtServRemPreco/v0_0_1"


class AdqExteriorCNaoNif(Enum):
    """
    :cvar VALUE_1: Dispensado de NIF
    :cvar VALUE_2: Não exigência de NIF
    """

    VALUE_1 = "1"
    VALUE_2 = "2"


class DestExteriorCNaoNifdest(Enum):
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


@dataclass(kw_only=True)
class DeRe(DereMixin):
    """
    Envelope raiz dos eventos da DeRE.

    :ivar evtServRemPreco: Evento de identificação e detalhamento de serviços
        remunerados por preço. Validação: Evento exclusivo e obrigatório para o
        registro de operações cujos códigos de base de cálculo ({codBC})
        correspondam a um dos seguintes valores: [1015; 1020; 1205; 1210; 1225;
        1230; 1805; 1810; 2005; 2010; 2015; 2020; 2210; 2805; 2810; 3605; 3610;
        3615; 3620; 3625; 3630; 3635; 3640; 3805; 3810; 4005; 4010].
    :ivar signature:
    """

    class Meta:
        name = "DeRE"
        namespace = "http://www.dere.gov.br/schemas/evtServRemPreco/v0_0_1"

    evtServRemPreco: DeRe.EvtServRemPreco = field(
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
    class EvtServRemPreco:
        """
        :ivar ideEvento: Informações de identificação do evento.
        :ivar ideContrib: Informações de identificação do contribuinte.
        :ivar idePeriodo: Período de referência das informações do evento.
        :ivar infoOper: Informações das operações.
        :ivar id: Identificador que representa unicamente o evento.
        """

        ideEvento: DeRe.EvtServRemPreco.IdeEvento = field(
            metadata={
                "type": "Element",
            }
        )
        ideContrib: DeRe.EvtServRemPreco.IdeContrib = field(
            metadata={
                "type": "Element",
            }
        )
        idePeriodo: DeRe.EvtServRemPreco.IdePeriodo = field(
            metadata={
                "type": "Element",
            }
        )
        infoOper: DeRe.EvtServRemPreco.InfoOper = field(
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

            gOper: list[DeRe.EvtServRemPreco.InfoOper.GOper] = field(
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
                    ser um código da listagem abaixo: [1015; 1020; 1205; 1210;
                    1225; 1230; 1805; 1810; 2005; 2010; 2015; 2020; 2210; 2805;
                    2810; 3605; 3610; 3615; 3620; 3625; 3630; 3635; 3640; 3805;
                    3810; 4005; 4010].
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
                idePartes: DeRe.EvtServRemPreco.InfoOper.GOper.IdePartes = field(
                    metadata={
                        "type": "Element",
                    }
                )
                dadosOper: DeRe.EvtServRemPreco.InfoOper.GOper.DadosOper = field(
                    metadata={
                        "type": "Element",
                    }
                )

                @dataclass(kw_only=True)
                class IdePartes:
                    """
                    :ivar infoAdq: Informações de identificação do adquirente.
                    """

                    infoAdq: DeRe.EvtServRemPreco.InfoOper.GOper.IdePartes.InfoAdq = (
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
                            | DeRe.EvtServRemPreco.InfoOper.GOper.IdePartes.InfoAdq.AdqExterior
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
                        individualizada. Nota: As operações são informadas
                        individualmente. Na existência de destinatários em
                        operações de intermediação, cada {detOper} pode conter um
                        único destinatário.
                    """

                    detOper: list[
                        DeRe.EvtServRemPreco.InfoOper.GOper.DadosOper.DetOper
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
                        :ivar infoDest: Informações do destinatário da operação
                            individualizada. Preenchimento: Exclusivo quando
                            {codBC} = [3605; 3610; 3615; 3620; 3625; 3630; 3635;
                            3640] (intermediação de negócios). Validação: Caso
                            exista um ou mais {infoDest} dentro do grupo
                            {dadosOper}, é obrigatório que todas as ocorrências
                            de {detOper} tenham {infoDest}. Se o contribuinte
                            tiver operações com e sem destinatário, deverá enviar
                            em eventos separados.
                        :ivar gBC: Grupo de aferição da base de cálculo do IBS e
                            da CBS.
                        :ivar gTributos: Grupo de totalização de tributos
                            incidentes sobre a operação.
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
                        infoDest: (
                            None
                            | DeRe.EvtServRemPreco.InfoOper.GOper.DadosOper.DetOper.InfoDest
                        ) = field(
                            default=None,
                            metadata={
                                "type": "Element",
                            },
                        )
                        gBC: DeRe.EvtServRemPreco.InfoOper.GOper.DadosOper.DetOper.GBc = field(
                            metadata={
                                "type": "Element",
                            }
                        )
                        gTributos: DeRe.EvtServRemPreco.InfoOper.GOper.DadosOper.DetOper.GTributos = field(
                            metadata={
                                "type": "Element",
                            }
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
                        class InfoDest:
                            """
                            :ivar CPFDest: Número de inscrição no CPF do
                                destinatário do serviço, se pessoa física.
                                Preenchimento: Vedado se o campo {CNPJDest} ou
                                grupo {destExterior} forem informados. Validação:
                                Deve ser um CPF válido.
                            :ivar CNPJDest: Número de inscrição no CNPJ do
                                destinatário do serviço, se pessoa jurídica.
                                Preenchimento: Vedado se o campo {CPFDest} ou o
                                grupo {destExterior} forem informados. Validação:
                                Deve ser um CNPJ válido.
                            :ivar cMunDest: Código IBGE do município do endereço
                                do destinatário, conforme informações existentes
                                na base cadastral do declarante. Preenchimento:
                                Obrigatório se {CPFDest} ou {CNPJDest} forem
                                informados. Vedado nos demais casos. Validação:
                                Deve ser um código existente na tabela de
                                municípios do IBGE.
                            :ivar destExterior: Identificação do destinatário
                                residente ou domiciliado no exterior.
                                Preenchimento: Exclusivo e obrigatório quando o
                                destinatário da operação for residente ou
                                domiciliado no exterior e não possuir inscrição
                                ativa no CPF ou CNPJ no território nacional.
                            """

                            CPFDest: None | str = field(
                                default=None,
                                metadata={
                                    "type": "Element",
                                    "length": 11,
                                    "white_space": "preserve",
                                    "pattern": r"[0-9]{11}",
                                },
                            )
                            CNPJDest: None | str = field(
                                default=None,
                                metadata={
                                    "type": "Element",
                                    "length": 14,
                                    "white_space": "preserve",
                                    "pattern": r"[0-9A-Z]{12}[0-9]{2}",
                                },
                            )
                            cMunDest: None | str = field(
                                default=None,
                                metadata={
                                    "type": "Element",
                                    "length": 7,
                                    "white_space": "preserve",
                                    "pattern": r"[0-9]{7}",
                                },
                            )
                            destExterior: (
                                None
                                | DeRe.EvtServRemPreco.InfoOper.GOper.DadosOper.DetOper.InfoDest.DestExterior
                            ) = field(
                                default=None,
                                metadata={
                                    "type": "Element",
                                },
                            )

                            @dataclass(kw_only=True)
                            class DestExterior:
                                """
                                :ivar NIFDest: Número de Identificação Fiscal
                                    (NIF) do destinatário estrangeiro, fornecido
                                    por órgão de administração tributária no
                                    exterior. Preenchimento: 1. Exclusivo e
                                    obrigatório se o {cNaoNIFDest} não for
                                    informado; 2. Formato alfanumérico, sem
                                    máscaras ou caracteres especiais.
                                :ivar cNaoNIFDest: Código do motivo para a não
                                    informação do NIF do destinatário
                                    estrangeiro. Preenchimento: Exclusivo e
                                    obrigatório se o {NIFDest} não for informado.
                                :ivar nrDocIdentDest: Número do documento de
                                    identificação oficial no exterior
                                    (passaporte, carteira de identidade
                                    estrangeira ou documento oficial
                                    equivalente). Preenchimento: 1. Exclusivo e
                                    obrigatório se {cNaoNIFDest} for informado;
                                    2. Formato alfanumérico, sem máscaras ou
                                    caracteres especiais.
                                :ivar cPaisDest: Código de identificação do país
                                    de domicílio fiscal (emissor do NIF) ou de
                                    residência física do destinatário residente
                                    no exterior, conforme coluna “A2” da [[Tabela
                                    15 – Tabela de Países]]. Exemplo: [US; PT;
                                    AR].
                                """

                                NIFDest: None | str = field(
                                    default=None,
                                    metadata={
                                        "type": "Element",
                                        "max_length": 20,
                                        "white_space": "preserve",
                                        "pattern": r"[0-9A-Z]+",
                                    },
                                )
                                cNaoNIFDest: None | DestExteriorCNaoNifdest = field(
                                    default=None,
                                    metadata={
                                        "type": "Element",
                                        "white_space": "preserve",
                                    },
                                )
                                nrDocIdentDest: None | str = field(
                                    default=None,
                                    metadata={
                                        "type": "Element",
                                        "max_length": 20,
                                        "white_space": "preserve",
                                        "pattern": r"[0-9A-Z]+",
                                    },
                                )
                                cPaisDest: str = field(
                                    metadata={
                                        "type": "Element",
                                        "length": 2,
                                        "white_space": "preserve",
                                        "pattern": r"[A-Z]{2}",
                                    }
                                )

                        @dataclass(kw_only=True)
                        class GBc:
                            """
                            :ivar vBCApur: Valor da base de cálculo líquida
                                correspondente à operação, obtido após a exclusão
                                dos tributos que não integram a base de cálculo
                                (ISS e PIS/COFINS), deduzidas as parcelas e
                                custos permitidos pela legislação e aplicado o
                                gross-down para exclusão dos tributos embutidos,
                                se aplicável.
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
