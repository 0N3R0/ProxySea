from ..util import ProxyInfo, ProxyProvider
from ..imports import bs4, lxml, typing

class FreeProxyListScrapper:
    def __init__(self, _html: str) -> None:
        self.html = bs4.BeautifulSoup(_html, "lxml")
        
        self.ANONYMITY_LEVELS: dict[str] = {
            "elite proxy": "HIGH",
            "anonymous": "MEDIUM",
            "transparent": "LOW"
        }

    def scrape_proxies(self) -> list[str]:
        table = self.html.select_one("#list > div > div.table-responsive > div > table > tbody")
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
                    _scheme = None,
                    _host = host,
                    _port = port,
                    _anonymity_level = self.ANONYMITY_LEVELS[anonymity]
                )
            )

        return proxies


class FreeProxyList(ProxyProvider):
    def __init__(self, _debug: bool = False) -> None:
        self.debug: bool = _debug

        super().__init__(
            _provider_url = "https://free-proxy-list.net/",
            _debug = self.debug
        )

    async def fetch_proxies(self) -> None:
        html = await self.download_page()

        if not html:
            return []

        free_proxy_list_scrapper: FreeProxyListScrapper = FreeProxyListScrapper(_html = html)
        proxies: list[str] = free_proxy_list_scrapper.scrape_proxies()

        if not proxies:
            return []

        for proxy in proxies:
            self.add_new_proxy(_new_proxy = proxy)

        return self.proxies
