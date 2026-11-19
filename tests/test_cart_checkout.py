import pytest
from playwright.sync_api import expect

pytestmark = pytest.mark.ui

BACKPACK = "sauce-labs-backpack"
BIKE_LIGHT = "sauce-labs-bike-light"


def test_add_and_remove_updates_cart_badge(logged_in):
    logged_in.add_to_cart(BACKPACK)
    expect(logged_in.cart_badge).to_have_text("1")
    logged_in.add_to_cart(BIKE_LIGHT)
    expect(logged_in.cart_badge).to_have_text("2")
    logged_in.remove_from_cart(BACKPACK)
    expect(logged_in.cart_badge).to_have_text("1")
    logged_in.remove_from_cart(BIKE_LIGHT)
    expect(logged_in.cart_badge).to_have_count(0)


def test_cart_shows_selected_products(logged_in, cart_page):
    logged_in.add_to_cart(BACKPACK)
    logged_in.add_to_cart(BIKE_LIGHT)
    logged_in.open_cart()
    cart_page.expect_items(["Sauce Labs Backpack", "Sauce Labs Bike Light"])


@pytest.mark.smoke
def test_full_checkout_flow(logged_in, cart_page, checkout_page):
    logged_in.add_to_cart(BACKPACK)
    logged_in.open_cart()
    cart_page.checkout()
    checkout_page.fill_details("Jan", "Kowalski", "44-100")
    checkout_page.finish()
    checkout_page.expect_order_complete()


def test_checkout_totals_are_consistent(logged_in, cart_page, checkout_page):
    logged_in.add_to_cart(BACKPACK)
    logged_in.add_to_cart(BIKE_LIGHT)
    logged_in.open_cart()
    cart_page.checkout()
    checkout_page.fill_details("Jan", "Kowalski", "44-100")

    item_total, tax, total = checkout_page.summary_amounts()
    assert item_total == pytest.approx(29.99 + 9.99)
    assert total == pytest.approx(item_total + tax, abs=0.01)


@pytest.mark.parametrize(
    "first, last, postal, expected_error",
    [
        ("", "Kowalski", "44-100", "First Name is required"),
        ("Jan", "", "44-100", "Last Name is required"),
        ("Jan", "Kowalski", "", "Postal Code is required"),
    ],
    ids=["no-first-name", "no-last-name", "no-postal-code"],
)
def test_checkout_form_validation(logged_in, cart_page, checkout_page, first, last, postal, expected_error):
    logged_in.add_to_cart(BACKPACK)
    logged_in.open_cart()
    cart_page.checkout()
    checkout_page.fill_details(first, last, postal)
    checkout_page.expect_error(expected_error)


def test_sort_by_price_low_to_high(logged_in):
    logged_in.sort_by("lohi")
    prices = logged_in.product_prices()
    assert prices == sorted(prices)


def test_sort_by_name_z_to_a(logged_in):
    logged_in.sort_by("za")
    names = logged_in.product_names()
    assert names == sorted(names, reverse=True)
