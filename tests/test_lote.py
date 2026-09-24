from derelib.lote import build_lote
from derelib.validation import validate_lote
from tests.helpers import sample_xml

EVENT_ID = "DeRE11991000000000000002026092416250700001"


def test_build_lote_inserts_event_as_is():
    inner = sample_xml("d1199.xml")
    lote = build_lote("00000000", [{"id": EVENT_ID, "xml": inner}])
    assert "evtFechMensal" in lote
    assert EVENT_ID in lote
    assert validate_lote(lote) == []


def test_build_lote_accepts_bytes():
    inner = sample_xml("d1199.xml").encode("utf-8")
    lote = build_lote("00000000", [{"id": EVENT_ID, "xml": inner}])
    assert validate_lote(lote) == []


def test_exported_lote_is_valid():
    assert validate_lote(sample_xml("lote.xml")) == []
