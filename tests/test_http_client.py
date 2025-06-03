# import pytest, httpx, json
# from ProxySea.util import HttpClient


# class TestHttpClient:
#     @pytest.mark.asyncio
#     async def test_get_with_json_response(self, monkeypatch):
#         async def mock_get(*args, **kwargs):
#             return httpx.Response(200, json={"message": "hello"})

#         monkeypatch.setattr(httpx.AsyncClient, "get", mock_get)

#         result = await HttpClient.get(_url="https://example.com")
#         assert result == {"message": "hello"}

#     @pytest.mark.asyncio
#     async def test_post_with_json_payload(self, monkeypatch):
#         async def mock_post(*args, **kwargs):
#             return httpx.Response(200, json={"received": kwargs.get("json")})

#         monkeypatch.setattr(httpx.AsyncClient, "post", mock_post)

#         result = await HttpClient.post(
#             _url="https://example.com",
#             _json={"key": "val"}
#         )
#         assert result == {"received": {"key": "val"}}

#     @pytest.mark.asyncio
#     async def test_get_returns_text_when_not_json(self, monkeypatch):
#         async def mock_get(*args, **kwargs):
#             return httpx.Response(
#                 200,
#                 content=b"<html>Hello</html>",
#                 headers={"Content-Type": "text/html"}
#             )

#         monkeypatch.setattr(httpx.AsyncClient, "get", mock_get)

#         result = await HttpClient.get(_url="https://example.com")
#         assert result == "<html>Hello</html>"
