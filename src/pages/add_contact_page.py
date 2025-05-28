from playwright.sync_api import Page

from src.pages.base_page import BasePage


class AddContactPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.relative_url: str = "/addContact"
        self.first_name_field = self.page.locator("#firstName")
        self.last_name_field = self.page.locator("#lastName")
        self.dob_field = self.page.locator("#birthdate")
        self.email_field = self.page.locator("#email")
        self.phone_field = self.page.locator("#phone")
        self.street_address1_field = self.page.locator("#street1")
        self.street_address2_field = self.page.locator("#street2")
        self.city_field = self.page.locator("#city")
        self.state_or_province_field = self.page.locator("#stateProvince")
        self.postal_code_field = self.page.locator("#postalCode")
        self.country_field = self.page.locator("#country")
        self.submit_btn = self.page.get_by_role(role="button", name="Submit")
        self.cancel_btn = self.page.get_by_role(role="button", name="Cancel")
        self.required_msg = "{}: Path `{}` is required."
