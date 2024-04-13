"""
Given a url or a path to a file, return an object that represents the document
including extracted text.

+-------------------+     +-------------------+
|   PlatDocument    |     |     PlatPage      |
|-------------------|     |-------------------|
| - location        |     | - file            |
| - pages           |     | - page_num        |
|-------------------|     | - image_data      |
| + plat_path       |     | - image_directory |
| + image_directory |     | - write_image     |
| + ocr_output_path |     |-------------------|
| + __post_init__   |     | + image_path      |
| + write_ocr_text  |     | + image_path.setter |
| + process_file    |     | + __post_init__   |
| + process_pdf     |     | + write_images    |
+-------------------+     | + image_string    |
                          +-------------------+
"""

import logging
from dataclasses import dataclass
from pathlib import Path

from plat.errors import PlatFileTypeError
from plat.processors import PDFProcessor

logger: logging.Logger = logging.getLogger(name=__name__)
logging.basicConfig(filename="plat_text_extract.log", encoding="utf-8", level=logging.INFO)


@dataclass()
class PlatDocument:
    """
    A class to represent a document for Optical Character Recognition (OCR) processing.

    Attributes:
    location (Path): The path to the document file.
    ocr_output_path (str): The path where the OCR results should be written.

    Methods:
    __post_init__: A special method in Python dataclasses that's called after the class is fully initialized.
                   It calls the process_file method to start processing the file.
    write_ocr_text: Writes the OCR results to a file. It first ensures that the directory for the output file exists,
                    then writes the OCR results to the output file.
    """

    location: Path
    ocr_output_path: str

    def __post_init__(self) -> None:
        """
        Construct path
        Dispatch file processing
        """

        self.process_file()

    def write_ocr_text(self) -> None:
        """
        Write out the ocr'd text results
        """
        Path(self.ocr_output_path).mkdir(parents=True, exist_ok=True)
        if self.ocr_text and len("\n".join(self.ocr_text)) > 0:
            logger.info("writing ocr text for %s to %s", self.location, self.ocr_output_path)
            with open(f"{Path(self.ocr_output_path)/self.location.stem}_ocr.txt", mode="w", encoding="utf8") as fp:
                fp.write("\n".join(self.ocr_text))

    def process_file(self) -> None:
        """
        process the file
        """
        if self.location.suffix.lower() == ".pdf":
            self.processor = PDFProcessor()
            self.ocr_text: list[str] = self.processor.process(path=self.location, logger=logger)
            self.write_ocr_text()
        else:
            error_message: str = (
                f"File type {self.location.suffix.lower()} not implemented for plat analysis {self.location}"
            )
            custom_exception = PlatFileTypeError(error_message, self.location)
            logger.warning(custom_exception)
