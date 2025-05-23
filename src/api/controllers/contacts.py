from playwright.sync_api import APIResponse

from src.api.request import Request


class Contacts:
    CONTACTS = "/contacts"
    CONTACT_BY_ID = "/contacts/{id}"

    def __init__(self, request: Request):
        self._request: Request = request

    def create_contact(self, contact_data: dict) -> APIResponse:
        return self._request.post(path=self.CONTACTS, data=contact_data)

    def get_contacts(self) -> APIResponse:
        return self._request.get(path=self.CONTACTS)

    def get_contact(self, contact_id: str) -> APIResponse:
        return self._request.get(path=self.CONTACT_BY_ID.format(id=contact_id))

    def delete_contact(self, contact_id: str) -> APIResponse:
        return self._request.delete(path=self.CONTACT_BY_ID.format(id=contact_id))
