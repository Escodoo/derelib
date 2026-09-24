from derelib.returns import parse_return
from tests.helpers import sample_xml


def test_parse_lote_return():
    data = parse_return(sample_xml("retorno_lote.xml"))
    assert data["cdResposta"] == "2"
    assert data["descResposta"] == "Processado"
    assert data["events"]
    assert data["events"][0]["cdRetorno"] == "1"
    assert data["events"][0]["tpEv"] == "D-1001"
    assert data["events"][0]["nrRecibo"].startswith("1001-")


def test_parse_event_return_with_occurrences():
    data = parse_return(sample_xml("retorno_evento.xml"))
    assert data["cdRetorno"] == "0"
    assert data["events"]
    assert data["events"][0]["ocorrencias"][0]["codigo"] == "12"
    assert data["events"][0]["ocorrencias"][0]["localizacao"] == "plAssistSaude"


def test_parse_return_accepts_bytes():
    data = parse_return(sample_xml("retorno_evento.xml").encode("utf-8"))
    assert data["descRetorno"] == "Erro"


def test_parse_return_reads_root_id():
    xml = """<DeRE id="evt-1" xmlns="http://www.dere.gov.br/schemas/evtRetornoTabela/v1_0_1">
      <evtRetornoTabela>
        <ideStatus>
          <cdRetorno>1</cdRetorno>
          <descRetorno>Sucesso</descRetorno>
        </ideStatus>
      </evtRetornoTabela>
    </DeRE>"""
    data = parse_return(xml)
    assert data["id"] == "evt-1"


def test_parse_return_single_ocorrencia():
    xml = """<DeRE xmlns="http://www.dere.gov.br/schemas/evtRetornoTabela/v1_0_1">
      <evtRetornoTabela>
        <ideStatus>
          <cdRetorno>0</cdRetorno>
          <descRetorno>Erro</descRetorno>
        </ideStatus>
        <ocorrencia>
          <codigo>99</codigo>
          <descricao>Other</descricao>
        </ocorrencia>
      </evtRetornoTabela>
    </DeRE>"""
    data = parse_return(xml)
    assert data["ocorrencias"][0]["codigo"] == "99"
