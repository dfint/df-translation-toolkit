from collections.abc import Iterator
from pathlib import Path
from typing import TextIO

from df_translation_toolkit.create_pot.from_speech import extract_from_speech_file
from df_translation_toolkit.parse.parse_raws import split_tag, tokenize_raw_file
from df_translation_toolkit.utils.po_utils import TranslationItem


def skip_text_set_header(file: TextIO) -> None:
    for item in tokenize_raw_file(file):
        if item.is_tag:
            object_tag = split_tag(item.text)

            if object_tag[0] not in ("OBJECT", "TEXT_SET"):
                msg = f"Unexpected tag: {object_tag[0]}"
                raise ValueError(msg)

            if object_tag[0] == "TEXT_SET":
                return


def extract_from_vanilla_text(file_name: Path, source_encoding: str) -> Iterator[TranslationItem]:
    with file_name.open(encoding=source_encoding) as file:
        skip_text_set_header(file)
        for item in extract_from_speech_file(file, file_name.name):
            item.source_file = file_name.name
            yield item
