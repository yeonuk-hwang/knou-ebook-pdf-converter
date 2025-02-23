import asyncio
import os

from src.browser import BrowserHandler
from src.ebook_parser import EbookParser
from src.ebook_service import EbookService
from src.images_to_pdf_service import ImagesToPDFService


def print_menu() -> None:
    print("\n=== 이북 캡처 및 PDF 생성 도구 ===")
    print("1. 이북 페이지 캡처")
    print("2. 캡처된 이미지로 PDF 생성")
    print("3. 종료")
    print("================================")


async def async_input(prompt: str) -> str:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, input, prompt)


async def capture_ebook() -> None:
    async with BrowserHandler() as handler:
        print("\n브라우저가 실행되었습니다.")
        print("1. 로그인을 진행해주세요.")
        print("2. 원하는 이북 페이지를 구 PDF 뷰어로 열어주세요.")

        _ = await async_input("모든 준비가 완료되면 Enter 키를 눌러주세요: ")

        pages = handler.context.pages
        ebook_viewer_page = next(
            (page for page in pages if EbookParser.is_ebook_viewer_page(page)), None
        )

        if ebook_viewer_page is None:
            raise LookupError("이북 뷰어 페이지를 찾을 수 없습니다.")

        parser = EbookParser(ebook_viewer_page)
        service = EbookService(page=ebook_viewer_page, parser=parser)
        captured_files = await service.capture_all_pages()

        print(f"\n캡처 완료! 총 {len(captured_files)}개의 파일이 저장되었습니다.")
        print("\n저장된 파일:")
        for file_path in captured_files:
            print(f"- {file_path}")

        print("\n다음 단계:")
        print("1. images 폴더에서 캡처된 이미지를 확인해주세요.")
        print(
            "2. 교과서는 'images/textbook' 폴더로, 워크북은 'images/workbook' 폴더로 분류해주세요."
        )
        print("3. 분류가 완료되면 메인 메뉴에서 'PDF 생성' 옵션을 선택해주세요.")


def create_pdf() -> None:
    print("\n=== PDF 생성 ===")

    # Check if required folders exist
    if not os.path.exists("images/textbook") or not os.path.exists("images/workbook"):
        print("\n오류: 'images/textbook'과 'images/workbook' 폴더가 필요합니다.")
        print("1. images 폴더의 파일들을 분류해주세요.")
        print("2. 교과서는 'images/textbook' 폴더로 이동")
        print("3. 워크북은 'images/workbook' 폴더로 이동")
        return

    images_to_pdf_service = ImagesToPDFService()

    print("\ntextbook PD를 생성합니다...")
    images_to_pdf_service.convert_images_to_pdf(
        "./images/textbook", "./output/textbook.pdf"
    )

    print("workbook PDF를 생성합니다...")
    images_to_pdf_service.convert_images_to_pdf(
        "./images/workbook", "./output/workbook.pdf"
    )

    print("\nPDF 생성이 완료되었습니다!")
    print("output 폴더에서 결과물을 확인해주세요:")
    print("- textbook.pdf")
    print("- workbook.pdf")


async def main() -> None:
    while True:
        print_menu()
        choice = await async_input("원하는 작업을 선택해주세요 (1-3): ")

        if choice == "1":
            try:
                await capture_ebook()
            except Exception as e:
                print(f"\n오류가 발생했습니다: {str(e)}")
        elif choice == "2":
            try:
                create_pdf()
            except Exception as e:
                print(f"\n오류가 발생했습니다: {str(e)}")
        elif choice == "3":
            print("\n프로그램을 종료합니다. 감사합니다!")
            break
        else:
            print("\n잘못된 선택입니다. 1-3 중에서 선택해주세요.")

        if choice in ["1", "2"]:
            _ = await async_input("\n메인 메뉴로 돌아가려면 Enter 키를 눌러주세요: ")


if __name__ == "__main__":
    asyncio.run(main())
