from playwright.sync_api import APIResponse

from src.api.request import Request


class Users:
    LOGIN: str = "/users/login"
    LOGOUT: str = "/users/logout"
    USERS: str = "/users"
    USER_PROFILE: str = "/users/me"

    def __init__(self, request: Request):
        self._request: Request = request

    def login(self, login_data: dict) -> APIResponse:
        return self._request.post(path=self.LOGIN, data=login_data)

    def logout(self) -> APIResponse:
        return self._request.post(path=self.LOGOUT)

    def create(self, user_data: dict) -> APIResponse:
        return self._request.post(path=self.USERS, data=user_data)

    def partial_update(self, user_data: dict) -> APIResponse:
        return self._request.patch(path=self.USER_PROFILE, data=user_data)

    def get(self) -> APIResponse:
        return self._request.get(path=self.USER_PROFILE)

    def delete(self) -> APIResponse:
        return self._request.delete(path=self.USER_PROFILE)
