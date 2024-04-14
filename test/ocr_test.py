import logging
from pathlib import Path

import pytest # noqa: F401 # pylint: disable=unused-import # type: ignore 

from documentanalysis.ocr import Document, PDFProcessor

logger: logging.Logger = logging.getLogger(name=__name__)
logging.basicConfig(
    filename="plat_text_extract.log", encoding="utf-8", level=logging.INFO,
    format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S'
)

TEST_FILES = ["plat/data/test_small/201100030.pdf"]


def test_process_file() -> None:
    """
    Test the process_file method of the Document class.

    This function tests the processing of a file using the process_file method of the Document class.  It asserts that 
    the processor attribute of the Document object is an instance of PDFProcessor after processing a PDF file,
    and that the ocr_text attribute is a list after processing any file.

    Returns:
        None
    """
    # Setup
    test_file = Path(TEST_FILES[0])  # replace with path to a test PDF file
    document = Document(location=test_file, ocr_output_path="plat/data/test_logger.log", logger=logger)

    # Test processing a PDF file
    document.process_file()
    assert isinstance(document.processor, PDFProcessor)
    assert isinstance(document.ocr_text, list)

    # Test processing a non-PDF file
    document.location = Path("/path/to/test.txt")  # replace with path to a non-PDF test file

    document.process_file()
