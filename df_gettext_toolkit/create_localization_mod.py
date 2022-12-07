from pathlib import Path

import typer
from loguru import logger


def parse_file(file_path: Path):
    ...


# def main(raws_path: Path, pot_file: typer.FileTextWrite, source_encoding: str = "cp437"):
def main(vanilla_path: Path):
    for directory in vanilla_path.glob("vanilla_*"):
        if directory.is_dir():
            objects = directory / "objects"
            if objects.exists():
                for file in objects.glob("*.txt"):
                    if file.is_file():
                        logger.info(file)
                        parse_file(file)


if __name__ == "__main__":
    typer.run(main)
