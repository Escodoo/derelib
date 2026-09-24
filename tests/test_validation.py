import pytest

from derelib.validation import validate, validate_against_schema, validate_lote
from tests.helpers import EVENT_SAMPLES, sample_xml


@pytest.mark.parametrize("event_type,filename", EVENT_SAMPLES.items())
def test_unsigned_events_match_xsd(event_type, filename):
    errors = validate(sample_xml(filename), event_type)
    assert errors == [], errors


def test_lote_matches_xsd():
    assert validate_lote(sample_xml("lote.xml")) == []


def test_invalid_event_returns_errors():
    xml = '<DeRE xmlns="http://www.dere.gov.br/schemas/evtFechMensal/v0_0_2"><evtFechMensal/></DeRE>'
    errors = validate(xml, "D-1199")
    assert errors


def test_unknown_event_type():
    with pytest.raises(ValueError, match="Unknown DeRE event type"):
        validate("<DeRE/>", "D-9999")


def test_validate_accepts_bytes():
    payload = sample_xml("d1199.xml").encode("utf-8")
    assert validate(payload, "D-1199") == []


def test_signed_flag_rejects_unsigned_event():
    errors = validate(sample_xml("d1199.xml"), "D-1199", signed=True)
    assert errors


def test_validate_against_schema_uses_filename():
    errors = validate_against_schema(
        sample_xml("d1199.xml"),
        "evtFechMensal-v0_0_2.xsd",
    )
    assert errors == []


def test_validate_against_schema_reports_errors():
    errors = validate_against_schema(
        "<DeRE/>",
        "evtFechMensal-v0_0_2.xsd",
    )
    assert errors


def test_invalid_lote_returns_errors():
    assert validate_lote("<DeRE/>")
