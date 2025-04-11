from collections import defaultdict
from collections.abc import Iterable
from pathlib import Path

import typer
from loguru import logger

from df_translation_toolkit.create_pot.from_raw_objects import extract_from_raw_file
from df_translation_toolkit.parse.parse_raws import split_tag, tokenize_raw_file
from df_translation_toolkit.parse.parse_text_set import extract_from_vanilla_text
from df_translation_toolkit.utils.po_utils import TranslationItem, save_pot


def traverse_vanilla_directories(vanilla_path: Path) -> Iterable[Path]:
    for directory in sorted(vanilla_path.glob("vanilla_*")):
        if directory.is_dir():
            objects = directory / "objects"
            if objects.is_dir():
                yield objects


def get_raw_object_type(file_name: Path, source_encoding: str) -> str | None:
    with file_name.open(encoding=source_encoding) as file:
        for item in tokenize_raw_file(file):
            if item.is_tag:
                object_tag = split_tag(item.text)

                if object_tag[0] not in ("OBJECTS", "OBJECT"):
                    msg = f"Unexpected tag: {object_tag[0]}"
                    raise ValueError(msg)

                return object_tag[1]
        return None


def get_translatable_strings(file_path: Path, source_encoding: str) -> tuple[str, Iterable[TranslationItem]] | None:
    object_type = get_raw_object_type(file_path, source_encoding)
    if object_type in dont_translate:
        return None

    if object_type == "TEXT_SET":
        key = object_type
        data = extract_from_vanilla_text(file_path, source_encoding)
    else:
        key = "OBJECTS"
        data = extract_from_raw_file(file_path, source_encoding)

    return key, data


def iterable_is_empty(iterable: Iterable) -> bool:
    iterator = iter(iterable)
    try:
        next(iterator)
    except StopIteration:
        return True

    return False


def file_is_translatable(file_path: Path, source_encoding: str) -> bool:
    result = get_translatable_strings(file_path, source_encoding)
    return result is not None and not iterable_is_empty(result[1])


dont_translate = {"LANGUAGE"}


def main(vanilla_path: Path, destination_path: Path, source_encoding: str = "cp437") -> None:
    if not vanilla_path.exists():
        msg = "Source path doesn't exist"
        raise ValueError(msg)

    if not destination_path.exists():
        msg = "Destination path doesn't exist"
        raise ValueError(msg)

    results = defaultdict(list)

    for directory in traverse_vanilla_directories(vanilla_path):
        logger.info(directory.relative_to(vanilla_path))
        for file_path in sorted(directory.glob("*.txt")):
            if file_path.is_file():
                result = get_translatable_strings(file_path, source_encoding)
                if not result:
                    continue

                group, data = result
                results[group].extend(data)

        for group, data in results.items():
            if data:
                pot_path = destination_path / (group.lower() + ".pot")
                with pot_path.open("wb") as file_path:
                    save_pot(file_path, data)


if __name__ == "__main__":
    typer.run(main)
