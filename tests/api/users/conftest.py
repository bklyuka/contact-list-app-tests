import pytest

from src.api.user_api import UserAPI
from src.payloads import CreateUser, LoginCredentials


@pytest.fixture(name="user_api", scope="class")
def get_user_api(auth_client) -> UserAPI:
    return UserAPI(auth_client)


@pytest.fixture(name="user_api_not_auth")
def get_user_api_not_auth(unauth_client) -> UserAPI:
    return UserAPI(unauth_client)


@pytest.fixture(name="credentials")
def get_creds_of_new_user(user_api_not_auth: UserAPI) -> LoginCredentials:
    credentials_ = LoginCredentials()

    user_api_not_auth.create(
        user_data=CreateUser(
            email=credentials_.email,
            password=credentials_.password
        ).__dict__
    )
    return credentials_


@pytest.fixture(name="client")
def get_authenticated_new_client(user_api_not_auth: UserAPI, credentials: LoginCredentials) -> UserAPI:
    user_api_not_auth.authenticate(
        user_email=credentials.email,
        password=credentials.password
    )
    return user_api_not_auth
