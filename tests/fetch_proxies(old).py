import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from ProxySea.imports import asyncio
from ProxySea import ProxySea
from ProxySea.util import ProxyInfo



async def main() -> None:
    # Create ProxySea instance with debugger set on.
    PS: ProxySea = ProxySea(_debug = True)

    # Fetch proxies from all available providers.
    proxies: list[ProxyInfo] = await PS.fetch_proxies()
    # Limit proxies to be shown in terminal.
    [print(proxy) for index, proxy in enumerate(proxies) if index < 5]

asyncio.run(main = main())
