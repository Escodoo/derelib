"""Layout helpers that do not belong to a single event."""

from __future__ import annotations

import re
from datetime import datetime, timezone
from decimal import ROUND_HALF_EVEN, Decimal

EVENT_ID_INSCRIPTION_TYPE = "1"
EVENT_ID_RE = re.compile(r"^DeRE[0-9]{4}[1-2][0-9A-Z]{14}[0-9]{19}$")
_EVENT_TYPE_RE = re.compile(r"^D-([0-9]{4})$")
_CNPJ_ROOT_RE = re.compile(r"^[0-9A-Z]{8}$")
_FRACTION_RE = re.compile(r"\.(\d+)")


def format_amount(
    value: Decimal | float | int | str | None, signed: bool = False
) -> str:
    """Format a monetary value with NBR 5891 half-even rounding (2 decimals)."""
    quantize = Decimal("0.01")
    amount = Decimal(str(value or 0)).quantize(quantize, rounding=ROUND_HALF_EVEN)
    if amount.copy_abs() < Decimal("0.005"):
        return "0.00"
    if signed:
        return f"{amount:.2f}"
    return f"{amount.copy_abs():.2f}"


def parse_datetime(value: str | None) -> datetime | None:
    """Return an aware datetime from a DeRE xs:dateTime string.

    Official returns use seven fractional digits. Values without a
    timezone are treated as UTC.
    """
    if not value:
        return None
    text = str(value).strip().replace("Z", "+00:00")
    text = _FRACTION_RE.sub(
        lambda match: "." + (match.group(1) + "000000")[:6], text, count=1
    )
    try:
        moment = datetime.fromisoformat(text)
    except ValueError:
        return None
    if moment.tzinfo is None:
        return moment.replace(tzinfo=timezone.utc)
    return moment


def make_event_id(event_type: str, nr_insc: str, moment: datetime, seq: int) -> str:
    """Build the official 42-character structured event id.

    The host keeps the sequential counter. ``nr_insc`` is the 8-character
    CNPJ root; it is padded to 14 characters as required by the XSD.
    """
    match = _EVENT_TYPE_RE.fullmatch(str(event_type))
    if not match:
        raise ValueError(f"Unknown DeRE event type {event_type}")
    root = str(nr_insc or "").upper()
    if not _CNPJ_ROOT_RE.fullmatch(root):
        raise ValueError("nr_insc must be an 8-character CNPJ root")
    sequence = int(seq)
    if sequence < 0 or sequence > 99999:
        raise ValueError("seq must be between 0 and 99999")
    inscription = root.rjust(14, "0")
    timestamp = moment.strftime("%Y%m%d%H%M%S")
    event_id = (
        f"DeRE{match.group(1)}{EVENT_ID_INSCRIPTION_TYPE}{inscription}"
        f"{timestamp}{sequence:05d}"
    )
    if not EVENT_ID_RE.fullmatch(event_id):
        raise ValueError(f"Generated event id is not valid: {event_id}")
    return event_id
