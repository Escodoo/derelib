"""derelib: xsdata binding for the Brazilian DeRE layout."""

from derelib.events import (
    EVENT_D1001,
    EVENT_D1011,
    EVENT_D1101,
    EVENT_D1106,
    EVENT_D1121,
    EVENT_D1198,
    EVENT_D1199,
    event_binding,
)
from derelib.lote import build_lote
from derelib.returns import parse_return
from derelib.utils import format_amount
from derelib.validation import validate, validate_lote

__version__ = "0.1.0"

__all__ = [
    "EVENT_D1001",
    "EVENT_D1011",
    "EVENT_D1101",
    "EVENT_D1106",
    "EVENT_D1121",
    "EVENT_D1198",
    "EVENT_D1199",
    "__version__",
    "build_lote",
    "event_binding",
    "format_amount",
    "parse_return",
    "validate",
    "validate_lote",
]
