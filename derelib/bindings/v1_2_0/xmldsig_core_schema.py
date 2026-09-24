from __future__ import annotations

from dataclasses import dataclass, field

__NAMESPACE__ = "http://www.w3.org/2000/09/xmldsig#"


@dataclass(kw_only=True)
class CanonicalizationMethodType:
    Algorithm: str = field(
        metadata={
            "type": "Attribute",
        }
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        },
    )


@dataclass(kw_only=True)
class DsakeyValueType:
    class Meta:
        name = "DSAKeyValueType"

    P: None | bytes = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.w3.org/2000/09/xmldsig#",
            "format": "base64",
        },
    )
    Q: None | bytes = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.w3.org/2000/09/xmldsig#",
            "format": "base64",
        },
    )
    G: None | bytes = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.w3.org/2000/09/xmldsig#",
            "format": "base64",
        },
    )
    Y: bytes = field(
        metadata={
            "type": "Element",
            "namespace": "http://www.w3.org/2000/09/xmldsig#",
            "format": "base64",
        }
    )
    J: None | bytes = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.w3.org/2000/09/xmldsig#",
            "format": "base64",
        },
    )
    Seed: None | bytes = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.w3.org/2000/09/xmldsig#",
            "format": "base64",
        },
    )
    PgenCounter: None | bytes = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.w3.org/2000/09/xmldsig#",
            "format": "base64",
        },
    )


@dataclass(kw_only=True)
class DigestMethodType:
    Algorithm: str = field(
        metadata={
            "type": "Attribute",
        }
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        },
    )


@dataclass(kw_only=True)
class DigestValue:
    class Meta:
        namespace = "http://www.w3.org/2000/09/xmldsig#"

    value: bytes = field(
        default=b"",
        metadata={
            "format": "base64",
        },
    )


@dataclass(kw_only=True)
class KeyName:
    class Meta:
        namespace = "http://www.w3.org/2000/09/xmldsig#"

    value: str = field(default="")


@dataclass(kw_only=True)
class MgmtData:
    class Meta:
        namespace = "http://www.w3.org/2000/09/xmldsig#"

    value: str = field(default="")


@dataclass(kw_only=True)
class ObjectType:
    Id: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    MimeType: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    Encoding: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        },
    )


@dataclass(kw_only=True)
class PgpdataType:
    class Meta:
        name = "PGPDataType"

    PGPKeyID: None | bytes = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.w3.org/2000/09/xmldsig#",
            "format": "base64",
        },
    )
    PGPKeyPacket: list[bytes] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.w3.org/2000/09/xmldsig#",
            "max_occurs": 2,
            "format": "base64",
        },
    )
    other_element: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##other",
        },
    )


@dataclass(kw_only=True)
class RsakeyValueType:
    class Meta:
        name = "RSAKeyValueType"

    Modulus: bytes = field(
        metadata={
            "type": "Element",
            "namespace": "http://www.w3.org/2000/09/xmldsig#",
            "format": "base64",
        }
    )
    Exponent: bytes = field(
        metadata={
            "type": "Element",
            "namespace": "http://www.w3.org/2000/09/xmldsig#",
            "format": "base64",
        }
    )


@dataclass(kw_only=True)
class SpkidataType:
    class Meta:
        name = "SPKIDataType"

    SPKISexp: list[bytes] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.w3.org/2000/09/xmldsig#",
            "min_occurs": 1,
            "sequence": 1,
            "format": "base64",
        },
    )
    other_element: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##other",
            "sequence": 1,
        },
    )


@dataclass(kw_only=True)
class SignatureMethodType:
    Algorithm: str = field(
        metadata={
            "type": "Attribute",
        }
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "HMACOutputLength",
                    "type": int,
                    "namespace": "http://www.w3.org/2000/09/xmldsig#",
                },
            ),
        },
    )


@dataclass(kw_only=True)
class SignaturePropertyType:
    Target: str = field(
        metadata={
            "type": "Attribute",
        }
    )
    Id: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        },
    )


@dataclass(kw_only=True)
class SignatureValueType:
    value: bytes = field(
        default=b"",
        metadata={
            "format": "base64",
        },
    )
    Id: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class TransformType:
    Algorithm: str = field(
        metadata={
            "type": "Attribute",
        }
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "XPath",
                    "type": str,
                    "namespace": "http://www.w3.org/2000/09/xmldsig#",
                },
            ),
        },
    )


@dataclass(kw_only=True)
class X509IssuerSerialType:
    X509IssuerName: str = field(
        metadata={
            "type": "Element",
            "namespace": "http://www.w3.org/2000/09/xmldsig#",
        }
    )
    X509SerialNumber: int = field(
        metadata={
            "type": "Element",
            "namespace": "http://www.w3.org/2000/09/xmldsig#",
        }
    )


