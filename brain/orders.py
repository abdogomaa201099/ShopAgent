"""Orders: read the shop's orders and answer questions about them.

Week 1 (A1) adds the first functions. The TODO parts are yours to write: they are the
heart of each task. Everything else in this file is set-up, already written for you.
"""
import json
from pathlib import Path

# Where the orders file is, found from this file's own place, so it works from any folder.
ORDERS_FILE = Path(__file__).resolve().parent.parent / "data" / "orders.json"


def load_orders(path):
    """Read the orders file and return a list with one dict per order.

    path: where the JSON file is, for example ORDERS_FILE.
    """
    with open(path, encoding="utf-8") as f:
        return json.load(f)
    # TODO A1.1 (Monday). The steps:
    # 1. Open the file for reading, as UTF-8 text, in a "with" block.
    # 2. Turn the JSON text into Python objects with json.load.
    # 3. Return what json.load gave you.
    # raise NotImplementedError("A1.1 (Monday): write load_orders")


def describe_order(order):
    """Return one line about an order, for a person to read.

    Example: "Order 5001: 3 items, 23.500 OMR, delivered"
    - the number of items is all the "qty" values added together: "1 item", but "3 items"
    - the total always has 3 decimals, then the currency
    """
    totQ = sum(p["qty"] for p in order["items"])
    itmStr = "item" if totQ==1 else "items" 
    return f"Order {order['order_id']}: {totQ} {itmStr}, " \
            f"{order['total']:.3f} {order['currency']}, {order['status']}" 
    # TODO A1.1 (Monday). The steps:
    # 1. Add up the "qty" of every item in order["items"].
    # 2. Choose the word: "item" when the count is 1, otherwise "items".
    # 3. Build the line with an f-string and return it (don't print it).
    raise NotImplementedError("A1.1 (Monday): write describe_order")


def find_order(orders, order_id):
    """Return the order whose "order_id" is exactly order_id, or None if there is none.

    order_id must be a string of digits, like "5003". If it is empty or has anything
    else in it ("abc"), the caller made a mistake: raise ValueError.
    """
    if not isinstance(order_id, str) and order_id.isnumeric():
        raise NotImplementedError("Error: Not a correct type of order ID!")
    for order in orders:
        if order["order_id"] == order_id:
            return order
    # TODO A1.2 (Tuesday). The steps:
    # 1. If order_id is not a string of digits, raise ValueError with a clear message.
    # 2. Go through the orders. When one has exactly this "order_id", return it.
    # 3. After the loop (nothing matched), return None.
    raise NotImplementedError("A1.2 (Tuesday): write find_order")


if __name__ == "__main__":
    # Set-up, written for you: prints every order, one line each.
    # Run it from the shop-agent folder:   .venv\Scripts\python -m brain.orders
    for order in load_orders(ORDERS_FILE):
        print(describe_order(order))
