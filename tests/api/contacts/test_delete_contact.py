from http import HTTPStatus
from typing import Any

import pytest
from assertpy import assert_that

from src.api.api_client import APIClient
from src.errors import CommonErrors, ContactErrors
from src.helpers import get_fake_id, get_random_string, get_random_bool, get_random_int


class TestAPIDeleteContact:

    def test_delete_contact(self, auth_client: APIClient, contact_id: str) -> None:
        response = auth_client.delete_contact(contact_id=contact_id)

        assert response.status == HTTPStatus.OK
        assert_that(response.text()).is_equal_to("Contact deleted")

    def test_delete_contact_with_non_existing_id(self, auth_client: APIClient) -> None:
        response = auth_client.delete_contact(contact_id=get_fake_id())

        assert response.status == HTTPStatus.NOT_FOUND
        assert_that(response.text()).is_empty()

    @pytest.mark.parametrize(
        "invalid",
        (get_random_string(), None, get_random_bool(), get_random_int()),
        ids=("string", "None", "boolean", "integer")
    )
    def test_delete_contact_with_invalid_contact_id(self, auth_client: APIClient, invalid: Any) -> None:
        response = auth_client.delete_contact(contact_id=invalid)

        assert response.status == HTTPStatus.BAD_REQUEST
        assert_that(response.text()).is_equal_to(ContactErrors.INVALID_ID)

    def test_delete_contact_without_token_provided(self, unauth_client: APIClient, contact_id: str) -> None:
        response = unauth_client.delete_contact(contact_id=contact_id)
        response_data = response.json()

        assert response.status == HTTPStatus.UNAUTHORIZED, response_data
        assert_that(response_data).is_equal_to(dict(error=CommonErrors.NOT_AUTHENTICATE))
