from pathlib import Path
from typing import Iterator, Mapping, NewType, Optional, Tuple

import typer
from babel.messages.pofile import read_po
from loguru import logger

import df_gettext_toolkit.create_mod.generate_preview as generate_preview
from df_gettext_toolkit.create_pot.from_steam_text import get_raw_object_type, traverse_vanilla_directories
from df_gettext_toolkit.parse.parse_raws import join_tag, split_tag, tokenize_raw_file
from df_gettext_toolkit.translate.translate_plain_text import translate_plain_text_file
from df_gettext_toolkit.translate.translate_raws import translate_single_raw_file
from df_gettext_toolkit.utils.backup import backup

Dictionaries = NewType("Dictionaries", Tuple[str, Mapping[Tuple[str, Optional[str]], str], Mapping[str, str]])


def create_single_localized_mod(
    template_path: Path,
    dictionaries: Dictionaries,
    source_encoding: str,
    destination_encoding: str,
) -> Iterator[str]:
    yield from localize_directory(template_path / "objects", dictionaries, source_encoding, destination_encoding)
    tranlated_files = len([*(template_path / "objects").glob("*.txt")])
    logger.info(f"{template_path.name} -> {template_path.name}: {tranlated_files} files")
    create_info(template_path / "info.txt", source_encoding, destination_encoding, dictionaries[0])
    generate_preview.main(
        template_path / "preview.png", dictionaries[0].upper(), str(template_path.name).replace("_", "\n").title()
    )
    template_path.rename(f"{str(template_path.resolve())}_{dictionaries[0].lower()}")


def localize_directory(
    template_path: Path,
    dictionaries: Dictionaries,
    source_encoding: str,
    destination_encoding: str,
) -> Iterator[str]:
    for file_path in template_path.glob("*.txt"):
        if file_path.is_file():
            object_type = get_raw_object_type(file_path, source_encoding)
            with backup(file_path) as bak_name:
                if object_type == "TEXT_SET":
                    yield from translate_plain_text_file(
                        bak_name, file_path, dictionaries[2], destination_encoding, False
                    )
                else:
                    yield from translate_single_raw_file(bak_name, file_path, dictionaries[1], destination_encoding)


def create_info(info_file: Path, source_encoding: str, destination_encoding: str, language: str) -> None:
    with backup(info_file) as bak_name:
        with open(bak_name, encoding=source_encoding) as src:
            with open(info_file, "w", encoding=destination_encoding) as dest:
                title = "Vanilla"
                for item in tokenize_raw_file(src):
                    if item.is_tag:
                        object_tag = split_tag(item.text)
                        if object_tag[0] == "NAME":
                            title = object_tag[1]
                        print(join_tag(patch_info_tag(object_tag, language)), file=dest)

                print(
                    f"""
[STEAM_TITLE: {language.upper()} {title}]
[STEAM_DESCRIPTION: {language.upper()} translation for {title}]
[STEAM_TAG:ui]
[STEAM_TAG:qol]
[STEAM_TAG:translation]
[STEAM_TAG:language]
[STEAM_TAG:{language.lower()}]
[STEAM_KEY_VALUE_TAG:what:isthis?]
[STEAM_METADATA:andthis?]
[STEAM_CHANGELOG:Changelog here]""",
                    file=dest,
                )


def pretty_directory_name(text: str) -> str:
    return text.replace("_", " ").title()


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
        dictionary_object = {(item.id, item.context): item.string for item in read_po(pofile)}
    with open(po_files["text_set"], "r", encoding="utf-8") as po_file:
        dictionary_textset = {item.id: item.string for item in read_po(po_file) if item.text}
    return Dictionaries((language.lower(), dictionary_object, dictionary_textset))


@logger.catch
def main(
    template_path: Path,
    translation_path: Path,
    language: str,
    destination_encoding: str,
    source_encoding: str = "cp437",
) -> None:
    assert template_path.exists(), "Source path doesn't exist"
    assert translation_path.exists(), "Translation path doesn't exist"

    dictionaries = get_dictionaries(
        translation_path,
        language,
    )

    for directory in traverse_vanilla_directories(template_path):
        for file in create_single_localized_mod(
            directory.parent,
            dictionaries,
            source_encoding,
            destination_encoding,
        ):
            logger.debug(f"{file} translated")

    for bak_file in template_path.glob("**/*.bak"):
        try:
            bak_file.unlink()
        except:
            logger.error(f"Error occured while removing {bak_file.resolve()}")

    logger.warning(
        "All done! Consider to change info.txt file and made unique preview.png before uploading to steam or sharing the mod."
    )


if __name__ == "__main__":
    typer.run(main)
