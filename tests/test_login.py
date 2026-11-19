import pytest
from playwright.sync_api import expect

from conftest import PASSWORD

pytestmark = pytest.mark.ui


@pytest.mark.smoke
def test_valid_login_opens_inventory(login_page, inventory_page):
    login_page.open()
    login_page.login("standard_user", PASSWORD)
    inventory_page.expect_loaded()


@pytest.mark.parametrize(
    "username, password, expected_error",
    [
        ("standard_user", "wrong_password", "Username and password do not match"),
        ("unknown_user", PASSWORD, "Username and password do not match"),
        ("", PASSWORD, "Username is required"),
        ("standard_user", "", "Password is required"),
        ("locked_out_user", PASSWORD, "this user has been locked out"),
    ],
    ids=["wrong-password", "unknown-user", "empty-username", "empty-password", "locked-out"],
)
def test_invalid_login_shows_error(login_page, username, password, expected_error):
    login_page.open()
    login_page.login(username, password)
    login_page.expect_error(expected_error)
    expect(login_page.page).to_have_url("/")


def test_protected_page_requires_login(page, login_page):
    page.goto("/inventory.html")
    expect(page).to_have_url("/")
    login_page.expect_error("You can only access '/inventory.html' when you are logged in")


def test_logout_returns_to_login(logged_in, page):
    logged_in.logout()
    expect(page).to_have_url("/")
