from http import HTTPStatus
from typing import Any

import pytest
from assertpy import assert_that
from jsonschema.validators import validate

from src.api.api_client import APIClient
from src.api.common import CommonAPIErrors, ContactAPIErrors
from src.helpers import get_random_string, get_random_bool, get_random_int
from src.responses import contact_schema


class TestUpdateContact:
    IGNORED_RESPONSE_FIELDS = ["_id", "owner", "__v"]

    def test_update_contact_with_valid_data(self, auth_client: APIClient, payload: dict, contact_id: str) -> None:
        response = auth_client.update_contact(contact_id=contact_id, contact_data=payload)
        response_data = response.json()

        assert response.status == HTTPStatus.OK, response_data
        assert_that(payload).is_equal_to(response_data, ignore=self.IGNORED_RESPONSE_FIELDS)
        validate(instance=response_data, schema=contact_schema)

    @pytest.mark.parametrize(
        "prop", (
                "email", "birthdate", "phone", "street1", "street2", "city", "stateProvince", "postalCode", "country"
        )
    )
    def test_update_contact_without_optional_property(
            self,
            auth_client: APIClient,
            contact_id: str,
            payload: dict,
            prop: str
    ) -> None:
        del payload[prop]

        response = auth_client.update_contact(contact_id=contact_id, contact_data=payload)
        response_data = response.json()

        assert response.status == HTTPStatus.OK, response_data
        payload[prop] = None
        assert_that(payload).is_equal_to(response_data, ignore=self.IGNORED_RESPONSE_FIELDS)
        validate(instance=response_data, schema=contact_schema)

    @pytest.mark.parametrize("prop", ("firstName", "lastName"))
    def test_update_contact_without_required_property(
            self,
            auth_client: APIClient,
            contact_id: str,
            payload: dict,
            prop: str
    ) -> None:
        del payload[prop]

        response = auth_client.update_contact(contact_id=contact_id, contact_data=payload)
        response_data = response.json()

        assert response.status == HTTPStatus.BAD_REQUEST, response_data
        assert_that(response_data["errors"][prop]["message"]).is_equal_to(f"Path `{prop}` is required.")

    @pytest.mark.parametrize(
        "prop, error_txt",
        [
            ("email", "Email is invalid"),
            ("birthdate", "Birthdate is invalid"),
            ("phone", "Phone number is invalid"),
            ("postalCode", "Postal code is invalid")
        ]
    )
    def test_update_contact_with_invalid_data(
            self,
            auth_client: APIClient,
            contact_id: str,
            payload: dict,
            prop: str,
            error_txt: str
    ) -> None:
        payload[prop] = get_random_string()

        response = auth_client.update_contact(contact_id=contact_id, contact_data=payload)
        response_data = response.json()

        assert response.status == HTTPStatus.BAD_REQUEST, response_data
        assert_that(response_data["errors"][prop]["message"]).is_equal_to(error_txt)

    def test_update_contact_without_token_provided(
            self,
            unauth_client: APIClient,
            contact_id: str,
            payload: dict
    ) -> None:
        response = unauth_client.update_contact(contact_id=contact_id, contact_data=payload)
        response_data = response.json()

        assert response.status == HTTPStatus.UNAUTHORIZED, response_data
        assert_that(response_data).is_equal_to(dict(error=CommonAPIErrors.NOT_AUTHENTICATE))

    @pytest.mark.parametrize(
        "invalid",
        (get_random_string(), None, get_random_bool(), get_random_int()),
        ids=("string", "None", "boolean", "integer")
    )
    def test_update_contact_with_invalid_contact_id(self, auth_client: APIClient, payload: dict, invalid: Any) -> None:
        response = auth_client.update_contact(contact_id=invalid, contact_data=payload)

        assert response.status == HTTPStatus.BAD_REQUEST
        assert_that(response.text()).is_equal_to(ContactAPIErrors.INVALID_ID)
