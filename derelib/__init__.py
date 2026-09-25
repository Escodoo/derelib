"""derelib: xsdata binding for the Brazilian DeRE layout."""

from derelib.events import (
    EVENT_D1001,
    EVENT_D1011,
    EVENT_D1101,
    EVENT_D1106,
    EVENT_D1121,
    EVENT_D1198,
    EVENT_D1199,
    RETURN_D9001,
    RETURN_D9101,
    RETURN_D9106,
    RETURN_D9112,
    RETURN_D9121,
    RETURN_D9198,
    RETURN_D9199,
    RETURN_D9209,
    RETURN_LOTE,
    event_binding,
    return_binding,
)
from derelib.lote import build_lote
from derelib.returns import parse_return
from derelib.utils import format_amount, make_event_id, parse_datetime
from derelib.validation import validate, validate_lote, validate_return

__version__ = "0.1.0"

__all__ = [
    "EVENT_D1001",
    "EVENT_D1011",
    "EVENT_D1101",
    "EVENT_D1106",
    "EVENT_D1121",
    "EVENT_D1198",
    "EVENT_D1199",
    "RETURN_D9001",
    "RETURN_D9101",
    "RETURN_D9106",
    "RETURN_D9112",
    "RETURN_D9121",
    "RETURN_D9198",
    "RETURN_D9199",
    "RETURN_D9209",
    "RETURN_LOTE",
    "__version__",
    "build_lote",
    "event_binding",
    "format_amount",
    "make_event_id",
    "parse_datetime",
    "parse_return",
    "return_binding",
    "validate",
    "validate_lote",
    "validate_return",
]
