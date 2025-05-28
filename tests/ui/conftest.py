import pytest
from playwright.sync_api import Playwright, Browser, Page

from src.application_data import config


@pytest.fixture(scope="session", name="token")
def get_token(playwright: Playwright) -> str:
    request_context = playwright.request.new_context(base_url=config.url)
    response = request_context.post("/users/login", data={
            "email": config.user_email,
            "password": config.user_password
        })
    response_data = response.json()
    yield response_data["token"]
    request_context.dispose()


@pytest.fixture(scope="class")
def browser(playwright: Playwright) -> Browser:
    browser = playwright.chromium.launch(headless=False)
    yield browser
    browser.close()


@pytest.fixture(scope="class")
def page(browser: Browser) -> Page:
    context = browser.new_context(base_url=config.url)
    page = context.new_page()
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
