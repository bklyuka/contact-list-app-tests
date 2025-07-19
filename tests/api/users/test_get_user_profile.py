from http import HTTPStatus

import pytest
from assertpy import assert_that
from jsonschema.validators import validate

from src.api.user_api import UserApi
from src.application_data import config
from src.errors import CommonErrors
from src.responses import user_profile_schema


class TestAPIGetUserProfile:

    @pytest.mark.testomatio("@Ta8001306")
    @pytest.mark.api
    def test_get_user_profile_success(self, user_api: UserApi) -> None:
        response = user_api.get_profile()
        response_data = response.json()

        assert response.status == HTTPStatus.OK, response_data
        assert_that(response_data).contains_entry({"email": config.user_email})
        validate(instance=response_data, schema=user_profile_schema)

    @pytest.mark.testomatio("@T5d325c5e")
    @pytest.mark.api
    def test_get_user_profile_without_token_provided(self, user_api_not_auth: UserApi) -> None:
        response = user_api_not_auth.get_profile()
        response_data = response.json()

        assert response.status == HTTPStatus.UNAUTHORIZED, response_data
        assert_that(response_data).is_equal_to(dict(error=CommonErrors.NOT_AUTHENTICATE))
