# miniasyncio

A minimal async event loop for Python. Built from scratch to understand how `asyncio` actually works

## Quick Start

```python
import miniasyncio as io

@io.__async__
def greet(name: str):
    print(f"Hello, {name}!")
    yield from io.sleep(0.1).__await__()
    print(f"Done with {name}")

@io.__async__
def main():
    yield from io.gather(
        greet("Alice"),
        greet("Bob"),
        greet("Charlie"),
    ).__await__()

io.run(main())
```

The equivalent code with asyncio would look like this
```python
import asyncio as io

async def greet(name: str):
    print(f"Hello, {name}!")
    await io.sleep(0.1)
    print(f"Done with {name}")

async def main():
    await io.gather(
        greet("Alice"),
        greet("Bob"),
        greet("Charlie"),
    )

io.run(main())
```

Output:
```
Hello, Alice!
Hello, Bob!
Hello, Charlie!
Done with Alice
Done with Bob
Done with Charlie
```

## How It Works

#### A `coroutine` is just a `generator` with extra steps. And `await` is just a disguised `yield`!

When you create an `async` function. Calling your function returns an coroutine object and the function body is not yet executed. The `__await__` dunder method on Awaitable objects such as coroutines returns a generator object. A generator allows for a routine to be paused and to yield control to the event loop. This allows the event loop to run another task while another is waiting.

The event loop runs tasks round-robin. When a task `await`s, it yields control back to the loop, which runs the next task. This is cooperative multitasking because tasks must `await` to yield control.

## API

| Function | Description |
|----------|-------------|
| `run(coro)` | Register a task and run the event loop to completion |
| `create_task(coro)` | Schedule a coroutine without awaiting |
| `gather(*coros)` | Await multiple coroutines concurrently, return results as list |
| `sleep(seconds)` | Non-blocking delay |
| `@__async__` | Decorator to make a generator function awaitable |
| `run_loop()` | Run the event loop manually |

## Features

- **Event loop** — cooperative multitasking with a task queue
- **Coroutines** — generator-based async functions via `@__async__` decorator
- **Tasks** — scheduled coroutines with future-like results
- **`gather`** — run multiple coroutines concurrently
- **`sleep`** — non-blocking delay
- **Zero dependencies** — pure Python and standard libraries

## Why?

To learn. This reimplements the main concepts of asyncio in a few readable lines so you can see exactly how the event loop works to make `async`/`await` feel like magic.

## Install

Using pip:
```bash
pip install miniasyncio
```

Using UV:
```bash
uv add miniasyncio
```
