import re

import pytest
from playwright.sync_api import expect

from src.application_data import config
from src.pages.login_page import LoginPage
from src.payloads import LoginCredentials


@pytest.fixture(name="login_page")
def get_login_page(page) -> LoginPage:
    return LoginPage(page).open()


@pytest.fixture(scope="class", name="credentials_data")
def get_credentials() -> LoginCredentials:
    return LoginCredentials()


class TestUILogin:
    def test_login_with_with_valid_data(self, login_page: LoginPage) -> None:
        login_page.email_field.fill(config.user_email)
        login_page.password_field.fill(config.user_password)
        login_page.submit_btn.click()
        expect(login_page.page_name).to_have_text("Contact List")
        expect(login_page.page).to_have_url(re.compile(".*contactList"))

    def test_login_without_email_and_password_set(self, login_page: LoginPage) -> None:
        login_page.submit_btn.click()
        expect(login_page.page).to_have_url(re.compile(".*login"))
        expect(login_page.error).to_have_text(login_page.incorrect_password_error_msg)

    def test_login_without_password_set(self, login_page: LoginPage, credentials_data: LoginCredentials) -> None:
        login_page.email_field.fill(credentials_data.email)
        login_page.submit_btn.click()
        expect(login_page.page).to_have_url(re.compile(".*login"))
        expect(login_page.error).to_have_text(login_page.incorrect_password_error_msg)

    def test_login_without_email_set(self, login_page: LoginPage, credentials_data: LoginCredentials) -> None:
        login_page.password_field.fill(credentials_data.password)
        login_page.submit_btn.click()
        expect(login_page.page).to_have_url(re.compile(".*login"))
        expect(login_page.error).to_have_text(login_page.incorrect_password_error_msg)

    def test_navigation_to_add_user_page_from_login(self, login_page: LoginPage) -> None:
        login_page.sign_up_btn.click()
        expect(login_page.page_name).to_have_text("Add User")
        expect(login_page.page).to_have_url(re.compile(".*addUser"))
