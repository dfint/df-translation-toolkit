import shutil
from pathlib import Path

from df_translation_toolkit.utils import csv_utils
from df_translation_toolkit.utils.backup import backup


def split_left(start, end):
    mid = (start + end) // 2
    return start, mid


def split_right(start, end):
    mid = (start + end) // 2
    return mid, end


def bisect(file_path: Path, encoding: str, data: list[list[str]]):
    def _bisect(start: int, end: int, bad: bool = False) -> bool:
        """
        returns:
        - True -> found
        - False -> not found
        """
        if start >= end:
            print("Empty slice, step back")
            return False

        print(f"From {start} to {end} (in total {end - start})")
        csv_utils.write_csv(file_path, encoding, data[start:end])

        if bad:
            confirmed = True
        else:
            confirmed = input("Is it bad (Y/N)? ").upper() == "Y"

        if not confirmed:
            return False

        if start == end - 1:
            print(f"Found string, line number {start+1}:")
            print(data[start])

            confirmed = input("Exclude from csv (Y/N)? ").upper() == "Y"
            if confirmed:
                csv_utils.write_csv(file_path, encoding, data[:start] + data[start + 1 :])

            return True

        print("Trying left half")
        result = _bisect(*split_left(start, end))
        if result:
            return result

        print("Trying right half")
        return _bisect(*split_right(start, end), bad=True)

    _bisect(0, len(data), bad=True)


def main(csv_file: Path, encoding: str):
    assert csv_file.is_file(), f"{csv_file.name} is not a file"

    try:
        with backup(csv_file, overwrite=True) as backup_path:
            data = list(csv_utils.read_csv(backup_path, encoding))
            bisect(csv_file, encoding, data)
    finally:
        confirmed = input("Restore from backup (Y/N)? ").upper() == "Y"
        if confirmed:
            shutil.copy(backup_path, csv_file)
