# Z_Test

# from ProxySea.providers.free_proxy_list import FreeProxyList
from ProxySea.util.proxy_tester import ProxyTester
from ProxySea.providers.spys_one import SpysOne
from ProxySea.providers.free_proxy_list import FreeProxyList
from typing import Literal
import asyncio, datetime

def save_to_file(data: str | list[str], _file_path: str, _mode: Literal["append", "write"] = "append"):
    write_mode = "a" if _mode == "append" else "w"

    with open(file = _file_path, mode = write_mode, encoding = "utf-8") as f:
        if type(data) is str:
            f.write(data)
            return
        
        for line in data:
            f.write(line)


async def main() -> None:
    fpl = FreeProxyList()
    # fpl = SpysOne()

    await fpl.setup()

    await fpl.test_all_proxies(500)

    save_to_file(f"\n\n\n{str(datetime.datetime.now()).split('.')[0]} (proxies flagged as working: {len([prx for prx in fpl.PROXIES if prx.IS_ACTIVE])})\n\n", _file_path = "swp.txt")
    save_to_file([f"{proxy}\n" for proxy in fpl.PROXIES if proxy.IS_ACTIVE], _file_path = "swp.txt")

    for proxy in fpl.PROXIES:
        print(proxy)

asyncio.run(main = main())
