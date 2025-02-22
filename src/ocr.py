from pathlib import Path

from fpdf import FPDF
from PIL import Image


def get_image_files(folder_path: Path) -> list[Path]:
    """
    주어진 폴더에서 PNG 파일들의 경로를 반환합니다.
    """
    return sorted(
        [f for f in folder_path.iterdir() if f.suffix.lower() == ".png"],
        key=lambda x: x.stem,
    )


def create_pdf(image_folder: str | Path, output_pdf: str | Path) -> None:
    """
    PNG 이미지들을 PDF로 변환합니다.
    """
    image_folder_path = Path(image_folder)
    image_files = get_image_files(image_folder_path)

    if not image_files:
        print("No PNG images found in the folder.")
        return

    pdf = FPDF()

    for image_path in image_files:
        with Image.open(image_path) as img:
            width, height = img.size
            pdf.add_page()
            pdf.image(str(image_path), x=10, y=10, w=pdf.w - 20, h=pdf.h - 20)

    pdf.output(str(output_pdf))
    print(f"PDF has been created: {output_pdf}")


if __name__ == "__main__":
    image_folder = "images"
    output_pdf = "output.pdf"
    create_pdf(image_folder, output_pdf)
