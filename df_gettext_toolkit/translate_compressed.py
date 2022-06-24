from pathlib import Path
from typing import Mapping, Iterator, Iterable

from df_raw_decoder import unpack_data, pack_data

from df_gettext_toolkit.backup import backup
from df_gettext_toolkit.parse_plain_text import parse_plain_text_file
from df_gettext_toolkit.parse_po import load_po


def translate_file(lines: Iterable[str], dictionary: Mapping[str, str]) -> Iterator[str]:
    for text_block, is_translatable, _ in parse_plain_text_file(lines, True):
        if text_block in dictionary:
            translation = dictionary[text_block]
            if not translation:
                translation = text_block
        else:
            translation = text_block

        yield translation


def encode_lines(lines: Iterable[str], encoding: str):
    return (line.encode(encoding) for line in lines)


def decode_lines(lines: Iterable[bytes], encoding: str = "cp437"):
    return (line.decode(encoding) for line in lines)


def translate_compressed_file(
    source_file_path: Path,
    destination_file_path: Path,
    dictionary: Mapping[str, str],
    encoding: str,
):
    with open(source_file_path, "rb") as src:
        with open(destination_file_path, "wb") as dest:
            yield destination_file_path.name
            decoded_lines = decode_lines(unpack_data(src))
            translated_lines = translate_file(decoded_lines, dictionary)
            encoded_translation = encode_lines(translated_lines, encoding)
            dest.write(pack_data(encoded_translation))


def translate_compressed(po_filename, path, encoding):
    with open(po_filename, "r", encoding="utf-8") as pofile:
        dictionary = {item["msgid"]: item["msgstr"] for item in load_po(pofile)}

    for file in Path(path).rglob("*"):
        if file.is_file() and "." not in file.name:
            # Don't patch index file
            # (it's encoded, it is possible to decode/encode it, but the game crashes if it is changed)
            if file.name == "index":
                continue

            with backup(file) as backup_file:
                try:
                    yield from translate_compressed_file(backup_file, file, dictionary, encoding)
                except Exception as ex:
                    yield "Error: " + str(ex)
