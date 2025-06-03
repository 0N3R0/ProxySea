from ..imports import httpx, typing

class HttpClientSettings:
    """
    Holds default HTTP client configuration settings such as headers.

    This class provides a centralized place for managing default HTTP headers that should be
    used in outbound requests from an HTTP client.

    Attributes:
        HEADERS (dict[str, str]): Default HTTP headers to include in each request.
            - "User-Agent": Identifies the client as a modern browser for compatibility.

    Examples:
    ```
        >>> import httpx

        >>> async with httpx.AsyncClient(headers=HttpClientSettings.HEADERS) as client:
        >>>     response = await client.get("https://example.com")
        >>>     print(response.status_code)
        >>>     print(response.text)
    ```
    """

    HEADERS: dict[str, str] = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
    }

class HttpClient:
    @staticmethod
    async def get(
        _url: str,
        _headers: dict[str, str] = HttpClientSettings.HEADERS,
        _params: dict[str, typing.Any] = None,
        _timeout: float = 3
    ) -> typing.Any:
        async with httpx.AsyncClient(timeout=_timeout) as client:
            response = await client.get(
                url=_url,
                headers=_headers,
                params=_params
            )

            response.raise_for_status()

            content_type = response.headers.get("Content-Type", "")

            if "application/json" in content_type:
                return response.json()

            return response.text

    @staticmethod
    async def post(
        _url: str,
        _headers: dict[str, str] = HttpClientSettings.HEADERS,
        _data: dict[str, typing.Any] = None,
        _json: dict[str, typing.Any] = None,
        _params: dict[str, typing.Any] = None,
        _timeout: float = 3.0
    ) -> typing.Any:
        async with httpx.AsyncClient(timeout=_timeout) as client:
            response = await client.post(
                url = _url,
                headers = _headers,
                data = _data,
                json = _json,
                params = _params
            )

            response.raise_for_status()

            content_type = response.headers.get("Content-Type", "")

            if "application/json" in content_type:
                return response.json()

            return response.text


# class HttpClient:
#     """
#     Asynchronous HTTP client wrapper using httpx for making various HTTP requests.

#     This class allows performing HTTP operations such as GET, POST, PUT, and PATCH
#     with optional parameters, headers, and payloads. It is intended to be a lightweight
#     abstraction over the `httpx.AsyncClient`.

#     Attributes:
#         url (str): The base URL for requests made through this client.

#     Methods:
#         request(_method, _params, _headers, _payload):
#             Core request method to perform asynchronous HTTP requests of various types.

#         get(_params, _headers):
#             Shortcut for performing a GET request.

#         post(_params, _headers, _payload):
#             Shortcut for performing a POST request.

#         put(_params, _headers, _payload):
#             Shortcut for performing a PUT request.

#         patch(_params, _headers, _payload):
#             Shortcut for performing a PATCH request.

#     Examples:
#     ```
#         >>> client = HttpClient("https://httpbin.org/")
#         >>> response = await client.get()
#         >>> print(response)
#     ```
#     """

#     def __init__(self, _url: str = "https://example.com/") -> None:
#         """
#         Initializes the HttpClient with a base URL.

#         Args:
#             _url (str): The base URL for HTTP requests. Defaults to 'https://example.com/'.

#         Examples:
#         ```
#             >>> client = HttpClient("https://api.example.com/")
#             >>> print(client.url)
#             >>> https://api.example.com/ # Result of the print
#         ```
#         """

#         self.url = _url

#     async def request(
#             self,
#             _method: typing.Literal["GET", "POST", "PATCH", "PUT"],
#             _params: str = "",
#             _headers: dict[str, str] = HttpClientSettings.HEADERS,
#             _payload: dict[str, str] = {}
#     ) -> typing.Any:
#         """
#         Sends an asynchronous HTTP request based on the given method.

#         Args:
#             _method (Literal["GET", "POST", "PATCH", "PUT"]): HTTP method to use.
#             _params (str): URL parameters to include in the request.
#             _headers (dict): Headers to include in the request.
#             _payload (dict): Data to send in the body of the request (for POST/PUT/PATCH).

#         Returns:
#              dict | str: Parsed JSON response if available, otherwise raw text response.

#         Raises:
#             httpx.HTTPStatusError: If the response status indicates an error.
#             ValueError: If an unknown method is provided.

#         Examples:
#         ```
#             >>> import asyncio

#             >>> client = HttpClient("https://httpbin.org")

#             >>> response = asyncio.run(client.request("GET", _params="get?show_env=1"))
#             >>> print("url" in response)
#             >>> True # Result of the print

#             >>> response = asyncio.run(client.request("POST", _params="post", _payload={"key": "value"}))
#             >>> print(response["json"])
#             >>> {'key': 'value'} # Result of the print
#         ```
#         """

