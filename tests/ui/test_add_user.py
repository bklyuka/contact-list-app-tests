import re

import pytest
from playwright.sync_api import expect

from src.application_data import config
from src.errors import UserErrors, CommonErrors
from src.helpers import get_random_string
from src.pages.add_user_page import AddUserPage
from src.payloads import CreateUser


@pytest.fixture(name="add_user_page")
def get_add_user_page(page) -> AddUserPage:
    return AddUserPage(page).open()


@pytest.fixture(scope="class", name="user_data")
def get_add_user_data() -> CreateUser:
    return CreateUser()


@pytest.mark.skip_login
class TestAddUser:

    def test_add_user_without_data_set(self, add_user_page: AddUserPage) -> None:
        add_user_page.submit_btn.click()
        expect(add_user_page.page).to_have_url(re.compile(".*addUser"))
        expect(add_user_page.error).to_have_text(
            f"User validation failed: {add_user_page.required_msg.format("firstName", "firstName")}, "
            f"{add_user_page.required_msg.format("lastName", "lastName")}, "
            f"email: {CommonErrors.INVALID_PROP.format("Email")}, "
            f"{add_user_page.required_msg.format("password", "password")}"
        )

    def test_add_user_without_first_name_set(self, add_user_page: AddUserPage, user_data: CreateUser) -> None:
        add_user_page.last_name_field.fill(user_data.lastName)
        add_user_page.email_field.fill(user_data.email)
        add_user_page.password_field.fill(user_data.password)
        add_user_page.submit_btn.click()
        expect(add_user_page.page).to_have_url(re.compile(".*addUser"))
        expect(add_user_page.error).to_have_text(
            f"User validation failed: {add_user_page.required_msg.format("firstName", "firstName")}"
        )

    def test_add_user_without_last_name_set(self, add_user_page: AddUserPage, user_data: CreateUser) -> None:
        add_user_page.first_name_field.fill(user_data.firstName)
        add_user_page.email_field.fill(user_data.email)
        add_user_page.password_field.fill(user_data.password)
        add_user_page.submit_btn.click()
        expect(add_user_page.page).to_have_url(re.compile(".*addUser"))
        expect(add_user_page.error).to_have_text(
            f"User validation failed: {add_user_page.required_msg.format("lastName", "lastName")}"
        )

    def test_add_user_without_email_set(self, add_user_page: AddUserPage, user_data: CreateUser) -> None:
        add_user_page.first_name_field.fill(user_data.firstName)
        add_user_page.last_name_field.fill(user_data.lastName)
        add_user_page.password_field.fill(user_data.password)
        add_user_page.submit_btn.click()
        expect(add_user_page.page).to_have_url(re.compile(".*addUser"))
        expect(add_user_page.error).to_have_text(
            f"User validation failed: email: {CommonErrors.INVALID_PROP.format("Email")}"
        )

    def test_add_user_without_password_set(self, add_user_page: AddUserPage, user_data: CreateUser) -> None:
        add_user_page.first_name_field.fill(user_data.firstName)
        add_user_page.last_name_field.fill(user_data.lastName)
        add_user_page.email_field.fill(user_data.email)
        add_user_page.submit_btn.click()
        expect(add_user_page.page).to_have_url(re.compile(".*addUser"))
        expect(add_user_page.error).to_have_text(
            f"User validation failed: {add_user_page.required_msg.format("password", "password")}"
        )

    def test_add_user_with_already_used_email_set(self, add_user_page: AddUserPage, user_data: CreateUser) -> None:
        add_user_page.first_name_field.fill(user_data.firstName)
        add_user_page.last_name_field.fill(user_data.lastName)
        add_user_page.email_field.fill(config.user_email)
        add_user_page.password_field.fill(user_data.password)
        add_user_page.submit_btn.click()
        expect(add_user_page.page).to_have_url(re.compile(".*addUser"))
        expect(add_user_page.error).to_have_text(UserErrors.USED_EMAIL)

    def test_add_user_with_invalid_length_value_for_password(
            self, add_user_page: AddUserPage, user_data: CreateUser
    ) -> None:
        invalid_password = get_random_string(length=6)
        add_user_page.first_name_field.fill(user_data.firstName)
        add_user_page.last_name_field.fill(user_data.lastName)
        add_user_page.email_field.fill(user_data.email)
        add_user_page.password_field.fill(invalid_password)
        add_user_page.submit_btn.click()
        expect(add_user_page.page).to_have_url(re.compile(".*addUser"))
        expect(add_user_page.error).to_have_text(
            f"User validation failed: password: "
            f"{CommonErrors.MIN_ALLOWED.format(property='password', value=invalid_password, min_limit=7)}"
        )

    def test_add_user_with_invalid_length_value_for_first_name(
            self, add_user_page: AddUserPage, user_data: CreateUser
    ) -> None:
        invalid_first_name = get_random_string(length=21)
        add_user_page.first_name_field.fill(invalid_first_name)
        add_user_page.last_name_field.fill(user_data.lastName)
        add_user_page.email_field.fill(user_data.email)
        add_user_page.password_field.fill(user_data.password)
        add_user_page.submit_btn.click()
        expect(add_user_page.page).to_have_url(re.compile(".*addUser"))
        expect(add_user_page.error).to_have_text(
            f"User validation failed: firstName: "
            f"{CommonErrors.MAX_ALLOWED.format('firstName', invalid_first_name, 20)}"
        )

    def test_add_user_with_invalid_length_value_for_last_name(
            self, add_user_page: AddUserPage, user_data: CreateUser
    ) -> None:
        invalid_last_name = get_random_string(length=21)
        add_user_page.first_name_field.fill(user_data.firstName)
        add_user_page.last_name_field.fill(invalid_last_name)
        add_user_page.email_field.fill(user_data.email)
        add_user_page.password_field.fill(user_data.password)
        add_user_page.submit_btn.click()
        expect(add_user_page.page).to_have_url(re.compile(".*addUser"))
        expect(add_user_page.error).to_have_text(
            f"User validation failed: lastName: "
            f"{CommonErrors.MAX_ALLOWED.format('lastName', invalid_last_name, 20)}"
        )

    def test_navigation_to_login_page_from_add_user(self, add_user_page: AddUserPage) -> None:
        add_user_page.cancel_btn.click()
        expect(add_user_page.page_name).to_have_text("Contact List App")
        expect(add_user_page.page).to_have_url(re.compile(".*login"))
