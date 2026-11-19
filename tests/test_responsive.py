"""Layout checks across common resolutions, the kind of check I run by hand on web/mobile products."""
import pytest
from playwright.sync_api import expect

pytestmark = [pytest.mark.ui, pytest.mark.responsive]

VIEWPORTS = {
    "mobile-375x667": {"width": 375, "height": 667},
    "tablet-768x1024": {"width": 768, "height": 1024},
    "laptop-1366x768": {"width": 1366, "height": 768},
    "desktop-1920x1080": {"width": 1920, "height": 1080},
}


@pytest.fixture(params=VIEWPORTS.values(), ids=VIEWPORTS.keys())
def sized_page(page, request):
    page.set_viewport_size(request.param)
    return page


def has_horizontal_scroll(page) -> bool:
    return page.evaluate(
        "document.documentElement.scrollWidth > document.documentElement.clientWidth + 1"
    )


def test_login_page_fits_viewport(sized_page, login_page):
    login_page.open()
    expect(login_page.username).to_be_visible()
    expect(login_page.submit).to_be_visible()
    assert not has_horizontal_scroll(sized_page)


def test_inventory_fits_viewport(sized_page, login_page, inventory_page):
    from conftest import PASSWORD

    login_page.open()
    login_page.login("standard_user", PASSWORD)
    inventory_page.expect_loaded()
    expect(inventory_page.cart_link).to_be_visible()
    expect(inventory_page.menu_button).to_be_visible()
    assert not has_horizontal_scroll(sized_page)
