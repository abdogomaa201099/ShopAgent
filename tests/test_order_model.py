"""A1.4 (Monday): the Order dataclass and Order.from_dict."""
# Run only these:   .venv\Scripts\python -m pytest tests/test_order_model.py -q
import dataclasses
from typing import List, Optional

import pytest

from brain.models import Item, Order
from brain.orders import ORDERS_FILE, load_orders


def test_from_dict_builds_an_order_with_the_right_types():
    order = Order.from_dict(load_orders(ORDERS_FILE)[0])
    assert order.order_id == "5001"
    assert order.customer == "Aisha Al-Harthy"
    assert order.total == 23.5
    assert order.delivered_on == "2026-09-05"
    # items is a list of Item objects now, not a list of dicts
    assert order.items[1] == Item(name="Phone case", qty=2, price=2.5)
    assert order.items[1].qty == 2


def test_an_order_not_delivered_yet_has_none():
    order = Order.from_dict(load_orders(ORDERS_FILE)[1])    # 5002 is still "shipped"
    assert order.delivered_on is None


def test_every_order_in_the_file_converts():
    orders = [Order.from_dict(d) for d in load_orders(ORDERS_FILE)]
    assert len(orders) == 20
    assert all(isinstance(item, Item) for o in orders for item in o.items)


def test_order_has_every_field_with_a_type_hint():
    names = [f.name for f in dataclasses.fields(Order)]
    types = {f.name: f.type for f in dataclasses.fields(Order)}
    assert names == ["order_id", "customer", "city", "items", "total",
                     "currency", "status", "ordered_on", "delivered_on"], \
        "A1.4 (Monday): write the Order fields, in the order the comment gives"
    assert types["total"] is float
    assert types["items"] in (list[Item], List[Item])
    assert types["delivered_on"] in (str | None, Optional[str])


def test_a_missing_key_gives_a_clear_error():
    d = dict(load_orders(ORDERS_FILE)[0])
    del d["status"]
    with pytest.raises(ValueError, match="status"):
        Order.from_dict(d)
