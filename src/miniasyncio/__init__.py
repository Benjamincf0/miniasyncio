from collections.abc import Awaitable, Callable, Generator
from functools import wraps
import time
from typing import Any, override

from .common import Coroutine, EventLoop, FutureState

EL = EventLoop()

def run(coro: Coroutine[Any, Any, Any]):
    EL.create_task(coro)
    EL.run_loop()

@wraps(EventLoop.run_loop)
def run_loop():
    EL.run_loop()

@wraps(EventLoop.create_task)
def create_task(coroutine):
    EL.create_task(coroutine)

class gather(Awaitable[Any]):
    def __init__(self, *coros):
        self.gathered_tasks = EL.create_tasks(*coros)

    @override
    def __await__(self):
        while not all([task.state == FutureState.FINISHED for task in self.gathered_tasks]):
            yield
        return [task.result for task in self.gathered_tasks]



def __async__[Y, S, R](gen_func: Callable[..., Generator[Y, S, R]]) -> Callable[..., Coroutine[Y, S, R]]:
    def coroutine_factory(*args: Any, **kwargs: Any) -> Coroutine[Y, S, R]:
        return Coroutine(gen_func, *args, **kwargs)
    return coroutine_factory

class sleep:
    def __init__(self, seconds: float):
        self._start: float = time.monotonic()
        self._expected_end: float = self._start + seconds

    def __await__(self) -> Generator[None, None, float]:
        while time.monotonic() < self._expected_end:
            yield
        return time.monotonic() - self._start
