proxies: list = []


response: str

while True:
    response = input(f"Provide proxies: ")

    if response == "break":
        break

    proxy_details: list[str] = response.split("://")[1].split(":")

    proxies.append((proxy_details[0], int(proxy_details[1])))

print(proxies)