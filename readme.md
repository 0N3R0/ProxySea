# 🌊 ProxySea

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/) [![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**ProxySea** is an asynchronous Python framework for fetching, testing, and managing public HTTP/HTTPS/SOCKS4/SOCKS5 proxies. It integrates seamlessly with libraries like `requests`, `httpx`, and more, allows testing of custom proxy lists, and is built with modularity and future extensibility in mind (e.g., adding an API layer).

---

## 📜 Table of Contents

1. [Disclaimer](#%EF%B8%8F-disclaimer)
2. [Features](#-features)
3. [Future Roadmap](#-future-roadmap)
4. [Requirements](#-requirements)
5. [Installation](#-installation)
6. [Quick Start](#-quickstart)
7. [Usage Example](#-usage-example)
8. [Other Example Scripts](#-other-example-scripts)
9. [Project Structure](#-project-structure)
10. [Contributing](#-contributing)
11. [License](#-license)
12. [Author](#%EF%B8%8F-author)

---

## ⚠️ Disclaimer

> **Intended for educational and research purposes only.**
> **No warranty** — The creator of ProxySea does **not take any responsibility** for how this software is used. You must ensure that your usage complies with all applicable laws and regulations in your jurisdiction.
> Whether you are scraping proxy data from public sources, testing network behavior, or sending requests via third-party proxies — **you use this software at your own risk**. Any misuse, abuse, or illegal activity carried out using ProxySea is solely the responsibility of the user.

---


## ✨ Features

| ✔️ | Feature                                                                                              |
|----|------------------------------------------------------------------------------------------------------|
| ✅ | **Public Proxy Scraping**: Fetch proxies from multiple online providers with minimal setup.          |
| ✅ | **Asynchronous Operations**: Fully async fetching and testing for maximum performance.               |
| ✅ | **Protocol Detection**: Automatically detect each proxy’s protocol (HTTP, HTTPS, SOCKS4, SOCKS5).    |
| ✅ | **Custom Proxy Testing**: Quickly test your own proxy list, with or without explicit schemes.        |
| ✅ | **Built-in Logging**: Detailed debug logs help you trace and troubleshoot proxy operations.          |
| ✅ | **Unit Tests Included**: Partial coverage of unit tests to ensure reliability (see `tests/`).         |

---

## 🛠 Future-Roadmap

- **Geolocation Metadata**: Augment each `ProxyInfo` with geolocation details (country, region, city) based on IP lookup.
- **Enhanced Health Checks**: Improve proxy validation by sending test requests to third-party services to verify IP and latency.
- **More proxy providers**: Add more proxy providers for fetching more proxies.
- **API Server**: Create and expose a REST API for real-time proxy access and management.

---

## 🚧 Requirements

- **Python**: 3.10 or higher
- **Libraries** (installed via `requirements.txt`):
  - `httpx`
  - `requests`
  - `beautifulsoup4`
  - `lxml`
  - `py-mini-racer`
  - `pytest` (for tests)
  - `pytest-asyncio` (for tests)
  - `poetry` (for pyproject.toml)
  - `asyncio` (standard library)

> All dependencies are listed in [requirements.txt](requirements.txt).

---

## 🧩 Installation

Clone the repository and install dependencies:

> **Requires Python 3.10 or higher**

```bash
git clone https://github.com/0N3R0/ProxySea.git
cd ProxySea
pip install -r requirements.txt
```

---

## ⚡ Quickstart

Want to get up and running in under a minute? Here’s the fastest way to start using ProxySea.

### 1. Clone the Repository

```bash
git clone https://github.com/0N3R0/ProxySea.git  
cd ProxySea
```

### 2. Install Dependencies  
> **Requires Python 3.10 or higher**

```bash
pip install -r requirements.txt
```

### 3. Run a Built-in Example  
Test your setup by running an included example:

```bash
python examples/fetch_and_test_proxies_from_public_providers.py
```

You’ll see:
- Proxies being fetched asynchronously from public providers.
- Each proxy being tested for availability.
- A summary of working proxies printed to the console.


### 4. (Optional) Try Custom Proxy List  
Want to test your own proxies? Use:

```bash
python examples/test_custom_proxies_with_schemes.py
```

Modify the `proxies` list in that script to include your own:

```python
proxies: list[str] = ["http://your-proxy:8080", "socks5://other-proxy:1080"]
```

✅ Done! You now have a working environment ready for testing proxies.

---

## 🚀 Usage Example

Below is one of the example scripts demonstrating how to convert, test, and display custom proxies with schemes.

> **File:** `examples/test_custom_proxies_with_schemes.py`

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

### 📂 Other Example Scripts

- **Fetch and Test Proxies from Public Providers**
  - **File:** `examples/fetch_and_test_proxies_from_public_providers.py`
  - **Description:** Asynchronously fetches proxies from all implemented public providers and immediately tests them for availability.

- **Fetch Proxies from Public Providers Only**
  - **File:** `examples/fetch_proxies_from_public_providers.py`
  - **Description:** Demonstrates fetching proxies without performing any testing, returning raw `ProxyInfo` objects.

- **Send Requests via Tested Proxies Using `httpx`**
  - **File:** `examples/send_requests_via_tested_proxies_using_httpx_lib.py`
  - **Description:** Shows how to filter active proxies by scheme and use them to send HTTP requests via the `httpx` library.

- **Send Requests via Tested Proxies Using `requests`**
  - **File:** `examples/send_requests_via_tested_proxies_using_requests_lib.py`
  - **Description:** Similar to the `httpx` example but uses the synchronous `requests` library for sending requests through tested proxies.

- **Test Custom Proxies With Schemes**
  - **File:** `examples/test_custom_proxies_with_schemes.py`
  - **Description:** Provides a template for converting user-defined "scheme://host:port" proxy strings into `ProxyInfo` objects, testing them, and displaying results.

- **Test Custom Proxies Without Schemes**
  - **File:** `examples/test_custom_proxies_without_schemes.py`
  - **Description:** Provides a template for testing a list of proxies given only as `host:port` (no explicit "scheme://" prefix). ProxySea will attempt to detect the correct protocol automatically.

---

## 📂 Project Structure
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

---

## 🤝 Contributing

Contributions are very welcome! To contribute:

1. **Fork** the repository.
2. **Create a new branch:**
   git checkout -b feature/your-feature-name
4. Make your changes and **add unit tests** if applicable.
5. **Commit** your changes:
   git commit -m "Add new feature"
6. **Push** your branch:
   git push origin feature/your-feature-name
7. **Open a Pull Request**, describing your changes in detail.

> Please adhere to consistent code style, include documentation for new functionality, and ensure all existing tests pass.

---

## 📄 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## ✍️ Author

© 2025 0N3R0
