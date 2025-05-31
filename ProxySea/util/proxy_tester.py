from ..imports import typing, asyncio, time, ssl

from ..logger import Logger
from .aio import AIOBase


class ProxyInfo:
    """
    Represents a single proxy's connection details, status, and metadata.

    This class encapsulates information about a proxy server, including its scheme,
    host, port, anonymity level, connection state, and retry handling.

    Note:
        - The `_scheme` parameter must be explicitly provided during initialization,
          but it may be set to `None` to indicate that the protocol is unknown or unspecified.
        - The `_anonymity_level` parameter is optional and will default to `None` if not provided.

    Attributes:
        scheme (str | None):
            Protocol used by the proxy (e.g., 'HTTP', 'HTTPS', 'SOCKS4', 'SOCKS5'), or None.
        host (str):
            Proxy server's IP address or hostname.
        port (int):
            Port number of the proxy.
        anonymity_level (str | None):
            Proxy anonymity classification ('HIGH', 'MEDIUM', 'LOW'), or None.
        is_active (bool):
            Whether the proxy is currently marked as active.
        connection_retries (int):
            Number of failed connection attempts.
        blacklist_after (int):
            Retry threshold after which the proxy is considered blacklisted.

    Properties:
        id (str):
            Unique proxy identifier, formatted as "HOST|PORT".
        url (str):
            Full proxy address, formatted as "SCHEME://HOST:PORT".
        is_blacklisted (bool):
            True if retry threshold exceeded.

    Methods:
        set_proxy_scheme(_scheme):
            Updates the scheme. Raises error if invalid or missing.

        set_is_active(_active):
            Sets the active status. Requires a boolean.

        update_connection_retries():
            Increments retry count if inactive, resets if active.
            No changes occur if proxy is blacklisted.

    Examples:
    ```
        >>> proxy = ProxyInfo("HTTP", "192.168.1.100", 8080, "HIGH")

        >>> print(proxy.id)
        >>> 192.168.1.100|8080 # Result of the print

        >>> print(proxy.url)
        >>> HTTP://192.168.1.100:8080 # Result of the print

        >>> proxy.set_is_active(True)
        >>> proxy.update_connection_retries()
        >>> print(proxy.connection_retries)
        >>> 0 # Result of the print

        >>> proxy.set_is_active(False)
        >>> proxy.update_connection_retries()
        >>> print(proxy.connection_retries)
        >>> 1 # Result of the print
    ```
    """

    def __init__(
            self,
            _scheme: typing.Literal["HTTPS", "HTTP", "SOCKS5", "SOCKS4"] | None,
            _host: str,
            _port: int,
            _anonymity_level: typing.Literal["HIGH", "MEDIUM", "LOW"] | None = None
        ) -> None:
        """
        Initializes a ProxyInfo instance with protocol, host, port, and anonymity level.

        The `scheme` and `anonymity_level` are optional and can be set to `None`
        if the information is not available or not applicable.

        Args:
            _scheme (Literal["HTTPS", "HTTP", "SOCKS5", "SOCKS4"] | None):
                The proxy protocol scheme. Can be None if unknown.
            _host (str):
                Hostname or IP address of the proxy.
            _port (int):
                Port number of the proxy.
            _anonymity_level (Literal["HIGH", "MEDIUM", "LOW"] | None):
                Level of anonymity provided by the proxy. Can be None if unknown.

        Examples:
        ```
            >>> proxy = ProxyInfo("HTTP", "192.168.1.1", 8080, "MEDIUM")
        ```
        """

        self.scheme: typing.Optional[str] = _scheme.upper() if _scheme else _scheme
        self.host: str = _host
        self.port: int = int(_port)
        self.anonymity_level: typing.Optional[str] = _anonymity_level.upper() if _anonymity_level else _anonymity_level

        self.is_active: bool = False
        self.connection_retries: int = 0
        self.blacklist_after: int = 3


    @property
    def id(self) -> str:
        """
        Returns the unique identifier of the proxy.

        Formatted as "HOST|PORT" (e.g., "192.168.0.1|8080").

        Returns:
            str:
                Unique proxy ID.

        Examples:
        ```
            >>> proxy = ProxyInfo("HTTP", "192.168.0.1", 8080)
            >>> print(proxy.id)
            >>> 192.168.0.1|8080 # Result of the print
        ```
        """

        return f"{self.host}|{self.port}"

    @property
    def url(self) -> str:
        """
        Returns the full proxy URL string.

        Formatted as "SCHEME://HOST:PORT" (e.g., "HTTP://192.168.0.1:8080").

        Returns:
            str:
                Full proxy URL.

        Examples:
        ```
            >>> proxy = ProxyInfo("HTTP", "192.168.0.1", 8080)
            >>> print(proxy.url)
            >>> HTTP://192.168.0.1:8080 # Result of the print
        ```
        """

        return f"{self.scheme}://{self.host}:{self.port}"

    @property
    def is_blacklisted(self) -> bool:
        """
        Indicates if the proxy is blacklisted based on connection retries.

        Returns:
            bool:
                True if `connection_retries` exceeds `blacklist_after`, else False.

        Examples:
        ```
            >>> proxy = ProxyInfo("HTTP", "192.168.0.1", 8080)
            >>> proxy.connection_retries = 4
            >>> print(proxy.is_blacklisted)
            >>> True # Result of the print
        ```
        """

        return self.connection_retries >= self.blacklist_after


    def set_proxy_scheme(self, _scheme: typing.Literal["HTTPS", "HTTP", "SOCKS5", "SOCKS4"]) -> None:
        """
        Sets the proxy scheme (protocol) for this proxy instance.

        Args:
            _scheme (Literal["HTTPS", "HTTP", "SOCKS5", "SOCKS4"]):
                New protocol to assign to the proxy.

        Raises:
            ValueError: If `_scheme` is not provided or is not one of the allowed values.

        Examples:
        ```
            >>> proxy = ProxyInfo(None, "192.168.0.1", 8080)
            >>> proxy.set_proxy_scheme("SOCKS5")
        ```
        """
        
        if not _scheme:
            raise ValueError(f"[ProxyInfo (set_proxy_scheme)] You have to provide _scheme. {self.id=} || {_scheme=}")
        
        if _scheme not in ["HTTPS", "HTTP", "SOCKS5", "SOCKS4"]:
            raise ValueError(f"[ProxyInfo (set_proxy_scheme)] Your provided _scheme should be one of them ['HTTPS', 'HTTP', 'SOCKS5', 'SOCKS4']. {self.id=} || {_scheme=}")

        self.scheme = _scheme.upper()


    def set_is_active(self, _active: bool) -> None:
        """
        Sets the active state of the proxy.

        Args:
            _active (bool): 
                Flag indicating whether the proxy is active (True) or inactive (False).

        Raises:
            ValueError: If `_active` is not a boolean.

        Examples:
        ```
            >>> proxy = ProxyInfo("HTTPS", "192.168.0.2", 3128)
            >>> proxy.set_is_active(True)
        ```
        """

        if not isinstance(_active, bool):
            raise ValueError(f"[ProxyInfo (set_is_active)] You have to provide bool value as flag. {self.id=} || {_active=}")

        self.is_active = _active


    def update_connection_retries(self) -> None:
        """
        Updates the retry counter based on the proxy's current activity state.

        Logic:
            - If the proxy is blacklisted (`is_blacklisted` is True), the method does nothing.
            - If the proxy is inactive (`is_active` is False), the retry counter is incremented.
            - If the proxy is active, the retry counter is reset to 0.

        This method is used to automatically track the reliability of a proxy during
        connection attempts.

        Examples:
        ```
            >>> proxy = ProxyInfo("HTTP", "10.0.0.5", 8080)

            >>> proxy.set_is_active(False)
            >>> proxy.update_connection_retries()
            >>> proxy.connection_retries
            >>> 1 # Result of the print
        ```
        """

        
        if self.is_blacklisted:
            return None

        if not self.is_active:
            self.connection_retries += 1
            return None

        self.connection_retries = 0


    def __str__(self) -> str:
        return f"[{self.scheme}] {self.host}:{self.port} (Anon: {self.anonymity_level}, Active: {self.is_active}, Blacklisted: {self.is_blacklisted}, Retries: {self.connection_retries})"


