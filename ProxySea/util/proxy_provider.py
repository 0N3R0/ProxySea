# Default imports
from ..imports import typing

# Logger imports
from ..logger import Logger

# Util imports
from .http_client import HttpClient


class ProxyProvider:
    """
    Manages proxy acquisition for specific provider URL.

    This class is responsible for handling a collection of proxy servers from a given provider,
    downloading content from the provider URL.

    Note:
        - The provider URL is expected to be a full HTTP/HTTPS URL, used to fetch a proxy list or content.
        - Requires external classes: `Logger`, `HttpClient`.

    Attributes:
        debug (bool): Enables debug-level logging output.
        url (str): Full provider URL from which proxy data may be fetched.
        domain (str): Extracted domain from the provider URL.
        logger (Logger): Logging helper for tracing internal actions and errors.
        http_client (HttpClient): Lightweight client used to fetch remote page content.

    Methods:
        download_page():
            Downloads the HTML content from the provider URL.
            Returns response object or None if an error occurred.
    
    Examples:
    ```
        >>> import asyncio

        >>> provider = ProxyProvider("https://example.com/proxies", _debug=True)
    ```
    """
    
    def __init__(self, _provider_url: str, _debug: bool = False) -> None:
        """
        Initializes the ProxyProvider instance and sets up internal utilities.

        Args:
            _provider_url (str):
                Full URL of the proxy provider endpoint.
            _debug (bool, optional):
                Enables debug output if set to True. Defaults to False.

        Examples:
        ```
            >>> provider = ProxyProvider("https://example.com/list.txt", _debug=True)
        ```
        """

        self.debug: bool = _debug
        
        # Some basic information
        self.url: str = _provider_url
        self.domain: str = _provider_url.split("://")[1].split("/")[0]

        # Create the Logger instance, for easier logging.
        self.logger: Logger = Logger(
            _logger_name = f"ProxyProvider [{self.domain}]",
            _debug = self.debug
        )

        # Create the HttpClient instance, for easier page downloading.
        self.http_client = HttpClient(_url = self.url)

    async def download_page(self) -> typing.Optional[str | dict]:
        """
        Downloads the page from the provider URL using the internal HTTP client.

        Logs success or failure and returns the response or None on error.

        Returns:
            typing.Optional[str | dict]:
                The page content as a string or dict, or None if download fails.

        Examples:
        ```
            >>> content = await provider.download_page()
            >>> if content:
            >>>     print(content)
        ```
        """
        
        res: typing.Optional[str | dict] = None

        try:
            res = await self.http_client.get()
        except Exception as e:
            self.logger.log(f"Exception during fetching page: {e}")

        if res:
            self.logger.log(f"Fetched page successfully.")
        else:
            self.logger.log(f"Something went wrong while fetching page.")

        return res
