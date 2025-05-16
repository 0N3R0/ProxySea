from ..util import ProxyProvider, ProxyInfo, MiniJS
from ..imports import bs4, lxml, typing

class SpysOneScrapper:
    def __init__(self, _html: str) -> None:
        self.HTML = bs4.BeautifulSoup(_html, "lxml")
        self.DETAILS = self.HTML.select("table")[1].select("tr")
        self.MiniJS = MiniJS()

        self.ANONYMITY_LEVELS: dict[str] = {
            "hia": "HIGH",
            "anm": "MEDIUM",
            "noa": "LOW"
        }

    def find_obfuscated_script(self) -> bs4.PageElement | None:
        all_scripts: list[bs4.PageElement] = self.HTML.select("script")

        obfs_flag = "eval(function(p,"
        for script in all_scripts:
            if obfs_flag in script.get_text():
                return script.get_text()

        return None

    def get_proxies(self) -> None:
        # Find and deobfuscate javascript with values
        obfuscated_script: str = self.find_obfuscated_script()
        deobfuscated_script: str = self.MiniJS.deobfuscate_script(script = obfuscated_script)
        self.MiniJS.set_temp_script(deobfuscated_script)


        proxy_list: list[str] = []

        for detail in self.DETAILS:
            if not "document.write(" in str(detail) or not "this.style" in str(detail) or "Proxy servers sorted by country" in str(detail):
                continue

            ip: str = detail.select_one("td:nth-child(1) > font").get_text().strip().replace(" ", "")
            # Find obfuscated script port
            obfuscated_port: str = detail.select_one("td:nth-child(1) > font > script").get_text()
            # Deobfuscate script port
            port = str(self.MiniJS.get_value_from_temp_script(obfuscated_port.replace('document.write(":', '("'))).strip().replace(" ", "")
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
        self.DEBUG = _debug

        super().__init__(
            _provider_url = "https://spys.one/en/",
            _debug = self.DEBUG
        )

    async def fetch_proxies(self) -> None:
        HTML = await self.download_page()

        if not HTML:
            return

        SOE: SpysOneScrapper = SpysOneScrapper(_html = HTML)
        proxies: list[str] = SOE.get_proxies()

        if not proxies:
            return

        for proxy in proxies:
            await self.add_new_proxy(_new_proxy = proxy)
