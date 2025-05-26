# Previous filename: async_wrapper.py

from ..imports import asyncio, typing

# Helper asyncio class
class AIOBase:
    def __init__(self, _semaphore: int = 5) -> None:
        self.semaphore = asyncio.Semaphore(_semaphore)
        self.tasks: list[typing.Coroutine] = []


    def add_task(self, _function, *_args: typing.Any, **_kwargs: typing.Any) -> asyncio.Task:
        # Create a semaphore task
        async def semaphore_task() -> typing.Any:
            async with self.semaphore:
                return await _function(*_args, **_kwargs)

        # Add emaphore task to self.tasks
        task = asyncio.create_task(semaphore_task())
        self.tasks.append(task)

        return task

    def clear_tasks(self) -> None:
        self.tasks = []

    async def run_tasks(self) -> list[any]:
        return await asyncio.gather(*self.tasks)
