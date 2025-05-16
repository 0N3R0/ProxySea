import requests



host_port: str = "219.65.73.81:80"

prot_1: str = "http"
prot_2: str = "https"

proxy = {
    prot_1: f"{prot_1}://{host_port}",
    prot_2: f"{prot_2}://{host_port}",
}

try:
    response = requests.get('http://api.ipify.org', proxies=proxy, timeout=60)

    print(response.content)
    print(response.headers)
except Exception as e:
    print(f"No: {e}")
