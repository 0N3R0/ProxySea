# Logger imports
from ..logger import Logger

# Util imports
from .aio import AIOBase
from .proxy_tester import ProxyTester, ProxyInfo
from .http_client import HttpClient

# Default imports
from ..imports import typing


# Provider manager, should do:
# Download all proxies.
# Test all downloaded proxies.
# Should in addition, contain scrapping methods from each provider site.

class ProxyProvider:
    def __init__(self, _provider_url: str, _debug: bool = False) -> None:
        self.DEBUG: bool = _debug
        
        # Some basic information
        self.URL: str = _provider_url
        self.DOMAIN: str = self.URL.split("://")[1].split("/")[0]

        # Proxies variables
        self.PROXIES: list[ProxyInfo] = []


        # Create the Logger instance, for easier logging.
        self.Logger: Logger = Logger(
            _logger_name = f"ProviderManager [{self.DOMAIN}]",
            _debug = self.DEBUG
        )

        # Create the ProxyTester instance, for easier proxy testing.
        self.ProxyTester: ProxyTester = ProxyTester(
            _connection_timeout = 1,
            _debug = self.DEBUG
        )

        # Create the HTTPClient instance, for easier page downloading.
        self.HttpClient = HttpClient(_url = self.URL)

    async def download_page(self) -> typing.Any:
        return await self.HttpClient.get()


    async def add_new_proxy(self, _new_proxy: ProxyInfo) -> None:
        is_new = _new_proxy.ID not in [proxy.ID for proxy in self.PROXIES]

        if not is_new:
            return
        
        self.PROXIES.append(_new_proxy)
    
    async def test_proxy(self, _proxy: ProxyInfo) -> ProxyInfo:
        self.Logger.log(f"Starting testing proxy: {_proxy}")

        # If proxy is blacklisted, skip that proxy.
        if _proxy.IS_BLACKLISTED:
            self.Logger.log(f"This proxy is blacklisted: {_proxy}")
            return

        # Check if provided proxy has defined valid proxy_type
        if not _proxy.TYPE or _proxy.TYPE not in ["HTTPS", "HTTP", "SOCKS5", "SOCKS4"]:
            # If the proxy doesn't have provided type of proxy, or is not in ["HTTPS", "HTTP", "SOCKS5", "SOCKS4"]

            # We are trying to detect the type of the proxy
            proxy_host, proxy_port, proxy_type = await self.ProxyTester.detect_type(
                _host = _proxy.HOST,
                _port = _proxy.PORT
            )

            # Checking if we got the proxy_type
            if proxy_type:
                # If we got the proxy_type, we are setting it and changing the active state of proxy to True
                _proxy.change_proxy_type(_type = proxy_type)
                _proxy.change_is_active(_active = True)

            else:
                # Else we are changing the state of proxy to False
                _proxy.change_is_active(_active = False)

        else:
            # If the proxy_type was provided, we are just checking the connection for provided proxy_type

            is_alive = await self.ProxyTester.check_connection(
                _scheme = _proxy.TYPE,
                _host = _proxy.HOST,
                _port = _proxy.PORT
            )

            _proxy.change_is_active(_active = is_alive)

        self.Logger.log(_proxy)

        # Call the method to update connection_retries variable
        # in _proxy class, to check if this proxy should be
        # blacklisted or not
        _proxy.update_connection_retries()

        return _proxy

    async def test_all_proxies(self, _concurrent_tasks: int = 10) -> None:
        self.Logger.log("Testing all provided proxies.")

        aio = AIOBase(_semaphore = _concurrent_tasks)

        for proxy in self.PROXIES:
            aio.add_task(self.test_proxy, proxy)
        
        results = await aio.run_tasks()
