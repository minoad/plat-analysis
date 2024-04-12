"""
Given a url or a path to a file, return an object that represents the document
including extracted text.
"""

import logging
from dataclasses import dataclass, field
from os import error
from pathlib import Path
from typing import Any

import pytesseract
from PIL import Image
from pypdf import PdfReader

IMAGE_PROC_DIR = Path()

logger: logging.Logger = logging.getLogger(name=__name__)
logging.basicConfig(filename='plat_text_extract.log', encoding='utf-8', level=logging.INFO)


@dataclass()
class PlatPage:
    """
    Represents a single page of a plat document
    TODO: Automate file type
    """
    # TODO: use properties to derive paths
    file: Path
    page_num: int
    image_data: Any  # TODO: Add type hint
    image_directory: Path
    write_image: bool = True

    @property
    def image_path(self) -> Path | None:
        """
        infers image path.  This is where we are going to save the images.
        """
        
        try:
            image_path = Path(
                f"{self.image_directory}/{self.image_data[0].name}") if self.image_data[0] else error("no image_data")
        except NotImplementedError as e:
            logger.error("Error extracting image path: %s", e)
            return None
        except OSError as e:
            logger.error("Error extracting image data, oserror: %s", e)
            return None

        return Path(image_path)

    @image_path.setter
    def image_path(self, value) -> None:
        self.image_path = Path(value)

    def __post_init__(self) -> None:
        if self.write_image:
            self.write_images()
        self.ocr()

    def write_images(self) -> None:
        """
        Write out the individual images
        """
        self.image_directory.mkdir(parents=True, exist_ok=True)
        if self.image_data and self.image_path:
            with open(self.image_path, "wb") as fp:
                fp.write(self.image_data[0].data)
                print(f"wrote: {self.image_path}")

    def ocr(self) -> None:
        """
        Extract text from image
        Can pass a pil or a filename
        """
        try:
            self.image_string = pytesseract.image_to_string(image=Image.open(fp=self.image_path))
        except AttributeError as e:
            logger.error("Error extracting text: %s", e)


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
        """
        Returns the inferred plat_path
        """
        return Path(self.location)

    @plat_path.setter
    def plat_path(self, value) -> None:
        if not Path(value).exists():
            logger.error("File %s not found", value)
            raise FileNotFoundError(f"File {value} not found")
        self.plat_path = Path(value)

    @property
    def image_directory(self) -> Path:
        """
        Returns the inferred image_directory
        """
        return Path(
            str(self.plat_path).split(sep=".", maxsplit=1)[0]
        )

    @image_directory.setter
    def image_directory(self, value) -> None:
        self.plat_path = Path(value)

    @property
    def ocr_output_path(self) -> Path:
        """
       Returns the inferred ocr_output_path
        """
        return Path(f"{self.image_directory}/{self.plat_path.stem}_ocr_text.txt")

    @ocr_output_path.setter
    def ocr_output_path(self, value) -> None:
        self.ocr_output_path = Path(value)

    def __post_init__(self) -> None:
        """
        Construct path
        Dispatch file processing
        """
        logger.info("processing file %s", self.plat_path)
        self.process_file()
        self.write_ocr_text()
        print("a")

    def write_ocr_text(self) -> None:
        """
        Write out the ocr'd text results
        """
        logger.info("writing ocr text for %s to %s", self.plat_path, self.ocr_output_path)
        with open(self.ocr_output_path, mode="w", encoding="utf8") as fp:
            try:
                for page in self.pages:  # TODO: Seeing a lot of no x.pages().
                    # deal with it here. writing ocr text to
                    # plat/data/plats_notes_sharepoint/FAIRWAYS/Fairways
                    # 1/Fairways 1_ocr_text.txt Error writing ocr text:
                    # 'PlatDocument' object has no attribute 'pages'
                    fp.write(page.image_string)
                    fp.write("\n")
            except AttributeError as e:
                logger.error("Error writing ocr text: %s", e)
        print("a")

    def process_file(self) -> None:
        """
        process the file
        """
        if self.plat_path.suffix == ".pdf":
            self.process_pdf()

    def process_pdf(self):
        """
        Process if file is of type pdf
        """
        for i, page in enumerate(iterable=PdfReader(stream=self.plat_path).pages):
            self.pages.append(
                PlatPage(
                    file=self.plat_path,
                    page_num=i,
                    image_data=page.images,
                    image_directory=self.image_directory,
                )
            )


# TODO: Can i remove watermarks?
