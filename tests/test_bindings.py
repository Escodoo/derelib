from pathlib import Path

import pytest
from lxml import etree

from derelib.events import event_binding
from derelib.mixin import DereMixin
from derelib.validation import validate
from tests.helpers import EVENT_SAMPLES, SAMPLES, sample_xml


def _c14n(xml: str) -> bytes:
    root = etree.fromstring(xml.encode("utf-8") if isinstance(xml, str) else xml)
    return etree.tostring(root, method="c14n")


@pytest.mark.parametrize("event_type,filename", EVENT_SAMPLES.items())
def test_roundtrip_binding(event_type, filename):
    xml = sample_xml(filename)
    cls = event_binding(event_type)
    parsed = cls.from_xml(xml)
    serialized = parsed.to_xml()
    again = cls.from_xml(serialized)
    assert parsed == again
    assert validate(serialized, event_type) == []
    assert _c14n(parsed.to_xml(indent=None)) == _c14n(again.to_xml(indent=None))


def test_from_path_and_validate_xml():
    path = SAMPLES / "d1199.xml"
    parsed = event_binding("D-1199").from_path(str(path))
    assert parsed.evtFechMensal.ideContrib.nrInsc == "00000000"
    assert parsed.validate_xml() == []


def test_unknown_binding():
    with pytest.raises(ValueError, match="Unknown DeRE event type"):
        event_binding("D-9999")


def test_resolve_schema_path_unknown_module():
    class Dummy(DereMixin):
        pass

    Dummy.__module__ = "derelib.bindings.v1_2_0.unknown_schema"
    with pytest.raises(ValueError, match="No XSD mapped"):
        Dummy._resolve_schema_path()


def test_schema_path_override(tmp_path: Path):
    class Dummy(DereMixin):
        schema_path = str(SAMPLES / "d1199.xml")

    assert Dummy._resolve_schema_path() == Dummy.schema_path
