from ..imports import asyncio, typing

# Helper asyncio class
class AIOBase:
    """
    Asynchronous task runner with semaphore control using asyncio.

    This helper class allows for managing and executing multiple asynchronous tasks
    with controlled concurrency, using a semaphore to limit simultaneous executions.

    Attributes:
        semaphore (asyncio.Semaphore): Controls concurrency level of async tasks.
        tasks (list[Coroutine]): List of tasks scheduled for execution.

    Methods:
        add_task(_function, *_args, **_kwargs):
            Adds an asynchronous task to the internal task list, wrapped in a semaphore.

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

        self.semaphore = asyncio.Semaphore(_semaphore)
        self.tasks: list[typing.Coroutine] = []


    def add_task(self, _function, *_args: typing.Any, **_kwargs: typing.Any) -> asyncio.Task:
        """
        Adds an asynchronous task to be executed, wrapped in semaphore control.

        The task is created and stored internally, ready to be executed later
        via `run_tasks()`.

        Args:
            _function (Callable): Asynchronous function to execute.
            *_args (Any): Positional arguments to pass to the function.
            **_kwargs (Any): Keyword arguments to pass to the function.

        Returns:
            asyncio.Task:
                The created asyncio task.

        Examples:
        ```
            >>> import asyncio
        
            >>> async def say_hello(name):
            >>>     await asyncio.sleep(0.1)
            >>>     return f"Hello, {name}!"
            
            >>> aio = AIOBase()
            
            >>> task = aio.add_task(say_hello, "Alice")
            >>> print(task)
        ```
        """

        # Create a semaphore task
        async def semaphore_task() -> typing.Any:
            async with self.semaphore:
                return await _function(*_args, **_kwargs)

        # Add emaphore task to self.tasks
        task = asyncio.create_task(semaphore_task())
        self.tasks.append(task)

        return task

    def clear_tasks(self) -> None:
        """
        Clears the list of scheduled tasks.

        This does not cancel any running tasks.

        Returns:
            None

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

    async def run_tasks(self) -> list[typing.Any]:
        """
        Runs all added tasks concurrently with respect to the semaphore limit.

        Returns:
            list[Any]: List of results from all completed tasks.

        Examples:
        ```
            >>> import asyncio

            >>> async def add(x, y):
            >>>     await asyncio.sleep(0.1)
            >>>     return x + y

            >>> aio = AIOBase()

            >>> aio.add_task(add, 2, 3)
            >>> aio.add_task(add, 10, 5)

            >>> results = asyncio.run(aio.run_tasks())
            >>> print(results)
            >>> [5, 15] # Result of the print
        ```
        """

        return await asyncio.gather(*self.tasks)
