from pathlib import Path
from typing import Iterable

import typer
from loguru import logger


def traverse_vanilla_directory(vanilla_path: Path) -> Iterable[Path]:
    for directory in sorted(vanilla_path.glob("vanilla_*")):
        if directory.is_dir():
            objects = directory / "objects"
            if objects.exists() and objects.is_dir():
                for file in sorted(objects.glob("*.txt")):
                    if file.is_file():
                        yield file


def parse_file(file_path: Path):
    ...


# def main(raws_path: Path, pot_file: typer.FileTextWrite, source_encoding: str = "cp437"):
def main(vanilla_path: Path):
    for file in traverse_vanilla_directory(vanilla_path):
        logger.info(file.relative_to(vanilla_path))


if __name__ == "__main__":
    typer.run(main)
