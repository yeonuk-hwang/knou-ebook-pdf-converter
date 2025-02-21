from types import TracebackType

from playwright.sync_api import Browser, Page, Playwright, sync_playwright
from typing_extensions import Self  # for Python < 3.11


class BrowserNotOpenedError(Exception):
    """Raised when trying to access browser resources before opening the browser"""

    def __init__(self) -> None:
        message = "Browser not opened"
        super().__init__(message)


class BrowserHandler:
    """Handles browser operation"""

    def __init__(self) -> None:
        self._playwright: Playwright | None = None
        self._browser: Browser | None = None
        self._page: Page | None = None

    def __enter__(self) -> Self:
        """Context manager entry point"""
        self.open()  # pyright: ignore[reportUnusedCallResult]
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Context manager exit point"""
        self.close()

    def open(self) -> None:
        self._playwright = sync_playwright().start()
        self._browser = self._playwright.chromium.launch(headless=False)
        self._page = self._browser.new_page()

    def close(self) -> None:
        """Closes all browser resources"""
        if self._page:
            self._page.close()
        if self._browser:
            self._browser.close()
        if self._playwright:
            self._playwright.stop()

    @property
    def page(self) -> Page:
        """
        Get the current page
        Returns:
            Page: The current browser page
        Raises:
            BrowserNotOpenedError: If browser is not opened
        """
        if not self._page:
            raise BrowserNotOpenedError()
        return self._page
