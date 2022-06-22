import sys
from pathlib import Path

import typer

from .translate_plain_text import translate_plain_text
from .translate_raws import translate_raws

patterns = {
    "raw/objects": dict(
        po_filename="raw-objects.po",
        func=translate_raws,
    ),
    "data_src": dict(
        po_filename="uncompressed.po",
        func=lambda *args: translate_plain_text(*args, join_paragraphs=True),
    ),
    "data/speech": dict(
        po_filename="speech.po",
        func=lambda *args: translate_plain_text(*args, join_paragraphs=False),
    ),
    "raw/objects/text": dict(
        po_filename="text.po",
        func=lambda *args: translate_plain_text(*args, join_paragraphs=False),
    ),
}


def main(
    base_path: str,
    po_directory: str,
    encoding: str,
    po_name_prefix: str = "",
    po_name_postfix: str = "",
):
    po_directory = Path(po_directory)

    for cur_dir in Path(base_path).rglob("*"):
        if cur_dir.is_dir():
            for pattern in patterns:
                if cur_dir.match("*/" + pattern):
                    print(f"Matched {pattern} pattern")
                    print(cur_dir, file=sys.stderr)
                    print(file=sys.stderr)

                    match = patterns[pattern]

                    po_filename = Path(match["po_filename"])
                    po_filename = po_filename.with_name(po_name_prefix + po_filename.name + po_name_postfix)

                    po_file_path = po_directory / po_filename
                    func = match["func"]
                    for filename in func(po_file_path, cur_dir, encoding):
                        print(filename, file=sys.stderr)
                    print(file=sys.stderr)


if __name__ == "__main__":
    typer.run(main)
