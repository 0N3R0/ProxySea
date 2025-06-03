import asyncio

from ProxySea import ProxySea
from ProxySea.util import ProxyInfo

# Initialize the asynchronous ProxySea module
PS: ProxySea = ProxySea(_debug = True)

# Fetch proxies from public sources using up to 10 concurrent tasks
fetched_proxies: list[ProxyInfo] = asyncio.run(PS.fetch_proxies(_concurrent_tasks = 10))

# Print each fetched proxy
print("Fetched proxies:")
for proxy in fetched_proxies:
    print(proxy)
