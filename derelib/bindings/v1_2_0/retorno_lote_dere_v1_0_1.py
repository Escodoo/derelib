from __future__ import annotations

from dataclasses import dataclass, field

from xsdata.models.datatype import XmlDateTime

from derelib.bindings.v1_2_0.xmldsig_core_schema import Signature
from derelib.mixin import DereMixin

__NAMESPACE__ = "http://www.dere.gov.br/schemas/retornoLoteDere/v1_0_1"


@dataclass(kw_only=True)
class TdadosProcessamento:
    """
    Define os dados de processamento de um lote de eventos.

    :ivar dhProcessamento: Data hora processamento.
    :ivar versaoAplicativoProcessamento: Versao do aplicativo de processamento do
        lote
    """

    class Meta:
        name = "TDadosProcessamento"

    dhProcessamento: XmlDateTime = field(
        metadata={
            "type": "Element",
            "namespace": "http://www.dere.gov.br/schemas/retornoLoteDere/v1_0_1",
        }
    )
    versaoAplicativoProcessamento: None | str = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.dere.gov.br/schemas/retornoLoteDere/v1_0_1",
            "max_length": 20,
        },
    )


@dataclass(kw_only=True)
class TdadosRecepcao:
    """
    Define os dados de recepcao do lote.

    :ivar dhRecepcao: Data hora recepcao
    :ivar versaoAplicativoRecepcao: Versao do aplicativo de recepcao
    :ivar protocolo: Protocolo gerado na recepcao do lote
    """

    class Meta:
        name = "TDadosRecepcao"

    dhRecepcao: XmlDateTime = field(
        metadata={
            "type": "Element",
            "namespace": "http://www.dere.gov.br/schemas/retornoLoteDere/v1_0_1",
        }
    )
    versaoAplicativoRecepcao: str = field(
        metadata={
            "type": "Element",
            "namespace": "http://www.dere.gov.br/schemas/retornoLoteDere/v1_0_1",
            "max_length": 20,
        }
    )
    protocolo: str = field(
        metadata={
            "type": "Element",
            "namespace": "http://www.dere.gov.br/schemas/retornoLoteDere/v1_0_1",
            "max_length": 28,
        }
    )


@dataclass(kw_only=True)
class TeventoDere:
    """
    Define os dados de um evento da DERE.

    :ivar any_element: Contem xml com o retorno do processamento do evento
        (conforme XSD de retorno do Evento)
    :ivar id: Contem chave de acesso do evento
    """

    class Meta:
        name = "TEventoDere"

    any_element: None | object = field(
        default=None,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "process_contents": "skip",
        },
    )
    id: str = field(
        metadata={
            "type": "Attribute",
        }
    )


@dataclass(kw_only=True)
class Tocorrencias:
    """
    Define as ocorrencias encontradas na validacao.
    """

    class Meta:
        name = "TOcorrencias"

    ocorrencia: list[Tocorrencias.Ocorrencia] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.dere.gov.br/schemas/retornoLoteDere/v1_0_1",
            "min_occurs": 1,
            "max_occurs": 10,
        },
    )

    @dataclass(kw_only=True)
    class Ocorrencia:
        """
        :ivar codigo: Codigo da ocorrencia
        :ivar descricao: Descricao da ocorrencia
        :ivar tipo: Contem o tipo da ocorrencia: 1 - Erro, 2 - Advertencia
        :ivar localizacao: Contem informacoes de onde no arquivo ocorreu o erro
        """

        codigo: str = field(
            metadata={
                "type": "Element",
                "namespace": "http://www.dere.gov.br/schemas/retornoLoteDere/v1_0_1",
                "max_length": 6,
            }
        )
        descricao: str = field(
            metadata={
                "type": "Element",
                "namespace": "http://www.dere.gov.br/schemas/retornoLoteDere/v1_0_1",
                "max_length": 2048,
            }
        )
        tipo: int = field(
            metadata={
                "type": "Element",
                "namespace": "http://www.dere.gov.br/schemas/retornoLoteDere/v1_0_1",
            }
        )
        localizacao: None | str = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "http://www.dere.gov.br/schemas/retornoLoteDere/v1_0_1",
                "max_length": 2048,
            },
        )


