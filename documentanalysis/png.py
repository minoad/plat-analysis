"""
png.py
-------

This module contains the `PDFProcessor` class, which is an implementation of the `DocumentProcessor` protocol for PDF files. 

The `PDFProcessor` uses the PyMuPDF library (imported as `fitz`) to handle PDF files. It provides functionality to open a PDF file, extract its metadata, and extract text from the document.

Classes:
    PDFProcessor: A class for processing PDF files.

Methods defined in PDFProcessor:
    __init__: Initializes the PDFProcessor with a path to a PDF file and a logger.
    extract_text: Extracts text from the PDF document using PyMuPDF.
"""

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Tuple

import fitz  # PyMuPDF

from documentanalysis.processor import DocumentProcessorNew


@dataclass
class PDFProcessorNew(DocumentProcessorNew):
    """
    PDFProcessor implementation using PyMuPDF (fitz) for PDF file handling.
    Implements the DocumentProcessor protocol.
    If no doc given during construction, load from method.

    Possibly add .convert() method to convert to other formats (e.g., text, image)
    add a context manager so i dont have to close()
    """
    path: Path = field(default_factory=Path)
    logger: logging.Logger = field(default_factory=logging.getLogger)

    def __post_init__(self) -> None:
        """
        Initialize the PDFProcessor with the given path and logger.
        """
        self.extracted_text_list = []
        self.logger.info(f"Processing PDF: {self.path}")
        self.document = fitz.open(self.path)
        self.metadata: Dict[str, Any] = dict(self.document.metadata)

        print('a')

    def extract_text(self) -> list[str]:
        """
        Extract text from the PDF document using PyMuPDF.

        Parameters:
            doc: PyMuPDF Document object (optional).

        Returns:
            The extracted text as a string.
        """

        extracted_text = []
        for page in self.document:
            extracted_text.append(page.get_text())

        self.metadata['text'] = '\n'.join(extracted_text)
        self.extracted_text_list = extracted_text

        return extracted_text

    def image_extraction(self, doc: Any = None) -> List[fitz.Pixmap]:
        """
        Extract images from the PDF document using PyMuPDF.

        Parameters:
            doc: PyMuPDF Document object (optional).

        Returns:
            A list of extracted images as PyMuPDF Pixmap objects.
        """
        # If a specific document is not provided, use the PDF document loaded during initialization.
        if doc is None:
            doc = self.document

        images = []
        for page_number in range(len(doc)):
            page = doc[page_number]
            # Iterate through each image in the page and create a Pixmap object.
            for img_index, img in enumerate(page.get_images(full=True)):
                xref = img[0]
                base_image = doc.extract_image(xref)
                img_data = base_image["image"]
                img_pixmap = fitz.open("png", img_data)
                images.append(img_pixmap)

        return images

    def close(self):
        """
        Close the PDF document.
        """
        self.document.close()
