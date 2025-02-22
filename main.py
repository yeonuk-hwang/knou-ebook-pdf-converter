import asyncio

from src.browser import BrowserHandler
from src.ebook_parser import EbookParser
from src.ebook_service import EbookService


async def async_input(prompt: str) -> str:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, input, prompt)


async def main() -> None:
    async with BrowserHandler() as handler:
        print("브라우저가 실행되었습니다.")
        print("원하는 페이지로 이동한 후, Enter 키를 눌러주세요.")

        _ = await async_input("준비가 되면 Enter 키를 눌러주세요: ")

        pages = handler.context.pages
        ebook_viewer_page = next(
            (page for page in pages if EbookParser.is_ebook_viewer_page(page)), None
        )

        if ebook_viewer_page is None:
            raise LookupError("No ebook viewer page found")

        parser = EbookParser(ebook_viewer_page)
        service = EbookService(page=ebook_viewer_page, parser=parser)
        captured_files = await service.capture_all_pages()

        print(f"\n캡처 완료! 총 {len(captured_files)}개의 파일이 저장되었습니다.")
        for file_path in captured_files:
            print(f"- {file_path}")


import easyocr

if __name__ == "__main__":
    reader = easyocr.Reader(["ko", "en"])

    with open("./images/489.png", "rb") as f:
        img = f.read()
        result = reader.readtext(img, detail=0)
        print(result)
    # asyncio.run(main())
