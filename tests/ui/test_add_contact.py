import re

import pytest
from playwright.sync_api import expect

from src.pages.add_contact_page import AddContactPage
from src.payloads import CreateUpdateContact


@pytest.fixture(name="add_contact_page")
def get_add_user_page(page) -> AddContactPage:
    return AddContactPage(page).open()


@pytest.fixture(scope="class", name="contact_data")
def get_add_user_data() -> CreateUpdateContact:
    return CreateUpdateContact()


class TestAddContact:

    def test_navigation_to_contact_list_page_from_add_contact(self, add_contact_page: AddContactPage) -> None:
        add_contact_page.cancel_btn.click()
        expect(add_contact_page.page_name).to_have_text("Contact List")
        expect(add_contact_page.page).to_have_url(re.compile(".*contactList"))

    def test_add_contact_without_data_set(self, add_contact_page: AddContactPage) -> None:
        add_contact_page.submit_btn.click()
        expect(add_contact_page.page).to_have_url(re.compile(".*addContact"))
        expect(add_contact_page.error).to_have_text(
            f"Contact validation failed: {add_contact_page.required_msg.format("firstName", "firstName")}, "
            f"{add_contact_page.required_msg.format("lastName", "lastName")}"
        )

    def test_add_contact_without_first_name_set(
            self, add_contact_page: AddContactPage, contact_data: CreateUpdateContact

    ) -> None:
        add_contact_page.last_name_field.fill(contact_data.lastName)
        add_contact_page.submit_btn.click()
        expect(add_contact_page.page).to_have_url(re.compile(".*addContact"))
        expect(add_contact_page.error).to_have_text(
            f"Contact validation failed: {add_contact_page.required_msg.format("firstName", "firstName")}"
        )

    def test_add_contact_without_last_name_set(
            self, add_contact_page: AddContactPage, contact_data: CreateUpdateContact

    ) -> None:
        add_contact_page.first_name_field.fill(contact_data.firstName)
        add_contact_page.submit_btn.click()
        expect(add_contact_page.page).to_have_url(re.compile(".*addContact"))
        expect(add_contact_page.error).to_have_text(
            f"Contact validation failed: {add_contact_page.required_msg.format("lastName", "lastName")}"
        )
