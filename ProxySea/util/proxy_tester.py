from ..logger import Logger
from .aio import AIOBase

from ..imports import typing, asyncio, time, ssl, random

class ProxyInfo:
    def __init__(self, _type: typing.Literal["HTTPS", "HTTP", "SOCKS5", "SOCKS4", None], _host: str, _port: int, _anonymity_level: typing.Literal["high", "mid", "low"]) -> None:
        self.TYPE: str = _type
        self.HOST: str = _host
        self.PORT: str = int(_port) if _port else _port
        self.PROXY_ANONYMITY_LEVEL: str = _anonymity_level

        self.IS_ACTIVE: bool = False
        self.CONNECTION_RETRIES: int = 0
        self.BLACKLIST_AFTER:int = 3


    @property
    def ID(self) -> str:
        return f"{self.HOST}|{self.PORT}"

    @property
    def IS_BLACKLISTED(self) -> bool:
        return self.CONNECTION_RETRIES > self.BLACKLIST_AFTER


    def change_proxy_type(self, _type: typing.Literal["HTTPS", "HTTP", "SOCKS5", "SOCKS4"]) -> None:
        if not _type:
            raise ValueError(f"[ProxyInfo (change_proxy_type)] You have to provide _type. {self.ID=} || {_type=}")
        
        if _type not in ["HTTPS", "HTTP", "SOCKS5", "SOCKS4"]:
            raise ValueError(f"[ProxyInfo (change_proxy_type)] Your provided _type should be one of them ['HTTPS', 'HTTP', 'SOCKS5', 'SOCKS4']. {self.ID=} || {_type=}")

        self.TYPE = _type

    def change_is_active(self, _active: bool) -> None:
        if not isinstance(_active, bool):
            raise ValueError(f"[ProxyInfo (change_is_active)] You have to provide bool value as flag. {self.ID=} || {_active=}")

        self.IS_ACTIVE = _active

    def update_connection_retries(self) -> None:
        if self.IS_BLACKLISTED:
            return

        if not self.IS_ACTIVE:
            self.CONNECTION_RETRIES += 1
            return

        self.CONNECTION_RETRIES = 0


    def __str__(self) -> str:
        return f"({self.PROXY_ANONYMITY_LEVEL=} | {self.IS_ACTIVE=} | {self.IS_BLACKLISTED=} | {self.CONNECTION_RETRIES=}) {self.TYPE}://{self.HOST}:{self.PORT}"


class ProxyTypeDetector:
    def __init__(
            self,
            _connection_timeout: int = 3,
            _debug: bool = False
        ) -> None:
        self.DEBUG: bool = _debug

        # Connection information
        self.CONNECTION_TIMEOUT: int = _connection_timeout

        # Basic informations
        self.PROXY_TYPES: list[str] = ["HTTPS", "HTTP", "SOCKS5", "SOCKS4"]


        # Create the logger instance
        self.Logger: Logger = Logger(
            _logger_name = "ProxyType",
            _debug = self.DEBUG
        )


    # Detect whether the type of proxy is SOCKS4
    async def is_socks4(self, _host: str, _port: int, _delay_before_request: float = 0.5) -> bool:
        is_alive: bool = False

        self.Logger.log(f"Delaying SOCKS4 request ({_host}:{_port}) for {_delay_before_request} seconds.")
        await asyncio.sleep(delay = _delay_before_request)

        try:

            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(_host, _port),
                timeout = self.CONNECTION_TIMEOUT
            )

            # Używamy trybu SOCKS4a: DSTIP = 0.0.0.1 oznacza, że podajemy nazwę domeny
            port_bytes = (80).to_bytes(2, 'big')
            ip_bytes = b"\x00\x00\x00\x01"

            user = b""
            domain = b"example.com\x00"
            request = b"\x04\x01" + port_bytes + ip_bytes + user + domain

            writer.write(request)
            resp = await asyncio.wait_for(
                reader.read(8),
                timeout = self.CONNECTION_TIMEOUT
            )

            writer.close()
            await writer.wait_closed()

            is_alive = bool(resp and resp[0] == 0x00)

        except Exception:
            pass

        return is_alive


    # Detect whether the type of proxy is SOCKS5
    async def is_socks5(self, _host: str, _port: int, _delay_before_request: float = 0.9) -> bool:
        is_alive: bool = False

        self.Logger.log(f"Delaying SOCKS5 request ({_host}:{_port}) for {_delay_before_request} seconds.")
        await asyncio.sleep(delay = _delay_before_request)

        try:

            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(_host, _port),
                timeout = self.CONNECTION_TIMEOUT
            )
            
            writer.write(b"\x05\x01\x00")
            resp = await asyncio.wait_for(
                reader.read(10),
                timeout = self.CONNECTION_TIMEOUT
            )
            
            writer.close()
            await writer.wait_closed()

            is_alive = bool(resp and resp[0] == 0x05)

        except Exception:
            pass

        return is_alive


    # Detect whether the type of proxy is HTTP
    async def is_http(self, _host: str, _port: int, _delay_before_request: float = 1.4) -> bool:
        is_alive: bool = False

        self.Logger.log(f"Delaying HTTP request ({_host}:{_port}) for {_delay_before_request} seconds.")
        await asyncio.sleep(delay = _delay_before_request)

        try:

            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(_host, _port),
                timeout = self.CONNECTION_TIMEOUT
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
                timeout = self.CONNECTION_TIMEOUT
            )

            writer.close()
            await writer.wait_closed()

            self.Logger.log(f"RESPONSE: {resp}")

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


    # Detect whether the type of proxy is HTTPS
    async def is_https(self, _host: str, _port: int, _delay_before_request: float = 1.9) -> bool:
        is_alive: bool = False

        self.Logger.log(f"Delaying HTTPS request ({_host}:{_port}) for {_delay_before_request} seconds.")
        await asyncio.sleep(delay = _delay_before_request)

        try:

            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE

            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(_host, _port, ssl=context),
                timeout = self.CONNECTION_TIMEOUT
            )

            writer.close()
            await writer.wait_closed()

            is_alive: bool = True

        except Exception:
            pass

        return is_alive


    # Detect proxy type in parallel
    async def detect_proxy_type_parallel(self, _host: str, _port: int) -> str:
        aio = AIOBase(_semaphore = 4)
        # aio = AIOBase(_semapphore = 4)

        # Add https proxy detect method
        aio.add_task(self.is_https, _host, _port)
        aio.add_task(self.is_http, _host, _port)
        aio.add_task(self.is_socks5, _host, _port)
        aio.add_task(self.is_socks4, _host, _port)

        results = await aio.run_tasks()
    
        for result, proxy_type in zip(results, self.PROXY_TYPES):
            self.Logger.log(f"{result}, {proxy_type}")

            if not result:
                continue

            self.Logger.log(f"({_host}:{_port}) is type of {proxy_type} proxy.")

            return proxy_type


