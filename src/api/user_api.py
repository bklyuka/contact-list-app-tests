from playwright.sync_api import APIResponse

from src.api.api_http_client import ApiHttpClient


class UserAPI:
    LOGIN: str = "/users/login"
    LOGOUT: str = "/users/logout"
    USERS: str = "/users"
    USER_PROFILE: str = "/users/me"

    def __init__(self, request):
        self._request = request

    def login(self, login_data: dict) -> APIResponse:
        return self._request.post(path=self.LOGIN, data=login_data)

    def logout(self) -> APIResponse:
        return self._request.post(path=self.LOGOUT)

    def create_user(self, user_data: dict) -> APIResponse:
        return self._request.post(path=self.USERS, data=user_data)

    def partial_update_user(self, user_data: dict) -> APIResponse:
        return self._request.patch(path=self.USER_PROFILE, data=user_data)

    def get_user_profile(self) -> APIResponse:
        return self._request.get(path=self.USER_PROFILE)

    def delete_user_me(self) -> APIResponse:
        return self._request.delete(path=self.USER_PROFILE)
