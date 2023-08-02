from pathlib import Path

import typer


def convert(pofile, outfile, encoding):
    pass


app = typer.Typer()


@app.command()
def main(po_file: Path, csv_file: Path, encoding: str, append: bool = False):
    """
    Convert a po file into a csv file in a specified encoding
    """

    with open(po_file, "r", encoding="utf-8") as pofile:
        mode = "a" if append else "w"
        with open(csv_file, mode, newline="", encoding=encoding, errors="replace") as outfile:
            convert(pofile, outfile, encoding)


if __name__ == "__main__":
    app()
