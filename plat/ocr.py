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
import struct
from dataclasses import dataclass, field
from pathlib import Path

import pytesseract
from PIL import Image
from pypdf import PdfReader
from pypdf._utils import ImageFile

from plat.errors import OCRError, PDFPageError, PlatFileTypeError, PlatPageImageError

logger: logging.Logger = logging.getLogger(name=__name__)
logging.basicConfig(filename='plat_text_extract.log', encoding='utf-8', level=logging.INFO)


@dataclass()
class PlatPage:
    """
    Represents a single page of a plat document
    """
    file: Path
    page_num: int
    image_data: ImageFile
    image_directory: Path
    write_image: bool = True

    @property
    def image_path(self) -> Path:
        """
        infers image path.  This is where we are going to save the images.
        """
        try:
            image_path: Path = Path(self.image_directory) / self.image_data.name
        except OSError as e:
            logger.error("OSerror in attempting to extract image path: %s", e)
            raise OCRError("oserror extracting image_path", Path(self.image_directory)) from e
        return image_path

    @image_path.setter
    def image_path(self, value) -> None:
        self._image_path = Path(value)

    def __post_init__(self) -> None:
        if self.write_image:
            self.write_images()
        self._image_string = ""

    def write_images(self) -> None:
        """
        Write out the individual images
        """
        self.image_directory.mkdir(parents=True, exist_ok=True)
        if isinstance(self.image_data.data, bytes) and self.image_path:
            with open(self.image_path, "wb") as fp:
                fp.write(self.image_data.data)
                print(f"wrote: {self.image_path}")
        else:
            raise PlatPageImageError("image_data not bytes", type(self.image_data.data), self.image_path)

    @property
    def image_string(self) -> str:
        """
        Extract text from image
        Can pass a pil or a filename
        If no text can be extracted, set self.image_string to None
        """

        try:
            self._image_string: str = pytesseract.image_to_string(image=Image.open(fp=self.image_path))
        except AttributeError as e:
            logger.error("error extracting string from %s: %s", self.image_path, e)
            raise OCRError("oserror extracting image_path", Path(self.image_directory)) from e
        return self._image_string


@dataclass()
class PlatDocument:
    """
    Represents a single plat
    Check the location exists
    Extract and infer details about the file
        - plat_path: Path to the plat file
        - image_directory: Path to the directory where the images are stored
        - ocr_output_path: Path to the file where the ocr text is stored
    """

    location: str
    pages: list[PlatPage] = field(default_factory=list)

    @property
    def plat_path(self) -> Path:
        print('a')
        """
        Returns the inferred plat_path
        """
        if not Path(self.location).exists():
            logger.error("File %s not found", self.location)
            raise FileNotFoundError(f"File {self.location} not found")

        return Path(self.location)

    @property
    def image_directory(self) -> Path:
        """
        Returns the inferred image_directory
        """
        return self.plat_path.parent / self.plat_path.stem

    @property
    def ocr_output_path(self) -> Path:
        """
       Returns the inferred ocr_output_path
        """
        return self.image_directory / f"{self.image_directory.stem}_ocr_text.txt"

    def __post_init__(self) -> None:
        """
        Construct path
        Dispatch file processing
        """

        self.process_file()
        self.write_ocr_text()
        print("a")

    def write_ocr_text(self) -> None:
        """
        Write out the ocr'd text results
        """

        if self.pages:
            logger.info("writing ocr text for %s to %s", self.plat_path, self.ocr_output_path)
            with open(self.ocr_output_path, mode="w", encoding="utf8") as fp:
                fp.write('\n'.join(page.image_string for page in self.pages))
        else:
            logger.warning("No pages found in %s", self.plat_path)
            # raise PDFPageError("No pages found", self.plat_path)
            # custom_exception = PDFPageError(error_message, self.plat_path)

    def process_file(self) -> None:
        """
        process the file
        """
        if self.plat_path.suffix.lower() == ".pdf":
            # self.document_parser: DocumentProcessor = PDFProcessor()
            # self.document_parser.process(self.plat_path)
            self.process_pdf()
        else:
            error_message: str = (
                f"File type {self.plat_path.suffix.lower()} not implemented for plat analysis {self.plat_path}"
            )
            custom_exception = PlatFileTypeError(error_message, self.plat_path)
            logger.warning(custom_exception)

    def process_pdf(self) -> None:
        """
        Process if file is of type pdf
        """
        # try:
        # pdfstream when bad has page_layout and page_mode of none.
        pdf_stream = PdfReader(stream=self.plat_path)
        for i, page in enumerate(iterable=pdf_stream.pages):
            try:
                page_image: ImageFile = page.images[0]
                self.pages.append(
                    PlatPage(
                        file=self.plat_path,
                        page_num=i,
                        image_data=page_image,
                        image_directory=self.image_directory,
                    )
                )
            except IndexError as e:
                error_message = f"Index error on pages in pdf {self.plat_path}: {e}"
                custom_exception = PDFPageError(error_message, self.plat_path)
                logger.warning(custom_exception)
            except NotImplementedError as e:
                error_message = f"Not implemented error on pages in pdf {self.plat_path}: {e}"
                custom_exception = PDFPageError(error_message, self.plat_path)
                logger.warning(custom_exception)
            except struct.error as e:
                error_message = f"Unable to extract page_image due to a struct error {self.plat_path}: {e}"
                custom_exception = PDFPageError(error_message, self.plat_path)
                logger.error(custom_exception)
