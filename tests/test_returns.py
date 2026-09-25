import pytest

from derelib.events import RETURN_D9101, return_binding
from derelib.returns import parse_return
from derelib.validation import validate, validate_return
from tests.helpers import sample_xml


def test_parse_lote_return():
    data = parse_return(sample_xml("retorno_lote.xml"))
    assert data["cdResposta"] == "2"
    assert data["descResposta"] == "Processado"
    assert data["cdRetorno"] is False
    assert data["nrRecibo"] is False
    assert data["events"]
    assert data["events"][0]["cdRetorno"] == "1"
    assert data["events"][0]["tpEv"] == "D-1001"
    assert data["events"][0]["nrRecibo"].startswith("1001-")


def test_parse_lote_return_keeps_event_fields_nested():
    xml = """<DeRE xmlns="http://www.dere.gov.br/schemas/retornoLoteDere/v1_0_1">
      <retornoLoteEventos id="IDLOTE1">
        <status>
          <cdResposta>3</cdResposta>
          <descResposta>Processado com erro</descResposta>
          <ocorrencias>
            <ocorrencia>
              <codigo>7</codigo>
              <descricao>Lot warning</descricao>
            </ocorrencia>
          </ocorrencias>
        </status>
        <dadosRecepcaoLote>
          <dhRecepcao>2026-12-05T12:00:00</dhRecepcao>
          <protocolo>2.000001.1</protocolo>
        </dadosRecepcaoLote>
        <dadosProcessamentoLote>
          <dhProcessamento>2026-12-05T12:00:01</dhProcessamento>
        </dadosProcessamentoLote>
        <retornoEventos>
          <evento id="A">
            <evtRetornoTabela xmlns="http://www.dere.gov.br/schemas/evtRetornoTabela/v1_0_1">
              <ideStatus><cdRetorno>1</cdRetorno><descRetorno>Sucesso</descRetorno></ideStatus>
              <infoRecEv><nrRecibo>1001-A</nrRecibo><tpEv>D-1001</tpEv></infoRecEv>
            </evtRetornoTabela>
          </evento>
          <evento id="B">
            <evtRetornoTabela xmlns="http://www.dere.gov.br/schemas/evtRetornoTabela/v1_0_1">
              <ideStatus><cdRetorno>0</cdRetorno><descRetorno>Erro</descRetorno></ideStatus>
              <ocorrencias><codigo>12</codigo><descricao>x</descricao></ocorrencias>
            </evtRetornoTabela>
          </evento>
        </retornoEventos>
      </retornoLoteEventos>
    </DeRE>"""
    data = parse_return(xml)
    assert data["id"] == "IDLOTE1"
    assert data["cdResposta"] == "3"
    assert data["protocolo"] == "2.000001.1"
    assert data["dhRecepcao"] == "2026-12-05T12:00:00"
    assert data["dhProcessamento"] == "2026-12-05T12:00:01"
    assert data["ocorrencias"][0]["codigo"] == "7"
    assert data["cdRetorno"] is False
    assert data["nrRecibo"] is False
    assert [event["id"] for event in data["events"]] == ["A", "B"]
    assert data["events"][0]["nrRecibo"] == "1001-A"
    assert data["events"][0]["cdRetorno"] == "1"
    assert data["events"][1]["cdRetorno"] == "0"
    assert data["events"][1]["ocorrencias"][0]["codigo"] == "12"


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


def test_parse_d9001_extract():
    data = parse_return(sample_xml("retorno_d9001.xml"))
    assert data["returnTag"] == "evtRetornoTabela"
    assert data["nrRecibo"].startswith("1001-")
    assert data["extract"]["validity"][0]["iniValid"] == "2026-10-01"
    assert data["extract"]["validity"][0]["fimValidEfetiva"] == "2026-10-31"
    assert data["extract"]["gaps"][0]["iniLacuna"] == "2026-11-01"


def test_parse_d9101_totals():
    data = parse_return(sample_xml("retorno_d9101.xml"))
    assert data["seqEvento"] == "00"
    assert data["perApur"] == "2026-10"
    assert data["nrReciboPGCC"].startswith("1011-")
    assert data["totals"][0]["codTrib"] == "110110001"
    assert data["totals"][0]["vApurTot"] == "150.00"


def test_parse_d9106_total():
    data = parse_return(sample_xml("retorno_d9106.xml"))
    assert data["totals"] == [{"vApurTot": "80.00"}]


def test_parse_d9199_taxes():
    data = parse_return(sample_xml("retorno_d9199.xml"))
    assert data["receipts"]["nrReciboBalancete"].startswith("1101-")
    assert data["taxes"]["lines"][0]["regime"] == "2"
    assert data["taxes"]["lines"][0]["codBC"] == "2101"
    assert data["taxes"]["lines"][0]["vIBSTot"] == "10.00"
    assert data["taxes"]["total"]["vCBS"] == "9.00"


def test_return_binding_roundtrip():
    cls = return_binding(RETURN_D9101)
    parsed = cls.from_xml(sample_xml("retorno_d9101.xml"))
    assert parsed.evtRetornoBalan.ideContrib.nrInsc == "00000000"
    assert parsed.evtRetornoBalan.infoEvento.idePeriodo.perApur == "2026-10"


def test_unknown_return_binding():
    with pytest.raises(ValueError, match="Unknown DeRE event type"):
        return_binding("D-9999")


def test_validate_return_samples():
    for name in (
        "retorno_d9001.xml",
        "retorno_d9101.xml",
        "retorno_d9106.xml",
        "retorno_d9199.xml",
    ):
        errors = validate_return(sample_xml(name))
        assert errors == [], (name, errors)


def test_validate_return_type_and_namespace():
    assert validate(sample_xml("retorno_d9101.xml"), RETURN_D9101) == []
    assert validate_return(sample_xml("retorno_d9001.xml")) == []
    assert (
        validate_return(
            '<DeRE xmlns="http://www.dere.gov.br/schemas/evtRetornoX/v9_9_9"/>'
        )
        is None
    )
    assert validate_return("<evtRetornoBalan/>") is None
    assert validate_return(
        '<DeRE xmlns="http://www.dere.gov.br/schemas/evtRetornoBalan/v1_0_0">'
        "<evtRetornoBalan/>"
        "</DeRE>"
    )


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
