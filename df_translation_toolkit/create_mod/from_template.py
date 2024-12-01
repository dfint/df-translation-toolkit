from collections.abc import Iterator, Mapping
from dataclasses import dataclass
from pathlib import Path

import jinja2
import typer
from babel.messages.pofile import read_po
from loguru import logger

from df_translation_toolkit.create_mod.generate_preview import main as generate_preview
from df_translation_toolkit.create_pot.from_steam_text import get_raw_object_type
from df_translation_toolkit.translate.translate_plain_text import translate_plain_text_file
from df_translation_toolkit.translate.translate_raws import translate_single_raw_file
from df_translation_toolkit.utils.backup import backup


@dataclass
class Dictionaries:
    language_name: str
    dictionary_object: Mapping[tuple[str, str | None], str]
    dictionary_textset: Mapping[str, str]


def create_single_localized_mod(
    template_path: Path,
    dictionaries: Dictionaries,
    source_encoding: str,
    destination_encoding: str,
) -> Iterator[str]:
    yield from localize_directory(template_path / "objects", dictionaries, source_encoding, destination_encoding)
    translated_files = len(list((template_path / "objects").glob("*.txt")))
    logger.info(f"Translated: {translated_files} files")
    language_name = dictionaries.language_name
    create_info(template_path / "info.txt", destination_encoding, language_name)

    svg_template_path = Path(__file__).parent / "templates" / "preview_template.svg"
    generate_preview(
        svg_template_path,
        language_name.upper(),
        "translation",
        template_path / "preview.svg",
    )


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
                        bak_name,
                        file_path,
                        dictionaries.dictionary_textset,
                        destination_encoding,
                        join_paragraphs=False,
                    )
                else:
                    yield from translate_single_raw_file(
                        bak_name,
                        file_path,
                        dictionaries.dictionary_object,
                        destination_encoding,
                    )


def fill_info_template(template_path: Path, **kwargs: str | list[str] | dict[str, str]) -> str:
    with template_path.open() as template_file:
        template_text = template_file.read()
        template = jinja2.Template(template_text)

        rendered = template.render(**kwargs)
        return "\n".join(filter(bool, rendered.splitlines()))


def create_info(info_file: Path, destination_encoding: str, language: str) -> None:
    with info_file.open("w", encoding=destination_encoding) as dest:
        info_template_path = Path(__file__).parent / "templates" / "info_template.txt"
        rendered = fill_info_template(
            info_template_path,
            name=f"{language.upper()} Translation",
            description=f"Translation to {language.upper()} language for vanilla mods",
            author="DFINT",
            id=f"{language.lower()}_vanilla_translation",
            steam_title=f"{language.upper()} Translation",
            steam_description=f"Translation to {language.upper()} language for vanilla mods",
            steam_tags=["ui", "qol", "translation"],
            steam_key_value_tags={"language": language},
        )
        print(rendered, file=dest)


def get_dictionaries(translation_path: Path, language: str) -> Dictionaries:
    po_files: dict[str, Path] = {}
    for po_file in ["objects", "text_set"]:
        mtime = 0
        for file in translation_path.glob(f"*{po_file}*{language}.po"):
            if file.is_file() and file.stat().st_mtime > mtime:
                po_files[po_file] = file

        if po_file not in po_files:
            msg = f"Unable to find {po_file} po file for language {language}"
            raise ValueError(msg)

    with open(po_files["objects"], encoding="utf-8") as pofile:
        dictionary_object: Mapping[tuple[str, str | None], str] = {
            (item.id, item.context): item.string for item in read_po(pofile)
        }
    with open(po_files["text_set"], encoding="utf-8") as po_file:
        dictionary_textset: Mapping[str, str] = {item.id: item.string for item in read_po(po_file) if item.id}
    return Dictionaries(language.lower(), dictionary_object, dictionary_textset)


@logger.catch
def main(
    template_path: Path,
    translation_path: Path,
    language: str,
    destination_encoding: str,
    source_encoding: str = "cp437",
) -> None:
    if not template_path.exists():
        msg = "Source path doesn't exist"
        raise ValueError(msg)

    if not translation_path.exists():
        msg = "Translation path doesn't exist"
        raise ValueError(msg)

    dictionaries = get_dictionaries(translation_path, language)

    for file in create_single_localized_mod(
        template_path,
        dictionaries,
        source_encoding,
        destination_encoding,
    ):
        logger.debug(f"{file} translated")

    for bak_file in template_path.glob("**/*.bak"):
        try:
            bak_file.unlink()
        except Exception:  # noqa: PERF203, BLE001
            logger.error(f"Error occurred while removing {bak_file.resolve()}")

    template_path.rename(template_path.parent / f"{template_path.name}_translation")
    logger.warning(
        "All done! Consider to change info.txt file and made unique preview.png "
        "before uploading to steam or sharing the mod.",
    )


if __name__ == "__main__":
    typer.run(main)
