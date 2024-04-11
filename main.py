from plat.ocr import doc, PlatDocument
import pathlib
import click

TESTFILE = ["plat/data/bluffs/201100030.pdf","plat/data/bluffs/201100031.pdf","plat/data/bluffs/201100043.pdf"]

@click.command()
@click.option('--count', default=1, help='Number of greetings.')
@click.option('--name', prompt='Your name',
              help='The person to greet.')
def hello(count, name):
    """Simple program that greets NAME for a total of COUNT times."""
    for x in range(count):
        click.echo(f"Hello {name}!")
        
# add file or folder detection
# TODO: Output to database
def main() -> int:
    """
    This is a docstring
    """
    #plat_dir = [str(i) for i in list(pathlib.Path('plat/data/bluffs').iterdir())]
    plat_base_directory = pathlib.Path('plat/data/plats_notes_sharepoint')
    plat_files = []
    for plat_dir in plat_base_directory.iterdir():
        if plat_dir.is_dir():
            for plat in plat_dir.iterdir():
                plat_files.append(plat)
    plat_dir = [str(i) for i in plat_files]
    #plat_dir = [str(i) for i in list(pathlib.Path('plat/data/grand_mesa').iterdir())]
    plats = [PlatDocument(i) for i in plat_dir]
    return 0

if __name__ == "__main__":
    main()

    
# Dev productivity
# cloud architecture
# networking
# observability
# finops 
# sre

# urashi
# alvero director manageing terraform
