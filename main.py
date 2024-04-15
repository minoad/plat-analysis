"""
Scans plat documents and stores the resulting data
"""

import logging
import pathlib
from pathlib import Path

import click

from documentanalysis.ocr import Document
from documentanalysis.secure import MONGODB_AUTHENTICATION
from documentanalysis.store import FileWriter, MongoWriter

TESTFILE: list[str] = [
    "documentanalysis/data/bluffs/201100030.pdf",
    "documentanalysis/data/bluffs/201100031.pdf",
    "documentanalysis/data/bluffs/201100043.pdf",
]

OCR_OUTPUT_PATH: str = "documentanalysis/data/ocr_output/"

# TODO: In test_small ensure one type of all errors.
# PLAT_DIR: str = "documentanalysis/data/srcs_notes_sharepoint"
# PLAT_DIR: str = "documentanalysis/data/test_small"
# PLAT_DIR: str = "documentanalysis/data/GRAND MESA"
# PLAT_DIR: str = "documentanalysis/all_plat_docs/"
# PLAT_DIR: str = "documentanalysis/data/HIGHLANDS/Highlands 3"
# PLAT_DIR: str = "documentanalysis/data/CAP ROCK"
# PLAT_DIR: str = "documentanalysis/data/test_small"
# PLAT_DIR: str = "documentanalysis/data/image_analysis"
# PLAT_DIR: str = "documentanalysis/data/ccrs"

dirs: dict[str, str] = {
    'plate_all_sharepoint': "documentanalysis/data/srcs_notes_sharepoint",
    'plat_test': "documentanalysis/data/test_small",
    'plat_grand_mesa': "documentanalysis/data/GRAND MESA",
    'plat_highlands_3': "documentanalysis/data/HIGHLANDS/Highlands 3",
    'plat_cap_rock': "documentanalysis/data/CAP ROCK",
    'generic_image_analysis': "documentanalysis/data/image_analysis",
    'ccrs_all': "documentanalysis/data/ccrs",
    'plat_test_all': "test/all_plat_docs",
}

logger: logging.Logger = logging.getLogger(name=__name__)
logging.basicConfig(
    filename="plat_text_extract.log", encoding="utf-8", level=logging.INFO,
    format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S'
)


@click.command()
@click.option("--count", default=1, help="Number of greetings.")
@click.option("--name", prompt="Your name", help="The person to greet.")
def hello(count, name):
    """Simple program that greets NAME for a total of COUNT times."""
    for x in range(count):
        click.echo(f"Hello {name} {x}!")


# add file or folder detection
# TODO: Output to database
def main() -> int:
    """
    Entry point of the program.
    This function iterates over the directories and files in the PLAT_DIR
    directory.
    It collects all the file paths and returns 0.
    Returns:
        int: The exit code of the program.
    """
    plat_base_directory = pathlib.Path(dirs['plat_test_all'])
    plat_files = []
    # TODO: Add file or folder detection

    for plat_dir in plat_base_directory.iterdir():
        if plat_dir.is_file():
            plat_files.append(plat_dir)
    plat_results: list[Document] = [
        Document(
            location=plat,
            logger=logger,
            writers=[
                FileWriter(
                    auth={},
                    path={'uri': str(Path(OCR_OUTPUT_PATH) / f"{plat.stem}.txt)").replace(' ', '')},
                ),
                MongoWriter(
                    auth=MONGODB_AUTHENTICATION,
                    path={'host': 'mongodb://mongo:27017/', 'dbname': 'hoa_docs', 'collection': 'ccrs'}
                ),
            ]
        ) for plat in plat_files
    ]
    print(len(plat_results))

    return 0


if __name__ == "__main__":
    print("begin")
    main()


# Dev productivity
# cloud architecture
# networking
# observability
# finops
# sre

# urashi
# alvero director manageing terraform
