import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from ProxySea.imports import asyncio
from ProxySea import ProxySea
from ProxySea.util import ProxyInfo



async def main() -> None:
    # Create ProxySea instance with debugger set on.
    PS: ProxySea = ProxySea(_debug = True)

    # Create list of proxies.
    proxies: list[ProxyInfo] = [
        ProxyInfo(_scheme = "HTTP", _host = "123.123.123", _port = 8000),
        ProxyInfo(_scheme = "HTTPS", _host = "124.124.124", _port = 8000),
        ProxyInfo(_scheme = None, _host = "125.125.125", _port = 8000)
    ]

    # Test all provided proxies.tested_proxies: list[ProxyInfo] = await PS.test_proxies(_proxies = proxies, _concurrent_tasks = 500)
    # Provided proxies have to be an instance of ProxyInfo class.
    tested_proxies: list[ProxyInfo] = await PS.test_proxies(_proxies = proxies, _concurrent_tasks = 500)

    # Limit proxies to be shown in terminal.
    [print(proxy) for index, proxy in enumerate(tested_proxies) if index < 5]

asyncio.run(main = main())
