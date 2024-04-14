"""
This module contains tests for the PDFProcessor class from the plat.processors module.

It includes the following tests:

- test_pdf_processor: This test function creates an instance of the PDFProcessor class,
    processes a test PDF file, and checks if the result is a list of strings.

The tests in this module use the pytest framework. Logging is configured to write messages
to a file named 'pytest_processor.log' with a level of INFO.

Test files are defined in the TEST_FILES list. Currently, it includes one test file located
at 'plat/data/test_small/201100030.pdf'.
"""

import logging
from pathlib import Path

import pytest  # type: ignore

from documentanalysis.processors import PDFProcessor

TEST_FILES = ["plat/data/test_small/201100030.pdf"]

logger: logging.Logger = logging.getLogger(name=__name__)
logging.basicConfig(filename="pytest_processor.log", encoding="utf-8", level=logging.INFO)


def test_pdf_processor():
    """
    Test the PDFProcessor class.
    """

    # Path to a test PDF file
    test_pdf_path = Path(TEST_FILES[0])

    # Process the test PDF file
    result = PDFProcessor(test_pdf_path, logger).process()

    # Check if the result is a list
    assert isinstance(result, list)

    # Check if all elements in the list are strings
    for element in result:
        assert isinstance(element, str)
