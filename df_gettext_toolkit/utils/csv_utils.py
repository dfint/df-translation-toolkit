import csv
from typing import TextIO


def writer(file: TextIO, **kwargs):
    return csv.writer(file, dialect="unix", lineterminator="\r\n", **kwargs)


def reader(file: TextIO, **kwargs):
    return csv.reader(file, dialect="unix", lineterminator="\r\n", **kwargs)
