from .providers import ProvidersManager
from .api import ApiServer
from .util import ProxyInfo
from .logger import Logger

class ProxySea:
    def __init__(self, _debug: bool = False) -> None:
        self.DEBUG = _debug

        self.Logger: Logger = Logger(_name = "App", _debug = self.DEBUG)
        
        self.ProvidersManager: ProvidersManager = ProvidersManager(_debug = self.DEBUG)
        self.ApiServer: ApiServer = ApiServer()
    
    def run_api(self) -> None:
        ...
        # self.ApiServer.run()

    def scrape_proxies(self) -> list[ProxyInfo]:
        return self.ProvidersManager.fetch_proxies()

    def test_proxies(self) -> list[ProxyInfo]:
        ...
