from typing import Optional

from playwright.sync_api import APIRequestContext, APIResponse


class Request:
    def __init__(self, request: APIRequestContext, base_url: str):
        self._request: APIRequestContext = request
        self._base_url: str = base_url
        self._token: Optional[str] = None
        self._headers: dict = {"Content-Type": "application/json"}

    def __build_headers(self, extra_headers) -> dict:
        return {**self._headers, **extra_headers} if extra_headers else self._headers

    def __build_url(self, path: str) -> str:
        return f"{self._base_url}{path}"

    def set_token(self, token: str) -> None:
        self._token = token
        self._headers["Authorization"] = f"Bearer {token}"

    def get(self, path: str, params: Optional[dict] = None, extra_headers: Optional[dict] = None) -> APIResponse:
        return self._request.get(
            url=self.__build_url(path),
            headers=self.__build_headers(extra_headers),
            params=params
        )

    def post(self, path: str, data: Optional[dict] = None, extra_headers: Optional[dict] = None) -> APIResponse:
        return self._request.post(
            url=self.__build_url(path),
            headers=self.__build_headers(extra_headers),
            data=data
        )

    def put(self, path: str, data: Optional[dict] = None, extra_headers: Optional[dict] = None) -> APIResponse:
        return self._request.put(
            url=self.__build_url(path),
            headers=self.__build_headers(extra_headers),
            data=data
        )

    def patch(self, path: str, data: Optional[dict] = None, extra_headers: Optional[dict] = None) -> APIResponse:
        return self._request.patch(
            url=self.__build_url(path),
            headers=self.__build_headers(extra_headers),
            data=data
        )

    def delete(self, path: str, extra_headers: Optional[dict] = None) -> APIResponse:
        headers = self.__build_headers(extra_headers)
        return self._request.delete(
            url=self.__build_url(path),
            headers=headers
        )
