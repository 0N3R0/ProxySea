import asyncio, pytest
from ProxySea.util import AIOBase

# Helper class for aiobase testing
class TestAIOBaseHelper:
    @staticmethod
    async def dummy():
        return "DUMMY!"

    @staticmethod
    async def multiply(x: int, y: int) -> int:
        await asyncio.sleep(0.1)
        return x * y


class TestAIOBase:
    def setup_method(self):
        self.aio = AIOBase(_semaphore = 2)

    @pytest.mark.asyncio
    async def test_aiobase_add_tasks(self) -> None:
        self.aio.add_task(TestAIOBaseHelper.dummy)

        assert len(self.aio.tasks) == 1

    @pytest.mark.asyncio
    async def test_aiobase_clear_tasks(self) -> None:
        self.aio.add_task(TestAIOBaseHelper.dummy)

        assert len(self.aio.tasks) == 1

        self.aio.clear_tasks()

        assert len(self.aio.tasks) == 0

    @pytest.mark.asyncio
    async def test_aiobase_run_tasks_with_correct_results(self) -> None:
        self.aio.add_task(TestAIOBaseHelper.multiply, 2, 3)
        self.aio.add_task(TestAIOBaseHelper.multiply, 5, 3)

        results = await self.aio.run_tasks()

        assert [6, 15] == results

    @pytest.mark.asyncio
    async def test_aiobase_with_failing_task(self):
        async def failing_task():
            raise RuntimeError("oops")

        self.aio.add_task(failing_task)

        with pytest.raises(RuntimeError):
            await self.aio.run_tasks()
