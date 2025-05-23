from http import HTTPStatus

import pytest
from assertpy import assert_that
from jsonschema.validators import validate

from src.api.api_client import APIClient
from src.helpers import get_random_string
from src.payloads import CreateUser
from src.responses import user_schema


@pytest.fixture(name="payload")
def get_user_payload() -> dict:
    return CreateUser().__dict__


class TestAddUser:

    def test_add_user_with_valid_data(self, auth_client: APIClient, payload: dict) -> None:
        response = auth_client.create_user(user_data=payload)
        response_data = response.json()

        assert response.status == HTTPStatus.CREATED, response_data
        assert_that(payload).is_equal_to(response_data["user"], ignore=["_id", "password", "__v"])
        validate(instance=response_data, schema=user_schema)

    @pytest.mark.parametrize("prop", ("firstName", "lastName", "password"))
    def test_add_user_without_required_property(self, auth_client: APIClient, payload: dict, prop: str) -> None:
        del payload[prop]

        response = auth_client.create_user(user_data=payload)
        response_data = response.json()

        assert response.status == HTTPStatus.BAD_REQUEST, response_data
        assert_that(response_data["errors"][prop]["message"]).is_equal_to(f"Path `{prop}` is required.")

    def test_add_user_without_email(self, auth_client: APIClient, payload: dict) -> None:
        del payload["email"]

        response = auth_client.create_user(user_data=payload)
        response_data = response.json()

        assert response.status == HTTPStatus.BAD_REQUEST, response_data
        assert_that(response_data["message"]).is_equal_to("Email address is already in use")

    def test_add_user_with_already_used_email(self, auth_client: APIClient, payload: dict) -> None:
        for _ in range(2):
            response = auth_client.create_user(user_data=payload)
            response_data = response.json()

        assert response.status == HTTPStatus.BAD_REQUEST, response_data
        assert_that(response_data["message"]).is_equal_to("Email address is already in use")

    @pytest.mark.parametrize(
        "prop, value, error_msg",
        [
            ("firstName", get_random_string(length=21), "Path `{}` (`{}`) is longer than the maximum allowed length (20)."),
            ("lastName", get_random_string(length=21), "Path `{}` (`{}`) is longer than the maximum allowed length (20)."),
            ("password", get_random_string(length=6), "Path `{}` (`{}`) is shorter than the minimum allowed length (7)."),
        ]
    )
    def test_add_user_with_invalid_length_value_for_property(
            self, auth_client: APIClient, payload: dict, prop: str, value: str, error_msg: str
    ) -> None:
        payload[prop] = value

        response = auth_client.create_user(user_data=payload)
        response_data = response.json()

        assert response.status == HTTPStatus.BAD_REQUEST, response_data
        assert_that(response_data["errors"][prop]["message"]).is_equal_to(error_msg.format(prop, value))