class ProxySchemeDetector:
    """
    Detects the scheme (protocol type) of a proxy server by attempting different connection types.

    This class attempts to determine whether a proxy supports one of the common proxy protocols:
    HTTPS, HTTP, SOCKS5, or SOCKS4. It does so by asynchronously probing the proxy endpoint using
    protocol-specific handshake methods.

    Attributes:
        debug (bool): If True, enables debug-level logging for proxy detection steps.
        connection_timeout (int): Timeout (in seconds) for individual connection attempts.
        PROXY_SCHEMES (list[str]): List of proxy schemes to test against.
        logger (Logger): Logger instance used for debug and status output.

    Methods:
        is_socks4 (_host, _port, _delay):
            Check if the proxy supports SOCKS4 protocol.

        is_socks5(_host, _port, _delay):
            Check if the proxy supports SOCKS5 protocol.

        is_http(_host, _port, _delay):
            Check if the proxy supports HTTP protocol.

        is_https(_host, _port, _delay):
            Check if the proxy supports HTTPS protocol.

        detect_proxy_scheme_parallel(_host, _port):
            Attempt all scheme detections in parallel and return the first valid one.
    
    Examples:
    ```
        >>> detector = ProxySchemeDetector(_connection_timeout=3, _debug=True)

        >>> scheme = await detector.detect_proxy_scheme_parallel("192.168.1.1", 8080)
        >>> print(scheme)
        >>> HTTP # Result of the print
    ```
    """


    def __init__(
            self,
            _connection_timeout: int = 3,
            _debug: bool = False
        ) -> None:
        """
        Initializes the ProxySchemeDetector instance with connection and logging settings.

        Sets up internal timeout configuration, initializes a logger for debug output,
        and defines a list of supported proxy schemes to be tested.

        Args:
            _connection_timeout (int):
                Timeout value (in seconds) for each individual connection attempt.
            _debug (bool):
                If True, enables debug logging output for internal events and detection status.

        Returns:
            None

        Examples:
        ```
            >>> detector = ProxySchemeDetector(_connection_timeout=5, _debug=True)
            >>> print(detector.PROXY_SCHEMES)
            >>> ['HTTPS', 'HTTP', 'SOCKS5', 'SOCKS4']  # Result of the print
        ```
        """
        self.debug: bool = _debug

        # Connection information
        self.connection_timeout: int = _connection_timeout

        # Basic informations
        self.PROXY_SCHEMES: list[str] = ["HTTPS", "HTTP", "SOCKS5", "SOCKS4"]


        # Create the logger instance
        self.logger: Logger = Logger(
            _logger_name = "ProxyScheme",
            _debug = self.debug
        )


    async def is_socks4(self, _host: str, _port: int, _delay_before_request: float = 0.0) -> bool:
        """
        Checks if the proxy server supports the SOCKS4 protocol.

        It sends a minimal SOCKS4 connection request and checks if the response
        matches the expected success byte (0x5A), indicating a valid SOCKS4 server.

        Args:
            _host (str):
                The hostname or IP address of the proxy.
            _port (int):
                The port number on which the proxy is running.
            _delay_before_request (float):
                Optional delay (in seconds) before attempting the connection.

        Returns:
            bool:
                - True if the proxy responds with a valid SOCKS4 response.
                - False if something went wrong.

        Examples:
        ```
            >>> is_socks4 = await detector.is_socks4("127.0.0.1", 9050)
            >>> print(is_socks4)
            >>> True  # Result of the print
        ```
        """
        
        is_alive: bool = False

        self.logger.log(f"Delaying SOCKS4 request ({_host}:{_port}) for {_delay_before_request} seconds.")
        await asyncio.sleep(delay = _delay_before_request)

        try:
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(_host, _port),
                timeout = self.connection_timeout
            )

            port_bytes = (80).to_bytes(2, 'big')
            ip_bytes = b"\x00\x00\x00\x01"

            user = b""
            domain = b"example.com\x00"
            request = b"\x04\x01" + port_bytes + ip_bytes + user + domain

            writer.write(request)
            resp = await asyncio.wait_for(
                reader.read(8),
                timeout = self.connection_timeout
            )

            writer.close()
            await writer.wait_closed()

            # is_alive = bool(resp and resp[0] == 0x00)
            is_alive = bool(resp and resp[0] == 0x5A)

        except Exception:
            pass

        return is_alive


    async def is_socks5(self, _host: str, _port: int, _delay_before_request: float = 0.0) -> bool:
        """
        Checks if the proxy server supports the SOCKS5 protocol.

        It attempts to initiate a SOCKS5 handshake. If the proxy responds with a valid
        SOCKS5 version byte (0x05), it is considered to support SOCKS5.

        Args:
            _host (str):
                The hostname or IP address of the proxy.
            _port (int):
                The port number on which the proxy is running.
            _delay_before_request (float):
                Optional delay (in seconds) before attempting the connection.

        Returns:
            bool:
                - True if the proxy responds with a valid SOCKS5 response.
                - False if something went wrong.

        Examples:
        ```
            >>> is_socks5 = await detector.is_socks5("10.10.1.1", 1080)
            >>> print(is_socks5)
            >>> False  # Result of the print
        ```
        """

        is_alive: bool = False

        self.logger.log(f"Delaying SOCKS5 request ({_host}:{_port}) for {_delay_before_request} seconds.")
        await asyncio.sleep(delay = _delay_before_request)

        try:
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(_host, _port),
                timeout = self.connection_timeout
            )
            
            writer.write(b"\x05\x01\x00")
            resp = await asyncio.wait_for(
                reader.read(10),
                timeout = self.connection_timeout
            )
            
            writer.close()
            await writer.wait_closed()

            is_alive = bool(resp and resp[0] == 0x05)

        except Exception:
            pass

        return is_alive


    async def is_http(self, _host: str, _port: int, _delay_before_request: float = 0.0) -> bool:
        """
        Checks if the proxy server supports the HTTP protocol.

        Sends a raw HTTP GET request and analyzes the response headers to determine
        if it behaves like an HTTP proxy (i.e., returns a valid HTTP response).

        Args:
            _host (str):
                The hostname or IP address of the proxy.
            _port (int):
                The port number on which the proxy is running.
            _delay_before_request (float):
                Optional delay (in seconds) before attempting the connection.

        Returns:
            bool:
                - True if a valid HTTP response has been received.
                - False if something went wrong.

        Examples:
        ```
            >>> is_http = await detector.is_http("192.168.1.100", 8080)
            >>> print(is_http)
            >>> True  # Result of the print
        ```
        """

        is_alive: bool = False

        self.logger.log(f"Delaying HTTP request ({_host}:{_port}) for {_delay_before_request} seconds.")
        await asyncio.sleep(delay = _delay_before_request)

        try:
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(_host, _port),
                timeout = self.connection_timeout
            )

            http_req = (
                "GET http://example.com/ HTTP/1.1\r\n"
                "Host: example.com\r\n"
                "Connection: keep-alive\r\n"
                "\r\n"
            )


            writer.write(http_req.encode('ascii'))
            resp = await asyncio.wait_for(
                reader.read(15),
                timeout = self.connection_timeout
            )

            writer.close()
            await writer.wait_closed()

            is_alive = bool(
                resp.startswith(b"HTTP/") and
                b"200" in resp and
                b"407" not in resp and
                b"500" not in resp and
                b"502" not in resp
            )

        except:
            pass

        return is_alive


    # Detect whether the scheme of proxy is HTTPS
    async def is_https(self, _host: str, _port: int, _delay_before_request: float = 0.0) -> bool:
        """
        Checks if the proxy server supports the HTTPS protocol.

        Attempts to establish an SSL/TLS handshake with the proxy. If the connection
        completes successfully without certificate verification, it is assumed to support HTTPS.

        Args:
            _host (str):
                The hostname or IP address of the proxy.
            _port (int):
                The port number on which the proxy is running.
            _delay_before_request (float):
                Optional delay (in seconds) before attempting the connection.

        Returns:
            bool:
                - True if the SSL/TLS handshake succeeds.
                - False if something went wrong.

        Examples:
        ```
            >>> is_https = await detector.is_https("proxy.example.com", 443)
            >>> print(is_https)
            >>> False  # Result of the print
        ```
        """

        is_alive: bool = False

        self.logger.log(f"Delaying HTTPS request ({_host}:{_port}) for {_delay_before_request} seconds.")
        await asyncio.sleep(delay = _delay_before_request)

        try:

            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE

            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(_host, _port, ssl=context),
                timeout = self.connection_timeout
            )

            writer.close()
            await writer.wait_closed()

            is_alive: bool = True

        except Exception:
            pass

        return is_alive


    # Detect proxy scheme in parallel
    async def detect_proxy_scheme_parallel(self, _host: str, _port: int) -> typing.Optional[str]:
        """
        Attempts to detect the proxy's scheme by testing all known protocols in parallel.

        Runs asynchronous checks for HTTPS, HTTP, SOCKS5, and SOCKS4 with staggered delays.
        Returns the first scheme that successfully completes its protocol-specific handshake.

        Args:
            _host (str):
                The hostname or IP address of the proxy.
            _port (int):
                The port number on which the proxy is running.

        Returns:
              str | None:
                - The name of the detected scheme (e.g., 'HTTP', 'SOCKS5'), or None if none matched.

        Examples:
        ```
            >>> scheme = await detector.detect_proxy_scheme_parallel("127.0.0.1", 1080)
            >>> print(scheme)
            >>> SOCKS5  # Result of the print
        ```
        """

        aio = AIOBase(_semaphore = 4)

        # Add https proxy detect method
        aio.add_task(self.is_https, _host, _port, 1.9)
        aio.add_task(self.is_http, _host, _port, 1.4)
        aio.add_task(self.is_socks5, _host, _port, 0.9)
        aio.add_task(self.is_socks4, _host, _port, 0.5)

        results = await aio.run_tasks()
    
        for result, proxy_scheme in zip(results, self.PROXY_SCHEMES):
            self.logger.log(f"{result}, {proxy_scheme}")

            if not result:
                continue

            self.logger.log(f"({_host}:{_port}) is scheme of {proxy_scheme} proxy.")
            return proxy_scheme

        return None


