import asyncio
import aiohttp
import socket



proxies = [('34.143.143.61', 7777), ('119.156.195.169', 3128), ('47.88.59.79', 82), ('66.201.7.151', 3128), ('198.74.51.79', 8888), ('52.194.186.70', 1080), ('37.120.172.84', 80), ('46.47.197.210', 3128), ('89.58.53.205', 80), ('188.68.52.244', 80), ('89.58.45.248', 80), ('89.58.8.250', 80), ('65.21.52.41', 8888), ('89.58.28.110', 80), ('119.156.195.170', 3128), ('202.61.199.166', 80), ('13.40.3.184', 3128), ('89.58.55.106', 80), ('81.169.213.169', 8888), ('23.247.136.254', 80), ('89.58.52.160', 80), ('200.250.131.218', 80), ('89.58.57.45', 80), ('54.214.109.103', 10001), ('54.245.27.232', 999), ('18.236.65.56', 3129), ('13.40.152.64', 3128), ('52.11.48.124', 3128), ('35.90.245.227', 31293), ('3.10.207.94', 4222), ('13.40.85.163', 999), ('18.170.63.85', 10001), ('40.76.69.94', 8080), ('89.58.55.193', 80), ('18.175.118.106', 999), ('89.58.55.33', 80)]

TARGET_URL = "https://httpbin.org/ip"  # ← Twój adres docelowy

success_event = asyncio.Event()

print(f"Provided proxies: {proxies}")

async def try_send(proxy_host, proxy_port):
    if success_event.is_set():
        return None

    proxy_url = f"http://{proxy_host}:{proxy_port}"
    connector = aiohttp.TCPConnector(ssl=False)

    async with aiohttp.ClientSession(connector=connector) as session:
        try:
            async with session.get(
                TARGET_URL, proxy=proxy_url, timeout=aiohttp.ClientTimeout(total=5)
            ) as resp:
                if not success_event.is_set() and resp.status == 200:
                    success_event.set()
                    print(f"✅ Sukces przez {proxy_host}:{proxy_port}")

                    return await resp.text()

        except Exception as e:
            # print(f"Proxy {proxy_host}:{proxy_port} nie działa: {e}")
            return None


async def main():
    tasks = [
        asyncio.create_task(
            try_send(h, p)
        ) for h, p in proxies
    ]
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

    for task in pending:
        task.cancel()

    for task in done:
        if task.result():
            print("Wysłano tylko raz.")
            return task.result()

    print("❌ Żadne proxy nie zadziałało.")
    return None

asyncio.run(main())
