from playwright.async_api import Page

from src.ebook_parser import EbookParser


class EbookService:
    def __init__(self, page: Page, parser: EbookParser) -> None:
        self._page: Page = page
        self._parser: EbookParser = parser

    async def capture_all_pages(self) -> list[str]:
        screenshot_paths: list[str] = []

        await self._parser.set_page_fit_scale()

        total_pages = await self._parser.get_total_pages()
        for index in range(total_pages):
            current_page = index + 1

            file_path = f"images/{current_page}.png"

            book_current_page_locator = self._page.locator(
                f'.page[data-page-number="{current_page}"]'
            )

            _ = await book_current_page_locator.screenshot(path=file_path)

            screenshot_paths.append(file_path)

            print(
                f"Screenshot saved as {file_path} | Progress: {current_page} / {total_pages}"
            )

            if not await self._parser.is_last_page():
                await self._parser.navigate_to_next_page()

        return screenshot_paths
