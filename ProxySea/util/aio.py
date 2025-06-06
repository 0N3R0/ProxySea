# AIOBase – Async task runner with concurrency control
# Copyright (c) 2025 0N3R0
# Licensed under the MIT License (see LICENSE file for details)

import asyncio
from typing import Coroutine, Callable, Awaitable, Any

# Helper asyncio class
class AIOBase:
    """
    Asynchronous task runner with semaphore control using asyncio.

    This helper class allows for managing and executing multiple asynchronous tasks
    with controlled concurrency, using a semaphore to limit simultaneous executions.

    Attributes:
        semaphore (asyncio.Semaphore): Controls concurrency level of async tasks.
        tasks (list[Callable[[], Awaitable[Any]]]): List of task_wrappers scheduled for execution.

    Methods:
        set_semaphore(_semaphores):
            Sets the new semaphore limit.

        add_task(_function, *_args, **_kwargs):
            Adds an asynchronous task wrapper to the internal task list, wrapped in a semaphore.

        clear_tasks():
            Clears the current list of scheduled tasks.

        run_tasks():
            Executes all scheduled tasks concurrently and returns their results.

    Examples:
    ```
        >>> import asyncio

        >>> async def sample_task(x):
        >>>     await asyncio.sleep(1)
        >>>     return x * 2

        >>> aio = AIOBase(_semaphore=2)

        >>> aio.add_task(sample_task, 3)
        >>> aio.add_task(sample_task, 5)

        >>> results = asyncio.run(aio.run_tasks())
        >>> print(results)
        >>> [6, 10] # Result of the print
    ```
    """

    def __init__(self, _semaphore: int = 5) -> None:
        """
        Initializes the AIOBase instance with a semaphore limit.

        Args:
            _semaphore (int): Maximum number of concurrent tasks allowed. Default is 5.
        
        Examples:
        ```
            >>> aio = AIOBase(_semaphore=3)
            >>> print(aio.semaphore._value)  # Accessing semaphore value (usually for debug)
            >>> 3 # Result of the print
        ```
        """

        self.semaphore: asyncio.Semaphore = asyncio.Semaphore(_semaphore)
        self.tasks: list[Callable[[], Awaitable[Any]]] = []
    

    def set_semaphore(self, _semaphore: int = 5) -> None:
        """
        Sets the new semaphore limit.

        Args:
            _semaphore (int): New semaphore limit.

        Examples:
        ```
            >>> import asyncio
        
            >>> aio = AIOBase(_semaphore = 5)
            
            >>> aio.set_semaphore(_semaphore = 10)
            >>> print(aio.semaphore._value)
            >>> 10 # Result of the print
        ```
        """

        if _semaphore < 0:
            raise ValueError("The semaphore limit must be at least 0.")

        self.semaphore = asyncio.Semaphore(_semaphore)


    def add_task(self, _function, *_args: Any, **_kwargs: Any) -> None:
        """
        Adds an asynchronous task to be executed, wrapped in semaphore control.

        The task is created and stored internally, ready to be executed later
        via `run_tasks()`.

        Args:
            _function (Callable): Asynchronous function to execute.
            *_args (Any): Positional arguments to pass to the function.
            **_kwargs (Any): Keyword arguments to pass to the function.

        Examples:
        ```
            >>> import asyncio
        
            >>> async def say_hello(name):
            >>>     await asyncio.sleep(0.1)
            >>>     return f"Hello, {name}!"
            
            >>> aio = AIOBase()
            
            >>> task = aio.add_task(say_hello, "Alice")
        ```
        """

        # Create a semaphore task
        async def wrapped_task() -> Any:
            async with self.semaphore:
                return await _function(*_args, **_kwargs)

        # Add semaphore task to self.tasks
        task = wrapped_task
        self.tasks.append(task)


    def clear_tasks(self) -> None:
        """
        Clears the list of scheduled tasks.

        This does not cancel any running tasks.

        Examples:
        ```
            >>> import asyncio

            >>> aio = AIOBase()
            >>> aio.add_task(asyncio.sleep, 1)

            >>> print(len(aio.tasks))
            >>> 1 # Result of the print

            >>> aio.clear_tasks()
            >>> print(len(aio.tasks))
            >>> 0 # Result of the print
        ```
        """

        self.tasks = []


    async def run_tasks(self, return_exceptions: bool = False) -> list[Any]:
        """
        Executes all added tasks concurrently, respecting the semaphore limit.

        Args:
            return_exceptions (bool): 
                If set to True, exceptions raised by tasks will be returned in the results list 
                instead of being propagated. Defaults to False.

        Returns:
            list[Any]: A list containing the results of the completed tasks, or exception instances 
                       if `return_exceptions` is set to True and any exceptions were raised.

        Examples:
        ```python
            >>> import asyncio

            >>> async def add(x, y):
            >>>     await asyncio.sleep(0.1)
            >>>     return x + y

            >>> aio = AIOBase()

            >>> aio.add_task(add, 2, 3)
            >>> aio.add_task(add, 10, 5)

            >>> results = asyncio.run(aio.run_tasks())
            >>> print(results)
            >>> [5, 15]  # Result of the print
        ```
        """

        coros: list[Coroutine] = [task() for task in self.tasks]
        return await asyncio.gather(*coros, return_exceptions = return_exceptions)