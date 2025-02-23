from abc import ABC, abstractmethod
from io import BytesIO
from pathlib import Path

import img2pdf
from typing_extensions import override


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
    def __init__(self, converter: PDFConverter | None = None):
        self.converter: PDFConverter = converter or Img2PDFConverter()

    def convert_images_to_pdf(
        self, image_directory: str | Path, output_filename: str | Path | None
    ) -> BytesIO:
        image_dir = Path(image_directory)

        if not image_dir.is_dir():
            raise FileNotFoundError(f"Directory not found: {image_directory}")

        image_files = self.converter.get_image_files(image_dir)

        if not image_files:
            raise ValueError(f"No supported image files found in {image_directory}")

        print(f"Converting {len(image_files)} images to PDF...")

        result: BytesIO = self.converter.convert(image_files)

        if output_filename is not None:
            output_path = Path(output_filename)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            with open(output_path, "wb") as pdf_file:
                _ = pdf_file.write(result.read())
                _ = result.seek(0)

            print(f"PDF created successfully: {output_path}")

        return result
