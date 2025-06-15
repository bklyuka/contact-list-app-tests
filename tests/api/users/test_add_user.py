from http import HTTPStatus

import pytest
from assertpy import assert_that
from jsonschema.validators import validate

from src.api.api_client import APIClient
from src.errors import CommonErrors, UserErrors
from src.helpers import get_random_string
from src.payloads import CreateUser
from src.responses import create_user_schema


@pytest.fixture(name="payload")
def get_user_payload() -> dict:
    return CreateUser().__dict__


class TestAPIAddUser:

    @pytest.mark.testomatio("@Tdf19d3af")
    @pytest.mark.api
    def test_add_user_with_valid_data(self, auth_client: APIClient, payload: dict) -> None:
        response = auth_client.create_user(user_data=payload)
        response_data = response.json()

        assert response.status == HTTPStatus.CREATED, response_data
        assert_that(payload).is_equal_to(response_data["user"], ignore=["_id", "password", "__v"])
        validate(instance=response_data, schema=create_user_schema)

    @pytest.mark.testomatio("@Taf29d325")
    @pytest.mark.api
    @pytest.mark.parametrize("prop", ("firstName", "lastName", "password"))
    def test_add_user_without_required_property(self, auth_client: APIClient, payload: dict, prop: str) -> None:
        del payload[prop]

        response = auth_client.create_user(user_data=payload)
        response_data = response.json()

        assert response.status == HTTPStatus.BAD_REQUEST, response_data
        assert_that(response_data["errors"][prop]["message"]).is_equal_to(CommonErrors.REQUIRED_PROP.format(prop))

    @pytest.mark.testomatio("@T04505cec")
    @pytest.mark.api
    def test_add_user_without_email(self, auth_client: APIClient, payload: dict) -> None:
        del payload["email"]

        response = auth_client.create_user(user_data=payload)
        response_data = response.json()

        assert response.status == HTTPStatus.BAD_REQUEST, response_data
        assert_that(response_data["message"]).is_equal_to(UserErrors.USED_EMAIL)

    @pytest.mark.testomatio("@T4ed45d7b")
    @pytest.mark.api
    def test_add_user_with_already_used_email(self, auth_client: APIClient, payload: dict) -> None:
        for _ in range(2):
            response = auth_client.create_user(user_data=payload)
            response_data = response.json()

        assert response.status == HTTPStatus.BAD_REQUEST, response_data
        assert_that(response_data["message"]).is_equal_to(UserErrors.USED_EMAIL)

    @pytest.mark.testomatio("@T4f330f6e")
    @pytest.mark.api
    @pytest.mark.parametrize(
        "prop, invalid_length_value, limit",
        [
            ("firstName", get_random_string(length=21), 20),
            ("lastName", get_random_string(length=21), 20),
            ("password", get_random_string(length=101), 100),
        ]
    )
    def test_add_user_with_invalid_max_length_value_for_property(
            self,
            auth_client: APIClient,
            payload: dict,
            prop: str,
            invalid_length_value: str,
            limit: int
    ) -> None:
        payload[prop] = invalid_length_value

        response = auth_client.create_user(user_data=payload)
        response_data = response.json()

        assert response.status == HTTPStatus.BAD_REQUEST, response_data
        assert_that(response_data["errors"][prop]["message"]).is_equal_to(
            CommonErrors.MAX_ALLOWED.format(prop, invalid_length_value, limit)
        )

    @pytest.mark.testomatio("@T01e9eb5f")
    @pytest.mark.api
    def test_add_user_with_invalid_min_length_value_for_password(
            self,
            auth_client: APIClient,
            payload: dict
    ) -> None:
        payload["password"] = get_random_string(length=6)

        response = auth_client.create_user(user_data=payload)
        response_data = response.json()

        assert response.status == HTTPStatus.BAD_REQUEST, response_data
        assert_that(response_data["errors"]["password"]["message"]).is_equal_to(
            CommonErrors.MIN_ALLOWED.format(
                property="password",
                value=payload["password"],
                min_limit=7
            )
        )
