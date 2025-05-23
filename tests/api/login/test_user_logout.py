from http import HTTPStatus

import pytest
from assertpy import assert_that

from src.api.api_client import APIClient
from src.api.common import CommonAPIErrors
from src.settings import config


@pytest.fixture(name="auth_client")
def get_login_payload(unauth_client: APIClient) -> APIClient:
    unauth_client.authenticate(user_email=config.user_email, password=config.user_password)
    return unauth_client


class TestUserLogout:

    def test_logout_successfully(self, auth_client: APIClient) -> None:
        response = auth_client.logout()

        assert response.status == HTTPStatus.OK
        assert_that(response.text()).is_empty()

    def test_logout_for_not_authenticated_client(self, unauth_client: APIClient) -> None:
        response = unauth_client.logout()
        response_data = response.json()

        assert response.status == HTTPStatus.UNAUTHORIZED, response_data
        assert_that(response_data).is_equal_to(dict(error=CommonAPIErrors.NOT_AUTHENTICATE))
