from playwright.sync_api import APIResponse

from src.api.api_http_client import ApiHttpClient


class UserApi:
    LOGIN: str = "/users/login"
    LOGOUT: str = "/users/logout"
    USERS: str = "/users"
    USER_PROFILE: str = "/users/me"

    def __init__(self, client: ApiHttpClient):
        self._client = client

    def login(self, login_data: dict) -> APIResponse:
        return self._client.post(path=self.LOGIN, data=login_data)

    def logout(self) -> APIResponse:
        return self._client.post(path=self.LOGOUT)

    def create(self, user_data: dict) -> APIResponse:
        return self._client.post(path=self.USERS, data=user_data)

    def partial_update(self, user_data: dict) -> APIResponse:
        return self._client.patch(path=self.USER_PROFILE, data=user_data)

    def get_profile(self) -> APIResponse:
        return self._client.get(path=self.USER_PROFILE)

    def delete_user_me(self) -> APIResponse:
        return self._client.delete(path=self.USER_PROFILE)

    def authenticate(self, user_email: str, password: str) -> None:
        response = self.login(login_data={"email": user_email, "password": password})
        self._client.set_token(response.json()["token"])
