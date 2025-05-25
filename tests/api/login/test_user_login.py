from http import HTTPStatus

import pytest
from assertpy import assert_that

from src.api.api_client import APIClient
from src.payloads import LoginCredentials
from src.responses import login_schema
from src.settings import config
from jsonschema.validators import validate


@pytest.fixture(name="payload")
def get_login_payload() -> dict:
    return LoginCredentials().__dict__


class TestUserLogin:

    def test_login_with_valid_data(self, unauth_client: APIClient) -> None:
        response = unauth_client.users.login(login_data={
            "email": config.user_email,
            "password": config.user_password
        })
        response_data = response.json()

        assert response.status == HTTPStatus.OK, response_data
        assert_that(response_data["user"]["email"]).is_equal_to(config.user_email)
        validate(instance=response_data, schema=login_schema)

    def test_login_with_invalid_data(self, unauth_client: APIClient, payload: dict) -> None:
        response = unauth_client.users.login(login_data=payload)

        assert response.status == HTTPStatus.UNAUTHORIZED
        assert_that(response.text()).is_empty()

    @pytest.mark.parametrize("prop", ("email", "password"))
    def test_login_without_required_property(self, unauth_client: APIClient, payload: dict, prop: str) -> None:
        del payload[prop]

        response = unauth_client.users.login(login_data=payload)

        assert response.status == HTTPStatus.UNAUTHORIZED
        assert_that(response.text()).is_empty()
