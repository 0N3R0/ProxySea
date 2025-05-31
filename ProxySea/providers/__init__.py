from ..util import ProxyProvider, ProxyInfo, AIOBase, ProxyTester
from ..imports import typing
from ..logger import Logger
from .free_proxy_list import FreeProxyList
from .spys_one import SpysOne

class ProvidersProxyTester:
    def __init__(self, _debug: bool = False) -> None:
        self.debug = _debug

        self.logger: Logger = Logger(
            _logger_name = "ProvidersProxyTester",
            _debug = self.debug
        )

        self.proxy_tester: ProxyTester = ProxyTester(
            _connection_timeout = 5,
            _debug = self.debug
        )
    
    async def test_proxy(self, _proxy: ProxyInfo) -> ProxyInfo:
        self.logger.log(f"Starting testing proxy: {_proxy}")

        # If proxy is blacklisted, skip that proxy.
        if _proxy.is_blacklisted:
            self.logger.log(f"This proxy is blacklisted: {_proxy}")
            return _proxy

        # Check if provided proxy has defined valid proxy_scheme
        if not _proxy.scheme or _proxy.scheme not in ["HTTPS", "HTTP", "SOCKS5", "SOCKS4"]:
            # If the proxy doesn't have provided scheme of proxy, or is not in ["HTTPS", "HTTP", "SOCKS5", "SOCKS4"]

            # We are trying to detect the scheme of the proxy
            proxy_host, proxy_port, proxy_scheme = await self.proxy_tester.detect_scheme(
                _host = _proxy.host,
                _port = _proxy.port
            )

            # Checking if we got the proxy_scheme
            if proxy_scheme:
                # If we got the proxy_scheme, we are setting it and changing the active state of proxy to True
                _proxy.set_proxy_scheme(_scheme = proxy_scheme)
                _proxy.set_is_active(_active = True)

            else:
                # Else we are changing the state of proxy to False
                _proxy.set_is_active(_active = False)

        else:
            # If the proxy_scheme was provided, we are just checking the connection for provided proxy_scheme

            is_alive = await self.proxy_tester.check_connection(
                _scheme = _proxy.scheme,
                _host = _proxy.host,
                _port = _proxy.port
            )

            _proxy.set_is_active(_active = is_alive)

        self.logger.log(_proxy)

        # Call the method to update connection_retries variable
        # in _proxy class, to check if this proxy should be
        # blacklisted or not
        _proxy.update_connection_retries()

        return _proxy

    async def test_proxies(self, _proxies: list[ProxyInfo], _concurrent_tasks: int = 500) -> list[ProxyInfo]:
        if not _proxies:
            return []
        
        if not _concurrent_tasks or _concurrent_tasks < 0:
            raise ValueError("You have to provide _concurrent_tasks > 0.")

        aio: AIOBase = AIOBase(_semaphore = _concurrent_tasks)

        for proxy in _proxies:
            aio.add_task(self.test_proxy, proxy)
        
        # Run tasks returns lists of proxies
        tested_proxies: list[ProxyInfo] = await aio.run_tasks()

        return tested_proxies


class ProvidersManager:
    def __init__(self, _debug: bool = False) -> None:
        self.debug: bool = _debug

        self.PROVIDERS: list[ProxyProvider] = [
            FreeProxyList(
                _debug = self.debug
            ),
            SpysOne(
                _debug = self.debug
            )
        ]

        self.logger: Logger = Logger(
            _logger_name = "ProvidersManager",
            _debug = self.debug
        )

    
    async def fetch_proxies(self, _concurrent_tasks: int = 10) -> list[ProxyInfo]:
        aio: AIOBase = AIOBase(_semaphore = _concurrent_tasks)

        # Fetch all proxies from each provider
        # --->
        for provider in self.PROVIDERS:
            aio.add_task(provider.fetch_proxies)

        provider_proxies = await aio.run_tasks()
        # <---

        # Append all fetched proxies to the proxies list and skip duplicates, and return it.
        # --->
        proxies: list[ProxyInfo] = []
        proxy_ids: list[str] = []

        for prov_proxies in provider_proxies:
            for proxy in prov_proxies:
                if proxy.id in proxy_ids:
                    continue

                proxies.append(proxy)
                proxy_ids.append(proxy.id)
        # <---

        return proxies

    def get_proxies(
            self,
            _proxies: list[ProxyInfo],
            _active: bool = True,
            _scheme: typing.Literal["HTTPS", "HTTP", "SOCKS5", "SOCKS4", "ALL"] = "ALL",
            _anonymity_level: typing.Literal["HIGH", "MEDIUM", "LOW", "ALL"] = "ALL"
        ) -> list[ProxyInfo]:
        _scheme = _scheme.upper()
        _anonymity_level = _anonymity_level.upper()

        if not _proxies:
            return _proxies

        proxies: list[ProxyInfo] = []

        for proxy in _proxies:
            if proxy.is_active != _active:
                continue

            if _scheme not in [proxy.scheme, "ALL"]:
                continue

            if _anonymity_level not in [proxy.anonymity_level, "ALL"]:
                continue

            proxies.append(proxy)

        return proxies
