import asyncio, pytest
from ProxySea.util import AIOBase

# Helper class for aiobase testing
class TestAIOBaseHelper:
    @staticmethod
    async def dummy():
        return "Dummy!"

    @staticmethod
    async def multiply(x: int, y: int) -> int:
        await asyncio.sleep(0.1)
        return x * y

    @staticmethod
    async def failing_task_with_runtime_error():
        raise RuntimeError("Oops!")

    @staticmethod
    async def failing_task_with_value_error():
        raise ValueError("Oops!")


class TestAIOBase:
    def setup_method(self):
        self.aio = AIOBase(_semaphore = 2)

    @pytest.mark.asyncio
    async def test_add_task_adds_task_to_queue(self) -> None:
        self.aio.add_task(TestAIOBaseHelper.dummy)

        assert len(self.aio.tasks) == 1

    @pytest.mark.asyncio
    async def test_clear_tasks_removes_all_tasks(self) -> None:
        self.aio.add_task(TestAIOBaseHelper.dummy)

        assert len(self.aio.tasks) == 1

        self.aio.clear_tasks()

        assert len(self.aio.tasks) == 0

    @pytest.mark.asyncio
    async def test_run_tasks_returns_correct_results(self) -> None:
        self.aio.add_task(TestAIOBaseHelper.multiply, 2, 3)
        self.aio.add_task(TestAIOBaseHelper.multiply, 5, 3)

        results = await self.aio.run_tasks()

        assert [6, 15] == results

    @pytest.mark.asyncio
    async def test_run_tasks_raises_on_exception_by_default(self):
        self.aio.add_task(TestAIOBaseHelper.failing_task_with_runtime_error)

        with pytest.raises(RuntimeError):
            await self.aio.run_tasks()

    @pytest.mark.asyncio
    async def test_run_tasks_with_returned_exceptions(self):
        self.aio.add_task(TestAIOBaseHelper.failing_task_with_value_error)

        results = await self.aio.run_tasks(return_exceptions=True)

        assert len(results) == 1
        assert isinstance(results[0], ValueError)

    @pytest.mark.asyncio
    async def test_run_tasks_with_mixed_results(self):
        self.aio.add_task(TestAIOBaseHelper.multiply, 2, 2)
        self.aio.add_task(TestAIOBaseHelper.failing_task_with_runtime_error)

        results = await self.aio.run_tasks(return_exceptions=True)

        assert len(results) == 2
        assert results[0] == 4
        assert isinstance(results[1], RuntimeError)