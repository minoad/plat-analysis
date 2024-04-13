from pathlib import Path

import pytest

from plat.ocr import PDFProcessor, PlatDocument, PlatFileTypeError

TEST_FILES = ["plat/data/test_small/201100030.pdf"]


def test_process_file():
    # Setup
    test_file = Path(TEST_FILES[0])  # replace with path to a test PDF file
    ocr_output_path = "test/test_output"  # replace with path to output directory
    document = PlatDocument(location=test_file, ocr_output_path=ocr_output_path)

    # Test processing a PDF file
    document.process_file()
    assert isinstance(document.processor, PDFProcessor)
    assert isinstance(document.ocr_text, list)

    # Test processing a non-PDF file
    document.location = Path("/path/to/test.txt")  # replace with path to a non-PDF test file
    
    document.process_file()
