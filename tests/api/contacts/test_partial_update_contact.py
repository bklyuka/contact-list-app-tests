from http import HTTPStatus
from typing import Any

import pytest
from assertpy import assert_that
from jsonschema.validators import validate

from src.api.api_client import APIClient
from src.errors import CommonErrors
from src.faker_provider import faker
from src.helpers import get_random_string, get_random_int, get_fake_email
from src.responses import contact_schema


class TestAPIPartialUpdateContact:

    @pytest.mark.testomatio("@Tf497ca9e")
    @pytest.mark.parametrize(
        "prop, value",
        [
            ("firstName", get_random_string()),
            ("lastName", get_random_string()),
            ("email", get_fake_email()),
            ("birthdate", faker.date_of_birth().strftime("%Y-%m-%d")),
            ("phone", str(get_random_int())),
            ("street1", faker.street_address()),
            ("street2", faker.street_address()),
            ("city", faker.city()),
            ("stateProvince", faker.state_abbr()),
            ("postalCode", faker.postcode()),
            ("country", faker.country())
        ]
    )
    def test_partial_update_contact_with_valid_data(
            self,
            auth_client: APIClient,
            contact_id: str,
            prop: str,
            value: Any
    ) -> None:
        payload = {prop: value}

        response = auth_client.partial_update_contact(contact_id=contact_id, contact_data=payload)
        response_data = response.json()

        assert response.status == HTTPStatus.OK, response_data
        assert_that(response_data).contains_entry(payload)
        validate(instance=response_data, schema=contact_schema)

    @pytest.mark.testomatio("@T9079d178")
    @pytest.mark.parametrize(
        "prop, invalid_length_value, limit",
        [
            ("firstName", get_random_string(length=21), 20),
            ("lastName", get_random_string(length=21), 20),
            ("phone", get_random_string(length=16), 15),
            ("street1", get_random_string(length=41), 40),
            ("street2", get_random_string(length=41), 40),
            ("city", get_random_string(length=41), 40),
            ("stateProvince", get_random_string(length=21), 20),
            ("postalCode", get_random_string(length=11), 10),
            ("country", get_random_string(length=41), 40),
        ]
    )
    def test_partial_update_contact_with_invalid_max_length_value_for_property(
            self,
            auth_client: APIClient,
            contact_id: str,
            prop: str,
            invalid_length_value: Any,
            limit: int
    ) -> None:
        payload = {prop: invalid_length_value}

        response = auth_client.partial_update_contact(contact_id=contact_id, contact_data=payload)
        response_data = response.json()

        assert response.status == HTTPStatus.BAD_REQUEST, response_data
        assert_that(response_data["errors"][prop]["message"]).is_equal_to(
            CommonErrors.MAX_ALLOWED.format(prop, invalid_length_value, limit)
        )

    @pytest.mark.testomatio("@Tb348abca")
    @pytest.mark.parametrize(
        "prop, error_msg",
        [
            ("email", CommonErrors.INVALID_PROP.format("Email")),
            ("birthdate", CommonErrors.INVALID_PROP.format("Birthdate")),
            ("phone", CommonErrors.INVALID_PROP.format("Phone number")),
            ("postalCode", CommonErrors.INVALID_PROP.format("Postal code")),
        ]
    )
    def test_partial_update_contact_with_invalid_value_for_property(
            self,
            auth_client: APIClient,
            contact_id: str,
            prop: str,
            error_msg: str
    ) -> None:
        payload = {prop: get_random_string()}

        response = auth_client.partial_update_contact(contact_id=contact_id, contact_data=payload)
        response_data = response.json()

        assert response.status == HTTPStatus.BAD_REQUEST, response_data
        assert_that(response_data["errors"][prop]["message"]).is_equal_to(error_msg)

    @pytest.mark.testomatio("@T7d66a4bb")
    def test_partial_update_contact_without_token_provided(self, unauth_client: APIClient, contact_id: str) -> None:
        response = unauth_client.partial_update_contact(contact_id=contact_id, contact_data={})
        response_data = response.json()

        assert response.status == HTTPStatus.UNAUTHORIZED, response_data
        assert_that(response_data).is_equal_to(dict(error=CommonErrors.NOT_AUTHENTICATE))
