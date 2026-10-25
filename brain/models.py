"""Models: the shape of an order, written down once.

Week 2 (A1.4). A dict can hold anything, so a typo like order["staus"] only fails when that
line runs. A dataclass names every field once, with its type, and from_dict checks the
data as it comes in. The TODO parts are yours to write.
"""
from dataclasses import dataclass


@dataclass
class Item:
    """One line of an order. Written for you: it shows the shape your Order will have."""
    name: str
    qty: int
    price: float


@dataclass
class Order:
    order_id: str
    customer : str
    city : str
    items : list[Item]
    total : float
    currency : str
    status : str
    ordered_on : str
    delivered_on : str | None

    """One order of the shop, with every field named and typed."""
    @classmethod
    def from_dict(cls, d):
        """Build an Order from one dict of data/orders.json.

        - Each dict in d["items"] becomes an Item.
        - If a key is missing, raise ValueError, and say which key: "order is missing 'status'".
        """
        fields = ["order_id", "customer","city", "items", "total", "currency", "status", "ordered_on", "delivered_on"]
        for f in fields:
            if f not in d:
                raise ValueError(f"{f} field not found in the order data")
        itms=[]
        for i in d["items"]:
            itms.append(Item(name = i["name"], qty = i["qty"], price = i["price"]))

        return cls(
            order_id = d["order_id"], customer= d["customer"],
            city = d["city"], items = itms, total = d["total"], 
            currency = d["currency"], status=d["status"], 
            ordered_on = d["ordered_on"], delivered_on = d["delivered_on"]
        )
       