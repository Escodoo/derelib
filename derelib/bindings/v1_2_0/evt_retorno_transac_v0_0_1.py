from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from derelib.bindings.v1_2_0.xmldsig_core_schema import Signature
from derelib.mixin import DereMixin

__NAMESPACE__ = "http://www.dere.gov.br/schemas/evtRetornoTransac/v0_0_1"


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

    :ivar evtRetornoTransac: Evento de retorno e recibo de processamento de
        eventos transacionais. Retorno gerado para eventos que não exijam um
        totalizador específico de cálculo.
    :ivar signature:
    """

    class Meta:
        name = "DeRE"
        namespace = "http://www.dere.gov.br/schemas/evtRetornoTransac/v0_0_1"

    evtRetornoTransac: DeRe.EvtRetornoTransac = field(
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
    class EvtRetornoTransac:
        """
        :ivar ideContrib: Informações de identificação do contribuinte.
        :ivar ideStatus: Situação do processamento do evento.
        :ivar infoRecEv: Informações de processamento dos eventos.
        :ivar infoPlanoSaude: Grupo de retorno do processamento de Planos de
            Assistência à Saúde. Preenchimento: Exclusivo quando {tpEv} =
            [D-3201] e existir campo {tpContrato} igual a [4] (Plano ou seguro
            sem valor definido por usuário).
        :ivar id: Identificação única do evento (campo id do evento transmitido
            pelo contribuinte, a que se refere este retorno).
        """

        ideContrib: DeRe.EvtRetornoTransac.IdeContrib = field(
            metadata={
                "type": "Element",
            }
        )
        ideStatus: DeRe.EvtRetornoTransac.IdeStatus = field(
            metadata={
                "type": "Element",
            }
        )
        infoRecEv: DeRe.EvtRetornoTransac.InfoRecEv = field(
            metadata={
                "type": "Element",
            }
        )
        infoPlanoSaude: None | DeRe.EvtRetornoTransac.InfoPlanoSaude = field(
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
            ocorrencias: list[DeRe.EvtRetornoTransac.IdeStatus.Ocorrencias] = field(
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
            :ivar protocoloLote: Número do protocolo de entrega do lote.
            :ivar dhRecepcao: Data e hora da recepção do evento (UTC). Máscara:
                AAAA-MM-DDThh:mm:ss.sssssssTZD
            :ivar dhProcess: Data e hora do processamento do evento (UTC).
                Máscara: AAAA-MM-DDThh:mm:ss.sssssssTZD
            :ivar tpEv: Sigla de identificação do tipo de evento. Exemplo:
                D-2201.
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
        class InfoPlanoSaude:
            """
            :ivar chDeREOper: Chave de acesso individualizada da operação da DeRE
                (chave-filha). Preenchimento: Chave de 53 caracteres que
                identifica unicamente a operação de rateio do beneficiário
                titular. Corresponde à chave-mãe do agrupamento ({chDeRE} do
                evento D-3201 de origem) com a substituição de seus 3 (três)
                últimos dígitos (sufixo aglutinador) pelo número sequencial
                ({seq}) individualizado.
            :ivar detRateioPremio: Grupo de detalhamento do rateio dos prêmios,
                individualizado por beneficiário titular. Gerado pelo sistema
                após a aplicação dos coeficientes de rateio da [[Tabela 33 –
                Coeficiente de Rateio do Prêmio não Individualizado]].
                Preenchimento: Listagem das ocorrências válidas extraídas da tag
                {CPFTitular} do evento D-3201 de origem, consolidando-as
                exclusivamente para os contratos de plano ou seguro sem valor
                definido por usuário ({tpContrato} = [4]).
            """

            chDeREOper: str = field(
                metadata={
                    "type": "Element",
                    "length": 53,
                    "white_space": "preserve",
                    "pattern": r"[0-9A-Z]{10}[1-59][0-9A-Z]{24}[0-9]{18}",
                }
            )
            detRateioPremio: list[
                DeRe.EvtRetornoTransac.InfoPlanoSaude.DetRateioPremio
            ] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "min_occurs": 1,
                    "max_occurs": 30000,
                },
            )

            @dataclass(kw_only=True)
            class DetRateioPremio:
                """
                :ivar chDeREOper: Chave de acesso individualizada da operação da
                    DeRE (chave-filha). Preenchimento: Chave de 53 caracteres que
                    identifica unicamente a operação de rateio do beneficiário
                    titular. Corresponde à chave-mãe do agrupamento ({chDeRE} do
                    evento D-3201 de origem) com a substituição de seus 3 (três)
                    últimos dígitos (sufixo aglutinador) pelo número sequencial
                    ({seq}) individualizado.
                :ivar CPFBenefTit: Número de inscrição no CPF do beneficiário
                    titular. Cálculo: Listagem de todas as ocorrências de
                    {CPFTitular} quando {tpContrato} = [4] (Plano ou seguro sem
                    valor definido por usuário).
                :ivar vPremIndivid: Valor consolidado do rateio do prêmio ou
                    contraprestação, individualizado por titular. Nota: O valor
                    alocado a cada titular será apurado pela proporção da soma
                    dos coeficientes do titular e de seus respectivos dependentes
                    em relação ao somatório dos coeficientes de todos os
                    beneficiários do contrato. Os coeficientes de alocação são
                    definidos pela faixa etária de cada pessoa no último dia da
                    competência da declaração ({perApur}). Cálculo: 1. Apurar a
                    idade em anos completos do titular e de cada dependente na
                    data do último dia do {perApur}. Identificar o coeficiente
                    individual de cada vida na [[Tabela 33 – Coeficiente de
                    Rateio do Prêmio não Individualizado]]; 2. Somar os
                    coeficientes individuais de todas as vidas do contrato para
                    obter o coeficiente total do contrato (cTotal); 3. Para cada
                    titular, somar o seu coeficiente individual ao de todos os
                    seus dependentes para obter o subcoeficiente do titular
                    (cTitular). 4. Calcular o coeficiente de rateio para cada
                    titular do contrato: cRatTit = cTitular / cTotal. 5.
                    Multiplicar o valor do contrato ({vOper}) pelo respectivo
                    cRatTit para se obter o valor individualizado vinculado a
                    este titular (e seus dependentes)
                """

                chDeREOper: str = field(
                    metadata={
                        "type": "Element",
                        "length": 53,
                        "white_space": "preserve",
                        "pattern": r"[0-9A-Z]{10}[1-59][0-9A-Z]{24}[0-9]{18}",
                    }
                )
                CPFBenefTit: str = field(
                    metadata={
                        "type": "Element",
                        "length": 11,
                        "white_space": "preserve",
                        "pattern": r"[0-9]{11}",
                    }
                )
                vPremIndivid: str = field(
                    metadata={
                        "type": "Element",
                        "min_length": 4,
                        "max_length": 18,
                        "white_space": "preserve",
                        "pattern": r"(0|[1-9][0-9]{0,14})\.[0-9]{2}",
                    }
                )
