import pytest
from playwright.sync_api import APIRequestContext
from playwright.sync_api import sync_playwright

from src.api.api_client import APIClient
from src.api.request import Request
from src.application_data import config


@pytest.fixture(scope="session")
def playwright_context():
    with sync_playwright() as p:
        context = p.request.new_context()
        yield context
        context.dispose()


def _build_request(context: APIRequestContext) -> Request:
    return Request(
        request=context,
        base_url=config.url
    )


@pytest.fixture(scope="session", name="auth_client")
def get_auth_client(playwright_context) -> APIClient:
    """Session with authentication"""
    request = _build_request(playwright_context)
    client = APIClient(request)
    client.authenticate(user_email=config.user_email, password=config.user_password)
    return client


@pytest.fixture(name="unauth_client")
def get_unauth_client(playwright_context) -> APIClient:
    """Session without authentication"""
    request = _build_request(playwright_context)
    return APIClient(request)
