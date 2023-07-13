import shutil
from pathlib import Path

import typer
from loguru import logger

from df_gettext_toolkit.create_pot.from_steam_text import file_is_translatable, traverse_vanilla_directories

directories_to_copy = {
    "vanilla_bodies",
    "vanilla_buildings",
    "vanilla_creatures",
    "vanilla_descriptors",
    "vanilla_entities",
    "vanilla_items",
    "vanilla_materials",
    "vanilla_plants",
    "vanilla_text",
}


@logger.catch
def main(
    vanilla_path: Path,
    destination_path: Path,
) -> None:
    assert vanilla_path.exists(), "Source path doesn't exist"
    assert destination_path.exists(), "Destination path doesn't exist"

    total_dirs = 0
    total_files = 0

    (destination_path / "objects").mkdir(parents=True, exist_ok=True)

    for directory in traverse_vanilla_directories(vanilla_path):
        if directory.parent.name not in directories_to_copy:
            continue

        logger.info(f"Copy {directory.parent.name}")

        for file_path in directory.glob("*.txt"):
            if file_path.is_file() and file_is_translatable(file_path, "cp437"):
                shutil.copy(file_path, destination_path / "objects" / file_path.name)
                total_files += 1

        total_dirs += 1

    logger.info(f"Total copied: {total_files} files from {total_dirs} dirs")


if __name__ == "__main__":
    typer.run(main)
