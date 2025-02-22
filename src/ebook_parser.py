import re
from dataclasses import dataclass
from typing import Final

from playwright.async_api import Page


@dataclass(frozen=True)
class PageInfo:
    current: int
    total: int

    def is_last_page(self) -> bool:
        """Check if current page is the last page."""
        return self.current == self.total


class EbookParser:
    _PAGE_INDICATOR_PATTERN: re.Pattern[str] = re.compile(r"\((\d+) of (\d+)\)")

    def __init__(self, page: Page) -> None:
        self._page: Page = page

    async def calculate_total_pages(self) -> int:
        return (await self._get_page_info()).total

    async def is_last_page(self) -> bool:
        return (await self._get_page_info()).is_last_page()

    async def _get_page_info(self) -> PageInfo:
        """Extract current and total page numbers from the page indicator text."""
        page_text = await self._get_page_indicator_text()
        current, total = self._parse_page_numbers(page_text)
        return PageInfo(current=current, total=total)

    async def _get_page_indicator_text(self) -> str:
        """Get the text content of the page indicator element."""
        page_indicator = self._page.get_by_text(self._PAGE_INDICATOR_PATTERN)
        return str(await page_indicator.inner_text())

    @staticmethod
    def _parse_page_numbers(text: str) -> tuple[int, int]:
        numbers = list(map(int, re.findall(r"\d+", text)))

        if len(numbers) != 2:
            raise ValueError(
                f"Expected exactly two numbers in '{text}', found {len(numbers)}"
            )

        return (numbers[0], numbers[1])

    async def navigate_to_next_page(self) -> None:
        next_button = self._page.locator("#toolbarViewerRight_knou #next")
        await next_button.click()