#         async with httpx.AsyncClient() as client:
#             # Some adjusting
#             # url = f"{'https://' if not self.URL.startswith('http') else ''}{self.URL}{'/' if not self.DOMAIN.endswith('/') else ''}{_path}"
#             url = self.url

#             # methods: dict[str, tuple] = {
#             #     "GET": (client.get, url, _params, _headers),
#             #     "POST": (client.post, url, _params, _headers, _payload),
#             #     "PUT": (client.put, url, _params, _headers, _payload),
#             #     "PATCH": (client.patch, url, _params, _headers, _payload)
#             # }

#             # if _method not in methods.keys():
#             #     raise ValueError(f"You have passed unknown request method: {_method}")

#             # chosen_fetch_method = methods[_method]
#             # func = chosen_fetch_method[0]
#             # await func()

#             if _method.upper() == "GET":
#                 response = await client.get(url = url, params = _params, headers = _headers)
            
#             elif _method.upper() == "POST":
#                 response = await client.post(url = url, params = _params, headers = _headers, json = _payload)

#             elif _method.upper() == "PUT":
#                 response = await client.put(url = url, params = _params, headers = _headers, json = _payload)

#             elif _method.upper() == "PATCH":
#                 response = await client.patch(url = url, params = _params, headers = _headers, json = _payload)
            
#             else:
#                 raise ValueError(f"You have passed unknown request method: {_method}")

#             response.raise_for_status() # Check for response status.

#             if "application/json" in response.headers.get("Content-Type", ""):
#                 return response.json()

#             else:
#                 return response.text

#     async def get(self, _params: str | None = None, _headers: dict[str, str] | None = HttpClientSettings.HEADERS) -> typing.Optional[str | dict]:
#         """
#         Performs an asynchronous GET request.

#         Args:
#             _params (str): Query parameters for the request.
#             _headers (dict): HTTP headers to include.

#         Returns:
#               dict | str | None: JSON or text response, or None on failure.

#         Examples:
#         ```
#             >>> import asyncio

#             >>> client = HttpClient("https://httpbin.org")

#             >>> result = asyncio.run(client.get("get?foo=bar"))
#             >>> print(result["args"]["foo"])
#             >>> bar # Result of the print
#         ```
#         """

#         return await self.request(_method = "GET", _params = _params, _headers = _headers)

#     async def post(self, _params: str | None = None, _headers: dict[str, str] | None = HttpClientSettings.HEADERS, _payload: dict[str, str] | None = None) -> typing.Optional[str | dict]:
#         """
#         Performs an asynchronous POST request.

#         Args:
#             _params (str): Query parameters for the request.
#             _headers (dict): HTTP headers to include.
#             _payload (dict): JSON body to send.

#         Returns:
#               dict | str | None: JSON or text response, or None on failure.

#         Examples:
#         ```
#             >>> import asyncio

#             >>> client = HttpClient("https://httpbin.org")

#             >>> result = asyncio.run(client.post("post", _payload={"name": "example"}))
#             >>> print(result["json"]["name"])
#             >>> example # Result of the print
#         ```
#         """

#         return await self.request(_method = "POST", _params = _params, _headers = _headers, _payload = _payload)

#     async def put(self, _params: str | None = None, _headers: dict[str, str] | None = HttpClientSettings.HEADERS, _payload: dict[str, str] = None) -> typing.Optional[str | dict]:
#         """
#         Performs an asynchronous PUT request.

#         Args:
#             _params (str): Query parameters for the request.
#             _headers (dict): HTTP headers to include.
#             _payload (dict): JSON body to send.

#         Returns:
#               dict | str | None: JSON or text response, or None on failure.

#         Examples:
#         ```
#             >>> import asyncio

#             >>> client = HttpClient("https://httpbin.org")

#             >>> result = asyncio.run(client.put("put", _payload={"update": "value"}))
#             >>> print(result["json"]["update"])
#             >>> value # Result of the print
#         ```
#         """

#         return await self.request(_method = "PUT", _params = _params, _headers = _headers, _payload = _payload)

#     async def patch(self, _params: str | None = None, _headers: dict[str, str] | None = HttpClientSettings.HEADERS, _payload: dict[str, str] | None = None) -> typing.Optional[str | dict]:
#         """
#         Performs an asynchronous PATCH request.

#         Args:
#             _params (str): Query parameters for the request.
#             _headers (dict): HTTP headers to include.
#             _payload (dict): JSON body to send.

#         Returns:
#               dict | str | None: JSON or text response, or None on failure.

#         Examples:
#         ```
#             >>> import asyncio

#             >>> client = HttpClient("https://httpbin.org")

#             >>> result = asyncio.run(client.patch("patch", _payload={"patch": "data"}))
#             >>> print(result["json"]["patch"])
#             >>> data # Result of the print
#         ```
#         """

#         return await self.request(_method = "PATCH", _params = _params, _headers = _headers, _payload = _payload)
