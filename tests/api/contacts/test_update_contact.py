from http import HTTPStatus
from typing import Any, List

import pytest
from assertpy import assert_that
from jsonschema.validators import validate

from src.api.contact_api import ContactAPI
from src.errors import ContactErrors, CommonErrors
from src.helpers import get_random_string, get_random_bool, get_random_int
from src.responses import contact_schema


class TestAPIUpdateContact:
    IGNORED_RESPONSE_FIELDS: List[str] = ["_id", "owner", "__v"]

    @pytest.mark.testomatio("@T796705bb")
    @pytest.mark.api
    def test_update_contact_with_valid_data(self, contact_api: ContactAPI, payload: dict, contact_id: str) -> None:
        response = contact_api.update(contact_id=contact_id, contact_data=payload)
        response_data = response.json()

        assert response.status == HTTPStatus.OK, response_data
        assert_that(payload).is_equal_to(response_data, ignore=self.IGNORED_RESPONSE_FIELDS)
        validate(instance=response_data, schema=contact_schema)

    @pytest.mark.testomatio("@T50936357")
    @pytest.mark.api
    @pytest.mark.parametrize(
        "prop", (
                "email", "birthdate", "phone", "street1", "street2", "city", "stateProvince", "postalCode", "country"
        )
    )
    def test_update_contact_without_optional_property(
            self,
            contact_api: ContactAPI,
            contact_id: str,
            payload: dict,
            prop: str
    ) -> None:
        del payload[prop]

        response = contact_api.update(contact_id=contact_id, contact_data=payload)
        response_data = response.json()

        assert response.status == HTTPStatus.OK, response_data
        payload[prop] = None
        assert_that(payload).is_equal_to(response_data, ignore=self.IGNORED_RESPONSE_FIELDS)
        validate(instance=response_data, schema=contact_schema)

    @pytest.mark.testomatio("@Td6f3dca7")
    @pytest.mark.api
    @pytest.mark.parametrize("prop", ("firstName", "lastName"))
    def test_update_contact_without_required_property(
            self,
            contact_api: ContactAPI,
            contact_id: str,
            payload: dict,
            prop: str
    ) -> None:
        del payload[prop]

        response = contact_api.update(contact_id=contact_id, contact_data=payload)
        response_data = response.json()

        assert response.status == HTTPStatus.BAD_REQUEST, response_data
        assert_that(response_data["errors"][prop]["message"]).is_equal_to(CommonErrors.REQUIRED_PROP.format(prop))

    @pytest.mark.testomatio("@T0b2a6ef6")
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
    def test_update_contact_with_invalid_data(
            self,
            contact_api: ContactAPI,
            contact_id: str,
            payload: dict,
            prop: str,
            error_txt: str
    ) -> None:
        payload[prop] = get_random_string()

        response = contact_api.update(contact_id=contact_id, contact_data=payload)
        response_data = response.json()

        assert response.status == HTTPStatus.BAD_REQUEST, response_data
        assert_that(response_data["errors"][prop]["message"]).is_equal_to(error_txt)

    @pytest.mark.testomatio("@Ta3d7f30f")
    @pytest.mark.api
    def test_update_contact_without_token_provided(
            self,
            contact_api_no_auth: ContactAPI,
            contact_id: str,
            payload: dict
    ) -> None:
        response = contact_api_no_auth.update(contact_id=contact_id, contact_data=payload)
        response_data = response.json()

        assert response.status == HTTPStatus.UNAUTHORIZED, response_data
        assert_that(response_data).is_equal_to(dict(error=CommonErrors.NOT_AUTHENTICATE))

    @pytest.mark.testomatio("@T709d6f24")
    @pytest.mark.api
    @pytest.mark.parametrize(
        "invalid",
        (get_random_string(), None, get_random_bool(), get_random_int()),
        ids=("string", "None", "boolean", "integer")
    )
    def test_update_contact_with_invalid_contact_id(self, contact_api: ContactAPI, payload: dict, invalid: Any) -> None:
        response = contact_api.update(contact_id=invalid, contact_data=payload)

        assert response.status == HTTPStatus.BAD_REQUEST
        assert_that(response.text()).is_equal_to(ContactErrors.INVALID_ID)
