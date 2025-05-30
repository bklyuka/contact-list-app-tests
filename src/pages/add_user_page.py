from playwright.sync_api import Page

from src.pages.base_page import BasePage
from src.payloads import CreateUser


class AddUserPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.relative_url: str = "/addUser"
        self.first_name_field = self.page.locator("#firstName")
        self.last_name_field = self.page.locator("#lastName")
        self.email_field = self.page.locator("#email")
        self.password_field = self.page.locator("#password")
        self.submit_btn = self.page.get_by_role(role="button", name="Submit")
        self.cancel_btn = self.page.get_by_role(role="button", name="Cancel")
        self.required_msg = "{}: Path `{}` is required."

    def fill_and_submit_form(
            self,
            first_name: str = "",
            last_name: str = "",
            email: str = "",
            password: str = ""
    ) -> None:
        self.first_name_field.fill(first_name)
        self.last_name_field.fill(last_name)
        self.email_field.fill(email)
        self.password_field.fill(password)
        self.submit_btn.click()
