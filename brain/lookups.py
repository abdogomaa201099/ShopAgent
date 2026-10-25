"""Lookups: do other work while waiting.

Week 2 (A1.6). Later, the agent waits for slow things: the AI model, a web page, the
orders database. While one answer is on its way, it can already ask for the next one.
Here a "lookup" only pretends to be slow (asyncio.sleep), so you can time it.
The TODO parts are yours to write.
"""
import asyncio
import time


async def fake_lookup(order_id, seconds):
    """Pretend to look up an order: wait `seconds` without blocking, then return "5003: found"."""
    # TODO A1.6 (Wednesday). The steps:
    # 1. Wait with asyncio.sleep (await it).
    # 2. Return the text f"{order_id}: found".
    raise NotImplementedError("A1.6 (Wednesday): write fake_lookup")


async def lookup_one_by_one(order_ids, seconds):
    """Look up each order after the one before has finished. Returns the answers, in order."""
    # TODO A1.6 (Wednesday). The steps:
    # 1. Start with an empty list.
    # 2. For each order_id: await fake_lookup(...) and add its answer to the list.
    # 3. Return the list.
    raise NotImplementedError("A1.6 (Wednesday): write lookup_one_by_one")


async def lookup_together(order_ids, seconds):
    """Start every lookup at once and wait for all of them. Returns the answers, in order."""
    # TODO A1.6 (Wednesday). The steps:
    # 1. Make one fake_lookup(...) for each order_id (don't await them one by one).
    # 2. Hand them all to asyncio.gather, and await it.
    # 3. Return what gather gives back, as a list.
    raise NotImplementedError("A1.6 (Wednesday): write lookup_together")


async def demo():
    # Set-up, written for you: times both ways for the same 3 orders.
    ids = ["5001", "5002", "5003"]
    for way in (lookup_one_by_one, lookup_together):
        start = time.perf_counter()
        answers = await way(ids, 1.0)
        print(f"{way.__name__:18} {time.perf_counter() - start:.2f} s   {answers}")


if __name__ == "__main__":
    # Run it from the shop-agent folder:   .venv\Scripts\python -m brain.lookups
    asyncio.run(demo())
