"""XML-DSig signing for DeRE events (RSA-SHA256, enveloped)."""

from __future__ import annotations

from lxml import etree

from derelib.events import DS_NS
from derelib.xml import fromstring

C14N_ALG = "http://www.w3.org/TR/2001/REC-xml-c14n-20010315"


def _require_signxml():
    try:
        from signxml import XMLSigner, methods
    except ImportError as exc:  # pragma: no cover - optional extra
        raise RuntimeError(
            "Install derelib[sign] to sign DeRE events (signxml is required)."
        ) from exc
    return XMLSigner, methods


def _strip_whitespace(root):
    for element in root.iter("*"):
        if element.text is not None and not element.text.strip():
            element.text = None
        if element.tail is not None and not element.tail.strip():
            element.tail = None
    return root


def sign_event(xml_content, key, cert_pem, reference):
    """Sign an event XML with RSA-SHA256.

    ``key`` and ``cert_pem`` are PEM bytes or strings. ``reference`` is the
    event ``id`` attribute (without the leading ``#``).
    """
    xml_signer, methods = _require_signxml()
    root = _strip_whitespace(fromstring(xml_content))
    signer = xml_signer(
        method=methods.enveloped,
        signature_algorithm="rsa-sha256",
        digest_algorithm="sha256",
        c14n_algorithm=C14N_ALG,
    )
    signer.excise_empty_xmlns_declarations = True
    signed_root = signer.sign(
        root,
        key=key,
        cert=cert_pem,
        reference_uri=f"#{reference}",
        id_attribute="id",
    )
    event_node = signed_root.find(f".//*[@id='{reference}']")
    signature = signed_root.find(f".//{{{DS_NS}}}Signature")
    if event_node is not None and signature is not None:
        parent = event_node.getparent()
        if parent is not None and signature.getparent() is not parent:
            parent.append(signature)
    return etree.tostring(signed_root, encoding="unicode")


def sign_event_with_certificate(xml_content, certificado, reference):
    """Sign using an ``erpbrasil.assinatura`` certificate object."""
    cert_pem = certificado.cert_chave()[0]
    return sign_event(xml_content, certificado.key, cert_pem, reference)
