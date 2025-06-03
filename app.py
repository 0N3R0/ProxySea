from ProxySea import ProxySea
import asyncio

async def main() -> None:
    PS: ProxySea = ProxySea(_debug = True)
    proxies = await PS.fetch_proxies()
    tested_proxies = await PS.test_proxies(_proxies = proxies)

asyncio.run(main = main())
