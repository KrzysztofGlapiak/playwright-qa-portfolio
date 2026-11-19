from playwright.sync_api import Page, expect


class CheckoutPage:
    def __init__(self, page: Page):
        self.page = page
        self.first_name = page.get_by_test_id("firstName")
        self.last_name = page.get_by_test_id("lastName")
        self.postal_code = page.get_by_test_id("postalCode")
        self.continue_button = page.get_by_test_id("continue")
        self.finish_button = page.get_by_test_id("finish")
        self.error = page.get_by_test_id("error")
        self.total = page.get_by_test_id("total-label")
        self.item_total = page.get_by_test_id("subtotal-label")
        self.tax = page.get_by_test_id("tax-label")
        self.confirmation = page.get_by_test_id("complete-header")

    def fill_details(self, first: str, last: str, postal: str) -> None:
        self.first_name.fill(first)
        self.last_name.fill(last)
        self.postal_code.fill(postal)
        self.continue_button.click()

    def expect_error(self, text: str) -> None:
        expect(self.error).to_contain_text(text)

    @staticmethod
    def _amount(text: str) -> float:
        return float(text.split("$")[-1])

    def summary_amounts(self) -> tuple[float, float, float]:
        """Returns (item_total, tax, total) shown on the overview page."""
        return (
            self._amount(self.item_total.inner_text()),
            self._amount(self.tax.inner_text()),
            self._amount(self.total.inner_text()),
        )

    def finish(self) -> None:
        self.finish_button.click()

    def expect_order_complete(self) -> None:
        expect(self.confirmation).to_have_text("Thank you for your order!")
