import shutil
from pathlib import Path
from typing import Iterator, Mapping, Optional, Tuple, NewType

import typer
from loguru import logger


from df_gettext_toolkit.create_pot.from_steam_text import traverse_vanilla_directories
from df_gettext_toolkit.create_pot.from_steam_text import get_raw_object_type
from df_gettext_toolkit.parse.parse_po import load_po
from df_gettext_toolkit.parse.parse_raws import split_tag, join_tag, tokenize_raw_file
from df_gettext_toolkit.translate.translate_raws import translate_single_raw_file
from df_gettext_toolkit.translate.translate_plain_text import translate_plain_text_file


Dictionaries = NewType("Dictionaries", Tuple[str, Mapping[Tuple[str, Optional[str]], str], Mapping[str, str]])


def create_single_localized_mod(
    source_path: Path,
    destination_path: Path,
    dictionaries: Dictionaries,
    source_encoding: str,
    destination_encoding: str,
) -> Iterator[str]:
    dest = Path(destination_path, f"{source_path.name}_{dictionaries[0]}")
    yield from localize_directory(
        source_path / "objects", dest / "objects", dictionaries, source_encoding, destination_encoding
    )
    tranlated_files = len([*dest.glob("**/*.txt")])
    if tranlated_files == 0:
        shutil.rmtree(dest)
    else:
        logger.info(f"{source_path.name} -> {dest.name}: {tranlated_files} files")
        create_info(source_path / "info.txt", dest / "info.txt", source_encoding, destination_encoding, dictionaries[0])


def localize_directory(
    source_directory: Path,
    destination_directory: Path,
    dictionaries: Dictionaries,
    source_encoding: str,
    destination_encoding: str,
) -> Iterator[str]:
    Path.mkdir(destination_directory, parents=True, exist_ok=True)

    for file_path in source_directory.glob("*.txt"):
        if file_path.is_file() and not file_path.name.startswith("language_"):
            object_type = get_raw_object_type(file_path, source_encoding)
            if object_type == "TEXT_SET":
                yield from translate_plain_text_file(
                    file_path, destination_directory / file_path.name, dictionaries[2], destination_encoding, False
                )
            else:
                yield from translate_single_raw_file(
                    file_path, destination_directory / file_path.name, dictionaries[1], destination_encoding
                )


def create_info(
    source_file: Path, destination_file: Path, source_encoding: str, destination_encoding: str, language: str
) -> None:
    with open(source_file, encoding=source_encoding) as src:
        with open(destination_file, "w", encoding=destination_encoding) as dest:
            for item in tokenize_raw_file(src):
                if item.is_tag:
                    object_tag = split_tag(item.text)
                    print(join_tag(patch_info_tag(object_tag, language)), file=dest)

            print(
                f"""
[STEAM_TITLE:Test Descriptors]
[STEAM_DESCRIPTION:Some test object definitions for shapes and colors.]
[STEAM_TAG:mod] <-- as many as you want, use a separate STEAM_TAG for each one
[STEAM_KEY_VALUE_TAG:test:stuff] <-- as many as you want, similarly
[STEAM_METADATA:metadata test]
[STEAM_CHANGELOG:made some changes]""",
                file=dest,
            )


def patch_info_tag(tag: list[str], language: str) -> list[str]:
    if tag[0] == "ID":
        tag[1] = f"{language.lower()}_{tag[1]}"
    elif tag[0] == "AUTHOR":
        tag[1] = f"DFINT (Original by {tag[1]})"
    elif tag[0] == "NAME":
        tag[1] = f"{tag[1]} ({language.upper()})"
    elif tag[0] == "DESCRIPTION":
        tag[1] = f"{tag[1]} (Translated to {language.upper()})"

    return tag


def get_dictionaries(tranlation_path: Path, language: str) -> Dictionaries:
    po_files = {"objects": Path(), "text_set": Path()}
    for po_file in po_files:
        mtime = 0
        for file in tranlation_path.glob(f"*{po_file}*{language}.po"):
            if file.is_file() and file.stat().st_mtime > mtime:
                po_files[po_file] = file
        if po_files[po_file].is_file() == False:
            raise Exception(f"Unable to find {po_file} po file for language {language}")

    with open(po_files["objects"], "r", encoding="utf-8") as pofile:
        dictionary_object = {(item.text, item.context): item.translation for item in load_po(pofile)}
    with open(po_files["text_set"], "r", encoding="utf-8") as po_file:
        dictionary_textset = {item.text: item.translation for item in load_po(po_file) if item.text}
    return Dictionaries((language.lower(), dictionary_object, dictionary_textset))


@logger.catch
def main(
    vanilla_path: Path,
    destination_path: Path,
    tranlation_path: Path,
    language: str,
    destination_encoding: str,
    source_encoding: str = "cp437",
) -> None:
    assert vanilla_path.exists(), "Source path doesn't exist"
    assert destination_path.exists(), "Destination path doesn't exist"

    dictionaries = get_dictionaries(
        tranlation_path,
        language,
    )

    for directory in traverse_vanilla_directories(vanilla_path):
        for file in create_single_localized_mod(
            directory.parent,
            destination_path,
            dictionaries,
            source_encoding,
            destination_encoding,
        ):
            logger.debug(f"{file} translated")


if __name__ == "__main__":
    typer.run(main)
