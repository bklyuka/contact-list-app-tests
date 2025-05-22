import pytest

from src.api.api_client import APIClient
from src.payloads.contacts import CreateContact


@pytest.fixture(name="payload")
def get_contact_payload() -> dict:
    return CreateContact().__dict__


class TestAddContact:

    def test_add_contact_with_valid_data(self, auth_client: APIClient, payload: CreateContact):
        print(payload)
        # response = auth_client.create_contact(contact_data=payload)
        # response_data = response.json()
        # print(response_data)

    def test_2(self, auth_client: APIClient, payload: CreateContact):
        print(payload)
        # response = auth_client.create_contact(contact_data=payload)
        # response_data = response.json()
        # print(response_data)
