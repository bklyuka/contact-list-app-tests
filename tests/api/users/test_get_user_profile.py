from http import HTTPStatus

import pytest
from assertpy import assert_that
from jsonschema.validators import validate
from src.api.api_client import APIClient

from src.api.user_api import UserAPI
from src.application_data import config
from src.errors import CommonErrors
from src.responses import user_profile_schema


@pytest.fixture(name="user_api", scope="class")
def get_user_api(auth_client):
    return UserAPI(auth_client)


@pytest.fixture(name="user_api", scope="class")
def get_user_api(unauth_client):
    return UserAPI(auth_client)



class TestAPIGetUserProfile:

    @pytest.mark.testomatio("@Ta8001306")
    @pytest.mark.api
    def test_get_user_profile_success(self, user_api: UserAPI) -> None:
        response = user_api.get_profile()
        response_data = response.json()

        assert response.status == HTTPStatus.OK, response_data
        assert_that(response_data).contains_entry({"email": config.user_email})
        validate(instance=response_data, schema=user_profile_schema)

    @pytest.mark.testomatio("@T5d325c5e")
    @pytest.mark.api
    def test_get_user_profile_without_token_provided(self, unauth_client: APIClient) -> None:
        response = unauth_client.get_user_profile()
        response_data = response.json()

        assert response.status == HTTPStatus.UNAUTHORIZED, response_data
        assert_that(response_data).is_equal_to(dict(error=CommonErrors.NOT_AUTHENTICATE))
