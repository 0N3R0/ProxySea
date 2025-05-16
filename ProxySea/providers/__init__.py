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
    
    async def get_proxies(
            self,
            _active: bool = True,
            _scheme: typing.Literal["HTTPS", "HTTP", "SOCKS5", "SOCKS4", "ALL"] = "ALL",
            _anonymity_level: typing.Literal["HIGH", "MEDIUM", "LOW", "ALL"] = "ALL"
        ) -> list[ProxyInfo]:
        _scheme = _scheme.upper()
        _anonymity_level = _anonymity_level.upper()

        proxies: list[ProxyInfo] = []

        for provider in self.ProxyProviders: # Iterate for every provider
            
            # Iterate for every proxy in provider
            for proxy in provider.PROXIES:
                if _scheme not in [proxy.SCHEME, "ALL"]:
                    continue

                if _anonymity_level not in [proxy.ANONYMITY_LEVEL, "ALL"]:
                    continue

                if _active != proxy.IS_ACTIVE:
                    continue

                proxies.append(proxy)

        return proxies


    async def setup(self):
        aio: AIOBase = AIOBase(_semaphore = 5)

        # Fetch all proxies from all providers --->
        for provider in self.ProxyProviders:
            aio.add_task(provider.fetch_proxies)

        await aio.run_tasks()
        # <---


        # Clear old tasks
        aio.clear_tasks()


        # Test all proxies --->
        for provider in self.ProxyProviders:
            aio.add_task(provider.test_all_proxies, 500)

        await aio.run_tasks()
        # <---
