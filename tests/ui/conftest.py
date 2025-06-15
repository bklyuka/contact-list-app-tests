from dataclasses import dataclass
from typing import Dict

import pytest
from playwright.sync_api import Playwright, Browser, Page

from src.application_data import config


@dataclass
class BrowserConfig:
    type: str
    config: Dict


def _create_browser_config(browser_type: str, headless: bool = True) -> BrowserConfig:
    return BrowserConfig(
        type=browser_type,
        config={"headless": headless}
    )


@pytest.fixture(scope="session")
def browser_config(request) -> BrowserConfig:
    browser_type = request.config.getoption("--browser-name")
    is_headless = not request.config.getoption("--show-browser")

    if browser_type not in ["chromium", "firefox", "webkit"]:
        raise ValueError(f"Unsupported browser: `{browser_type}`")

    return _create_browser_config(browser_type=browser_type, headless=is_headless)


@pytest.fixture(scope="class")
def get_browser(playwright: Playwright, browser_config: BrowserConfig) -> Browser:
    browser: Browser = getattr(playwright, browser_config.type).launch(**browser_config.config)
    yield browser
    browser.close()


@pytest.fixture(scope="class")
def page(get_browser: Browser) -> Page:
    context = get_browser.new_context(base_url=config.url)
    page = context.new_page()
    page.set_viewport_size({"width": 1920, "height": 1024})
    yield page
    page.close()
    context.close()


@pytest.fixture(autouse=True)
def auto_login(page, request, token):
    if request.node.get_closest_marker("skip_login"):
        yield
        return
    page.context.add_cookies([{
        "name": "token",
        "value": token,
        "url": config.url
    }])
    yield


@pytest.fixture(scope="session", name="token")
def get_token(playwright: Playwright) -> str:
    request_context = playwright.request.new_context(base_url=config.url)
    response = request_context.post(
        url="/users/login",
        data={
            "email": config.user_email,
            "password": config.user_password
        }
    )
    response_data = response.json()
    yield response_data["token"]
    request_context.dispose()
