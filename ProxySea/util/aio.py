# Previous filename: async_wrapper.py

from ..imports import asyncio, typing

# Helper asyncio class
class AIOBase:
    def __init__(self, _semaphore: int = 5) -> None:
        self.SEMAPHORE = asyncio.Semaphore(_semaphore)
        self.TASKS: list[typing.Coroutine] = []


    def add_task(self, _function, *_args: typing.Any, **_kwargs: typing.Any) -> asyncio.Task:
        # Createa semaphore task
        async def semaphore_task() -> typing.Any:
            async with self.SEMAPHORE:
                return await _function(*_args, **_kwargs)

        # Add emaphore task to self.TASKS
        task = asyncio.create_task(semaphore_task())
        self.TASKS.append(task)

        return task

    def clear_tasks(self) -> None:
        self.TASKS = []

    async def run_tasks(self) -> list[any]:
        return await asyncio.gather(*self.TASKS)
