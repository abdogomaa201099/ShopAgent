"""A1.2 (Tuesday): find_order."""
# Run only these:   .venv\Scripts\python -m pytest tests/test_find_order.py -q
import pytest

from brain.orders import find_order

# A small, made-up list for the tests. "50031" comes before "5003" on purpose.
ORDERS = [
    {"order_id": "5001", "status": "delivered"},
    {"order_id": "50031", "status": "shipped"},
    {"order_id": "5003", "status": "processing"},
]

# ---- Your two tests go here (A1.2) ---------------------------------------------
# 1. test_find_order_finds_an_order: "5001" gives back the order whose status is "delivered".
# 2. test_find_order_unknown_number_gives_none: "9999" gives back None.
# ----------------------------------------------------------------------------------


def test_find_order_matches_the_whole_number_only():
    assert find_order(ORDERS, "5003")["status"] == "processing"   # not "50031"
    assert find_order(ORDERS, "500") is None                      # the start of a number is not a match
    assert find_order(ORDERS, "50011") is None                    # "5001" is inside "50011": still not the same number


def test_find_order_rejects_text_that_is_not_a_number():
    with pytest.raises(ValueError):
        find_order(ORDERS, "")
    with pytest.raises(ValueError):
        find_order(ORDERS, "abc")