@dataclass(kw_only=True)
class CanonicalizationMethod(CanonicalizationMethodType):
    class Meta:
        namespace = "http://www.w3.org/2000/09/xmldsig#"


@dataclass(kw_only=True)
class DsakeyValue(DsakeyValueType):
    class Meta:
        name = "DSAKeyValue"
        namespace = "http://www.w3.org/2000/09/xmldsig#"


@dataclass(kw_only=True)
class DigestMethod(DigestMethodType):
    class Meta:
        namespace = "http://www.w3.org/2000/09/xmldsig#"


@dataclass(kw_only=True)
class _Object(ObjectType):
    class Meta:
        name = "Object"
        namespace = "http://www.w3.org/2000/09/xmldsig#"


@dataclass(kw_only=True)
class Pgpdata(PgpdataType):
    class Meta:
        name = "PGPData"
        namespace = "http://www.w3.org/2000/09/xmldsig#"


@dataclass(kw_only=True)
class RsakeyValue(RsakeyValueType):
    class Meta:
        name = "RSAKeyValue"
        namespace = "http://www.w3.org/2000/09/xmldsig#"


@dataclass(kw_only=True)
class Spkidata(SpkidataType):
    class Meta:
        name = "SPKIData"
        namespace = "http://www.w3.org/2000/09/xmldsig#"


@dataclass(kw_only=True)
class SignatureMethod(SignatureMethodType):
    class Meta:
        namespace = "http://www.w3.org/2000/09/xmldsig#"


@dataclass(kw_only=True)
class SignatureProperty(SignaturePropertyType):
    class Meta:
        namespace = "http://www.w3.org/2000/09/xmldsig#"


@dataclass(kw_only=True)
class SignatureValue(SignatureValueType):
    class Meta:
        namespace = "http://www.w3.org/2000/09/xmldsig#"


@dataclass(kw_only=True)
class Transform(TransformType):
    class Meta:
        namespace = "http://www.w3.org/2000/09/xmldsig#"


@dataclass(kw_only=True)
class X509DataType:
    X509IssuerSerial: list[X509IssuerSerialType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.w3.org/2000/09/xmldsig#",
            "sequence": 1,
        },
    )
    X509SKI: list[bytes] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.w3.org/2000/09/xmldsig#",
            "sequence": 1,
            "format": "base64",
        },
    )
    X509SubjectName: list[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.w3.org/2000/09/xmldsig#",
            "sequence": 1,
        },
    )
    X509Certificate: list[bytes] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.w3.org/2000/09/xmldsig#",
            "sequence": 1,
            "format": "base64",
        },
    )
    X509CRL: list[bytes] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.w3.org/2000/09/xmldsig#",
            "sequence": 1,
            "format": "base64",
        },
    )
    other_element: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##other",
            "sequence": 1,
        },
    )


@dataclass(kw_only=True)
class KeyValueType:
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "DSAKeyValue",
                    "type": DsakeyValue,
                    "namespace": "http://www.w3.org/2000/09/xmldsig#",
                },
                {
                    "name": "RSAKeyValue",
                    "type": RsakeyValue,
                    "namespace": "http://www.w3.org/2000/09/xmldsig#",
                },
            ),
        },
    )


@dataclass(kw_only=True)
class SignaturePropertiesType:
    signatureProperty: list[SignatureProperty] = field(
        default_factory=list,
        metadata={
            "name": "SignatureProperty",
            "type": "Element",
            "namespace": "http://www.w3.org/2000/09/xmldsig#",
            "min_occurs": 1,
        },
    )
    Id: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class TransformsType:
    transform: list[Transform] = field(
        default_factory=list,
        metadata={
            "name": "Transform",
            "type": "Element",
            "namespace": "http://www.w3.org/2000/09/xmldsig#",
            "min_occurs": 1,
        },
    )


@dataclass(kw_only=True)
class X509Data(X509DataType):
    class Meta:
        namespace = "http://www.w3.org/2000/09/xmldsig#"


@dataclass(kw_only=True)
class KeyValue(KeyValueType):
    class Meta:
        namespace = "http://www.w3.org/2000/09/xmldsig#"


@dataclass(kw_only=True)
class SignatureProperties(SignaturePropertiesType):
    class Meta:
        namespace = "http://www.w3.org/2000/09/xmldsig#"


@dataclass(kw_only=True)
class Transforms(TransformsType):
    class Meta:
        namespace = "http://www.w3.org/2000/09/xmldsig#"


