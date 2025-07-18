from random import choice
from typing import Any

import pytest

from src.api.contact_api import ContactAPI
from src.payloads import CreateUpdateContact


@pytest.fixture(name="payload")
def get_contact_payload() -> dict[str, Any]:
    return CreateUpdateContact().__dict__


@pytest.fixture(scope="class", name="contact_id")
def get_contact_id(contact_api: ContactAPI) -> str:
    data = contact_api.get_all()
    contacts = data.json()

    if not contacts:
        contact = contact_api.create(contact_data=CreateUpdateContact().__dict__)
        return contact.json()["_id"]
    return choice(contacts)["_id"]


@pytest.fixture(name="contact_api", scope="class")
def get_contact_api(auth_client) -> ContactAPI:
    return ContactAPI(auth_client)


@pytest.fixture(name="contact_api_no_auth")
def get_contact_api_not_auth(unauth_client) -> ContactAPI:
    return ContactAPI(unauth_client)
