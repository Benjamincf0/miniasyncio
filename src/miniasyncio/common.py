from collections.abc import Generator
from enum import auto, Enum
from typing import Any, Callable, override
from .linkedlist import CircularDoubleLL
import inspect

class FutureState(Enum):
    PENDING = auto()
    CANCELED = auto()
    FINISHED = auto()

class Future:
    """ Resolves sometime in the future """
    def __init__(self):
        self._result: Any|None = None
        self.state: FutureState = FutureState.PENDING

    @property
    def result(self):
        return self._result

    @result.setter
    def result(self, result: Any):
        self._result = result
        self.state = FutureState.FINISHED

class Task[Y,S,R](Future):
    def __init__(self, coroutine: Coroutine[Y,S,R]):
        super().__init__()
        self.coroutine: Coroutine[Y,S,R] = coroutine

    @override
    def __str__(self):
        return f"{self.state}{self.result}{self.coroutine}"

class TaskQueue(CircularDoubleLL[Task[Any, Any, Any]]):
    def __init__(self):
        super().__init__()

    def enqueue(self, task: Task[Any, Any, Any]):
        self.add(task)

    def dequeue(self):
        it = iter(self)
        return next(it)

class Coroutine[Y, S, R]:
    """ Awaitable object """
    def __init__(self, gen_func: Callable[..., Generator[Y, S, R]], *args: Any, **kwargs: Any) -> None:
        if not inspect.isgeneratorfunction(gen_func):
            raise Exception("Expect a generator function.")

        self.generator: Generator[Y, S, R] = gen_func(*args, **kwargs)

    def __await__(self) -> Generator[Y, S, R]:
        """ Should return a generator object """
        return self.generator

class EventLoop:
    """Main orchestrator"""
    unique_instance: EventLoop|None = None

    def __init__(self):
        if self.unique_instance is not None:
            return self.unique_instance

        self.taskQueue: TaskQueue = TaskQueue()

    def run_loop(self):
        """ Runs until loop is empty """
        for task in self.taskQueue.iter_forever():

            try:
                task.coroutine.__await__().send(None)
            except StopIteration as e:
                task.state = FutureState.FINISHED
                task.result = e.value
                self.taskQueue.delete(task)

    def create_task(self, coroutine: Coroutine[Any, Any, Any]):
        """ Wraps a Coroutine in a task and adds it to the event loop. """
        task = Task(coroutine)
        self.taskQueue.add(task)
        return task

    def create_tasks(self, *coros: Coroutine[Any, Any, Any]) -> list[Task[Any, Any, Any]]:
        tasks = [self.create_task(coro) for coro in coros]
        return tasks
