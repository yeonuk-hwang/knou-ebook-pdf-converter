# KNOU eBook to PDF Converter

[한국어 README](README.ko.md)

A tool to convert KNOU (Korea National Open University) eBook Viewer content into searchable PDFs with OCR (Optical Character Recognition).

## Features

- Automated eBook page capture
- OCR-based text extraction
- Searchable PDF generation

## ⚠️ Legal Notice

**This tool is intended for personal learning purposes only.**

- Unauthorized distribution or commercial use of captured content is prohibited under copyright law.
- Use beyond personal learning purposes may result in legal consequences.
- Users are solely responsible for all legal implications arising from the use of captured content.

## Installation

### 1. Prerequisites

- [uv](https://docs.astral.sh/uv/): Python package manager

### 2. Install uv

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

For detailed installation instructions, refer to the [uv official documentation](https://docs.astral.sh/uv/getting-started/installation/).

### 3. Project Setup

```bash
# Clone the repository
git clone https://github.com/yeonuk-hwang/knou-ebook-pdf-converter.git
cd knou-ebook-pdf-converter

# Create virtual environment and install dependencies
uv sync --frozen

# Install Playwright browsers
uv run playwright install
```

## Usage

```bash
uv run main.py
```

## How to Use

### Basic Workflow

1. After running the program, log in to the KNOU eBook site in the automatically opened browser.
2. Select the desired textbook and **open it using the old PDF viewer**.
3. Choose your desired operation from the main menu:
   - 1: Capture eBook pages - Automatically captures all pages of the currently opened textbook
   - 2: Generate PDF from captured images - Creates a searchable PDF with OCR processing
   - 3: Exit

### Step-by-Step Process

1. First, capture all pages using option 1.
2. Organize captured pages into folders: `images/textbook` for textbooks and `images/workbook` for workbooks.
3. Once organized, generate the PDF using option 2.
4. The generated PDF will be available in the `output` folder.

## Important Notes

### Before Use

- You must open the eBook using the old PDF viewer (new viewer is not supported)

### File Management

- Captured images are automatically saved in the `images` folder
- Final PDFs are generated in the `output` folder

### OCR Related

- Recognition accuracy may be lower compared to commercial OCR tools
- Always cross-check important content with the original source

## Technical Decisions

This project involved several key technical decisions to balance automation, usability, and maintainability:

### Browser Automation

- **Headed mode instead of headless**: Since users need to log in with their own credentials and select specific eBooks, the browser runs in headed (visible) mode. This approach prioritizes flexibility over background operation.
- **Playwright over Puppeteer**: Chose Playwright for its intuitive locators (`getByRole`, `getByText`) and better developer experience with the Playwright Inspector.

### Viewer Selection

- **Old PDF viewer required**: The new eBook viewer displays content in two-page mode, which complicates screenshot processing. The old PDF viewer's single-page mode provides cleaner, more consistent captures.

### OCR Engine

- **PaddleOCR**: Selected based on community feedback and performance comparisons. Implemented with an abstraction layer to allow future switching between OCR engines (EasyOCR, Tesseract, etc.) without major refactoring.

### Architecture

- **Separation of concerns**: The tool separates capture and PDF generation into distinct steps, allowing users to organize images before processing and enabling manual intervention if needed.

For detailed decision rationale and technical specifications, see [specification.md](specification.md).

## Troubleshooting

- If you encounter browser launch errors, try reinstalling browsers with: `playwright install`

## Contributing

- Bug reports and feature suggestions are welcome via Issues

## License

This project is licensed under the MIT License.
