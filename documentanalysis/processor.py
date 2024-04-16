"""
processor.py
------------

This module defines the `DocumentProcessor` protocol, which outlines the interface for a document processor. 

A document processor is responsible for extracting text, images, and font information from a document. The document can be of any type (e.g., an image, a PDF), and the appropriate extraction method is used depending on the document type.

Classes:
    DocumentProcessor: An interface for a document processor.

Methods defined in DocumentProcessor:
    extract_text: Extracts text from a document using the appropriate method.
    image_extraction: Extracts images from a document.
    font_extraction: Extracts font information from a document.
"""

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class DocumentProcessorNew(Protocol):

    """
    Interface for a document processor.
    """

    def extract_text(self) -> str:
        """
        Extract text from the document using the appropriate method
        (OCR for images, direct extraction for searchable PDFs).
        Parameters:
        doc: The document or image to extract text from.
        Returns:
        The extracted text as a string.
        """

    def image_extraction(self) -> list[Any]:
        """
        Extract images from the document.
        Parameters:
        doc: The document to extract images from.
        Returns:
        A list of extracted images.
        """
