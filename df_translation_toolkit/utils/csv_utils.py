import csv
from collections.abc import Iterable, Iterator
from pathlib import Path
from typing import IO, Protocol, TextIO


class CSVWriter(Protocol):
    def writerow(self, row: list[str]) -> None: ...
    def writerows(self, rows: Iterable[list[str]]) -> None: ...


class CSVReader(Protocol):
    def __iter__(self) -> Iterator[list[str]]: ...


def writer(file: IO[str], **kwargs) -> CSVWriter:
    return csv.writer(file, dialect="unix", lineterminator="\r\n", **kwargs)


def reader(file: TextIO, **kwargs) -> CSVReader:
    return csv.reader(file, dialect="unix", lineterminator="\r\n", **kwargs)


def write_csv(file_path: Path, encoding: str, data: list[list[str]]) -> None:
    with file_path.open("w", encoding=encoding, newline="") as file:
        csv_writer = writer(file)
        csv_writer.writerows(data)


def read_csv(file_path: Path, encoding: str) -> Iterator[list[str]]:
    with file_path.open(encoding=encoding, newline="") as file:
        csv_reader = reader(file)
        yield from csv_reader
