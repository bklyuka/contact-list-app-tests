from random import choice
from http import HTTPStatus
from typing import Any

import pytest
from assertpy import assert_that
from jsonschema.validators import validate

from src.api.contact_api import ContactAPI
from src.errors import CommonErrors, ContactErrors
from src.helpers import get_random_string, get_random_bool, get_random_int, get_fake_id
from src.payloads import CreateUpdateContact
from src.responses import contact_schema


@pytest.fixture(scope="class", name="contact")
def get_contact(contact_api: ContactAPI) -> dict:
    data = contact_api.get_all()
    contacts = data.json()

    if not contacts:
        contact = contact_api.create(contact_data=CreateUpdateContact().__dict__)
        return contact.json()
    return choice(contacts)


class TestAPIGetContact:

    @pytest.mark.testomatio("@Tc1e88708")
    @pytest.mark.api
    def test_get_contact(self, contact_api: ContactAPI, contact: dict) -> None:
        response = contact_api.get(contact_id=contact["_id"])
        response_data = response.json()

        assert response.status == HTTPStatus.OK, response_data
        assert_that(response_data).is_equal_to(contact)
        validate(instance=response_data, schema=contact_schema)

    @pytest.mark.testomatio("@T15642495")
    @pytest.mark.api
    def test_get_contact_with_non_existing_id(self, contact_api: ContactAPI) -> None:
        response = contact_api.get(contact_id=get_fake_id())

        assert response.status == HTTPStatus.NOT_FOUND
        assert_that(response.text()).is_empty()

    @pytest.mark.testomatio("@Tb4e68d02")
    @pytest.mark.api
    @pytest.mark.parametrize(
        "invalid",
        (get_random_string(), None, get_random_bool(), get_random_int()),
        ids=("string", "None", "boolean", "integer")
    )
    def test_get_contact_with_invalid_data(self, contact_api: ContactAPI, invalid: Any) -> None:
        response = contact_api.get(contact_id=invalid)

        assert response.status == HTTPStatus.BAD_REQUEST
        assert_that(response.text()).is_equal_to(ContactErrors.INVALID_ID)

    @pytest.mark.testomatio("@T13fb3a78")
    @pytest.mark.api
    def test_get_contact_without_token_provided(self, contact_api_no_auth: ContactAPI, contact: dict) -> None:
        response = contact_api_no_auth.get(contact_id=contact["_id"])
        response_data = response.json()

        assert response.status == HTTPStatus.UNAUTHORIZED, response_data
        assert_that(response_data).is_equal_to(dict(error=CommonErrors.NOT_AUTHENTICATE))
