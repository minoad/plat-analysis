"""


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
from typing import Any, Protocol

import pytesseract  # pylint: disable=import-error
from PIL import Image, UnidentifiedImageError  # pylint: disable=import-error
from pypdf import PageObject, PdfReader  # pylint: disable=import-error
from pypdf._utils import ImageFile  # pylint: disable=import-error

from documentanalysis.errors import PDFPageError


class DocumentProcessor(Protocol):
    """
    Interface for a document processor.
    TODO: Should this be a path or a string?
    """

    def __init__(self, path: Path, logger: logging.Logger) -> None:
        """
        Initialize the processor with the given path and logger.
        """

    def ocr(self, image: Any) -> str:  # ImageFile
        """
        Perform OCR on an image.
        """
        return ""

    def process(self) -> list[str]:
        """
        Process a document and return the extracted text.
        """
        return [""]


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
    Get the pdf metadata for the document.
    Go through each page
        go through each image in page
            dict: image_name: text, for each image, extract text


    """

    def __init__(self, path: Path, logger: logging.Logger) -> None:
        self.path: Path = path
        self.logger = logger
        self.logger.info(f"Processing PDF: {path}")
        self.metadata = {}

    def ocr(self, image: ImageFile) -> dict[str, str]:
        """
        Perform OCR on an image.
        Save the text to the medatadata.
        """
        image_data = Image.open(io.BytesIO(initial_bytes=image.data))
        image_text = pytesseract.image_to_string(image_data)
        # self.metadata[image.name] = {'format': image.image.format, 'text': image_text}
        # return pytesseract.image_to_string(image_data)

        # Return the image data
        return {'format': image.image.format, 'text': image_text}

    def collect_pdf_images(self, page: PageObject) -> list[dict[str, Any]]:
        """
        Get image from self.image_data.data
        """
        image_data: list[str] = []
        try:
            for image in page.images:
                # self.metadata[image.name] = {'format': image.image.format_description}
                image_data.append(self.ocr(image))
        except NotImplementedError as e:
            error_message = f"Not implemented error on pages in pdf {self.path}: {e}"
            custom_exception = PDFPageError(error_message, self.path)
            self.logger.warning(custom_exception)
            image_data.append(error_message)
        except UnidentifiedImageError as e:
            error_message = f"UnidentifiedImageError error on pages in pdf {self.path}: {e}"
            custom_exception = PDFPageError(error_message, self.path)
            self.logger.warning(custom_exception)
            image_data.append(error_message)
        except struct.error as e:
            error_message = f"Unable to extract page_image due to a struct error {self.path}: {e}"
            custom_exception = PDFPageError(error_message, self.path)
            self.logger.error(custom_exception)
            image_data.append(error_message)
        # collect all of the imagedata into metadtata for the page.

        # TODO: This should be implemented as a list of dicts.
        # Add to the dict.  Things like character count.
        # maybe even some quick text analysis here.  percent of valid words, things like that
        # maybe include the error that was thrown.

        return image_data

    def collect_pdf_pages(self, pdf: PdfReader) -> list[str]:
        """
        Collects pages from the pdf document.

        """
        print(self.metadata)
        page_data = []
        for page in pdf.pages:
            # TODO: This is returning empty lists in some cases, deal with it here.
            # should record something.
            page_data.append(self.collect_pdf_images(page))

        self.metadata['pdf_pages'] = page_data
        return self.metadata['pdf_pages']

    def process(self) -> dict[str, Any]:
        """
        PDFProcessor process method
        1. Collects pages from the pdf document.
        1. Collects images from each page.
        1. OCR's the images.
        1. Returns the OCR'd text for each page.
        
        ## TODO!!! Get the text extract going here
        ## look at textacy
        ## Text classifier using nlp

        # TODO: How do i know if this is a searchable doc?
        """
        pdf_file = PdfReader(stream=self.path)
        self.metadata['path'] = str(self.path)
        self.metadata['pdf_file_metadata'] = pdf_file.metadata
        self.collect_pdf_pages(pdf_file)

        return self.metadata
