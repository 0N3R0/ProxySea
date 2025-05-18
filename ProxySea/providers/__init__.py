from ..util import ProxyProvider, ProxyInfo, AIOBase
from ..imports import typing
from .free_proxy_list import FreeProxyList
from .spys_one import SpysOne

class ProvidersManager:
    def __init__(self, _debug: bool = False) -> None:
        self.DEBUG = _debug

        self.ProxyProviders: list[ProxyProvider] = [
            FreeProxyList(
                _debug = self.DEBUG
            ),
            SpysOne(
                _debug = self.DEBUG
            )
        ]

        self.ALL_PROXIES: list[ProxyInfo] = []


    async def get_proxies(
            self,
            _active: bool = True,
            _scheme: typing.Literal["HTTPS", "HTTP", "SOCKS5", "SOCKS4", "ALL"] = "ALL",
            _anonymity_level: typing.Literal["HIGH", "MEDIUM", "LOW", "ALL"] = "ALL"
        ) -> list[ProxyInfo]:
        _scheme = _scheme.upper()
        _anonymity_level = _anonymity_level.upper()

        proxies: list[ProxyInfo] = []

        for proxy in self.ALL_PROXIES:
            if _scheme not in [proxy.SCHEME, "ALL"]:
                continue

            if _anonymity_level not in [proxy.ANONYMITY_LEVEL, "ALL"]:
                continue

            if _active != proxy.IS_ACTIVE:
                continue

            proxies.append(proxy)

        return proxies



    async def test_fetched_proxies(self) -> list[ProxyInfo]:
        """
            Use this method, to test all fetched proxies.
            ProvidersManager.test_proxies() returns None.
        """
        aio: AIOBase = AIOBase(_semaphore = 5)

        # Test all proxies from each provider
        # --->
        for provider in self.ProxyProviders:
            aio.add_task(provider.test_all_proxies, 300)

        tested_proxies = await aio.run_tasks()
        # <---

        # Set all tested proxies too self.ALL_PROXIES
        # --->
        proxies: list[ProxyInfo] = []
        for tested_proxy_list in tested_proxies:
            proxies.extend(tested_proxy_list)
        
        self.ALL_PROXIES = proxies
        # <---

        return self.ALL_PROXIES


    async def fetch_proxies(self) -> list[ProxyInfo]:
        aio: AIOBase = AIOBase(_semaphore = 5)

        # Fetch all proxies from each provider
        # --->
        for provider in self.ProxyProviders:
            aio.add_task(provider.fetch_proxies)

        provider_proxies = await aio.run_tasks()
        # <---

        # Set all fetched proxies to self.ALL_PROXIES
        # --->
        proxies: list[ProxyInfo] = []
        for provider_proxy_list in provider_proxies:
            proxies.extend(provider_proxy_list)

        self.ALL_PROXIES = proxies
        # <---

        return self.ALL_PROXIES
