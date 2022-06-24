from pathlib import Path
from typing import Mapping

from df_raw_decoder import decode_data, encode_data

from .backup import backup
from .parse_plain_text import parse_plain_text_file
from .parse_po import load_po


def translate_compressed_file(
    source_file_path: Path,
    destination_file_path: Path,
    dictionary: Mapping[str, str],
    encoding: str,
    is_index_file: bool,
):

    with open(source_file_path, "rb") as src:
        with open(destination_file_path, "wb") as dest:
            yield destination_file_path.name

            translations = []

            lines = (line.decode("cp437") for line in decode_data(src, is_index_file))
            for text_block, is_translatable, _ in parse_plain_text_file(lines, True):
                if text_block in dictionary:
                    translation = dictionary[text_block]
                    if not translation:
                        translation = text_block
                else:
                    translation = text_block
                translations.append(translation.encode(encoding))

            dest.write(encode_data(translations, is_index_file))


def translate_compressed(po_filename, path, encoding):
    with open(po_filename, "r", encoding="utf-8") as pofile:
        dictionary = {item["msgid"]: item["msgstr"] for item in load_po(pofile)}

    for file in Path(path).rglob("*"):
        if file.is_file() and "." not in file.name:
            is_index_file = file.name == "index"
            # Fix crash game due to changes in index file
            if is_index_file:
                continue

            with backup(file) as backup_file:
                try:
                    yield from translate_compressed_file(backup_file, file, dictionary, encoding, is_index_file)
                except Exception as ex:
                    yield "Error: " + str(ex)
