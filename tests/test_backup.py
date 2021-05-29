import shutil
from unittest.mock import Mock
from pathlib import Path

from df_gettext_toolkit.backup import backup


def test_backup_doesnt_exist(monkeypatch, mocker):
    monkeypatch.setattr(Path, "exists", Mock(return_value=False))
    mocker.patch("shutil.copy")
    file_name = "file.txt"
    backup_name = "file.bak"
    with backup(file_name) as backup_file:
        assert Path(backup_file).name == backup_name
        shutil.copy.assert_called_once_with(Path(file_name), Path(backup_name))


def test_backup_exists(monkeypatch, mocker):
    monkeypatch.setattr(Path, "exists", Mock(return_value=True))
    mocker.patch("shutil.copy")
    file_name = "file.txt"
    backup_name = "file.bak"
    with backup(file_name) as backup_file:
        assert Path(backup_file).name == backup_name
        shutil.copy.assert_not_called()
