from playwright.sync_api import Page, expect


class CartPage:
    def __init__(self, page: Page):
        self.page = page
        self.items = page.get_by_test_id("inventory-item")
        self.names = page.get_by_test_id("inventory-item-name")
        self.checkout_button = page.get_by_test_id("checkout")

    def expect_items(self, expected_names: list[str]) -> None:
        expect(self.page).to_have_url("/cart.html")
        expect(self.names).to_have_text(expected_names)

    def expect_empty(self) -> None:
        expect(self.items).to_have_count(0)

    def checkout(self) -> None:
        self.checkout_button.click()