@dataclass(kw_only=True)
class Tstatus:
    """
    Contem o status atual do lote.

    :ivar cdResposta: Codigo de resposta do processamento do lote 1 - O lote esta
        aguardando processamento 2 - Lote processado com sucesso - Todos eventos
        processados com sucesso 3 - Lote processado com sucesso - Possui um ou
        mais eventos com ocorrências de erro 4 - Consulta nao executada -
        Verificar ocorrencias 5 - Consulta executada - Lote nao encontrado com o
        protocolo informado 7 - Lote nao recebido - Verificar ocorrencias 9 -
        Ocorreu um erro interno na aplicacao. Retornado um identificador do erro
        para acionamento ao Fale Conosco.
    :ivar descResposta: Contem a descricao correspondente ao codigo de resposta
    :ivar ocorrencias: Contem as ocorrencias encontradas durante a validacao
    """

    class Meta:
        name = "TStatus"

    cdResposta: int = field(
        metadata={
            "type": "Element",
            "namespace": "http://www.dere.gov.br/schemas/retornoLoteDere/v1_0_1",
        }
    )
    descResposta: str = field(
        metadata={
            "type": "Element",
            "namespace": "http://www.dere.gov.br/schemas/retornoLoteDere/v1_0_1",
            "max_length": 2048,
        }
    )
    ocorrencias: None | Tocorrencias = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.dere.gov.br/schemas/retornoLoteDere/v1_0_1",
        },
    )


@dataclass(kw_only=True)
class DeRe(DereMixin):
    """
    :ivar retornoLoteEventos: Retorno da recepcao/processamento do lote
    :ivar signature:
    """

    class Meta:
        name = "DeRE"
        namespace = "http://www.dere.gov.br/schemas/retornoLoteDere/v1_0_1"

    retornoLoteEventos: DeRe.RetornoLoteEventos = field(
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
    class RetornoLoteEventos:
        """
        :ivar ideContrib: Identificacao do Contribuinte
        :ivar ideTransmissor:
        :ivar status: Contem o status atual do lote
        :ivar dadosRecepcaoLote: Contem os dados de recepcao do lote
        :ivar dadosProcessamentoLote: Contem os dados de processamento do lote
        :ivar retornoEventos: Contem o(s) resultado(s) do processamento dos
            eventos do lote
        :ivar id: Identificacao unica
        """

        ideContrib: DeRe.RetornoLoteEventos.IdeContrib = field(
            metadata={
                "type": "Element",
            }
        )
        ideTransmissor: DeRe.RetornoLoteEventos.IdeTransmissor = field(
            metadata={
                "type": "Element",
            }
        )
        status: Tstatus = field(
            metadata={
                "type": "Element",
            }
        )
        dadosRecepcaoLote: None | TdadosRecepcao = field(
            default=None,
            metadata={
                "type": "Element",
            },
        )
        dadosProcessamentoLote: None | TdadosProcessamento = field(
            default=None,
            metadata={
                "type": "Element",
            },
        )
        retornoEventos: None | DeRe.RetornoLoteEventos.RetornoEventos = field(
            default=None,
            metadata={
                "type": "Element",
            },
        )
        id: str = field(
            metadata={
                "type": "Attribute",
            }
        )

        @dataclass(kw_only=True)
        class IdeContrib:
            nrInsc: str = field(
                metadata={
                    "type": "Element",
                    "max_length": 8,
                    "pattern": r"[0-9A-Z]{8}",
                }
            )

        @dataclass(kw_only=True)
        class IdeTransmissor:
            """
            :ivar niTransmissor: Numero Inscricao do Transmissor
            """

            niTransmissor: str = field(
                metadata={
                    "type": "Element",
                    "min_length": 1,
                    "max_length": 14,
                }
            )

        @dataclass(kw_only=True)
        class RetornoEventos:
            evento: list[TeventoDere] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "min_occurs": 1,
                    "max_occurs": 50,
                },
            )