@dataclass(kw_only=True)
class ReferenceType:
    transforms: None | Transforms = field(
        default=None,
        metadata={
            "name": "Transforms",
            "type": "Element",
            "namespace": "http://www.w3.org/2000/09/xmldsig#",
        },
    )
    digestMethod: DigestMethod = field(
        metadata={
            "name": "DigestMethod",
            "type": "Element",
            "namespace": "http://www.w3.org/2000/09/xmldsig#",
        }
    )
    digestValue: DigestValue = field(
        metadata={
            "name": "DigestValue",
            "type": "Element",
            "namespace": "http://www.w3.org/2000/09/xmldsig#",
        }
    )
    Id: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    URI: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    Type: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class RetrievalMethodType:
    transforms: None | Transforms = field(
        default=None,
        metadata={
            "name": "Transforms",
            "type": "Element",
            "namespace": "http://www.w3.org/2000/09/xmldsig#",
        },
    )
    URI: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    Type: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Reference(ReferenceType):
    class Meta:
        namespace = "http://www.w3.org/2000/09/xmldsig#"


@dataclass(kw_only=True)
class RetrievalMethod(RetrievalMethodType):
    class Meta:
        namespace = "http://www.w3.org/2000/09/xmldsig#"


@dataclass(kw_only=True)
class KeyInfoType:
    Id: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "KeyName",
                    "type": KeyName,
                    "namespace": "http://www.w3.org/2000/09/xmldsig#",
                },
                {
                    "name": "KeyValue",
                    "type": KeyValue,
                    "namespace": "http://www.w3.org/2000/09/xmldsig#",
                },
                {
                    "name": "RetrievalMethod",
                    "type": RetrievalMethod,
                    "namespace": "http://www.w3.org/2000/09/xmldsig#",
                },
                {
                    "name": "X509Data",
                    "type": X509Data,
                    "namespace": "http://www.w3.org/2000/09/xmldsig#",
                },
                {
                    "name": "PGPData",
                    "type": Pgpdata,
                    "namespace": "http://www.w3.org/2000/09/xmldsig#",
                },
                {
                    "name": "SPKIData",
                    "type": Spkidata,
                    "namespace": "http://www.w3.org/2000/09/xmldsig#",
                },
                {
                    "name": "MgmtData",
                    "type": MgmtData,
                    "namespace": "http://www.w3.org/2000/09/xmldsig#",
                },
            ),
        },
    )


@dataclass(kw_only=True)
class ManifestType:
    reference: list[Reference] = field(
        default_factory=list,
        metadata={
            "name": "Reference",
            "type": "Element",
            "namespace": "http://www.w3.org/2000/09/xmldsig#",
            "min_occurs": 1,
        },
    )
    Id: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class SignedInfoType:
    canonicalizationMethod: CanonicalizationMethod = field(
        metadata={
            "name": "CanonicalizationMethod",
            "type": "Element",
            "namespace": "http://www.w3.org/2000/09/xmldsig#",
        }
    )
    signatureMethod: SignatureMethod = field(
        metadata={
            "name": "SignatureMethod",
            "type": "Element",
            "namespace": "http://www.w3.org/2000/09/xmldsig#",
        }
    )
    reference: list[Reference] = field(
        default_factory=list,
        metadata={
            "name": "Reference",
            "type": "Element",
            "namespace": "http://www.w3.org/2000/09/xmldsig#",
            "min_occurs": 1,
        },
    )
    Id: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class KeyInfo(KeyInfoType):
    class Meta:
        namespace = "http://www.w3.org/2000/09/xmldsig#"


@dataclass(kw_only=True)
class Manifest(ManifestType):
    class Meta:
        namespace = "http://www.w3.org/2000/09/xmldsig#"


@dataclass(kw_only=True)
class SignedInfo(SignedInfoType):
    class Meta:
        namespace = "http://www.w3.org/2000/09/xmldsig#"


@dataclass(kw_only=True)
class SignatureType:
    signedInfo: SignedInfo = field(
        metadata={
            "name": "SignedInfo",
            "type": "Element",
            "namespace": "http://www.w3.org/2000/09/xmldsig#",
        }
    )
    signatureValue: SignatureValue = field(
        metadata={
            "name": "SignatureValue",
            "type": "Element",
            "namespace": "http://www.w3.org/2000/09/xmldsig#",
        }
    )
    keyInfo: None | KeyInfo = field(
        default=None,
        metadata={
            "name": "KeyInfo",
            "type": "Element",
            "namespace": "http://www.w3.org/2000/09/xmldsig#",
        },
    )
    Object: list[_Object] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.w3.org/2000/09/xmldsig#",
        },
    )
    Id: None | str = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class Signature(SignatureType):
    class Meta:
        namespace = "http://www.w3.org/2000/09/xmldsig#"
