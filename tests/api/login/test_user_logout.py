from http import HTTPStatus

import pytest
from assertpy import assert_that

from src.api.api_client import APIClient
from src.api.common import CommonAPIErrors
from src.payloads import CreateUser, LoginCredentials


@pytest.fixture(name="credentials")
def get_creds_of_new_user(unauth_client: APIClient) -> LoginCredentials:
    credentials_ = LoginCredentials()

    unauth_client.create_user(
        user_data=CreateUser(
            email=credentials_.email,
            password=credentials_.password
        ).__dict__
    )
    return credentials_


@pytest.fixture(name="client")
def get_authenticated_new_client(unauth_client: APIClient, credentials: LoginCredentials) -> APIClient:
    unauth_client.authenticate(
        user_email=credentials.email,
        password=credentials.password
    )
    return unauth_client


class TestUserLogout:

    def test_logout_successfully(self, client: APIClient) -> None:
        response = client.logout()

        assert response.status == HTTPStatus.OK
        assert_that(response.text()).is_empty()

    def test_logout_for_not_authenticated_client(self, unauth_client: APIClient) -> None:
        response = unauth_client.logout()
        response_data = response.json()

        assert response.status == HTTPStatus.UNAUTHORIZED, response_data
        assert_that(response_data).is_equal_to(dict(error=CommonAPIErrors.NOT_AUTHENTICATE))
