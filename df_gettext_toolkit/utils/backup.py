import shutil
from contextlib import contextmanager
from pathlib import Path


@contextmanager
def backup(file: str | Path, overwrite: bool = False):
    file = Path(file)
    backup_path = file.with_suffix(".bak")

    if overwrite or not backup_path.exists():
        shutil.copy(file, backup_path)

    yield backup_path
