import pytest
from playwright.sync_api import APIRequestContext
from playwright.sync_api import sync_playwright

from src.api.api_client import APIClient
from src.api.request import Request
from src.settings import API_URL, TEST_USER_PASSWORD, TEST_USER_EMAIL


@pytest.fixture(scope="session")
def playwright_context():
    with sync_playwright() as p:
        context = p.request.new_context()
        yield context
        context.dispose()


def _build_request(context: APIRequestContext) -> Request:
    return Request(
        request=context,
        base_url=API_URL
    )


@pytest.fixture(scope="session", name="auth_client")
def get_auth_client(playwright_context) -> APIClient:
    """Session with authentication"""
    request = _build_request(playwright_context)
    client = APIClient(request)
    client.authenticate(user_email=TEST_USER_EMAIL, password=TEST_USER_PASSWORD)
    return client


@pytest.fixture(scope="session", name="unauth_client")
def get_unauth_client(playwright_context) -> APIClient:
    """Session without authentication"""
    request = _build_request(playwright_context)
    return APIClient(request)
