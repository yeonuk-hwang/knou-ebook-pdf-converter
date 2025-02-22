# pyright: reportAny=false
from unittest.mock import MagicMock

import pytest
from playwright.sync_api import Locator, Page

from src.ebook_parser import EbookParser


@pytest.fixture
def mock_page() -> MagicMock:
    return MagicMock(spec=Page)


@pytest.fixture
def mock_locator() -> MagicMock:
    return MagicMock(spec=Locator)


@pytest.fixture
def parser(mock_page: MagicMock) -> EbookParser:
    return EbookParser(mock_page)


class TestCalculateTotalPages:
    def test_extracts_total_pages_from_page_text(
        self, parser: EbookParser, mock_page: MagicMock, mock_locator: MagicMock
    ) -> None:
        # Arrange
        mock_page.get_by_text.return_value = mock_locator
        mock_locator.inner_text.return_value = "1 of 464"

        # Act
        result = parser.calculate_total_pages()

        # Assert
        mock_page.get_by_text.assert_called_with(r"\(\d+ of \d+\)")
        mock_locator.inner_text.assert_called_once()
        assert result == 464


class TestIsLastPage:
    @pytest.mark.parametrize(
        "page_text,expected",
        [
            ("464 of 464", True),
            ("1 of 464", False),
            ("463 of 464", False),
        ],
    )
    def test_correctly_identifies_last_page(
        self,
        parser: EbookParser,
        mock_page: MagicMock,
        mock_locator: MagicMock,
        page_text: str,
        expected: bool,
    ) -> None:
        # Arrange
        mock_page.get_by_text.return_value = mock_locator
        mock_locator.inner_text.return_value = page_text

        # Act
        result = parser.is_last_page()

        # Assert
        assert result == expected


class TestNavigeToNextPage:
    def test_navigate_to_next_page(
        self, parser: EbookParser, mock_page: MagicMock, mock_locator: MagicMock
    ) -> None:
        mock_page.locator.return_value = mock_locator

        parser.navigate_to_next_page()

        mock_page.locator.assert_called_with("#toolbarViewerRight_knou #next")
        mock_locator.click.assert_called_once()
