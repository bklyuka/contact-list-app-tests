from http import HTTPStatus

import pytest
from assertpy import assert_that
from jsonschema.validators import validate

from src.api.api_client import APIClient
from src.errors import CommonErrors
from src.responses import get_contacts_schema


class TestAPIGetContacts:

    @pytest.mark.testomatio("@T47741f1c")
    @pytest.mark.api
    def test_get_contacts(self, auth_client: APIClient) -> None:
        response = auth_client.get_contacts()
        response_data = response.json()

        assert response.status == HTTPStatus.OK, response_data
        validate(instance=response_data, schema=get_contacts_schema)

    @pytest.mark.testomatio("@T0824170f")
    @pytest.mark.api
    def test_get_contacts_without_token_provided(self, unauth_client: APIClient) -> None:
        response = unauth_client.get_contacts()
        response_data = response.json()

        assert response.status == HTTPStatus.UNAUTHORIZED, response_data
        assert_that(response_data).is_equal_to(dict(error=CommonErrors.NOT_AUTHENTICATE))
