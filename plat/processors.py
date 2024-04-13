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
from pathlib import Path
from typing import Protocol

import pytesseract
from PIL import Image
from pypdf import PageObject, PdfReader
from pypdf._utils import ImageFile


class DocumentProcessor(Protocol):
    """
    Interface for a document processor.
    TODO: Should this be a path or a string?
    """

    def ocr(self, image: ImageFile) -> str:
        """
        Perform OCR on an image.
        """

    def process(self, path: Path, logger: logging.Logger) -> list[str]:
        """
        Process a document and return the extracted text.
        """


class PDFProcessor(DocumentProcessor):
    """
    Processor for PDF documents.
    PDF Documents store pages and within pages they store images.
    Accepts a path to a pdf document.
    Returns a list of strings, one for each page.
    """

    def ocr(self, image: ImageFile) -> str:
        """
        Perform OCR on an image.
        """
        image_data = Image.open(io.BytesIO(image.data))
        return pytesseract.image_to_string(image_data)

    def collect_pdf_images(self, page: PageObject) -> str:
        """
        Get image from self.image_data.data
        """

        return '\n'.join([self.ocr(image) for image in page.images])

    def collect_pdf_pages(self, pdf: PdfReader) -> list[str]:
        """
        Collects pages from the pdf document.

        """
        return [self.collect_pdf_images(i) for i in pdf.pages]

    def process(self, path: Path, logger: logging.Logger) -> list[str]:
        """
        Given the path to a pdf document, return a list of ocr'd text for each page.
        """
        logger.info(f"Processing PDF: {path}")

        return self.collect_pdf_pages(PdfReader(stream=path))
