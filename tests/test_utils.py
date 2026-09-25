from datetime import datetime, timezone

import pytest

from derelib.utils import format_amount, make_event_id, parse_datetime


def test_format_amount_half_even():
    assert format_amount("10.125") == "10.12"
    assert format_amount("10.135") == "10.14"
    assert format_amount(0) == "0.00"
    assert format_amount("0.004") == "0.00"
    assert format_amount(-1.5) == "1.50"
    assert format_amount(-1.5, signed=True) == "-1.50"
    assert format_amount(None) == "0.00"


def test_parse_datetime_seven_fraction_digits():
    moment = parse_datetime("2026-12-05T12:00:00.1234567-03:00")
    assert moment is not None
    assert moment.tzinfo is not None
    assert moment.utcoffset().total_seconds() == -3 * 3600
    assert moment.microsecond == 123456


def test_parse_datetime_naive_is_utc():
    moment = parse_datetime("2026-12-05T12:00:00")
    assert moment.tzinfo == timezone.utc


def test_parse_datetime_invalid():
    assert parse_datetime("") is None
    assert parse_datetime(None) is None
    assert parse_datetime("not-a-date") is None


def test_make_event_id():
    moment = datetime(2026, 9, 24, 16, 25, 7, tzinfo=timezone.utc)
    event_id = make_event_id("D-1199", "00000000", moment, 1)
    assert event_id == "DeRE11991000000000000002026092416250700001"
    assert len(event_id) == 42


def test_make_event_id_rejects_bad_input():
    moment = datetime(2026, 9, 24, 16, 25, 7)
    with pytest.raises(ValueError, match="Unknown DeRE event type"):
        make_event_id("X-1199", "00000000", moment, 1)
    with pytest.raises(ValueError, match="CNPJ root"):
        make_event_id("D-1199", "12", moment, 1)
    with pytest.raises(ValueError, match="seq must be"):
        make_event_id("D-1199", "00000000", moment, 100000)
