from http import HTTPStatus
from random import choice
from typing import Any

import pytest
from assertpy import assert_that
from jsonschema.validators import validate

from src.api.api_client import APIClient
from src.api.common import CommonAPIErrors
from src.faker_provider import faker
from src.helpers import get_random_string, get_random_int, get_fake_email
from src.payloads import CreateUpdateContact
from src.responses import contact_schema


@pytest.fixture(scope="class", name="contact_id")
def get_contact_id(auth_client: APIClient) -> str:
    data = auth_client.get_contacts()
    contacts = data.json()

    if not contacts:
        contact = auth_client.create_contact(contact_data=CreateUpdateContact().__dict__)
        return contact.json()["_id"]
    return choice(contacts)["_id"]


class TestPartialUpdateContact:

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

    @pytest.mark.parametrize(
        "prop, value, error_msg",
        [
            ("firstName", get_random_string(length=21), "Path `{}` (`{}`) is longer than the maximum allowed length (20)."),
            ("lastName", get_random_string(length=21), "Path `{}` (`{}`) is longer than the maximum allowed length (20)."),
            ("phone", get_random_string(length=16), "Path `{}` (`{}`) is longer than the maximum allowed length (15)."),
            ("street1", get_random_string(length=41), "Path `{}` (`{}`) is longer than the maximum allowed length (40)."),
            ("street2", get_random_string(length=41), "Path `{}` (`{}`) is longer than the maximum allowed length (40)."),
            ("city", get_random_string(length=41), "Path `{}` (`{}`) is longer than the maximum allowed length (40)."),
            ("stateProvince", get_random_string(length=21), "Path `{}` (`{}`) is longer than the maximum allowed length (20)."),
            ("postalCode", get_random_string(length=11), "Path `{}` (`{}`) is longer than the maximum allowed length (10)."),
            ("country", get_random_string(length=41), "Path `{}` (`{}`) is longer than the maximum allowed length (40)."),
        ]
    )
    def test_partial_update_contact_with_invalid_length_value_for_property(
            self,
            auth_client: APIClient,
            contact_id: str,
            prop: str,
            value: Any,
            error_msg: str
    ) -> None:
        payload = {prop: value}

        response = auth_client.partial_update_contact(contact_id=contact_id, contact_data=payload)
        response_data = response.json()

        assert response.status == HTTPStatus.BAD_REQUEST, response_data
        assert_that(response_data["errors"][prop]["message"]).is_equal_to(error_msg.format(prop, value))

    @pytest.mark.parametrize(
        "prop, error_msg",
        [
            ("email", "Email is invalid"),
            ("birthdate", "Birthdate is invalid"),
            ("phone", "Phone number is invalid"),
            ("postalCode", "Postal code is invalid"),
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

    def test_partial_update_contact_without_token_provided(self, unauth_client: APIClient, contact_id: str) -> None:
        response = unauth_client.partial_update_contact(contact_id=contact_id, contact_data={})
        response_data = response.json()

        assert response.status == HTTPStatus.UNAUTHORIZED, response_data
        assert_that(response_data).is_equal_to(dict(error=CommonAPIErrors.NOT_AUTHENTICATE))
