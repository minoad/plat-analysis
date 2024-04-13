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


class PlatPageImageError(Exception):
    """ Exception in case of no pages in PDF"""

    def __init__(self, message, image_data_type, image_path):
        self.image_data_type = image_data_type
        self.image_path = image_path
        super().__init__(f"{message}. Image data type: {image_data_type}, Image path: {image_path}")


class PlatFileTypeError(Exception):
    """
    Exception in case of no pages in PDF
    raise with raise PDFNoPagesError("Some error message", self.file_path) from e
    """

    def __init__(self, message, file_path):
        self.file_path = file_path
        super().__init__(f"{message}. File path: {file_path}")
