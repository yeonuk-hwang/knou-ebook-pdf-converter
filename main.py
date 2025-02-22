import asyncio

from src.browser import BrowserHandler
from src.ebook_parser import EbookParser
from src.ebook_service import EbookService


async def async_input(prompt: str) -> str:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, input, prompt)


async def main() -> None:
    async with BrowserHandler() as handler:
        # 사용자에게 안내 메시지 출력
        print("브라우저가 실행되었습니다.")
        print("원하는 페이지로 이동한 후, Enter 키를 눌러주세요.")

        # 사용자가 Enter 키를 누를 때까지 대기
        await async_input("준비가 되면 Enter 키를 눌러주세요: ")

        page = handler.page

        # 현재 페이지에서 스크린샷 캡처 시작
        parser = EbookParser(page)
        service = EbookService(page=page, parser=parser)
        captured_files = await service.capture_all_pages()

        print(f"\n캡처 완료! 총 {len(captured_files)}개의 파일이 저장되었습니다.")
        for file_path in captured_files:
            print(f"- {file_path}")


if __name__ == "__main__":
    asyncio.run(main())
