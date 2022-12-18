import shutil
from pathlib import Path
from typing import List, Tuple

from df_gettext_toolkit.utils import csv_utils
from df_gettext_toolkit.utils.backup import backup


def split_left(start, end):
    mid = (start + end) // 2
    return start, mid


def split_right(start, end):
    mid = (start + end) // 2
    return mid, end


def bisect(data: List[Tuple[str, str]], start: int, end: int) -> bool:
    """
    returns:
    - True -> found
    - False -> not found
    """
    if start == end - 1:
        print(f"Found string index {start}:")
        print(data[start])
        return True
    elif start >= end:
        print("Empty slice, step back")
        return False
    else:
        print(f"From {start} to {end} (in total {end - start})")
        # TODO: write csv

        answer = input("[G]ood/[B]ad/Step [U]p").upper()
        if answer == "G":
            return False
        elif answer == "B":
            print("Trying left half")
            result = bisect(data, *split_left(start, end))
            if result:
                return result

            print("Trying right half")
            return bisect(data, *split_right(start, end))


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
