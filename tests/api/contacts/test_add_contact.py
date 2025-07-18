from http import HTTPStatus

import pytest
from assertpy import assert_that
from jsonschema.validators import validate

from src.api.contact_api import ContactAPI
from src.errors import CommonErrors
from src.helpers import get_random_string
from src.responses import contact_schema


class TestAPIAddContact:
    IGNORED_RESPONSE_FIELDS: list[str] = ["_id", "owner", "__v"]

    @pytest.mark.testomatio("@T0aaa513b")
    @pytest.mark.api
    def test_add_contact_with_valid_data(self, contact_api: ContactAPI, payload: dict) -> None:
        response = contact_api.create(contact_data=payload)
        response_data = response.json()

        assert response.status == HTTPStatus.CREATED, response_data
        assert_that(payload).is_equal_to(response_data, ignore=self.IGNORED_RESPONSE_FIELDS)
        validate(instance=response_data, schema=contact_schema)

    @pytest.mark.testomatio("@T62495e27")
    @pytest.mark.api
    @pytest.mark.parametrize(
        "prop", (
                "email", "birthdate", "phone", "street1", "street2", "city", "stateProvince", "postalCode", "country"
        )
    )
    def test_add_contact_without_optional_property(self, contact_api: ContactAPI, payload: dict, prop: str) -> None:
        del payload[prop]

        response = contact_api.create(contact_data=payload)
        response_data = response.json()

        assert response.status == HTTPStatus.CREATED, response_data
        assert_that(payload).is_equal_to(response_data, ignore=self.IGNORED_RESPONSE_FIELDS)
        validate(instance=response_data, schema=contact_schema)

    @pytest.mark.testomatio("@T9afcc0e3")
    @pytest.mark.api
    @pytest.mark.parametrize("prop", ("firstName", "lastName"))
    def test_add_contact_without_required_property(self, contact_api: ContactAPI, payload: dict, prop: str) -> None:
        del payload[prop]

        response = contact_api.create(contact_data=payload)
        response_data = response.json()

        assert response.status == HTTPStatus.BAD_REQUEST, response_data
        assert_that(response_data["errors"][prop]["message"]).is_equal_to(CommonErrors.REQUIRED_PROP.format(prop))

    @pytest.mark.testomatio("@T958b50b1")
    @pytest.mark.api
    @pytest.mark.parametrize(
        "prop, error_txt",
        [
            ("email", CommonErrors.INVALID_PROP.format("Email")),
            ("birthdate", CommonErrors.INVALID_PROP.format("Birthdate")),
            ("phone", CommonErrors.INVALID_PROP.format("Phone number")),
            ("postalCode", CommonErrors.INVALID_PROP.format("Postal code")),
        ]
    )
    def test_add_contact_with_invalid_data(
            self,
            contact_api: ContactAPI,
            payload: dict,
            prop: str,
            error_txt: str
    ) -> None:
        payload[prop] = get_random_string()

        response = contact_api.create(contact_data=payload)
        response_data = response.json()

        assert response.status == HTTPStatus.BAD_REQUEST, response_data
        assert_that(response_data["errors"][prop]["message"]).is_equal_to(error_txt)

    @pytest.mark.testomatio("@Tdccf994e")
    @pytest.mark.api
    def test_add_contact_without_token_provided(self, contact_api_no_auth: ContactAPI, payload: dict) -> None:
        response = contact_api_no_auth.create(contact_data=payload)
        response_data = response.json()

        assert response.status == HTTPStatus.UNAUTHORIZED, response_data
        assert_that(response_data).is_equal_to(dict(error=CommonErrors.NOT_AUTHENTICATE))
