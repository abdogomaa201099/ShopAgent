"""A1.1 (Monday): load_orders and describe_order."""
# Run only these:   .venv\Scripts\python -m pytest tests/test_load_orders.py -q
from brain.orders import ORDERS_FILE, describe_order, load_orders


def test_load_orders_reads_all_20_orders():
    orders = load_orders(ORDERS_FILE)
    assert len(orders) == 20
    assert orders[0]["order_id"] == "5001"
    # This name has Arabic letters. It only comes out right if the file is read as UTF-8.
    assert orders[6]["items"][0]["name"] == "Khalas dates (تمر خلاص)"


def test_describe_order_counts_items_and_formats_the_total():
    order_5001 = {"order_id": "5001", "currency": "OMR", "status": "delivered", "total": 23.5,
                  "items": [{"name": "Wireless earbuds", "qty": 1, "price": 18.5},
                            {"name": "Phone case", "qty": 2, "price": 2.5}]}
    order_5002 = {"order_id": "5002", "currency": "OMR", "status": "shipped", "total": 7.9,
                  "items": [{"name": "USB-C charger 30W", "qty": 1, "price": 7.9}]}
    assert describe_order(order_5001) == "Order 5001: 3 items, 23.500 OMR, delivered"
    assert describe_order(order_5002) == "Order 5002: 1 item, 7.900 OMR, shipped"
