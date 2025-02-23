import re

from playwright.async_api import Page


class EbookParser:
    def __init__(self, page: Page) -> None:
        self._page: Page = page

    async def get_total_pages(self) -> int:
        page_text = await self._get_page_indicator_text()

        total: int | None = re.findall(r"of (\d+)", page_text)[0]

        print(total)

        if total is None:
            raise LookupError("eBook Viewer의 총 페이지 수를 찾는데 실패했습니다.")

        return int(total)

    async def navigate_to_next_page(self) -> None:
        next_button = self._page.locator("#toolbarViewerRight_knou #next")
        await next_button.click()

    async def set_page_fit_scale(self) -> None:
        _ = await self._page.select_option("select#scaleSelect", "page-fit")

    @staticmethod
    def is_ebook_viewer_page(page: Page) -> bool:
        ebook_viewer_base_url = "https://press.knou.ac.kr/common/supportPdfViewer.do"
        result: bool = page.url.startswith(ebook_viewer_base_url)
        return result

    async def _get_page_indicator_text(self) -> str:
        """Get the text content of the page indicator element."""
        page_indicator = self._page.locator(".toolbarPageMax")
        return str(await page_indicator.inner_text())
