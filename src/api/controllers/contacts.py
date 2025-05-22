from dataclasses import asdict

from playwright.sync_api import APIResponse

from src.api.request import Request
from src.payloads.contacts import CreateContact


class Contacts:
    def __init__(self, request: Request):
        self._request = request

    def create_contact(self, contact_data: CreateContact) -> APIResponse:
        return self._request.post(path="/contacts", data=asdict(contact_data))
