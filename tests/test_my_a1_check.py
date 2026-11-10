import pytest

from check.a1_find import find_order

ORDERS = [
    {"order_id": "5001", "status": "delivered"},
    {"order_id": "50031", "status": "shipped"},
    {"order_id": "5003", "status": "processing"},
]

def test_find_order_with_digit():
    assert find_order(ORDERS, "5001") is not None

def test_find_order_with_arabic_digits():
    assert find_order(ORDERS, "٥٠٠١") is not None

def test_find_order_with_arabic_digits_and_words():
    assert find_order(ORDERS, "with٥٠٠١number") is not None

def test_find_order_with_non_exist_order():
    assert find_order(ORDERS, "6431") is None