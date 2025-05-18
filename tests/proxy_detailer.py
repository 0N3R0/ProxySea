proxies: list = []


response: str

while True:
    response = input(f"Provide proxies: ")

    if response == "break":
        break

    scheme, host_port = response.split("://")
    scheme = scheme.split(") ")[-1].lower()
    host, port = host_port.split(":")

    proxies.append((scheme, host, port))

print(proxies)

[print(f"{proxy[1]}:{proxy[2]}") for proxy in proxies]