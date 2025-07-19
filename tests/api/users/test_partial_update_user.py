from http import HTTPStatus
from typing import Any

import pytest
from assertpy import assert_that
from jsonschema.validators import validate

from src.api.user_api import UserAPI
from src.errors import CommonErrors
from src.helpers import get_random_string, get_fake_email
from src.responses import user_profile_schema
from src.application_data import config


class TestAPIPartialUpdateUser:

    @pytest.mark.testomatio("@Td447d494")
    @pytest.mark.api
    @pytest.mark.parametrize(
        "prop, value",
        [
            ("firstName", get_random_string()),
            ("lastName", get_random_string()),
            ("email", get_fake_email()),
            ("password", get_random_string(length=7)),
        ]
    )
    def test_partial_update_user_with_valid_data(self, client: UserAPI, prop: str, value: object) -> None:
        payload = {prop: value}

        response = client.partial_update(user_data=payload)
        response_data = response.json()

        assert response.status == HTTPStatus.OK, response_data
        if prop != "password":
            assert_that(response_data).contains_entry(payload)
        validate(instance=response_data, schema=user_profile_schema)

    @pytest.mark.testomatio("@Tc352a2c7")
    @pytest.mark.api
    def test_partial_update_user_with_already_used_email(self, client: UserAPI) -> None:
        payload = {"email": config.user_email}

        response = client.partial_update(user_data=payload)
        response_data = response.json()

        assert response.status == HTTPStatus.BAD_REQUEST, response_data
        assert_that(response_data["keyValue"]).contains_entry(payload)

    @pytest.mark.testomatio("@T9eef2b93")
    @pytest.mark.api
    @pytest.mark.parametrize(
        "prop, invalid_length_value, limit",
        [
            ("firstName", get_random_string(length=21), 20),
            ("lastName", get_random_string(length=21), 20),
            ("password", get_random_string(length=101), 100),
        ]
    )
    def test_partial_update_user_with_invalid_max_length_value_for_property(
            self,
            client: UserAPI,
            prop: str,
            invalid_length_value: str,
            limit: int
    ) -> None:
        payload = {prop: invalid_length_value}

        response = client.partial_update(user_data=payload)
        response_data = response.json()

        assert response.status == HTTPStatus.BAD_REQUEST, response_data
        assert_that(response_data["errors"][prop]["message"]).is_equal_to(
            CommonErrors.MAX_ALLOWED.format(prop, invalid_length_value, limit)
        )

    @pytest.mark.testomatio("@T3220ce10")
    @pytest.mark.api
    @pytest.mark.parametrize("prop", ("firstName", "lastName", "password"))
    def test_partial_update_user_with_no_data_provided_for_property(
            self,
            client: UserAPI,
            prop: str
    ) -> None:
        payload = {prop: ""}

        response = client.partial_update(user_data=payload)
        response_data = response.json()

        assert response.status == HTTPStatus.BAD_REQUEST, response_data
        assert_that(response_data["errors"][prop]["message"]).is_equal_to(CommonErrors.REQUIRED_PROP.format(prop))

    @pytest.mark.testomatio("@Tca463288")
    @pytest.mark.api
    def test_partial_update_user_with_invalid_min_length_value_for_password(self, client: UserAPI) -> None:
        payload = {"password": get_random_string(length=6)}

        response = client.partial_update(user_data=payload)
        response_data = response.json()

        assert response.status == HTTPStatus.BAD_REQUEST, response_data
        assert_that(response_data["errors"]["password"]["message"]).is_equal_to(
            CommonErrors.MIN_ALLOWED.format(
                property="password",
                value=payload["password"],
                min_limit=7
            )
        )
