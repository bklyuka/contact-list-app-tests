import pytest
from playwright.sync_api import sync_playwright

from src.api.api_http_client import ApiHttpClient
from src.api.user_api import UserAPI
from src.application_data import config


@pytest.fixture(scope="session")
def playwright_context():
    with sync_playwright() as p:
        context = p.request.new_context()
        yield context
        context.dispose()


@pytest.fixture(scope="session", name="auth_client")
def get_auth_client(playwright_context) -> ApiHttpClient:
    """Session with authentication"""
    client = ApiHttpClient(playwright_context, config.url)
    user_api = UserAPI(client)
    user_api.authenticate(user_email=config.user_email, password=config.user_password)
    return client


@pytest.fixture(name="unauth_client")
def get_unauth_client(playwright_context) -> ApiHttpClient:
    """Session without authentication"""
    return ApiHttpClient(playwright_context, config.url)


def pytest_addoption(parser):
    parser.addoption(
        "--browser-name", action="store", default="chromium", help="Browser type: chromium, firefox, webkit"
    )
    parser.addoption(
        "--show-browser", action="store_true", default=False, help="run tests in headed or headless browser"
    )
