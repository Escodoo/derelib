"""Layout helpers that do not belong to a single event."""

from decimal import ROUND_HALF_EVEN, Decimal


def format_amount(value, signed=False):
    """Format a monetary value with NBR 5891 half-even rounding (2 decimals)."""
    quantize = Decimal("0.01")
    amount = Decimal(str(value or 0)).quantize(quantize, rounding=ROUND_HALF_EVEN)
    if amount.copy_abs() < Decimal("0.005"):
        return "0.00"
    if signed:
        return f"{amount:.2f}"
    return f"{amount.copy_abs():.2f}"
