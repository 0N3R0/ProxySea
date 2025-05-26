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
        self.debug: bool = _debug
        
        # Some basic information
        self.url: str = _provider_url
        self.domain: str = _provider_url.split("://")[1].split("/")[0]

        # Proxies variables
        self.proxies: list[ProxyInfo] = []

        # Create the Logger instance, for easier logging.
        self.logger: Logger = Logger(
            _logger_name = f"ProxyProvider [{self.domain}]",
            _debug = self.debug
        )

        # Create the ProxyTester instance, for easier proxy testing.
        self.proxy_tester: ProxyTester = ProxyTester(
            _connection_timeout = 2,
            _debug = self.debug
        )

        # Create the HttpClient instance, for easier page downloading.
        self.http_client = HttpClient(_url = self.url)

    def add_new_proxy(self, _new_proxy: ProxyInfo) -> None:
        is_new = _new_proxy.id not in [proxy.id for proxy in self.proxies]

        if not is_new:
            return

        self.proxies.append(_new_proxy)


    async def download_page(self) -> typing.Any:
        res = None

        try:
            res = await self.http_client.get()
        except Exception as e:
            self.logger.log(f"Exception during fetching page: {e}")

        if res:
            self.logger.log(f"Fetched page successfully.")
        else:
            self.logger.log(f"Something went wrong while fetching page.")

        return res
    
    async def test_proxy(self, _proxy: ProxyInfo) -> typing.Optional[ProxyInfo]:
        self.logger.log(f"Starting testing proxy: {_proxy}")

        # If proxy is blacklisted, skip that proxy.
        if _proxy.is_blacklisted:
            self.logger.log(f"This proxy is blacklisted: {_proxy}")
            return

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
                # Otherwise, we are changing the state of proxy to False
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

    async def test_all_proxies(self, _concurrent_tasks: int = 10) -> list[ProxyInfo]:
        self.logger.log("Testing all provided proxies.")

        aio = AIOBase(_semaphore = _concurrent_tasks)

        for proxy in self.proxies:
            aio.add_task(self.test_proxy, proxy)
        
        results = await aio.run_tasks()

        return results
