import pytest
from playwright.sync_api import expect

from src.application_data import config
from src.pages.add_user_page import AddUserPage
from src.payloads import CreateUser


@pytest.fixture(name="add_user_page")
def get_add_user_page(page) -> AddUserPage:
    return AddUserPage(page).open()


@pytest.fixture(scope="class", name="user_data")
def get_add_user_data() -> CreateUser:
    return CreateUser()


class TestAddUser:

    def test_add_user_without_data_set(self, add_user_page: AddUserPage):
        add_user_page.submit_btn.click()
        expect(add_user_page.error).to_have_text(
            f"User validation failed: {add_user_page.required_msg.format("firstName", "firstName")}, "
            f"{add_user_page.required_msg.format("lastName", "lastName")}, "
            f"email: {add_user_page.invalid_email_msg}, {add_user_page.required_msg.format("password", "password")}"
        )

    def test_add_user_without_first_name_set(self, add_user_page: AddUserPage, user_data: CreateUser):
        add_user_page.last_name_field.fill(user_data.lastName)
        add_user_page.email_field.fill(user_data.email)
        add_user_page.password_field.fill(user_data.password)
        add_user_page.submit_btn.click()
        expect(add_user_page.error).to_have_text(
            f"User validation failed: {add_user_page.required_msg.format("firstName", "firstName")}"
        )

    def test_add_user_without_last_name_set(self, add_user_page: AddUserPage, user_data: CreateUser):
        add_user_page.first_name_field.fill(user_data.firstName)
        add_user_page.email_field.fill(user_data.email)
        add_user_page.password_field.fill(user_data.password)
        add_user_page.submit_btn.click()
        expect(add_user_page.error).to_have_text(
            f"User validation failed: {add_user_page.required_msg.format("lastName", "lastName")}"
        )

    def test_add_user_without_email_set(self, add_user_page: AddUserPage, user_data: CreateUser):
        add_user_page.first_name_field.fill(user_data.firstName)
        add_user_page.last_name_field.fill(user_data.lastName)
        add_user_page.password_field.fill(user_data.password)
        add_user_page.submit_btn.click()
        expect(add_user_page.error).to_have_text(f"User validation failed: email: {add_user_page.invalid_email_msg}")

    def test_add_user_without_password_set(self, add_user_page: AddUserPage, user_data: CreateUser):
        add_user_page.first_name_field.fill(user_data.firstName)
        add_user_page.last_name_field.fill(user_data.lastName)
        add_user_page.email_field.fill(user_data.email)
        add_user_page.submit_btn.click()
        expect(add_user_page.error).to_have_text(
            f"User validation failed: {add_user_page.required_msg.format("password", "password")}"
        )

    def test_add_user_with_already_used_email_set(self, add_user_page: AddUserPage, user_data: CreateUser):
        add_user_page.first_name_field.fill(user_data.firstName)
        add_user_page.last_name_field.fill(user_data.lastName)
        add_user_page.email_field.fill(config.user_email)
        add_user_page.password_field.fill(user_data.password)
        add_user_page.submit_btn.click()
        expect(add_user_page.error).to_have_text(add_user_page.used_email_msg)
