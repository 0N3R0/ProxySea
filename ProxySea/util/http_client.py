from ..imports import httpx, typing

class HttpClientSettings:
    HEADERS: dict[str, str] = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
    }

class HttpClient:
    def __init__(self, _url: str = "https://example.com/") -> None:
        self.url = _url

    async def request(
            self,
            _method: typing.Literal["GET", "POST", "PATCH", "PUT"],
            _params: str = "",
            _headers: dict[str, str] = HttpClientSettings.HEADERS,
            _payload: dict[str, str] = {}
    ) -> typing.Any:
        async with httpx.AsyncClient() as client:
            # Some adjusting
            # url = f"{'https://' if not self.URL.startswith('http') else ''}{self.URL}{'/' if not self.DOMAIN.endswith('/') else ''}{_path}"
            url = self.url

            # methods: dict[str, tuple] = {
            #     "GET": (client.get, url, _params, _headers),
            #     "POST": (client.post, url, _params, _headers, _payload),
            #     "PUT": (client.put, url, _params, _headers, _payload),
            #     "PATCH": (client.patch, url, _params, _headers, _payload)
            # }

            # if _method not in methods.keys():
            #     raise ValueError(f"You have passed unknown request method: {_method}")

            # chosen_fetch_method = methods[_method]
            # func = chosen_fetch_method[0]
            # await func()

            if _method.upper() == "GET":
                response = await client.get(url = url, params = _params, headers = _headers)
            
            elif _method.upper() == "POST":
                response = await client.post(url = url, params = _params, headers = _headers, json = _payload)

            elif _method.upper() == "PUT":
                response = await client.put(url = url, params = _params, headers = _headers, json = _payload)

            elif _method.upper() == "PATCH":
                response = await client.patch(url = url, params = _params, headers = _headers, json = _payload)
            
            else:
                raise ValueError(f"You have passed unknown request method: {_method}")

            response.raise_for_status() # Check for response status.

            if "application/json" in response.headers.get("Content-Type", ""):
                return response.json()

            else:
                return response.text
        
    async def get(self, _params: str | None = None, _headers: dict[str, str] | None = HttpClientSettings.HEADERS):
        """Performs an asynchronous GET request."""
        return await self.request(_method = "GET", _params = _params, _headers = _headers)

    async def post(self, _params: str | None = None, _headers: dict[str, str] | None = HttpClientSettings.HEADERS, _payload: dict[str, str] | None = None):
        """Performs an asynchronous POST request."""
        return await self.request(_method = "POST", _params = _params, _headers = _headers, _payload = _payload)

    async def put(self, _params: str | None = None, _headers: dict[str, str] | None = HttpClientSettings.HEADERS, _payload: dict[str, str] = None):
        """Performs an asynchronous PUT request."""
        return await self.request(_method = "PUT", _params = _params, _headers = _headers, _payload = _payload)

    async def patch(self, _params: str | None = None, _headers: dict[str, str] | None = HttpClientSettings.HEADERS, _payload: dict[str, str] | None = None):
        """Performs an asynchronous PATCH request."""
        return await self.request(_method = "PATCH", _params = _params, _headers = _headers, _payload = _payload)
