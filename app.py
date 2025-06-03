import asyncio, requests
from ProxySea import ProxySea
from ProxySea.util import ProxyInfo

async def main() -> None:
    PS: ProxySea = ProxySea(_debug = True)
    proxies = await PS.fetch_proxies()
    tested_proxies = await PS.test_proxies(_proxies = proxies)

    filtered_proxies: list[ProxyInfo] = [proxy for proxy in tested_proxies if proxy.scheme in ["HTTP", "HTTPS"]]
    
    for proxy in filtered_proxies:
        # Get the first proxy from the list
        requests_proxy = proxy

        requests_proxies: dict[str, str] = {
            "http":  f"{requests_proxy.host}:{requests_proxy.port}",
            "https": f"{requests_proxy.host}:{requests_proxy.port}"
        }

        print(f"Sending requests via |{requests_proxy}| proxy.")

        # Set the base URL for requesting the resource
        BASE_URL: str = "https://ipinfo.io/json"

        res = None

        try:
            # Send request via the selected proxy
            res = requests.get(url = BASE_URL, proxies = requests_proxies, timeout = 5, verify = False)
        except Exception as e:
            pass
            # print(f"Got error {e}")

        if res:
            # Show the response
            print(f"{res.text}\n")

asyncio.run(main = main())
