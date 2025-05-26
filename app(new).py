from ProxySea import ProxySea
from ProxySea.util import ProxyInfo
import asyncio

async def main() -> None:
    proxy_sea: ProxySea = ProxySea(_debug = True)
    proxies: list[ProxyInfo] = await proxy_sea.fetch_proxies()
    tested_proxies: list[ProxyInfo] = await proxy_sea.test_proxies(_proxies = proxies)

    [print(proxy) for proxy in proxies if proxy.is_active]

asyncio.run(main = main())
