from http import HTTPStatus

import pytest
from assertpy import assert_that
from jsonschema.validators import validate

from src.api.user_api import UserApi
from src.application_data import config
from src.responses import login_schema


class TestAPIUserLogin:

    @pytest.mark.testomatio("@Td89de591")
    @pytest.mark.api
    def test_login_with_valid_data(self, user_api: UserApi) -> None:
        response = user_api.login(login_data={
            "email": config.user_email,
            "password": config.user_password
        })
        response_data = response.json()

        assert response.status == HTTPStatus.OK, response_data
        assert_that(response_data["user"]["email"]).is_equal_to(config.user_email)
        validate(instance=response_data, schema=login_schema)

    @pytest.mark.testomatio("@T2e674c91")
    @pytest.mark.api
    def test_login_with_invalid_data(self, user_api: UserApi, payload: dict) -> None:
        response = user_api.login(login_data=payload)

        assert response.status == HTTPStatus.UNAUTHORIZED
        assert_that(response.text()).is_empty()

    @pytest.mark.testomatio("@Tdf33394c")
    @pytest.mark.api
    @pytest.mark.parametrize("prop", ("email", "password"))
    def test_login_without_required_property(self, user_api: UserApi, payload: dict, prop: str) -> None:
        del payload[prop]

        response = user_api.login(login_data=payload)

        assert response.status == HTTPStatus.UNAUTHORIZED
        assert_that(response.text()).is_empty()
