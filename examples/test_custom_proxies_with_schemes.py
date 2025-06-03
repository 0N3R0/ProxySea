import asyncio, typing
from ProxySea import ProxySea
from ProxySea.util import ProxyInfo  # Import the ProxyInfo object

# Initialize the asynchronous ProxySea module
PS: ProxySea = ProxySea(_debug = True)

# Define your custom proxies; you can also load them from a file
proxies: list[str] = ["http://123.123.123:80", "socks5://199.190.231:443"]

# Convert the provided proxies into ProxyInfo objects
converted_proxies: list[ProxyInfo] = []

# Convert each "scheme://host:port" string into a ProxyInfo object
for proxy in proxies:
    # Extract scheme, host, and port from the proxy string
    scheme, host, port = proxy.replace("//", "").split(":")

    # Set the proxy scheme/protocol
    proxy_scheme: typing.Optional[str] = scheme

    # Set the proxy host
    proxy_host: str = host

    # Set the proxy port
    proxy_port: int = int(port)

    # Optionally, set the proxy's anonymity level (HIGH, MEDIUM, LOW)
    proxy_anon: typing.Literal['HIGH', 'MEDIUM', 'LOW'] | None = None

    # Create a ProxyInfo object and add it to the list
    proxy_info: ProxyInfo = ProxyInfo(
        _scheme = proxy_scheme,
        _host = proxy_host,
        _port = proxy_port,
        _anonymity_level = proxy_anon
    )

    converted_proxies.append(proxy_info)

# Print information about each converted proxy
print("Converted proxies:")
for proxy in converted_proxies:
    print(proxy)

# Test the proxies using ProxySea
tested_proxies: list[ProxyInfo] = asyncio.run(PS.test_proxies(_proxies = converted_proxies, _concurrent_tasks = 500))

# Print test results for each proxy
print("\nTested proxies:")
for proxy in tested_proxies:
    print(proxy)
    # Additional info available after testing:
    # - Is the proxy alive
    # - Is the proxy blacklisted (if retries > 3)
    # - Number of connection retries
    # - Proxy anonymity level
