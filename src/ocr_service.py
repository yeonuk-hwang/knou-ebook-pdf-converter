from abc import ABC, abstractmethod
from io import BytesIO

import ocrmypdf
from ocrmypdf.pluginspec import get_ocr_engine
from typing_extensions import override


class OCREngine(ABC):
    @abstractmethod
    def process(self, input_pdf: BytesIO) -> BytesIO:
        pass


class EasyOCREngine(OCREngine):
    @override
    def process(self, input_pdf: BytesIO) -> BytesIO:
        output_buffer = BytesIO()

        _ = ocrmypdf.ocr(
            input_file=input_pdf,
            output_file=output_buffer,
            # NOTE: Somehow the easyocr plugin is automatically registered. Therefore, applying plugins with this options raise "Plugin already registered under a different name Error"
            # plugins=["ocrmypdf_easyocr"],
            pdf_renderer="sandwich",
            language=[
                "kor",
                "eng",
            ],
            # NOTE: language code reference: https://github.com/ocrmypdf/OCRmyPDF-EasyOCR/blob/fa5c168a3cd622c00ebe89a5f425ee4a9de7f093/ocrmypdf_easyocr/__init__.py#L37:L101
        )

        print(get_ocr_engine())

        _ = output_buffer.seek(0)
        return output_buffer


class OCRService:
    def __init__(self, engine: OCREngine | None = None):
        self.engine: OCREngine = engine or EasyOCREngine()

    def make_searchable_pdf(self, pdf_data: BytesIO) -> BytesIO:
        print("Converting PDF to searchable format...")
        return self.engine.process(pdf_data)
