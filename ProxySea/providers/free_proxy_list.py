from ..util import ProxyInfo
from ..util import ProxyProvider
from ..imports import bs4, lxml

class FreeProxyListScrapper:
    def __init__(self, _html: str) -> None:
        self.HTML = bs4.BeautifulSoup(_html, "lxml")
        
        self.ANONYMITY_LEVELS: dict[str] = {
            "elite proxy": "high",
            "anonymous": "mid",
            "transparent": "low"
        }

    def scrape_proxies(self) -> list[str]:
        table = self.HTML.select_one("#list > div > div.table-responsive > div > table > tbody")
        proxies: list[str] = []

        # Check for every <tr> element in <tbody>
        for tableRow in table:
            proxy_info: list = tableRow.select("td")

            if not proxy_info:
                continue

            if not bool(proxy_info[0] and proxy_info[1]):
                continue

            host: str = proxy_info[0].get_text()
            port: str = proxy_info[1].get_text()
            anonymity: str = proxy_info[4].get_text()

            proxies.append(
                ProxyInfo(
                    _type = None,
                    _host = host,
                    _port = port,
                    _anonymity_level = self.ANONYMITY_LEVELS[anonymity]
                )
            )

        return proxies


class FreeProxyList(ProxyProvider):
    def __init__(self) -> None:
        super().__init__(
            _provider_url = "https://free-proxy-list.net/",
            _debug = True
        )

    async def setup(self) -> None:
        HTML = await self.download_page()

        if not HTML:
            return

        FPLS: FreeProxyListScrapper = FreeProxyListScrapper(_html = HTML)
        proxies: list[str] = FPLS.scrape_proxies()

        if not proxies:
            return

        for proxy in proxies:
            await self.add_new_proxy(_new_proxy = proxy)
            # await self.add_to_new_proxies(new_proxy = proxy)
