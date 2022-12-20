import shutil
from pathlib import Path
from typing import List

from df_gettext_toolkit.utils import csv_utils
from df_gettext_toolkit.utils.backup import backup


def split_left(start, end):
    mid = (start + end) // 2
    return start, mid


def split_right(start, end):
    mid = (start + end) // 2
    return mid, end


class Bisector:
    file_path: Path
    encoding: str
    data: List[List[str, str]]

    def __init__(self, file_path: Path, encoding: str, data: List[List[str, str]]):
        self.file_path = file_path
        self.encoding = encoding
        self.data = data

    def bisect(self) -> bool:
        return self._bisect(0, len(self.data), first_time=True)

    def _bisect(self, start: int, end: int, first_time: bool = False) -> bool:
        """
        returns:
        - True -> found
        - False -> not found
        """
        if start >= end:
            print("Empty slice, step back")
            return False

        print(f"From {start} to {end} (in total {end - start})")
        csv_utils.write_csv(self.file_path, self.encoding, self.data[start:end])

        if first_time:
            confirmed = True
        else:
            confirmed = input("Is it bad (Y/N)? ").upper() == "Y"

        if confirmed:
            if start == end - 1:
                print(f"Found string:")
                print(self.data[start])

                confirmed = input("Exclude from csv (Y/N)? ").upper() == "Y"
                if confirmed:
                    csv_utils.write_csv(self.file_path, self.encoding, self.data[:start] + self.data[start + 1:])

                return True

            print("Trying left half")
            result = self._bisect(*split_left(start, end))
            if result:
                return result

            print("Trying right half")
            return self._bisect(*split_right(start, end))
        else:
            return False


def main(csv_file: Path, encoding: str):
    assert csv_file.is_file(), f"{csv_file.name} is not a file"

    with backup(csv_file) as backup_path:
        data = list(csv_utils.read_csv(backup_path, encoding))
        Bisector(csv_file, encoding, data).bisect()

    confirmed = input("Restore from backup (Y/N)? ").upper() == "Y"
    if confirmed:
        shutil.copy(backup_path, csv_file)
