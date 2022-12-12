from collections import defaultdict
from pathlib import Path
from typing import Iterable, TextIO

import typer
from loguru import logger

from df_gettext_toolkit.create_pot_from_raw_objects import extract_from_raw_file
from df_gettext_toolkit.create_pot_from_speech import extract_from_speech_file
from df_gettext_toolkit.parse_po import save_pot
from df_gettext_toolkit.parse_raws import split_tag, tokenize_raw_file


def traverse_vanilla_directories(vanilla_path: Path) -> Iterable[Path]:
    for directory in sorted(vanilla_path.glob("vanilla_*")):
        if directory.is_dir():
            objects = directory / "objects"
            if objects.is_dir():
                yield objects


def get_raw_object_type(file_name: Path, source_encoding: str) -> str:
    with open(file_name, encoding=source_encoding) as file:
        for item in tokenize_raw_file(file):
            if item.is_tag:
                object_tag = split_tag(item.text)
                assert object_tag[0] == "OBJECT"
                return object_tag[1]


def skip_text_set_header(file: TextIO) -> None:
    for item in tokenize_raw_file(file):
        if item.is_tag:
            object_tag = split_tag(item.text)
            assert object_tag[0] in {"OBJECT", "TEXT_SET"}
            if object_tag[0] == "TEXT_SET":
                return


def extract_from_vanilla_text(file_name: Path, source_encoding: str):
    with open(file_name, encoding=source_encoding) as file:
        skip_text_set_header(file)
        for item in extract_from_speech_file(file, file_name.name):
            item.source_file = file_name.name
            yield item


dont_translate = {"LANGUAGE"}


def main(vanilla_path: Path, destination_path: Path, source_encoding: str = "cp437"):
    assert destination_path.exists()

    results = defaultdict(list)

    for directory in traverse_vanilla_directories(vanilla_path):
        logger.info(directory.relative_to(vanilla_path))
        for file_path in sorted(directory.glob("*.txt")):
            if file_path.is_file():
                object_type = get_raw_object_type(file_path, source_encoding)
                if object_type in dont_translate:
                    continue
                elif object_type == "TEXT_SET":
                    key = object_type
                    data = extract_from_vanilla_text(file_path, source_encoding)
                else:
                    key = "OBJECTS"
                    data = extract_from_raw_file(file_path, source_encoding)

                results[key].extend(data)

        for group, data in results.items():
            if data:
                pot_path = destination_path / (group.lower() + ".pot")
                with open(pot_path, "wt", encoding=source_encoding) as file_path:
                    save_pot(file_path, data)


if __name__ == "__main__":
    typer.run(main)
