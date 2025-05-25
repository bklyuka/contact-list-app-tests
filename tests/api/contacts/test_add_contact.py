from http import HTTPStatus

import pytest
from assertpy import assert_that
from jsonschema.validators import validate

from src.api.api_client import APIClient
from src.api.common import CommonAPIErrors
from src.helpers import get_random_string
from src.responses import contact_schema


class TestAddContact:
    IGNORED_RESPONSE_FIELDS: list = ["_id", "owner", "__v"]

    def test_add_contact_with_valid_data(self, auth_client: APIClient, payload: dict) -> None:
        response = auth_client.create_contact(contact_data=payload)
        response_data = response.json()

        assert response.status == HTTPStatus.CREATED, response_data
        assert_that(payload).is_equal_to(response_data, ignore=self.IGNORED_RESPONSE_FIELDS)
        validate(instance=response_data, schema=contact_schema)

    @pytest.mark.parametrize(
        "prop", (
                "email", "birthdate", "phone", "street1", "street2", "city", "stateProvince", "postalCode", "country"
        )
    )
    def test_add_contact_without_optional_property(self, auth_client: APIClient, payload: dict, prop: str) -> None:
        del payload[prop]

        response = auth_client.create_contact(contact_data=payload)
        response_data = response.json()

        assert response.status == HTTPStatus.CREATED, response_data
        assert_that(payload).is_equal_to(response_data, ignore=self.IGNORED_RESPONSE_FIELDS)
        validate(instance=response_data, schema=contact_schema)

    @pytest.mark.parametrize("prop", ("firstName", "lastName"))
    def test_add_contact_without_required_property(self, auth_client: APIClient, payload: dict, prop: str) -> None:
        del payload[prop]

        response = auth_client.create_contact(contact_data=payload)
        response_data = response.json()

        assert response.status == HTTPStatus.BAD_REQUEST, response_data
        assert_that(response_data["errors"][prop]["message"]).is_equal_to(CommonAPIErrors.REQUIRED_PROP.format(prop))

    @pytest.mark.parametrize(
        "prop, error_txt",
        [
            ("email", "Email is invalid"),
            ("birthdate", "Birthdate is invalid"),
            ("phone", "Phone number is invalid"),
            ("postalCode", "Postal code is invalid")
        ]
    )
    def test_add_contact_with_invalid_data(
            self,
            auth_client: APIClient,
            payload: dict,
            prop: str,
            error_txt: str
    ) -> None:
        payload[prop] = get_random_string()

        response = auth_client.create_contact(contact_data=payload)
        response_data = response.json()

        assert response.status == HTTPStatus.BAD_REQUEST, response_data
        assert_that(response_data["errors"][prop]["message"]).is_equal_to(error_txt)

    def test_add_contact_without_token_provided(self, unauth_client: APIClient, payload: dict) -> None:
        response = unauth_client.create_contact(contact_data=payload)
        response_data = response.json()

        assert response.status == HTTPStatus.UNAUTHORIZED, response_data
        assert_that(response_data).is_equal_to(dict(error=CommonAPIErrors.NOT_AUTHENTICATE))
