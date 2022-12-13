import shutil
from pathlib import Path

from df_gettext_toolkit.utils.backup import backup


def test_backup_doesnt_exist(mocker):
    mocker.patch("pathlib.Path.exists", return_value=False)
    mocker.patch("shutil.copy")
    file_name = "file.txt"
    backup_name = "file.bak"
    with backup(file_name) as backup_file:
        assert Path(backup_file).name == backup_name
        shutil.copy.assert_called_once_with(Path(file_name), Path(backup_name))


def test_backup_exists(mocker):
    mocker.patch("pathlib.Path.exists", return_value=True)
    mocker.patch("shutil.copy")
    file_name = "file.txt"
    backup_name = "file.bak"
    with backup(file_name) as backup_file:
        assert Path(backup_file).name == backup_name
        shutil.copy.assert_not_called()
