from playwright.sync_api import Page, expect


class InventoryPage:
    def __init__(self, page: Page):
        self.page = page
        self.items = page.get_by_test_id("inventory-item")
        self.names = page.get_by_test_id("inventory-item-name")
        self.prices = page.get_by_test_id("inventory-item-price")
        self.sort = page.get_by_test_id("product-sort-container")
        self.cart_link = page.get_by_test_id("shopping-cart-link")
        self.cart_badge = page.get_by_test_id("shopping-cart-badge")
        self.menu_button = page.get_by_role("button", name="Open Menu")
        self.logout_link = page.get_by_test_id("logout-sidebar-link")

    def expect_loaded(self) -> None:
        expect(self.page).to_have_url("/inventory.html")
        expect(self.items.first).to_be_visible()

    def add_to_cart(self, product_slug: str) -> None:
        """product_slug example: 'sauce-labs-backpack'."""
        self.page.get_by_test_id(f"add-to-cart-{product_slug}").click()

    def remove_from_cart(self, product_slug: str) -> None:
        self.page.get_by_test_id(f"remove-{product_slug}").click()

    def sort_by(self, value: str) -> None:
        """value: az | za | lohi | hilo"""
        self.sort.select_option(value)

    def product_names(self) -> list[str]:
        return self.names.all_inner_texts()

    def product_prices(self) -> list[float]:
        return [float(p.replace("$", "")) for p in self.prices.all_inner_texts()]

    def open_cart(self) -> None:
        self.cart_link.click()

    def logout(self) -> None:
        self.menu_button.click()
        self.logout_link.click()
