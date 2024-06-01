from pathlib import PurePath
from unittest.mock import Mock

from df_translation_toolkit.translate.batch import Pattern, translate_files


def test_translate_files():
    def function(po_filename, path, encoding):
        yield po_filename, path, encoding

    directory_name = "directory"

    po_filename = "po_filename"
    patterns = [Pattern(directory_name, po_filename, function=function)]

    base_dir_mock = Mock("base_dir")
    directory_mock = Mock("directory")
    directory_mock.is_dir = lambda: True
    directory_mock.match = lambda pattern: pattern == "*/" + directory_name
    base_dir_mock.rglob = lambda *_args: [directory_mock]
    po_directory = PurePath("po_directory")
    encoding = "utf-8"
    postfix = "postfix"

    assert list(
        translate_files(base_dir_mock, po_directory, encoding, po_name_postfix=postfix, directory_patterns=patterns),
    ) == [
        f"Matched {directory_name} pattern",
        (po_directory / f"{po_filename}_{postfix}.po", directory_mock, encoding),
    ]