# Proxy tester class, used for testing a proxy.
class ProxyTester:
    def __init__(
            self,
            _connection_timeout: int = 5,
            _debug: bool = False
        ) -> None:
        self.DEBUG: bool = _debug

        # Connection information
        self.CONNECTION_TIMEOUT: int = _connection_timeout


        # Create the ProxyTypeDetector instance, for detecting the proxy type
        self.ProxyTypeDetector: ProxyTypeDetector = ProxyTypeDetector(
            _connection_timeout = self.CONNECTION_TIMEOUT, # _connection_timeout is set by forwarding the parameter from ProxyTester
            _debug = self.DEBUG
        )

        # Create the logger instance
        self.Logger: Logger = Logger(
            _logger_name = "ProxyTester",
            _debug = self.DEBUG
        )

    async def check_connection(self, _scheme: typing.Literal["HTTPS", "HTTP", "SOCKS5", "SOCKS4"], _host: str, _port: int) -> bool:
        """
        This method is used to test if the proxy is available.

        If connection was established successfully, this method returns True else False.
        
        Example:
            is_alive = check_connection(...) -> True
        """

        start = time.perf_counter()

        if _scheme not in ["HTTPS", "HTTP", "SOCKS5", "SOCKS4"]:
            raise ValueError(f"Couldn't recognize the scheme you provided: {_scheme}")

        result: bool | None = None

        if _scheme == "HTTPS":
            result = await self.ProxyTypeDetector.is_https(
                _host = _host,
                _port = _port,
                _delay_before_request = 0.0
            )

        if _scheme == "HTTP":
            result = await self.ProxyTypeDetector.is_http(
                _host = _host,
                _port = _port,
                _delay_before_request = 0.0
            )

        if _scheme == "SOCKS5":
            result = await self.ProxyTypeDetector.is_socks5(
                _host = _host,
                _port = _port,
                _delay_before_request = 0.0
            )

        if _scheme == "SOCKS4":
            result = await self.ProxyTypeDetector.is_socks4(
                _host = _host,
                _port = _port,
                _delay_before_request = 0.0
            )

        self.Logger.log(f"Connection for ({_scheme}://{_host}:{_port}) was established: ({self.Logger.CLR.GREEN if bool(result) else self.Logger.CLR.RED}{bool(result)}{self.Logger.CLR.RESET}) in {(time.perf_counter() - start):.2f} seconds.")

        return bool(result)


    async def detect_type(self, _host: str, _port: int) -> tuple[str, int, str | None]:
        """
        This method returns tuple[pos1, pos2, pos3]:
            Position 1: HOST (Providen _host)
            Position 2: PORT (Providen _port)
            Position 3: TYPE (Detected type of proxy ["HTTPS", "HTTP", "SOCKS5", "SOCKS4"] or None if connection couldn't be established)

            Example:
                host, port, scheme = detect_type(...)
        """
        start: float = time.perf_counter()

        proxy_type = await self.ProxyTypeDetector.detect_proxy_type_parallel(_host = _host, _port = _port)

        if not proxy_type:
            self.Logger.log(
                f"Testing proxy connection {self.Logger.CLR.RED}failed{self.Logger.CLR.RESET} ({proxy_type}://{_host}:{_port}) in {(time.perf_counter() - start):.2f} seconds."
            )
        else:
            self.Logger.log(
                f"Testing proxy connection {self.Logger.CLR.GREEN}succeeded{self.Logger.CLR.RESET} ({proxy_type}://{_host}:{_port}) in {(time.perf_counter() - start):.2f} seconds."
            )

        return _host, _port, proxy_type
