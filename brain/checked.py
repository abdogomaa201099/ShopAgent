"""Checked orders: refuse bad data at the door, with an error a person can read.

Week 2 (A1.5). A dataclass trusts what you give it: total="a lot" goes straight in.
A Pydantic model checks every value when the object is built, and says what is wrong.
The TODO part is yours to write.
"""
from datetime import date

from pydantic import BaseModel, ValidationError, field_validator


class CheckedOrder(BaseModel):
    """The parts of an order that must be right before the agent uses it.

    Fields (Pydantic checks the types for you):
        order_id: str · customer: str · total: float · currency: str · status: str
        ordered_on: date   ("2026-09-02" in the file becomes a real date)

    Two checks of your own:
    - order_id must be digits only, 0-9: otherwise the error says "order_id must be digits".
    - ordered_on must not be in the future: otherwise the error says "ordered_on is in the future".
    Keys of the dict that are not fields (city, items...) are simply ignored.
    """
    # TODO A1.5 (Tuesday). The steps:
    # 1. Delete the two __init__ lines below first. Then write the six fields above, with type hints.
    # 2. A @field_validator("order_id") classmethod: raise ValueError("order_id must be digits")
    #    when it is not digits 0-9; otherwise return the value.
    # 3. A @field_validator("ordered_on") classmethod: raise ValueError("ordered_on is in the future")
    #    when it is after date.today(); otherwise return the value.
    order_id: str 
    customer: str 
    total: float 
    currency: str 
    status: str
    ordered_on: date

    @field_validator("order_id")
    @classmethod
    def orderIdInRightForm(cls, value):
        if not(value.isascii() and value.isdigit()):
            raise ValueError("order_id must be digits")
        return value

    @field_validator("ordered_on")
    @classmethod
    def checkDate(cls, value):
        if date.today()<value:
            raise ValueError("ordered_on is in the future")
        return value

def check_rows(rows):
    """Check every row. Written for you: it shows how a caller uses CheckedOrder.

    Returns (good, problems): the CheckedOrder objects that passed, and one readable line
    for each row that did not, like "row 21, order_id: order_id must be digits".
    """
    good, problems = [], []
    for number, row in enumerate(rows, start=1):
        try:
            good.append(CheckedOrder(**row))
        except ValidationError as e:
            for err in e.errors():
                problems.append(f"row {number}, {err['loc'][0]}: {err['msg'].removeprefix('Value error, ')}")
    return good, problems


if __name__ == "__main__":
    # Set-up, written for you. Run it from the shop-agent folder:   .venv\Scripts\python -m brain.checked
    from brain.orders import ORDERS_FILE, load_orders
    rows = load_orders(ORDERS_FILE) + [
        {"order_id": "50x1", "customer": "Test", "total": 1.0, "currency": "OMR",
         "status": "shipped", "ordered_on": "2026-10-01"},
    ]
    good, problems = check_rows(rows)
    print(f"{len(good)} good rows")
    for line in problems:
        print(line)
