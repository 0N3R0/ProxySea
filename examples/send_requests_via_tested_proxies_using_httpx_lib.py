import asyncio, requests
from ProxySea import ProxySea
from ProxySea.util import ProxyInfo

PS: ProxySea = ProxySea(_debug = True)

# Fetch proxies for testing
fetched_proxies: list[ProxyInfo] = asyncio.run(PS.fetch_proxies())

# Test fetched proxies before using them
tested_proxies: list[ProxyInfo] = asyncio.run(
    PS.test_proxies(_proxies = fetched_proxies)
)

# Filter only active HTTP proxies
http_proxies: list[ProxyInfo] = [
    proxy for proxy in tested_proxies
    if proxy.is_active and proxy.scheme == "HTTP"
]

if len(http_proxies) <= 0:
    raise ValueError("There are no ACTIVE HTTP proxies in http_proxies list.")

print(f"Found {len(http_proxies)} HTTP and ACTIVE proxies.")

# Iterate for each active http proxy
for proxy in http_proxies:
    # Get the first proxy from the list
    requests_proxy = proxy

    requests_proxies: dict[str, str] = {
        "http":  f"{requests_proxy.host}:{requests_proxy.port}",
        "https": f"{requests_proxy.host}:{requests_proxy.port}"
    }

    print(f"Sending request via |{requests_proxy}| proxy.")

    # Set the base URL for requesting the resource
    BASE_URL: str = "https://ipinfo.io/json"

    res = None

    try:
        # Send request via the selected proxy
        res = requests.get(url = BASE_URL, proxies = requests_proxies, timeout = 5, verify = False)
    except Exception as e:
        pass

    if res:
        # Show the response
        print(f"{res.text}\n")
