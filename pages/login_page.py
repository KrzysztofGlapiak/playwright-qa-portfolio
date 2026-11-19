from playwright.sync_api import Page, expect


class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.username = page.get_by_test_id("username")
        self.password = page.get_by_test_id("password")
        self.submit = page.get_by_test_id("login-button")
        self.error = page.get_by_test_id("error")

    def open(self) -> None:
        self.page.goto("/")

    def login(self, username: str, password: str) -> None:
        self.username.fill(username)
        self.password.fill(password)
        self.submit.click()

    def expect_error(self, text: str) -> None:
        expect(self.error).to_contain_text(text)
