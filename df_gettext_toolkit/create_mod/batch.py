from pathlib import Path
from urllib.error import HTTPError

import requests
import typer
from loguru import logger

from df_gettext_toolkit.create_mod.from_template import main as from_template
from df_gettext_toolkit.create_mod.template_from_vanilla import main as template_from_vanilla

PO_URL = "https://raw.githubusercontent.com/dfint/translations-backup/main/translations/dwarf-fortress-steam"


def fetch_po_from_git(language: str, destination_path: Path) -> None:
    resources: list[str] = ["objects", "text_set"]
    for resource in resources:
        response = requests.get(f"{PO_URL}/{resource}/{language.lower()}.po")
        response.raise_for_status()
        file_path = Path(destination_path / f"{resource}_{language.lower()}.po")
        with file_path.open("w", encoding="utf-8") as file:
            file.write(response.text)
    logger.info(f"PO files for {language.upper()} downloaded")


@logger.catch
def main(vanilla_path: Path, destination_path: Path, encoding: str, languages: list[str]) -> None:
    assert vanilla_path.exists(), "Source path doesn't exist"
    assert destination_path.exists(), "Destination path doesn't exist"

    for language in languages:
        try:
            fetch_po_from_git(language, destination_path)
        except HTTPError as e:
            raise Exception(f"Unable to download po file for language {language}. Error: {e.code}, {e.reason}")
        Path.mkdir(destination_path / language.lower(), parents=True, exist_ok=True)
        template_from_vanilla(vanilla_path, destination_path / language.lower())
        from_template(destination_path / language.lower(), destination_path, language, encoding)

    for po in destination_path.glob("**/*.po"):
        po.unlink()

    logger.success("All done!")


if __name__ == "__main__":
    typer.run(main)
