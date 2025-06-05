# 🌊 ProxySea

**ProxySea** is an asynchronous Python framework for fetching, testing, and managing public HTTP/HTTPS/SOCKS4/SOCKS5 proxies. It supports integration with libraries like `requests`, `httpx`, and more, allows testing of custom proxy lists, and is designed with modularity and future extensibility in mind (for example, adding an API layer).


## Disclaimer

This project is intended **strictly for educational and research purposes**.

The creator of ProxySea does **not take any responsibility** for how this software is used. You are fully responsible for ensuring that your usage of this tool complies with all applicable laws and regulations in your country.

Whether you're scraping proxy data from public sources, testing network behavior, or sending requests via third-party proxies — **you use this software at your own risk**. Any misuse, abuse, or illegal activity carried out using ProxySea is solely the responsibility of the user.

Please respect target servers and third-party services. ProxySea was created to provide technical insight and support ethical use only.


## Features

- Fetches public proxies from multiple online providers.
- Fully asynchronous fetching and testing of proxies.
- Automatically detects each proxy’s protocol (HTTP, HTTPS, SOCKS4, SOCKS5).
- Enables very fast testing of your own proxy list.
- Built-in logging system with optional debug mode.
- Includes unit tests (partial coverage).



## Installation
Clone the repository and instsall dependencies:

> **Requires Python 3.10+**

```bash
    git clone https://github.com/0N3R0/ProxySea.git
    cd ProxySea
    pip install -r requirements.txt
```


## One of the examples from `./examples` directory.

*[test_custom_proxies_with_schemes.py](./examples/test_custom_proxies_with_schemes.py)*
```python
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
```


## Project Structure
```
ProxySea/               # Root of the ProxySea project
├── ProxySea/           # Main package folder
│   ├── api/            # API implementation (future)
│   ├── imports/        # Dependency imports
│   ├── logger/         # Logging utilities
│   ├── providers/      # Public proxy providers
│   └── util/           # Utility classes and functions
├── examples/           # Example usage scripts
└── tests/              # Unit tests and pytest
```
