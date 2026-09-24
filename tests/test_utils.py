from derelib.utils import format_amount


def test_format_amount_half_even():
    assert format_amount("10.125") == "10.12"
    assert format_amount("10.135") == "10.14"
    assert format_amount(0) == "0.00"
    assert format_amount("0.004") == "0.00"
    assert format_amount(-1.5) == "1.50"
    assert format_amount(-1.5, signed=True) == "-1.50"
    assert format_amount(None) == "0.00"
