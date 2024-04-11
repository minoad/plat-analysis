from dataclasses import dataclass, field
import pathlib
import pytesseract
from pdf2image import convert_from_path
import tempfile
from pypdf import PdfReader
from typing import Any
from PIL import Image

"""
Given a url or a path to a file, return an object that represents the document including extracted text.
"""

IMAGE_PROC_DIR = pathlib.Path()

@dataclass()
class PlatPage:
    """
    Represents a single page of a plat document
    TODO: Automate file type
    """
    file: pathlib.Path
    page_num: int
    image_data: Any
    image_directory: pathlib.Path
    
    def __post_init__(self):
        self.write_images()
        self.ocr()
        
    def write_images(self):
        pathlib.Path(self.image_directory).mkdir(parents=True, exist_ok=True)
        try:
            for image in self.image_data:
                self.image_path = f"{self.image_directory}/{image.name}"
                with open(self.image_path, "wb") as fp:
                    fp.write(image.data)
                    print(f'wrote: {self.image_path}')
        except Exception as e:
            print(f"Error writing images: {e}")

    def ocr(self):
        """
        Extract text from image
        Can pass a pil or a filename
        """
        try:
            self.image_string = pytesseract.image_to_string(Image.open(self.image_path))
        except AttributeError as e:
            print(f"Error extracting text: {e}")


@dataclass()
class PlatDocument:
    """
    Represents a single plat
    Check the location exists
    Extract and infer details about the file
    
    TODO: Instead of saving out a temp file/folder, I think I can just do the tesseract ocr here
    TODO: Should have a platpage object that represents a single page
    """
    _location: str # TODO: add pathlib support|pathlib.Path
    
    def __post_init__(self):
        """
        Construct path
        Dispatch file processing
        """
        self.file = pathlib.Path(self._location) # TODO: Add this to the constructor of location
        self.image_directory = pathlib.Path(str(self.file).split('.')[0]) # TODO: Move this from pages to document
        if not self.file.exists():
            raise FileNotFoundError(f"File {self._location} not found")
        self.ocr_output_path = pathlib.Path(f"{self.image_directory}/{self.file.stem}_ocr_text.txt")

        self.process_file()
        self.write_ocr_text()
        print('a')

    def write_ocr_text(self):
        print(f'writing ocr text to {self.ocr_output_path}')
        try:
            with open(self.ocr_output_path, 'w') as fp:
                try:
                    for page in self.pages: # TODO: Seeing a lot of no x.pages().  deal with it here. writing ocr text to plat/data/plats_notes_sharepoint/FAIRWAYS/Fairways 1/Fairways 1_ocr_text.txt Error writing ocr text: 'PlatDocument' object has no attribute 'pages'
                        fp.write(page.image_string)
                        fp.write('\n')
                except AttributeError as e:
                    print(f"Error writing ocr text: {e}")
        except FileNotFoundError as e:
            print(f"Error writing ocr text: {e}")
        print('a')

    def process_file(self):
        if self.file.suffix == ".pdf":
            self.process_pdf()
                
    def process_pdf(self):
        self.pages = []
        for i, page in enumerate(PdfReader(self.file).pages):
            self.pages.append(PlatPage(file=self.file, page_num=i, image_data=page.images, image_directory=self.image_directory))

    

# TODO: Can i remove watermarks?

def doc():
    """
    This is a docstring
    """
    print("doc doc")
    return None