# Proxy tester class, used for testing a proxy.
class ProxyTester:
    """
    A class responsible for testing the connectivity and detecting the scheme of proxy servers.

    Attributes:
        debug (bool): Enables debug logging if set to True.
        connection_timeout (int): Timeout for connection attempts in seconds.
        proxy_scheme_detector (ProxySchemeDetector): Tool for detecting proxy schemes (SOCKS4/5, HTTP/HTTPS).
        logger (Logger): Logger instance for outputting debug/info messages.

    Methods:
        check_connection(_scheme, _host, _port):
            Asynchronously tests whether a connection can be made to a given proxy using the specified scheme.

        detect_scheme(_host, _port):
            Asynchronously attempts to determine the correct proxy scheme by testing all supported types in parallel.

    Examples:
    ```
        >>> tester = ProxyTester(_connection_timeout=10, _debug=True)

        >>> result = await tester.check_connection("SOCKS5", "192.168.1.1", 1080)
        >>> print(result)
        >>> True # Result of the print

        >>> host, port, scheme = await tester.detect_scheme("192.168.1.1", 1080)
        >>> print(f"{host}:{port} uses {scheme}")
        >>> 192.168.1.1:1080 uses SOCKS5 # Result of the print
    ```
    """

    def __init__(
            self,
            _connection_timeout: int = 5,
            _debug: bool = False
        ) -> None:
        """
        Initializes the ProxyTester instance with configuration for timeout and logging.

        Creates internal instances of ProxySchemeDetector and Logger to handle proxy testing
        and logging output.

        Args:
            _connection_timeout (int):
                The timeout value (in seconds) to use for proxy connection attempts.
            _debug (bool):
                If True, enables debug logging output for verbose feedback.

        Examples:
        ```
            >>> tester = ProxyTester(_connection_timeout=10, _debug=True)

            >>> print(tester.connection_timeout)
            >>> 10  # Result of the print

            >>> print(tester.debug)
            >>> True  # Result of the print
        ```
        """

        self.debug: bool = _debug

        # Connection information
        self.connection_timeout: int = _connection_timeout


        # Create the ProxySchemeDetector instance, for detecting the proxy scheme
        self.proxy_scheme_detector: ProxySchemeDetector = ProxySchemeDetector(
            _connection_timeout = self.connection_timeout, # _connection_timeout is set by forwarding the parameter from ProxyTester
            _debug = self.debug
        )

        # Create the logger instance
        self.logger: Logger = Logger(
            _logger_name = "ProxyTester",
            _debug = self.debug
        )


    async def check_connection(self, _scheme: typing.Literal["HTTPS", "HTTP", "SOCKS5", "SOCKS4"], _host: str, _port: int) -> bool:
        """
        Checks whether a connection to the given proxy server can be established using a specific scheme.

        This method delegates the connection attempt to a dedicated scheme-specific detector method.

        Args:
            _scheme (Literal["HTTPS", "HTTP", "SOCKS5", "SOCKS4"]):
                The proxy protocol to use for the connection test.
            _host (str):
                The IP address or hostname of the proxy.
            _port (int):
                The port number on which the proxy is running.

        Returns:
            bool:
                - True if the connection is successful.
                - False if the connection fails or the scheme is invalid.

        Raises:
            ValueError:
                If the provided scheme is not one of the allowed options.

        Examples:
        ```
            >>> tester = ProxyTester(_debug=True)

            >>> success = await tester.check_connection("HTTP", "192.168.0.1", 8080)
            >>> print(success)
            >>> True  # Result of the print
        ```
        """

        _scheme = _scheme.upper()
        start = time.perf_counter()

        if _scheme not in ["HTTPS", "HTTP", "SOCKS5", "SOCKS4"]:
            raise ValueError(f"Couldn't recognize the scheme you provided: {_scheme}")

        result: typing.Optional[bool] = None

        detectors: dict[str, typing.Callable[[str, int], typing.Awaitable[bool]]] = {
            "HTTPS": self.proxy_scheme_detector.is_https,
            "HTTP": self.proxy_scheme_detector.is_http,
            "SOCKS5": self.proxy_scheme_detector.is_socks5,
            "SOCKS4": self.proxy_scheme_detector.is_socks4
        }

        result: bool = await detectors[_scheme](_host = _host, _port = _port)

        self.logger.log(f"Connection for ({_scheme}://{_host}:{_port}) was established: ({self.logger.CLR.GREEN if bool(result) else self.logger.CLR.RED}{bool(result)}{self.logger.CLR.RESET}) in {(time.perf_counter() - start):.2f} seconds.")

        return result if result is not None else False


    async def detect_scheme(self, _host: str, _port: int) -> tuple[str, int, str | None]:
        """
        Attempts to determine the correct scheme (protocol) of a proxy server.

        It launches parallel checks for all supported schemes (SOCKS4, SOCKS5, HTTP, HTTPS) and
        returns the first one that succeeds.

        Args:
            _host (str):
                The hostname or IP address of the proxy.
            _port (int):
                The port number on which the proxy is operating.

        Returns:
               tuple[str, int, str | None]:
                - The host address.
                - The port number.
                - The detected scheme (e.g., 'HTTP', 'SOCKS5'), or None if none succeeded.

        Examples:
        ```
            >>> tester = ProxyTester(_debug=True)

            >>> host, port, scheme = await tester.detect_scheme("10.0.0.1", 9050)
            >>> print(host, port, scheme)
            >>> 10.0.0.1 9050 SOCKS5  # Result of the print
        ```
        """
        start: float = time.perf_counter()

        proxy_scheme = await self.proxy_scheme_detector.detect_proxy_scheme_parallel(_host = _host, _port = _port)

        if not proxy_scheme:
            self.logger.log(
                f"Testing proxy connection {self.logger.CLR.RED}failed{self.logger.CLR.RESET} ({proxy_scheme}://{_host}:{_port}) in {(time.perf_counter() - start):.2f} seconds."
            )
        else:
            self.logger.log(
                f"Testing proxy connection {self.logger.CLR.GREEN}succeeded{self.logger.CLR.RESET} ({proxy_scheme}://{_host}:{_port}) in {(time.perf_counter() - start):.2f} seconds."
            )

        return _host, _port, proxy_scheme
