from playwright.sync_api import APIResponse

from src.api.request import Request


class ContactAPI:
    CONTACTS: str = "/contacts"
    CONTACT_BY_ID: str = "/contacts/{id}"

    def __init__(self, request: Request):
        self._request: Request = request

    def create_contact(self, contact_data: dict) -> APIResponse:
        return self._request.post(path=self.CONTACTS, data=contact_data)

    def update_contact(self, contact_id: str, contact_data: dict) -> APIResponse:
        return self._request.put(path=self.CONTACT_BY_ID.format(id=contact_id), data=contact_data)

    def partial_update_contact(self, contact_id: str, contact_data: dict) -> APIResponse:
        return self._request.patch(path=self.CONTACT_BY_ID.format(id=contact_id), data=contact_data)

    def get_contacts(self) -> APIResponse:
        return self._request.get(path=self.CONTACTS)

    def get_contact(self, contact_id: str) -> APIResponse:
        return self._request.get(path=self.CONTACT_BY_ID.format(id=contact_id))

    def delete_contact(self, contact_id: str) -> APIResponse:
        return self._request.delete(path=self.CONTACT_BY_ID.format(id=contact_id))
