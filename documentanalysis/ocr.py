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
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from documentanalysis.errors import FileTypeError
from documentanalysis.processors import DocumentProcessor, PDFProcessor, PNGProcessor
from documentanalysis.store import StoreWriter


@dataclass()
class Document:
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

    .save(
        ,
        obj={"name": "John", "address": "Highway 37"}
    )
    """

    location: Path
    logger: logging.Logger
    processor: DocumentProcessor = field(init=False)
    writers: list[StoreWriter]

    def __post_init__(self) -> None:
        """
        Construct path
        Dispatch file processing
        """
        self.process_file()

    def write_ocr_text(self, ocr_text) -> None:
        """
        Write out the ocr'd text results
        """
        if ocr_text and len("\n".join(ocr_text)) > 0:
            for writer in self.writers:
                writer.save({"file": str(self.location), "text": "\n".join(ocr_text)}, logger=self.logger)

    def write_metadata_text(self, metadata: dict[str, Any]) -> None:
        """
        Write out the ocr'd text results
        """
        if metadata:
            for writer in self.writers:
                writer.save(metadata, logger=self.logger)

    def process_file(self) -> None:
        """
        process the file
        """
        if self.location.suffix.lower() == ".pdf":
            self.processor = PDFProcessor(path=self.location, logger=self.logger)
            # self.write_ocr_text(self.processor.process())
            self.processor.process()
            self.write_metadata_text(self.processor.metadata)
            return
        if self.location.suffix.lower() == ".png":
            self.processor = PNGProcessor(path=self.location, logger=self.logger)
            # self.write_ocr_text(self.processor.process())
            self.processor.process()
            self.write_ocr_text(self.processor.process())
            # self.write_metadata_text(self.processor.metadata)
            return
        error_message: str = (
            f"File type {self.location.suffix.lower()} not implemented for plat analysis {self.location}"
        )
        custom_exception = FileTypeError(error_message, self.location)
        self.logger.warning(custom_exception)
