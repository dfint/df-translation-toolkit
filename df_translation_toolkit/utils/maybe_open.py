from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path
from typing import TextIO


@contextmanager
def maybe_open(file_name: str | Path | None, *args, **kwargs) -> Generator[TextIO | None, None, None]:
    file = None
    try:
        if file_name:
            file = open(file_name, *args, **kwargs)  # noqa: SIM115

        yield file
    finally:
        if file:
            file.close()
