import pytest

from src.api.user_api import UserApi
from src.payloads import LoginCredentials


@pytest.fixture(name="payload")
def get_login_payload() -> dict:
    return LoginCredentials().__dict__


@pytest.fixture(name="user_api")
def get_user_api(unauth_client):
    return UserApi(unauth_client)
