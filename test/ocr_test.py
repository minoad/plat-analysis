from pathlib import Path
#from pytest_mock import mocker

import pytest

from plat.ocr import PlatPage, PlatDocument  # replace with your actual module


def test_image_path(mocker):
    # Arrange
    mocker.patch('plat.ocr.PlatPage.image_directory', new=Path("/test/directory"))
    mocker.patch('plat.ocr.PlatPage.image_data', new=["test_image.jpg"])
    ocr_instance = PlatPage(file=Path("plat/data/grand_mesa/GM 5 Lot 170.pdf"), page_num=0, image_data="",
                            image_directory=Path("/test/directory"))
    
    # Act
    result = ocr_instance.image_path

    # Assert
    assert result == Path("/test/directory/test_image.jpg")
    
def test_plat_document():
    # Arrange
    plat_document = PlatDocument(location="plat/data/grand_mesa/GM 5 Lot 170.pdf", pages=[1, 2, 3])

    # Act
    file = plat_document.file
    pages = plat_document.pages

    # Assert
    assert file == Path("plat/data/grand_mesa/GM 5 Lot 170.pdf")
    assert pages == [1, 2, 3]