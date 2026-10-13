"""A1.3 (Wednesday): normalize_order_id."""
# Run only these:   .venv\Scripts\python -m pytest tests/test_normalize_order_id.py -q
from brain.clean import normalize_order_id


def test_arabic_digits_become_0_to_9():
    assert normalize_order_id("٥٠٠٣") == "5003"


def test_spaces_around_the_number_are_dropped():
    assert normalize_order_id("  5003  ") == "5003"


def test_hash_sign_is_dropped():
    assert normalize_order_id("#5003") == "5003"


def test_english_words_around_the_number():
    assert normalize_order_id("my order is 5003, sent 2 days ago") == "5003"   # only the first number counts


def test_arabic_words_around_the_number():
    assert normalize_order_id("رقم ٥٠٠٣") == "5003"


def test_no_number_gives_none():
    assert normalize_order_id("where is my order?") is None
    assert normalize_order_id("") is None
