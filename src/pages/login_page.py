from playwright.sync_api import Page

from src.pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.relative_url: str = "/login"
        self.email_field = self.page.locator("#email")
        self.password_field = self.page.locator("#password")
        self.submit_btn = self.page.get_by_role(role="button", name="Submit")
        self.sign_up_btn = self.page.get_by_role(role="button", name="Sign up")
        self.incorrect_password_error_msg: str = "Incorrect username or password"
