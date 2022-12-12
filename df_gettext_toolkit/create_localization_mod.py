from pathlib import Path
from typing import Iterable

import typer
from loguru import logger

from df_gettext_toolkit.parse_raws import split_tag, tokenize_raw_file


def traverse_vanilla_directory(vanilla_path: Path) -> Iterable[Path]:
    for directory in sorted(vanilla_path.glob("vanilla_*")):
        if directory.is_dir():
            objects = directory / "objects"
            if objects.exists() and objects.is_dir():
                for file in sorted(objects.glob("*.txt")):
                    if file.is_file():
                        yield file


def get_raw_object_type(file_name: Path, source_encoding: str) -> str:
    with open(file_name, encoding=source_encoding) as file:
        for item in tokenize_raw_file(file):
            if item.is_tag:
                object_tag = split_tag(item.text)
                assert object_tag[0] == "OBJECT"
                return object_tag[1]


def parse_file(file_path: Path, source_encoding: str):
    logger.info(get_raw_object_type(file_path, source_encoding))


# def main(raws_path: Path, pot_file: typer.FileTextWrite, source_encoding: str = "cp437"):
def main(vanilla_path: Path, source_encoding: str = "cp437"):
    for file in traverse_vanilla_directory(vanilla_path):
        logger.info(file.relative_to(vanilla_path))
        parse_file(file, source_encoding)


if __name__ == "__main__":
    typer.run(main)
