from ProxySea.util.proxy_tester import ProxyTypeDetector
import asyncio

async def main() -> None:
    # tester = ProxyTester(_connection_timeout = 5, _debug = True)
    detector = ProxyTypeDetector(_connection_timeout = 5, _debug = True)
    scheme, host, port = "HTTP://71.14.218.2:8080".replace("//", "").split(':')

    # await tester.check_connection(_scheme = scheme, _host = host, _port = port)
    # await tester.detect_type(_host = host, _port = port)

    print(f"is_{scheme}: {await detector.is_http(_host = host, _port = port)}")

asyncio.run(main = main())