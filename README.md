# shop-agent

A support agent for a small online shop, built step by step: **one brain, two doors**.

- **The brain** (`brain/`): one Python package that knows the shop: its orders now, its policies later.
- **The doors** (coming later): a web chat page, a voice door, and an MCP server. They all share the same brain.

Shop name: BlaBla Shop

## Set up once

```
py -3.10 -m venv .venv
.venv\Scripts\python -m pip install -r requirements-dev.txt
```

## Run the tests

```
.venv\Scripts\python -m pytest -q
```

Tests for sessions you haven't done yet fail with a message like `A1.2 (Tuesday): write find_order`. That is expected.

## Progress

| Level | What it adds | Status |
|---|---|---|
| A1 · Python | load, describe, find and clean orders | in progress |
