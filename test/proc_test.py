"""
processor_test.py
-----------------

This module contains the test suite for the `PDFProcessor` class in the `png` module. 

It uses the pytest framework to define and run the tests. The tests cover the `convert` and `close` methods of the `PDFProcessor` class.

Functions:
    test_convert_to_image: Tests that the `convert` method correctly converts a PDF to a list of images.
    test_convert_to_text: Tests that the `convert` method correctly converts a PDF to a string of text.
    test_close: Tests that the `close` method correctly closes the PDF document.
"""
import logging
from typing import Any

import pytest

from documentanalysis.png import PDFProcessorNew

logger: logging.Logger = logging.getLogger(name=__name__)
logging.basicConfig(
    filename="plat_text_extract.log",
    encoding="utf-8",
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

TESTS: dict[str, dict[str, Any]] = {
    "test_single_ccr_extract_text": {
        "path": "test/test_files/AR Dec - Bluffs v01 copy.pdf",
        "logger": logger,
        "expect_type": dict, 
    },
    "test_multiple_ccr": {
        "path": "documentanalysis/data/ccrs/",
        "logger": logger,
    },
}


def test_text_extract(test_name: str, test: dict[str, Any]):
    """
    Test the text extraction functionality of the PDFProcessorNew class.

    Args:
        test_name (str): The name of the test.
        test (dict[str, Any]): The test parameters.

    Returns:
        None
    """
    pdf = PDFProcessorNew(test["path"], test["logger"])
    pdf.extract_text()
    assert isinstance(pdf.metadata, test['expect_type'])
    print('a')
    # assert isinstance(converted_doc, list)
    # assert all(isinstance(image, Image.Image) for image in converted_doc)


# def test_convert_to_text(test_name: str, test: dict[str, Any]) -> None:
#     processor = PDFProcessorNew('path_to_test_pdf', 'logger')
#     converted_doc = processor.convert('text')
#     assert isinstance(converted_doc, str)

# def test_close(test_name: str, test: dict[str, Any]) -> None:
#     processor = PDFProcessorNew('path_to_test_pdf', 'logger')
#     processor.close()
#     assert processor.document.is_closed


def test_main():

    for test_name, test in TESTS.items():
        test_text_extract(test_name, test)

        


if __name__ == '__main__':
    test_main()
