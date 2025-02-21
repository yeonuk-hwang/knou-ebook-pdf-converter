import pytest
from playwright.sync_api import BrowserType, Page

from src.browser import BrowserHandler, BrowserNotOpenedError


def test_browser_opens_headed() -> None:
    """Test that browser opens in headed mode using context manager"""
    # When/Then

    with BrowserHandler() as browser_handler:
        page = browser_handler.page
        browser = page.context.browser

        assert browser is not None, "Browser should not be None"

        browser_type = browser.browser_type
        assert browser_type is not None, "BrowserType should not be None"

        assert browser.is_connected()


def test_page_property_raises_error_when_not_opened() -> None:
    """Test that accessing page before opening browser raises error"""
    browser = BrowserHandler()
    with pytest.raises(BrowserNotOpenedError):
        _ = browser.page
