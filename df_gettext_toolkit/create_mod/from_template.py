from dataclasses import dataclass
from pathlib import Path
from typing import Iterator, List, Mapping, Optional, Tuple

import jinja2
import typer
from babel.messages.pofile import read_po
from loguru import logger

from df_gettext_toolkit.create_mod.generate_preview import main as generate_preview
from df_gettext_toolkit.create_pot.from_steam_text import get_raw_object_type, traverse_vanilla_directories
from df_gettext_toolkit.parse.parse_raws import split_tag, tokenize_raw_file
from df_gettext_toolkit.translate.translate_plain_text import translate_plain_text_file
from df_gettext_toolkit.translate.translate_raws import translate_single_raw_file
from df_gettext_toolkit.utils.backup import backup


@dataclass
class Dictionaries:
    language_name: str
    dictionary_object: Mapping[Tuple[str, Optional[str]], str]
    dictionary_textset: Mapping[str, str]


def create_single_localized_mod(
    template_path: Path,
    dictionaries: Dictionaries,
    source_encoding: str,
    destination_encoding: str,
) -> Iterator[str]:
    yield from localize_directory(template_path / "objects", dictionaries, source_encoding, destination_encoding)
    translated_files = len(list((template_path / "objects").glob("*.txt")))
    logger.info(f"{template_path.name} -> {template_path.name}: {translated_files} files")
    language_name = dictionaries.language_name
    create_info(template_path / "info.txt", source_encoding, destination_encoding, language_name)

    svg_template_path = Path(__file__).parent / "templates" / "preview_template.svg"
    generate_preview(
        svg_template_path,
        language_name.upper(),
        str(template_path.name).replace("_", "\n").title(),
        template_path / "preview.png",
    )

    template_path.rename(template_path.parent / f"{template_path.name}_{language_name.lower()}")


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
                        bak_name, file_path, dictionaries.dictionary_textset, destination_encoding, False
                    )
                else:
                    yield from translate_single_raw_file(
                        bak_name, file_path, dictionaries.dictionary_object, destination_encoding
                    )


def fill_info_template(template_path: Path, **kwargs) -> str:
    with open(template_path) as template_file:
        template_text = template_file.read()
        template = jinja2.Template(template_text)

        rendered = template.render(**kwargs)
        result = "\n".join(filter(lambda x: bool(x), rendered.splitlines()))
        return result


def create_info(info_file: Path, source_encoding: str, destination_encoding: str, language: str) -> None:
    with backup(info_file) as bak_name:
        with open(bak_name, encoding=source_encoding) as src:
            with open(info_file, "w", encoding=destination_encoding) as dest:
                title = "Vanilla"
                source_info = dict()
                for item in tokenize_raw_file(src):
                    if item.is_tag:
                        tag = split_tag(item.text)
                        if tag[0] == "NAME":
                            title = tag[1]

                        source_info[tag[0].lower()] = patch_info_tag(tag, language)

                info_template_path = Path(__file__).parent / "templates" / "info_template.txt"
                rendered = fill_info_template(
                    info_template_path,
                    steam_title=f"{language.upper()} {title}",
                    steam_description=f"{language.upper()} translation for {title}",
                    steam_tags=["ui", "qol", "translation"],
                    steam_key_value_tags=dict(language=language),
                    **source_info,
                )
                print(rendered, file=dest)


def pretty_directory_name(text: str) -> str:
    return text.replace("_", " ").title()


def patch_info_tag(tag: List[str], language: str) -> str:
    if tag[0] == "ID":
        return f"{language.lower()}_{tag[1]}"
    elif tag[0] == "AUTHOR":
        return f"DFINT (Original by {tag[1]})"
    elif tag[0] == "NAME":
        return f"{tag[1]} ({language.upper()})"
    elif tag[0] == "DESCRIPTION":
        return f"{tag[1]} (Translated to {language.upper()})"

    return tag[1]


def get_dictionaries(translation_path: Path, language: str) -> Dictionaries:
    po_files = {"objects": Path(), "text_set": Path()}
    for po_file in po_files:
        mtime = 0
        for file in translation_path.glob(f"*{po_file}*{language}.po"):
            if file.is_file() and file.stat().st_mtime > mtime:
                po_files[po_file] = file
        if not po_files[po_file].is_file():
            raise Exception(f"Unable to find {po_file} po file for language {language}")

    with open(po_files["objects"], "r", encoding="utf-8") as pofile:
        dictionary_object = {(item.id, item.context): item.string for item in read_po(pofile)}
    with open(po_files["text_set"], "r", encoding="utf-8") as po_file:
        dictionary_textset = {item.id: item.string for item in read_po(po_file) if item.id}
    return Dictionaries(language.lower(), dictionary_object, dictionary_textset)


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
        except Exception:
            logger.error(f"Error occurred while removing {bak_file.resolve()}")

    logger.warning(
        "All done! Consider to change info.txt file and made unique preview.png "
        "before uploading to steam or sharing the mod."
    )


if __name__ == "__main__":
    typer.run(main)
