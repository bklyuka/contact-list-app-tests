from http import HTTPStatus

from assertpy import assert_that
from jsonschema.validators import validate

from src.api.api_client import APIClient
from src.errors import CommonErrors
from src.responses import user_profile_schema
from src.application_data import config


class TestGetUserProfile:

    def test_get_user_profile_success(self, auth_client: APIClient) -> None:
        response = auth_client.get_user_profile()
        response_data = response.json()

        assert response.status == HTTPStatus.OK, response_data
        assert_that(response_data).contains_entry({"email": config.user_email})
        validate(instance=response_data, schema=user_profile_schema)

    def test_get_user_profile_without_token_provided(self, unauth_client: APIClient) -> None:
        response = unauth_client.get_user_profile()
        response_data = response.json()

        assert response.status == HTTPStatus.UNAUTHORIZED, response_data
        assert_that(response_data).is_equal_to(dict(error=CommonErrors.NOT_AUTHENTICATE))
