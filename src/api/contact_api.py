from playwright.sync_api import APIResponse

from src.api.api_http_client import ApiHttpClient


class ContactAPI:
    CONTACTS: str = "/contacts"
    CONTACT_BY_ID: str = "/contacts/{id}"

    def __init__(self, client: ApiHttpClient):
        self._client: ApiHttpClient = client

    def create(self, contact_data: dict) -> APIResponse:
        return self._client.post(path=self.CONTACTS, data=contact_data)

    def update(self, contact_id: str, contact_data: dict) -> APIResponse:
        return self._client.put(path=self.CONTACT_BY_ID.format(id=contact_id), data=contact_data)

    def partial_update(self, contact_id: str, contact_data: dict) -> APIResponse:
        return self._client.patch(path=self.CONTACT_BY_ID.format(id=contact_id), data=contact_data)

    def get_all(self) -> APIResponse:
        return self._client.get(path=self.CONTACTS)

    def get(self, contact_id: str) -> APIResponse:
        return self._client.get(path=self.CONTACT_BY_ID.format(id=contact_id))

    def delete(self, contact_id: str) -> APIResponse:
        return self._client.delete(path=self.CONTACT_BY_ID.format(id=contact_id))
