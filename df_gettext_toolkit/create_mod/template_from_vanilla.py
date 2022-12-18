import shutil
from pathlib import Path

import typer
from loguru import logger

from df_gettext_toolkit.create_pot.from_steam_text import traverse_vanilla_directories

directories_to_copy = {
    "vanilla_bodies",
    "vanilla_buildings",
    "vanilla_creatures",
    "vanilla_descriptors",
    "vanilla_entities",
    "vanilla_interactions",
    "vanilla_items",
    "vanilla_materials",
    "vanilla_plants",
    "vanilla_reactions",
    "vanilla_text",
}


@logger.catch
def main(
    vanilla_path: Path,
    destination_path: Path,
    source_encoding: str = "cp437",
) -> None:
    assert vanilla_path.exists(), "Source path doesn't exist"
    assert destination_path.exists(), "Destination path doesn't exist"

    total = 0

    for directory in traverse_vanilla_directories(vanilla_path):
        if directory.parent.name not in directories_to_copy:
            continue
        shutil.copytree(directory.parent, destination_path / directory.parent.name)
        logger.info(f"Copy {directory.parent.name}")
        total += 1

    logger.info(f"Total copied directories: {total}")


if __name__ == "__main__":
    typer.run(main)
