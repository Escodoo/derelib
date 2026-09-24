from types import SimpleNamespace

import pytest

from derelib.signing import sign_event, sign_event_with_certificate
from derelib.validation import validate
from tests.helpers import sample_xml

REFERENCE = "DeRE11991000000000000002026092416250700001"


def test_sign_event_and_verify(rsa_material):
    from signxml import XMLVerifier

    key_pem, cert_pem = rsa_material
    signed = sign_event(sample_xml("d1199.xml"), key_pem, cert_pem, REFERENCE)
    assert "Signature" in signed
    assert validate(signed, "D-1199", signed=True) == []
    XMLVerifier().verify(signed, x509_cert=cert_pem)
    assert validate(signed, "D-1199") == []


def test_sign_event_with_certificate(rsa_material):
    key_pem, cert_pem = rsa_material
    certificado = SimpleNamespace(key=key_pem, cert_chave=lambda: (cert_pem, None))
    signed = sign_event_with_certificate(
        sample_xml("d1199.xml"), certificado, REFERENCE
    )
    assert "SignatureValue" in signed


def test_sign_event_accepts_bytes(rsa_material):
    key_pem, cert_pem = rsa_material
    signed = sign_event(
        sample_xml("d1199.xml").encode("utf-8"),
        key_pem,
        cert_pem,
        REFERENCE,
    )
    assert signed.startswith("<")


def test_mixin_sign_xml(rsa_material):
    from derelib.events import event_binding

    key_pem, cert_pem = rsa_material
    parsed = event_binding("D-1199").from_xml(sample_xml("d1199.xml"))
    signed = parsed.sign_xml(key_pem, cert_pem, REFERENCE)
    assert "Signature" in signed


def test_missing_signxml(monkeypatch):
    import builtins

    real_import = builtins.__import__

    def fake_import(name, *args, **kwargs):
        if name == "signxml" or name.startswith("signxml."):
            raise ImportError("no signxml")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", fake_import)
    with pytest.raises(RuntimeError, match="derelib\\[sign\\]"):
        sign_event("<DeRE/>", b"key", b"cert", "id")
