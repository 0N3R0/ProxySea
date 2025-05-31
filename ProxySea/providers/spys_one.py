from ..util import ProxyProvider, ProxyInfo, MiniJS
from ..imports import bs4, lxml, typing

class SpysOneScrapper:
    def __init__(self, _html: str) -> None:
        self.html = bs4.BeautifulSoup(_html, "lxml")
        self.details = self.html.select("table")[1].select("tr")
        self.mini_js = MiniJS()

        self.ANONYMITY_LEVELS: dict[str] = {
            "hia": "HIGH",
            "anm": "MEDIUM",
            "noa": "LOW"
        }

    def find_obfuscated_script(self) -> bs4.PageElement:
        all_scripts: list[bs4.PageElement] = self.html.select("script")

        obfs_flag = "eval(function(p,"
        for script in all_scripts:
            if obfs_flag in script.get_text():
                return script.get_text()

        return None

    def get_proxies(self) -> None:
        # Find and deobfuscate javascript with values
        obfuscated_script: str = self.find_obfuscated_script()
        deobfuscated_script: str = self.mini_js.deobfuscate_script(_script = obfuscated_script)
        self.mini_js.set_temp_script(_new_script = deobfuscated_script)

        proxy_list: list[str] = []

        for detail in self.details:
            if not "document.write(" in str(detail) or not "this.style" in str(detail) or "Proxy servers sorted by country" in str(detail):
                continue

            ip: str = detail.select_one("td:nth-child(1) > font").get_text().strip().replace(" ", "")
            # Find obfuscated script port
            obfuscated_port: str = detail.select_one("td:nth-child(1) > font > script").get_text()
            # Deobfuscate script port
            port = str(self.mini_js.get_value_from_temp_script(obfuscated_port.replace('document.write(":', '("'))).strip().replace(" ", "")
            # Proxy anonymity
            anonymity: str = detail.select_one("td:nth-child(3) > font").get_text().lower()

            if not ip or not port:
                continue

            proxy_list.append(
                ProxyInfo(
                    _scheme = None,
                    _host = ip,
                    _port = port,
                    _anonymity_level = self.ANONYMITY_LEVELS[anonymity]
                )
            )
        
        return proxy_list


class SpysOne(ProxyProvider):
    def __init__(self, _debug: bool = False) -> None:
        self.debug: bool = _debug

        super().__init__(
            _provider_url = "https://spys.one/en/",
            _debug = self.debug
        )

    async def fetch_proxies(self) -> list[ProxyInfo]:
        html = await self.download_page()

        if not html:
            return []

        spys_one_scrapper: SpysOneScrapper = SpysOneScrapper(_html = html)
        proxies: list[str] = spys_one_scrapper.get_proxies()

        if not proxies:
            return []

        return proxies
