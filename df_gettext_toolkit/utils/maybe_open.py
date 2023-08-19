from contextlib import contextmanager
from pathlib import Path


@contextmanager
def maybe_open(file_name: str | Path, *args, **kwargs):
    file = None
    try:
        if file_name:
            file = open(file_name, *args, **kwargs)

        yield file
    finally:
        if file:
            file.close()
