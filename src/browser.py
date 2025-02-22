from types import TracebackType
from typing import Literal

from playwright.async_api import (
    Browser,
    BrowserContext,
    Page,
    Playwright,
    ViewportSize,
    async_playwright,
)
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
        self._context: BrowserContext | None = None
        self._page: Page | None = None

    async def __aenter__(self) -> Self:
        """Context manager entry point"""
        await self._open()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> Literal[False]:
        """Context manager exit point"""
        await self._close()
        return False

    async def _open(self) -> None:
        self._playwright = await async_playwright().start()
        self._browser = await self._playwright.chromium.launch(
            executable_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            headless=False,
            slow_mo=500,
        )
        self._context = await self._browser.new_context(
            viewport=ViewportSize(width=1920, height=1440)
        )
        await self._context.add_init_script("""
            const defaultGetter = Object.getOwnPropertyDescriptor(
              Navigator.prototype,
              "webdriver"
            ).get;
            defaultGetter.apply(navigator);
            defaultGetter.toString();
            Object.defineProperty(Navigator.prototype, "webdriver", {
              set: undefined,
              enumerable: true,
              configurable: true,
              get: new Proxy(defaultGetter, {
                apply: (target, thisArg, args) => {
                  Reflect.apply(target, thisArg, args);
                  return false;
                },
              }),
            });
            const patchedGetter = Object.getOwnPropertyDescriptor(
              Navigator.prototype,
              "webdriver"
            ).get;
            patchedGetter.apply(navigator);
            patchedGetter.toString();
        """)
        self._context.on("page", self._on_new_page)
        self._page = await self._context.new_page()
        _ = await self._page.goto(
            "https://ucampus.knou.ac.kr/ekp/user/login/retrieveULOLogin.do"
        )

    async def _on_new_page(self, page: Page) -> None:
        """새로 열린 페이지가 있을 때 호출됨"""
        self._page = page
        print(f"New page opened: {page.url}")

    async def _close(self) -> None:
        """Closes all browser resources"""
        if self._context:
            await self._context.close()
        if self._browser:
            await self._browser.close()
        if self._playwright:
            await self._playwright.stop()
        print("browser has been closed gracefully")

    @property
    def browser(self) -> Browser:
        if self._browser is None or not self._browser.is_connected():
            raise BrowserNotOpenedError()
        return self._browser

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
