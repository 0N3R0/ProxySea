# ProxySea – Async-first, ultra-fast Python library for scraping,
# detecting, and testing public HTTP/HTTPS/SOCKS4/SOCKS5 proxies
# with modular OOP design and built-in logging.
# Copyright (c) 2025 0N3R0
# Licensed under the MIT License (see LICENSE file for details)


from .imports import time

from .providers import ProvidersManager, ProvidersProxyTester
from .util import ProxyInfo
from .logger import Logger

class ProxySea:
    def __init__(self, _debug: bool = False) -> None:
        self.debug: bool = _debug

        self.logger: Logger = Logger(_logger_name = "ProxySea", _debug = self.debug)

        self.providers_manager: ProvidersManager = ProvidersManager(_debug = self.debug)
        self.providers_proxy_tester: ProvidersProxyTester = ProvidersProxyTester(_debug = self.debug)
        
        # TODO: Create api server for proxies
        # self.api_server: ApiServer = ApiServer()

    # TODO: Create api server for proxies
    # async def run_api(self) -> None:
        # self.ApiServer.run()
        # ...


    async def fetch_proxies(self, _concurrent_tasks: int = 10) -> list[ProxyInfo]:
        """
            Fetches public proxies from online providers.

            This method uses `ProvidersManager` to fetch public proxies.
            Fetching is performed asynchronously with an optional limit on concurrent tasks.

            Args:
                _concurrent_tasks (int, optional): Maximum number of concurrent fetching tasks. Defaults to 10.
            

            Returns:
                list[ProxyInfo]: A list of fetched proxies converted into `ProxyInfo` object.
        """

        self.logger.log(f"Starting fetching proxies from {len(self.providers_manager.PROVIDERS)} public providers.")

        proxies: list[ProxyInfo] = await self.providers_manager.fetch_proxies(_concurrent_tasks = _concurrent_tasks)

        self.logger.log(f"Fetched {len(proxies)} proxies.")

        return proxies


    async def test_proxies(self, _proxies: list[ProxyInfo], _concurrent_tasks: int = 500) -> list[ProxyInfo]:
        """
            Tests the given proxies concurrently and returns a list of verified proxies.

            This method uses `ProvidersProxyTester` to test a list of `ProxyInfo` objects.
            The tests are performed asynchronously with an optional limit on concurrent tasks.

            Args:
                _proxies (list[ProxyInfo]): A list of `ProxyInfo` objects to be tested.
                _concurrent_tasks (int, optional): Maximum number of concurrent testing tasks. Defaults to 500.

            Returns:
                list[ProxyInfo]: A list of tested (e.g., working or verified) `ProxyInfo` objects.
            
            Raises:
                ValueError: You have to pass a list of ProxyInfo instances in _proxies parameter.
        """

        start = time.perf_counter()
        self.logger.log(f"Starting testing proxies.")

        if not _proxies:
            return []

        if not all(isinstance(proxy, ProxyInfo) for proxy in _proxies):
            raise ValueError("All items in _proxies must be instances of ProxyInfo.")

        self.logger.log(f"Testing {len(_proxies)} proxies.")

        tested_proxies: list[ProxyInfo] = await self.providers_proxy_tester.test_proxies(_proxies = _proxies, _concurrent_tasks = _concurrent_tasks)
        working: int = sum(proxy.is_active for proxy in tested_proxies)

        self.logger.log(f"Tested {len(tested_proxies)} proxies, {working} of them are flagged as working. Tested all proxies in {float(time.perf_counter() - start):.2f} seconds.")

        return tested_proxies
