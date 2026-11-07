"""Web calls: ask another computer for data, safely.

Week 3 (A1.7). Soon the agent calls the AI model over the web (A3), and every call
needs a secret key. Three rules start today:
  - the key lives in a file called .env, never in the code (and .env is never committed);
  - every call has a timeout, so a slow server cannot freeze the agent;
  - every call is logged: what was asked, the answer's status, how long it took. Never the key.
The TODO parts are yours to write.
"""
import asyncio
import logging
import time

import httpx
from dotenv import dotenv_values

log = logging.getLogger("shop.web")


def read_api_key(env_file=".env"):
    """Return the value of SHOP_API_KEY in the env_file.

    No file, or no SHOP_API_KEY in it, or an empty value: raise RuntimeError with a
    message that says what to do ("add SHOP_API_KEY=... to .env").
    """
    # TODO A1.7 (Monday). The steps:
    # 1. Read the file into a dict with dotenv_values(env_file). (No file gives an empty dict.)
    # 2. Take the "SHOP_API_KEY" value with .get, so a missing key gives None, not a crash.
    # 3. None or empty? Raise RuntimeError with a clear message. Otherwise return the key.
    
    file_env = dotenv_values(env_file)
    shopApiKey = file_env.get("SHOP_API_KEY")
    if shopApiKey == None or len(shopApiKey) == 0:
        raise RuntimeError("add SHOP_API_KEY=... to .env")
    return shopApiKey
    # raise NotImplementedError("A1.7 (Monday): write read_api_key")


async def get_json(client, url, api_key, timeout=5.0):
    """GET url with the key in the header, and return the JSON answer as a dict.

    On a timeout or an error status (404, 500...): log an ERROR line and return None.
    On success: log an INFO line with the url, the status code and the seconds it took.
    The key goes in the header "Authorization: Bearer <key>", and never in a log line.
    """
    # TODO A1.7 (Monday). The steps:
    # 1. Note the start time (time.perf_counter()).
    # 2. In a try block: await client.get(url, headers=..., timeout=timeout),
    #    then response.raise_for_status() (it raises on 4xx and 5xx).
    # 3. except httpx.TimeoutException: log.error(...) with the url, return None.
    # 4. except httpx.HTTPStatusError as e: log.error(...) with the url and e.response.status_code, return None.
    # 5. Success: log.info(...) with the url, the status code and the seconds; return response.json().
    start_time = time.perf_counter()
    try:
        response = await client.get(url, headers={"Authorization": f"Bearer {api_key}"}, timeout=timeout)
        response.raise_for_status()
    except httpx.TimeoutException as e:
        log.error("url : %s is not reached" , url)
        return None
    except httpx.HTTPStatusError as e :
        log.error("%s returned %s " , url, e.response.status_code)
        return None
    log.info("%s %s in %.2f s", url, response.status_code, time.perf_counter() - start_time)
    return response.json()

async def get_many(client, urls, api_key):
    """Fetch every url at the same time. Return the answers in the same order as urls.

    Then log one INFO line with how many urls and the total seconds, like
    "3 urls in 1.02 s".
    """
    # TODO A1.7 (Monday). The steps:
    # 1. Note the start time.
    # 2. Make one get_json(...) job per url, and await them all with asyncio.gather.
    # 3. log.info(...) the count and the total seconds; return the answers as a list.
    start_time = time.perf_counter()
    response = await asyncio.gather(*[get_json(client, url, api_key) for url in urls])
    log.info("%d urls in %f s", len(urls), time.perf_counter()- start_time)
    return response
    raise NotImplementedError("A1.7 (Monday): write get_many")


def setup_logging():
    # Set-up, written for you: one line per log record, with the time and the level.
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)-5s %(name)s: %(message)s")


async def demo():
    # Set-up, written for you: 3 real web calls at once. httpbin.org waits as long as the url asks.
    setup_logging()
    key = read_api_key()
    urls = ["https://httpbin.org/delay/1", "https://httpbin.org/delay/2", "https://httpbin.org/status/404"]
    async with httpx.AsyncClient() as client:
        answers = await get_many(client, urls, key)
    print([a is not None for a in answers])


if __name__ == "__main__":
    # Run it from the shop-agent folder (it needs the internet and your .env):
    #   .venv\Scripts\python -m brain.web
    asyncio.run(demo())
