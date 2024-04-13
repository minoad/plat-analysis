import logging
from pathlib import Path

import pytest

from plat.processors import PDFProcessor

TEST_FILES = ["plat/data/test_small/201100030.pdf"]

logger: logging.Logger = logging.getLogger(name=__name__)
logging.basicConfig(filename="pytest_processor.log", encoding="utf-8", level=logging.INFO)


def test_pdf_processor():
    """
    Test the PDFProcessor class.
    """
    # Create an instance of PDFProcessor
    processor = PDFProcessor()

    # Path to a test PDF file
    test_pdf_path = Path(TEST_FILES[0])

    # Process the test PDF file
    result = processor.process(test_pdf_path, logger)

    # Check if the result is a list
    assert isinstance(result, list)

    # Check if all elements in the list are strings
    for element in result:
        assert isinstance(element, str)
