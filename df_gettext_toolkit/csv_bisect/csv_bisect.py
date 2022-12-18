import shutil
from pathlib import Path

from df_gettext_toolkit.utils import csv_utils
from df_gettext_toolkit.utils.backup import backup


def split_left(start, end):
    mid = (start + end) // 2
    return start, mid


def split_right(start, end):
    mid = (start + end) // 2
    return mid, end


def main(csv_file: Path, encoding: str):
    assert csv_file.is_file(), f"{csv_file.name} is not a file"

    with backup(csv_file) as backup_path:
        with open(backup_path, encoding=encoding,  newline="") as file:
            csv_reader = csv_utils.reader(file)
            data = list(csv_reader)

        prev = (0, len(data))
        stack = [prev]

        while prev[0] < prev[1]:
            break

    # Restore backup
    shutil.copy(csv_file, backup_path)
