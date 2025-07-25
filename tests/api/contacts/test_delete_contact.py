from http import HTTPStatus

import pytest
from assertpy import assert_that

from src.api.contact_api import ContactApi
from src.errors import CommonErrors, ContactErrors
from src.helpers import get_fake_id, get_random_string, get_random_bool, get_random_int


class TestAPIDeleteContact:

    @pytest.mark.testomatio("@Ta0c34c2a")
    @pytest.mark.api
    def test_delete_contact(self, contact_api: ContactApi, contact_id: str) -> None:
        response = contact_api.delete(contact_id=contact_id)

        assert response.status == HTTPStatus.OK
        assert_that(response.text()).is_equal_to("Contact deleted")

    @pytest.mark.testomatio("@T79109dca")
    @pytest.mark.api
    def test_delete_contact_with_non_existing_id(self, contact_api: ContactApi) -> None:
        response = contact_api.delete(contact_id=get_fake_id())

        assert response.status == HTTPStatus.NOT_FOUND
        assert_that(response.text()).is_empty()

    @pytest.mark.testomatio("@T2549e3d9")
    @pytest.mark.api
    @pytest.mark.parametrize(
        "invalid",
        (get_random_string(), None, get_random_bool(), get_random_int()),
        ids=("string", "None", "boolean", "integer")
    )
    def test_delete_contact_with_invalid_contact_id(self, contact_api: ContactApi, invalid: object) -> None:
        response = contact_api.delete(contact_id=invalid)

        assert response.status == HTTPStatus.BAD_REQUEST
        assert_that(response.text()).is_equal_to(ContactErrors.INVALID_ID)

    @pytest.mark.testomatio("@T0901b6cf")
    @pytest.mark.api
    def test_delete_contact_without_token_provided(self, contact_api_no_auth: ContactApi, contact_id: str) -> None:
        response = contact_api_no_auth.delete(contact_id=contact_id)
        response_data = response.json()

        assert response.status == HTTPStatus.UNAUTHORIZED, response_data
        assert_that(response_data).is_equal_to(dict(error=CommonErrors.NOT_AUTHENTICATE))
