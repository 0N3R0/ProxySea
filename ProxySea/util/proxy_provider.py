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
    """
    Manages proxy acquisition, testing, and logging for a specific provider URL.

    This class is responsible for handling a collection of proxy servers from a given provider,
    downloading content from the provider URL, validating and testing proxies for availability,
    and tracking their operational status.

    Note:
        - Each proxy must be an instance of `ProxyInfo`.
        - The provider URL is expected to be a full HTTP/HTTPS URL, used to fetch a proxy list or content.
        - Requires external classes: `ProxyInfo`, `Logger`, `ProxyTester`, `HttpClient`, `AIOBase`.

    Attributes:
        debug (bool): Enables debug-level logging output.
        url (str): Full provider URL from which proxy data may be fetched.
        domain (str): Extracted domain from the provider URL.
        proxies (list[ProxyInfo]): List of currently known proxy objects.
        logger (Logger): Logging helper for tracing internal actions and errors.
        proxy_tester (ProxyTester): Utility to validate and check the health of proxies.
        http_client (HttpClient): Lightweight client used to fetch remote page content.

    Methods:
        add_new_proxy(_new_proxy):
            Adds a new proxy to the internal list if not already present.

        download_page():
            Downloads the HTML content from the provider URL.
            Returns response object or None if an error occurred.

        test_proxy(_proxy):
            Tests the functionality and validity of a single proxy.
            Returns updated ProxyInfo instance or None if skipped.

        test_all_proxies(_concurrent_tasks):
            Concurrently tests all stored proxies using asynchronous tasks.
            Returns a list of tested ProxyInfo objects.
    
    Examples:
    ```
        >>> import asyncio

        >>> provider = ProxyProvider("https://example.com/proxies", _debug=True)

        >>> proxy = ProxyInfo(_scheme=None, _host="1.2.3.4", _port=8080)
        >>> provider.add_new_proxy(proxy)

        >>> results = asyncio.run(provider.test_all_proxies())

        >>> active_proxies = [p for p in results if p.is_active]
        >>> print(active_proxies)
    ```
    """
    
    def __init__(self, _provider_url: str, _debug: bool = False) -> None:
        """
        Initializes the ProxyProvider instance and sets up internal utilities.

        Args:
            _provider_url (str):
                Full URL of the proxy provider endpoint.
            _debug (bool, optional):
                Enables debug output if set to True. Defaults to False.

        Examples:
        ```
            >>> provider = ProxyProvider("https://example.com/list.txt", _debug=True)
        ```
        """

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
        """
        Adds a new proxy to the list if it does not already exist.

        Args:
            _new_proxy (ProxyInfo):
                The proxy to be added.
        
        Returns:
            None

        Examples:
        ```
            >>> proxy = ProxyInfo(_scheme="HTTP", _host="127.0.0.1", _port=8000)
            >>> provider.add_new_proxy(proxy)
        ```
        """

        is_new = _new_proxy.id not in [proxy.id for proxy in self.proxies]

        if not is_new:
            return None

        self.proxies.append(_new_proxy)


    async def download_page(self) -> typing.Optional[str | dict]:
        """
        Downloads the page from the provider URL using the internal HTTP client.

        Logs success or failure and returns the response or None on error.

        Returns:
            typing.Optional[str | dict]:
                The page content as a string or dict, or None if download fails.

        Examples:
        ```
            >>> content = await provider.download_page()
            >>> if content:
            >>>     print(content)
        ```
        """
        
        res: typing.Optional[str | dict] = None

        try:
            res = await self.http_client.get()
        except Exception as e:
            self.logger.log(f"Exception during fetching page: {e}")

        if res:
            self.logger.log(f"Fetched page successfully.")
        else:
            self.logger.log(f"Something went wrong while fetching page.")

        return res
    
    async def test_proxy(self, _proxy: ProxyInfo) -> ProxyInfo:
        """
        Tests a single proxy for connectivity and updates its state.

        This includes detecting the proxy scheme if missing, checking if it is blacklisted,
        and validating its connectivity.

        Args:
            _proxy (ProxyInfo):
                Proxy to be tested.

        Returns:
            ProxyInfo:
                Updated proxy with its active state and retry count adjusted.

        Examples:
        ```
            >>> tested_proxy = await provider.test_proxy(proxy)
            >>> print(tested_proxy.is_active)
            >>> False  # Result of the print
        ```
        """

        self.logger.log(f"Starting testing proxy: {_proxy}")

        # If proxy is blacklisted, skip that proxy.
        if _proxy.is_blacklisted:
            self.logger.log(f"This proxy is blacklisted: {_proxy}")
            return _proxy

        # Check if provided proxy has defined valid proxy_scheme
        if not _proxy.scheme or _proxy.scheme.upper() not in {"HTTPS", "HTTP", "SOCKS5", "SOCKS4"}:
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
        """
        Tests all stored proxies concurrently with a limit on parallel tasks.

        Args:
            _concurrent_tasks (int, optional):
                Number of concurrent proxy tests to run. Defaults to 10.

        Returns:
            list[ProxyInfo]:
                List of proxies with updated connection and status information.

        Examples:
        ```
            >>> results = await provider.test_all_proxies(_concurrent_tasks=5)
            >>> active = [proxy for proxy in results if proxy.is_active]
        ```
        """

        self.logger.log("Testing all provided proxies.")

        aio = AIOBase(_semaphore = _concurrent_tasks)

        for proxy in self.proxies:
            aio.add_task(self.test_proxy, proxy)
        
        results = await aio.run_tasks()

        return results
