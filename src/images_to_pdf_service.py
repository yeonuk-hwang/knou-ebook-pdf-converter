from abc import ABC, abstractmethod
from io import BytesIO
from pathlib import Path

import img2pdf
from typing_extensions import override

from src.ocr_service import OCRService


class PDFConverter(ABC):
    @abstractmethod
    def convert(self, image_paths: list[Path]) -> BytesIO:
        pass

    def get_image_files(self, folder_path: Path) -> list[Path]:
        return sorted(
            (f for f in folder_path.iterdir() if f.suffix.lower() == ".png"),
            key=lambda x: int(x.stem),
        )


class Img2PDFConverter(PDFConverter):
    @override
    def convert(self, image_paths: list[Path]) -> BytesIO:
        pdf_bytes = img2pdf.convert([str(p) for p in image_paths])

        if pdf_bytes is None:
            raise ValueError()

        pdf_buffer: BytesIO = BytesIO(pdf_bytes)
        return pdf_buffer


class ImagesToPDFService:
    def __init__(
        self,
        converter: PDFConverter | None = None,
        ocr_service: OCRService | None = None,
    ):
        self.converter: PDFConverter = converter or Img2PDFConverter()
        self.ocr_service: OCRService = ocr_service or OCRService()

    def convert_images_to_pdf(
        self, image_directory: str | Path, output_filename: str | Path
    ) -> None:
        image_dir = Path(image_directory)

        if not image_dir.is_dir():
            raise FileNotFoundError(f"Directory not found: {image_directory}")

        image_files = self.converter.get_image_files(image_dir)

        if not image_files:
            raise ValueError(f"No supported image files found in {image_directory}")

        print(f"Converting {len(image_files)} images to PDF...")
        pdf_bytes: BytesIO = self.converter.convert(image_files)

        print("Applying OCR to make the PDF searchable...")
        searchable_pdf_bytes: BytesIO = self.ocr_service.make_searchable_pdf(pdf_bytes)

        output_path = Path(output_filename)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "wb") as pdf_file:
            _ = pdf_file.write(searchable_pdf_bytes.read())

        print(f"PDF created successfully: {output_path}")
