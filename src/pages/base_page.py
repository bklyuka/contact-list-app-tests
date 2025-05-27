from typing import Optional

from playwright.sync_api import Page


class BasePage:
    def __init__(self, page: Page):
        self.page: Page = page
        self.relative_url: Optional[str] = None
        self.error = self.page.locator("#error")

    def open(self):
        self.page.goto(self.relative_url)
        return self
