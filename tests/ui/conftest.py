import pytest
from playwright.sync_api import Playwright, Browser

from src.application_data import config


@pytest.fixture(scope="class")
def browser(playwright: Playwright):
    browser = playwright.chromium.launch(headless=False)
    yield browser
    browser.close()


@pytest.fixture(scope="class")
def page(browser: Browser):
    context = browser.new_context(base_url=config.url)
    page = context.new_page()
    yield page
    page.close()
    context.close()


@pytest.fixture(autouse=True)
def auto_login(page, request):
    if request.node.get_closest_marker("skip_login"):
        yield
        return
    # TODO: login logic
    yield
