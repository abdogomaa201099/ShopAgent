"""A1.5 (Tuesday): CheckedOrder, a Pydantic model with two checks of your own."""
# Run only these:   .venv\Scripts\python -m pytest tests/test_checked_order.py -q
from datetime import date

import pytest
from pydantic import ValidationError

from brain.checked import CheckedOrder, check_rows
from brain.orders import ORDERS_FILE, load_orders

GOOD = {"order_id": "5001", "customer": "Aisha Al-Harthy", "total": 23.5, "currency": "OMR",
        "status": "delivered", "ordered_on": "2026-09-02", "city": "Muscat"}


def bad(**change):
    """GOOD with one value changed."""
    return {**GOOD, **change}


def test_a_good_row_passes_and_the_date_becomes_a_date():
    order = CheckedOrder(**GOOD)
    assert order.order_id == "5001"
    assert order.ordered_on == date(2026, 9, 2)


def test_all_20_orders_in_the_file_pass():
    good, problems = check_rows(load_orders(ORDERS_FILE))
    assert len(good) == 20
    assert problems == []


def test_an_order_id_that_is_not_digits_is_refused():
    for wrong in ["50x1", "", "order 5001", "٥٠٠١"]:     # the last one: Arabic digits are not 0-9
        with pytest.raises(ValidationError, match="order_id must be digits"):
            CheckedOrder(**bad(order_id=wrong))


def test_a_date_in_the_future_is_refused():
    with pytest.raises(ValidationError, match="ordered_on is in the future"):
        CheckedOrder(**bad(ordered_on="2099-01-01"))
    CheckedOrder(**bad(ordered_on=date.today().isoformat()))     # today itself is fine


def test_three_bad_rows_give_three_readable_lines():
    rows = [GOOD, bad(order_id="50x1"), bad(ordered_on="2099-01-01"), bad(total="a lot")]
    good, problems = check_rows(rows)
    assert len(good) == 1
    assert problems[0] == "row 2, order_id: order_id must be digits"
    assert problems[1] == "row 3, ordered_on: ordered_on is in the future"
    assert problems[2].startswith("row 4, total: ")      # Pydantic wrote this one for you
