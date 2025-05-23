from playwright.sync_api import APIResponse

from src.api.request import Request


class Contacts:
    def __init__(self, request: Request):
        self._request = request

    def create_contact(self, contact_data: dict) -> APIResponse:
        return self._request.post(path="/contacts", data=contact_data)
