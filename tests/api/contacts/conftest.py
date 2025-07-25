from random import choice

import pytest

from src.api.contact_api import ContactApi
from src.payloads import CreateUpdateContact


@pytest.fixture(name="payload")
def get_contact_payload() -> dict[str, object]:
    return CreateUpdateContact().__dict__


@pytest.fixture(scope="class", name="contact_id")
def get_contact_id(contact_api: ContactApi) -> str:
    data = contact_api.get_all()
    contacts = data.json()

    if not contacts:
        contact = contact_api.create(contact_data=CreateUpdateContact().__dict__)
        return contact.json()["_id"]
    return choice(contacts)["_id"]


@pytest.fixture(name="contact_api", scope="module")
def get_contact_api(auth_client) -> ContactApi:
    return ContactApi(auth_client)


@pytest.fixture(name="contact_api_no_auth")
def get_contact_api_not_auth(unauth_client) -> ContactApi:
    return ContactApi(unauth_client)
