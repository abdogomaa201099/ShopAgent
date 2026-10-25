"""A1.6 (Wednesday): fake_lookup, lookup_one_by_one, lookup_together."""
# Run only these:   .venv\Scripts\python -m pytest tests/test_lookups.py -q
import asyncio
import time

from brain.lookups import fake_lookup, lookup_one_by_one, lookup_together

IDS = ["5001", "5002", "5003"]


def timed(coroutine):
    """Run one coroutine to the end. Returns (its result, the seconds it took)."""
    start = time.perf_counter()
    result = asyncio.run(coroutine)
    return result, time.perf_counter() - start


def test_fake_lookup_waits_then_answers():
    answer, seconds = timed(fake_lookup("5003", 0.2))
    assert answer == "5003: found"
    assert seconds >= 0.19


def test_one_by_one_takes_the_sum_of_the_waits():
    answers, seconds = timed(lookup_one_by_one(IDS, 0.2))
    assert answers == ["5001: found", "5002: found", "5003: found"]
    assert seconds >= 0.58              # 3 waits of 0.2 s, one after the other


def test_together_takes_about_one_wait():
    answers, seconds = timed(lookup_together(IDS, 0.2))
    assert answers == ["5001: found", "5002: found", "5003: found"]    # same order as IDS
    assert seconds < 0.4                # the 3 waits overlap: about 0.2 s, not 0.6 s
