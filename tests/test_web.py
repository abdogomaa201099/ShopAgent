"""A1.7 (Monday): read_api_key, get_json, get_many.

No real internet here: httpx.MockTransport plays the web server, so the tests are fast
and always give the same answer.
"""
# Run only these:   .venv\Scripts\python -m pytest tests/test_web.py -q
import asyncio
import logging
import time

import httpx
import pytest

from brain.web import get_json, get_many, read_api_key

KEY = "test-key-123"


def fake_server(handler):
    """A client whose "web" is the handler function: it gets each request, returns a response."""
    return httpx.AsyncClient(transport=httpx.MockTransport(handler))


async def call_get_json(handler, url="https://shop.test/orders/5003", timeout=5.0):
    async with fake_server(handler) as client:
        return await get_json(client, url, KEY, timeout=timeout)


def test_read_api_key_from_the_env_file(tmp_path):
    env = tmp_path / ".env"
    env.write_text("SHOP_API_KEY=abc-999\n", encoding="utf-8")
    assert read_api_key(env) == "abc-999"


def test_read_api_key_missing_says_what_to_do(tmp_path):
    env = tmp_path / ".env"
    env.write_text("OTHER=1\n", encoding="utf-8")
    with pytest.raises(RuntimeError, match="SHOP_API_KEY"):
        read_api_key(env)
    with pytest.raises(RuntimeError, match="SHOP_API_KEY"):
        read_api_key(tmp_path / "no-such-file.env")


def test_get_json_sends_the_key_and_returns_the_json(caplog):
    seen = {}

    def handler(request):
        seen["auth"] = request.headers.get("Authorization")
        return httpx.Response(200, json={"order_id": "5003", "status": "shipped"})

    with caplog.at_level(logging.INFO, logger="shop.web"):
        answer = asyncio.run(call_get_json(handler))
    assert answer == {"order_id": "5003", "status": "shipped"}
    assert seen["auth"] == f"Bearer {KEY}"
    info = [r for r in caplog.records if r.name == "shop.web" and r.levelno == logging.INFO]
    assert info, "log one INFO line for a call that worked"
    assert "shop.test/orders/5003" in info[0].getMessage() and "200" in info[0].getMessage()


def test_get_json_timeout_logs_an_error_and_returns_none(caplog):
    def handler(request):
        raise httpx.ReadTimeout("the server is too slow", request=request)

    with caplog.at_level(logging.INFO, logger="shop.web"):
        answer = asyncio.run(call_get_json(handler))
    assert answer is None
    errors = [r for r in caplog.records if r.name == "shop.web" and r.levelno == logging.ERROR]
    assert errors, "log one ERROR line when the call times out"
    assert "shop.test/orders/5003" in errors[0].getMessage()


def test_get_json_error_status_logs_the_code_and_returns_none(caplog):
    def handler(request):
        return httpx.Response(404, json={"detail": "no such order"})

    with caplog.at_level(logging.INFO, logger="shop.web"):
        answer = asyncio.run(call_get_json(handler))
    assert answer is None
    errors = [r for r in caplog.records if r.name == "shop.web" and r.levelno == logging.ERROR]
    assert errors and "404" in errors[0].getMessage()


def test_get_json_uses_the_timeout_it_is_given():
    seen = {}

    def handler(request):
        seen["timeout"] = request.extensions.get("timeout")
        return httpx.Response(200, json={})

    asyncio.run(call_get_json(handler, timeout=2.5))
    assert seen["timeout"]["read"] == 2.5


def test_the_key_never_appears_in_the_log(caplog):
    def ok(request):
        return httpx.Response(200, json={"ok": True})

    def slow(request):
        raise httpx.ReadTimeout("too slow", request=request)

    def broken(request):
        return httpx.Response(500)

    with caplog.at_level(logging.DEBUG):
        for handler in (ok, slow, broken):
            asyncio.run(call_get_json(handler))
    assert KEY not in caplog.text


def test_get_many_runs_together_keeps_the_order_and_logs_the_total(caplog):
    async def handler(request):
        await asyncio.sleep(0.2)                     # every "page" takes 0.2 s
        return httpx.Response(200, json={"path": request.url.path})

    async def run():
        async with fake_server(handler) as client:
            return await get_many(client, ["https://shop.test/a", "https://shop.test/b", "https://shop.test/c"], KEY)

    start = time.perf_counter()
    with caplog.at_level(logging.INFO, logger="shop.web"):
        answers = asyncio.run(run())
    seconds = time.perf_counter() - start
    assert answers == [{"path": "/a"}, {"path": "/b"}, {"path": "/c"}]
    assert seconds < 0.45, "the 3 waits should overlap: about 0.2 s, not 0.6 s"
    summary = [r for r in caplog.records if r.name == "shop.web" and "3 urls" in r.getMessage()]
    assert summary, 'log one line like "3 urls in 0.21 s" after gather'
