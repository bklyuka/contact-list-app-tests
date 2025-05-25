from http import HTTPStatus

from assertpy import assert_that
from jsonschema.validators import validate

from src.api.api_client import APIClient
from src.api.common import CommonAPIErrors
from src.responses import get_contacts_schema


class TestGetContacts:

    def test_get_contacts(self, auth_client: APIClient) -> None:
        response = auth_client.contacts.get_all()
        response_data = response.json()

        assert response.status == HTTPStatus.OK, response_data
        validate(instance=response_data, schema=get_contacts_schema)

    def test_get_contacts_without_token_provided(self, unauth_client: APIClient) -> None:
        response = unauth_client.contacts.get_all()
        response_data = response.json()

        assert response.status == HTTPStatus.UNAUTHORIZED, response_data
        assert_that(response_data).is_equal_to(dict(error=CommonAPIErrors.NOT_AUTHENTICATE))
