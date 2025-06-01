from random import choice
from http import HTTPStatus
from typing import Any

import pytest
from assertpy import assert_that
from jsonschema.validators import validate

from src.api.api_client import APIClient
from src.errors import CommonErrors, ContactErrors
from src.helpers import get_random_string, get_random_bool, get_random_int, get_fake_id
from src.payloads import CreateUpdateContact
from src.responses import contact_schema


@pytest.fixture(scope="class", name="contact")
def get_contact(auth_client: APIClient) -> dict:
    data = auth_client.get_contacts()
    contacts = data.json()

    if not contacts:
        contact = auth_client.create_contact(contact_data=CreateUpdateContact().__dict__)
        return contact.json()
    return choice(contacts)


class TestAPIGetContact:

    def test_get_contact(self, auth_client: APIClient, contact: dict) -> None:
        response = auth_client.get_contact(contact_id=contact["_id"])
        response_data = response.json()

        assert response.status == HTTPStatus.OK, response_data
        assert_that(response_data).is_equal_to(contact)
        validate(instance=response_data, schema=contact_schema)

    def test_get_contact_with_non_existing_id(self, auth_client: APIClient) -> None:
        response = auth_client.get_contact(contact_id=get_fake_id())

        assert response.status == HTTPStatus.NOT_FOUND
        assert_that(response.text()).is_empty()

    @pytest.mark.parametrize(
        "invalid",
        (get_random_string(), None, get_random_bool(), get_random_int()),
        ids=("string", "None", "boolean", "integer")
    )
    def test_get_contact_with_invalid_data(self, auth_client: APIClient, invalid: Any) -> None:
        response = auth_client.get_contact(contact_id=invalid)

        assert response.status == HTTPStatus.BAD_REQUEST
        assert_that(response.text()).is_equal_to(ContactErrors.INVALID_ID)

    def test_get_contact_without_token_provided(self, unauth_client: APIClient, contact: dict) -> None:
        response = unauth_client.get_contact(contact_id=contact["_id"])
        response_data = response.json()

        assert response.status == HTTPStatus.UNAUTHORIZED, response_data
        assert_that(response_data).is_equal_to(dict(error=CommonErrors.NOT_AUTHENTICATE))
