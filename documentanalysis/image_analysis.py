import sys
from pathlib import Path

import cv2 as cv
import PIL
from matplotlib import pyplot as plt
from numpy import dtype, generic, ndarray

IMAGE_DIR: Path = Path("plat/data/image_analysis/")
IMAGE_FILES: list[Path] = list(IMAGE_DIR.iterdir())
BLUE: list[int] = [255, 0, 0]

# def extract_color_from_image(path: Path|str, color: str) -> ndarray:
#     """
#     Given the path to an image, extract only the specified color.
#     """


def load_image(path: Path | str) -> ndarray:
    if isinstance(path, str):
        path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    return cv.imread(str(path))


def main() -> int:
    img1 = load_image(IMAGE_FILES[2])

    cv.imshow("img", img1)
    cv.waitKey(15)
    # b, g, r = cv.split(img1)
    replicate = cv.copyMakeBorder(img1, 10, 10, 10, 10, cv.BORDER_REPLICATE)
    reflect = cv.copyMakeBorder(img1, 10, 10, 10, 10, cv.BORDER_REFLECT)
    reflect101 = cv.copyMakeBorder(img1, 10, 10, 10, 10, cv.BORDER_REFLECT_101)
    wrap = cv.copyMakeBorder(img1, 10, 10, 10, 10, cv.BORDER_WRAP)
    constant = cv.copyMakeBorder(img1, 10, 10, 10, 10, cv.BORDER_CONSTANT, value=BLUE)

    _ = plt.subplot(231), plt.imshow(img1, "gray"), plt.title("ORIGINAL")
    _ = plt.subplot(232), plt.imshow(replicate, "gray"), plt.title("REPLICATE")
    _ = plt.subplot(233), plt.imshow(reflect, "gray"), plt.title("REFLECT")
    _ = plt.subplot(234), plt.imshow(reflect101, "gray"), plt.title("REFLECT_101")
    _ = plt.subplot(235), plt.imshow(wrap, "gray"), plt.title("WRAP")
    _ = plt.subplot(236), plt.imshow(constant, "gray"), plt.title("CONSTANT")
    plt.show()
    return 0


if __name__ == "__main__":
    sys.exit(main())
