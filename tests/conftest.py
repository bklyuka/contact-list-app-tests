from dataclasses import dataclass
from typing import Dict

import pytest
from playwright.sync_api import APIRequestContext
from playwright.sync_api import Playwright, Browser, Page
from playwright.sync_api import sync_playwright

from src.api.api_client import APIClient
from src.api.request import Request
from src.application_data import config


@pytest.fixture(scope='session')
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


@pytest.fixture(scope='session', name='auth_client')
def get_auth_client(playwright_context) -> APIClient:
    """Session with authentication"""
    request = _build_request(playwright_context)
    client = APIClient(request)
    client.authenticate(user_email=config.user_email, password=config.user_password)
    return client


@pytest.fixture(name='unauth_client')
def get_unauth_client(playwright_context) -> APIClient:
    """Session without authentication"""
    request = _build_request(playwright_context)
    return APIClient(request)


@pytest.fixture(scope='session', name='token')
def get_token(playwright: Playwright) -> str:
    request_context = playwright.request.new_context(base_url=config.url)
    response = request_context.post('/users/login', data={
            'email': config.user_email,
            'password': config.user_password
        })
    response_data = response.json()
    yield response_data['token']
    request_context.dispose()


def pytest_addoption(parser):
    parser.addoption(
        '--browser-name', action='store', default='chromium', help='Browser type: chromium, firefox, webkit'
    )
    parser.addoption(
        '--show-browser', action='store_true', default=False, help='run tests in headed or headless browser'
    )


@dataclass
class BrowserConfig:
    type: str
    config: Dict
    browser_context_args: Dict


def _create_browser_config(browser_type: str, headless: bool = True) -> BrowserConfig:
    return BrowserConfig(
        type=browser_type,
        config={"headless": headless},
        browser_context_args={"viewport": {"width": 1440, "height": 768}}
    )


@pytest.fixture(scope='session')
def browser_config(request) -> BrowserConfig:
    browser_type = request.config.getoption('--browser-name')
    is_headless = not request.config.getoption('--show-browser')

    if browser_type not in ['chromium', 'firefox', 'webkit']:
        raise ValueError(f'Unsupported browser: `{browser_type}`')

    return _create_browser_config(browser_type=browser_type, headless=is_headless)


@pytest.fixture(scope='class')
def get_browser(playwright: Playwright, browser_config: BrowserConfig) -> Browser:
    browser = getattr(playwright, browser_config.type).launch(**browser_config.config)
    yield browser
    browser.close()


@pytest.fixture(scope='class')
def page(get_browser: Browser) -> Page:
    context = get_browser.new_context(base_url=config.url)
    page = context.new_page()
    yield page
    page.close()
    context.close()


@pytest.fixture(autouse=True)
def auto_login(page, request, token):
    if request.node.get_closest_marker('skip_login'):
        yield
        return
    page.context.add_cookies([{
        'name': 'token',
        'value': token,
        'url': config.url
    }])
    yield
