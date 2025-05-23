from playwright.sync_api import APIResponse

from src.api.request import Request


class Users:
    LOGIN = "/users/login"

    def __init__(self, request: Request):
        self._request: Request = request

    def login(self, login_data: dict) -> APIResponse:
        return self._request.post(path=self.LOGIN, data=login_data)
