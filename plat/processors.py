"""
+-------------------+      +-------------------+      +-------------------+
|   PDFProcessor    |      |   PdfReader       |      |   PageObject      |
|-------------------|      |-------------------|      |-------------------|
| - ocr()           |<-----| - pages           |<-----| - images          |
| - collect_pdf_images()   |                   |      |                   |
| - collect_pdf_pages()    |                   |      |                   |
| - process()       |      |                   |      |                   |
+-------------------+      +-------------------+      +-------------------+
        ^                         ^                         ^
        |                         |                         |
        |                         |                         |
+-------------------+      +-------------------+      +-------------------+
| DocumentProcessor |      |   Path            |      |   ImageFile       |
|-------------------|      |-------------------|      |-------------------|
| - ocr()           |      | - stream          |<-----| - data            |
| - process()       |      |                   |      |                   |
+-------------------+      +-------------------+      +-------------------+

This module defines the interfaces and classes for processing documents.

It includes the following:

- `DocumentProcessor`: An interface (protocol) for document processors. It defines two methods:
  - `ocr`: Perform OCR on an image.
  - `process`: Process a document and return the extracted text.

- `PDFProcessor`: A class for processing PDF documents.
    It implements the `DocumentProcessor` interface and provides the following methods:
  - `ocr`: Perform OCR on an image and return the extracted text.
  - `collect_pdf_images`: Extract images from a PDF page and perform OCR on each image.
  - `collect_pdf_pages`: Extract pages from a PDF document and collect the OCR'd text from each page.
  - `process`: Given the path to a PDF document, return a list of OCR'd text for each page.

This module is part of the plat project, which is used for processing plat documents.
"""

import io
import logging
import struct
from pathlib import Path
from typing import Protocol, Any

import pytesseract  # pylint: disable=import-error
from PIL import Image  # pylint: disable=import-error
from pypdf import PageObject, PdfReader  # pylint: disable=import-error
from pypdf._utils import ImageFile  # pylint: disable=import-error

from plat.errors import PDFPageError


class DocumentProcessor(Protocol):
    """
    Interface for a document processor.
    TODO: Should this be a path or a string?
    """

    def __init__(self, path: Path, logger: logging.Logger) -> None:
        """
        Initialize the processor with the given path and logger.
        """

    def ocr(self, image: Any) -> str: # ImageFile
        """
        Perform OCR on an image.
        """

    def process(self) -> list[str]:
        """
        Process a document and return the extracted text.
        """


class PNGProcessor(DocumentProcessor):
    """
    Interface for a document processor.
    TODO: Should this be a path or a string?
    """

    def __init__(self, path: Path, logger: logging.Logger) -> None:
        """
        Initialize the processor with the given path and logger.
        """
        self.path: Path = path
        self.logger = logger
        self.logger.info(f"Processing PDF: {path}")

    def ocr(self, image: Any) -> str:
        """
        Perform OCR on an image.
        """
        return pytesseract.image_to_string(image)

    def process(self) -> list[str]:
        """
        Process a document and return the extracted text.
        """
        return [self.ocr(Image.open(str(self.path)))]


class PDFProcessor(DocumentProcessor):
    """
    Processor for PDF documents.
    PDF Documents store pages and within pages they store images.
    Accepts a path to a pdf document.
    Returns a list of strings, one for each page.
    """

    def __init__(self, path: Path, logger: logging.Logger) -> None:
        self.path: Path = path
        self.logger = logger
        self.logger.info(f"Processing PDF: {path}")

    def ocr(self, image: ImageFile) -> str:
        """
        Perform OCR on an image.
        """
        image_data = Image.open(io.BytesIO(initial_bytes=image.data))
        return pytesseract.image_to_string(image_data)

    def collect_pdf_images(self, page: PageObject) -> str:
        """
        Get image from self.image_data.data
        """
        ocr_text: list[str] = []
        try:
            for image in page.images:
                ocr_text.append(self.ocr(image))
        except NotImplementedError as e:
            error_message = f"Not implemented error on pages in pdf {self.path}: {e}"
            custom_exception = PDFPageError(error_message, self.path)
            self.logger.warning(custom_exception)
            return ""
        except struct.error as e:
            error_message = f"Unable to extract page_image due to a struct error {self.path}: {e}"
            custom_exception = PDFPageError(error_message, self.path)
            self.logger.error(custom_exception)
            return ""

        return "\n".join(ocr_text)

    def collect_pdf_pages(self, pdf: PdfReader) -> list[str]:
        """
        Collects pages from the pdf document.

        """
        return [self.collect_pdf_images(i) for i in pdf.pages]

    def process(self) -> list[str]:
        """
        PDFProcessor process method
        1. Collects pages from the pdf document.
        1. Collects images from each page.
        1. OCR's the images.
        1. Returns the OCR'd text for each page.
        """
        return self.collect_pdf_pages(PdfReader(stream=self.path))
