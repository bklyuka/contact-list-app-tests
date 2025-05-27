from playwright.sync_api import Page

from src.pages.base_page import BasePage


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
        self.used_email_msg: str = "Email address is already in use"
        self.required_msg = "{}: Path `{}` is required."
        self.invalid_email_msg = "Email is invalid"
