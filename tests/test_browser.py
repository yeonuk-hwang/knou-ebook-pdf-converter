# pyright: reportAny=false

from unittest.mock import MagicMock, patch

import pytest
from playwright.sync_api import Browser, Page, Playwright

from src.browser import BrowserHandler, BrowserNotOpenedError


def test_browser_opens_in_headed_mode() -> None:
    """
    Test that browser opens in headed mode configuration and calls expected methods
    """
    # Arrange
    mock_page = MagicMock(spec=Page)
    mock_browser = MagicMock(spec=Browser)
    mock_browser.new_page.return_value = mock_page

    mock_chromium = MagicMock()
    mock_chromium.launch.return_value = mock_browser

    mock_playwright = MagicMock(spec=Playwright)
    mock_playwright.chromium = mock_chromium

    mock_sync_playwright = MagicMock()
    mock_sync_playwright.start.return_value = mock_playwright

    # Act
    with patch("src.browser.sync_playwright", return_value=mock_sync_playwright):
        with BrowserHandler() as handler:
            # Assert
            mock_sync_playwright.start.assert_called_once()
            mock_chromium.launch.assert_called_once_with(headless=False)
            mock_browser.new_page.assert_called_once()
            assert handler.page == mock_page


def test_browser_properly_closed_after_with_statements() -> None:
    """
    Test that all browser resources are properly closed after exiting context
    """
    # Arrange
    mock_page = MagicMock(spec=Page)
    mock_browser = MagicMock(spec=Browser)
    mock_browser.new_page.return_value = mock_page

    mock_chromium = MagicMock()
    mock_chromium.launch.return_value = mock_browser

    mock_playwright = MagicMock(spec=Playwright)
    mock_playwright.chromium = mock_chromium

    mock_sync_playwright = MagicMock()
    mock_sync_playwright.start.return_value = mock_playwright

    # Act
    with patch("src.browser.sync_playwright", return_value=mock_sync_playwright):
        with BrowserHandler():
            pass  # Context execution

    # Assert
    mock_page.close.assert_called_once()
    mock_browser.close.assert_called_once()
    mock_playwright.stop.assert_called_once()


def test_raises_browser_not_opened_error_outside_context() -> None:
    """
    Test that accessing page property outside context manager raises BrowserNotOpenedError
    """
    # Arrange
    handler = BrowserHandler()

    # Act & Assert
    with pytest.raises(BrowserNotOpenedError):
        _ = handler.page
