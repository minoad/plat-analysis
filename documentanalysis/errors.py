"""
This module defines custom exception classes for handling errors in the plat project.

It includes the following exception classes:

- OCRError: Raised when there's an error during Optical Character Recognition (OCR) processing.
    It includes the file path in the error message.

- PDFPageError: Raised when a PDF file has no pages. It includes the file path in the error message.

- PlatPageImageError: Raised when there's an error related to an image in a plat page.
    It includes the image data type and image path in the error message.

- PlatFileTypeError: Raised when there's an error related to the file type of a plat.
    It includes the file path in the error message.

Each exception class inherits from the built-in Exception class and adds additional context
to the error message, such as the file path or image data type.
"""


class OCRError(Exception):
    """
    Generic OCR Error
    raise with raise OCRError("Some error message", self.file_path) from e
    """

    def __init__(self, message, file_path):
        self.file_path = file_path
        super().__init__(f"{message}. File path: {file_path}")


class PDFPageError(Exception):
    """
    Exception in case of no pages in PDF
    raise with raise PDFNoPagesError("Some error message", self.file_path) from e
    """

    def __init__(self, message, file_path):
        self.file_path = file_path
        super().__init__(f"{message}. File path: {file_path}")


class PageImageError(Exception):
    """Exception in case of no pages in PDF"""

    def __init__(self, message, image_data_type, image_path):
        self.image_data_type = image_data_type
        self.image_path = image_path
        super().__init__(f"{message}. Image data type: {image_data_type}, Image path: {image_path}")


class FileTypeError(Exception):
    """
    Exception in case of no pages in PDF
    raise with raise PDFNoPagesError("Some error message", self.file_path) from e
    """

    def __init__(self, message, file_path):
        self.file_path = file_path
        super().__init__(f"{message}. File path: {file_path}")
