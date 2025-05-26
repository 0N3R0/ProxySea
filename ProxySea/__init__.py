from .providers import ProvidersManager
from .api import ApiServer
from .util import ProxyInfo
from .logger import Logger

class ProxySea:
    def __init__(self, _debug: bool = False) -> None:
        self.debug: bool = _debug

        self.logger: Logger = Logger(_logger_name = "ProxySea", _debug = self.debug)
        
        self.providers_manager: ProvidersManager = ProvidersManager(_debug = self.debug)
        # self.api_server: ApiServer = ApiServer()

    # Will be done later.
    # async def run_api(self) -> None:
        # self.ApiServer.run()
        # ...

    async def fetch_proxies(self) -> list[ProxyInfo]:
        return await self.providers_manager.fetch_proxies()

    async def test_proxies(self, _proxies: list[ProxyInfo], _concurrent_tasks: int = 500) -> list[ProxyInfo]:
        """
            Tests the given proxies concurrently and returns a list of verified proxies.

            This method uses `ProvidersManager` to test a list of `ProxyInfo` objects.
            The tests are performed asynchronously with an optional limit on concurrent tasks.

            Args:
                _proxies (list[ProxyInfo]): A list of `ProxyInfo` objects to be tested.
                _concurrent_tasks (int, optional): Maximum number of concurrent testing tasks. Defaults to 500.

            Returns:
                list[ProxyInfo]: A list of tested (e.g., working or verified) `ProxyInfo` objects.
        """

        if not _proxies:
            return []
        
        tested_proxies: list[ProxyInfo] = await self.providers_manager.test_proxies(_proxies = _proxies, _concurrent_tasks = _concurrent_tasks)

        return tested_proxies
