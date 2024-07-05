from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path
from typing import Any


@contextmanager
def maybe_open(file_name: str | Path, *args, **kwargs) -> Generator[Any, Any, None]:
    file = None
    try:
        if file_name:
            file = open(file_name, *args, **kwargs)  # noqa: SIM115

        yield file
    finally:
        if file:
            file.close()
