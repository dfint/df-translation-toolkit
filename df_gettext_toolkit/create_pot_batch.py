from pathlib import Path
from typing import Callable, NamedTuple

import typer

from df_gettext_toolkit.create_pot_from_compressed import main as create_pot_from_compressed
from df_gettext_toolkit.create_pot_from_plain_text import main as create_pot_from_plain_text
from df_gettext_toolkit.create_pot_from_raw_objects import main as create_pot_from_raw_objects
from df_gettext_toolkit.create_pot_from_speech import main as create_pot_from_speech


class Parameters(NamedTuple):
    function: Callable
    pot_file_name: str
    source_file_path: str


parameters = [
    Parameters(create_pot_from_raw_objects, "raws.pot", "raw/objects"),
    Parameters(create_pot_from_speech, "speech.pot", "data/speech"),
    Parameters(create_pot_from_plain_text, "text.pot", "raw/objects/text"),
    Parameters(create_pot_from_compressed, "uncompressed.pot", "data"),
]

app = typer.Typer()


@app.command()
def main(df_path: Path):
    for function, pot_file_name, source_file_path in parameters:
        with open(pot_file_name, "wt", encoding="utf-8") as pot_file:
            print(f"Creating {pot_file_name} from {df_path / source_file_path}")
            function(df_path / source_file_path, pot_file)
