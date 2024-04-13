"""
Scans plat documents and stores the resulting data
"""

import pathlib

import click

from plat.ocr import PlatDocument

TESTFILE: list[str] = [
    "plat/data/bluffs/201100030.pdf",
    "plat/data/bluffs/201100031.pdf",
    "plat/data/bluffs/201100043.pdf",
]

OCR_OUTPUT_PATH: str = "plat/data/ocr_output/"

# TODO: In test_small ensure one type of all errors.
# PLAT_DIR: str = "plat/data/plats_notes_sharepoint"
PLAT_DIR: str = "plat/data/bluffs"
# PLAT_DIR: str = "plat/data/grand_mesa"
# PLAT_DIR: str = "plat/data/HIGHLANDS/Highlands 3"
# PLAT_DIR: str = "plat/data/CAP ROCK"
# PLAT_DIR: str = "plat/data/test_small"


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
    plat_base_directory = pathlib.Path(PLAT_DIR)
    plat_files = []
    # TODO: Add file or folder detection

    for plat_dir in plat_base_directory.iterdir():
        if plat_dir.is_file():
            plat_files.append(plat_dir)
    plat_results: list[PlatDocument] = [PlatDocument(
        location=plat, ocr_output_path=OCR_OUTPUT_PATH) for plat in plat_files]
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
