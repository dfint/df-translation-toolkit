from pathlib import Path

import jinja2
import typer


def generate_preview(template_text: str, title: str, description: str, destination_path: Path) -> None:
    template = jinja2.Template(template_text)
    result_svg = template.render(title=title, description=description)
    destination_path.write_text(result_svg)


def main(template_path: Path, title: str, description: str, destination_path: Path) -> None:
    with template_path.open() as template_file:
        template = template_file.read()
        generate_preview(template, title, description, destination_path)


if __name__ == "__main__":
    typer.run(main)
