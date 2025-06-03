import asyncio

from ProxySea import ProxySea
from ProxySea.util import ProxyInfo

# Initialize the asynchronous ProxySea module
PS: ProxySea = ProxySea(_debug = True)

# Fetch proxies from public sources using up to 10 concurrent tasks
fetched_proxies: list[ProxyInfo] = asyncio.run(
    PS.fetch_proxies(_concurrent_tasks = 10)
)

# Print all fetched proxies
print("Fetched proxies:")
for proxy in fetched_proxies:
    print(proxy)

# Test all fetched proxies using up to 500 concurrent tasks
tested_proxies: list[ProxyInfo] = asyncio.run(
    PS.test_proxies(_proxies = fetched_proxies, _concurrent_tasks = 500)
)

# Print all tested proxies
print("\nTested proxies:")
for proxy in tested_proxies:
    print(proxy)

# Filter and print proxies using the SOCKS5 protocol
print("\nProxies using the SOCKS5 protocol:")
for proxy in [p for p in tested_proxies if p.scheme == "SOCKS5"]:
    print(proxy)

# Filter and print active HTTP proxies with HIGH anonymity
print("\nActive SOCKS5 proxies with HIGH anonymity:")
for proxy in [p for p in tested_proxies if p.scheme == "HTTP" and p.anonymity_level == "HIGH"]:
    print(proxy)
