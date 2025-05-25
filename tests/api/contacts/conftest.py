from random import choice

import pytest

from src.api.api_client import APIClient
from src.payloads import CreateUpdateContact


@pytest.fixture(name="payload")
def get_contact_payload() -> dict:
    """Fixture returns dictionary payload for create/update contact"""
    return CreateUpdateContact().__dict__


@pytest.fixture(scope="class", name="contact_id")
def get_contact_id(auth_client: APIClient) -> str:
    data = auth_client.get_contacts()
    contacts = data.json()

    if not contacts:
        contact = auth_client.create_contact(contact_data=CreateUpdateContact().__dict__)
        return contact.json()["_id"]
    return choice(contacts)["_id"]
