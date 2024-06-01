import csv
from collections.abc import Iterator
from pathlib import Path
from typing import TextIO


def writer(file: TextIO, **kwargs):
    return csv.writer(file, dialect="unix", lineterminator="\r\n", **kwargs)


def reader(file: TextIO, **kwargs):
    return csv.reader(file, dialect="unix", lineterminator="\r\n", **kwargs)


def write_csv(file_path: Path, encoding: str, data: list[list[str]]) -> None:
    with file_path.open("w", encoding=encoding, newline="") as file:
        csv_writer = writer(file)
        csv_writer.writerows(data)


def read_csv(file_path: Path, encoding: str) -> Iterator[list[str]]:
    with file_path.open(encoding=encoding, newline="") as file:
        csv_reader = reader(file)
        yield from csv_reader
