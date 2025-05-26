# from ProxySea.providers.free_proxy_list import FreeProxyList
from ProxySea.util.proxy_tester import ProxyTester
from ProxySea.providers.spys_one import SpysOne
from ProxySea.providers.free_proxy_list import FreeProxyList
from ProxySea.providers import ProvidersManager
from ProxySea.util import ProxyInfo

from typing import Literal
import asyncio, datetime, time

def save_to_file(data: str | list[str], _file_path: str, _mode: Literal["append", "write"] = "append"):
    write_mode = "a" if _mode == "append" else "w"

    with open(file = _file_path, mode = write_mode, encoding = "utf-8") as f:
        if type(data) is str:
            f.write(data)
            return
        
        for line in data:
            f.write(line)


async def main() -> None:
    PM: ProvidersManager = ProvidersManager(_debug = True)

    # start = time.perf_counter()

    fetched_proxies = await PM.fetch_proxies()
    [print(proxy, len(fetched_proxies)) for proxy in fetched_proxies]

    tested_proxies = await PM.test_proxies(_proxies = fetched_proxies)
    [print(proxy, len(tested_proxies)) for proxy in tested_proxies]

    print()

    active_proxies: list = PM.filter_proxies(_proxies = tested_proxies, _active = True)
    [print(proxy, len(active_proxies)) for proxy in active_proxies]

    # all_proxies: list = []

    # for provider in PM.ProxyProviders:
    #     for proxy in provider.PROXIES:
    #         all_proxies.append(proxy)
    #         print(f"{provider.DOMAIN} > {proxy}")

    # print(f"Checked ({len(all_proxies)}) proxies in {(time.perf_counter() - start):.2f}")

    # save_to_file(f"\n\n\n{str(datetime.datetime.now()).split('.')[0]} (proxies flagged as working: {len([prx for prx in all_proxies if prx.IS_ACTIVE])})\n\n", _file_path = "swp.txt")
    # save_to_file([f"{prx}\n" for prx in all_proxies if prx.IS_ACTIVE], _file_path = "swp.txt")

    # while True:
    #     res = input("Provide command: ")

    #     if res == "get_proxies":
    #         _active: bool = bool(input("Do you wanna active proxies? y/n: ") == "y")
    #         _proxy_scheme: str = input("Provide proxy scheme ['HTTPS', 'HTTP', 'SOCKS5', 'SOCKS4', 'ALL']: ")
    #         _anonymity_level: str = input("Provide anonymity level ['HIGH', 'MEDIUM', 'LOW', 'ALL']: ")

    #         proxies = await PM.get_proxies(
    #             _active = _active,
    #             _scheme = _proxy_scheme,
    #             _anonymity_level = _anonymity_level
    #         )

    #         for proxy in proxies:
    #             print(proxy)


    # Testing provider one by one
    # fpl = FreeProxyList()
    # fpl = SpysOne(_debug = False)

    # await fpl.fetch_proxies()

    # res = await fpl.test_all_proxies(500)
    # for proxy in res:
    #     print(proxy)

    # save_to_file(f"\n\n\n{str(datetime.datetime.now()).split('.')[0]} (proxies flagged as working: {len([prx for prx in fpl.PROXIES if prx.IS_ACTIVE])})\n\n", _file_path = "swp.txt")
    # save_to_file([f"{proxy}\n" for proxy in fpl.PROXIES if proxy.IS_ACTIVE], _file_path = "swp.txt")

    # for proxy in fpl.PROXIES:
    #     print(proxy)

asyncio.run(main = main())
