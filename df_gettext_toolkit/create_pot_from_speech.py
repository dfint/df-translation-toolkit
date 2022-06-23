import sys
from pathlib import Path

import typer

from .parse_po import format_po_item


def main(path: Path):
    print("Path:", path, file=sys.stderr)

    for file_path in sorted(path.glob("*.txt")):
        if file_path.is_file():
            print("File:", file_path.name, file=sys.stderr)
            with open(file_path) as file:
                for i, line in enumerate(file, 1):
                    if line.rstrip("\n"):
                        print(
                            format_po_item(msgid=line.rstrip("\n"), file_name=file_path.name, line_number=i),
                            end="\n\n",
                        )


if __name__ == "__main__":
    typer.run(main)
