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


def write_csv(file_path: Path, encoding: str, data: List[Tuple[str, str]]):
    with open(file_path, "w", encoding=encoding, newline="") as file:
        csv_writer = csv_utils.writer(file)
        csv_writer.writerows(data)


def bisect(file_path: Path, encoding: str, data: List[Tuple[str, str]], start: int, end: int, first_time=False) -> bool:
    """
    returns:
    - True -> found
    - False -> not found
    """
    if start >= end:
        print("Empty slice, step back")
        return False

    print(f"From {start} to {end} (in total {end - start})")
    write_csv(file_path, encoding, data[start:end])

    if first_time:
        confirmed = True
    else:
        confirmed = input("Is it bad (Y/N)? ").upper() == "Y"

    if confirmed:
        if start == end - 1:
            print(f"Found string:")
            print(data[start])

            confirmed = input("Exclude from csv (Y/N)? ").upper() == "Y"
            if confirmed:
                write_csv(file_path, encoding, data[:start] + data[start + 1:])

            return True

        print("Trying left half")
        result = bisect(file_path, encoding, data, *split_left(start, end))
        if result:
            return result

        print("Trying right half")
        return bisect(file_path, encoding, data, *split_right(start, end))
    else:
        return False


def main(csv_file: Path, encoding: str):
    assert csv_file.is_file(), f"{csv_file.name} is not a file"

    with backup(csv_file) as backup_path:
        with open(backup_path, encoding=encoding, newline="") as file:
            csv_reader = csv_utils.reader(file)
            data = list(csv_reader)

        bisect(csv_file, encoding, data, 0, len(data), first_time=True)

    confirmed = input("Restore from backup (Y/N)? ").upper() == "Y"
    if confirmed:
        shutil.copy(backup_path, csv_file)
